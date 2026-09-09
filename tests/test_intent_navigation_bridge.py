from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

import src.control.intent_navigation_bridge as intent_navigation_bridge
from src.autonomy.environment import EnvironmentConfig, SearchRescueEnvironment
from src.cognitive.bayes import EpisodeStatus
from src.cognitive.replay_episode import BayesianReplayEpisodeResult, BayesianReplayUpdate
from src.control.human_interaction import HumanCommand, HumanCommandType, HumanInteractionController
from src.control.intent_navigation_bridge import (
    IntentNavigationStatus,
    authorize_episode_navigation,
)
from src.control.navigation_runtime import NavigationRuntime, NavigationStatus


def make_environment() -> SearchRescueEnvironment:
    return SearchRescueEnvironment(
        EnvironmentConfig(
            rows=3,
            columns=5,
            start=(1, 0),
            goals={"victim_a": (1, 4), "victim_b": (0, 2)},
        )
    )


def episode(
    *,
    posterior: tuple[float, float],
    update_count: int,
    status: EpisodeStatus,
    committed_candidate: str | None = None,
    candidates: tuple[str, str] = ("victim_a", "victim_b"),
) -> BayesianReplayEpisodeResult:
    updates = tuple(
        BayesianReplayUpdate(
            replay_index=index,
            canonical_trial_identity=(1, 4, "source.edf", 100 + index, "T1"),
            class_labels=("left", "right"),
            calibrated_probabilities=(0.5, 0.5),
            posterior_after_update=posterior if index == update_count - 1 else (0.5, 0.5),
            update_count=index + 1,
            status_after_update=status if index == update_count - 1 else EpisodeStatus.PENDING,
            committed_candidate_after_update=committed_candidate if index == update_count - 1 else None,
        )
        for index in range(update_count)
    )
    return BayesianReplayEpisodeResult(
        candidate_names=candidates,
        initial_prior=(0.5, 0.5),
        status=status,
        posterior=posterior,
        committed_candidate=committed_candidate,
        update_count=update_count,
        evidence_updates=updates,
    )


def test_committed_episode_authorizes_exact_goal_and_creates_zero_movement_plan() -> None:
    environment = make_environment()
    controller = HumanInteractionController()
    position_before = environment.state.position

    result = authorize_episode_navigation(
        episode(posterior=(1.0, 0.0), update_count=1, status=EpisodeStatus.COMMITTED, committed_candidate="victim_a"),
        controller,
        environment,
        NavigationRuntime(),
        execution_id="execution-1",
    )

    assert result.status is IntentNavigationStatus.READY
    assert result.bayesian_episode is not None
    assert result.bayesian_episode.candidate_names == ("victim_a", "victim_b")
    assert result.bayesian_episode.posterior == (1.0, 0.0)
    assert result.bayesian_episode.update_count == 1
    assert result.bayesian_episode.status is EpisodeStatus.COMMITTED
    assert result.bayesian_episode.committed_candidate == "victim_a"
    assert result.authorization is not None and result.authorization.approved_goal == "victim_a"
    assert result.navigation is not None and result.navigation.status is NavigationStatus.READY
    assert result.navigation.symbolic_goal == "victim_a"
    assert not result.navigation.moved and not result.moved
    assert environment.state.position == position_before


def test_pending_and_deferred_episodes_hold_without_navigation() -> None:
    environment = make_environment()
    controller = HumanInteractionController()
    runtime = NavigationRuntime()

    pending = authorize_episode_navigation(
        episode(posterior=(0.6, 0.4), update_count=1, status=EpisodeStatus.PENDING),
        controller,
        environment,
        runtime,
    )
    deferred = authorize_episode_navigation(
        episode(posterior=(0.6, 0.4), update_count=5, status=EpisodeStatus.DEFER),
        controller,
        environment,
        runtime,
    )

    assert pending.status is deferred.status is IntentNavigationStatus.HOLD
    assert pending.shared_autonomy_decision is not None
    assert pending.shared_autonomy_decision.mode.value == "WAITING"
    assert deferred.shared_autonomy_decision is not None
    assert deferred.shared_autonomy_decision.mode.value == "DEFER"
    assert pending.navigation is deferred.navigation is None
    assert runtime.session is None and environment.state.position == (1, 0)


def test_horizon_confirmation_opens_existing_request_without_navigation() -> None:
    environment = make_environment()
    controller = HumanInteractionController()
    runtime = NavigationRuntime()

    result = authorize_episode_navigation(
        episode(posterior=(0.8, 0.2), update_count=5, status=EpisodeStatus.DEFER),
        controller,
        environment,
        runtime,
        confirmation_request_id="request-1",
    )

    assert result.status is IntentNavigationStatus.HOLD
    assert result.authorization is not None and result.authorization.confirmation_opened
    assert controller.state.active_confirmation is not None
    assert controller.state.active_confirmation.request_id == "request-1"
    assert result.navigation is None and runtime.session is None
    assert environment.state.position == (1, 0)


def test_missing_identifiers_fail_closed_without_authorization_side_effects() -> None:
    environment = make_environment()
    controller = HumanInteractionController()
    proceed = authorize_episode_navigation(
        episode(posterior=(1.0, 0.0), update_count=1, status=EpisodeStatus.COMMITTED, committed_candidate="victim_a"),
        controller,
        environment,
        NavigationRuntime(),
    )
    confirm = authorize_episode_navigation(
        episode(posterior=(0.8, 0.2), update_count=5, status=EpisodeStatus.DEFER),
        controller,
        environment,
        NavigationRuntime(),
    )

    assert proceed.status is confirm.status is IntentNavigationStatus.HOLD
    assert controller.state.approved_goal is None
    assert controller.state.active_confirmation is None


def test_invalid_episode_goal_and_human_authority_states_hold_without_movement() -> None:
    environment = make_environment()
    invalid_goal = authorize_episode_navigation(
        episode(
            posterior=(1.0, 0.0),
            update_count=1,
            status=EpisodeStatus.COMMITTED,
            committed_candidate="missing_goal",
            candidates=("missing_goal", "victim_b"),
        ),
        HumanInteractionController(),
        environment,
        NavigationRuntime(),
        execution_id="invalid-goal",
    )

    paused = HumanInteractionController()
    paused.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
    paused_result = authorize_episode_navigation(
        episode(posterior=(1.0, 0.0), update_count=1, status=EpisodeStatus.COMMITTED, committed_candidate="victim_a"),
        paused,
        environment,
        NavigationRuntime(),
        execution_id="paused",
    )

    stopped = HumanInteractionController()
    stopped.handle_command(HumanCommand("stop", HumanCommandType.STOP))
    stopped_result = authorize_episode_navigation(
        episode(posterior=(1.0, 0.0), update_count=1, status=EpisodeStatus.COMMITTED, committed_candidate="victim_a"),
        stopped,
        environment,
        NavigationRuntime(),
        execution_id="stopped",
    )

    assert invalid_goal.status is paused_result.status is stopped_result.status is IntentNavigationStatus.HOLD
    assert all(result.navigation is None for result in (invalid_goal, paused_result, stopped_result))
    assert environment.state.position == (1, 0)


def test_active_confirmation_and_reused_execution_id_cannot_be_bypassed() -> None:
    environment = make_environment()
    runtime = NavigationRuntime()
    active = HumanInteractionController()
    active.open_confirmation_request("active-request", "victim_b")
    held = authorize_episode_navigation(
        episode(posterior=(1.0, 0.0), update_count=1, status=EpisodeStatus.COMMITTED, committed_candidate="victim_a"),
        active,
        environment,
        runtime,
        execution_id="active",
    )

    first_controller = HumanInteractionController()
    first = authorize_episode_navigation(
        episode(posterior=(1.0, 0.0), update_count=1, status=EpisodeStatus.COMMITTED, committed_candidate="victim_a"),
        first_controller,
        environment,
        runtime,
        execution_id="duplicate",
    )
    second_controller = HumanInteractionController()
    duplicate = authorize_episode_navigation(
        episode(posterior=(1.0, 0.0), update_count=1, status=EpisodeStatus.COMMITTED, committed_candidate="victim_a"),
        second_controller,
        environment,
        runtime,
        execution_id="duplicate",
    )

    assert held.status is IntentNavigationStatus.HOLD and held.navigation is None
    assert first.status is IntentNavigationStatus.READY
    assert duplicate.status is IntentNavigationStatus.HOLD
    assert duplicate.navigation is not None and duplicate.navigation.status is NavigationStatus.ALREADY_CONSUMED
    assert environment.state.position == (1, 0)


def test_malformed_result_rejected_and_bridge_never_steps_or_replans(monkeypatch: pytest.MonkeyPatch) -> None:
    environment = make_environment()
    runtime = NavigationRuntime()
    monkeypatch.setattr(runtime, "advance_one_step", lambda *args: pytest.fail("must not advance"))
    monkeypatch.setattr(runtime, "replan_after_environment_change", lambda *args: pytest.fail("must not replan"))

    result = authorize_episode_navigation(object(), HumanInteractionController(), environment, runtime)

    assert result.status is IntentNavigationStatus.REJECTED
    assert not result.moved and environment.state.position == (1, 0)
    source = Path(intent_navigation_bridge.__file__).read_text(encoding="utf-8")
    assert ".advance_one_step(" not in source
    assert ".replan_after_environment_change(" not in source


def test_inconsistent_committed_candidate_fails_closed() -> None:
    environment = make_environment()
    accepted = episode(
        posterior=(1.0, 0.0),
        update_count=1,
        status=EpisodeStatus.COMMITTED,
        committed_candidate="victim_a",
    )
    forged_update = replace(accepted.evidence_updates[-1], committed_candidate_after_update="victim_b")
    forged = replace(accepted, committed_candidate="victim_b", evidence_updates=(forged_update,))

    result = authorize_episode_navigation(
        forged,
        HumanInteractionController(),
        environment,
        NavigationRuntime(),
        execution_id="forged",
    )

    assert result.status is IntentNavigationStatus.REJECTED
    assert environment.state.position == (1, 0)
