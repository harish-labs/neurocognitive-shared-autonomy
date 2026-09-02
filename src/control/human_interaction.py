"""Deterministic human-command state handling for D-067.

This module deliberately records human authority without planning or executing
movement. A later integration layer must route any fresh execution request
through the approved planner, safety, and environment sequence.
"""

from __future__ import annotations

from collections.abc import Mapping, Set
from dataclasses import dataclass
from enum import Enum


class HumanCommandType(str, Enum):
    """The complete M5-T01 human-command vocabulary."""

    CONFIRM = "CONFIRM"
    OVERRIDE = "OVERRIDE"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    STOP = "STOP"


class CommandStatus(str, Enum):
    """Deterministic outcomes for command handling."""

    APPLIED = "APPLIED"
    REJECTED = "REJECTED"
    STALE_REQUEST = "STALE_REQUEST"
    ALREADY_CONSUMED = "ALREADY_CONSUMED"
    INVALID_GOAL = "INVALID_GOAL"
    INVALID_STATE = "INVALID_STATE"


class PolicyGoalStatus(str, Enum):
    """Outcomes for non-human policy-goal adoption under D-068."""

    APPLIED = "APPLIED"
    INVALID_GOAL = "INVALID_GOAL"
    INVALID_STATE = "INVALID_STATE"


class HumanInteractionError(ValueError):
    """Raised when a confirmation request cannot be registered."""


@dataclass(frozen=True)
class ConfirmationRequest:
    """One explicit candidate-goal confirmation awaiting human authority."""

    request_id: str
    candidate_goal: object


@dataclass(frozen=True)
class HumanCommand:
    """One caller-identified human command; fields apply to specific command types."""

    command_id: object
    command_type: object
    request_id: object | None = None
    goal: object | None = None


@dataclass(frozen=True)
class HumanControlState:
    """Read-only interaction state retained within one controller session."""

    approved_goal: object | None
    active_confirmation: ConfirmationRequest | None
    paused: bool
    stopped: bool
    consumed_command_ids: frozenset[str]
    closed_request_ids: frozenset[str]


@dataclass(frozen=True)
class CommandResult:
    """Read-only audit result for one handled human command."""

    status: CommandStatus
    command_id: object
    command_type: object
    accepted: bool
    applied: bool
    approved_goal: object | None
    paused: bool
    stopped: bool
    active_request_id: str | None
    requires_fresh_execution: bool
    reason: str


@dataclass(frozen=True)
class PolicyGoalAdoptionResult:
    """Read-only result for one authorization-only policy goal adoption attempt."""

    status: PolicyGoalStatus
    policy_goal: object
    approved_goal: object | None
    paused: bool
    stopped: bool
    active_request_id: str | None
    applied: bool
    reason: str


class HumanInteractionController:
    """Own D-067 command, confirmation, pause, and stop state for one session."""

    def __init__(self) -> None:
        self._state = _initial_state()

    @property
    def state(self) -> HumanControlState:
        """Return the current immutable interaction state."""
        return self._state

    def open_confirmation_request(self, request_id: object, candidate_goal: object) -> ConfirmationRequest:
        """Register the sole active confirmation request for this controller session."""
        if not _is_non_empty_identifier(request_id):
            raise HumanInteractionError("Confirmation request_id must be a non-empty string.")
        if request_id in self._state.closed_request_ids or (
            self._state.active_confirmation is not None
            and request_id == self._state.active_confirmation.request_id
        ):
            raise HumanInteractionError("Confirmation request_id must be unique within the session.")
        if self._state.stopped:
            raise HumanInteractionError("Cannot open a confirmation request after STOP.")
        if self._state.active_confirmation is not None:
            raise HumanInteractionError("Only one confirmation request may be active at a time.")

        request = ConfirmationRequest(request_id=request_id, candidate_goal=candidate_goal)
        self._state = _replace_state(self._state, active_confirmation=request)
        return request

    def handle_command(
        self,
        command: HumanCommand,
        *,
        valid_goals: Mapping[object, object] | Set[object] | None = None,
    ) -> CommandResult:
        """Consume one command and return its deterministic control-state outcome."""
        if not isinstance(command, HumanCommand):
            return self._result(
                CommandStatus.REJECTED,
                None,
                None,
                reason="Command must be a HumanCommand instance.",
            )
        if not _is_non_empty_identifier(command.command_id):
            return self._result(
                CommandStatus.REJECTED,
                command.command_id,
                command.command_type,
                reason="command_id must be a non-empty string.",
            )
        if command.command_id in self._state.consumed_command_ids:
            return self._result(
                CommandStatus.ALREADY_CONSUMED,
                command.command_id,
                command.command_type,
                reason="This command_id has already been consumed.",
            )

        self._state = _replace_state(
            self._state,
            consumed_command_ids=self._state.consumed_command_ids | {command.command_id},
        )
        if not isinstance(command.command_type, HumanCommandType):
            return self._result(
                CommandStatus.REJECTED,
                command.command_id,
                command.command_type,
                reason="command_type is outside the approved M5-T01 vocabulary.",
            )

        if command.command_type is HumanCommandType.STOP:
            return self._handle_stop(command)
        if self._state.stopped:
            return self._result(
                CommandStatus.INVALID_STATE,
                command.command_id,
                command.command_type,
                reason="STOP is terminal until an explicit reset or new session.",
            )
        if command.command_type is HumanCommandType.PAUSE:
            return self._handle_pause(command)
        if command.command_type is HumanCommandType.RESUME:
            return self._handle_resume(command)
        if command.command_type is HumanCommandType.OVERRIDE:
            return self._handle_override(command, valid_goals)
        return self._handle_confirm(command)

    def reset(self) -> None:
        """Start a fresh M5-T01 interaction session without touching other modules."""
        self._state = _initial_state()

    def adopt_policy_goal(
        self,
        policy_goal: object,
        *,
        goal_registry: Mapping[object, object],
    ) -> PolicyGoalAdoptionResult:
        """Adopt one exact symbolic policy goal without creating a human command."""
        if self._state.stopped:
            return self._policy_goal_result(
                PolicyGoalStatus.INVALID_STATE,
                policy_goal,
                applied=False,
                reason="STOP is terminal until an explicit reset or new session.",
            )
        if self._state.paused:
            return self._policy_goal_result(
                PolicyGoalStatus.INVALID_STATE,
                policy_goal,
                applied=False,
                reason="PAUSE blocks autonomous policy-goal adoption.",
            )
        if self._state.active_confirmation is not None:
            return self._policy_goal_result(
                PolicyGoalStatus.INVALID_STATE,
                policy_goal,
                applied=False,
                reason="An active confirmation request cannot be bypassed by policy adoption.",
            )
        if not _is_current_symbolic_goal(policy_goal, goal_registry):
            return self._policy_goal_result(
                PolicyGoalStatus.INVALID_GOAL,
                policy_goal,
                applied=False,
                reason="Policy goal must exactly match a current symbolic goal-registry key.",
            )

        changed = self._state.approved_goal != policy_goal
        self._state = _replace_state(self._state, approved_goal=policy_goal)
        return self._policy_goal_result(
            PolicyGoalStatus.APPLIED,
            policy_goal,
            applied=changed,
            reason="Exact symbolic policy goal adopted without human-command processing.",
        )

    def _handle_stop(self, command: HumanCommand) -> CommandResult:
        active = self._state.active_confirmation
        self._state = _replace_state(
            self._state,
            active_confirmation=None,
            paused=True,
            stopped=True,
            closed_request_ids=_closed_with(self._state, active),
        )
        return self._result(
            CommandStatus.APPLIED,
            command.command_id,
            command.command_type,
            accepted=True,
            applied=True,
            reason="STOP is terminal and cancels any active confirmation request.",
        )

    def _handle_pause(self, command: HumanCommand) -> CommandResult:
        was_paused = self._state.paused
        self._state = _replace_state(self._state, paused=True)
        return self._result(
            CommandStatus.APPLIED,
            command.command_id,
            command.command_type,
            accepted=True,
            applied=not was_paused,
            reason="PAUSE preserves approved-goal and confirmation state." if not was_paused else "PAUSE is already active; the command is idempotent.",
        )

    def _handle_resume(self, command: HumanCommand) -> CommandResult:
        if not self._state.paused:
            return self._result(
                CommandStatus.INVALID_STATE,
                command.command_id,
                command.command_type,
                reason="RESUME is valid only while PAUSE is active.",
            )
        self._state = _replace_state(self._state, paused=False)
        has_goal = self._state.approved_goal is not None
        return self._result(
            CommandStatus.APPLIED,
            command.command_id,
            command.command_type,
            accepted=True,
            applied=True,
            requires_fresh_execution=has_goal,
            reason=(
                "RESUME requires fresh downstream authorization for the preserved approved goal."
                if has_goal
                else "RESUME cleared PAUSE; no approved goal exists to execute."
            ),
        )

    def _handle_override(
        self,
        command: HumanCommand,
        valid_goals: Mapping[object, object] | Set[object] | None,
    ) -> CommandResult:
        if not _goal_is_valid(command.goal, valid_goals):
            return self._result(
                CommandStatus.INVALID_GOAL,
                command.command_id,
                command.command_type,
                reason="OVERRIDE must name a currently valid mission goal.",
            )
        active = self._state.active_confirmation
        self._state = _replace_state(
            self._state,
            approved_goal=command.goal,
            active_confirmation=None,
            closed_request_ids=_closed_with(self._state, active),
        )
        return self._result(
            CommandStatus.APPLIED,
            command.command_id,
            command.command_type,
            accepted=True,
            applied=True,
            requires_fresh_execution=True,
            reason="OVERRIDE set the human-approved goal and requires fresh downstream authorization.",
        )

    def _handle_confirm(self, command: HumanCommand) -> CommandResult:
        active = self._state.active_confirmation
        if not _is_non_empty_identifier(command.request_id) or active is None or command.request_id != active.request_id:
            return self._result(
                CommandStatus.STALE_REQUEST,
                command.command_id,
                command.command_type,
                reason="CONFIRM must reference the exact currently active request_id.",
            )
        if command.goal is not None and command.goal != active.candidate_goal:
            return self._result(
                CommandStatus.REJECTED,
                command.command_id,
                command.command_type,
                reason="CONFIRM cannot substitute a goal for its request candidate.",
            )
        self._state = _replace_state(
            self._state,
            approved_goal=active.candidate_goal,
            active_confirmation=None,
            closed_request_ids=_closed_with(self._state, active),
        )
        return self._result(
            CommandStatus.APPLIED,
            command.command_id,
            command.command_type,
            accepted=True,
            applied=True,
            reason="CONFIRM approved the candidate goal attached to the active request.",
        )

    def _result(
        self,
        status: CommandStatus,
        command_id: object,
        command_type: object,
        *,
        accepted: bool = False,
        applied: bool = False,
        requires_fresh_execution: bool = False,
        reason: str,
    ) -> CommandResult:
        active = self._state.active_confirmation
        return CommandResult(
            status=status,
            command_id=command_id,
            command_type=command_type,
            accepted=accepted,
            applied=applied,
            approved_goal=self._state.approved_goal,
            paused=self._state.paused,
            stopped=self._state.stopped,
            active_request_id=None if active is None else active.request_id,
            requires_fresh_execution=requires_fresh_execution,
            reason=reason,
        )

    def _policy_goal_result(
        self,
        status: PolicyGoalStatus,
        policy_goal: object,
        *,
        applied: bool,
        reason: str,
    ) -> PolicyGoalAdoptionResult:
        active = self._state.active_confirmation
        return PolicyGoalAdoptionResult(
            status=status,
            policy_goal=policy_goal,
            approved_goal=self._state.approved_goal,
            paused=self._state.paused,
            stopped=self._state.stopped,
            active_request_id=None if active is None else active.request_id,
            applied=applied,
            reason=reason,
        )


def _initial_state() -> HumanControlState:
    return HumanControlState(
        approved_goal=None,
        active_confirmation=None,
        paused=False,
        stopped=False,
        consumed_command_ids=frozenset(),
        closed_request_ids=frozenset(),
    )


def _replace_state(state: HumanControlState, **changes: object) -> HumanControlState:
    values = {
        "approved_goal": state.approved_goal,
        "active_confirmation": state.active_confirmation,
        "paused": state.paused,
        "stopped": state.stopped,
        "consumed_command_ids": state.consumed_command_ids,
        "closed_request_ids": state.closed_request_ids,
    }
    values.update(changes)
    return HumanControlState(**values)  # type: ignore[arg-type]


def _closed_with(state: HumanControlState, request: ConfirmationRequest | None) -> frozenset[str]:
    if request is None:
        return state.closed_request_ids
    return state.closed_request_ids | {request.request_id}


def _is_non_empty_identifier(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _goal_is_valid(
    goal: object,
    valid_goals: Mapping[object, object] | Set[object] | None,
) -> bool:
    if not _is_non_empty_identifier(goal) or valid_goals is None:
        return False
    if isinstance(valid_goals, Mapping):
        try:
            return goal in valid_goals
        except TypeError:
            return False
    if isinstance(valid_goals, Set):
        try:
            return goal in valid_goals
        except TypeError:
            return False
    return False


def _is_current_symbolic_goal(goal: object, goal_registry: object) -> bool:
    """Require a non-empty symbolic goal to match one configured registry key exactly."""
    if not isinstance(goal, str) or not goal or not isinstance(goal_registry, Mapping):
        return False
    return goal in goal_registry
