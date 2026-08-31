from __future__ import annotations

from dataclasses import dataclass

import mne
import numpy as np
import torch
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, TensorDataset

from src.eeg.epochs import EPOCH_TMAX, EPOCH_TMIN
from src.eeg.loader import EXPECTED_CHANNEL_COUNT, EXPECTED_SAMPLING_FREQUENCY

CLASS_LABELS = ("left", "right")
LABEL_TO_INDEX = {label: index for index, label in enumerate(CLASS_LABELS)}
INPUT_CHANNELS = 1
TEMPORAL_FILTERS = 8
DEPTH_MULTIPLIER = 2
SEPARABLE_FILTERS = 16
TEMPORAL_KERNEL_LENGTH = 64
SEPARABLE_KERNEL_LENGTH = 16
FIRST_POOL_KERNEL = (1, 4)
FIRST_POOL_STRIDE = (1, 4)
SECOND_POOL_KERNEL = (1, 8)
SECOND_POOL_STRIDE = (1, 8)
DEPTHWISE_MAX_NORM = 1.0
DROPOUT_PROBABILITY = 0.5
LOGIT_COUNT = 2
LEARNING_RATE = 1e-3
WEIGHT_DECAY = 0.0
BATCH_SIZE = 32
MAX_EPOCHS = 200
EARLY_STOPPING_PATIENCE = 20
RANDOM_SEED = 42
TRAIN_PARTITION = "train"
VALIDATION_PARTITION = "validation"
TEST_PARTITIONS = ("test", "final_test")
LABEL_COLUMN = "semantic_label"
PARTITION_COLUMN = "partition"
DEFAULT_DEVICE = "cpu"


class EEGNetError(ValueError):
    """Raised when the approved EEGNet contract is violated."""


@dataclass(frozen=True)
class EpochMetrics:
    epoch_index: int
    train_loss: float
    validation_loss: float
    validation_balanced_accuracy: float


@dataclass(frozen=True)
class PartitionMetrics:
    partition_name: str
    sample_count: int
    loss: float
    accuracy: float
    balanced_accuracy: float


@dataclass(frozen=True)
class _PartitionPredictions:
    partition_name: str
    loss: float
    true_label_indices: np.ndarray
    predicted_label_indices: np.ndarray
    probabilities: np.ndarray


@dataclass(frozen=True)
class EEGNetTrainingResult:
    decoder: "EEGNetDecoder"
    selected_epoch_index: int
    best_validation_balanced_accuracy: float
    history: tuple[EpochMetrics, ...]
    partition_metrics: tuple[PartitionMetrics, ...]


class MaxNormConv2d(nn.Conv2d):
    def __init__(self, *args, max_norm_value: float, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.max_norm_value = float(max_norm_value)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        constrained_weight = self._constrained_weight()
        return F.conv2d(
            inputs,
            constrained_weight,
            self.bias,
            self.stride,
            self.padding,
            self.dilation,
            self.groups,
        )

    def _constrained_weight(self) -> torch.Tensor:
        flattened = self.weight.view(self.weight.shape[0], -1)
        norms = flattened.norm(p=2, dim=1, keepdim=True).clamp_min(1e-12)
        scale = torch.clamp(self.max_norm_value / norms, max=1.0)
        return (flattened * scale).view_as(self.weight)


class EEGNetModel(nn.Module):
    def __init__(self, *, n_times: int) -> None:
        super().__init__()
        self.n_times = int(n_times)
        self.temporal_conv = nn.Conv2d(
            INPUT_CHANNELS,
            TEMPORAL_FILTERS,
            kernel_size=(1, TEMPORAL_KERNEL_LENGTH),
            padding="same",
            bias=False,
        )
        self.temporal_batch_norm = nn.BatchNorm2d(TEMPORAL_FILTERS)
        self.depthwise_spatial_conv = MaxNormConv2d(
            TEMPORAL_FILTERS,
            TEMPORAL_FILTERS * DEPTH_MULTIPLIER,
            kernel_size=(EXPECTED_CHANNEL_COUNT, 1),
            groups=TEMPORAL_FILTERS,
            bias=False,
            max_norm_value=DEPTHWISE_MAX_NORM,
        )
        self.depthwise_batch_norm = nn.BatchNorm2d(TEMPORAL_FILTERS * DEPTH_MULTIPLIER)
        self.activation = nn.ELU()
        self.first_average_pool = nn.AvgPool2d(FIRST_POOL_KERNEL, stride=FIRST_POOL_STRIDE)
        self.first_dropout = nn.Dropout(p=DROPOUT_PROBABILITY)
        self.separable_depthwise_conv = nn.Conv2d(
            TEMPORAL_FILTERS * DEPTH_MULTIPLIER,
            TEMPORAL_FILTERS * DEPTH_MULTIPLIER,
            kernel_size=(1, SEPARABLE_KERNEL_LENGTH),
            padding="same",
            groups=TEMPORAL_FILTERS * DEPTH_MULTIPLIER,
            bias=False,
        )
        self.separable_pointwise_conv = nn.Conv2d(
            TEMPORAL_FILTERS * DEPTH_MULTIPLIER,
            SEPARABLE_FILTERS,
            kernel_size=(1, 1),
            bias=False,
        )
        self.separable_batch_norm = nn.BatchNorm2d(SEPARABLE_FILTERS)
        self.second_average_pool = nn.AvgPool2d(SECOND_POOL_KERNEL, stride=SECOND_POOL_STRIDE)
        self.second_dropout = nn.Dropout(p=DROPOUT_PROBABILITY)
        feature_count = self._infer_feature_count()
        self.classifier = nn.Linear(feature_count, LOGIT_COUNT)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        _validate_input_tensor(inputs, expected_n_times=self.n_times)
        features = self._forward_features(inputs)
        return self.classifier(features)

    def _forward_features(self, inputs: torch.Tensor) -> torch.Tensor:
        outputs = self.temporal_conv(inputs)
        outputs = self.temporal_batch_norm(outputs)
        outputs = self.depthwise_spatial_conv(outputs)
        outputs = self.depthwise_batch_norm(outputs)
        outputs = self.activation(outputs)
        outputs = self.first_average_pool(outputs)
        outputs = self.first_dropout(outputs)
        outputs = self.separable_depthwise_conv(outputs)
        outputs = self.separable_pointwise_conv(outputs)
        outputs = self.separable_batch_norm(outputs)
        outputs = self.activation(outputs)
        outputs = self.second_average_pool(outputs)
        outputs = self.second_dropout(outputs)
        return torch.flatten(outputs, start_dim=1)

    def _infer_feature_count(self) -> int:
        with torch.no_grad():
            sample = torch.zeros(
                1,
                INPUT_CHANNELS,
                EXPECTED_CHANNEL_COUNT,
                self.n_times,
                dtype=torch.float32,
            )
            return int(self._forward_features(sample).shape[1])


class EEGNetDecoder:
    def __init__(self, *, model: EEGNetModel, class_labels: tuple[str, ...] = CLASS_LABELS) -> None:
        self._model = model.eval()
        self.class_labels = class_labels

    def predict_logits(self, epochs: mne.Epochs) -> np.ndarray:
        inputs = _epochs_to_tensor(epochs)
        with torch.no_grad():
            logits = self._model(inputs)
        return logits.detach().cpu().numpy()

    def predict_proba(self, epochs: mne.Epochs) -> np.ndarray:
        logits = self.predict_logits(epochs)
        probabilities = torch.softmax(torch.from_numpy(logits), dim=1).numpy()
        if probabilities.shape[1] != len(self.class_labels):
            raise EEGNetError("Probability output does not match the learned class-label order.")
        return probabilities

    def predict(self, epochs: mne.Epochs) -> np.ndarray:
        probabilities = self.predict_proba(epochs)
        predicted_indices = probabilities.argmax(axis=1)
        return np.asarray([self.class_labels[index] for index in predicted_indices], dtype=object)


def fit_eegnet(
    epochs: mne.Epochs,
    *,
    partition_column: str = PARTITION_COLUMN,
    label_column: str = LABEL_COLUMN,
    device: str = DEFAULT_DEVICE,
) -> EEGNetTrainingResult:
    _validate_epochs_contract(epochs)
    metadata = _validated_partition_metadata(epochs, partition_column=partition_column, label_column=label_column)
    _set_random_seed(RANDOM_SEED)

    train_epochs = _select_partition_epochs(
        epochs,
        metadata=metadata,
        partition_name=TRAIN_PARTITION,
        partition_column=partition_column,
    )
    validation_epochs = _select_partition_epochs(
        epochs,
        metadata=metadata,
        partition_name=VALIDATION_PARTITION,
        partition_column=partition_column,
    )

    torch_device = torch.device(device)
    model = EEGNetModel(n_times=len(epochs.times)).to(torch_device)
    loss_function = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)

    train_loader = _build_data_loader(
        train_epochs,
        label_column=label_column,
        partition_name=TRAIN_PARTITION,
        shuffle=True,
    )
    validation_loader = _build_data_loader(
        validation_epochs,
        label_column=label_column,
        partition_name=VALIDATION_PARTITION,
        shuffle=False,
    )

    history: list[EpochMetrics] = []
    best_state: dict[str, torch.Tensor] | None = None
    best_validation_score = float("-inf")
    best_epoch_index = 0
    epochs_without_improvement = 0

    for epoch_index in range(1, MAX_EPOCHS + 1):
        train_loss = _run_training_epoch(
            model,
            loader=train_loader,
            optimizer=optimizer,
            loss_function=loss_function,
            device=torch_device,
        )
        validation_predictions = _evaluate_partition(
            model,
            loader=validation_loader,
            loss_function=loss_function,
            device=torch_device,
            partition_name=VALIDATION_PARTITION,
        )
        validation_score = float(
            balanced_accuracy_score(
                validation_predictions.true_label_indices,
                validation_predictions.predicted_label_indices,
            )
        )
        history.append(
            EpochMetrics(
                epoch_index=epoch_index,
                train_loss=train_loss,
                validation_loss=validation_predictions.loss,
                validation_balanced_accuracy=validation_score,
            )
        )
        if validation_score > best_validation_score:
            best_validation_score = validation_score
            best_epoch_index = epoch_index
            best_state = _clone_state_dict(model.state_dict())
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
        if epochs_without_improvement >= EARLY_STOPPING_PATIENCE:
            break

    if best_state is None:
        raise EEGNetError("No EEGNet checkpoint was selected from validation performance.")

    model.load_state_dict(best_state)
    decoder = EEGNetDecoder(model=model)
    partition_metrics = _evaluate_frozen_partitions(
        decoder,
        epochs,
        metadata=metadata,
        label_column=label_column,
        partition_column=partition_column,
        device=torch_device,
    )
    return EEGNetTrainingResult(
        decoder=decoder,
        selected_epoch_index=best_epoch_index,
        best_validation_balanced_accuracy=best_validation_score,
        history=tuple(history),
        partition_metrics=tuple(partition_metrics),
    )


def _evaluate_frozen_partitions(
    decoder: EEGNetDecoder,
    epochs: mne.Epochs,
    *,
    metadata,
    label_column: str,
    partition_column: str,
    device: torch.device,
) -> list[PartitionMetrics]:
    loss_function = nn.CrossEntropyLoss()
    metrics: list[PartitionMetrics] = []
    observed_partitions = set(metadata[partition_column].astype(str))

    for partition_name in (VALIDATION_PARTITION,) + TEST_PARTITIONS:
        if partition_name not in observed_partitions:
            continue
        partition_epochs = _select_partition_epochs(
            epochs,
            metadata=metadata,
            partition_name=partition_name,
            partition_column=partition_column,
        )
        loader = _build_data_loader(
            partition_epochs,
            label_column=label_column,
            partition_name=partition_name,
            shuffle=False,
        )
        predictions = _evaluate_partition(
            decoder._model,
            loader=loader,
            loss_function=loss_function,
            device=device,
            partition_name=partition_name,
        )
        metrics.append(
            PartitionMetrics(
                partition_name=partition_name,
                sample_count=int(len(predictions.true_label_indices)),
                loss=float(predictions.loss),
                accuracy=float(
                    accuracy_score(
                        predictions.true_label_indices,
                        predictions.predicted_label_indices,
                    )
                ),
                balanced_accuracy=float(
                    balanced_accuracy_score(
                        predictions.true_label_indices,
                        predictions.predicted_label_indices,
                    )
                ),
            )
        )
    return metrics


def _build_data_loader(
    epochs: mne.Epochs,
    *,
    label_column: str,
    partition_name: str,
    shuffle: bool,
) -> DataLoader:
    inputs = _epochs_to_tensor(epochs)
    targets = _labels_to_tensor(epochs, label_column=label_column)
    dataset = TensorDataset(inputs, targets)
    if len(dataset) == 0:
        raise EEGNetError(f"Partition {partition_name!r} is empty.")
    generator = None
    if shuffle:
        generator = torch.Generator()
        generator.manual_seed(RANDOM_SEED)
    return DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=shuffle,
        generator=generator,
    )


def _run_training_epoch(
    model: EEGNetModel,
    *,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    loss_function: nn.Module,
    device: torch.device,
) -> float:
    model.train()
    batch_losses: list[float] = []
    for inputs, targets in loader:
        inputs = inputs.to(device)
        targets = targets.to(device)
        optimizer.zero_grad(set_to_none=True)
        logits = model(inputs)
        loss = loss_function(logits, targets)
        loss.backward()
        optimizer.step()
        batch_losses.append(float(loss.detach().cpu().item()))
    if not batch_losses:
        raise EEGNetError("Training loader did not yield any batches.")
    return float(np.mean(batch_losses))


def _evaluate_partition(
    model: EEGNetModel,
    *,
    loader: DataLoader,
    loss_function: nn.Module,
    device: torch.device,
    partition_name: str,
) -> _PartitionPredictions:
    model.eval()
    losses: list[float] = []
    probabilities: list[np.ndarray] = []
    true_label_indices: list[np.ndarray] = []
    predicted_label_indices: list[np.ndarray] = []

    with torch.no_grad():
        for inputs, targets in loader:
            inputs = inputs.to(device)
            targets = targets.to(device)
            logits = model(inputs)
            loss = loss_function(logits, targets)
            losses.append(float(loss.detach().cpu().item()))
            batch_probabilities = torch.softmax(logits, dim=1).detach().cpu().numpy()
            batch_predictions = batch_probabilities.argmax(axis=1)
            probabilities.append(batch_probabilities)
            predicted_label_indices.append(batch_predictions)
            true_label_indices.append(targets.detach().cpu().numpy())

    if not losses:
        raise EEGNetError(f"Partition {partition_name!r} did not yield any evaluation batches.")

    return _PartitionPredictions(
        partition_name=partition_name,
        loss=float(np.mean(losses)),
        true_label_indices=np.concatenate(true_label_indices, axis=0),
        predicted_label_indices=np.concatenate(predicted_label_indices, axis=0),
        probabilities=np.concatenate(probabilities, axis=0),
    )


def _epochs_to_tensor(epochs: mne.Epochs) -> torch.Tensor:
    _validate_epochs_contract(epochs)
    data = epochs.get_data(copy=True).astype(np.float32, copy=False)
    if not np.isfinite(data).all():
        raise EEGNetError("Epoch data contains non-finite values.")
    return torch.from_numpy(data).unsqueeze(1)


def _labels_to_tensor(epochs: mne.Epochs, *, label_column: str) -> torch.Tensor:
    if epochs.metadata is None or label_column not in epochs.metadata.columns:
        raise EEGNetError(f"Epoch metadata must include {label_column!r}.")
    labels = epochs.metadata[label_column].astype(str).tolist()
    invalid_labels = sorted(set(labels) - set(CLASS_LABELS))
    if invalid_labels:
        raise EEGNetError(
            "EEGNet only supports canonical binary left/right labels. "
            f"Found unsupported labels: {', '.join(invalid_labels)}."
        )
    indices = np.asarray([LABEL_TO_INDEX[label] for label in labels], dtype=np.int64)
    return torch.from_numpy(indices)


def _select_partition_epochs(
    epochs: mne.Epochs,
    *,
    metadata,
    partition_name: str,
    partition_column: str,
) -> mne.Epochs:
    indices = metadata.index[metadata[partition_column] == partition_name].tolist()
    if not indices:
        raise EEGNetError(f"Partition {partition_name!r} is empty.")
    return epochs[indices]


def _validated_partition_metadata(epochs: mne.Epochs, *, partition_column: str, label_column: str):
    if epochs.metadata is None:
        raise EEGNetError("Epoch metadata is required for partitioned EEGNet fitting.")
    metadata = epochs.metadata.reset_index(drop=True).copy()
    for column in (partition_column, label_column):
        if column not in metadata.columns:
            raise EEGNetError(f"Epoch metadata is missing required column {column!r}.")

    observed_labels = set(metadata[label_column].astype(str))
    invalid_labels = observed_labels - set(CLASS_LABELS)
    if invalid_labels:
        raise EEGNetError("EEGNet only supports canonical binary left/right labels.")

    observed_partitions = set(metadata[partition_column].astype(str))
    missing_partitions = {TRAIN_PARTITION, VALIDATION_PARTITION} - observed_partitions
    if missing_partitions:
        raise EEGNetError(
            "Epoch metadata is missing required partition(s): "
            + ", ".join(sorted(missing_partitions))
            + "."
        )

    for partition_name in (TRAIN_PARTITION, VALIDATION_PARTITION):
        partition_labels = set(
            metadata.loc[metadata[partition_column] == partition_name, label_column].astype(str)
        )
        if partition_labels != set(CLASS_LABELS):
            raise EEGNetError(
                f"Partition {partition_name!r} must contain both approved labels left and right."
            )
    return metadata


def _validate_epochs_contract(epochs: mne.Epochs) -> None:
    if len(epochs.ch_names) != EXPECTED_CHANNEL_COUNT:
        raise EEGNetError(
            f"EEGNet expects the approved {EXPECTED_CHANNEL_COUNT}-channel epoch representation."
        )
    if float(epochs.info["sfreq"]) != EXPECTED_SAMPLING_FREQUENCY:
        raise EEGNetError(
            f"EEGNet expects the approved native {EXPECTED_SAMPLING_FREQUENCY} Hz sampling rate."
        )
    if epochs.tmin != EPOCH_TMIN or epochs.tmax != EPOCH_TMAX:
        raise EEGNetError(
            "EEGNet expects canonical M1-T03 epochs spanning -1.0 s to +4.0 s with no CSP-only crop."
        )
    expected_n_times = int(round((EPOCH_TMAX - EPOCH_TMIN) * EXPECTED_SAMPLING_FREQUENCY)) + 1
    if len(epochs.times) != expected_n_times:
        raise EEGNetError(
            f"EEGNet expects {expected_n_times} time samples for canonical M1-T03 epochs."
        )


def _validate_input_tensor(inputs: torch.Tensor, *, expected_n_times: int) -> None:
    expected_shape = (INPUT_CHANNELS, EXPECTED_CHANNEL_COUNT, expected_n_times)
    if inputs.ndim != 4:
        raise EEGNetError("EEGNet expects a 4D tensor shaped batch × 1 × 64 × time.")
    if tuple(inputs.shape[1:]) != expected_shape:
        raise EEGNetError(
            "EEGNet expects input tensors shaped batch × 1 × 64 × time "
            f"with time={expected_n_times}. Received {tuple(inputs.shape)}."
        )


def _clone_state_dict(state_dict: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
    return {name: tensor.detach().cpu().clone() for name, tensor in state_dict.items()}


def _set_random_seed(seed: int) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)

