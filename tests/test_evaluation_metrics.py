import numpy as np
import pytest

from src.autonomy.environment import Action, EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.planner import RiskAwareAStarPlanner
from src.autonomy.safety import SafetyController
from src.evaluation.autonomy_metrics import (
    EpisodeRecord,
    compute_autonomy_metrics,
    compute_planning_safety_metrics,
)
from src.evaluation.eeg_metrics import calibration_metrics, classification_metrics


def test_eeg_classification_metrics_are_analytic_and_denominators_explicit():
    result = classification_metrics(["left", "left", "right", "right"], ["left", "right", "right", "right"])
    assert result.sample_count == 4
    assert result.correct_count == 3
    assert result.accuracy == 0.75
    assert result.balanced_accuracy == 0.75
    assert result.confusion_matrix == ((1, 1), (0, 2))
    assert result.per_class[0].precision == 1.0
    assert result.per_class[0].recall == 0.5
    assert result.per_class[1].precision == pytest.approx(2 / 3)


def test_undefined_class_denominators_are_none_not_silently_zero():
    result = classification_metrics(["left", "left"], ["left", "left"])
    assert result.per_class[1].true_count == 0
    assert result.per_class[1].predicted_count == 0
    assert result.per_class[1].precision is None
    assert result.per_class[1].recall is None
    assert result.balanced_accuracy is None
    assert result.macro_f1 is None


def test_d050_equal_width_reliability_and_brier_are_reused_exactly():
    probabilities = np.asarray([[0.8, 0.2], [0.3, 0.7], [0.1, 0.9], [0.6, 0.4]])
    result = calibration_metrics(probabilities, ["left", "right", "left", "right"])
    assert result.bin_count == 10
    assert np.asarray([(item.lower_bound, item.upper_bound) for item in result.reliability_bins]) == pytest.approx(
        np.asarray([(index / 10, (index + 1) / 10) for index in range(10)])
    )
    assert result.expected_calibration_error == pytest.approx(0.5)
    assert result.brier_score == pytest.approx((0.04 + 0.09 + 0.81 + 0.36) / 4)
    with pytest.raises(ValueError, match="at least one"):
        calibration_metrics(np.empty((0, 2)), [])


def test_full_system_rates_keep_wrong_goal_and_success_denominators_separate():
    records = (
        EpisodeRecord("e1", "s1", "A", "A", 0.95, 0.2, 2, "PROCEED", navigation_steps=2, path_length=2, cumulative_risk=0.25, path_cost=2.5, proposed_actions=2, executed_actions=2, reached_goal="A"),
        EpisodeRecord("e2", "s2", "A", "B", 0.92, 0.3, 3, "PROCEED", navigation_steps=1, path_length=1, cumulative_risk=0.0, path_cost=1.0, proposed_actions=2, executed_actions=1, unsafe_action_attempts=1, reached_goal="B"),
        EpisodeRecord("e3", "s3", "A", None, 0.6, 0.9, 5, "DEFER", deferrals=1, no_safe_path=True),
    )
    result = compute_autonomy_metrics(records)
    assert result.wrong_goal.numerator == 1
    assert result.wrong_goal.denominator == 2
    assert result.wrong_goal.denominator_unit == "committed_episode"
    assert result.task_success.numerator == 1
    assert result.task_success.denominator == 3
    assert result.task_success.denominator_unit == "evaluated_episode"
    assert result.mean_accepted_evidence_count == pytest.approx(10 / 3)
    assert result.decision_latency_episode_count == 3
    assert result.posterior_episode_count == 3
    assert result.total_navigation_steps == 3
    assert result.no_safe_path_count == 1


def test_controlled_planning_and_safety_accounting_consumes_accepted_results():
    environment = SearchRescueEnvironment(EnvironmentConfig(rows=2, columns=3, start=(0, 0), goals={"goal": (0, 2)}, risk_map={(0, 1): 0.25}))
    plan = RiskAwareAStarPlanner().plan(environment, start=(0, 0), approved_goal=(0, 2))
    safety = SafetyController()
    decisions = (
        safety.check(environment, current_position=(0, 0), proposed_action=Action.RIGHT),
        safety.check(environment, current_position=(0, 0), proposed_action=Action.UP),
    )
    unreachable_environment = SearchRescueEnvironment(EnvironmentConfig(rows=1, columns=3, start=(0, 0), goals={"goal": (0, 2)}, blocked_cells=frozenset({(0, 1)})))
    no_path = RiskAwareAStarPlanner().plan(unreachable_environment, start=(0, 0), approved_goal=(0, 2))
    result = compute_planning_safety_metrics((plan, no_path), decisions, replanning_count=0, executed_action_count=1, executed_hard_safety_violations=0)
    assert result.planning_success.rate == 0.5
    assert result.no_safe_path_count == 1
    assert result.path_length_sum == 2
    assert result.cumulative_risk_sum == 0.25
    assert result.path_cost_sum == 2.5
    assert result.unsafe_action_attempts == 1
    assert result.safety_violation_rate.denominator == 1
