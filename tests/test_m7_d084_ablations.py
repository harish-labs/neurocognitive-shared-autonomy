from __future__ import annotations

import numpy as np

from src.control.human_interaction import HumanCommand, HumanCommandType, HumanInteractionController
from src.evaluation.ablation_semantics import (
    D084_ABLATION_SEMANTICS,
    evaluate_full_minus_bayes,
    evaluate_full_minus_uncertainty,
)
from src.evaluation.conditions import ABLATIONS, PRINCIPAL_CONDITIONS, ConditionId
from src.evaluation.experiments import DevelopmentEpisodeInput, run_development_condition
from src.evaluation.simulated_human import apply_simulated_human_policy


CANDIDATES = ("victim_a", "victim_b")


def test_full_minus_bayes_uses_calibrated_running_mean_without_bayesian_recursion() -> None:
    evidence = ((0.8, 0.2), (0.6, 0.4), (0.6, 0.4), (0.6, 0.4), (0.6, 0.4))
    result = evaluate_full_minus_bayes(evidence, candidate_names=CANDIDATES)
    assert result.accepted_evidence_count == 5
    assert result.posterior == (0.64, 0.36)
    assert result.posterior_history[1] == (0.7, 0.30000000000000004)
    assert result.autonomy_mode == "DEFER"
    assert result.committed_goal is None
    assert result.posterior != (0.970754716981132, 0.029245283018867928)
    assert D084_ABLATION_SEMANTICS["full_minus_bayes"]["aggregation"] == "cumulative_arithmetic_mean_of_calibrated_binary_evidence"


def test_full_minus_bayes_proceeds_early_only_at_running_mean_threshold() -> None:
    result = evaluate_full_minus_bayes(
        ((0.89, 0.11), (0.91, 0.09), (0.5, 0.5), (0.5, 0.5), (0.5, 0.5)), candidate_names=CANDIDATES
    )
    assert result.accepted_evidence_count == 2
    assert result.posterior == (0.9, 0.1)
    assert result.autonomy_mode == "PROCEED"
    assert result.committed_goal == "victim_a"


def test_full_minus_bayes_final_confirm_and_defer_preserve_human_behavior() -> None:
    confirm = evaluate_full_minus_bayes(((0.8, 0.2),) * 5, candidate_names=CANDIDATES)
    defer = evaluate_full_minus_bayes(((0.74, 0.26),) * 5, candidate_names=CANDIDATES)
    assert (confirm.accepted_evidence_count, confirm.autonomy_mode, confirm.candidate_goal, confirm.committed_goal) == (
        5,
        "CONFIRM",
        "victim_a",
        None,
    )
    assert (defer.accepted_evidence_count, defer.autonomy_mode, defer.candidate_goal, defer.committed_goal) == (
        5,
        "DEFER",
        None,
        None,
    )
    confirm_human = apply_simulated_human_policy(
        episode_id="confirm", autonomy_mode=confirm.autonomy_mode, proposed_goal=confirm.candidate_goal,
        intended_goal="victim_a", candidate_names=CANDIDATES, controller=HumanInteractionController(),
    )
    defer_human = apply_simulated_human_policy(
        episode_id="defer", autonomy_mode=defer.autonomy_mode, proposed_goal=defer.candidate_goal,
        intended_goal="victim_b", candidate_names=CANDIDATES, controller=HumanInteractionController(),
    )
    assert confirm_human.command_type == "CONFIRM"
    assert defer_human.command_type == "OVERRIDE"
    assert defer_human.final_approved_goal == "victim_b"


def test_full_minus_bayes_changes_only_sequential_bayes_from_full() -> None:
    full = PRINCIPAL_CONDITIONS[ConditionId.D].components
    ablation = ABLATIONS["full_minus_bayes"].components
    differences = [name for name in full.__dataclass_fields__ if getattr(full, name) != getattr(ablation, name)]
    assert differences == ["sequential_bayes"]
    assert ablation.calibration and ablation.uncertainty_gating and ablation.adaptation and ablation.hard_safety


def test_full_minus_uncertainty_uses_all_five_bayesian_updates_without_early_commitment() -> None:
    evidence = ((0.99, 0.01),) * 5
    result = evaluate_full_minus_uncertainty(evidence, candidate_names=CANDIDATES)
    assert result.accepted_evidence_count == 5
    assert len(result.posterior_history) == 5
    assert result.posterior_history[0] == (0.99, 0.01)
    assert result.autonomy_mode == "PROCEED"
    assert result.committed_goal == "victim_a"
    assert not result.tie_break_applied


def test_full_minus_uncertainty_final_argmax_tie_breaks_to_candidate_a_and_entropy_is_descriptive() -> None:
    result = evaluate_full_minus_uncertainty(((0.5, 0.5),) * 5, candidate_names=CANDIDATES)
    assert result.posterior == (0.5, 0.5)
    assert result.entropy_bits == 1.0
    assert result.autonomy_mode == "PROCEED"
    assert result.committed_goal == "victim_a"
    assert result.tie_break_applied
    assert D084_ABLATION_SEMANTICS["full_minus_uncertainty"]["entropy_role"] == "descriptive_only"


def test_full_minus_uncertainty_generates_no_uncertainty_human_intervention_and_preserves_emergency_authority() -> None:
    decision = evaluate_full_minus_uncertainty(((0.5, 0.5),) * 5, candidate_names=CANDIDATES)
    human = apply_simulated_human_policy(
        episode_id="uncertainty-off", autonomy_mode=decision.autonomy_mode, proposed_goal=decision.committed_goal,
        intended_goal="victim_b", candidate_names=CANDIDATES, controller=HumanInteractionController(),
    )
    assert human.command_type is None
    controller = HumanInteractionController()
    pause = controller.handle_command(HumanCommand("pause", HumanCommandType.PAUSE))
    stop = controller.handle_command(HumanCommand("stop", HumanCommandType.STOP))
    assert pause.accepted and stop.accepted and stop.stopped


def test_d084_does_not_change_full_condition_execution() -> None:
    episode = DevelopmentEpisodeInput(
        episode_id="full-regression", subject_key="subject", split="synthetic", decoder_family="csp_lda",
        candidate_names=CANDIDATES, raw_probabilities=((0.9, 0.1),) * 5,
        calibrated_probabilities=((0.7, 0.3),) * 5, true_goal="victim_a",
    )
    result = run_development_condition(episode, "D")
    assert (result.accepted_evidence_count, result.autonomy_mode, result.committed_goal) == (3, "PROCEED", "victim_a")
    assert np.isclose(result.posterior[0], 0.927027027027027)
