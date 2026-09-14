"""Deterministic, non-empirical dashboard demo using accepted production interfaces."""

from __future__ import annotations

from dataclasses import asdict

from src.autonomy.environment import EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.execution import PlannerSafetyEnvironmentExecutor
from src.cognitive.bayes import BinaryBayesianGoalEpisode, binary_goal_evidence_from_calibrated_probabilities
from src.cognitive.uncertainty import estimate_binary_uncertainty
from src.control.human_interaction import HumanInteractionController
from src.control.interaction_bridge import authorize_shared_autonomy_decision
from src.control.shared_autonomy import decide_shared_autonomy

DEMO_EVIDENCE = ((0.68, 0.32), (0.72, 0.28), (0.76, 0.24), (0.81, 0.19))


def build_demo_trace() -> dict[str, object]:
    """Exercise the accepted runtime chain using fixed non-empirical evidence."""
    episode = BinaryBayesianGoalEpisode(candidate_a="victim_a", candidate_b="victim_b")
    updates: list[dict[str, object]] = []
    decision = None
    for index, probabilities in enumerate(DEMO_EVIDENCE, start=1):
        result = episode.accept_evidence(
            binary_goal_evidence_from_calibrated_probabilities(probabilities)
        )
        uncertainty = estimate_binary_uncertainty(result.posterior)
        decision = decide_shared_autonomy(result, uncertainty)
        updates.append(
            {
                "update": index,
                "calibrated_left": probabilities[0],
                "calibrated_right": probabilities[1],
                "posterior_a": result.posterior[0],
                "posterior_b": result.posterior[1],
                "entropy_bits": uncertainty.entropy_bits,
                "mode": decision.mode.value,
            }
        )
        if decision.approved_goal is not None:
            break
    assert decision is not None and decision.approved_goal == "victim_a"
    environment = SearchRescueEnvironment(
        EnvironmentConfig(
            rows=3,
            columns=5,
            start=(1, 0),
            goals={"victim_a": (1, 4), "victim_b": (0, 2)},
            risk_map={(0, 3): 1.0},
        )
    )
    interaction = HumanInteractionController()
    authorization = authorize_shared_autonomy_decision(
        decision,
        interaction,
        goal_registry=environment.config.goals,
    )
    approved_goal = interaction.state.approved_goal
    assert approved_goal == "victim_a"
    execution = PlannerSafetyEnvironmentExecutor().execute(
        environment,
        approved_goal=environment.config.goals[approved_goal],
    )
    plan = execution.planning_result
    assert plan is not None
    safety_trace = tuple(
        {
            "step": index,
            "proposed_action": item.proposed_action.name,
            "status": item.status.value,
            "safe": item.safe,
            "approved_action": None if item.approved_action is None else item.approved_action.name,
            "intervention_type": item.intervention_type.value,
            "current_position": item.current_position,
            "proposed_next_position": item.proposed_next_position,
            "requires_replan": item.requires_replan,
        }
        for index, item in enumerate(execution.safety_decisions, start=1)
    )
    return {
        "fixture_kind": "DETERMINISTIC_EXPLANATORY_DEMO_NOT_EMPIRICAL",
        "fixture_metadata": {
            "source": "fixed presentation probabilities; no protected EEG accessed",
            "runtime_entry_boundary": "calibrated Left/Right probability representation passed to the accepted goal-evidence adapter",
            "decoder_invoked": False,
            "calibrator_invoked": False,
            "reportable_experiment": False,
        },
        "updates": tuple(updates),
        "decision": asdict(decision),
        "human_authority": {
            "interface": "HumanInteractionController via authorize_shared_autonomy_decision",
            "authorization_status": authorization.status.value,
            "policy_goal_adopted": authorization.policy_goal_adopted,
            "approved_goal": approved_goal,
            "human_commands": (),
            "note": "No human command was required because the accepted policy reached PROCEED; STOP/PAUSE/confirmation authority remained enforced by the controller boundary.",
        },
        "approved_goal": approved_goal,
        "environment": {
            "start": environment.config.start,
            "goal_registry": dict(environment.config.goals),
            "prohibited_cells": tuple(
                coordinate
                for coordinate, risk in environment.config.risk_map.items()
                if risk >= 1.0
            ),
        },
        "plan": {
            "status": plan.status.value,
            "path": plan.path,
            "actions": tuple(action.name for action in plan.actions),
            "path_cost": plan.path_cost,
            "cumulative_risk": plan.cumulative_risk,
        },
        "safety_decisions": safety_trace,
        "execution": {
            "status": execution.status.value,
            "executed_actions": tuple(action.name for action in execution.executed_actions),
            "visited_positions": execution.visited_positions,
            "terminal_position": execution.final_position,
            "environment_terminated": execution.terminated,
            "reached_goal": environment.state.reached_goal,
            "goal_reached": environment.state.reached_goal == approved_goal,
            "cumulative_risk": plan.cumulative_risk,
            "reason": execution.reason,
        },
    }
