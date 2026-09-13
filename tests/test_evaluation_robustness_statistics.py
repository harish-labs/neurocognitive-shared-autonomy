import numpy as np
import pytest

from src.evaluation.robustness import RobustnessError, contaminate_contradictory_evidence, flatten_evidence
from src.evaluation.statistics import (
    BOOTSTRAP_RESAMPLES,
    ObservationMetric,
    StatisticsError,
    SubjectMetric,
    aggregate_subject_means,
    holm_adjust,
    paired_subject_inference,
)


def test_r1_frozen_endpoints_and_intermediate_values():
    evidence = np.asarray([[0.8, 0.2], [0.1, 0.9]])
    assert flatten_evidence(evidence, 0.0).perturbed_evidence == ((0.8, 0.2), (0.1, 0.9))
    assert np.asarray(flatten_evidence(evidence, 0.5).perturbed_evidence) == pytest.approx(np.asarray(((0.65, 0.35), (0.3, 0.7))))
    assert flatten_evidence(evidence, 1.0).perturbed_evidence == ((0.5, 0.5), (0.5, 0.5))
    with pytest.raises(RobustnessError):
        flatten_evidence(evidence, 0.2)


def test_r2_is_seed_reproducible_records_indices_and_swaps_only_selected_rows():
    evidence = np.asarray([[0.9 - i / 100, 0.1 + i / 100] for i in range(10)])
    observation_ids = tuple(f"global-{index}" for index in range(10))
    first = contaminate_contradictory_evidence(evidence, 0.3, seed=42, observation_ids=observation_ids)
    second = contaminate_contradictory_evidence(evidence, 0.3, seed=42, observation_ids=observation_ids)
    different = contaminate_contradictory_evidence(evidence, 0.3, seed=43, observation_ids=observation_ids)
    assert first == second
    assert first.requested_q == 0.3
    assert first.population_size == 10
    assert first.realized_count == 3
    assert first.realized_fraction == 0.3
    assert len(first.selected_indices) == 3
    assert first.selected_observation_ids == tuple(observation_ids[index] for index in first.selected_indices)
    assert first.selected_indices != different.selected_indices
    for index, (original, perturbed) in enumerate(zip(first.original_evidence, first.perturbed_evidence)):
        assert perturbed == (original[1], original[0]) if index in first.selected_indices else perturbed == original


def test_r2_rejects_non_unique_or_misaligned_population_identities():
    evidence = np.asarray([[0.8, 0.2], [0.7, 0.3]])
    with pytest.raises(RobustnessError, match="one-to-one"):
        contaminate_contradictory_evidence(evidence, 0.1, seed=1, observation_ids=("only-one",))
    with pytest.raises(RobustnessError, match="unique"):
        contaminate_contradictory_evidence(evidence, 0.1, seed=1, observation_ids=("same", "same"))


def test_paired_subject_bootstrap_and_exact_sign_flip_are_deterministic():
    a = [SubjectMetric(f"s{i}", float(i), 20) for i in range(1, 5)]
    b = [SubjectMetric(f"s{i}", float(i + 1), 20) for i in range(1, 5)]
    first = paired_subject_inference(a, b, bootstrap_seed=7)
    second = paired_subject_inference(a, b, bootstrap_seed=7)
    assert first == second
    assert first.bootstrap_resamples == BOOTSTRAP_RESAMPLES
    assert first.raw_effect_mean_difference == 1.0
    assert (first.ci_lower, first.ci_upper) == (1.0, 1.0)
    assert first.permutation_method == "exact_paired_sign_flip"
    assert first.permutation_assignments == 16
    assert first.raw_p_value == pytest.approx(0.125)


def test_complete_seventeen_subject_vector_uses_all_exact_sign_assignments():
    a = [SubjectMetric(f"s{i:02d}", 0.0, 5) for i in range(17)]
    b = [SubjectMetric(f"s{i:02d}", float((i % 3) - 1), 5) for i in range(17)]
    result = paired_subject_inference(a, b, bootstrap_seed=42)
    assert result.permutation_method == "exact_paired_sign_flip"
    assert result.permutation_assignments == 131_072
    assert result.permutation_seed is None


def test_larger_subject_vector_requires_and_records_monte_carlo_seed_and_size():
    a = [SubjectMetric(f"s{i:02d}", 0.0, 5) for i in range(18)]
    b = [SubjectMetric(f"s{i:02d}", float(i % 4), 5) for i in range(18)]
    with pytest.raises(StatisticsError, match="permutation_samples"):
        paired_subject_inference(a, b, bootstrap_seed=1)
    result = paired_subject_inference(a, b, bootstrap_seed=1, permutation_seed=9, permutation_samples=1_000)
    assert result.permutation_method == "monte_carlo_paired_sign_flip"
    assert result.permutation_assignments == 1_000
    assert result.permutation_seed == 9


def test_subject_level_api_rejects_duplicate_subject_pseudo_replication():
    duplicated = [SubjectMetric("s1", 0.1, 10), SubjectMetric("s1", 0.2, 10)]
    with pytest.raises(StatisticsError, match="pseudo-replication"):
        paired_subject_inference(duplicated, [SubjectMetric("s1", 0.3, 10)], bootstrap_seed=1)


def test_lower_level_observations_are_aggregated_once_per_subject_before_inference():
    aggregated = aggregate_subject_means(
        [
            ObservationMetric("s2", "o3", 1.0),
            ObservationMetric("s1", "o1", 0.0),
            ObservationMetric("s1", "o2", 1.0),
        ]
    )
    assert aggregated == (SubjectMetric("s1", 0.5, 2), SubjectMetric("s2", 1.0, 1))


def test_holm_adjustment_matches_step_down_definition():
    adjusted = holm_adjust({"a": 0.01, "b": 0.04, "c": 0.03})
    assert adjusted == pytest.approx({"a": 0.03, "b": 0.06, "c": 0.06})
