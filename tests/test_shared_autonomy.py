from __future__ import annotations

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.cognitive import bayes, uncertainty
from src.control import shared_autonomy


def result(
    posterior: tuple[float, float],
    update_count: int,
    status: bayes.EpisodeStatus,
) -> bayes.BayesianEpisodeResult:
    return bayes.BayesianEpisodeResult(
        candidate_names=("candidate_a", "candidate_b"),
        posterior=posterior,
        update_count=update_count,
        status=status,
        committed_candidate=None,
    )


def decide(
    posterior: tuple[float, float],
    update_count: int,
    status: bayes.EpisodeStatus,
    *,
    human_action: shared_autonomy.HumanAction = shared_autonomy.HumanAction.NONE,
) -> shared_autonomy.SharedAutonomyDecision:
    episode_result = result(posterior, update_count, status)
    return shared_autonomy.decide_shared_autonomy(
        episode_result,
        uncertainty.estimate_binary_uncertainty(posterior),
        human_action=human_action,
    )


def test_early_commitment_threshold_outputs_proceed() -> None:
    decision = decide((0.9, 0.1), 1, bayes.EpisodeStatus.COMMITTED)

    assert decision.mode is shared_autonomy.AutonomyMode.PROCEED
    assert decision.candidate_goal == "candidate_a"
    assert decision.approved_goal == "candidate_a"


def test_pre_horizon_below_proceed_threshold_remains_waiting() -> None:
    decision = decide((0.8, 0.2), 4, bayes.EpisodeStatus.PENDING)

    assert decision.mode is shared_autonomy.AutonomyMode.WAITING
    assert decision.candidate_goal is None
    assert decision.approved_goal is None
    assert not decision.requires_human_confirmation


def test_update_five_at_confirm_boundary_requires_explicit_human_confirmation() -> None:
    decision = decide((0.75, 0.25), 5, bayes.EpisodeStatus.DEFER)

    assert decision.mode is shared_autonomy.AutonomyMode.CONFIRM
    assert decision.candidate_goal == "candidate_a"
    assert decision.approved_goal is None
    assert decision.requires_human_confirmation


def test_update_five_just_below_confirm_boundary_defers_without_forced_approval() -> None:
    decision = decide((0.749999, 0.250001), 5, bayes.EpisodeStatus.DEFER)

    assert decision.mode is shared_autonomy.AutonomyMode.DEFER
    assert decision.candidate_goal is None
    assert decision.approved_goal is None
    assert decision.holds_position
    assert decision.requests_human_input


def test_defer_remains_deferred_without_human_input() -> None:
    first = decide((0.6, 0.4), 5, bayes.EpisodeStatus.DEFER)
    repeated = decide((0.6, 0.4), 5, bayes.EpisodeStatus.DEFER)

    assert first.mode is shared_autonomy.AutonomyMode.DEFER
    assert repeated.mode is shared_autonomy.AutonomyMode.DEFER
    assert repeated.approved_goal is None


def test_update_five_just_below_proceed_threshold_confirms() -> None:
    decision = decide((0.899999, 0.100001), 5, bayes.EpisodeStatus.DEFER)

    assert decision.mode is shared_autonomy.AutonomyMode.CONFIRM
    assert decision.candidate_goal == "candidate_a"
    assert decision.approved_goal is None


def test_update_five_at_proceed_boundary_outputs_proceed() -> None:
    decision = decide((0.9, 0.1), 5, bayes.EpisodeStatus.COMMITTED)

    assert decision.mode is shared_autonomy.AutonomyMode.PROCEED
    assert decision.approved_goal == "candidate_a"


@pytest.mark.parametrize(
    ("human_action", "expected_mode"),
    (
        (shared_autonomy.HumanAction.STOP, shared_autonomy.AutonomyMode.STOP),
        (shared_autonomy.HumanAction.PAUSE, shared_autonomy.AutonomyMode.PAUSE),
    ),
)
def test_stop_and_pause_override_normal_posterior_policy(
    human_action: shared_autonomy.HumanAction,
    expected_mode: shared_autonomy.AutonomyMode,
) -> None:
    decision = decide((0.99, 0.01), 1, bayes.EpisodeStatus.COMMITTED, human_action=human_action)

    assert decision.mode is expected_mode
    assert decision.human_action is human_action
    assert decision.approved_goal is None
    assert decision.holds_position


def test_override_takes_precedence_without_becoming_bayesian_evidence_or_adaptation_data() -> None:
    decision = decide(
        (0.99, 0.01),
        1,
        bayes.EpisodeStatus.COMMITTED,
        human_action=shared_autonomy.HumanAction.OVERRIDE,
    )

    assert decision.mode is shared_autonomy.AutonomyMode.WAITING
    assert decision.human_action is shared_autonomy.HumanAction.OVERRIDE
    assert decision.candidate_goal is None
    assert decision.approved_goal is None
    assert "reset transitions are outside" in decision.reason


def test_entropy_is_a_validated_measurement_not_an_independent_action_rule() -> None:
    episode_result = result((0.9, 0.1), 1, bayes.EpisodeStatus.COMMITTED)
    decision = shared_autonomy.decide_shared_autonomy(
        episode_result,
        uncertainty.estimate_binary_uncertainty((0.9, 0.1)),
    )

    assert decision.mode is shared_autonomy.AutonomyMode.PROCEED
    assert decision.entropy_bits == pytest.approx(0.4689955936, abs=1e-10)
    with pytest.raises(uncertainty.UncertaintyError):
        shared_autonomy.decide_shared_autonomy(
            episode_result,
            uncertainty.BinaryUncertainty(posterior=(0.9, 0.1), entropy_bits=1.0),
        )


def test_policy_api_has_no_planner_safety_or_execution_dependency() -> None:
    episode_result = result((0.5, 0.5), 1, bayes.EpisodeStatus.PENDING)
    with pytest.raises(TypeError):
        shared_autonomy.decide_shared_autonomy(
            episode_result,
            uncertainty.estimate_binary_uncertainty((0.5, 0.5)),
            planner_cost=1.0,  # type: ignore[call-arg]
        )
