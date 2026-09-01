from __future__ import annotations

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.control.human_interaction import (
    CommandStatus,
    HumanCommand,
    HumanCommandType,
    HumanInteractionController,
    HumanInteractionError,
)
import src.control.human_interaction as human_interaction


VALID_GOALS = {"victim_a", "victim_b"}


def command(
    command_id: str,
    command_type: HumanCommandType,
    *,
    request_id: str | None = None,
    goal: object | None = None,
) -> HumanCommand:
    return HumanCommand(command_id, command_type, request_id=request_id, goal=goal)


def test_confirmation_request_is_immutable_unique_and_single_active() -> None:
    controller = HumanInteractionController()
    request = controller.open_confirmation_request("request-1", "victim_a")

    assert request.request_id == "request-1"
    assert request.candidate_goal == "victim_a"
    with pytest.raises(AttributeError):
        request.request_id = "changed"  # type: ignore[misc]
    with pytest.raises(HumanInteractionError, match="Only one"):
        controller.open_confirmation_request("request-2", "victim_b")


def test_exact_active_confirm_approves_its_candidate_and_closes_request() -> None:
    controller = HumanInteractionController()
    controller.open_confirmation_request("request-1", "victim_a")

    result = controller.handle_command(command("command-1", HumanCommandType.CONFIRM, request_id="request-1"))

    assert result.status is CommandStatus.APPLIED
    assert result.accepted and result.applied
    assert result.approved_goal == "victim_a"
    assert result.active_request_id is None
    assert not result.requires_fresh_execution
    assert controller.state.closed_request_ids == frozenset({"request-1"})


def test_confirm_cannot_substitute_another_goal() -> None:
    controller = HumanInteractionController()
    controller.open_confirmation_request("request-1", "victim_a")

    result = controller.handle_command(
        command("command-1", HumanCommandType.CONFIRM, request_id="request-1", goal="victim_b")
    )

    assert result.status is CommandStatus.REJECTED
    assert result.approved_goal is None
    assert result.active_request_id == "request-1"


def test_stale_and_consumed_confirmation_requests_cannot_apply_again() -> None:
    controller = HumanInteractionController()
    controller.open_confirmation_request("request-1", "victim_a")

    stale = controller.handle_command(command("command-stale", HumanCommandType.CONFIRM, request_id="other"))
    accepted = controller.handle_command(command("command-accept", HumanCommandType.CONFIRM, request_id="request-1"))
    repeated = controller.handle_command(command("command-repeat", HumanCommandType.CONFIRM, request_id="request-1"))

    assert stale.status is CommandStatus.STALE_REQUEST
    assert accepted.status is CommandStatus.APPLIED
    assert repeated.status is CommandStatus.STALE_REQUEST
    assert repeated.approved_goal == "victim_a"
    with pytest.raises(HumanInteractionError, match="unique"):
        controller.open_confirmation_request("request-1", "victim_b")


def test_command_id_is_consumed_once_without_repeating_effect() -> None:
    controller = HumanInteractionController()
    first = controller.handle_command(command("command-1", HumanCommandType.PAUSE))
    duplicate = controller.handle_command(command("command-1", HumanCommandType.RESUME))

    assert first.status is CommandStatus.APPLIED
    assert duplicate.status is CommandStatus.ALREADY_CONSUMED
    assert duplicate.paused
    assert not duplicate.requires_fresh_execution
    assert controller.state.consumed_command_ids == frozenset({"command-1"})


def test_malformed_command_id_is_rejected_without_consumption() -> None:
    controller = HumanInteractionController()

    result = controller.handle_command(HumanCommand("", HumanCommandType.PAUSE))

    assert result.status is CommandStatus.REJECTED
    assert not controller.state.consumed_command_ids


def test_valid_override_changes_approved_goal_and_cancels_confirmation() -> None:
    controller = HumanInteractionController()
    controller.open_confirmation_request("request-1", "victim_a")

    result = controller.handle_command(
        command("command-1", HumanCommandType.OVERRIDE, goal="victim_b"), valid_goals=VALID_GOALS
    )

    assert result.status is CommandStatus.APPLIED
    assert result.approved_goal == "victim_b"
    assert result.active_request_id is None
    assert result.requires_fresh_execution
    assert controller.state.closed_request_ids == frozenset({"request-1"})


def test_invalid_override_goal_is_consumed_without_changing_state() -> None:
    controller = HumanInteractionController()
    controller.open_confirmation_request("request-1", "victim_a")

    result = controller.handle_command(
        command("command-1", HumanCommandType.OVERRIDE, goal="unknown"), valid_goals=VALID_GOALS
    )

    assert result.status is CommandStatus.INVALID_GOAL
    assert result.approved_goal is None
    assert result.active_request_id == "request-1"
    assert controller.state.consumed_command_ids == frozenset({"command-1"})


def test_override_accepts_current_goal_values_from_a_mapping() -> None:
    controller = HumanInteractionController()

    result = controller.handle_command(
        command("command-1", HumanCommandType.OVERRIDE, goal=(1, 2)),
        valid_goals={"victim_a": (1, 2)},
    )

    assert result.status is CommandStatus.APPLIED
    assert result.approved_goal == (1, 2)


def test_override_while_paused_preserves_pause() -> None:
    controller = HumanInteractionController()
    controller.handle_command(command("pause", HumanCommandType.PAUSE))

    result = controller.handle_command(
        command("override", HumanCommandType.OVERRIDE, goal="victim_b"), valid_goals=VALID_GOALS
    )

    assert result.status is CommandStatus.APPLIED
    assert result.paused
    assert result.approved_goal == "victim_b"
    assert result.requires_fresh_execution


def test_pause_preserves_approved_goal_and_repeated_pause_is_idempotent() -> None:
    controller = HumanInteractionController()
    controller.handle_command(command("override", HumanCommandType.OVERRIDE, goal="victim_a"), valid_goals=VALID_GOALS)

    first = controller.handle_command(command("pause-1", HumanCommandType.PAUSE))
    repeated = controller.handle_command(command("pause-2", HumanCommandType.PAUSE))

    assert first.approved_goal == repeated.approved_goal == "victim_a"
    assert first.applied
    assert not repeated.applied
    assert repeated.paused


def test_resume_only_from_pause_preserves_goal_and_requests_fresh_execution() -> None:
    controller = HumanInteractionController()
    controller.handle_command(command("override", HumanCommandType.OVERRIDE, goal="victim_a"), valid_goals=VALID_GOALS)

    invalid = controller.handle_command(command("resume-invalid", HumanCommandType.RESUME))
    controller.handle_command(command("pause", HumanCommandType.PAUSE))
    resumed = controller.handle_command(command("resume", HumanCommandType.RESUME))

    assert invalid.status is CommandStatus.INVALID_STATE
    assert resumed.status is CommandStatus.APPLIED
    assert resumed.approved_goal == "victim_a"
    assert not resumed.paused
    assert resumed.requires_fresh_execution


def test_resume_without_goal_only_clears_pause_and_invents_nothing() -> None:
    controller = HumanInteractionController()
    controller.handle_command(command("pause", HumanCommandType.PAUSE))

    result = controller.handle_command(command("resume", HumanCommandType.RESUME))

    assert result.status is CommandStatus.APPLIED
    assert result.approved_goal is None
    assert not result.requires_fresh_execution


def test_stop_is_terminal_cancels_confirmation_and_blocks_lower_authority_commands() -> None:
    controller = HumanInteractionController()
    controller.open_confirmation_request("request-1", "victim_a")
    stopped = controller.handle_command(command("stop", HumanCommandType.STOP))

    confirm = controller.handle_command(command("confirm", HumanCommandType.CONFIRM, request_id="request-1"))
    override = controller.handle_command(
        command("override", HumanCommandType.OVERRIDE, goal="victim_b"), valid_goals=VALID_GOALS
    )
    pause = controller.handle_command(command("pause", HumanCommandType.PAUSE))
    resume = controller.handle_command(command("resume", HumanCommandType.RESUME))

    assert stopped.status is CommandStatus.APPLIED
    assert stopped.stopped and stopped.paused and stopped.active_request_id is None
    assert all(result.status is CommandStatus.INVALID_STATE for result in (confirm, override, pause, resume))
    assert all(result.stopped and result.paused for result in (confirm, override, pause, resume))
    assert controller.state.closed_request_ids == frozenset({"request-1"})


def test_stop_is_idempotent_for_a_distinct_command_id() -> None:
    controller = HumanInteractionController()
    controller.handle_command(command("stop-1", HumanCommandType.STOP))

    repeated = controller.handle_command(command("stop-2", HumanCommandType.STOP))

    assert repeated.status is CommandStatus.APPLIED
    assert repeated.stopped and repeated.paused
    assert not repeated.requires_fresh_execution


def test_reset_is_explicit_and_only_replaces_interaction_state() -> None:
    controller = HumanInteractionController()
    controller.handle_command(command("stop", HumanCommandType.STOP))

    controller.reset()

    assert controller.state.approved_goal is None
    assert controller.state.active_confirmation is None
    assert not controller.state.paused
    assert not controller.state.stopped
    assert not controller.state.consumed_command_ids


def test_handlers_have_no_execution_stack_dependencies_or_calls() -> None:
    controller = HumanInteractionController()
    forbidden_dependencies = (
        "src.autonomy",
        "src.cognition",
        "src.eeg",
        "src.models",
    )

    source = Path(human_interaction.__file__).read_text(encoding="utf-8")
    assert not any(dependency in source for dependency in forbidden_dependencies)
    controller.open_confirmation_request("request-1", "victim_a")
    result = controller.handle_command(command("confirm", HumanCommandType.CONFIRM, request_id="request-1"))

    assert result.status is CommandStatus.APPLIED


def test_identical_sequences_produce_identical_state_and_results() -> None:
    def run_sequence() -> tuple[object, ...]:
        controller = HumanInteractionController()
        controller.open_confirmation_request("request-1", "victim_a")
        return (
            controller.handle_command(command("confirm", HumanCommandType.CONFIRM, request_id="request-1")),
            controller.handle_command(command("pause", HumanCommandType.PAUSE)),
            controller.handle_command(command("resume", HumanCommandType.RESUME)),
            controller.state,
        )

    assert run_sequence() == run_sequence()
