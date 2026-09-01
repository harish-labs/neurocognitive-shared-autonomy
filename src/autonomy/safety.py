"""Hard-constraint safety checks between planner proposals and environment execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from numbers import Integral

from src.autonomy.environment import ACTION_DELTAS, Action, Coordinate, SearchRescueEnvironment


class SafetyStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REPLAN_REQUIRED = "REPLAN_REQUIRED"
    HALTED = "HALTED"


class InterventionType(str, Enum):
    NONE = "NONE"
    OUT_OF_BOUNDS = "OUT_OF_BOUNDS"
    BLOCKED_CELL = "BLOCKED_CELL"
    PROHIBITED_HAZARD = "PROHIBITED_HAZARD"
    PAUSED = "PAUSED"
    EMERGENCY_STOP = "EMERGENCY_STOP"
    INVALID_ACTION = "INVALID_ACTION"
    INVALID_STATE = "INVALID_STATE"


@dataclass(frozen=True)
class SafetyDecision:
    """Read-only authorization or rejection of one proposed environment action."""

    status: SafetyStatus
    proposed_action: object
    approved_action: Action | None
    safe: bool
    intervention_type: InterventionType
    reason: str
    requires_replan: bool
    current_position: object
    proposed_next_position: Coordinate | None


class SafetyController:
    """Validate a proposal without planning or executing an environment transition."""

    def check(
        self,
        environment: SearchRescueEnvironment,
        *,
        current_position: object,
        proposed_action: object,
        paused: bool = False,
        emergency_stop: bool = False,
    ) -> SafetyDecision:
        """Apply the approved deterministic hard-safety precedence order."""
        if emergency_stop:
            return _rejection(
                SafetyStatus.HALTED,
                proposed_action,
                current_position,
                InterventionType.EMERGENCY_STOP,
                "Emergency stop is active.",
            )
        if paused:
            return _rejection(
                SafetyStatus.HALTED,
                proposed_action,
                current_position,
                InterventionType.PAUSED,
                "Movement is paused.",
            )
        if not _is_valid_current_position(environment, current_position):
            return _rejection(
                SafetyStatus.HALTED,
                proposed_action,
                current_position,
                InterventionType.INVALID_STATE,
                "Current position is malformed, out of bounds, blocked, or prohibited.",
            )

        action = _normalize_action(proposed_action)
        if action is None:
            return _rejection(
                SafetyStatus.REJECTED,
                proposed_action,
                current_position,
                InterventionType.INVALID_ACTION,
                "Proposed action is outside the approved action vocabulary.",
            )

        delta = ACTION_DELTAS[action]
        next_position = (current_position[0] + delta[0], current_position[1] + delta[1])
        if not environment.in_bounds(next_position):
            return _rejection(
                SafetyStatus.REJECTED,
                proposed_action,
                current_position,
                InterventionType.OUT_OF_BOUNDS,
                "Proposed movement leaves the map bounds.",
                proposed_next_position=next_position,
                requires_replan=True,
            )
        if environment.is_blocked(next_position):
            return _rejection(
                SafetyStatus.REPLAN_REQUIRED,
                proposed_action,
                current_position,
                InterventionType.BLOCKED_CELL,
                "Proposed movement enters a blocked cell.",
                proposed_next_position=next_position,
                requires_replan=True,
            )
        if environment.is_prohibited(next_position):
            return _rejection(
                SafetyStatus.REPLAN_REQUIRED,
                proposed_action,
                current_position,
                InterventionType.PROHIBITED_HAZARD,
                "Proposed movement enters a prohibited hazard cell.",
                proposed_next_position=next_position,
                requires_replan=True,
            )
        return SafetyDecision(
            status=SafetyStatus.APPROVED,
            proposed_action=proposed_action,
            approved_action=action,
            safe=True,
            intervention_type=InterventionType.NONE,
            reason="Proposed action satisfies the current hard safety constraints.",
            requires_replan=False,
            current_position=current_position,
            proposed_next_position=next_position,
        )


def _is_valid_current_position(environment: SearchRescueEnvironment, position: object) -> bool:
    if not _is_coordinate(position) or not environment.in_bounds(position):
        return False
    return not environment.is_blocked(position) and not environment.is_prohibited(position)


def _normalize_action(action: object) -> Action | None:
    if isinstance(action, Action):
        return action
    if isinstance(action, bool) or not isinstance(action, Integral):
        return None
    try:
        return Action(action)
    except ValueError:
        return None


def _is_coordinate(value: object) -> bool:
    return isinstance(value, tuple) and len(value) == 2 and all(isinstance(item, int) for item in value)


def _rejection(
    status: SafetyStatus,
    proposed_action: object,
    current_position: object,
    intervention_type: InterventionType,
    reason: str,
    *,
    proposed_next_position: Coordinate | None = None,
    requires_replan: bool = False,
) -> SafetyDecision:
    return SafetyDecision(
        status=status,
        proposed_action=proposed_action,
        approved_action=None,
        safe=False,
        intervention_type=intervention_type,
        reason=reason,
        requires_replan=requires_replan,
        current_position=current_position,
        proposed_next_position=proposed_next_position,
    )
