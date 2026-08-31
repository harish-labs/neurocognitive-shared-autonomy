"""Approved subject- and candidate-pair-specific Bayesian prior personalization."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

UNIFORM_PRIOR = (0.5, 0.5)
INITIAL_ALPHA = 1
WARM_UP_EVENTS = 3
PRIOR_LOWER_BOUND = 0.25
PRIOR_UPPER_BOUND = 0.75


class AdaptationError(ValueError):
    """Raised when an adaptation operation violates D-058 through D-060."""


class FeedbackAction(str, Enum):
    CONFIRM = "CONFIRM"
    OVERRIDE = "OVERRIDE"
    PAUSE = "PAUSE"
    STOP = "STOP"
    DEFER = "DEFER"
    PROCEED = "PROCEED"


@dataclass(frozen=True)
class CandidatePair:
    """Stable unordered identity for the two candidates in an episode."""

    candidate_ids: tuple[str, str]

    @classmethod
    def from_presented_candidates(cls, candidate_a_id: str, candidate_b_id: str) -> "CandidatePair":
        ids = (str(candidate_a_id), str(candidate_b_id))
        if not all(ids) or ids[0] == ids[1]:
            raise AdaptationError("A candidate pair requires two distinct non-empty stable candidate IDs.")
        return cls(candidate_ids=tuple(sorted(ids)))


@dataclass(frozen=True)
class AdaptationState:
    subject_id: str
    candidate_pair: CandidatePair
    alpha_by_candidate: tuple[int, int] = (INITIAL_ALPHA, INITIAL_ALPHA)
    update_count: int = 0

    def alpha_for(self, candidate_id: str) -> int:
        try:
            return self.alpha_by_candidate[self.candidate_pair.candidate_ids.index(str(candidate_id))]
        except ValueError as exc:
            raise AdaptationError("Candidate is not part of this adaptation state.") from exc


@dataclass(frozen=True)
class ExplicitFeedbackObservation:
    subject_id: str
    candidate_a_id: str
    candidate_b_id: str
    action: FeedbackAction
    source_observation_id: str
    approved_goal_id: str | None = None
    between_episodes: bool = True


@dataclass(frozen=True)
class AdaptationUpdateRecord:
    subject_id: str
    candidate_pair: CandidatePair
    source_observation_id: str
    action: FeedbackAction
    approved_goal_id: str
    prior_state: AdaptationState
    updated_state: AdaptationState


class PriorPersonalizer:
    """Stores only approved explicit-feedback prior state, isolated by subject and pair."""

    def __init__(self, *, adaptation_enabled: bool = True) -> None:
        self.adaptation_enabled = adaptation_enabled
        self._states: dict[tuple[str, CandidatePair], AdaptationState] = {}
        self._records: list[AdaptationUpdateRecord] = []

    @property
    def update_records(self) -> tuple[AdaptationUpdateRecord, ...]:
        return tuple(self._records)

    def state_for(self, subject_id: str, candidate_a_id: str, candidate_b_id: str) -> AdaptationState:
        key = self._key(subject_id, candidate_a_id, candidate_b_id)
        if key not in self._states:
            self._states[key] = AdaptationState(subject_id=key[0], candidate_pair=key[1])
        return self._states[key]

    def initial_prior_for_new_episode(
        self,
        subject_id: str,
        candidate_a_id: str,
        candidate_b_id: str,
        *,
        episode_is_active: bool = False,
    ) -> tuple[float, float]:
        """Return only a future episode's A/B prior; never mutate active Bayes state."""
        if episode_is_active:
            raise AdaptationError("Adaptation may supply a prior only before a new Bayesian episode starts.")
        state = self.state_for(subject_id, candidate_a_id, candidate_b_id)
        if not self.adaptation_enabled or state.update_count < WARM_UP_EVENTS:
            return UNIFORM_PRIOR
        raw = self._raw_prior(state, candidate_a_id, candidate_b_id)
        bounded_a = float(np.clip(raw[0], PRIOR_LOWER_BOUND, PRIOR_UPPER_BOUND))
        return (bounded_a, 1.0 - bounded_a)

    def record_explicit_feedback(
        self,
        observation: ExplicitFeedbackObservation,
    ) -> AdaptationUpdateRecord | None:
        """Accept only approved explicit final-choice feedback between episodes."""
        if not isinstance(observation, ExplicitFeedbackObservation):
            raise AdaptationError("Adaptation requires an ExplicitFeedbackObservation.")
        if not observation.between_episodes:
            raise AdaptationError("Adaptation state cannot change during an active Bayesian evidence sequence.")
        if observation.action not in {FeedbackAction.CONFIRM, FeedbackAction.OVERRIDE}:
            return None
        if not observation.source_observation_id or observation.approved_goal_id is None:
            raise AdaptationError("Accepted feedback requires a source observation ID and explicit approved goal.")

        state = self.state_for(observation.subject_id, observation.candidate_a_id, observation.candidate_b_id)
        approved_goal = str(observation.approved_goal_id)
        if approved_goal not in state.candidate_pair.candidate_ids:
            raise AdaptationError("Explicit approved goal must belong to the active candidate pair.")
        index = state.candidate_pair.candidate_ids.index(approved_goal)
        alphas = list(state.alpha_by_candidate)
        alphas[index] += 1
        updated = AdaptationState(
            subject_id=state.subject_id,
            candidate_pair=state.candidate_pair,
            alpha_by_candidate=(alphas[0], alphas[1]),
            update_count=state.update_count + 1,
        )
        self._states[(state.subject_id, state.candidate_pair)] = updated
        record = AdaptationUpdateRecord(
            subject_id=state.subject_id,
            candidate_pair=state.candidate_pair,
            source_observation_id=observation.source_observation_id,
            action=observation.action,
            approved_goal_id=approved_goal,
            prior_state=state,
            updated_state=updated,
        )
        self._records.append(record)
        return record

    def reset(self, subject_id: str, candidate_a_id: str, candidate_b_id: str) -> AdaptationState:
        key = self._key(subject_id, candidate_a_id, candidate_b_id)
        state = AdaptationState(subject_id=key[0], candidate_pair=key[1])
        self._states[key] = state
        return state

    def _key(self, subject_id: str, candidate_a_id: str, candidate_b_id: str) -> tuple[str, CandidatePair]:
        normalized_subject = str(subject_id)
        if not normalized_subject:
            raise AdaptationError("Anonymous subject ID must be non-empty.")
        return (normalized_subject, CandidatePair.from_presented_candidates(candidate_a_id, candidate_b_id))

    @staticmethod
    def _raw_prior(
        state: AdaptationState,
        candidate_a_id: str,
        candidate_b_id: str,
    ) -> tuple[float, float]:
        alpha_a = state.alpha_for(candidate_a_id)
        alpha_b = state.alpha_for(candidate_b_id)
        total = alpha_a + alpha_b
        return (alpha_a / total, alpha_b / total)
