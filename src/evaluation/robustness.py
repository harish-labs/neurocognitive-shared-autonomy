"""Frozen D-078 binary evidence perturbations with auditable selection provenance."""

from __future__ import annotations

from dataclasses import dataclass
from math import floor

import numpy as np

R1_SEVERITIES = (0.0, 0.25, 0.5, 0.75, 1.0)
R2_SEVERITIES = (0.0, 0.1, 0.2, 0.3, 0.4)


class RobustnessError(ValueError):
    """Raised when a D-078 perturbation request is malformed."""


@dataclass(frozen=True)
class PerturbationResult:
    family: str
    severity: float
    seed: int | None
    selection_rule: str
    selected_indices: tuple[int, ...]
    original_evidence: tuple[tuple[float, float], ...]
    perturbed_evidence: tuple[tuple[float, float], ...]
    realized_fraction: float


def flatten_evidence(evidence: np.ndarray, epsilon: float) -> PerturbationResult:
    values = _validate_evidence(evidence)
    severity = _validated_severity(epsilon, R1_SEVERITIES, "epsilon")
    perturbed = (1.0 - severity) * values + severity * np.asarray((0.5, 0.5))
    return _result("R1_EVIDENCE_FLATTENING", severity, None, "all_indices_formula", tuple(range(len(values))), values, perturbed)


def contaminate_contradictory_evidence(evidence: np.ndarray, fraction: float, *, seed: int) -> PerturbationResult:
    values = _validate_evidence(evidence)
    severity = _validated_severity(fraction, R2_SEVERITIES, "q")
    if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)) or int(seed) < 0:
        raise RobustnessError("seed must be a non-negative integer.")
    # Nearest-integer count, with half rounded upward, is recorded explicitly so
    # small development fixtures remain auditable rather than implying q*N is exact.
    selected_count = floor(severity * len(values) + 0.5)
    generator = np.random.default_rng(int(seed))
    selected = tuple(sorted(int(index) for index in generator.permutation(len(values))[:selected_count]))
    perturbed = values.copy()
    if selected:
        perturbed[list(selected)] = perturbed[list(selected), ::-1]
    return _result(
        "R2_CONTRADICTORY_EVIDENCE",
        severity,
        int(seed),
        "numpy_default_rng_permutation_nearest_integer_half_up",
        selected,
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


def _result(family: str, severity: float, seed: int | None, rule: str, selected: tuple[int, ...], original: np.ndarray, perturbed: np.ndarray) -> PerturbationResult:
    return PerturbationResult(
        family=family,
        severity=severity,
        seed=seed,
        selection_rule=rule,
        selected_indices=selected,
        original_evidence=tuple(tuple(float(item) for item in row) for row in original),
        perturbed_evidence=tuple(tuple(float(item) for item in row) for row in perturbed),
        realized_fraction=len(selected) / len(original),
    )
