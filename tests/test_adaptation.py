from __future__ import annotations

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.cognitive import adaptation, bayes


def observation(
    action: adaptation.FeedbackAction,
    approved_goal_id: str | None = None,
    *,
    subject_id: str = "subject-001",
    candidate_a_id: str = "goal-a",
    candidate_b_id: str = "goal-b",
    source_id: str = "feedback-1",
    between_episodes: bool = True,
) -> adaptation.ExplicitFeedbackObservation:
    return adaptation.ExplicitFeedbackObservation(
        subject_id=subject_id,
        candidate_a_id=candidate_a_id,
        candidate_b_id=candidate_b_id,
        action=action,
        source_observation_id=source_id,
        approved_goal_id=approved_goal_id,
        between_episodes=between_episodes,
    )


def add_a_feedback(personalizer: adaptation.PriorPersonalizer, count: int) -> None:
    for index in range(count):
        personalizer.record_explicit_feedback(
            observation(adaptation.FeedbackAction.CONFIRM, "goal-a", source_id=f"confirm-{index}")
        )


def test_new_state_is_symmetric_and_has_uniform_prior() -> None:
    personalizer = adaptation.PriorPersonalizer()
    state = personalizer.state_for("subject-001", "goal-a", "goal-b")

    assert state.alpha_by_candidate == (1, 1)
    assert state.update_count == 0
    assert personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-b") == (0.5, 0.5)


def test_adaptation_off_always_returns_uniform_prior_despite_history() -> None:
    personalizer = adaptation.PriorPersonalizer(adaptation_enabled=False)
    add_a_feedback(personalizer, 4)

    assert personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-b") == (0.5, 0.5)


def test_warm_up_keeps_uniform_prior_until_third_valid_event() -> None:
    personalizer = adaptation.PriorPersonalizer()
    add_a_feedback(personalizer, 1)
    assert personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-b") == (0.5, 0.5)
    add_a_feedback(personalizer, 1)
    assert personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-b") == (0.5, 0.5)
    add_a_feedback(personalizer, 1)
    assert personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-b") == pytest.approx((0.75, 0.25))


def test_a_and_b_feedback_increment_only_the_approved_candidate_count() -> None:
    personalizer = adaptation.PriorPersonalizer()
    personalizer.record_explicit_feedback(observation(adaptation.FeedbackAction.CONFIRM, "goal-a"))
    personalizer.record_explicit_feedback(observation(adaptation.FeedbackAction.OVERRIDE, "goal-b", source_id="override-1"))
    state = personalizer.state_for("subject-001", "goal-a", "goal-b")

    assert state.alpha_for("goal-a") == 2
    assert state.alpha_for("goal-b") == 2
    assert state.update_count == 2


def test_personalized_formula_and_bounds_preserve_normalization() -> None:
    personalizer = adaptation.PriorPersonalizer()
    add_a_feedback(personalizer, 10)
    prior = personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-b")

    assert prior == pytest.approx((0.75, 0.25))
    assert sum(prior) == pytest.approx(1.0)


def test_raw_formula_is_used_when_the_personalized_prior_is_inside_bounds() -> None:
    personalizer = adaptation.PriorPersonalizer()
    add_a_feedback(personalizer, 2)
    personalizer.record_explicit_feedback(
        observation(adaptation.FeedbackAction.OVERRIDE, "goal-b", source_id="override-raw-formula")
    )

    assert personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-b") == pytest.approx((0.6, 0.4))


def test_reset_restores_initial_state_and_uniform_prior() -> None:
    personalizer = adaptation.PriorPersonalizer()
    add_a_feedback(personalizer, 3)
    state = personalizer.reset("subject-001", "goal-a", "goal-b")

    assert state.alpha_by_candidate == (1, 1)
    assert state.update_count == 0
    assert personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-b") == (0.5, 0.5)


def test_subjects_and_candidate_pairs_are_isolated_and_order_independent() -> None:
    personalizer = adaptation.PriorPersonalizer()
    add_a_feedback(personalizer, 3)

    assert personalizer.initial_prior_for_new_episode("subject-002", "goal-a", "goal-b") == (0.5, 0.5)
    assert personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-c") == (0.5, 0.5)
    assert personalizer.initial_prior_for_new_episode("subject-001", "goal-b", "goal-a") == pytest.approx((0.25, 0.75))


def test_trace_record_preserves_explicit_feedback_provenance() -> None:
    personalizer = adaptation.PriorPersonalizer()
    record = personalizer.record_explicit_feedback(
        observation(adaptation.FeedbackAction.OVERRIDE, "goal-b", source_id="operator-correction-42")
    )

    assert record is not None
    assert record.source_observation_id == "operator-correction-42"
    assert record.action is adaptation.FeedbackAction.OVERRIDE
    assert record.approved_goal_id == "goal-b"


@pytest.mark.parametrize(
    "action",
    (adaptation.FeedbackAction.PAUSE, adaptation.FeedbackAction.STOP, adaptation.FeedbackAction.DEFER, adaptation.FeedbackAction.PROCEED),
)
def test_nonexplicit_or_unresolved_actions_do_not_update_adaptation(action: adaptation.FeedbackAction) -> None:
    personalizer = adaptation.PriorPersonalizer()

    assert personalizer.record_explicit_feedback(observation(action)) is None
    assert personalizer.state_for("subject-001", "goal-a", "goal-b").update_count == 0


def test_rejects_active_episode_and_data_not_in_feedback_contract() -> None:
    personalizer = adaptation.PriorPersonalizer()
    with pytest.raises(adaptation.AdaptationError, match="active Bayesian"):
        personalizer.record_explicit_feedback(
            observation(adaptation.FeedbackAction.CONFIRM, "goal-a", between_episodes=False)
        )
    with pytest.raises(TypeError):
        personalizer.record_explicit_feedback(  # type: ignore[call-arg]
            observation(adaptation.FeedbackAction.CONFIRM, "goal-a"),
            hidden_test_truth="goal-a",
        )
    with pytest.raises(TypeError):
        personalizer.record_explicit_feedback(  # type: ignore[call-arg]
            observation(adaptation.FeedbackAction.CONFIRM, "goal-a"),
            planner_cost=1.0,
            safety_state="safe",
        )


def test_personalized_prior_initializes_only_a_fresh_bayesian_episode() -> None:
    personalizer = adaptation.PriorPersonalizer()
    add_a_feedback(personalizer, 3)
    with pytest.raises(adaptation.AdaptationError, match="before a new Bayesian episode"):
        personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-b", episode_is_active=True)

    personalized_prior = personalizer.initial_prior_for_new_episode("subject-001", "goal-a", "goal-b")
    episode = bayes.BinaryBayesianGoalEpisode(
        candidate_a="goal-a",
        candidate_b="goal-b",
        initial_prior=personalized_prior,
    )
    assert episode.posterior == pytest.approx((0.75, 0.25))
    result = episode.accept_evidence(bayes.binary_goal_evidence_from_calibrated_probabilities([0.8, 0.2]))
    assert result.posterior == pytest.approx((0.9230769230769231, 0.07692307692307693))
