"""Deterministic risk-aware A* planning over the approved static SAR map."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from heapq import heappop, heappush
from itertools import count

from src.autonomy.environment import ACTION_DELTAS, Action, Coordinate, SearchRescueEnvironment


RISK_LAMBDA = 2.0


class PlannerStatus(str, Enum):
    SUCCESS = "SUCCESS"
    NO_SAFE_PATH = "NO_SAFE_PATH"
    INVALID_START = "INVALID_START"
    INVALID_GOAL = "INVALID_GOAL"


@dataclass(frozen=True)
class PlanningResult:
    """Read-only result of planning toward the caller-supplied approved goal."""

    status: PlannerStatus
    start: Coordinate
    goal: Coordinate
    path: tuple[Coordinate, ...]
    actions: tuple[Action, ...]
    path_cost: float | None
    movement_cost: float | None
    cumulative_risk: float | None
    risk_cost: float | None
    expanded_nodes: int


class RiskAwareAStarPlanner:
    """A* planner that reads map state but never executes environment transitions."""

    def plan(
        self,
        environment: SearchRescueEnvironment,
        *,
        start: Coordinate,
        approved_goal: Coordinate,
    ) -> PlanningResult:
        """Plan from ``start`` to the fixed, already-approved goal.

        Risk is charged only when entering a destination cell.  Cells that are
        blocked or have risk at least 1.00 are never considered traversable.
        """
        if not _is_valid_traversable_coordinate(environment, start):
            return _failure_result(PlannerStatus.INVALID_START, start, approved_goal)
        if not _is_valid_traversable_coordinate(environment, approved_goal):
            return _failure_result(PlannerStatus.INVALID_GOAL, start, approved_goal)
        if start == approved_goal:
            return PlanningResult(
                status=PlannerStatus.SUCCESS,
                start=start,
                goal=approved_goal,
                path=(start,),
                actions=(),
                path_cost=0.0,
                movement_cost=0.0,
                cumulative_risk=0.0,
                risk_cost=0.0,
                expanded_nodes=0,
            )

        frontier: list[tuple[float, float, int, Coordinate]] = []
        sequence = count()
        heappush(frontier, (manhattan_distance(start, approved_goal), 0.0, next(sequence), start))
        parent: dict[Coordinate, tuple[Coordinate, Action]] = {}
        best_cost: dict[Coordinate, float] = {start: 0.0}
        expanded_nodes = 0

        while frontier:
            _, current_cost, _, current = heappop(frontier)
            if current_cost != best_cost.get(current):
                continue
            expanded_nodes += 1
            if current == approved_goal:
                path, actions = _reconstruct_path(parent, start, approved_goal)
                return _success_result(environment, start, approved_goal, path, actions, expanded_nodes)

            for action in (Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT):
                delta = ACTION_DELTAS[action]
                neighbor = (current[0] + delta[0], current[1] + delta[1])
                if not _is_valid_traversable_coordinate(environment, neighbor):
                    continue
                candidate_cost = current_cost + step_cost(environment.risk_at(neighbor))
                if candidate_cost >= best_cost.get(neighbor, float("inf")):
                    continue
                best_cost[neighbor] = candidate_cost
                parent[neighbor] = (current, action)
                heuristic = manhattan_distance(neighbor, approved_goal)
                heappush(frontier, (candidate_cost + heuristic, candidate_cost, next(sequence), neighbor))

        return _failure_result(PlannerStatus.NO_SAFE_PATH, start, approved_goal, expanded_nodes)


def manhattan_distance(first: Coordinate, second: Coordinate) -> int:
    """Four-connected lower-bound distance without a hidden risk term."""
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def step_cost(destination_risk: float) -> float:
    """Approved D-063 cost for entering one traversable destination cell."""
    return 1.0 + RISK_LAMBDA * destination_risk


def _is_valid_traversable_coordinate(environment: SearchRescueEnvironment, coordinate: object) -> bool:
    if not _is_coordinate(coordinate) or not environment.in_bounds(coordinate):
        return False
    return not environment.is_blocked(coordinate) and not environment.is_prohibited(coordinate)


def _is_coordinate(value: object) -> bool:
    return isinstance(value, tuple) and len(value) == 2 and all(isinstance(item, int) for item in value)


def _reconstruct_path(
    parent: dict[Coordinate, tuple[Coordinate, Action]], start: Coordinate, goal: Coordinate
) -> tuple[tuple[Coordinate, ...], tuple[Action, ...]]:
    reverse_path = [goal]
    reverse_actions: list[Action] = []
    current = goal
    while current != start:
        previous, action = parent[current]
        reverse_path.append(previous)
        reverse_actions.append(action)
        current = previous
    reverse_path.reverse()
    reverse_actions.reverse()
    return tuple(reverse_path), tuple(reverse_actions)


def _success_result(
    environment: SearchRescueEnvironment,
    start: Coordinate,
    goal: Coordinate,
    path: tuple[Coordinate, ...],
    actions: tuple[Action, ...],
    expanded_nodes: int,
) -> PlanningResult:
    movement_cost = float(len(actions))
    cumulative_risk = sum(environment.risk_at(cell) for cell in path[1:])
    risk_cost = RISK_LAMBDA * cumulative_risk
    return PlanningResult(
        status=PlannerStatus.SUCCESS,
        start=start,
        goal=goal,
        path=path,
        actions=actions,
        path_cost=movement_cost + risk_cost,
        movement_cost=movement_cost,
        cumulative_risk=cumulative_risk,
        risk_cost=risk_cost,
        expanded_nodes=expanded_nodes,
    )


def _failure_result(
    status: PlannerStatus,
    start: Coordinate,
    goal: Coordinate,
    expanded_nodes: int = 0,
) -> PlanningResult:
    return PlanningResult(
        status=status,
        start=start,
        goal=goal,
        path=(),
        actions=(),
        path_cost=None,
        movement_cost=None,
        cumulative_risk=None,
        risk_cost=None,
        expanded_nodes=expanded_nodes,
    )
