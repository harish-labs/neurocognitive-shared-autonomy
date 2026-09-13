import json

import pytest

from src.cognitive.adaptation import ExplicitFeedbackObservation, FeedbackAction, PriorPersonalizer
from src.evaluation.experiments import (
    DevelopmentEpisodeInput,
    ExperimentError,
    run_development_condition,
    run_development_condition_batch,
)
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


def _episode_batch(count=20, *, observations=1, split="synthetic"):
    return tuple(
        DevelopmentEpisodeInput(
            episode_id=f"dev-{index:03d}",
            subject_key=f"anon-s{index:03d}",
            split=split,
            decoder_family="csp_lda",
            candidate_names=("victim-a", "victim-b"),
            raw_probabilities=((0.8, 0.2),) * observations,
            calibrated_probabilities=((0.7, 0.3),) * observations,
            true_goal="victim-a",
        )
        for index in range(count)
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


def test_single_episode_r2_fails_closed_instead_of_rounding_per_episode():
    with pytest.raises(ExperimentError, match="evaluation batch"):
        run_development_condition(_episode(), "A", perturbation_family="R2", severity=0.1, perturbation_seed=42)


def test_r2_system_a_one_observation_episodes_use_one_global_population_selection():
    batch = run_development_condition_batch(
        _episode_batch(),
        "A",
        perturbation_family="R2",
        severity=0.1,
        perturbation_seed=42,
    )
    perturbation = batch.population_perturbation
    assert perturbation.requested_q == 0.1
    assert perturbation.population_size == 20
    assert perturbation.realized_count == 2
    assert perturbation.realized_fraction == 0.1
    assert len(perturbation.selected_observation_ids) == 2
    assert tuple(assignment.global_indices for assignment in batch.episode_assignments) == tuple(
        (index,) for index in range(20)
    )
    assert sum(bool(assignment.selected_global_indices) for assignment in batch.episode_assignments) == 2
    for index, (result, assignment) in enumerate(zip(batch.episode_results, batch.episode_assignments)):
        expected = (0.2, 0.8) if index in perturbation.selected_indices else (0.8, 0.2)
        assert result.posterior == expected
        assert assignment.perturbed_evidence == (expected,)
        assert result.correct_commitment is (index not in perturbation.selected_indices)
    assert all(episode.true_goal == "victim-a" for episode in _episode_batch())


def test_r2_frozen_q_levels_are_distinct_on_adequate_system_b_population():
    batches = {
        q: run_development_condition_batch(
            _episode_batch(), "B", perturbation_family="R2", severity=q, perturbation_seed=17
        )
        for q in (0.1, 0.2, 0.3, 0.4)
    }
    assert [batches[q].population_perturbation.realized_count for q in batches] == [2, 4, 6, 8]
    assert [batches[q].population_perturbation.realized_fraction for q in batches] == [0.1, 0.2, 0.3, 0.4]
    assert len({batches[q].population_perturbation.selected_indices for q in batches}) == 4


def test_r2_batch_selection_is_seed_deterministic_and_records_global_provenance():
    inputs = _episode_batch()
    first = run_development_condition_batch(inputs, "B", perturbation_family="R2", severity=0.3, perturbation_seed=7)
    repeated = run_development_condition_batch(inputs, "B", perturbation_family="R2", severity=0.3, perturbation_seed=7)
    different = run_development_condition_batch(inputs, "B", perturbation_family="R2", severity=0.3, perturbation_seed=8)
    assert first == repeated
    assert first.population_perturbation.selected_indices != different.population_perturbation.selected_indices
    perturbation = first.population_perturbation
    assert perturbation.seed == 7
    assert perturbation.selection_rule == "ordered_population_numpy_default_rng_permutation_nearest_integer_half_up"
    assert perturbation.observation_ids == tuple(
        f"anon-s{index:03d}::dev-{index:03d}::observation-0000" for index in range(20)
    )
    assert perturbation.selected_observation_ids == tuple(
        perturbation.observation_ids[index] for index in perturbation.selected_indices
    )
    assert len(perturbation.original_evidence) == len(perturbation.perturbed_evidence) == 20


@pytest.mark.parametrize("condition_id", ["C", "D"])
def test_r2_c_and_d_multi_observation_episodes_share_global_selection_contract(condition_id):
    batch = run_development_condition_batch(
        _episode_batch(4, observations=5),
        condition_id,
        perturbation_family="R2",
        severity=0.3,
        perturbation_seed=23,
    )
    perturbation = batch.population_perturbation
    assert perturbation.population_size == 20
    assert perturbation.realized_count == 6
    assert tuple(assignment.global_indices for assignment in batch.episode_assignments) == (
        (0, 1, 2, 3, 4),
        (5, 6, 7, 8, 9),
        (10, 11, 12, 13, 14),
        (15, 16, 17, 18, 19),
    )
    selected = set(perturbation.selected_indices)
    for assignment in batch.episode_assignments:
        assert assignment.selected_global_indices == tuple(index for index in assignment.global_indices if index in selected)
        for global_index, original, perturbed in zip(
            assignment.global_indices, assignment.original_evidence, assignment.perturbed_evidence
        ):
            assert perturbed == (original[1], original[0]) if global_index in selected else perturbed == original


def test_r2_c_and_d_same_ordered_population_and_seed_select_same_global_observations():
    inputs = _episode_batch(4, observations=5)
    result_c = run_development_condition_batch(
        inputs, "C", perturbation_family="R2", severity=0.2, perturbation_seed=51
    )
    result_d = run_development_condition_batch(
        inputs, "D", perturbation_family="R2", severity=0.2, perturbation_seed=51
    )
    assert result_c.population_perturbation.selected_indices == result_d.population_perturbation.selected_indices
    assert (
        result_c.population_perturbation.selected_observation_ids
        == result_d.population_perturbation.selected_observation_ids
    )


def test_batch_r1_remains_episode_local_and_unchanged():
    batch = run_development_condition_batch(_episode_batch(2), "B", perturbation_family="R1", severity=1.0)
    assert batch.population_perturbation is None
    assert batch.episode_assignments == ()
    assert all(result.posterior == (0.5, 0.5) for result in batch.episode_results)
    assert all(result.perturbation.original_evidence == ((0.7, 0.3),) for result in batch.episode_results)


def test_r2_batch_refuses_protected_final_test_inputs_before_population_selection():
    with pytest.raises(ExperimentError, match="refuses protected"):
        run_development_condition_batch(
            _episode_batch(split="final_test"),
            "A",
            perturbation_family="R2",
            severity=0.1,
            perturbation_seed=42,
        )


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
