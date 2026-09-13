"""D-079 paired subject-level inference without pseudo-replication."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np

BOOTSTRAP_RESAMPLES = 10_000
ALPHA = 0.05
EXACT_SIGN_FLIP_MAX_SUBJECTS = 17


class StatisticsError(ValueError):
    """Raised when paired subject-level inference inputs are invalid."""


@dataclass(frozen=True)
class SubjectMetric:
    subject_key: str
    value: float
    contributing_observations: int
    evaluation_unit: str = "subject"


@dataclass(frozen=True)
class ObservationMetric:
    subject_key: str
    observation_id: str
    value: float


def aggregate_subject_means(
    observations: list[ObservationMetric] | tuple[ObservationMetric, ...],
) -> tuple[SubjectMetric, ...]:
    """Collapse lower-level observations to exactly one equally weighted value per subject."""
    if not observations:
        raise StatisticsError("Subject aggregation requires at least one observation.")
    grouped: dict[str, list[float]] = {}
    seen_observation_ids: set[str] = set()
    for observation in observations:
        if not isinstance(observation, ObservationMetric):
            raise StatisticsError("Subject aggregation accepts only ObservationMetric values.")
        if not observation.subject_key or not observation.observation_id:
            raise StatisticsError("Subject and observation identities must be non-empty.")
        if observation.observation_id in seen_observation_ids:
            raise StatisticsError("observation_id values must be globally unique.")
        if not np.isfinite(observation.value):
            raise StatisticsError("Observation metric values must be finite.")
        seen_observation_ids.add(observation.observation_id)
        grouped.setdefault(observation.subject_key, []).append(float(observation.value))
    return tuple(
        SubjectMetric(subject_key, float(np.mean(values)), len(values))
        for subject_key, values in sorted(grouped.items())
    )


@dataclass(frozen=True)
class PairedInferenceResult:
    evaluation_unit: str
    subject_count: int
    subject_keys: tuple[str, ...]
    condition_a_values: tuple[float, ...]
    condition_b_values: tuple[float, ...]
    paired_differences_b_minus_a: tuple[float, ...]
    raw_effect_mean_difference: float
    confidence_level: float
    bootstrap_resamples: int
    bootstrap_seed: int
    ci_lower: float
    ci_upper: float
    permutation_method: str
    permutation_assignments: int
    permutation_seed: int | None
    raw_p_value: float


def paired_subject_inference(
    condition_a: list[SubjectMetric] | tuple[SubjectMetric, ...],
    condition_b: list[SubjectMetric] | tuple[SubjectMetric, ...],
    *,
    bootstrap_seed: int,
    permutation_seed: int | None = None,
    permutation_samples: int | None = None,
) -> PairedInferenceResult:
    first = _subject_mapping(condition_a, "condition_a")
    second = _subject_mapping(condition_b, "condition_b")
    if first.keys() != second.keys():
        raise StatisticsError("Paired conditions must contain exactly the same subject keys.")
    keys = tuple(sorted(first))
    a_values = np.asarray([first[key] for key in keys], dtype=np.float64)
    b_values = np.asarray([second[key] for key in keys], dtype=np.float64)
    differences = b_values - a_values
    bootstrap_seed = _seed(bootstrap_seed, "bootstrap_seed")
    generator = np.random.default_rng(bootstrap_seed)
    indices = generator.integers(0, len(keys), size=(BOOTSTRAP_RESAMPLES, len(keys)))
    bootstrap_effects = differences[indices].mean(axis=1)
    ci_lower, ci_upper = np.quantile(bootstrap_effects, (ALPHA / 2, 1 - ALPHA / 2))

    observed = abs(float(differences.mean()))
    if len(keys) <= EXACT_SIGN_FLIP_MAX_SUBJECTS:
        null = np.fromiter(
            (abs(float(np.mean(differences * np.asarray(signs)))) for signs in product((-1.0, 1.0), repeat=len(keys))),
            dtype=np.float64,
            count=2 ** len(keys),
        )
        p_value = float(np.mean(null >= observed - 1e-15))
        method = "exact_paired_sign_flip"
        assignments = 2 ** len(keys)
        used_permutation_seed = None
    else:
        if isinstance(permutation_samples, bool) or not isinstance(permutation_samples, int) or permutation_samples <= 0:
            raise StatisticsError("More than 17 subjects requires an explicit positive permutation_samples value.")
        used_permutation_seed = _seed(permutation_seed, "permutation_seed")
        permutation_generator = np.random.default_rng(used_permutation_seed)
        signs = permutation_generator.choice((-1.0, 1.0), size=(permutation_samples, len(keys)))
        null = np.abs((signs * differences).mean(axis=1))
        p_value = float((np.count_nonzero(null >= observed - 1e-15) + 1) / (permutation_samples + 1))
        method = "monte_carlo_paired_sign_flip"
        assignments = permutation_samples

    return PairedInferenceResult(
        evaluation_unit="subject",
        subject_count=len(keys),
        subject_keys=keys,
        condition_a_values=tuple(float(value) for value in a_values),
        condition_b_values=tuple(float(value) for value in b_values),
        paired_differences_b_minus_a=tuple(float(value) for value in differences),
        raw_effect_mean_difference=float(differences.mean()),
        confidence_level=0.95,
        bootstrap_resamples=BOOTSTRAP_RESAMPLES,
        bootstrap_seed=bootstrap_seed,
        ci_lower=float(ci_lower),
        ci_upper=float(ci_upper),
        permutation_method=method,
        permutation_assignments=assignments,
        permutation_seed=used_permutation_seed,
        raw_p_value=p_value,
    )


def holm_adjust(p_values: dict[str, float]) -> dict[str, float]:
    if not p_values:
        raise StatisticsError("Holm correction requires at least one named test.")
    for name, value in p_values.items():
        if not isinstance(name, str) or not name or not np.isfinite(value) or not 0.0 <= value <= 1.0:
            raise StatisticsError("Holm inputs require unique non-empty names and finite p-values within [0, 1].")
    ordered = sorted(p_values.items(), key=lambda item: (item[1], item[0]))
    adjusted: dict[str, float] = {}
    running = 0.0
    total = len(ordered)
    for rank, (name, value) in enumerate(ordered):
        running = max(running, (total - rank) * value)
        adjusted[name] = min(1.0, running)
    return {name: adjusted[name] for name in p_values}


def _subject_mapping(records: object, label: str) -> dict[str, float]:
    if not isinstance(records, (list, tuple)) or not records:
        raise StatisticsError(f"{label} requires a non-empty subject-level sequence.")
    result: dict[str, float] = {}
    for record in records:
        if not isinstance(record, SubjectMetric) or record.evaluation_unit != "subject":
            raise StatisticsError("Primary inference accepts only SubjectMetric records with evaluation_unit='subject'.")
        if not record.subject_key or record.subject_key in result:
            raise StatisticsError("Each subject may occur exactly once per condition; pseudo-replication is forbidden.")
        if (
            not np.isfinite(record.value)
            or isinstance(record.contributing_observations, bool)
            or not isinstance(record.contributing_observations, int)
            or record.contributing_observations <= 0
        ):
            raise StatisticsError("Subject metrics require a finite value and positive contributing-observation count.")
        result[record.subject_key] = float(record.value)
    return result


def _seed(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or int(value) < 0:
        raise StatisticsError(f"{name} must be a non-negative integer.")
    return int(value)
