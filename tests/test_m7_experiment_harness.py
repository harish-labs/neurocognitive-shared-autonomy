import json

import pytest

from src.cognitive.adaptation import ExplicitFeedbackObservation, FeedbackAction, PriorPersonalizer
from src.evaluation.experiments import DevelopmentEpisodeInput, ExperimentError, run_development_condition
from src.evaluation.schemas import ExperimentProvenance, ExperimentResult, ExperimentStatus, SchemaError


def _episode(decoder_family="csp_lda", split="synthetic"):
    return DevelopmentEpisodeInput(
        episode_id="dev-001",
        subject_key="anon-s01",
        split=split,
        decoder_family=decoder_family,
        candidate_names=("victim-a", "victim-b"),
        raw_probabilities=((0.8, 0.2),) * 5,
        calibrated_probabilities=((0.7, 0.3),) * 5,
        true_goal="victim-a",
    )


@pytest.mark.parametrize("decoder_family", ["csp_lda", "eegnet"])
def test_synthetic_orchestration_supports_both_approved_decoder_labels(decoder_family):
    result_a = run_development_condition(_episode(decoder_family), "A")
    result_b = run_development_condition(_episode(decoder_family), "B")
    result_c = run_development_condition(_episode(decoder_family), "C")
    result_d = run_development_condition(_episode(decoder_family), "D")
    assert (result_a.evidence_source, result_a.accepted_evidence_count, result_a.autonomy_mode) == ("raw_identity", 1, "PROCEED")
    assert (result_b.evidence_source, result_b.accepted_evidence_count, result_b.autonomy_mode) == ("calibrated", 1, "DEFER")
    assert result_c.accepted_evidence_count == 3
    assert result_c.autonomy_mode == "PROCEED"
    assert result_d.accepted_evidence_count == 3
    assert result_d.autonomy_mode == "PROCEED"
    assert result_d.initial_prior == (0.5, 0.5)


def test_orchestration_applies_robustness_after_condition_calibration_selection():
    result = run_development_condition(_episode(), "B", perturbation_family="R1", severity=1.0)
    assert result.evidence_source == "calibrated"
    assert result.posterior == (0.5, 0.5)
    assert result.autonomy_mode == "DEFER"
    assert result.perturbation.original_evidence == ((0.7, 0.3),)


@pytest.mark.parametrize(
    ("probability", "expected_mode"),
    [(0.90, "PROCEED"), (0.899, "CONFIRM"), (0.75, "CONFIRM"), (0.749, "DEFER")],
)
def test_system_b_uses_exact_approved_single_observation_boundaries(probability, expected_mode):
    value = DevelopmentEpisodeInput(
        "dev-boundary", "anon-s01", "validation", "csp_lda", ("victim-a", "victim-b"),
        ((probability, 1 - probability),), ((probability, 1 - probability),), "victim-a",
    )
    assert run_development_condition(value, "B").autonomy_mode == expected_mode


def test_system_d_uses_only_accepted_personalizer_state_while_c_stays_uniform():
    personalizer = PriorPersonalizer()
    for index in range(3):
        personalizer.record_explicit_feedback(
            ExplicitFeedbackObservation(
                subject_id="anon-s01", candidate_a_id="victim-a", candidate_b_id="victim-b",
                action=FeedbackAction.CONFIRM, source_observation_id=f"feedback-{index}", approved_goal_id="victim-a",
            )
        )
    neutral = DevelopmentEpisodeInput(
        "dev-adapt", "anon-s01", "development", "eegnet", ("victim-a", "victim-b"),
        ((0.5, 0.5),) * 5, ((0.5, 0.5),) * 5, "victim-a",
    )
    result_c = run_development_condition(neutral, "C", personalizer=personalizer)
    result_d = run_development_condition(neutral, "D", personalizer=personalizer)
    assert result_c.initial_prior == (0.5, 0.5)
    assert result_c.autonomy_mode == "DEFER"
    assert result_d.initial_prior == (0.75, 0.25)
    assert result_d.autonomy_mode == "CONFIRM"


@pytest.mark.parametrize("split", ["test", "final_test", "protected_final_test"])
def test_m7_t01_orchestration_refuses_protected_test_execution(split):
    with pytest.raises(ExperimentError, match="refuses protected"):
        run_development_condition(_episode(split=split), "A")


def test_result_schema_is_json_ready_and_requires_metric_denominators():
    provenance = ExperimentProvenance(
        experiment_family="E6",
        experiment_id="dev-e6-001",
        condition="D",
        ablation=None,
        decoder_family="eegnet",
        split="development",
        evaluation_track="cross_subject_development",
        subject_key="anon-s01",
        seeds={"bootstrap": 42},
        perturbation_family=None,
        perturbation_severity=None,
        perturbation_selection_rule=None,
        selected_indices=(),
        effective_operational_configuration={"source": "synthetic_fixture"},
        scientific_policy_ids=("D-077", "D-079"),
        input_provenance=({"episode_id": "dev-001"},),
        software_git_sha="caller-supplied-sha",
        status=ExperimentStatus.DEVELOPMENT_ONLY,
    )
    result = ExperimentResult(
        provenance=provenance,
        metric_definitions={"task_success_rate": {"evaluation_unit": "episode", "denominator": "evaluated_episodes"}},
        subject_level_metrics=({"subject_key": "anon-s01", "task_success_rate": 1.0},),
        aggregate_metrics={"task_success_rate": 1.0},
        statistical_outputs={},
    )
    assert json.loads(result.to_json())["provenance"]["status"] == "DEVELOPMENT_ONLY"
    malformed = ExperimentResult(provenance, {"bad": {"evaluation_unit": "episode"}}, (), {}, {})
    with pytest.raises(SchemaError, match="denominator"):
        malformed.validate()


def test_schema_refuses_final_test_and_fabricated_final_status():
    base = dict(
        experiment_family="E6", experiment_id="x", condition="D", ablation=None, decoder_family="eegnet",
        evaluation_track="cross_subject", subject_key="s", seeds={}, perturbation_family=None,
        perturbation_severity=None, perturbation_selection_rule=None, selected_indices=(), effective_operational_configuration={},
        scientific_policy_ids=("D-077",), input_provenance=(), software_git_sha="sha",
    )
    with pytest.raises(SchemaError):
        ExperimentProvenance(split="final_test", status=ExperimentStatus.DEVELOPMENT_ONLY, **base).validate()
    with pytest.raises(SchemaError):
        ExperimentProvenance(split="development", status=ExperimentStatus.VALID, **base).validate()
