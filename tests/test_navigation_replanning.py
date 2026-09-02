from __future__ import annotations

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.autonomy.environment import Action, EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.planner import PlannerStatus, PlanningResult
from src.autonomy.safety import InterventionType, SafetyController, SafetyDecision, SafetyStatus
from src.control.human_interaction import HumanCommand, HumanCommandType, HumanInteractionController
from src.control.interaction_bridge import authorize_shared_autonomy_decision
from src.control.navigation_runtime import NavigationReplanTrigger, NavigationRuntime, NavigationStatus
from src.control.shared_autonomy import AutonomyMode, HumanAction, SharedAutonomyDecision


def environment(*, start: tuple[int, int] = (1, 0), blocked: frozenset[tuple[int, int]] = frozenset(), risk: dict[tuple[int, int], float] | None = None) -> SearchRescueEnvironment:
    return SearchRescueEnvironment(EnvironmentConfig(rows=3, columns=5, start=start, goals={"victim_a": (1, 4), "victim_b": (0, 2)}, blocked_cells=blocked, risk_map={} if risk is None else risk))


def authorization(env: SearchRescueEnvironment, controller: HumanInteractionController):
    decision = SharedAutonomyDecision(AutonomyMode.PROCEED, "victim_a", "victim_a", False, False, False, HumanAction.NONE, 0.9, 0.4, 1, "test")
    return authorize_shared_autonomy_decision(decision, controller, goal_registry=env.config.goals)


def source_runtime(*, planner=None, safety=None):
    source = environment()
    controller = HumanInteractionController()
    runtime = NavigationRuntime(planner=planner, safety_controller=safety)
    started = runtime.start_navigation(source, controller, authorization(source, controller), execution_id="source")
    assert started.status is NavigationStatus.READY
    return runtime, source, controller


def replacement(source: SearchRescueEnvironment, *, blocked: frozenset[tuple[int, int]] = frozenset({(2, 2)}), risk: dict[tuple[int, int], float] | None = None) -> SearchRescueEnvironment:
    return environment(start=source.state.position, blocked=blocked, risk=risk)


def test_explicit_changed_snapshot_creates_zero_movement_replacement_session(monkeypatch: pytest.MonkeyPatch) -> None:
    runtime, source, controller = source_runtime()
    changed = replacement(source)
    steps: list[object] = []
    monkeypatch.setattr(changed, "step", lambda action: steps.append(action))

    result = runtime.replan_after_environment_change(source, changed, controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED)

    assert result.status is NavigationStatus.READY
    assert result.planner_invoked and result.replacement_session_created
    assert not result.navigation_result.moved
    assert steps == []
    assert runtime.session is not None and runtime.session.execution_id == "replacement"


@pytest.mark.parametrize("changed", (lambda source: replacement(source), lambda source: replacement(source, blocked=frozenset(), risk={(1, 1): 0.75})))
def test_changed_blocked_or_risk_snapshot_is_accepted(changed) -> None:
    runtime, source, controller = source_runtime()
    result = runtime.replan_after_environment_change(source, changed(source), controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED)
    assert result.status is NavigationStatus.READY


def test_invalid_preplanner_snapshot_and_authority_do_not_consume_event() -> None:
    runtime, source, controller = source_runtime()
    unchanged = environment(start=source.state.position)
    invalid = runtime.replan_after_environment_change(source, unchanged, controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED)
    changed = replacement(source)
    controller.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
    paused = runtime.replan_after_environment_change(source, changed, controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED)

    assert invalid.status is NavigationStatus.STALE_STATE
    assert paused.status is NavigationStatus.PAUSED
    assert not invalid.planner_invoked and not paused.planner_invoked


def test_consumed_event_allows_at_most_one_planner_invocation_even_on_no_safe_path() -> None:
    runtime, source, controller = source_runtime()
    changed = replacement(source, blocked=frozenset({(0, 1), (1, 1), (2, 1)}))
    first = runtime.replan_after_environment_change(source, changed, controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED)
    second = runtime.replan_after_environment_change(source, changed, controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement-2", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED)

    assert first.status is NavigationStatus.NO_SAFE_PATH
    assert first.planner_invoked
    assert second.status is NavigationStatus.ALREADY_CONSUMED
    assert not second.planner_invoked


def test_replan_requires_distinct_new_execution_and_preserves_exact_goal_mapping() -> None:
    runtime, source, controller = source_runtime()
    changed_goals = SearchRescueEnvironment(EnvironmentConfig(rows=3, columns=5, start=source.state.position, goals={"victim_a": (1, 3), "victim_b": (0, 2)}, blocked_cells=frozenset({(2, 2)})))
    same_id = runtime.replan_after_environment_change(source, replacement(source), controller, source_execution_id="source", event_id="event-1", new_execution_id="source", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED)
    wrong_goals = runtime.replan_after_environment_change(source, changed_goals, controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED)

    assert same_id.status is NavigationStatus.INVALID_AUTHORIZATION
    assert wrong_goals.status is NavigationStatus.STALE_STATE
    assert not same_id.planner_invoked and not wrong_goals.planner_invoked


def test_safety_replan_trigger_requires_genuine_prior_result_and_changed_snapshot() -> None:
    runtime, source, controller = source_runtime(safety=ReplanSafety())
    prior = runtime.advance_one_step(source, controller)
    changed = replacement(source)
    accepted = runtime.replan_after_environment_change(source, changed, controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.SAFETY_REPLAN_REQUIRED, prior_result=prior)

    second_runtime, second_source, second_controller = source_runtime(safety=ReplanSafety())
    unchanged_prior = second_runtime.advance_one_step(second_source, second_controller)
    unchanged = environment(start=second_source.state.position)
    rejected = second_runtime.replan_after_environment_change(second_source, unchanged, second_controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.SAFETY_REPLAN_REQUIRED, prior_result=unchanged_prior)

    assert prior.status is NavigationStatus.REPLAN_REQUIRED
    assert accepted.status is NavigationStatus.READY
    assert rejected.status is NavigationStatus.STALE_STATE


def test_changed_while_paused_requires_applied_resume_and_never_replays_old_path() -> None:
    runtime, source, controller = source_runtime()
    runtime.advance_one_step(source, controller)
    controller.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
    paused = runtime.advance_one_step(source, controller)
    changed = replacement(source)
    blocked = runtime.replan_after_environment_change(source, changed, controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED)
    resume = controller.handle_command(HumanCommand("resume", HumanCommandType.RESUME))
    replanned = runtime.replan_after_environment_change(source, changed, controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED, resume_result=resume)

    assert paused.status is NavigationStatus.PAUSED
    assert blocked.status is NavigationStatus.PAUSED
    assert replanned.status is NavigationStatus.READY
    assert replanned.navigation_result.path[0] == source.state.position == (1, 1)


def test_replacement_session_only_moves_through_ordinary_step_and_old_environment_fails_closed() -> None:
    runtime, source, controller = source_runtime()
    changed = replacement(source)
    replan = runtime.replan_after_environment_change(source, changed, controller, source_execution_id="source", event_id="event-1", new_execution_id="replacement", trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED)
    old = runtime.advance_one_step(source, controller)
    new = runtime.advance_one_step(changed, controller)

    assert replan.status is NavigationStatus.READY
    assert old.status is NavigationStatus.STALE_STATE
    assert not old.moved
    assert new.status is NavigationStatus.HOLD


def test_replan_runtime_never_calls_whole_route_components_or_human_command_handler() -> None:
    source = Path(__file__).resolve().parents[1] / "src" / "control" / "navigation_runtime.py"
    text = source.read_text(encoding="utf-8")
    assert ".handle_command(" not in text
    assert "ControlledReplanningCoordinator" not in text
    assert "PlannerSafetyEnvironmentExecutor" not in text
    assert "src.cognition" not in text
    assert "src.models" not in text
    assert "src.eeg" not in text
    assert "src.app" not in text


class ReplanSafety(SafetyController):
    def check(self, environment: SearchRescueEnvironment, **kwargs: object) -> SafetyDecision:
        return SafetyDecision(SafetyStatus.REPLAN_REQUIRED, kwargs["proposed_action"], None, False, InterventionType.BLOCKED_CELL, "test replan", True, kwargs["current_position"], None)
