"""Interruptible, authorization-gated stepwise navigation under D-069."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

from src.autonomy.environment import ACTION_DELTAS, Action, Coordinate, SearchRescueEnvironment
from src.autonomy.planner import PlannerStatus, PlanningResult, RiskAwareAStarPlanner
from src.autonomy.safety import SafetyController, SafetyDecision, SafetyStatus
from src.control.human_interaction import CommandResult, CommandStatus, HumanCommandType, HumanInteractionController
from src.control.interaction_bridge import BridgeStatus, InteractionBridgeResult
from src.control.shared_autonomy import AutonomyMode


class NavigationStatus(str, Enum):
    """Explicit outcomes for a single D-069 navigation attempt or step."""

    READY = "READY"
    STEP_EXECUTED = "STEP_EXECUTED"
    GOAL_REACHED = "GOAL_REACHED"
    NO_SAFE_PATH = "NO_SAFE_PATH"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    HOLD = "HOLD"
    REPLAN_REQUIRED = "REPLAN_REQUIRED"
    SAFETY_REJECTED = "SAFETY_REJECTED"
    STALE_STATE = "STALE_STATE"
    INVALID_AUTHORIZATION = "INVALID_AUTHORIZATION"
    INVALID_GOAL_OR_PLAN = "INVALID_GOAL_OR_PLAN"
    ALREADY_CONSUMED = "ALREADY_CONSUMED"


@dataclass(frozen=True)
class EnvironmentSignature:
    """Structural map snapshot used to reject implicit runtime changes."""

    rows: int
    columns: int
    goals: tuple[tuple[str, Coordinate], ...]
    blocked_cells: frozenset[Coordinate]
    risk_map: tuple[tuple[Coordinate, float], ...]


@dataclass(frozen=True)
class NavigationSession:
    """Read-only active plan and authority snapshot for one execution ID."""

    execution_id: str
    symbolic_goal: str
    goal_coordinate: Coordinate
    path: tuple[Coordinate, ...]
    actions: tuple[Action, ...]
    next_action_index: int
    expected_position: Coordinate
    environment_signature: EnvironmentSignature
    active: bool


@dataclass(frozen=True)
class NavigationResult:
    """Auditable output of zero-movement start or one-step advancement."""

    status: NavigationStatus
    execution_id: object
    symbolic_goal: str | None
    goal_coordinate: Coordinate | None
    path: tuple[Coordinate, ...]
    proposed_action: Action | None
    safety_decision: SafetyDecision | None
    position_before: Coordinate | None
    position_after: Coordinate | None
    moved: bool
    active: bool
    closed: bool
    requires_replan: bool
    remaining_action_count: int
    reason: str


class NavigationRuntime:
    """Start plans without movement and advance at most one safety-gated action."""

    def __init__(
        self,
        *,
        planner: RiskAwareAStarPlanner | None = None,
        safety_controller: SafetyController | None = None,
    ) -> None:
        self._planner = RiskAwareAStarPlanner() if planner is None else planner
        self._safety_controller = SafetyController() if safety_controller is None else safety_controller
        self._session: NavigationSession | None = None
        self._consumed_execution_ids: set[str] = set()

    @property
    def session(self) -> NavigationSession | None:
        """Return the current immutable active session, if one exists."""
        return self._session

    def start_navigation(
        self,
        environment: SearchRescueEnvironment,
        controller: HumanInteractionController,
        authorization: object,
        *,
        execution_id: object,
    ) -> NavigationResult:
        """Validate fresh authority and create one plan without moving the environment."""
        if not _is_non_empty_identifier(execution_id):
            return _result(
                NavigationStatus.INVALID_AUTHORIZATION,
                execution_id,
                None,
                None,
                (),
                None,
                None,
                None,
                None,
                False,
                False,
                False,
                False,
                0,
                "execution_id must be a non-empty string.",
            )
        if execution_id in self._consumed_execution_ids or (
            self._session is not None and self._session.execution_id == execution_id
        ):
            return _result(
                NavigationStatus.ALREADY_CONSUMED,
                execution_id,
                None,
                None,
                (),
                None,
                None,
                None,
                None,
                False,
                False,
                True,
                False,
                0,
                "execution_id has already identified a navigation attempt.",
            )
        if self._session is not None and self._session.active:
            return _result(
                NavigationStatus.HOLD,
                execution_id,
                self._session.symbolic_goal,
                self._session.goal_coordinate,
                self._session.path,
                None,
                None,
                environment.state.position,
                environment.state.position,
                False,
                True,
                False,
                False,
                _remaining(self._session),
                "An active navigation attempt must close before another one starts.",
            )
        if not isinstance(environment, SearchRescueEnvironment) or not isinstance(controller, HumanInteractionController):
            return _result(
                NavigationStatus.INVALID_AUTHORIZATION,
                execution_id,
                None,
                None,
                (),
                None,
                None,
                None,
                None,
                False,
                False,
                False,
                False,
                0,
                "Navigation requires the accepted environment and human-interaction controller.",
            )
        symbolic_goal = _fresh_authorized_goal(authorization, controller)
        if symbolic_goal is None:
            return _result(
                NavigationStatus.INVALID_AUTHORIZATION,
                execution_id,
                None,
                None,
                (),
                None,
                None,
                environment.state.position,
                environment.state.position,
                False,
                False,
                False,
                False,
                0,
                "Authorization is not a fresh accepted M5 execution source.",
            )
        if controller.state.stopped or controller.state.paused or controller.state.active_confirmation is not None:
            return _result(
                NavigationStatus.INVALID_AUTHORIZATION,
                execution_id,
                symbolic_goal,
                None,
                (),
                None,
                None,
                environment.state.position,
                environment.state.position,
                False,
                False,
                False,
                False,
                0,
                "Current human authority does not permit navigation start.",
            )
        if not _is_exact_environment_goal(symbolic_goal, environment):
            return _result(
                NavigationStatus.INVALID_GOAL_OR_PLAN,
                execution_id,
                symbolic_goal,
                None,
                (),
                None,
                None,
                environment.state.position,
                environment.state.position,
                False,
                False,
                False,
                False,
                0,
                "Approved symbolic goal must exactly match a current environment goal key.",
            )

        goal_coordinate = environment.config.goals[symbolic_goal]
        start = environment.state.position
        if environment.state.terminated:
            return _result(
                NavigationStatus.INVALID_GOAL_OR_PLAN,
                execution_id,
                symbolic_goal,
                goal_coordinate,
                (),
                None,
                None,
                start,
                start,
                False,
                False,
                False,
                False,
                0,
                "Cannot start navigation from an already terminated environment state.",
            )
        self._consumed_execution_ids.add(execution_id)
        planning = self._planner.plan(environment, start=start, approved_goal=goal_coordinate)
        if planning.status is PlannerStatus.NO_SAFE_PATH:
            return _result(
                NavigationStatus.NO_SAFE_PATH,
                execution_id,
                symbolic_goal,
                goal_coordinate,
                (),
                None,
                None,
                start,
                start,
                False,
                False,
                True,
                False,
                0,
                "Planner reported no safe route to the exact approved goal.",
            )
        if not _is_consistent_success_plan(planning, start, goal_coordinate):
            return _result(
                NavigationStatus.INVALID_GOAL_OR_PLAN,
                execution_id,
                symbolic_goal,
                goal_coordinate,
                (),
                None,
                None,
                start,
                start,
                False,
                False,
                True,
                False,
                0,
                "Planner result is not a structurally valid route for the exact request.",
            )
        if not planning.actions:
            return _result(
                NavigationStatus.INVALID_GOAL_OR_PLAN,
                execution_id,
                symbolic_goal,
                goal_coordinate,
                planning.path,
                None,
                None,
                start,
                start,
                False,
                False,
                True,
                False,
                0,
                "A zero-action plan cannot establish an exact environment goal-entry event.",
            )
        if _crosses_another_goal(planning.path, symbolic_goal, environment.config.goals):
            return _result(
                NavigationStatus.INVALID_GOAL_OR_PLAN,
                execution_id,
                symbolic_goal,
                goal_coordinate,
                planning.path,
                None,
                None,
                start,
                start,
                False,
                False,
                True,
                False,
                0,
                "Planned route enters another configured terminal goal before the approved goal.",
            )

        self._session = NavigationSession(
            execution_id=execution_id,
            symbolic_goal=symbolic_goal,
            goal_coordinate=goal_coordinate,
            path=planning.path,
            actions=planning.actions,
            next_action_index=0,
            expected_position=start,
            environment_signature=_environment_signature(environment),
            active=True,
        )
        return _session_result(
            NavigationStatus.READY,
            self._session,
            position_before=start,
            position_after=start,
            moved=False,
            safety_decision=None,
            requires_replan=False,
            reason="Fresh authorization produced a plan; start_navigation performed zero movement.",
        )

    def advance_one_step(
        self,
        environment: SearchRescueEnvironment,
        controller: HumanInteractionController,
    ) -> NavigationResult:
        """Revalidate authority, safety-check one action, and step at most once."""
        session = self._session
        if session is None or not session.active:
            return _result(
                NavigationStatus.HOLD,
                None if session is None else session.execution_id,
                None if session is None else session.symbolic_goal,
                None if session is None else session.goal_coordinate,
                () if session is None else session.path,
                None,
                None,
                None if not isinstance(environment, SearchRescueEnvironment) else environment.state.position,
                None if not isinstance(environment, SearchRescueEnvironment) else environment.state.position,
                False,
                False,
                True,
                False,
                0 if session is None else _remaining(session),
                "No active navigation attempt is available for advancement.",
            )
        if not isinstance(environment, SearchRescueEnvironment) or not isinstance(controller, HumanInteractionController):
            return self._close(NavigationStatus.STALE_STATE, environment, session, "Runtime dependencies changed or are invalid.")
        if controller.state.stopped:
            return self._close(NavigationStatus.STOPPED, environment, session, "STOP closes the active navigation attempt.")
        if controller.state.paused:
            return self._close(NavigationStatus.PAUSED, environment, session, "PAUSE invalidates the executable plan before movement.")
        if controller.state.active_confirmation is not None:
            return self._close(NavigationStatus.HOLD, environment, session, "Active confirmation blocks movement from historical authorization.")
        if controller.state.approved_goal != session.symbolic_goal:
            return self._close(NavigationStatus.STALE_STATE, environment, session, "Approved symbolic goal changed after planning.")
        if not _is_exact_environment_goal(session.symbolic_goal, environment):
            return self._close(NavigationStatus.STALE_STATE, environment, session, "Approved symbolic goal is no longer current in the environment.")
        if _environment_signature(environment) != session.environment_signature:
            return self._close(NavigationStatus.STALE_STATE, environment, session, "Environment configuration changed after planning.")
        if environment.state.position != session.expected_position or environment.state.terminated:
            return self._close(NavigationStatus.STALE_STATE, environment, session, "Environment position or terminal state changed unexpectedly.")
        if session.next_action_index >= len(session.actions):
            return self._close(NavigationStatus.STALE_STATE, environment, session, "Plan has no executable next action before exact goal completion.")

        action = session.actions[session.next_action_index]
        position_before = environment.state.position
        safety = self._safety_controller.check(
            environment,
            current_position=position_before,
            proposed_action=action,
            paused=controller.state.paused,
            emergency_stop=controller.state.stopped,
        )
        if safety.requires_replan or safety.status is SafetyStatus.REPLAN_REQUIRED:
            return self._close(
                NavigationStatus.REPLAN_REQUIRED,
                environment,
                session,
                safety.reason,
                proposed_action=action,
                safety_decision=safety,
                requires_replan=True,
            )
        if safety.status is not SafetyStatus.APPROVED or safety.approved_action is None:
            return self._close(
                NavigationStatus.SAFETY_REJECTED,
                environment,
                session,
                safety.reason,
                proposed_action=action,
                safety_decision=safety,
            )

        environment.step(safety.approved_action)
        position_after = environment.state.position
        expected_next = session.path[session.next_action_index + 1]
        if position_after != expected_next:
            return self._close(
                NavigationStatus.STALE_STATE,
                environment,
                session,
                "Environment transition did not match the safety-approved planned action.",
                proposed_action=action,
                safety_decision=safety,
                position_before=position_before,
                moved=position_after != position_before,
            )
        advanced = replace(session, next_action_index=session.next_action_index + 1, expected_position=position_after)
        if environment.state.terminated:
            self._session = replace(advanced, active=False)
            if position_after == session.goal_coordinate and environment.state.reached_goal == session.symbolic_goal:
                return _session_result(
                    NavigationStatus.GOAL_REACHED,
                    self._session,
                    position_before=position_before,
                    position_after=position_after,
                    moved=True,
                    proposed_action=action,
                    safety_decision=safety,
                    requires_replan=False,
                    reason="Exact approved symbolic goal reached through one safety-approved step.",
                )
            return _session_result(
                NavigationStatus.INVALID_GOAL_OR_PLAN,
                self._session,
                position_before=position_before,
                position_after=position_after,
                moved=True,
                proposed_action=action,
                safety_decision=safety,
                requires_replan=False,
                reason="Environment terminated at a goal other than the exact approved symbolic goal.",
            )

        self._session = advanced
        return _session_result(
            NavigationStatus.STEP_EXECUTED,
            self._session,
            position_before=position_before,
            position_after=position_after,
            moved=True,
            proposed_action=action,
            safety_decision=safety,
            requires_replan=False,
            reason="Exactly one planned action passed safety and was executed.",
        )

    def _close(
        self,
        status: NavigationStatus,
        environment: object,
        session: NavigationSession,
        reason: str,
        *,
        proposed_action: Action | None = None,
        safety_decision: SafetyDecision | None = None,
        requires_replan: bool = False,
        position_before: Coordinate | None = None,
        moved: bool = False,
    ) -> NavigationResult:
        self._session = replace(session, active=False)
        position = environment.state.position if isinstance(environment, SearchRescueEnvironment) else None
        return _session_result(
            status,
            self._session,
            position_before=position if position_before is None else position_before,
            position_after=position,
            moved=moved,
            proposed_action=proposed_action,
            safety_decision=safety_decision,
            requires_replan=requires_replan,
            reason=reason,
        )


def _fresh_authorized_goal(authorization: object, controller: HumanInteractionController) -> str | None:
    approved_goal = controller.state.approved_goal
    if not isinstance(approved_goal, str) or not approved_goal:
        return None
    if isinstance(authorization, InteractionBridgeResult):
        if (
            authorization.status is BridgeStatus.AUTHORIZED
            and authorization.policy_goal_adopted
            and authorization.policy_mode is AutonomyMode.PROCEED
            and authorization.candidate_goal == approved_goal
            and authorization.approved_goal == approved_goal
            and authorization.active_request_id is None
            and not authorization.holds_position
            and not authorization.requests_human_input
        ):
            return approved_goal
        return None
    if not isinstance(authorization, CommandResult):
        return None
    if (
        authorization.status is not CommandStatus.APPLIED
        or not authorization.accepted
        or not authorization.applied
        or authorization.approved_goal != approved_goal
        or authorization.paused != controller.state.paused
        or authorization.stopped != controller.state.stopped
        or authorization.stopped
    ):
        return None
    if authorization.command_type is HumanCommandType.CONFIRM:
        return approved_goal if authorization.active_request_id is None and not authorization.requires_fresh_execution else None
    if authorization.command_type is HumanCommandType.OVERRIDE:
        return approved_goal if authorization.requires_fresh_execution else None
    if authorization.command_type is HumanCommandType.RESUME:
        return approved_goal if not authorization.paused and authorization.requires_fresh_execution else None
    return None


def _is_exact_environment_goal(symbolic_goal: object, environment: SearchRescueEnvironment) -> bool:
    return isinstance(symbolic_goal, str) and bool(symbolic_goal) and symbolic_goal in environment.config.goals


def _is_consistent_success_plan(planning: object, start: Coordinate, goal: Coordinate) -> bool:
    if not isinstance(planning, PlanningResult) or planning.status is not PlannerStatus.SUCCESS:
        return False
    if planning.start != start or planning.goal != goal:
        return False
    if not planning.path or planning.path[0] != start or planning.path[-1] != goal:
        return False
    if len(planning.actions) != len(planning.path) - 1:
        return False
    for position, action, next_position in zip(planning.path, planning.actions, planning.path[1:]):
        if not isinstance(action, Action) or action is Action.WAIT:
            return False
        if not _is_coordinate(position) or not _is_coordinate(next_position):
            return False
        delta = ACTION_DELTAS[action]
        if (position[0] + delta[0], position[1] + delta[1]) != next_position:
            return False
    return True


def _crosses_another_goal(
    path: tuple[Coordinate, ...],
    symbolic_goal: str,
    goals: object,
) -> bool:
    if not hasattr(goals, "items"):
        return True
    for position in path[1:]:
        for name, coordinate in goals.items():
            if name != symbolic_goal and coordinate == position:
                return True
    return False


def _environment_signature(environment: SearchRescueEnvironment) -> EnvironmentSignature:
    config = environment.config
    return EnvironmentSignature(
        rows=config.rows,
        columns=config.columns,
        goals=tuple(sorted(config.goals.items())),
        blocked_cells=frozenset(config.blocked_cells),
        risk_map=tuple(sorted((coordinate, float(risk)) for coordinate, risk in config.risk_map.items())),
    )


def _remaining(session: NavigationSession) -> int:
    return len(session.actions) - session.next_action_index


def _is_non_empty_identifier(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _is_coordinate(value: object) -> bool:
    return isinstance(value, tuple) and len(value) == 2 and all(isinstance(item, int) for item in value)


def _session_result(
    status: NavigationStatus,
    session: NavigationSession,
    *,
    position_before: Coordinate | None,
    position_after: Coordinate | None,
    moved: bool,
    proposed_action: Action | None = None,
    safety_decision: SafetyDecision | None,
    requires_replan: bool,
    reason: str,
) -> NavigationResult:
    return _result(
        status,
        session.execution_id,
        session.symbolic_goal,
        session.goal_coordinate,
        session.path,
        proposed_action,
        safety_decision,
        position_before,
        position_after,
        moved,
        session.active,
        not session.active,
        requires_replan,
        _remaining(session),
        reason,
    )


def _result(
    status: NavigationStatus,
    execution_id: object,
    symbolic_goal: str | None,
    goal_coordinate: Coordinate | None,
    path: tuple[Coordinate, ...],
    proposed_action: Action | None,
    safety_decision: SafetyDecision | None,
    position_before: Coordinate | None,
    position_after: Coordinate | None,
    moved: bool,
    active: bool,
    closed: bool,
    requires_replan: bool,
    remaining_action_count: int,
    reason: str,
) -> NavigationResult:
    return NavigationResult(
        status=status,
        execution_id=execution_id,
        symbolic_goal=symbolic_goal,
        goal_coordinate=goal_coordinate,
        path=path,
        proposed_action=proposed_action,
        safety_decision=safety_decision,
        position_before=position_before,
        position_after=position_after,
        moved=moved,
        active=active,
        closed=closed,
        requires_replan=requires_replan,
        remaining_action_count=remaining_action_count,
        reason=reason,
    )
