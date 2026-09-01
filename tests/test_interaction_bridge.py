from __future__ import annotations

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import src.control.interaction_bridge as interaction_bridge
from src.control.human_interaction import HumanCommand, HumanCommandType, HumanInteractionController
from src.control.interaction_bridge import BridgeStatus, authorize_shared_autonomy_decision
from src.control.shared_autonomy import AutonomyMode, HumanAction, SharedAutonomyDecision


GOALS = {"victim_a": (0, 1), "victim_b": (1, 2)}


def policy_decision(
    mode: object,
    *,
    candidate_goal: object | None = None,
    approved_goal: object | None = None,
    requires_human_confirmation: bool = False,
    holds_position: bool = True,
    requests_human_input: bool = False,
    human_action: object = HumanAction.NONE,
) -> SharedAutonomyDecision:
    return SharedAutonomyDecision(
        mode=mode,  # type: ignore[arg-type]
        candidate_goal=candidate_goal,  # type: ignore[arg-type]
        approved_goal=approved_goal,  # type: ignore[arg-type]
        requires_human_confirmation=requires_human_confirmation,
        holds_position=holds_position,
        requests_human_input=requests_human_input,
        human_action=human_action,  # type: ignore[arg-type]
        posterior_confidence=0.8,
        entropy_bits=0.7,
        update_count=5,
        reason="synthetic bridge test decision",
    )


def proceed(goal: str = "victim_a") -> SharedAutonomyDecision:
    return policy_decision(
        AutonomyMode.PROCEED,
        candidate_goal=goal,
        approved_goal=goal,
        holds_position=False,
    )


def confirm(goal: str = "victim_a") -> SharedAutonomyDecision:
    return policy_decision(
        AutonomyMode.CONFIRM,
        candidate_goal=goal,
        requires_human_confirmation=True,
        holds_position=True,
        requests_human_input=True,
    )


def test_valid_proceed_adopts_exact_symbolic_goal_without_command_consumption() -> None:
    controller = HumanInteractionController()

    result = authorize_shared_autonomy_decision(proceed(), controller, goal_registry=GOALS)

    assert result.status is BridgeStatus.AUTHORIZED
    assert result.approved_goal == "victim_a"
    assert result.policy_goal_adopted
    assert not result.holds_position
    assert not controller.state.consumed_command_ids


def test_proceed_rejects_substring_and_value_goal_matches() -> None:
    controller = HumanInteractionController()

    substring = authorize_shared_autonomy_decision(proceed("victim"), controller, goal_registry=GOALS)
    value = authorize_shared_autonomy_decision(proceed("(0, 1)"), controller, goal_registry=GOALS)

    assert substring.status is BridgeStatus.INVALID_GOAL
    assert value.status is BridgeStatus.INVALID_GOAL
    assert controller.state.approved_goal is None


@pytest.mark.parametrize("state", ("paused", "stopped", "confirming"))
def test_proceed_cannot_bypass_pause_stop_or_active_confirmation(state: str) -> None:
    controller = HumanInteractionController()
    if state == "paused":
        controller.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
    elif state == "stopped":
        controller.handle_command(HumanCommand("stop", HumanCommandType.STOP))
    else:
        controller.open_confirmation_request("request-1", "victim_a")

    result = authorize_shared_autonomy_decision(proceed(), controller, goal_registry=GOALS)

    assert result.status is BridgeStatus.INVALID_STATE
    assert result.holds_position
    assert controller.state.approved_goal is None


def test_repeated_same_proceed_is_state_idempotent_without_movement_signal() -> None:
    controller = HumanInteractionController()

    first = authorize_shared_autonomy_decision(proceed(), controller, goal_registry=GOALS)
    repeated = authorize_shared_autonomy_decision(proceed(), controller, goal_registry=GOALS)

    assert first.status is repeated.status is BridgeStatus.AUTHORIZED
    assert first.policy_goal_adopted
    assert not repeated.policy_goal_adopted
    assert repeated.approved_goal == "victim_a"
    assert not repeated.holds_position


def test_valid_confirm_opens_exact_request_without_autonomous_approval() -> None:
    controller = HumanInteractionController()

    result = authorize_shared_autonomy_decision(confirm(), controller, goal_registry=GOALS, request_id="request-1")

    assert result.status is BridgeStatus.WAITING_FOR_CONFIRMATION
    assert result.confirmation_opened
    assert result.active_request_id == "request-1"
    assert result.approved_goal is None
    assert result.holds_position and result.requests_human_input


def test_confirm_rejects_invalid_candidate_or_missing_request_id() -> None:
    controller = HumanInteractionController()

    invalid_goal = authorize_shared_autonomy_decision(confirm("victim"), controller, goal_registry=GOALS, request_id="request-1")
    missing_id = authorize_shared_autonomy_decision(confirm(), controller, goal_registry=GOALS)

    assert invalid_goal.status is BridgeStatus.INVALID_GOAL
    assert missing_id.status is BridgeStatus.REJECTED
    assert controller.state.active_confirmation is None


def test_confirm_while_paused_preserves_pause_but_stop_blocks_registration() -> None:
    paused = HumanInteractionController()
    paused.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
    stopped = HumanInteractionController()
    stopped.handle_command(HumanCommand("stop", HumanCommandType.STOP))

    paused_result = authorize_shared_autonomy_decision(confirm(), paused, goal_registry=GOALS, request_id="paused-request")
    stopped_result = authorize_shared_autonomy_decision(confirm(), stopped, goal_registry=GOALS, request_id="stopped-request")

    assert paused_result.status is BridgeStatus.WAITING_FOR_CONFIRMATION
    assert paused_result.active_request_id == "paused-request"
    assert paused.state.paused
    assert stopped_result.status is BridgeStatus.INVALID_STATE
    assert stopped.state.active_confirmation is None


def test_confirm_never_replaces_an_active_request() -> None:
    controller = HumanInteractionController()
    first = authorize_shared_autonomy_decision(confirm("victim_a"), controller, goal_registry=GOALS, request_id="request-1")
    replacement = authorize_shared_autonomy_decision(confirm("victim_b"), controller, goal_registry=GOALS, request_id="request-2")

    assert first.status is BridgeStatus.WAITING_FOR_CONFIRMATION
    assert replacement.status is BridgeStatus.INVALID_STATE
    assert controller.state.active_confirmation is not None
    assert controller.state.active_confirmation.request_id == "request-1"
    assert controller.state.approved_goal is None


def test_waiting_and_defer_preserve_state_without_fallback_commitment() -> None:
    controller = HumanInteractionController()
    authorize_shared_autonomy_decision(proceed("victim_b"), controller, goal_registry=GOALS)
    waiting = policy_decision(AutonomyMode.WAITING)
    deferred = policy_decision(AutonomyMode.DEFER, requests_human_input=True)

    waiting_result = authorize_shared_autonomy_decision(waiting, controller, goal_registry=GOALS)
    deferred_result = authorize_shared_autonomy_decision(deferred, controller, goal_registry=GOALS)

    assert waiting_result.status is BridgeStatus.HOLD
    assert deferred_result.status is BridgeStatus.HOLD
    assert waiting_result.approved_goal == deferred_result.approved_goal == "victim_b"
    assert waiting_result.holds_position and deferred_result.holds_position
    assert deferred_result.requests_human_input


def test_policy_human_actions_never_create_duplicate_human_commands() -> None:
    paused = HumanInteractionController()
    paused.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
    pause_decision = policy_decision(AutonomyMode.PAUSE, human_action=HumanAction.PAUSE)
    pause_result = authorize_shared_autonomy_decision(pause_decision, paused, goal_registry=GOALS)

    overridden = HumanInteractionController()
    overridden.handle_command(
        HumanCommand("override", HumanCommandType.OVERRIDE, goal="victim_b"), valid_goals=set(GOALS)
    )
    override_decision = policy_decision(AutonomyMode.WAITING, human_action=HumanAction.OVERRIDE)
    override_result = authorize_shared_autonomy_decision(override_decision, overridden, goal_registry=GOALS)

    assert pause_result.status is BridgeStatus.HOLD
    assert override_result.status is BridgeStatus.HOLD
    assert paused.state.consumed_command_ids == frozenset({"pause"})
    assert overridden.state.consumed_command_ids == frozenset({"override"})


def test_conflicting_observed_human_action_fails_closed() -> None:
    controller = HumanInteractionController()
    decision = policy_decision(AutonomyMode.PAUSE, human_action=HumanAction.PAUSE)

    result = authorize_shared_autonomy_decision(decision, controller, goal_registry=GOALS)

    assert result.status is BridgeStatus.INVALID_STATE
    assert result.holds_position
    assert not controller.state.consumed_command_ids


@pytest.mark.parametrize(
    "decision",
    (
        policy_decision(AutonomyMode.PROCEED, candidate_goal="victim_a", holds_position=False),
        policy_decision(
            AutonomyMode.PROCEED,
            candidate_goal="victim_a",
            approved_goal="victim_b",
            holds_position=False,
        ),
        policy_decision(AutonomyMode.CONFIRM, candidate_goal="victim_a", holds_position=True, requests_human_input=True),
        policy_decision(
            AutonomyMode.CONFIRM,
            candidate_goal="victim_a",
            approved_goal="victim_a",
            requires_human_confirmation=True,
            holds_position=True,
            requests_human_input=True,
        ),
        policy_decision(AutonomyMode.DEFER, approved_goal="victim_a", requests_human_input=True),
        policy_decision("UNSUPPORTED"),
    ),
)
def test_forged_or_inconsistent_policy_decisions_fail_closed(decision: SharedAutonomyDecision) -> None:
    controller = HumanInteractionController()

    result = authorize_shared_autonomy_decision(decision, controller, goal_registry=GOALS, request_id="request-1")

    assert result.status is BridgeStatus.REJECTED
    assert result.holds_position
    assert controller.state.approved_goal is None
    assert controller.state.active_confirmation is None


def test_bridge_has_no_execution_eeg_adaptation_or_ui_dependency() -> None:
    source = Path(interaction_bridge.__file__).read_text(encoding="utf-8")
    forbidden_imports = (
        "src.autonomy",
        "src.cognition",
        "src.eeg",
        "src.models",
        "src.app",
    )

    assert not any(dependency in source for dependency in forbidden_imports)


def test_identical_inputs_on_fresh_controllers_produce_identical_results_and_state() -> None:
    def run() -> tuple[object, object]:
        controller = HumanInteractionController()
        result = authorize_shared_autonomy_decision(confirm(), controller, goal_registry=GOALS, request_id="request-1")
        return result, controller.state

    assert run() == run()
