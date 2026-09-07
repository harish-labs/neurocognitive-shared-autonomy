import numpy as np
import pytest

from src.cognitive.bayes import EpisodeStatus
from src.cognitive.replay_episode import (
    ReplayEpisodeIntegrationError,
    run_bayesian_replay_episode,
)
from src.models.runtime_adapter import DecodedReplayObservation


def observation(
    replay_index: int,
    probabilities: tuple[float, float] = (0.5, 0.5),
    *,
    identity: tuple[int, int, str, int, str] | None = None,
    class_labels: tuple[str, str] = ("left", "right"),
    values: object | None = None,
) -> DecodedReplayObservation:
    return DecodedReplayObservation(
        replay_index=replay_index,
        canonical_trial_identity=identity or (1, 1, "sample.fif", replay_index, "left"),
        subject_id=1,
        run_id=1,
        trial_index=replay_index,
        source_file="sample.fif",
        event_code="left",
        semantic_label="left",
        event_sample=replay_index,
        model_family="csp_lda",
        class_labels=class_labels,
        raw_decoder_output=np.asarray([[0.5, 0.5]]),
        calibrated_probabilities=np.asarray(values if values is not None else [probabilities]),
    )


def test_one_update_preserves_prior_mapping_and_provenance() -> None:
    result = run_bayesian_replay_episode([observation(0, (0.8, 0.2))], candidate_a="A", candidate_b="B")
    assert result.initial_prior == (0.5, 0.5)
    assert result.status is EpisodeStatus.PENDING
    assert result.update_count == 1
    assert result.evidence_updates[0].replay_index == 0
    assert result.evidence_updates[0].calibrated_probabilities == (0.8, 0.2)
    assert result.evidence_updates[0].canonical_trial_identity == (1, 1, "sample.fif", 0, "left")


def test_candidate_a_and_b_commit_with_left_right_mapping() -> None:
    assert run_bayesian_replay_episode([observation(0, (1.0, 0.0))], candidate_a="A", candidate_b="B").committed_candidate == "A"
    assert run_bayesian_replay_episode([observation(0, (0.0, 1.0))], candidate_a="A", candidate_b="B").committed_candidate == "B"


def test_stops_at_commit_without_consuming_later_observation() -> None:
    consumed: list[int] = []

    def stream():
        for index, probabilities in enumerate(((1.0, 0.0), (0.5, 0.5))):
            consumed.append(index)
            yield observation(index, probabilities)

    result = run_bayesian_replay_episode(stream(), candidate_a="A", candidate_b="B")
    assert result.status is EpisodeStatus.COMMITTED
    assert consumed == [0]


def test_five_unresolved_updates_defer_without_forced_argmax() -> None:
    result = run_bayesian_replay_episode(
        [observation(index, (0.5, 0.5)) for index in range(5)], candidate_a="A", candidate_b="B"
    )
    assert result.status is EpisodeStatus.DEFER
    assert result.update_count == 5
    assert result.committed_candidate is None


@pytest.mark.parametrize("indices", [(1, 1), (2, 1)])
def test_rejects_duplicate_or_decreasing_replay_index(indices: tuple[int, int]) -> None:
    with pytest.raises(ReplayEpisodeIntegrationError):
        run_bayesian_replay_episode([observation(indices[0]), observation(indices[1])], candidate_a="A", candidate_b="B")


def test_rejects_duplicate_identity_and_invalid_inputs() -> None:
    duplicate_identity = (1, 1, "sample.fif", 99, "left")
    with pytest.raises(ReplayEpisodeIntegrationError):
        run_bayesian_replay_episode(
            [observation(0, identity=duplicate_identity), observation(1, identity=duplicate_identity)],
            candidate_a="A",
            candidate_b="B",
        )
    with pytest.raises(ReplayEpisodeIntegrationError):
        run_bayesian_replay_episode([], candidate_a="A", candidate_b="B")
    with pytest.raises(ReplayEpisodeIntegrationError):
        run_bayesian_replay_episode([observation(0, class_labels=("right", "left"))], candidate_a="A", candidate_b="B")
    with pytest.raises(ReplayEpisodeIntegrationError):
        run_bayesian_replay_episode([observation(0, values=[[0.4, 0.4]])], candidate_a="A", candidate_b="B")


@pytest.mark.parametrize("candidate_a,candidate_b", [("", "B"), ("A", ""), ("A", "A")])
def test_rejects_invalid_candidates(candidate_a: str, candidate_b: str) -> None:
    with pytest.raises(ReplayEpisodeIntegrationError):
        run_bayesian_replay_episode([observation(0)], candidate_a=candidate_a, candidate_b=candidate_b)
