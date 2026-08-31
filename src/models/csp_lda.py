from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import mne
import numpy as np
from mne.decoding import CSP
from sklearn.metrics import balanced_accuracy_score
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from src.eeg.epochs import EPOCH_TMIN, EPOCH_TMAX
from src.eeg.loader import EXPECTED_CHANNEL_COUNT

APPROVED_CSP_COMPONENT_CANDIDATES = (2, 4, 6, 8)
DEFAULT_CSP_COMPONENT = 4
APPROVED_CSP_REGULARIZATION = None
CSP_CROP_TMIN = 1.0
CSP_CROP_TMAX = 2.0
TRAIN_PARTITION = "train"
VALIDATION_PARTITION = "validation"
TEST_PARTITIONS = ("test", "final_test")
LABEL_COLUMN = "semantic_label"
PARTITION_COLUMN = "partition"


class CspLdaError(ValueError):
    """Raised when the governed CSP+LDA baseline contract is violated."""


@dataclass(frozen=True)
class CandidateScore:
    n_components: int
    validation_balanced_accuracy: float


@dataclass(frozen=True)
class CspLdaTrainingResult:
    decoder: "CspLdaDecoder"
    selected_n_components: int
    candidate_scores: tuple[CandidateScore, ...]


class CspLdaDecoder:
    def __init__(
        self,
        *,
        csp: CSP,
        lda: LinearDiscriminantAnalysis,
        class_labels: tuple[str, ...],
    ) -> None:
        self._csp = csp
        self._lda = lda
        self.class_labels = class_labels

    def predict(self, epochs: mne.Epochs) -> np.ndarray:
        features = self._transform_features(epochs)
        return self._lda.predict(features)

    def predict_proba(self, epochs: mne.Epochs) -> np.ndarray:
        features = self._transform_features(epochs)
        probabilities = self._lda.predict_proba(features)
        if probabilities.shape[1] != len(self.class_labels):
            raise CspLdaError("Probability output does not match the learned class-label order.")
        return probabilities

    def _transform_features(self, epochs: mne.Epochs) -> np.ndarray:
        cropped = crop_epochs_for_csp(epochs)
        return self._csp.transform(cropped.get_data(copy=True))


def crop_epochs_for_csp(epochs: mne.Epochs) -> mne.Epochs:
    _validate_epochs_contract(epochs)
    cropped = epochs.copy().crop(tmin=CSP_CROP_TMIN, tmax=CSP_CROP_TMAX)
    if cropped.tmin != CSP_CROP_TMIN or cropped.tmax != CSP_CROP_TMAX:
        raise CspLdaError("CSP crop did not preserve the approved +1.0 s to +2.0 s window.")
    return cropped


def fit_csp_lda(
    epochs: mne.Epochs,
    *,
    partition_column: str = PARTITION_COLUMN,
    label_column: str = LABEL_COLUMN,
    component_candidates: Iterable[int] = APPROVED_CSP_COMPONENT_CANDIDATES,
    covariance_regularization: str | float | None = APPROVED_CSP_REGULARIZATION,
) -> CspLdaTrainingResult:
    _validate_epochs_contract(epochs)
    metadata = _validated_partition_metadata(epochs, partition_column=partition_column, label_column=label_column)
    ordered_candidates = _normalize_component_candidates(component_candidates)
    if covariance_regularization is not APPROVED_CSP_REGULARIZATION:
        raise CspLdaError("M1-T05 only authorizes reg=None for the primary CSP+LDA baseline.")

    candidate_scores: list[CandidateScore] = []
    best_candidate: int | None = None
    best_score = float("-inf")
    for n_components in ordered_candidates:
        candidate_decoder = _fit_decoder_for_candidate(
            epochs,
            metadata=metadata,
            n_components=n_components,
            label_column=label_column,
            partition_column=partition_column,
            covariance_regularization=covariance_regularization,
        )
        validation_score = _score_decoder_on_partition(
            candidate_decoder,
            epochs,
            metadata=metadata,
            partition_name=VALIDATION_PARTITION,
            label_column=label_column,
            partition_column=partition_column,
        )
        candidate_scores.append(
            CandidateScore(
                n_components=n_components,
                validation_balanced_accuracy=validation_score,
            )
        )
        if validation_score > best_score:
            best_score = validation_score
    best_candidates = tuple(
        score.n_components for score in candidate_scores if score.validation_balanced_accuracy == best_score
    )
    best_candidate = _select_best_candidate(best_candidates)

    if best_candidate is None:
        raise CspLdaError("No approved CSP candidate could be selected.")

    final_decoder = _fit_decoder_for_candidate(
        epochs,
        metadata=metadata,
        n_components=best_candidate,
        label_column=label_column,
        partition_column=partition_column,
        covariance_regularization=covariance_regularization,
    )
    return CspLdaTrainingResult(
        decoder=final_decoder,
        selected_n_components=best_candidate,
        candidate_scores=tuple(candidate_scores),
    )


def _fit_decoder_for_candidate(
    epochs: mne.Epochs,
    *,
    metadata,
    n_components: int,
    label_column: str,
    partition_column: str,
    covariance_regularization: str | float | None,
) -> CspLdaDecoder:
    train_epochs = _select_partition_epochs(
        epochs,
        metadata=metadata,
        partition_name=TRAIN_PARTITION,
        partition_column=partition_column,
    )
    train_labels = _labels_from_epochs(train_epochs, label_column=label_column)
    train_data = crop_epochs_for_csp(train_epochs).get_data(copy=True)

    csp = CSP(
        n_components=n_components,
        reg=covariance_regularization,
        log=True,
        norm_trace=False,
    )
    train_features = csp.fit_transform(train_data, train_labels)
    lda = LinearDiscriminantAnalysis()
    lda.fit(train_features, train_labels)
    return CspLdaDecoder(
        csp=csp,
        lda=lda,
        class_labels=tuple(str(label) for label in lda.classes_),
    )


def _score_decoder_on_partition(
    decoder: CspLdaDecoder,
    epochs: mne.Epochs,
    *,
    metadata,
    partition_name: str,
    label_column: str,
    partition_column: str,
) -> float:
    partition_epochs = _select_partition_epochs(
        epochs,
        metadata=metadata,
        partition_name=partition_name,
        partition_column=partition_column,
    )
    true_labels = _labels_from_epochs(partition_epochs, label_column=label_column)
    predicted = decoder.predict(partition_epochs)
    return float(balanced_accuracy_score(true_labels, predicted))


def _select_partition_epochs(
    epochs: mne.Epochs,
    *,
    metadata,
    partition_name: str,
    partition_column: str,
) -> mne.Epochs:
    indices = metadata.index[metadata[partition_column] == partition_name].tolist()
    if not indices:
        raise CspLdaError(f"Partition {partition_name!r} is empty.")
    return epochs[indices]


def _labels_from_epochs(epochs: mne.Epochs, *, label_column: str) -> np.ndarray:
    if epochs.metadata is None or label_column not in epochs.metadata.columns:
        raise CspLdaError(f"Epoch metadata must include {label_column!r}.")
    return epochs.metadata[label_column].astype(str).to_numpy()


def _validated_partition_metadata(epochs: mne.Epochs, *, partition_column: str, label_column: str):
    if epochs.metadata is None:
        raise CspLdaError("Epoch metadata is required for CSP+LDA partitioned fitting.")
    metadata = epochs.metadata.reset_index(drop=True).copy()
    for column in (partition_column, label_column):
        if column not in metadata.columns:
            raise CspLdaError(f"Epoch metadata is missing required column {column!r}.")

    if set(metadata[label_column].astype(str)) - {"left", "right"}:
        raise CspLdaError("CSP+LDA only supports canonical binary left/right labels.")

    required_partitions = {TRAIN_PARTITION, VALIDATION_PARTITION}
    observed_partitions = set(metadata[partition_column].astype(str))
    missing = required_partitions - observed_partitions
    if missing:
        raise CspLdaError(
            "Epoch metadata is missing required partition(s): "
            + ", ".join(sorted(missing))
            + "."
        )
    return metadata


def _normalize_component_candidates(component_candidates: Iterable[int]) -> tuple[int, ...]:
    normalized = tuple(int(value) for value in component_candidates)
    if not normalized:
        raise CspLdaError("At least one CSP component candidate is required.")
    normalized_set = set(normalized)
    approved_set = set(APPROVED_CSP_COMPONENT_CANDIDATES)
    invalid = normalized_set - approved_set
    if invalid:
        raise CspLdaError(
            "M1-T05 only authorizes CSP candidates from {2,4,6,8}. "
            f"Received unsupported candidate(s): {sorted(invalid)}."
        )
    if normalized_set != approved_set or len(normalized) != len(APPROVED_CSP_COMPONENT_CANDIDATES):
        raise CspLdaError(
            "M1-T05 requires evaluating the full approved CSP candidate set {2,4,6,8} exactly once."
        )
    return APPROVED_CSP_COMPONENT_CANDIDATES


def _select_best_candidate(best_candidates: Iterable[int]) -> int:
    normalized = tuple(sorted({int(candidate) for candidate in best_candidates}))
    if not normalized:
        raise CspLdaError("At least one best CSP candidate is required for tie-breaking.")
    if DEFAULT_CSP_COMPONENT in normalized:
        return DEFAULT_CSP_COMPONENT
    return normalized[0]


def _validate_epochs_contract(epochs: mne.Epochs) -> None:
    if len(epochs.ch_names) != EXPECTED_CHANNEL_COUNT:
        raise CspLdaError(
            f"CSP+LDA expects the approved {EXPECTED_CHANNEL_COUNT}-channel epoch representation."
        )
    if epochs.tmin != EPOCH_TMIN or epochs.tmax != EPOCH_TMAX:
        raise CspLdaError(
            "CSP+LDA expects canonical M1-T03 epochs spanning -1.0 s to +4.0 s before internal cropping."
        )
