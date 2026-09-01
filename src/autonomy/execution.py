"""One-route planner-to-safety-to-environment execution orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.autonomy.environment import ACTION_DELTAS, Action, Coordinate, SearchRescueEnvironment
from src.autonomy.planner import PlannerStatus, PlanningResult, RiskAwareAStarPlanner
from src.autonomy.safety import SafetyController, SafetyDecision, SafetyStatus


class ExecutionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    NO_SAFE_PATH = "NO_SAFE_PATH"
    SAFETY_REJECTED = "SAFETY_REJECTED"
    HALTED = "HALTED"
    INVALID_GOAL_OR_PLAN = "INVALID_GOAL_OR_PLAN"


@dataclass(frozen=True)
class ExecutionResult:
    """Immutable trace for one fixed-goal execution attempt."""

    status: ExecutionStatus
    approved_goal: Coordinate
    planning_result: PlanningResult | None
    executed_actions: tuple[Action, ...]
    visited_positions: tuple[Coordinate, ...]
    safety_decisions: tuple[SafetyDecision, ...]
    final_position: Coordinate
    terminated: bool
    reason: str


class PlannerSafetyEnvironmentExecutor:
    """Execute a single static plan with explicit safety authorization per action."""

    def __init__(
        self,
        *,
        planner: RiskAwareAStarPlanner | None = None,
        safety_controller: SafetyController | None = None,
    ) -> None:
        self._planner = RiskAwareAStarPlanner() if planner is None else planner
        self._safety_controller = SafetyController() if safety_controller is None else safety_controller

    def execute(
        self,
        environment: SearchRescueEnvironment,
        *,
        approved_goal: Coordinate,
        paused: bool = False,
        emergency_stop: bool = False,
    ) -> ExecutionResult:
        """Run an already-approved goal through planner, safety, then environment.

        This method deliberately performs no automatic replan after a rejection.
        """
        start = environment.state.position
        if approved_goal not in environment.config.goals.values():
            return _result(
                ExecutionStatus.INVALID_GOAL_OR_PLAN,
                approved_goal,
                None,
                (),
                (start,),
                (),
                environment,
                "Approved goal is not a configured environment goal.",
            )

        planning_result = self._planner.plan(environment, start=start, approved_goal=approved_goal)
        if planning_result.status is PlannerStatus.NO_SAFE_PATH:
            return _result(
                ExecutionStatus.NO_SAFE_PATH,
                approved_goal,
                planning_result,
                (),
                (start,),
                (),
                environment,
                "Planner reported no safe route to the approved goal.",
            )
        if planning_result.status is not PlannerStatus.SUCCESS:
            return _result(
                ExecutionStatus.INVALID_GOAL_OR_PLAN,
                approved_goal,
                planning_result,
                (),
                (start,),
                (),
                environment,
                "Planner could not produce a valid plan for the approved goal.",
            )
        if not _is_consistent_success_plan(planning_result, start, approved_goal):
            return _result(
                ExecutionStatus.INVALID_GOAL_OR_PLAN,
                approved_goal,
                planning_result,
                (),
                (start,),
                (),
                environment,
                "Planner SUCCESS result is structurally inconsistent with the execution request.",
            )

        executed_actions: list[Action] = []
        visited_positions: list[Coordinate] = [start]
        safety_decisions: list[SafetyDecision] = []
        for action in planning_result.actions:
            decision = self._safety_controller.check(
                environment,
                current_position=environment.state.position,
                proposed_action=action,
                paused=paused,
                emergency_stop=emergency_stop,
            )
            safety_decisions.append(decision)
            if decision.status is SafetyStatus.HALTED:
                return _result(
                    ExecutionStatus.HALTED,
                    approved_goal,
                    planning_result,
                    tuple(executed_actions),
                    tuple(visited_positions),
                    tuple(safety_decisions),
                    environment,
                    decision.reason,
                )
            if decision.status is not SafetyStatus.APPROVED or decision.approved_action is None:
                return _result(
                    ExecutionStatus.SAFETY_REJECTED,
                    approved_goal,
                    planning_result,
                    tuple(executed_actions),
                    tuple(visited_positions),
                    tuple(safety_decisions),
                    environment,
                    decision.reason,
                )

            environment.step(decision.approved_action)
            executed_actions.append(decision.approved_action)
            visited_positions.append(environment.state.position)

        if environment.state.position != approved_goal or not environment.state.terminated:
            return _result(
                ExecutionStatus.INVALID_GOAL_OR_PLAN,
                approved_goal,
                planning_result,
                tuple(executed_actions),
                tuple(visited_positions),
                tuple(safety_decisions),
                environment,
                "Execution ended without reaching and terminating at the approved goal.",
            )
        return _result(
            ExecutionStatus.SUCCESS,
            approved_goal,
            planning_result,
            tuple(executed_actions),
            tuple(visited_positions),
            tuple(safety_decisions),
            environment,
            "Approved goal reached through planner, safety, and environment execution.",
        )


def _result(
    status: ExecutionStatus,
    approved_goal: Coordinate,
    planning_result: PlanningResult | None,
    executed_actions: tuple[Action, ...],
    visited_positions: tuple[Coordinate, ...],
    safety_decisions: tuple[SafetyDecision, ...],
    environment: SearchRescueEnvironment,
    reason: str,
) -> ExecutionResult:
    return ExecutionResult(
        status=status,
        approved_goal=approved_goal,
        planning_result=planning_result,
        executed_actions=executed_actions,
        visited_positions=visited_positions,
        safety_decisions=safety_decisions,
        final_position=environment.state.position,
        terminated=environment.state.terminated,
        reason=reason,
    )


def _is_consistent_success_plan(
    planning_result: PlanningResult,
    start: Coordinate,
    approved_goal: Coordinate,
) -> bool:
    """Fail closed unless the successful route exactly reconstructs the fixed request."""
    if planning_result.start != start or planning_result.goal != approved_goal:
        return False
    path = planning_result.path
    actions = planning_result.actions
    if not path or path[0] != start or path[-1] != approved_goal:
        return False
    if len(actions) != len(path) - 1:
        return False
    if any(not _is_coordinate(position) for position in path):
        return False
    for position, action, next_position in zip(path, actions, path[1:]):
        if not isinstance(action, Action) or action is Action.WAIT:
            return False
        delta = ACTION_DELTAS[action]
        if (position[0] + delta[0], position[1] + delta[1]) != next_position:
            return False
    return True


def _is_coordinate(value: object) -> bool:
    return isinstance(value, tuple) and len(value) == 2 and all(isinstance(item, int) for item in value)
