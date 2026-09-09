"""D-074 through D-076 handoff from one Bayesian replay episode to navigation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.autonomy.environment import SearchRescueEnvironment
from src.cognitive.bayes import BayesianEpisodeResult, EpisodeStatus, INITIAL_PRIOR, MAX_EVIDENCE_UPDATES
from src.cognitive.replay_episode import BayesianReplayEpisodeResult, BayesianReplayUpdate
from src.cognitive.uncertainty import BinaryUncertainty, estimate_binary_uncertainty
from src.control.human_interaction import HumanInteractionController
from src.control.interaction_bridge import (
    BridgeStatus,
    InteractionBridgeResult,
    authorize_shared_autonomy_decision,
)
from src.control.navigation_runtime import NavigationResult, NavigationRuntime, NavigationStatus
from src.control.shared_autonomy import AutonomyMode, SharedAutonomyDecision, decide_shared_autonomy


class IntentNavigationStatus(str, Enum):
    """Non-moving outcomes at the M6-T04 composition boundary."""

    READY = "READY"
    HOLD = "HOLD"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class IntentNavigationResult:
    """Immutable audit record for one M6-T04 authorization attempt."""

    status: IntentNavigationStatus
    replay_episode: BayesianReplayEpisodeResult | None
    bayesian_episode: BayesianEpisodeResult | None
    uncertainty: BinaryUncertainty | None
    shared_autonomy_decision: SharedAutonomyDecision | None
    authorization: InteractionBridgeResult | None
    navigation: NavigationResult | None
    moved: bool
    reason: str


def authorize_episode_navigation(
    replay_episode: object,
    controller: object,
    environment: object,
    navigation_runtime: object,
    *,
    confirmation_request_id: object | None = None,
    execution_id: object | None = None,
) -> IntentNavigationResult:
    """Compose one accepted replay episode through policy and fresh navigation authorization."""

    if not isinstance(controller, HumanInteractionController):
        return _rejected("Bridge requires a HumanInteractionController.")
    if not isinstance(environment, SearchRescueEnvironment):
        return _rejected("Bridge requires an accepted SearchRescueEnvironment.")
    if not isinstance(navigation_runtime, NavigationRuntime):
        return _rejected("Bridge requires an accepted NavigationRuntime.")

    try:
        bayesian_episode = _episode_snapshot(replay_episode)
        uncertainty = estimate_binary_uncertainty(bayesian_episode.posterior)
        decision = decide_shared_autonomy(bayesian_episode, uncertainty)
        _validate_terminal_policy_consistency(replay_episode, decision)
    except (TypeError, ValueError) as error:
        return _rejected(str(error), replay_episode=replay_episode)

    if decision.mode is AutonomyMode.PROCEED and not _is_non_empty_identifier(execution_id):
        return _hold(
            replay_episode,
            bayesian_episode,
            uncertainty,
            decision,
            reason="PROCEED requires a caller-supplied non-empty execution_id before authorization.",
        )
    if decision.mode is AutonomyMode.CONFIRM and not _is_non_empty_identifier(confirmation_request_id):
        return _hold(
            replay_episode,
            bayesian_episode,
            uncertainty,
            decision,
            reason="CONFIRM requires a caller-supplied non-empty confirmation_request_id.",
        )

    authorization = authorize_shared_autonomy_decision(
        decision,
        controller,
        goal_registry=environment.config.goals,
        request_id=confirmation_request_id,
    )
    if authorization.status is not BridgeStatus.AUTHORIZED:
        return _hold(
            replay_episode,
            bayesian_episode,
            uncertainty,
            decision,
            authorization=authorization,
            reason=authorization.reason,
        )

    navigation = navigation_runtime.start_navigation(
        environment,
        controller,
        authorization,
        execution_id=execution_id,
    )
    if navigation.status is NavigationStatus.READY:
        return IntentNavigationResult(
            status=IntentNavigationStatus.READY,
            replay_episode=replay_episode,
            bayesian_episode=bayesian_episode,
            uncertainty=uncertainty,
            shared_autonomy_decision=decision,
            authorization=authorization,
            navigation=navigation,
            moved=navigation.moved,
            reason=navigation.reason,
        )
    return _hold(
        replay_episode,
        bayesian_episode,
        uncertainty,
        decision,
        authorization=authorization,
        navigation=navigation,
        reason=navigation.reason,
    )


def _episode_snapshot(value: object) -> BayesianEpisodeResult:
    if not isinstance(value, BayesianReplayEpisodeResult):
        raise ValueError("Bridge requires an accepted BayesianReplayEpisodeResult.")
    if value.initial_prior != INITIAL_PRIOR:
        raise ValueError("Replay episode initial prior is inconsistent with the accepted Bayesian contract.")
    if not isinstance(value.candidate_names, tuple) or len(value.candidate_names) != 2:
        raise ValueError("Replay episode must preserve exactly two candidate names.")
    if not all(isinstance(candidate, str) and candidate for candidate in value.candidate_names):
        raise ValueError("Replay episode candidate names must be non-empty strings.")
    if value.candidate_names[0] == value.candidate_names[1]:
        raise ValueError("Replay episode candidate names must be distinct.")
    if not isinstance(value.update_count, int) or not 1 <= value.update_count <= MAX_EVIDENCE_UPDATES:
        raise ValueError("Replay episode update count is outside the accepted evidence horizon.")
    if not isinstance(value.status, EpisodeStatus):
        raise ValueError("Replay episode status must be an accepted EpisodeStatus.")
    if not isinstance(value.evidence_updates, tuple) or len(value.evidence_updates) != value.update_count:
        raise ValueError("Replay episode evidence-update history is inconsistent with its update count.")

    for expected_count, update in enumerate(value.evidence_updates, start=1):
        if not isinstance(update, BayesianReplayUpdate) or update.update_count != expected_count:
            raise ValueError("Replay episode evidence-update history is structurally inconsistent.")

    final_update = value.evidence_updates[-1]
    if (
        final_update.posterior_after_update != value.posterior
        or final_update.status_after_update is not value.status
        or final_update.committed_candidate_after_update != value.committed_candidate
    ):
        raise ValueError("Replay episode terminal snapshot differs from its final evidence update.")
    if value.status is EpisodeStatus.COMMITTED:
        if value.committed_candidate not in value.candidate_names:
            raise ValueError("Committed replay episode must preserve an exact candidate name.")
    elif value.committed_candidate is not None:
        raise ValueError("Uncommitted replay episode must not expose a committed candidate.")
    if value.status is EpisodeStatus.PENDING and value.update_count >= MAX_EVIDENCE_UPDATES:
        raise ValueError("Pending replay episode cannot exceed the accepted evidence horizon.")
    if value.status is EpisodeStatus.DEFER and value.update_count != MAX_EVIDENCE_UPDATES:
        raise ValueError("Deferred replay episode must end at the accepted evidence horizon.")

    return BayesianEpisodeResult(
        candidate_names=value.candidate_names,
        posterior=value.posterior,
        update_count=value.update_count,
        status=value.status,
        committed_candidate=value.committed_candidate,
    )


def _is_non_empty_identifier(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _validate_terminal_policy_consistency(
    replay_episode: BayesianReplayEpisodeResult,
    decision: SharedAutonomyDecision,
) -> None:
    if replay_episode.status is EpisodeStatus.COMMITTED:
        if decision.mode is not AutonomyMode.PROCEED or decision.candidate_goal != replay_episode.committed_candidate:
            raise ValueError("Committed replay episode is inconsistent with the accepted shared-autonomy policy.")
    elif replay_episode.status is EpisodeStatus.PENDING:
        if decision.mode is not AutonomyMode.WAITING:
            raise ValueError("Pending replay episode is inconsistent with the accepted shared-autonomy policy.")
    elif replay_episode.status is EpisodeStatus.DEFER and decision.mode not in (AutonomyMode.CONFIRM, AutonomyMode.DEFER):
        raise ValueError("Deferred replay episode is inconsistent with the accepted shared-autonomy policy.")


def _rejected(reason: str, *, replay_episode: object | None = None) -> IntentNavigationResult:
    return IntentNavigationResult(
        status=IntentNavigationStatus.REJECTED,
        replay_episode=replay_episode if isinstance(replay_episode, BayesianReplayEpisodeResult) else None,
        bayesian_episode=None,
        uncertainty=None,
        shared_autonomy_decision=None,
        authorization=None,
        navigation=None,
        moved=False,
        reason=reason,
    )


def _hold(
    replay_episode: BayesianReplayEpisodeResult,
    bayesian_episode: BayesianEpisodeResult,
    uncertainty: BinaryUncertainty,
    decision: SharedAutonomyDecision,
    *,
    authorization: InteractionBridgeResult | None = None,
    navigation: NavigationResult | None = None,
    reason: str,
) -> IntentNavigationResult:
    return IntentNavigationResult(
        status=IntentNavigationStatus.HOLD,
        replay_episode=replay_episode,
        bayesian_episode=bayesian_episode,
        uncertainty=uncertainty,
        shared_autonomy_decision=decision,
        authorization=authorization,
        navigation=navigation,
        moved=False,
        reason=reason,
    )
