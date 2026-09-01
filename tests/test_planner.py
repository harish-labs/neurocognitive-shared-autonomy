from __future__ import annotations

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.autonomy.environment import Action, EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.planner import PlannerStatus, RiskAwareAStarPlanner, manhattan_distance, step_cost


def make_environment(
    *,
    rows: int = 3,
    columns: int = 4,
    start: tuple[int, int] = (1, 0),
    blocked_cells: frozenset[tuple[int, int]] = frozenset(),
    risk_map: dict[tuple[int, int], float] | None = None,
) -> SearchRescueEnvironment:
    return SearchRescueEnvironment(
        EnvironmentConfig(
            rows=rows,
            columns=columns,
            start=start,
            goals={"approved": (0, columns - 1)},
            blocked_cells=blocked_cells,
            risk_map={} if risk_map is None else risk_map,
        )
    )


def plan(environment: SearchRescueEnvironment, start: tuple[int, int], goal: tuple[int, int]):
    return RiskAwareAStarPlanner().plan(environment, start=start, approved_goal=goal)


def test_zero_risk_shortest_path_and_action_reconstruction() -> None:
    result = plan(make_environment(), (1, 0), (0, 3))

    assert result.status is PlannerStatus.SUCCESS
    assert result.path == ((1, 0), (0, 0), (0, 1), (0, 2), (0, 3))
    assert result.actions == (Action.UP, Action.RIGHT, Action.RIGHT, Action.RIGHT)
    assert len(result.actions) == len(result.path) - 1
    assert result.movement_cost == result.path_cost == 4.0
    assert result.cumulative_risk == result.risk_cost == 0.0


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    (((0, 0), (0, 0), 0), ((0, 0), (2, 3), 5), ((4, 1), (1, 5), 7)),
)
def test_manhattan_heuristic(first: tuple[int, int], second: tuple[int, int], expected: int) -> None:
    assert manhattan_distance(first, second) == expected


def test_start_equals_goal_has_zero_cost_without_start_risk_charge() -> None:
    env = make_environment(risk_map={(1, 0): 0.75})
    result = plan(env, (1, 0), (1, 0))

    assert result.status is PlannerStatus.SUCCESS
    assert result.path == ((1, 0),)
    assert result.actions == ()
    assert result.movement_cost == result.cumulative_risk == result.risk_cost == result.path_cost == 0.0


def test_blocked_and_prohibited_cells_never_appear_in_path() -> None:
    blocked = (1, 1)
    prohibited = (0, 2)
    result = plan(make_environment(blocked_cells=frozenset({blocked}), risk_map={prohibited: 1.0}), (1, 0), (0, 3))

    assert result.status is PlannerStatus.SUCCESS
    assert blocked not in result.path
    assert prohibited not in result.path


def test_high_risk_remains_traversable_when_it_is_the_only_route() -> None:
    high_risk = (0, 1)
    env = make_environment(rows=1, columns=3, start=(0, 0), risk_map={high_risk: 0.75})
    result = plan(env, (0, 0), (0, 2))

    assert result.status is PlannerStatus.SUCCESS
    assert high_risk in result.path
    assert result.cumulative_risk == 0.75
    assert result.risk_cost == 1.5
    assert result.path_cost == 3.5


def test_longer_lower_risk_route_beats_shorter_high_risk_route() -> None:
    env = make_environment(rows=3, columns=5, start=(1, 0), risk_map={(1, 1): 0.75, (1, 2): 0.75, (1, 3): 0.75})
    result = plan(env, (1, 0), (1, 4))

    assert result.status is PlannerStatus.SUCCESS
    assert len(result.actions) == 6
    assert all(cell[0] != 1 or cell in {(1, 0), (1, 4)} for cell in result.path)
    assert result.path_cost == 6.0


def test_cost_decomposition_uses_destination_risk_only() -> None:
    env = make_environment(rows=1, columns=3, start=(0, 0), risk_map={(0, 0): 0.75, (0, 1): 0.25, (0, 2): 0.5})
    result = plan(env, (0, 0), (0, 2))

    assert step_cost(0.25) == 1.5
    assert result.movement_cost == 2.0
    assert result.cumulative_risk == 0.75
    assert result.risk_cost == 1.5
    assert result.path_cost == 3.5


@pytest.mark.parametrize(
    ("start", "expected_status"),
    (((-1, 0), PlannerStatus.INVALID_START), ((0, 1), PlannerStatus.INVALID_START), ((0, 2), PlannerStatus.INVALID_START)),
)
def test_invalid_blocked_and_prohibited_start_are_explicit(
    start: tuple[int, int], expected_status: PlannerStatus
) -> None:
    env = make_environment(rows=1, columns=3, start=(0, 0), blocked_cells=frozenset({(0, 1)}), risk_map={(0, 2): 1.0})
    assert plan(env, start, (0, 0)).status is expected_status


@pytest.mark.parametrize("goal", ((-1, 0), (0, 1), (0, 2)))
def test_invalid_blocked_and_prohibited_goal_are_explicit(goal: tuple[int, int]) -> None:
    env = make_environment(rows=1, columns=3, start=(0, 0), blocked_cells=frozenset({(0, 1)}), risk_map={(0, 2): 1.0})
    assert plan(env, (0, 0), goal).status is PlannerStatus.INVALID_GOAL


def test_fully_separated_goal_returns_no_safe_path_without_substitution() -> None:
    approved_goal = (1, 2)
    env = make_environment(rows=3, columns=3, start=(1, 0), blocked_cells=frozenset({(0, 1), (1, 1), (2, 1)}))
    result = plan(env, (1, 0), approved_goal)

    assert result.status is PlannerStatus.NO_SAFE_PATH
    assert result.goal == approved_goal
    assert result.path == result.actions == ()


def test_identical_requests_are_deterministic_and_do_not_mutate_environment() -> None:
    env = make_environment(rows=3, columns=3, start=(1, 0))
    original_state = env.state

    first = plan(env, (1, 0), (1, 2))
    second = plan(env, (1, 0), (1, 2))

    assert first.path == second.path
    assert first.actions == second.actions
    assert env.state == original_state


def test_wait_is_never_introduced_into_successful_plan() -> None:
    result = plan(make_environment(), (1, 0), (0, 3))

    assert Action.WAIT not in result.actions
