"""Deterministic M7-T02 simulated operator over the accepted human-authority API."""

from __future__ import annotations

from dataclasses import dataclass

from src.cognitive.adaptation import ExplicitFeedbackObservation, FeedbackAction
from src.control.human_interaction import (
    CommandStatus,
    HumanCommand,
    HumanCommandType,
    HumanInteractionController,
)
from src.evaluation.final_contract import SIMULATED_HUMAN_POLICY_ID


class SimulatedHumanError(ValueError):
    """Raised when a frozen simulated-human interaction cannot be represented safely."""


@dataclass(frozen=True)
class SimulatedHumanResult:
    policy_id: str
    interpretation: str
    episode_id: str
    autonomy_mode: str
    proposed_goal: str | None
    intended_goal: str
    command_type: str | None
    command_id: str | None
    request_id: str | None
    command_status: str | None
    final_approved_goal: str | None
    correction_applied: bool
    explicit_feedback: ExplicitFeedbackObservation | None


def apply_simulated_human_policy(
    *,
    episode_id: str,
    autonomy_mode: str,
    proposed_goal: str | None,
    intended_goal: str,
    candidate_names: tuple[str, str],
    controller: HumanInteractionController,
) -> SimulatedHumanResult:
    """Apply only the deterministic D-080 CONFIRM/correction/DEFER rules."""

    if not episode_id or not isinstance(controller, HumanInteractionController):
        raise SimulatedHumanError("A non-empty episode ID and interaction controller are required.")
    if len(candidate_names) != 2 or len(set(candidate_names)) != 2 or intended_goal not in candidate_names:
        raise SimulatedHumanError("The intended goal must belong to the exact ordered candidate pair.")
    if autonomy_mode == "PROCEED":
        return SimulatedHumanResult(
            SIMULATED_HUMAN_POLICY_ID,
            "simulated human / offline software evaluation",
            episode_id,
            autonomy_mode,
            proposed_goal,
            intended_goal,
            None,
            None,
            None,
            None,
            proposed_goal,
            False,
            None,
        )
    if autonomy_mode == "CONFIRM":
        if proposed_goal not in candidate_names:
            raise SimulatedHumanError("CONFIRM requires a valid proposed candidate goal.")
        request_id = f"{episode_id}::confirmation"
        controller.open_confirmation_request(request_id, proposed_goal)
        if proposed_goal == intended_goal:
            command_type = HumanCommandType.CONFIRM
            command = HumanCommand(
                command_id=f"{episode_id}::simulated-confirm",
                command_type=command_type,
                request_id=request_id,
                goal=proposed_goal,
            )
            correction = False
        else:
            command_type = HumanCommandType.OVERRIDE
            command = HumanCommand(
                command_id=f"{episode_id}::simulated-override",
                command_type=command_type,
                goal=intended_goal,
            )
            correction = True
    elif autonomy_mode == "DEFER":
        if proposed_goal is not None:
            raise SimulatedHumanError("DEFER must not carry an autonomous argmax proposal.")
        request_id = None
        command_type = HumanCommandType.OVERRIDE
        command = HumanCommand(
            command_id=f"{episode_id}::simulated-defer-override",
            command_type=command_type,
            goal=intended_goal,
        )
        correction = True
    else:
        raise SimulatedHumanError("Primary simulated-human policy accepts only PROCEED, CONFIRM, or DEFER.")

    command_result = controller.handle_command(command, valid_goals=set(candidate_names))
    if command_result.status is not CommandStatus.APPLIED or not command_result.accepted:
        raise SimulatedHumanError("Accepted human interaction API rejected the frozen simulated command.")
    if command_result.approved_goal != intended_goal:
        raise SimulatedHumanError("Simulated command did not produce the evaluation-only intended goal.")
    feedback_action = FeedbackAction(command_type.value)
    feedback = ExplicitFeedbackObservation(
        subject_id="__assigned_by_orchestrator__",
        candidate_a_id=candidate_names[0],
        candidate_b_id=candidate_names[1],
        action=feedback_action,
        source_observation_id=str(command.command_id),
        approved_goal_id=str(command_result.approved_goal),
        between_episodes=True,
    )
    return SimulatedHumanResult(
        SIMULATED_HUMAN_POLICY_ID,
        "simulated human / offline software evaluation",
        episode_id,
        autonomy_mode,
        proposed_goal,
        intended_goal,
        command_type.value,
        str(command.command_id),
        request_id,
        command_result.status.value,
        str(command_result.approved_goal),
        correction,
        feedback,
    )


def feedback_for_subject(result: SimulatedHumanResult, subject_key: str) -> ExplicitFeedbackObservation | None:
    """Bind applied explicit API feedback to an anonymous subject; never accept hidden truth directly."""

    feedback = result.explicit_feedback
    if feedback is None:
        return None
    if not subject_key:
        raise SimulatedHumanError("Anonymous subject key must be non-empty.")
    return ExplicitFeedbackObservation(
        subject_id=subject_key,
        candidate_a_id=feedback.candidate_a_id,
        candidate_b_id=feedback.candidate_b_id,
        action=feedback.action,
        source_observation_id=feedback.source_observation_id,
        approved_goal_id=feedback.approved_goal_id,
        between_episodes=True,
    )
