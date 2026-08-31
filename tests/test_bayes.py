from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.cognitive import bayes


def evidence(left: float, right: float) -> bayes.BinaryGoalEvidence:
    return bayes.binary_goal_evidence_from_calibrated_probabilities([left, right])


def episode() -> bayes.BinaryBayesianGoalEpisode:
    return bayes.BinaryBayesianGoalEpisode(candidate_a="victim_a", candidate_b="victim_b")


def test_episode_starts_with_the_exact_approved_uniform_prior() -> None:
    state = episode()

    assert state.posterior == (0.5, 0.5)
    assert state.update_count == 0
    assert state.status is bayes.EpisodeStatus.PENDING


def test_one_step_bayesian_update_uses_prior_times_likelihood_then_normalizes() -> None:
    result = episode().accept_evidence(evidence(0.8, 0.2))

    np.testing.assert_allclose(result.posterior, (0.8, 0.2), atol=1e-12)
    assert result.update_count == 1
    assert result.status is bayes.EpisodeStatus.PENDING


def test_repeated_updates_use_the_previous_posterior_as_the_next_prior() -> None:
    state = episode()
    state.accept_evidence(evidence(0.6, 0.4))
    result = state.accept_evidence(evidence(0.75, 0.25))

    np.testing.assert_allclose(result.posterior, (0.8181818181818182, 0.18181818181818182), atol=1e-12)
    assert len(state.history) == 2


def test_each_posterior_is_normalized_and_finite() -> None:
    result = episode().accept_evidence(evidence(0.55, 0.45))

    assert np.isfinite(result.posterior).all()
    assert sum(result.posterior) == pytest.approx(1.0)


@pytest.mark.parametrize("values", ([np.nan, 1.0], [np.inf, 0.0], [-0.1, 1.1], [0.0, 0.0]))
def test_malformed_nonfinite_negative_or_zero_mass_evidence_is_rejected(values: list[float]) -> None:
    with pytest.raises(bayes.BayesianGoalInferenceError):
        bayes.binary_goal_evidence_from_calibrated_probabilities(values)


@pytest.mark.parametrize("values", ([1.0], [0.2, 0.3, 0.5], [[0.5, 0.5]]))
def test_non_binary_or_k_goal_evidence_is_rejected(values: object) -> None:
    with pytest.raises(bayes.BayesianGoalInferenceError):
        bayes.binary_goal_evidence_from_calibrated_probabilities(values)  # type: ignore[arg-type]


def test_calibrated_left_maps_to_candidate_a_and_right_maps_to_candidate_b() -> None:
    left_support = evidence(0.8, 0.2)
    right_support = evidence(0.2, 0.8)

    assert left_support.likelihoods == (0.8, 0.2)
    assert right_support.likelihoods == (0.2, 0.8)
    assert episode().accept_evidence(left_support).posterior[0] > 0.5
    assert episode().accept_evidence(right_support).posterior[1] > 0.5


def test_noncanonical_or_reversed_class_order_is_rejected() -> None:
    with pytest.raises(bayes.BayesianGoalInferenceError, match="class order"):
        bayes.binary_goal_evidence_from_calibrated_probabilities([0.5, 0.5], class_labels=("right", "left"))


def test_exact_commitment_boundary_commits_candidate_a() -> None:
    result = episode().accept_evidence(evidence(0.90, 0.10))

    assert result.posterior[0] == pytest.approx(0.90)
    assert result.status is bayes.EpisodeStatus.COMMITTED
    assert result.committed_candidate == "victim_a"


def test_earliest_valid_commitment_is_terminal() -> None:
    state = episode()
    result = state.accept_evidence(evidence(0.95, 0.05))

    assert result.update_count == 1
    assert result.status is bayes.EpisodeStatus.COMMITTED
    with pytest.raises(bayes.BayesianGoalInferenceError, match="Start a new episode"):
        state.accept_evidence(evidence(0.5, 0.5))


def test_five_update_maximum_defers_without_forcing_the_posterior_argmax() -> None:
    state = episode()
    for update_number in range(1, 6):
        result = state.accept_evidence(evidence(0.55, 0.45))
        if update_number < 5:
            assert result.status is bayes.EpisodeStatus.PENDING
            assert result.committed_candidate is None

    assert result.update_count == 5
    assert result.posterior[0] > result.posterior[1]
    assert result.status is bayes.EpisodeStatus.DEFER
    assert result.committed_candidate is None
    with pytest.raises(bayes.BayesianGoalInferenceError, match="Start a new episode"):
        state.accept_evidence(evidence(0.5, 0.5))


def test_new_episode_resets_prior_history_count_and_terminal_status() -> None:
    state = episode()
    state.accept_evidence(evidence(0.95, 0.05))

    result = state.start_new_episode()

    assert result.posterior == (0.5, 0.5)
    assert result.update_count == 0
    assert result.status is bayes.EpisodeStatus.PENDING
    assert result.committed_candidate is None
    assert state.history == ()


def test_planner_and_safety_information_cannot_be_passed_to_likelihood_adapter() -> None:
    with pytest.raises(TypeError):
        bayes.binary_goal_evidence_from_calibrated_probabilities(
            [0.5, 0.5],
            planner_cost=1.0,  # type: ignore[call-arg]
        )
