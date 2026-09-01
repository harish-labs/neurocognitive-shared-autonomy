from __future__ import annotations

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import src.control.navigation_runtime as navigation_runtime
from src.autonomy.environment import Action, EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.planner import PlannerStatus, PlanningResult
from src.autonomy.safety import InterventionType, SafetyController, SafetyDecision, SafetyStatus
from src.control.human_interaction import HumanCommand, HumanCommandType, HumanInteractionController
from src.control.interaction_bridge import authorize_shared_autonomy_decision
from src.control.navigation_runtime import NavigationRuntime, NavigationStatus
from src.control.shared_autonomy import AutonomyMode, HumanAction, SharedAutonomyDecision


def make_environment(
    *,
    goals: dict[str, tuple[int, int]] | None = None,
    blocked_cells: frozenset[tuple[int, int]] = frozenset(),
    risk_map: dict[tuple[int, int], float] | None = None,
) -> SearchRescueEnvironment:
    return SearchRescueEnvironment(
        EnvironmentConfig(
            rows=3,
            columns=5,
            start=(1, 0),
            goals={"victim_a": (1, 4), "victim_b": (0, 2)} if goals is None else goals,
            blocked_cells=blocked_cells,
            risk_map={} if risk_map is None else risk_map,
        )
    )


def proceed(goal: str = "victim_a") -> SharedAutonomyDecision:
    return SharedAutonomyDecision(
        mode=AutonomyMode.PROCEED,
        candidate_goal=goal,
        approved_goal=goal,
        requires_human_confirmation=False,
        holds_position=False,
        requests_human_input=False,
        human_action=HumanAction.NONE,
        posterior_confidence=0.9,
        entropy_bits=0.4,
        update_count=1,
        reason="synthetic accepted proceed",
    )


def fresh_proceed(environment: SearchRescueEnvironment, controller: HumanInteractionController, goal: str = "victim_a"):
    return authorize_shared_autonomy_decision(proceed(goal), controller, goal_registry=environment.config.goals)


def start_ready(
    environment: SearchRescueEnvironment,
    controller: HumanInteractionController | None = None,
    *,
    execution_id: str = "execution-1",
    runtime: NavigationRuntime | None = None,
):
    actual_controller = HumanInteractionController() if controller is None else controller
    actual_runtime = NavigationRuntime() if runtime is None else runtime
    authorization = fresh_proceed(environment, actual_controller)
    result = actual_runtime.start_navigation(environment, actual_controller, authorization, execution_id=execution_id)
    return actual_runtime, actual_controller, result


def test_start_navigation_performs_zero_movement_for_exact_proceed_authorization(monkeypatch: pytest.MonkeyPatch) -> None:
    environment = make_environment()
    step_calls: list[Action] = []
    original_step = environment.step
    monkeypatch.setattr(environment, "step", lambda action: step_calls.append(action))

    runtime, controller, result = start_ready(environment)

    assert result.status is NavigationStatus.READY
    assert result.position_before == result.position_after == (1, 0)
    assert not result.moved
    assert step_calls == []
    assert runtime.session is not None and runtime.session.symbolic_goal == controller.state.approved_goal
    monkeypatch.setattr(environment, "step", original_step)


def test_repeated_non_adopting_proceed_cannot_start_navigation() -> None:
    environment = make_environment()
    controller = HumanInteractionController()
    first = fresh_proceed(environment, controller)
    repeated = fresh_proceed(environment, controller)

    result = NavigationRuntime().start_navigation(environment, controller, repeated, execution_id="execution-1")

    assert first.policy_goal_adopted
    assert not repeated.policy_goal_adopted
    assert result.status is NavigationStatus.INVALID_AUTHORIZATION
    assert environment.state.position == (1, 0)


def test_applied_confirm_override_and_resume_are_fresh_authorization_sources() -> None:
    environment = make_environment()

    confirmed = HumanInteractionController()
    confirmed.open_confirmation_request("request-1", "victim_a")
    confirm_result = confirmed.handle_command(HumanCommand("confirm", HumanCommandType.CONFIRM, request_id="request-1"))
    confirm_start = NavigationRuntime().start_navigation(environment, confirmed, confirm_result, execution_id="confirm")

    overridden = HumanInteractionController()
    override_result = overridden.handle_command(
        HumanCommand("override", HumanCommandType.OVERRIDE, goal="victim_a"), valid_goals=environment.config.goals
    )
    override_start = NavigationRuntime().start_navigation(environment, overridden, override_result, execution_id="override")

    resumed = HumanInteractionController()
    resumed.handle_command(HumanCommand("override", HumanCommandType.OVERRIDE, goal="victim_a"), valid_goals=environment.config.goals)
    resumed.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
    resume_result = resumed.handle_command(HumanCommand("resume", HumanCommandType.RESUME))
    resume_start = NavigationRuntime().start_navigation(environment, resumed, resume_result, execution_id="resume")

    assert all(result.status is NavigationStatus.READY for result in (confirm_start, override_start, resume_start))


def test_invalid_and_duplicate_command_results_cannot_start() -> None:
    environment = make_environment()
    controller = HumanInteractionController()
    invalid = controller.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
    duplicate = controller.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))

    first = NavigationRuntime().start_navigation(environment, controller, invalid, execution_id="invalid")
    second = NavigationRuntime().start_navigation(environment, controller, duplicate, execution_id="duplicate")

    assert first.status is second.status is NavigationStatus.INVALID_AUTHORIZATION


def test_exact_symbolic_goal_resolution_rejects_missing_key_and_does_not_value_match() -> None:
    environment = make_environment(goals={"victim_a": (1, 4)})
    controller = HumanInteractionController()
    override = controller.handle_command(
        HumanCommand("override", HumanCommandType.OVERRIDE, goal="(1, 4)"), valid_goals={"(1, 4)"}
    )

    result = NavigationRuntime().start_navigation(environment, controller, override, execution_id="execution-1")

    assert result.status is NavigationStatus.INVALID_GOAL_OR_PLAN
    assert not result.moved


def test_malformed_success_plan_and_other_terminal_goal_path_fail_closed_before_movement() -> None:
    environment = make_environment()
    controller = HumanInteractionController()
    authorization = fresh_proceed(environment, controller)
    malformed = FixedPlanner(path=((1, 0), (1, 4)), actions=(Action.RIGHT,), goal=(1, 4))
    malformed_result = NavigationRuntime(planner=malformed).start_navigation(environment, controller, authorization, execution_id="bad-plan")

    second_controller = HumanInteractionController()
    second_authorization = fresh_proceed(environment, second_controller)
    crosses_other_goal = FixedPlanner(
        path=((1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4)),
        actions=(Action.UP, Action.RIGHT, Action.RIGHT, Action.RIGHT, Action.RIGHT, Action.DOWN),
        goal=(1, 4),
    )
    terminal_result = NavigationRuntime(planner=crosses_other_goal).start_navigation(
        environment, second_controller, second_authorization, execution_id="wrong-terminal"
    )

    assert malformed_result.status is NavigationStatus.INVALID_GOAL_OR_PLAN
    assert terminal_result.status is NavigationStatus.INVALID_GOAL_OR_PLAN
    assert environment.state.position == (1, 0)


def test_advance_executes_at_most_one_step_and_safety_is_immediately_before_step(monkeypatch: pytest.MonkeyPatch) -> None:
    environment = make_environment()
    events: list[str] = []
    safety = RecordingSafety(events)
    runtime, controller, ready = start_ready(environment, runtime=NavigationRuntime(safety_controller=safety))
    original_step = environment.step

    def recording_step(action: Action):
        assert events[-1] == "safety"
        events.append("step")
        return original_step(action)

    monkeypatch.setattr(environment, "step", recording_step)
    result = runtime.advance_one_step(environment, controller)

    assert ready.status is NavigationStatus.READY
    assert result.status is NavigationStatus.STEP_EXECUTED
    assert result.moved
    assert result.position_before == (1, 0)
    assert result.position_after == (1, 1)
    assert events == ["safety", "step"]
    assert result.remaining_action_count == len(ready.path) - 2


def test_pause_stop_override_and_active_confirmation_between_steps_close_old_plan() -> None:
    for authority in ("pause", "stop", "override", "confirm"):
        environment = make_environment()
        runtime, controller, _ = start_ready(environment)
        runtime.advance_one_step(environment, controller)
        position = environment.state.position
        if authority == "pause":
            controller.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
            expected = NavigationStatus.PAUSED
        elif authority == "stop":
            controller.handle_command(HumanCommand("stop", HumanCommandType.STOP))
            expected = NavigationStatus.STOPPED
        elif authority == "override":
            controller.handle_command(
                HumanCommand("override", HumanCommandType.OVERRIDE, goal="victim_b"), valid_goals=environment.config.goals
            )
            expected = NavigationStatus.STALE_STATE
        else:
            controller.open_confirmation_request("request-1", "victim_b")
            expected = NavigationStatus.HOLD

        result = runtime.advance_one_step(environment, controller)

        assert result.status is expected
        assert not result.moved
        assert environment.state.position == position
        assert runtime.session is not None and not runtime.session.active


def test_resume_requires_new_execution_id_and_fresh_plan_from_current_position() -> None:
    environment = make_environment()
    runtime, controller, _ = start_ready(environment)
    runtime.advance_one_step(environment, controller)
    controller.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
    paused = runtime.advance_one_step(environment, controller)
    resume = controller.handle_command(HumanCommand("resume", HumanCommandType.RESUME))

    replay = runtime.start_navigation(environment, controller, resume, execution_id="execution-1")
    restarted = runtime.start_navigation(environment, controller, resume, execution_id="execution-2")

    assert paused.status is NavigationStatus.PAUSED
    assert replay.status is NavigationStatus.ALREADY_CONSUMED
    assert restarted.status is NavigationStatus.READY
    assert restarted.path[0] == environment.state.position == (1, 1)


def test_map_mutation_and_external_position_change_fail_closed_before_next_step() -> None:
    goals = {"victim_a": (1, 4), "victim_b": (0, 2)}
    environment = make_environment(goals=goals)
    runtime, controller, _ = start_ready(environment)
    goals["new_goal"] = (2, 4)

    changed_map = runtime.advance_one_step(environment, controller)

    second_environment = make_environment()
    second_runtime, second_controller, _ = start_ready(second_environment)
    second_environment.step(Action.RIGHT)
    changed_position = second_runtime.advance_one_step(second_environment, second_controller)

    assert changed_map.status is changed_position.status is NavigationStatus.STALE_STATE
    assert not changed_map.moved and not changed_position.moved


def test_safety_rejection_and_replan_required_hold_without_movement_or_retry() -> None:
    environment = make_environment()
    rejected_runtime, rejected_controller, _ = start_ready(
        environment, runtime=NavigationRuntime(safety_controller=FixedSafety(SafetyStatus.REJECTED, False))
    )
    rejected = rejected_runtime.advance_one_step(environment, rejected_controller)

    replan_environment = make_environment()
    replan_runtime, replan_controller, _ = start_ready(
        replan_environment, runtime=NavigationRuntime(safety_controller=FixedSafety(SafetyStatus.REPLAN_REQUIRED, True))
    )
    replan = replan_runtime.advance_one_step(replan_environment, replan_controller)
    repeated = replan_runtime.advance_one_step(replan_environment, replan_controller)

    assert rejected.status is NavigationStatus.SAFETY_REJECTED
    assert replan.status is NavigationStatus.REPLAN_REQUIRED
    assert replan.requires_replan
    assert repeated.status is NavigationStatus.HOLD
    assert environment.state.position == replan_environment.state.position == (1, 0)


def test_no_safe_path_is_stationary_and_execution_id_cannot_replay() -> None:
    environment = make_environment(blocked_cells=frozenset({(0, 1), (1, 1), (2, 1)}))
    controller = HumanInteractionController()
    authorization = fresh_proceed(environment, controller)
    runtime = NavigationRuntime()

    first = runtime.start_navigation(environment, controller, authorization, execution_id="execution-1")
    duplicate = runtime.start_navigation(environment, controller, authorization, execution_id="execution-1")

    assert first.status is NavigationStatus.NO_SAFE_PATH
    assert duplicate.status is NavigationStatus.ALREADY_CONSUMED
    assert environment.state.position == (1, 0)


def test_exact_approved_goal_completion_and_wrong_goal_is_not_success() -> None:
    environment = make_environment(goals={"victim_a": (1, 1), "victim_b": (0, 2)})
    runtime, controller, _ = start_ready(environment)

    result = runtime.advance_one_step(environment, controller)

    assert result.status is NavigationStatus.GOAL_REACHED
    assert environment.state.reached_goal == "victim_a"
    assert not result.active and result.closed


def test_runtime_never_processes_human_commands_or_uses_whole_route_execution_or_replanning() -> None:
    source = Path(navigation_runtime.__file__).read_text(encoding="utf-8")

    assert ".handle_command(" not in source
    assert "PlannerSafetyEnvironmentExecutor" not in source
    assert "ControlledReplanningCoordinator" not in source
    assert "src.cognition" not in source
    assert "src.models" not in source
    assert "src.eeg" not in source
    assert "src.app" not in source


def test_identical_fresh_inputs_are_deterministic() -> None:
    def run() -> tuple[object, object, object]:
        environment = make_environment()
        runtime, controller, ready = start_ready(environment)
        advanced = runtime.advance_one_step(environment, controller)
        return ready, advanced, runtime.session

    assert run() == run()


class RecordingSafety(SafetyController):
    def __init__(self, events: list[str]) -> None:
        self._events = events

    def check(self, *args: object, **kwargs: object) -> SafetyDecision:
        self._events.append("safety")
        return super().check(*args, **kwargs)


class FixedSafety(SafetyController):
    def __init__(self, status: SafetyStatus, requires_replan: bool) -> None:
        self._status = status
        self._requires_replan = requires_replan

    def check(self, environment: SearchRescueEnvironment, **kwargs: object) -> SafetyDecision:
        return SafetyDecision(
            status=self._status,
            proposed_action=kwargs["proposed_action"],
            approved_action=None,
            safe=False,
            intervention_type=InterventionType.BLOCKED_CELL,
            reason="synthetic safety rejection",
            requires_replan=self._requires_replan,
            current_position=kwargs["current_position"],
            proposed_next_position=None,
        )


class FixedPlanner:
    def __init__(self, *, path: tuple[tuple[int, int], ...], actions: tuple[Action, ...], goal: tuple[int, int]) -> None:
        self._path = path
        self._actions = actions
        self._goal = goal

    def plan(self, environment: SearchRescueEnvironment, *, start: tuple[int, int], approved_goal: tuple[int, int]) -> PlanningResult:
        return PlanningResult(
            status=PlannerStatus.SUCCESS,
            start=start,
            goal=self._goal,
            path=self._path,
            actions=self._actions,
            path_cost=float(len(self._actions)),
            movement_cost=float(len(self._actions)),
            cumulative_risk=0.0,
            risk_cost=0.0,
            expanded_nodes=1,
        )
