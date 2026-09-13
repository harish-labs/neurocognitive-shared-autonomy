"""Frozen D-078 binary evidence perturbations with auditable selection provenance."""

from __future__ import annotations

from dataclasses import dataclass
from math import floor
from typing import Sequence

import numpy as np

R1_SEVERITIES = (0.0, 0.25, 0.5, 0.75, 1.0)
R2_SEVERITIES = (0.0, 0.1, 0.2, 0.3, 0.4)


class RobustnessError(ValueError):
    """Raised when a D-078 perturbation request is malformed."""


@dataclass(frozen=True)
class PerturbationResult:
    family: str
    severity: float
    requested_q: float | None
    seed: int | None
    selection_rule: str
    selected_indices: tuple[int, ...]
    observation_ids: tuple[str, ...]
    selected_observation_ids: tuple[str, ...]
    population_size: int
    realized_count: int
    original_evidence: tuple[tuple[float, float], ...]
    perturbed_evidence: tuple[tuple[float, float], ...]
    realized_fraction: float


def flatten_evidence(evidence: np.ndarray, epsilon: float) -> PerturbationResult:
    values = _validate_evidence(evidence)
    severity = _validated_severity(epsilon, R1_SEVERITIES, "epsilon")
    perturbed = (1.0 - severity) * values + severity * np.asarray((0.5, 0.5))
    identities = _validated_observation_ids(None, len(values))
    return _result(
        "R1_EVIDENCE_FLATTENING",
        severity,
        None,
        None,
        "all_indices_formula",
        tuple(range(len(values))),
        identities,
        values,
        perturbed,
    )


def contaminate_contradictory_evidence(
    evidence: np.ndarray,
    fraction: float,
    *,
    seed: int,
    observation_ids: Sequence[str] | None = None,
) -> PerturbationResult:
    values = _validate_evidence(evidence)
    severity = _validated_severity(fraction, R2_SEVERITIES, "q")
    if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)) or int(seed) < 0:
        raise RobustnessError("seed must be a non-negative integer.")
    identities = _validated_observation_ids(observation_ids, len(values))
    # Nearest-integer count, with half rounded upward, is recorded explicitly so
    # finite evaluation populations remain auditable rather than implying q*N is exact.
    selected_count = floor(severity * len(values) + 0.5)
    generator = np.random.default_rng(int(seed))
    selected = tuple(sorted(int(index) for index in generator.permutation(len(values))[:selected_count]))
    perturbed = values.copy()
    if selected:
        perturbed[list(selected)] = perturbed[list(selected), ::-1]
    return _result(
        "R2_CONTRADICTORY_EVIDENCE",
        severity,
        severity,
        int(seed),
        "ordered_population_numpy_default_rng_permutation_nearest_integer_half_up",
        selected,
        identities,
        values,
        perturbed,
    )


def _validate_evidence(evidence: object) -> np.ndarray:
    values = np.asarray(evidence, dtype=np.float64)
    if values.ndim != 2 or values.shape[1] != 2 or len(values) == 0:
        raise RobustnessError("Evidence must have shape (n_observations, 2) and be non-empty.")
    if not np.isfinite(values).all() or (values < 0.0).any() or (values > 1.0).any():
        raise RobustnessError("Evidence probabilities must be finite and within [0, 1].")
    if not np.allclose(values.sum(axis=1), 1.0, rtol=0.0, atol=1e-8):
        raise RobustnessError("Each evidence row must sum to one.")
    return values


def _validated_severity(value: object, allowed: tuple[float, ...], name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise RobustnessError(f"{name} must be one of the frozen D-078 levels.")
    normalized = float(value)
    if normalized not in allowed:
        raise RobustnessError(f"{name} must be one of {allowed}.")
    return normalized


def _validated_observation_ids(values: Sequence[str] | None, population_size: int) -> tuple[str, ...]:
    if values is None:
        return tuple(f"observation-{index:08d}" for index in range(population_size))
    identities = tuple(values)
    if len(identities) != population_size:
        raise RobustnessError("observation_ids must align one-to-one with the evidence population.")
    if any(not isinstance(value, str) or not value for value in identities):
        raise RobustnessError("observation_ids must contain non-empty strings.")
    if len(set(identities)) != len(identities):
        raise RobustnessError("observation_ids must be unique across the evidence population.")
    return identities


def _result(
    family: str,
    severity: float,
    requested_q: float | None,
    seed: int | None,
    rule: str,
    selected: tuple[int, ...],
    observation_ids: tuple[str, ...],
    original: np.ndarray,
    perturbed: np.ndarray,
) -> PerturbationResult:
    return PerturbationResult(
        family=family,
        severity=severity,
        requested_q=requested_q,
        seed=seed,
        selection_rule=rule,
        selected_indices=selected,
        observation_ids=observation_ids,
        selected_observation_ids=tuple(observation_ids[index] for index in selected),
        population_size=len(original),
        realized_count=len(selected),
        original_evidence=tuple(tuple(float(item) for item in row) for row in original),
        perturbed_evidence=tuple(tuple(float(item) for item in row) for row in perturbed),
        realized_fraction=len(selected) / len(original),
    )
