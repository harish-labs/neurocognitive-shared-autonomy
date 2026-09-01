"""Controlled one-attempt replanning after an explicit environment-change event."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.autonomy.environment import Coordinate, SearchRescueEnvironment
from src.autonomy.execution import ExecutionResult, ExecutionStatus, PlannerSafetyEnvironmentExecutor
from src.autonomy.safety import SafetyDecision, SafetyStatus


class ReplanTrigger(str, Enum):
    ENVIRONMENT_CHANGED = "ENVIRONMENT_CHANGED"
    SAFETY_REPLAN_REQUIRED = "SAFETY_REPLAN_REQUIRED"


class ReplanningStatus(str, Enum):
    SUCCESS = "SUCCESS"
    NO_SAFE_PATH = "NO_SAFE_PATH"
    HALTED = "HALTED"
    SAFETY_REJECTED = "SAFETY_REJECTED"
    INVALID_CHANGE = "INVALID_CHANGE"
    INVALID_TRIGGER = "INVALID_TRIGGER"
    ALREADY_CONSUMED = "ALREADY_CONSUMED"
    INVALID_GOAL_OR_PLAN = "INVALID_GOAL_OR_PLAN"


@dataclass(frozen=True)
class ReplanningResult:
    """Immutable result of one event-bounded controlled replan attempt."""

    status: ReplanningStatus
    event_id: object
    trigger: object
    approved_goal: Coordinate
    original_position: Coordinate
    replacement_start: Coordinate | None
    replacement_environment_used: bool
    execution_result: ExecutionResult | None
    consumed_event: bool
    reason: str


class ControlledReplanningCoordinator:
    """Enforce D-066's explicit snapshot and one-attempt-per-event contract."""

    def __init__(self, *, executor: PlannerSafetyEnvironmentExecutor | None = None) -> None:
        self._executor = PlannerSafetyEnvironmentExecutor() if executor is None else executor
        self._consumed_event_ids: set[str] = set()

    def replan(
        self,
        current_environment: SearchRescueEnvironment,
        replacement_environment: SearchRescueEnvironment,
        *,
        event_id: object,
        trigger: object,
        approved_goal: Coordinate,
        safety_decision: SafetyDecision | None = None,
        paused: bool = False,
        emergency_stop: bool = False,
    ) -> ReplanningResult:
        """Validate one explicit replacement snapshot and delegate once to execution."""
        original_position = current_environment.state.position
        if not isinstance(event_id, str) or not event_id:
            return _result(
                ReplanningStatus.INVALID_TRIGGER,
                event_id,
                trigger,
                approved_goal,
                original_position,
                None,
                False,
                None,
                False,
                "A non-empty environment-change event ID is required.",
            )
        if event_id in self._consumed_event_ids:
            return _result(
                ReplanningStatus.ALREADY_CONSUMED,
                event_id,
                trigger,
                approved_goal,
                original_position,
                None,
                False,
                None,
                True,
                "This environment-change event has already been used for a replan attempt.",
            )
        if not _is_valid_trigger(trigger, safety_decision):
            return _result(
                ReplanningStatus.INVALID_TRIGGER,
                event_id,
                trigger,
                approved_goal,
                original_position,
                None,
                False,
                None,
                False,
                "The supplied trigger does not authorize controlled replanning.",
            )
        if not _is_valid_replacement_snapshot(current_environment, replacement_environment, approved_goal):
            return _result(
                ReplanningStatus.INVALID_CHANGE,
                event_id,
                trigger,
                approved_goal,
                original_position,
                _replacement_start(replacement_environment),
                False,
                None,
                False,
                "Replacement snapshot does not satisfy the D-066 environment-change contract.",
            )

        self._consumed_event_ids.add(event_id)
        execution_result = self._executor.execute(
            replacement_environment,
            approved_goal=approved_goal,
            paused=paused,
            emergency_stop=emergency_stop,
        )
        return _result(
            _status_from_execution(execution_result.status),
            event_id,
            trigger,
            approved_goal,
            original_position,
            replacement_environment.config.start,
            True,
            execution_result,
            True,
            execution_result.reason,
        )


def _is_valid_trigger(trigger: object, safety_decision: SafetyDecision | None) -> bool:
    if trigger is ReplanTrigger.ENVIRONMENT_CHANGED:
        return True
    if trigger is not ReplanTrigger.SAFETY_REPLAN_REQUIRED or not isinstance(safety_decision, SafetyDecision):
        return False
    return (
        safety_decision.status is not SafetyStatus.HALTED
        and not safety_decision.safe
        and safety_decision.approved_action is None
        and safety_decision.requires_replan
    )


def _is_valid_replacement_snapshot(
    current_environment: object,
    replacement_environment: object,
    approved_goal: Coordinate,
) -> bool:
    if not isinstance(current_environment, SearchRescueEnvironment):
        return False
    if not isinstance(replacement_environment, SearchRescueEnvironment) or replacement_environment is current_environment:
        return False
    current_config = current_environment.config
    replacement_config = replacement_environment.config
    if (replacement_config.rows, replacement_config.columns) != (current_config.rows, current_config.columns):
        return False
    if dict(replacement_config.goals) != dict(current_config.goals):
        return False
    current_position = current_environment.state.position
    if replacement_config.start != current_position or replacement_environment.state.position != current_position:
        return False
    if replacement_environment.state.terminated or replacement_environment.is_blocked(current_position):
        return False
    if replacement_environment.is_prohibited(current_position):
        return False
    if approved_goal not in current_config.goals.values() or approved_goal not in replacement_config.goals.values():
        return False
    return (
        replacement_config.blocked_cells != current_config.blocked_cells
        or dict(replacement_config.risk_map) != dict(current_config.risk_map)
    )


def _replacement_start(replacement_environment: object) -> Coordinate | None:
    if isinstance(replacement_environment, SearchRescueEnvironment):
        return replacement_environment.config.start
    return None


def _status_from_execution(status: ExecutionStatus) -> ReplanningStatus:
    return ReplanningStatus(status.value)


def _result(
    status: ReplanningStatus,
    event_id: object,
    trigger: object,
    approved_goal: Coordinate,
    original_position: Coordinate,
    replacement_start: Coordinate | None,
    replacement_environment_used: bool,
    execution_result: ExecutionResult | None,
    consumed_event: bool,
    reason: str,
) -> ReplanningResult:
    return ReplanningResult(
        status=status,
        event_id=event_id,
        trigger=trigger,
        approved_goal=approved_goal,
        original_position=original_position,
        replacement_start=replacement_start,
        replacement_environment_used=replacement_environment_used,
        execution_result=execution_result,
        consumed_event=consumed_event,
        reason=reason,
    )
