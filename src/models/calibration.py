from __future__ import annotations

from dataclasses import dataclass

import mne
import numpy as np
import torch
from torch.nn import functional as F

APPROVED_CLASS_LABELS = ("left", "right")
TRAIN_PARTITION = "train"
VALIDATION_PARTITION = "validation"
PROTECTED_PARTITIONS = ("test", "final_test")
PARTITION_COLUMN = "partition"
LABEL_COLUMN = "semantic_label"
EEGNET_MODEL_FAMILY = "eegnet"
CSP_LDA_MODEL_FAMILY = "csp_lda"
IDENTITY_METHOD = "identity"
TEMPERATURE_SCALING_METHOD = "temperature_scaling"
PLATT_SCALING_METHOD = "platt_scaling"
ECE_BIN_COUNT = 10
ECE_BIN_EDGES = tuple(float(value) for value in np.linspace(0.0, 1.0, ECE_BIN_COUNT + 1))


class CalibrationError(ValueError):
    """Raised when approved calibration constraints are violated."""


@dataclass(frozen=True)
class ReliabilityBin:
    bin_index: int
    lower_bound: float
    upper_bound: float
    sample_count: int
    mean_confidence: float
    empirical_accuracy: float


@dataclass(frozen=True)
class CalibrationMetrics:
    class_labels: tuple[str, ...]
    positive_class_label: str
    bin_count: int
    reliability_bins: tuple[ReliabilityBin, ...]
    expected_calibration_error: float
    brier_score: float


@dataclass(frozen=True)
class IdentityCalibrator:
    model_family: str
    method: str = IDENTITY_METHOD
    class_labels: tuple[str, ...] = APPROVED_CLASS_LABELS

    def predict_proba(self, probabilities: np.ndarray) -> np.ndarray:
        validated = _validate_probabilities(probabilities, class_labels=self.class_labels)
        return _normalize_probabilities(validated)


@dataclass(frozen=True)
class TemperatureScalingCalibrator:
    temperature: float
    method: str = TEMPERATURE_SCALING_METHOD
    model_family: str = EEGNET_MODEL_FAMILY
    fit_partition: str = VALIDATION_PARTITION
    class_labels: tuple[str, ...] = APPROVED_CLASS_LABELS

    def predict_proba(self, logits: np.ndarray) -> np.ndarray:
        validated_logits = _validate_logits(logits, class_labels=self.class_labels)
        scaled = validated_logits / self.temperature
        return _softmax(scaled)


@dataclass(frozen=True)
class PlattScalingCalibrator:
    slope: float
    intercept: float
    method: str = PLATT_SCALING_METHOD
    model_family: str = CSP_LDA_MODEL_FAMILY
    fit_partition: str = VALIDATION_PARTITION
    class_labels: tuple[str, ...] = APPROVED_CLASS_LABELS

    def predict_proba(self, probabilities: np.ndarray) -> np.ndarray:
        validated = _validate_probabilities(probabilities, class_labels=self.class_labels)
        positive_probabilities = np.clip(validated[:, 1], 1e-6, 1.0 - 1e-6)
        scores = np.log(positive_probabilities / (1.0 - positive_probabilities))
        calibrated_positive = _sigmoid((self.slope * scores) + self.intercept)
        calibrated = np.column_stack([1.0 - calibrated_positive, calibrated_positive])
        return _normalize_probabilities(calibrated)


def build_identity_calibrator(*, model_family: str) -> IdentityCalibrator:
    _validate_model_family(model_family)
    return IdentityCalibrator(model_family=model_family)


def fit_model_specific_calibrator(
    *,
    model_family: str,
    decoder,
    epochs: mne.Epochs,
    partition_column: str = PARTITION_COLUMN,
    label_column: str = LABEL_COLUMN,
):
    normalized_model_family = _validate_model_family(model_family)
    if normalized_model_family == EEGNET_MODEL_FAMILY:
        return fit_eegnet_temperature_scaler(
            decoder,
            epochs,
            partition_column=partition_column,
            label_column=label_column,
        )
    return fit_csp_lda_platt_scaler(
        decoder,
        epochs,
        partition_column=partition_column,
        label_column=label_column,
    )


def fit_eegnet_temperature_scaler(
    decoder,
    epochs: mne.Epochs,
    *,
    partition_column: str = PARTITION_COLUMN,
    label_column: str = LABEL_COLUMN,
) -> TemperatureScalingCalibrator:
    metadata = _validated_partition_metadata(
        epochs,
        partition_column=partition_column,
        label_column=label_column,
    )
    validation_epochs = _select_partition_epochs(
        epochs,
        metadata=metadata,
        partition_name=VALIDATION_PARTITION,
        partition_column=partition_column,
    )
    logits = decoder.predict_logits(validation_epochs)
    label_indices = _labels_to_indices(validation_epochs.metadata[label_column].astype(str).tolist())
    return _fit_temperature_scaler(logits=logits, true_label_indices=label_indices)


def fit_csp_lda_platt_scaler(
    decoder,
    epochs: mne.Epochs,
    *,
    partition_column: str = PARTITION_COLUMN,
    label_column: str = LABEL_COLUMN,
) -> PlattScalingCalibrator:
    metadata = _validated_partition_metadata(
        epochs,
        partition_column=partition_column,
        label_column=label_column,
    )
    validation_epochs = _select_partition_epochs(
        epochs,
        metadata=metadata,
        partition_name=VALIDATION_PARTITION,
        partition_column=partition_column,
    )
    probabilities = decoder.predict_proba(validation_epochs)
    label_indices = _labels_to_indices(validation_epochs.metadata[label_column].astype(str).tolist())
    return _fit_platt_scaler(probabilities=probabilities, true_label_indices=label_indices)


def evaluate_calibration(
    probabilities: np.ndarray,
    true_labels: list[str] | tuple[str, ...] | np.ndarray,
    *,
    class_labels: tuple[str, ...] = APPROVED_CLASS_LABELS,
) -> CalibrationMetrics:
    validated_probabilities = _validate_probabilities(probabilities, class_labels=class_labels)
    label_indices = _labels_to_indices(true_labels, class_labels=class_labels)
    bins = compute_reliability_bins(validated_probabilities, label_indices, class_labels=class_labels)
    ece = float(
        sum(
            (reliability_bin.sample_count / len(label_indices))
            * abs(reliability_bin.empirical_accuracy - reliability_bin.mean_confidence)
            for reliability_bin in bins
        )
    )
    brier = brier_score(validated_probabilities, label_indices, class_labels=class_labels)
    return CalibrationMetrics(
        class_labels=class_labels,
        positive_class_label=class_labels[1],
        bin_count=ECE_BIN_COUNT,
        reliability_bins=bins,
        expected_calibration_error=ece,
        brier_score=brier,
    )


def compute_reliability_bins(
    probabilities: np.ndarray,
    true_label_indices: list[int] | tuple[int, ...] | np.ndarray,
    *,
    class_labels: tuple[str, ...] = APPROVED_CLASS_LABELS,
) -> tuple[ReliabilityBin, ...]:
    validated_probabilities = _validate_probabilities(probabilities, class_labels=class_labels)
    labels = np.asarray(true_label_indices, dtype=np.int64)
    if len(validated_probabilities) != len(labels):
        raise CalibrationError("Probability rows and true labels must have the same length.")

    confidences = validated_probabilities.max(axis=1)
    predicted_indices = validated_probabilities.argmax(axis=1)
    correctness = (predicted_indices == labels).astype(np.float64)
    bins: list[ReliabilityBin] = []

    for bin_index in range(ECE_BIN_COUNT):
        lower_bound = ECE_BIN_EDGES[bin_index]
        upper_bound = ECE_BIN_EDGES[bin_index + 1]
        if bin_index == ECE_BIN_COUNT - 1:
            mask = (confidences >= lower_bound) & (confidences <= upper_bound)
        else:
            mask = (confidences >= lower_bound) & (confidences < upper_bound)
        sample_count = int(mask.sum())
        if sample_count == 0:
            mean_confidence = 0.0
            empirical_accuracy = 0.0
        else:
            mean_confidence = float(confidences[mask].mean())
            empirical_accuracy = float(correctness[mask].mean())
        bins.append(
            ReliabilityBin(
                bin_index=bin_index,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
                sample_count=sample_count,
                mean_confidence=mean_confidence,
                empirical_accuracy=empirical_accuracy,
            )
        )
    return tuple(bins)


def brier_score(
    probabilities: np.ndarray,
    true_label_indices: list[int] | tuple[int, ...] | np.ndarray,
    *,
    class_labels: tuple[str, ...] = APPROVED_CLASS_LABELS,
) -> float:
    validated_probabilities = _validate_probabilities(probabilities, class_labels=class_labels)
    labels = np.asarray(true_label_indices, dtype=np.int64)
    if len(validated_probabilities) != len(labels):
        raise CalibrationError("Probability rows and true labels must have the same length.")

    positive_targets = (labels == 1).astype(np.float64)
    positive_probabilities = validated_probabilities[:, 1].astype(np.float64)
    return float(np.mean((positive_probabilities - positive_targets) ** 2))


def _fit_temperature_scaler(
    *,
    logits: np.ndarray,
    true_label_indices: np.ndarray,
) -> TemperatureScalingCalibrator:
    validated_logits = _validate_logits(logits, class_labels=APPROVED_CLASS_LABELS)
    labels = np.asarray(true_label_indices, dtype=np.int64)
    _validate_binary_label_indices(labels)

    logits_tensor = torch.tensor(validated_logits, dtype=torch.float64)
    labels_tensor = torch.tensor(labels, dtype=torch.int64)
    log_temperature = torch.nn.Parameter(torch.zeros(1, dtype=torch.float64))
    optimizer = torch.optim.LBFGS([log_temperature], lr=0.1, max_iter=100, line_search_fn="strong_wolfe")

    def closure() -> torch.Tensor:
        optimizer.zero_grad()
        temperature = torch.exp(log_temperature).clamp_min(1e-6)
        loss = F.cross_entropy(logits_tensor / temperature, labels_tensor)
        loss.backward()
        return loss

    optimizer.step(closure)
    temperature = float(torch.exp(log_temperature).item())
    if not np.isfinite(temperature) or temperature <= 0.0:
        raise CalibrationError("Temperature scaling produced an invalid temperature.")
    return TemperatureScalingCalibrator(temperature=temperature)


def _fit_platt_scaler(
    *,
    probabilities: np.ndarray,
    true_label_indices: np.ndarray,
) -> PlattScalingCalibrator:
    validated_probabilities = _validate_probabilities(probabilities, class_labels=APPROVED_CLASS_LABELS)
    labels = np.asarray(true_label_indices, dtype=np.int64)
    _validate_binary_label_indices(labels)

    positive_probabilities = np.clip(validated_probabilities[:, 1], 1e-6, 1.0 - 1e-6)
    scores = np.log(positive_probabilities / (1.0 - positive_probabilities))
    score_tensor = torch.tensor(scores, dtype=torch.float64)
    labels_tensor = torch.tensor(labels.astype(np.float64), dtype=torch.float64)
    slope = torch.nn.Parameter(torch.ones(1, dtype=torch.float64))
    intercept = torch.nn.Parameter(torch.zeros(1, dtype=torch.float64))
    optimizer = torch.optim.LBFGS([slope, intercept], lr=0.1, max_iter=100, line_search_fn="strong_wolfe")

    def closure() -> torch.Tensor:
        optimizer.zero_grad()
        logits = (slope * score_tensor) + intercept
        loss = F.binary_cross_entropy_with_logits(logits, labels_tensor)
        loss.backward()
        return loss

    optimizer.step(closure)
    fitted_slope = float(slope.item())
    fitted_intercept = float(intercept.item())
    if not np.isfinite(fitted_slope) or not np.isfinite(fitted_intercept):
        raise CalibrationError("Platt scaling produced invalid parameters.")
    return PlattScalingCalibrator(slope=fitted_slope, intercept=fitted_intercept)


def _validated_partition_metadata(
    epochs: mne.Epochs,
    *,
    partition_column: str,
    label_column: str,
):
    if epochs.metadata is None:
        raise CalibrationError("Epoch metadata is required for calibration fitting.")
    metadata = epochs.metadata.reset_index(drop=True).copy()
    for column in (partition_column, label_column):
        if column not in metadata.columns:
            raise CalibrationError(f"Epoch metadata is missing required column {column!r}.")

    observed_labels = set(metadata[label_column].astype(str))
    invalid_labels = observed_labels - set(APPROVED_CLASS_LABELS)
    if invalid_labels:
        raise CalibrationError(
            "Calibration only supports canonical binary left/right labels. "
            f"Found unsupported labels: {sorted(invalid_labels)}."
        )

    observed_partitions = set(metadata[partition_column].astype(str))
    missing = {TRAIN_PARTITION, VALIDATION_PARTITION} - observed_partitions
    if missing:
        raise CalibrationError(
            "Epoch metadata is missing required partition(s): " + ", ".join(sorted(missing)) + "."
        )
    return metadata


def _select_partition_epochs(
    epochs: mne.Epochs,
    *,
    metadata,
    partition_name: str,
    partition_column: str,
) -> mne.Epochs:
    indices = metadata.index[metadata[partition_column] == partition_name].tolist()
    if not indices:
        raise CalibrationError(f"Partition {partition_name!r} is empty.")
    return epochs[indices]


def _validate_model_family(model_family: str) -> str:
    normalized = str(model_family)
    if normalized not in {EEGNET_MODEL_FAMILY, CSP_LDA_MODEL_FAMILY}:
        raise CalibrationError(
            f"Unsupported model family {model_family!r}. Expected 'eegnet' or 'csp_lda'."
        )
    return normalized


def _labels_to_indices(
    true_labels: list[str] | tuple[str, ...] | np.ndarray,
    *,
    class_labels: tuple[str, ...] = APPROVED_CLASS_LABELS,
) -> np.ndarray:
    _validate_class_labels(class_labels)
    label_to_index = {label: index for index, label in enumerate(class_labels)}
    labels = np.asarray(true_labels, dtype=object)
    try:
        indices = np.asarray([label_to_index[str(label)] for label in labels], dtype=np.int64)
    except KeyError as exc:
        raise CalibrationError(f"Encountered unsupported class label {exc.args[0]!r}.") from exc
    return indices


def _validate_class_labels(class_labels: tuple[str, ...]) -> None:
    if tuple(class_labels) != APPROVED_CLASS_LABELS:
        raise CalibrationError("Calibration must preserve the approved class order ('left', 'right').")


def _validate_binary_label_indices(label_indices: np.ndarray) -> None:
    unique_indices = sorted(set(label_indices.tolist()))
    invalid = set(unique_indices) - {0, 1}
    if invalid:
        raise CalibrationError(f"Binary calibration received invalid label indices: {sorted(invalid)}.")
    if len(label_indices) == 0:
        raise CalibrationError("Calibration fitting requires at least one validation example.")


def _validate_probabilities(
    probabilities: np.ndarray,
    *,
    class_labels: tuple[str, ...],
) -> np.ndarray:
    _validate_class_labels(class_labels)
    array = np.asarray(probabilities, dtype=np.float64)
    if array.ndim != 2 or array.shape[1] != len(class_labels):
        raise CalibrationError("Probabilities must have shape (n_samples, 2).")
    if not np.isfinite(array).all():
        raise CalibrationError("Probabilities must be finite.")
    if (array < 0.0).any():
        raise CalibrationError("Probabilities must be non-negative.")
    row_sums = array.sum(axis=1)
    if (row_sums <= 0.0).any():
        raise CalibrationError("Probability rows must have positive total mass.")
    return array


def _validate_logits(
    logits: np.ndarray,
    *,
    class_labels: tuple[str, ...],
) -> np.ndarray:
    _validate_class_labels(class_labels)
    array = np.asarray(logits, dtype=np.float64)
    if array.ndim != 2 or array.shape[1] != len(class_labels):
        raise CalibrationError("Logits must have shape (n_samples, 2).")
    if not np.isfinite(array).all():
        raise CalibrationError("Logits must be finite.")
    return array


def _normalize_probabilities(probabilities: np.ndarray) -> np.ndarray:
    row_sums = probabilities.sum(axis=1, keepdims=True)
    normalized = probabilities / row_sums
    if not np.isfinite(normalized).all():
        raise CalibrationError("Probability normalization produced a non-finite value.")
    return normalized


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=1, keepdims=True)
    exponentiated = np.exp(shifted)
    return _normalize_probabilities(exponentiated)


def _sigmoid(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))
