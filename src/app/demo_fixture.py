"""Deterministic, non-empirical dashboard demo using accepted production interfaces."""

from __future__ import annotations

from dataclasses import asdict

from src.autonomy.environment import EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.planner import RiskAwareAStarPlanner
from src.cognitive.bayes import BinaryBayesianGoalEpisode, binary_goal_evidence_from_calibrated_probabilities
from src.cognitive.uncertainty import estimate_binary_uncertainty
from src.control.shared_autonomy import decide_shared_autonomy

DEMO_EVIDENCE = ((0.68, 0.32), (0.72, 0.28), (0.76, 0.24), (0.81, 0.19))


def build_demo_trace() -> dict[str, object]:
    """Exercise Bayes, uncertainty, policy, and A* with a fixed explanatory fixture."""
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
        )
    )
    plan = RiskAwareAStarPlanner().plan(
        environment,
        start=environment.state.position,
        approved_goal=environment.config.goals[decision.approved_goal],
    )
    return {
        "fixture_kind": "DETERMINISTIC_EXPLANATORY_DEMO_NOT_EMPIRICAL",
        "source": "fixed calibrated-probability fixture; no protected EEG accessed",
        "updates": tuple(updates),
        "decision": asdict(decision),
        "plan": {
            "status": plan.status.value,
            "path": plan.path,
            "actions": tuple(action.name for action in plan.actions),
            "path_cost": plan.path_cost,
            "cumulative_risk": plan.cumulative_risk,
        },
    }
