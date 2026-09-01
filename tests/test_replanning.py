from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.autonomy.environment import Action, EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.execution import ExecutionStatus
from src.autonomy.replanning import ControlledReplanningCoordinator, ReplanningStatus, ReplanTrigger
from src.autonomy.safety import SafetyController, SafetyStatus


def make_environment(
    *,
    start: tuple[int, int] = (1, 0),
    blocked_cells: frozenset[tuple[int, int]] = frozenset(),
    risk_map: dict[tuple[int, int], float] | None = None,
) -> SearchRescueEnvironment:
    return SearchRescueEnvironment(
        EnvironmentConfig(
            rows=3,
            columns=5,
            start=start,
            goals={"approved-goal": (1, 4)},
            blocked_cells=blocked_cells,
            risk_map={} if risk_map is None else risk_map,
        )
    )


def replacement_for(current: SearchRescueEnvironment, **kwargs: object) -> SearchRescueEnvironment:
    return make_environment(start=current.state.position, **kwargs)


def replan(
    coordinator: ControlledReplanningCoordinator,
    current: SearchRescueEnvironment,
    replacement: SearchRescueEnvironment,
    *,
    event_id: str = "change-1",
    trigger: ReplanTrigger = ReplanTrigger.ENVIRONMENT_CHANGED,
    **kwargs: object,
):
    return coordinator.replan(
        current,
        replacement,
        event_id=event_id,
        trigger=trigger,
        approved_goal=(1, 4),
        **kwargs,
    )


def test_explicit_changed_snapshot_causes_one_controlled_replan_with_preserved_goal() -> None:
    current = make_environment()
    replacement = replacement_for(current, blocked_cells=frozenset({(0, 2)}))
    result = replan(ControlledReplanningCoordinator(), current, replacement)

    assert result.status is ReplanningStatus.SUCCESS
    assert result.original_position == result.replacement_start == (1, 0)
    assert result.approved_goal == (1, 4)
    assert result.replacement_environment_used
    assert result.consumed_event
    assert result.execution_result.status is ExecutionStatus.SUCCESS
    assert current.state.position == (1, 0)


def test_changed_blocked_cells_produce_new_valid_route() -> None:
    current = make_environment()
    replacement = replacement_for(current, blocked_cells=frozenset({(1, 1)}))
    result = replan(ControlledReplanningCoordinator(), current, replacement)

    assert result.status is ReplanningStatus.SUCCESS
    assert (1, 1) not in result.execution_result.visited_positions
    assert result.execution_result.final_position == (1, 4)


def test_changed_risk_map_produces_risk_aware_route() -> None:
    current = make_environment()
    replacement = replacement_for(current, risk_map={(1, 1): 0.75, (1, 2): 0.75, (1, 3): 0.75})
    result = replan(ControlledReplanningCoordinator(), current, replacement)

    assert result.status is ReplanningStatus.SUCCESS
    assert all(position[0] != 1 or position in {(1, 0), (1, 4)} for position in result.execution_result.visited_positions)


def test_unchanged_map_and_same_instance_are_invalid_without_execution() -> None:
    current = make_environment()
    coordinator = ControlledReplanningCoordinator()

    unchanged = replan(coordinator, current, replacement_for(current))
    same_instance = replan(coordinator, current, current, event_id="change-2")

    assert unchanged.status is same_instance.status is ReplanningStatus.INVALID_CHANGE
    assert not unchanged.replacement_environment_used
    assert not same_instance.replacement_environment_used
    assert current.state.position == (1, 0)


def test_replacement_requires_same_grid_and_named_goal_mapping() -> None:
    current = make_environment()
    wrong_grid = SearchRescueEnvironment(
        EnvironmentConfig(rows=4, columns=5, start=(1, 0), goals={"approved-goal": (1, 4)}, blocked_cells=frozenset({(0, 1)}))
    )
    wrong_goals = SearchRescueEnvironment(
        EnvironmentConfig(rows=3, columns=5, start=(1, 0), goals={"different-goal": (1, 3)}, blocked_cells=frozenset({(0, 1)}))
    )

    grid_result = replan(ControlledReplanningCoordinator(), current, wrong_grid)
    goal_result = replan(ControlledReplanningCoordinator(), current, wrong_goals)

    assert grid_result.status is goal_result.status is ReplanningStatus.INVALID_CHANGE
    assert not grid_result.replacement_environment_used
    assert not goal_result.replacement_environment_used


def test_duplicate_event_is_consumed_after_one_executor_attempt(monkeypatch) -> None:
    current = make_environment()
    coordinator = ControlledReplanningCoordinator()
    first_replacement = replacement_for(current, blocked_cells=frozenset({(0, 1)}))
    second_replacement = replacement_for(current, blocked_cells=frozenset({(0, 2)}))
    calls: list[object] = []
    original_execute = coordinator._executor.execute

    def counting_execute(*args: object, **kwargs: object):
        calls.append(args)
        return original_execute(*args, **kwargs)

    monkeypatch.setattr(coordinator._executor, "execute", counting_execute)
    first = replan(coordinator, current, first_replacement, event_id="change-1")
    second = replan(coordinator, current, second_replacement, event_id="change-1")

    assert first.consumed_event
    assert second.status is ReplanningStatus.ALREADY_CONSUMED
    assert len(calls) == 1


def test_safety_replan_trigger_requires_nonapproved_requires_replan_decision() -> None:
    current = make_environment()
    replacement = replacement_for(current, blocked_cells=frozenset({(0, 1)}))
    safety = SafetyController()
    valid_decision = safety.check(
        current,
        current_position=(1, 0),
        proposed_action=Action.RIGHT,
    )
    invalid_decision = safety.check(current, current_position=(1, 0), proposed_action=Action.UP)

    valid = replan(
        ControlledReplanningCoordinator(),
        current,
        replacement,
        trigger=ReplanTrigger.SAFETY_REPLAN_REQUIRED,
        safety_decision=SafetyController().check(
            make_environment(blocked_cells=frozenset({(1, 1)})), current_position=(1, 0), proposed_action=Action.RIGHT
        ),
    )
    invalid = replan(
        ControlledReplanningCoordinator(),
        current,
        replacement,
        event_id="change-2",
        trigger=ReplanTrigger.SAFETY_REPLAN_REQUIRED,
        safety_decision=invalid_decision,
    )

    assert valid.status is ReplanningStatus.SUCCESS
    assert invalid.status is ReplanningStatus.INVALID_TRIGGER
    assert valid_decision.status is SafetyStatus.APPROVED


def test_halted_safety_decision_cannot_trigger_replanning() -> None:
    current = make_environment()
    replacement = replacement_for(current, blocked_cells=frozenset({(0, 1)}))
    halted = SafetyController().check(current, current_position=(1, 0), proposed_action=Action.RIGHT, emergency_stop=True)
    result = replan(
        ControlledReplanningCoordinator(),
        current,
        replacement,
        trigger=ReplanTrigger.SAFETY_REPLAN_REQUIRED,
        safety_decision=halted,
    )

    assert halted.status is SafetyStatus.HALTED
    assert result.status is ReplanningStatus.INVALID_TRIGGER


def test_safety_replan_request_without_changed_snapshot_does_not_execute() -> None:
    current = make_environment(blocked_cells=frozenset({(1, 1)}))
    unchanged_replacement = replacement_for(current, blocked_cells=frozenset({(1, 1)}))
    decision = SafetyController().check(current, current_position=(1, 0), proposed_action=Action.RIGHT)
    result = replan(
        ControlledReplanningCoordinator(),
        current,
        unchanged_replacement,
        trigger=ReplanTrigger.SAFETY_REPLAN_REQUIRED,
        safety_decision=decision,
    )

    assert decision.requires_replan
    assert result.status is ReplanningStatus.INVALID_CHANGE
    assert result.execution_result is None
    assert unchanged_replacement.state.position == (1, 0)


def test_no_safe_path_holds_replacement_at_preserved_start_and_does_not_retry() -> None:
    current = make_environment()
    replacement = replacement_for(current, blocked_cells=frozenset({(0, 1), (1, 1), (2, 1)}))
    coordinator = ControlledReplanningCoordinator()
    first = replan(coordinator, current, replacement)
    duplicate = replan(coordinator, current, replacement)

    assert first.status is ReplanningStatus.NO_SAFE_PATH
    assert first.execution_result.executed_actions == ()
    assert replacement.state.position == (1, 0)
    assert duplicate.status is ReplanningStatus.ALREADY_CONSUMED


def test_pause_and_stop_halt_valid_change_without_movement() -> None:
    current = make_environment()
    paused_replacement = replacement_for(current, blocked_cells=frozenset({(0, 1)}))
    stopped_replacement = replacement_for(current, blocked_cells=frozenset({(0, 2)}))

    paused = replan(ControlledReplanningCoordinator(), current, paused_replacement, paused=True)
    stopped = replan(ControlledReplanningCoordinator(), current, stopped_replacement, emergency_stop=True)

    assert paused.status is stopped.status is ReplanningStatus.HALTED
    assert paused.execution_result.executed_actions == stopped.execution_result.executed_actions == ()
    assert paused_replacement.state.position == stopped_replacement.state.position == (1, 0)


def test_high_risk_remains_traversable_and_valid_calls_are_deterministic() -> None:
    first_current = make_environment()
    second_current = make_environment()
    first = replan(
        ControlledReplanningCoordinator(),
        first_current,
        replacement_for(first_current, risk_map={(0, 1): 0.75}),
    )
    second = replan(
        ControlledReplanningCoordinator(),
        second_current,
        replacement_for(second_current, risk_map={(0, 1): 0.75}),
    )

    assert first == second
    assert first.status is ReplanningStatus.SUCCESS


def test_prohibited_constraints_remain_enforced() -> None:
    current = make_environment()
    replacement = replacement_for(current, risk_map={(0, 1): 1.0, (1, 1): 1.0, (2, 1): 1.0})
    result = replan(ControlledReplanningCoordinator(), current, replacement)

    assert result.status is ReplanningStatus.NO_SAFE_PATH
    assert replacement.state.position == (1, 0)
