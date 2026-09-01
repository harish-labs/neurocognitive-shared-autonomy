"""Authorization-only bridge from shared-autonomy policy to human interaction."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from src.control.human_interaction import HumanInteractionController, PolicyGoalStatus
from src.control.shared_autonomy import AutonomyMode, HumanAction, SharedAutonomyDecision


class BridgeStatus(str, Enum):
    """Explicit outcomes at the D-068 authorization boundary."""

    AUTHORIZED = "AUTHORIZED"
    WAITING_FOR_CONFIRMATION = "WAITING_FOR_CONFIRMATION"
    HOLD = "HOLD"
    REJECTED = "REJECTED"
    INVALID_GOAL = "INVALID_GOAL"
    INVALID_STATE = "INVALID_STATE"


@dataclass(frozen=True)
class InteractionBridgeResult:
    """Read-only record of a policy decision routed without execution."""

    status: BridgeStatus
    policy_mode: object
    candidate_goal: object | None
    approved_goal: object | None
    active_request_id: str | None
    holds_position: bool
    requests_human_input: bool
    policy_goal_adopted: bool
    confirmation_opened: bool
    reason: str


def authorize_shared_autonomy_decision(
    decision: object,
    controller: object,
    *,
    goal_registry: object,
    request_id: object | None = None,
) -> InteractionBridgeResult:
    """Route one accepted policy decision into D-068 authorization state only."""
    if not isinstance(controller, HumanInteractionController):
        return _result(
            BridgeStatus.REJECTED,
            decision,
            None,
            reason="Bridge requires a HumanInteractionController.",
        )
    if not isinstance(decision, SharedAutonomyDecision):
        return _result(
            BridgeStatus.REJECTED,
            decision,
            controller,
            reason="Bridge requires an accepted SharedAutonomyDecision.",
        )
    if not isinstance(goal_registry, Mapping):
        return _result(
            BridgeStatus.REJECTED,
            decision,
            controller,
            reason="Goal registry must be a mapping of current symbolic goal keys.",
        )
    if not _is_structurally_valid(decision):
        return _result(
            BridgeStatus.REJECTED,
            decision,
            controller,
            reason="SharedAutonomyDecision violates the D-068 structural contract.",
        )
    if decision.human_action is not HumanAction.NONE:
        return _human_action_hold(decision, controller)

    if decision.mode is AutonomyMode.PROCEED:
        adoption = controller.adopt_policy_goal(decision.approved_goal, goal_registry=goal_registry)
        if adoption.status is PolicyGoalStatus.APPLIED:
            return _result(
                BridgeStatus.AUTHORIZED,
                decision,
                controller,
                policy_goal_adopted=adoption.applied,
                reason=adoption.reason,
            )
        return _result(
            _status_from_policy_adoption(adoption.status),
            decision,
            controller,
            reason=adoption.reason,
        )

    if decision.mode is AutonomyMode.CONFIRM:
        if not _is_current_symbolic_goal(decision.candidate_goal, goal_registry):
            return _result(
                BridgeStatus.INVALID_GOAL,
                decision,
                controller,
                reason="CONFIRM candidate must exactly match a current symbolic goal-registry key.",
            )
        if controller.state.stopped:
            return _result(
                BridgeStatus.INVALID_STATE,
                decision,
                controller,
                reason="STOP blocks confirmation-request registration.",
            )
        if not _is_non_empty_identifier(request_id):
            return _result(
                BridgeStatus.REJECTED,
                decision,
                controller,
                reason="CONFIRM requires a caller-supplied non-empty request_id.",
            )
        try:
            controller.open_confirmation_request(request_id, decision.candidate_goal)
        except ValueError as error:
            return _result(BridgeStatus.INVALID_STATE, decision, controller, reason=str(error))
        return _result(
            BridgeStatus.WAITING_FOR_CONFIRMATION,
            decision,
            controller,
            confirmation_opened=True,
            reason="Confirmation request opened; only an explicit human CONFIRM can approve it.",
        )

    return _result(
        BridgeStatus.HOLD,
        decision,
        controller,
        reason="Policy mode creates no new goal commitment at this authorization boundary.",
    )


def _is_structurally_valid(decision: SharedAutonomyDecision) -> bool:
    if not isinstance(decision.mode, AutonomyMode) or not isinstance(decision.human_action, HumanAction):
        return False
    if not isinstance(decision.holds_position, bool) or not isinstance(decision.requests_human_input, bool):
        return False
    if not isinstance(decision.requires_human_confirmation, bool):
        return False
    if decision.mode is AutonomyMode.PROCEED:
        return (
            decision.human_action is HumanAction.NONE
            and _is_non_empty_symbolic_goal(decision.candidate_goal)
            and decision.candidate_goal == decision.approved_goal
            and not decision.requires_human_confirmation
            and not decision.holds_position
            and not decision.requests_human_input
        )
    if decision.mode is AutonomyMode.CONFIRM:
        return (
            decision.human_action is HumanAction.NONE
            and _is_non_empty_symbolic_goal(decision.candidate_goal)
            and decision.approved_goal is None
            and decision.requires_human_confirmation
            and decision.holds_position
            and decision.requests_human_input
        )
    if decision.mode is AutonomyMode.WAITING:
        return (
            decision.human_action in (HumanAction.NONE, HumanAction.OVERRIDE)
            and decision.candidate_goal is None
            and decision.approved_goal is None
            and not decision.requires_human_confirmation
            and decision.holds_position
            and not decision.requests_human_input
        )
    if decision.mode is AutonomyMode.DEFER:
        return (
            decision.human_action is HumanAction.NONE
            and decision.candidate_goal is None
            and decision.approved_goal is None
            and not decision.requires_human_confirmation
            and decision.holds_position
            and decision.requests_human_input
        )
    if decision.mode is AutonomyMode.PAUSE:
        return _is_human_authority_decision(decision, HumanAction.PAUSE)
    if decision.mode is AutonomyMode.STOP:
        return _is_human_authority_decision(decision, HumanAction.STOP)
    return False


def _is_human_authority_decision(decision: SharedAutonomyDecision, action: HumanAction) -> bool:
    return (
        decision.human_action is action
        and decision.candidate_goal is None
        and decision.approved_goal is None
        and not decision.requires_human_confirmation
        and decision.holds_position
        and not decision.requests_human_input
    )


def _human_action_hold(
    decision: SharedAutonomyDecision,
    controller: HumanInteractionController,
) -> InteractionBridgeResult:
    if decision.human_action is HumanAction.STOP and not controller.state.stopped:
        return _result(
            BridgeStatus.INVALID_STATE,
            decision,
            controller,
            reason="Observed policy STOP conflicts with the controller's non-stopped state.",
        )
    if decision.human_action is HumanAction.PAUSE and not controller.state.paused:
        return _result(
            BridgeStatus.INVALID_STATE,
            decision,
            controller,
            reason="Observed policy PAUSE conflicts with the controller's non-paused state.",
        )
    if decision.human_action is HumanAction.OVERRIDE and controller.state.approved_goal is None:
        return _result(
            BridgeStatus.INVALID_STATE,
            decision,
            controller,
            reason="Observed policy OVERRIDE conflicts with a controller state lacking an approved goal.",
        )
    return _result(
        BridgeStatus.HOLD,
        decision,
        controller,
        reason="Observed human authority is not converted into a duplicate human command.",
    )


def _status_from_policy_adoption(status: PolicyGoalStatus) -> BridgeStatus:
    if status is PolicyGoalStatus.INVALID_GOAL:
        return BridgeStatus.INVALID_GOAL
    return BridgeStatus.INVALID_STATE


def _is_current_symbolic_goal(goal: object, goal_registry: Mapping[object, object]) -> bool:
    return isinstance(goal, str) and bool(goal) and goal in goal_registry


def _is_non_empty_symbolic_goal(goal: object) -> bool:
    return isinstance(goal, str) and bool(goal)


def _is_non_empty_identifier(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _result(
    status: BridgeStatus,
    decision: object,
    controller: HumanInteractionController | None,
    *,
    policy_goal_adopted: bool = False,
    confirmation_opened: bool = False,
    reason: str,
) -> InteractionBridgeResult:
    state = None if controller is None else controller.state
    active = None if state is None else state.active_confirmation
    return InteractionBridgeResult(
        status=status,
        policy_mode=decision.mode if isinstance(decision, SharedAutonomyDecision) else None,
        candidate_goal=decision.candidate_goal if isinstance(decision, SharedAutonomyDecision) else None,
        approved_goal=None if state is None else state.approved_goal,
        active_request_id=None if active is None else active.request_id,
        holds_position=status is not BridgeStatus.AUTHORIZED,
        requests_human_input=(
            status is BridgeStatus.WAITING_FOR_CONFIRMATION
            or (isinstance(decision, SharedAutonomyDecision) and decision.requests_human_input)
        ),
        policy_goal_adopted=policy_goal_adopted,
        confirmation_opened=confirmation_opened,
        reason=reason,
    )
