from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.autonomy.environment import Action, EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.execution import ExecutionStatus, PlannerSafetyEnvironmentExecutor
from src.autonomy.planner import PlannerStatus, PlanningResult
from src.autonomy.safety import SafetyController, SafetyStatus


def make_environment(
    *,
    rows: int = 3,
    columns: int = 4,
    start: tuple[int, int] = (1, 0),
    goal: tuple[int, int] = (0, 3),
    blocked_cells: frozenset[tuple[int, int]] = frozenset(),
    risk_map: dict[tuple[int, int], float] | None = None,
) -> SearchRescueEnvironment:
    return SearchRescueEnvironment(
        EnvironmentConfig(
            rows=rows,
            columns=columns,
            start=start,
            goals={"approved-goal": goal},
            blocked_cells=blocked_cells,
            risk_map={} if risk_map is None else risk_map,
        )
    )


def execute(environment: SearchRescueEnvironment, goal: tuple[int, int], **kwargs: object):
    return PlannerSafetyEnvironmentExecutor().execute(environment, approved_goal=goal, **kwargs)


def test_successful_zero_risk_execution_reaches_fixed_approved_goal() -> None:
    env = make_environment()
    result = execute(env, (0, 3))

    assert result.status is ExecutionStatus.SUCCESS
    assert result.approved_goal == (0, 3)
    assert result.final_position == (0, 3)
    assert result.terminated
    assert result.executed_actions == result.planning_result.actions
    assert result.visited_positions[0] == (1, 0)
    assert result.visited_positions[-1] == result.approved_goal


def test_risk_aware_planner_route_is_followed() -> None:
    env = make_environment(
        rows=3,
        columns=5,
        start=(1, 0),
        goal=(1, 4),
        risk_map={(1, 1): 0.75, (1, 2): 0.75, (1, 3): 0.75},
    )
    result = execute(env, (1, 4))

    assert result.status is ExecutionStatus.SUCCESS
    assert result.executed_actions == result.planning_result.actions
    assert len(result.executed_actions) == 6
    assert all(position[0] != 1 or position in {(1, 0), (1, 4)} for position in result.visited_positions)


def test_safety_is_checked_before_every_environment_step(monkeypatch) -> None:
    env = make_environment()
    safety = RecordingSafetyController()
    executor = PlannerSafetyEnvironmentExecutor(safety_controller=safety)
    original_step = env.step

    def checked_step(action: object):
        assert len(safety.decisions) == len(executed_before_step) + 1
        executed_before_step.append(action)
        return original_step(action)

    executed_before_step: list[object] = []
    monkeypatch.setattr(env, "step", checked_step)
    result = executor.execute(env, approved_goal=(0, 3))

    assert result.status is ExecutionStatus.SUCCESS
    assert len(safety.decisions) == len(result.executed_actions)


def test_high_risk_route_executes_when_planner_and_safety_permit_it() -> None:
    env = make_environment(rows=1, columns=3, start=(0, 0), goal=(0, 2), risk_map={(0, 1): 0.75})
    result = execute(env, (0, 2))

    assert result.status is ExecutionStatus.SUCCESS
    assert result.visited_positions == ((0, 0), (0, 1), (0, 2))
    assert all(decision.status is SafetyStatus.APPROVED for decision in result.safety_decisions)


def test_no_safe_path_causes_zero_movement_and_preserves_goal() -> None:
    env = make_environment(rows=3, columns=3, start=(1, 0), goal=(1, 2), blocked_cells=frozenset({(0, 1), (1, 1), (2, 1)}))
    result = execute(env, (1, 2))

    assert result.status is ExecutionStatus.NO_SAFE_PATH
    assert result.approved_goal == (1, 2)
    assert result.executed_actions == result.safety_decisions == ()
    assert result.visited_positions == ((1, 0),)
    assert result.final_position == (1, 0)


def test_emergency_stop_halts_before_any_movement() -> None:
    env = make_environment()
    result = execute(env, (0, 3), emergency_stop=True)

    assert result.status is ExecutionStatus.HALTED
    assert result.executed_actions == ()
    assert result.final_position == (1, 0)
    assert result.safety_decisions[0].status is SafetyStatus.HALTED


def test_pause_halts_before_any_movement() -> None:
    env = make_environment()
    result = execute(env, (0, 3), paused=True)

    assert result.status is ExecutionStatus.HALTED
    assert result.executed_actions == ()
    assert result.final_position == (1, 0)
    assert result.safety_decisions[0].status is SafetyStatus.HALTED


def test_blocked_action_from_a_proposed_successful_plan_is_not_executed() -> None:
    env = make_environment(blocked_cells=frozenset({(1, 1)}), goal=(1, 1))
    planner = FixedActionPlanner(goal=(1, 1), action=Action.RIGHT)
    result = PlannerSafetyEnvironmentExecutor(planner=planner).execute(env, approved_goal=(1, 1))

    assert result.status is ExecutionStatus.SAFETY_REJECTED
    assert result.executed_actions == ()
    assert result.final_position == (1, 0)
    assert result.safety_decisions[0].requires_replan


def test_prohibited_action_from_a_proposed_successful_plan_is_not_executed() -> None:
    env = make_environment(risk_map={(1, 1): 1.0}, goal=(1, 1))
    planner = FixedActionPlanner(goal=(1, 1), action=Action.RIGHT)
    result = PlannerSafetyEnvironmentExecutor(planner=planner).execute(env, approved_goal=(1, 1))

    assert result.status is ExecutionStatus.SAFETY_REJECTED
    assert result.executed_actions == ()
    assert result.final_position == (1, 0)
    assert result.safety_decisions[0].requires_replan


def test_trace_is_deterministic_and_internally_consistent() -> None:
    first = execute(make_environment(), (0, 3))
    second = execute(make_environment(), (0, 3))

    assert first == second
    assert len(first.visited_positions) == len(first.executed_actions) + 1
    assert len(first.safety_decisions) == len(first.executed_actions)
    assert all(decision.approved_action is action for decision, action in zip(first.safety_decisions, first.executed_actions))


def test_unknown_goal_is_not_substituted_or_executed() -> None:
    env = make_environment()
    result = execute(env, (2, 3))

    assert result.status is ExecutionStatus.INVALID_GOAL_OR_PLAN
    assert result.approved_goal == (2, 3)
    assert result.executed_actions == ()
    assert result.final_position == (1, 0)


def test_success_result_for_different_goal_is_rejected_before_safety_or_execution(monkeypatch) -> None:
    env = make_environment()
    safety = RecordingSafetyController()
    planner = FixedActionPlanner(goal=(2, 3), path=((1, 0), (2, 3)), actions=(Action.DOWN,))
    step_calls: list[object] = []
    monkeypatch.setattr(env, "step", lambda action: step_calls.append(action))

    result = PlannerSafetyEnvironmentExecutor(planner=planner, safety_controller=safety).execute(env, approved_goal=(0, 3))

    assert_malformed_plan_rejected(result, env, (0, 3))
    assert safety.decisions == []
    assert step_calls == []


def test_inconsistent_success_path_is_rejected_before_safety_or_execution(monkeypatch) -> None:
    env = make_environment()
    safety = RecordingSafetyController()
    planner = FixedActionPlanner(goal=(0, 3), path=((1, 0), (0, 3)), actions=(Action.RIGHT,))
    step_calls: list[object] = []
    monkeypatch.setattr(env, "step", lambda action: step_calls.append(action))

    result = PlannerSafetyEnvironmentExecutor(planner=planner, safety_controller=safety).execute(env, approved_goal=(0, 3))

    assert_malformed_plan_rejected(result, env, (0, 3))
    assert safety.decisions == []
    assert step_calls == []


class RecordingSafetyController(SafetyController):
    def __init__(self) -> None:
        self.decisions = []

    def check(self, *args: object, **kwargs: object):
        decision = super().check(*args, **kwargs)
        self.decisions.append(decision)
        return decision


class FixedActionPlanner:
    def __init__(
        self,
        *,
        goal: tuple[int, int],
        action: Action | None = None,
        path: tuple[tuple[int, int], ...] | None = None,
        actions: tuple[Action, ...] | None = None,
    ) -> None:
        self._goal = goal
        self._action = action
        self._path = path
        self._actions = actions

    def plan(self, environment: SearchRescueEnvironment, *, start: tuple[int, int], approved_goal: tuple[int, int]) -> PlanningResult:
        path = self._path if self._path is not None else (start, self._goal)
        actions = self._actions if self._actions is not None else (self._action,)
        return PlanningResult(
            status=PlannerStatus.SUCCESS,
            start=start,
            goal=self._goal,
            path=path,
            actions=actions,
            path_cost=1.0,
            movement_cost=1.0,
            cumulative_risk=0.0,
            risk_cost=0.0,
            expanded_nodes=1,
        )


def assert_malformed_plan_rejected(result: object, environment: SearchRescueEnvironment, approved_goal: tuple[int, int]) -> None:
    assert getattr(result, "status") is ExecutionStatus.INVALID_GOAL_OR_PLAN
    assert getattr(result, "approved_goal") == approved_goal
    assert getattr(result, "executed_actions") == ()
    assert getattr(result, "visited_positions") == ((1, 0),)
    assert environment.state.position == (1, 0)
