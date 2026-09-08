"""Synchronous integration from calibrated replay evidence to one Bayesian episode."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from src.cognitive.bayes import (
    APPROVED_CLASS_LABELS,
    INITIAL_PRIOR,
    BayesianEpisodeResult,
    BinaryBayesianGoalEpisode,
    EpisodeStatus,
    binary_goal_evidence_from_calibrated_probabilities,
)
from src.models.runtime_adapter import DecodedReplayObservation


class ReplayEpisodeIntegrationError(ValueError):
    """Raised when calibrated replay evidence cannot safely enter one episode."""


@dataclass(frozen=True)
class BayesianReplayUpdate:
    """Immutable audit record for one accepted Bayesian evidence update."""

    replay_index: int
    canonical_trial_identity: tuple[int, int, str, int, str]
    class_labels: tuple[str, str]
    calibrated_probabilities: tuple[float, float]
    posterior_after_update: tuple[float, float]
    update_count: int
    status_after_update: EpisodeStatus
    committed_candidate_after_update: str | None


@dataclass(frozen=True)
class BayesianReplayEpisodeResult:
    """Immutable audit result for one bounded binary Bayesian episode."""

    candidate_names: tuple[str, str]
    initial_prior: tuple[float, float]
    status: EpisodeStatus
    posterior: tuple[float, float]
    committed_candidate: str | None
    update_count: int
    evidence_updates: tuple[BayesianReplayUpdate, ...]


def run_bayesian_replay_episode(
    observations: Iterable[DecodedReplayObservation],
    *,
    candidate_a: str,
    candidate_b: str,
) -> BayesianReplayEpisodeResult:
    """Consume one ordered calibrated replay sequence through one accepted episode."""

    candidate_names = _validate_candidates(candidate_a, candidate_b)
    episode = BinaryBayesianGoalEpisode(candidate_a=candidate_names[0], candidate_b=candidate_names[1])
    updates: list[BayesianReplayUpdate] = []
    seen_replay_indices: set[int] = set()
    seen_trial_identities: set[tuple[int, int, str, int, str]] = set()
    previous_replay_index: int | None = None

    try:
        iterator = iter(observations)
    except TypeError as error:
        raise ReplayEpisodeIntegrationError("Observations must be an iterable sequence.") from error

    while episode.status is EpisodeStatus.PENDING:
        try:
            observation = next(iterator)
        except StopIteration:
            break
        if not isinstance(observation, DecodedReplayObservation):
            raise ReplayEpisodeIntegrationError("Each observation must be a DecodedReplayObservation.")
        _validate_order_and_uniqueness(
            observation,
            previous_replay_index=previous_replay_index,
            seen_replay_indices=seen_replay_indices,
            seen_trial_identities=seen_trial_identities,
        )
        previous_replay_index = observation.replay_index
        seen_replay_indices.add(observation.replay_index)
        seen_trial_identities.add(observation.canonical_trial_identity)

        probabilities = _validated_probability_row(observation)
        evidence = binary_goal_evidence_from_calibrated_probabilities(
            probabilities[0],
            class_labels=observation.class_labels,
        )
        bayesian_result = episode.accept_evidence(evidence)
        _validate_consistency(episode, bayesian_result)
        updates.append(
            BayesianReplayUpdate(
                replay_index=observation.replay_index,
                canonical_trial_identity=observation.canonical_trial_identity,
                class_labels=tuple(observation.class_labels),
                calibrated_probabilities=(float(probabilities[0, 0]), float(probabilities[0, 1])),
                posterior_after_update=bayesian_result.posterior,
                update_count=bayesian_result.update_count,
                status_after_update=bayesian_result.status,
                committed_candidate_after_update=bayesian_result.committed_candidate,
            )
        )

    if not updates:
        raise ReplayEpisodeIntegrationError("At least one decoded observation is required.")

    final_result = episode.history[-1]
    _validate_consistency(episode, final_result)
    return BayesianReplayEpisodeResult(
        candidate_names=episode.candidate_names,
        initial_prior=INITIAL_PRIOR,
        status=final_result.status,
        posterior=final_result.posterior,
        committed_candidate=final_result.committed_candidate,
        update_count=final_result.update_count,
        evidence_updates=tuple(updates),
    )


def _validate_candidates(candidate_a: str, candidate_b: str) -> tuple[str, str]:
    if not isinstance(candidate_a, str) or not candidate_a:
        raise ReplayEpisodeIntegrationError("candidate_a must be a non-empty string.")
    if not isinstance(candidate_b, str) or not candidate_b:
        raise ReplayEpisodeIntegrationError("candidate_b must be a non-empty string.")
    if candidate_a == candidate_b:
        raise ReplayEpisodeIntegrationError("candidate_a and candidate_b must be distinct.")
    return candidate_a, candidate_b


def _validate_order_and_uniqueness(
    observation: DecodedReplayObservation,
    *,
    previous_replay_index: int | None,
    seen_replay_indices: set[int],
    seen_trial_identities: set[tuple[int, int, str, int, str]],
) -> None:
    if observation.replay_index in seen_replay_indices:
        raise ReplayEpisodeIntegrationError("Duplicate replay_index is not allowed.")
    if previous_replay_index is not None and observation.replay_index <= previous_replay_index:
        raise ReplayEpisodeIntegrationError("replay_index values must strictly increase.")
    if observation.canonical_trial_identity in seen_trial_identities:
        raise ReplayEpisodeIntegrationError("Duplicate canonical trial identity is not allowed.")


def _validated_probability_row(observation: DecodedReplayObservation) -> np.ndarray:
    if tuple(observation.class_labels) != APPROVED_CLASS_LABELS:
        raise ReplayEpisodeIntegrationError("Observation must preserve the approved class order.")
    probabilities = np.asarray(observation.calibrated_probabilities, dtype=np.float64)
    if probabilities.shape != (1, 2):
        raise ReplayEpisodeIntegrationError("Calibrated probabilities must have shape (1, 2).")
    if not np.isfinite(probabilities).all():
        raise ReplayEpisodeIntegrationError("Calibrated probabilities must be finite.")
    if (probabilities < 0.0).any() or (probabilities > 1.0).any():
        raise ReplayEpisodeIntegrationError("Calibrated probabilities must be within [0, 1].")
    if not np.isclose(probabilities.sum(), 1.0, rtol=0.0, atol=1e-8):
        raise ReplayEpisodeIntegrationError("Calibrated probabilities must sum to one.")
    return probabilities


def _validate_consistency(
    episode: BinaryBayesianGoalEpisode,
    result: BayesianEpisodeResult,
) -> None:
    if result.candidate_names != episode.candidate_names:
        raise ReplayEpisodeIntegrationError("Bayesian result candidate names are inconsistent.")
    if result.posterior != episode.posterior:
        raise ReplayEpisodeIntegrationError("Bayesian result posterior is inconsistent.")
    if result.update_count != episode.update_count:
        raise ReplayEpisodeIntegrationError("Bayesian result update count is inconsistent.")
    if result.status is not episode.status:
        raise ReplayEpisodeIntegrationError("Bayesian result status is inconsistent.")
