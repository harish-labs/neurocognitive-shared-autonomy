"""Deterministic EEG and D-050 calibration metrics with explicit denominators."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.models.calibration import APPROVED_CLASS_LABELS, CalibrationMetrics, evaluate_calibration


class MetricError(ValueError):
    """Raised when metric inputs are malformed or scientifically ambiguous."""


@dataclass(frozen=True)
class ClassMetric:
    class_name: str
    true_count: int
    predicted_count: int
    true_positive: int
    precision: float | None
    recall: float | None
    f1: float | None


@dataclass(frozen=True)
class ClassificationMetrics:
    evaluation_unit: str
    class_names: tuple[str, str]
    sample_count: int
    correct_count: int
    accuracy: float
    balanced_accuracy: float | None
    per_class: tuple[ClassMetric, ClassMetric]
    macro_f1: float | None
    confusion_matrix: tuple[tuple[int, int], tuple[int, int]]


def classification_metrics(
    true_labels: list[str] | tuple[str, ...] | np.ndarray,
    predicted_labels: list[str] | tuple[str, ...] | np.ndarray,
    *,
    class_names: tuple[str, str] = APPROVED_CLASS_LABELS,
    evaluation_unit: str = "eeg_trial",
) -> ClassificationMetrics:
    _validate_class_names(class_names)
    truth = _label_indices(true_labels, class_names)
    predictions = _label_indices(predicted_labels, class_names)
    if truth.size == 0:
        raise MetricError("At least one EEG trial is required.")
    if truth.shape != predictions.shape:
        raise MetricError("True and predicted labels must have equal length.")
    if not isinstance(evaluation_unit, str) or not evaluation_unit:
        raise MetricError("evaluation_unit must be a non-empty string.")

    matrix = np.zeros((2, 2), dtype=np.int64)
    for true_index, predicted_index in zip(truth, predictions):
        matrix[true_index, predicted_index] += 1
    class_metrics: list[ClassMetric] = []
    recalls: list[float] = []
    f1_values: list[float] = []
    for index, name in enumerate(class_names):
        true_positive = int(matrix[index, index])
        true_count = int(matrix[index, :].sum())
        predicted_count = int(matrix[:, index].sum())
        precision = true_positive / predicted_count if predicted_count else None
        recall = true_positive / true_count if true_count else None
        if recall is not None:
            recalls.append(recall)
        f1 = None if precision is None or recall is None or precision + recall == 0 else 2 * precision * recall / (precision + recall)
        if f1 is not None:
            f1_values.append(f1)
        class_metrics.append(ClassMetric(name, true_count, predicted_count, true_positive, precision, recall, f1))

    correct = int(np.trace(matrix))
    return ClassificationMetrics(
        evaluation_unit=evaluation_unit,
        class_names=class_names,
        sample_count=int(truth.size),
        correct_count=correct,
        accuracy=correct / int(truth.size),
        balanced_accuracy=float(np.mean(recalls)) if len(recalls) == 2 else None,
        per_class=(class_metrics[0], class_metrics[1]),
        macro_f1=float(np.mean(f1_values)) if len(f1_values) == 2 else None,
        confusion_matrix=((int(matrix[0, 0]), int(matrix[0, 1])), (int(matrix[1, 0]), int(matrix[1, 1]))),
    )


def calibration_metrics(
    probabilities: np.ndarray,
    true_labels: list[str] | tuple[str, ...] | np.ndarray,
    *,
    class_names: tuple[str, str] = APPROVED_CLASS_LABELS,
) -> CalibrationMetrics:
    """Reuse the accepted D-050 implementation (10 equal-width bins and binary Brier)."""
    _validate_class_names(class_names)
    if np.asarray(probabilities).ndim != 2 or len(np.asarray(probabilities)) == 0:
        raise MetricError("Calibration evaluation requires at least one probability row.")
    try:
        return evaluate_calibration(probabilities, true_labels, class_labels=class_names)
    except ValueError as exc:
        raise MetricError(str(exc)) from exc


def _validate_class_names(class_names: tuple[str, str]) -> None:
    if tuple(class_names) != APPROVED_CLASS_LABELS:
        raise MetricError("Metrics must preserve approved class order ('left', 'right').")


def _label_indices(labels: object, class_names: tuple[str, str]) -> np.ndarray:
    array = np.asarray(labels, dtype=object)
    if array.ndim != 1:
        raise MetricError("Labels must be a one-dimensional sequence.")
    mapping = {name: index for index, name in enumerate(class_names)}
    try:
        return np.asarray([mapping[str(label)] for label in array], dtype=np.int64)
    except KeyError as exc:
        raise MetricError(f"Unsupported label {exc.args[0]!r}.") from exc
