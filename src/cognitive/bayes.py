"""Approved binary Bayesian goal inference for one decision episode at a time."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

APPROVED_CLASS_LABELS = ("left", "right")
INITIAL_PRIOR = (0.5, 0.5)
COMMITMENT_THRESHOLD = 0.90
MAX_EVIDENCE_UPDATES = 5


class BayesianGoalInferenceError(ValueError):
    """Raised when evidence or an episode violates the approved binary protocol."""


class EpisodeStatus(str, Enum):
    """The state of a bounded binary decision episode."""

    PENDING = "PENDING"
    COMMITTED = "COMMITTED"
    DEFER = "DEFER"


@dataclass(frozen=True)
class BinaryGoalEvidence:
    """Calibrated left/right probabilities aligned to candidate A/B likelihoods."""

    candidate_a_likelihood: float
    candidate_b_likelihood: float
    class_labels: tuple[str, str] = APPROVED_CLASS_LABELS

    @classmethod
    def from_calibrated_probabilities(
        cls,
        probabilities: tuple[float, float] | list[float] | np.ndarray,
        *,
        class_labels: tuple[str, str] = APPROVED_CLASS_LABELS,
    ) -> "BinaryGoalEvidence":
        """Map approved left/right evidence directly to the active A/B candidates."""
        _validate_class_labels(class_labels)
        values = _validated_normalized_probabilities(probabilities, name="Calibrated probabilities")
        return cls(
            candidate_a_likelihood=float(values[0]),
            candidate_b_likelihood=float(values[1]),
            class_labels=class_labels,
        )

    @property
    def likelihoods(self) -> tuple[float, float]:
        return (self.candidate_a_likelihood, self.candidate_b_likelihood)


@dataclass(frozen=True)
class BayesianEpisodeResult:
    """An auditable snapshot after one accepted evidence update."""

    candidate_names: tuple[str, str]
    posterior: tuple[float, float]
    update_count: int
    status: EpisodeStatus
    committed_candidate: str | None


class BinaryBayesianGoalEpisode:
    """A bounded Bayesian episode with an explicit prior only at episode start."""

    def __init__(
        self,
        *,
        candidate_a: str,
        candidate_b: str,
        initial_prior: tuple[float, float] | list[float] | np.ndarray | None = None,
    ) -> None:
        candidate_names = (str(candidate_a), str(candidate_b))
        if not all(candidate_names) or candidate_names[0] == candidate_names[1]:
            raise BayesianGoalInferenceError("Candidate A and candidate B must be distinct non-empty names.")
        self._candidate_names = candidate_names
        self.start_new_episode(initial_prior=initial_prior)

    @property
    def candidate_names(self) -> tuple[str, str]:
        return self._candidate_names

    @property
    def posterior(self) -> tuple[float, float]:
        return tuple(float(value) for value in self._posterior)

    @property
    def update_count(self) -> int:
        return self._update_count

    @property
    def status(self) -> EpisodeStatus:
        return self._status

    @property
    def history(self) -> tuple[BayesianEpisodeResult, ...]:
        return tuple(self._history)

    def start_new_episode(
        self,
        *,
        initial_prior: tuple[float, float] | list[float] | np.ndarray | None = None,
    ) -> BayesianEpisodeResult:
        """Discard episode state and apply a validated prior for the new episode only."""
        if (
            initial_prior is not None
            and getattr(self, "_status", None) is EpisodeStatus.PENDING
            and getattr(self, "_update_count", 0) > 0
        ):
            raise BayesianGoalInferenceError(
                "A custom initial prior cannot be injected during an active Bayesian evidence sequence."
            )
        selected_prior = INITIAL_PRIOR if initial_prior is None else initial_prior
        self._posterior = _validated_normalized_probabilities(selected_prior, name="Initial prior")
        self._update_count = 0
        self._status = EpisodeStatus.PENDING
        self._history: list[BayesianEpisodeResult] = []
        return self._snapshot(committed_candidate=None)

    def accept_evidence(self, evidence: BinaryGoalEvidence) -> BayesianEpisodeResult:
        """Apply one accepted calibrated binary evidence update to this episode."""
        if not isinstance(evidence, BinaryGoalEvidence):
            raise BayesianGoalInferenceError("Evidence must be a BinaryGoalEvidence instance.")
        if self._status is not EpisodeStatus.PENDING:
            raise BayesianGoalInferenceError("Start a new episode before accepting evidence after a terminal outcome.")

        _validate_class_labels(evidence.class_labels)
        likelihoods = _validated_normalized_probabilities(evidence.likelihoods, name="Evidence likelihoods")
        unnormalized = self._posterior * likelihoods
        total_mass = float(unnormalized.sum())
        if not np.isfinite(total_mass) or total_mass <= 0.0:
            raise BayesianGoalInferenceError("Bayesian update has non-positive or non-finite normalization mass.")

        self._posterior = unnormalized / total_mass
        if not np.isfinite(self._posterior).all() or (self._posterior < 0.0).any():
            raise BayesianGoalInferenceError("Bayesian update produced an invalid posterior.")
        self._update_count += 1

        committed_candidate = self._committed_candidate()
        if committed_candidate is not None:
            self._status = EpisodeStatus.COMMITTED
        elif self._update_count == MAX_EVIDENCE_UPDATES:
            self._status = EpisodeStatus.DEFER

        result = self._snapshot(committed_candidate=committed_candidate)
        self._history.append(result)
        return result

    def _committed_candidate(self) -> str | None:
        if self._posterior[0] >= COMMITMENT_THRESHOLD:
            return self._candidate_names[0]
        if self._posterior[1] >= COMMITMENT_THRESHOLD:
            return self._candidate_names[1]
        return None

    def _snapshot(self, *, committed_candidate: str | None) -> BayesianEpisodeResult:
        return BayesianEpisodeResult(
            candidate_names=self.candidate_names,
            posterior=self.posterior,
            update_count=self.update_count,
            status=self.status,
            committed_candidate=committed_candidate,
        )


def binary_goal_evidence_from_calibrated_probabilities(
    probabilities: tuple[float, float] | list[float] | np.ndarray,
    *,
    class_labels: tuple[str, str] = APPROVED_CLASS_LABELS,
) -> BinaryGoalEvidence:
    """Build the only approved evidence adapter for a binary decision episode."""
    return BinaryGoalEvidence.from_calibrated_probabilities(probabilities, class_labels=class_labels)


def _validate_class_labels(class_labels: tuple[str, str]) -> None:
    if tuple(class_labels) != APPROVED_CLASS_LABELS:
        raise BayesianGoalInferenceError(
            "Binary goal evidence must preserve the approved class order ('left', 'right')."
        )


def _validated_normalized_probabilities(
    values: tuple[float, float] | list[float] | np.ndarray,
    *,
    name: str,
) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1 or array.shape != (2,):
        raise BayesianGoalInferenceError(f"{name} must contain exactly two values.")
    if not np.isfinite(array).all():
        raise BayesianGoalInferenceError(f"{name} must be finite.")
    if (array < 0.0).any():
        raise BayesianGoalInferenceError(f"{name} must be non-negative.")
    if not np.isclose(array.sum(), 1.0, rtol=0.0, atol=1e-8):
        raise BayesianGoalInferenceError(f"{name} must sum to 1.0.")
    return array
