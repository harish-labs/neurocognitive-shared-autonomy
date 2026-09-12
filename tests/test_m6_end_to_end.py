from __future__ import annotations

from pathlib import Path

import mne
import numpy as np
import pandas as pd
import pytest

from src.autonomy.environment import EnvironmentConfig, SearchRescueEnvironment
from src.cognitive.replay_episode import BayesianReplayEpisodeResult
from src.control.human_interaction import CommandStatus, HumanCommand, HumanCommandType
from src.control.navigation_runtime import NavigationReplanTrigger, NavigationStatus
from src.control.offline_mission import MissionStage, OfflineMission
from src.eeg.replay import OfflineEpochReplay
from src.models.calibration import PlattScalingCalibrator
from src.models.csp_lda import CspLdaDecoder


class RecordingCspDecoder(CspLdaDecoder):
    def __init__(self, outputs: list[tuple[float, float]]) -> None:
        self.class_labels = ("left", "right")
        self._outputs = iter(outputs)
        self.calls = 0

    def predict_proba(self, single_epoch: mne.BaseEpochs) -> np.ndarray:
        self.calls += 1
        return np.asarray([next(self._outputs)])


class IdentityPlattCalibrator(PlattScalingCalibrator):
    def __init__(self) -> None:
        super().__init__(slope=1.0, intercept=0.0)

    def predict_proba(self, probabilities: np.ndarray) -> np.ndarray:
        return probabilities


def environment(*, blocked: frozenset[tuple[int, int]] = frozenset()) -> SearchRescueEnvironment:
    return SearchRescueEnvironment(
        EnvironmentConfig(
            rows=3,
            columns=5,
            start=(1, 0),
            goals={"victim_a": (1, 4), "victim_b": (0, 2)},
            blocked_cells=blocked,
        )
    )


def canonical_epochs(count: int) -> mne.EpochsArray:
    metadata = []
    events = []
    samples = np.arange(count * 64 * 801, dtype=float).reshape(count, 64, 801)
    for index in range(count):
        code, label, event_id = ("T1", "left", 2) if index % 2 == 0 else ("T2", "right", 3)
        metadata.append(
            {
                "trial_index": index,
                "subject_id": 1,
                "run_id": 4,
                "source_file": "canonical.edf",
                "event_code": code,
                "semantic_label": label,
                "event_sample": 100 + index,
            }
        )
        events.append([100 + index, 0, event_id])
    return mne.EpochsArray(
        samples,
        mne.create_info([f"EEG {index:03d}" for index in range(64)], 160.0, "eeg"),
        events=np.asarray(events),
        event_id={"left": 2, "right": 3} if count > 1 else {"left": 2},
        tmin=-1.0,
        metadata=pd.DataFrame(metadata),
        verbose="ERROR",
    )


def begin(
    mission: OfflineMission,
    probabilities: list[tuple[float, float]],
    **kwargs: object,
) -> tuple[object, RecordingCspDecoder]:
    decoder = RecordingCspDecoder(probabilities)
    result = mission.begin_from_epochs(
        canonical_epochs(len(probabilities)),
        decoder,
        IdentityPlattCalibrator(),
        candidate_a="victim_a",
        candidate_b="victim_b",
        **kwargs,
    )
    return result, decoder


def test_proceed_path_preserves_canonical_replay_evidence_and_zero_movement_plan() -> None:
    mission = OfflineMission(environment())
    result, decoder = begin(mission, [(1.0, 0.0), (0.5, 0.5)], execution_id="proceed-1")

    assert result.stage is MissionStage.EPISODE
    assert result.replay_episode is not None
    assert result.replay_episode.candidate_names == ("victim_a", "victim_b")
    assert result.replay_episode.initial_prior == (0.5, 0.5)
    assert result.replay_episode.update_count == 1
    assert result.replay_episode.committed_candidate == "victim_a"
    update = result.replay_episode.evidence_updates[0]
    assert update.replay_index == 0
    assert update.canonical_trial_identity == (1, 4, "canonical.edf", 100, "T1")
    assert update.class_labels == ("left", "right")
    assert update.calibrated_probabilities == (1.0, 0.0)
    assert decoder.calls == 1
    assert result.navigation is not None and result.navigation.status is NavigationStatus.READY
    assert result.navigation.symbolic_goal == "victim_a"
    assert not result.moved and mission.environment.state.position == (1, 0)


def test_replay_is_deterministic_and_never_uses_hidden_semantic_label_for_goal() -> None:
    def run() -> tuple[BayesianReplayEpisodeResult, object]:
        mission = OfflineMission(environment())
        result, _ = begin(mission, [(0.0, 1.0)], execution_id="right-1")
        assert result.replay_episode is not None
        return result.replay_episode, result.navigation

    first_episode, first_navigation = run()
    second_episode, second_navigation = run()

    assert first_episode == second_episode
    assert first_navigation == second_navigation
    assert first_episode.committed_candidate == "victim_b"
    assert first_episode.evidence_updates[0].canonical_trial_identity[-1] == "T1"


def test_commitment_and_five_update_horizon_never_consume_an_extra_observation() -> None:
    committed, committed_decoder = begin(OfflineMission(environment()), [(1.0, 0.0), (0.5, 0.5)], execution_id="commit")
    deferred, deferred_decoder = begin(OfflineMission(environment()), [(0.5, 0.5)] * 6)

    assert committed.replay_episode is not None and committed.replay_episode.update_count == 1
    assert committed_decoder.calls == 1
    assert deferred.replay_episode is not None and deferred.replay_episode.update_count == 5
    assert deferred.replay_episode.committed_candidate is None
    assert deferred_decoder.calls == 5
    assert deferred.navigation is None


def test_confirm_waits_for_human_command_then_creates_fresh_zero_movement_navigation() -> None:
    mission = OfflineMission(environment())
    waiting, _ = begin(mission, [(0.5, 0.5)] * 4 + [(0.8, 0.2)], confirmation_request_id="confirm-1")

    assert waiting.navigation is None
    assert mission.controller.state.active_confirmation is not None
    assert mission.environment.state.position == (1, 0)
    stale = mission.submit_human_command(HumanCommand("stale", HumanCommandType.CONFIRM, request_id="wrong"))
    accepted = mission.submit_human_command(HumanCommand("confirm", HumanCommandType.CONFIRM, request_id="confirm-1"))
    started = mission.start_navigation_from_command(accepted.command, execution_id="confirmed")

    assert stale.command is not None and stale.command.status is CommandStatus.STALE_REQUEST
    assert accepted.command is not None and accepted.command.status is CommandStatus.APPLIED
    assert started.navigation is not None and started.navigation.status is NavigationStatus.READY
    assert not started.moved and mission.environment.state.position == (1, 0)


def test_waiting_and_defer_hold_without_goal_approval_or_movement() -> None:
    waiting, _ = begin(OfflineMission(environment()), [(0.6, 0.4)])
    deferred_mission = OfflineMission(environment())
    deferred, _ = begin(deferred_mission, [(0.5, 0.5)] * 5)

    assert waiting.navigation is None and waiting.replay_episode is not None
    assert waiting.replay_episode.committed_candidate is None
    assert deferred.navigation is None and deferred.replay_episode is not None
    assert deferred.replay_episode.committed_candidate is None
    assert deferred_mission.controller.state.approved_goal is None
    assert deferred_mission.environment.state.position == (1, 0)


def test_override_pause_resume_and_stop_require_fresh_authority_without_queued_motion() -> None:
    mission = OfflineMission(environment())
    ready, _ = begin(mission, [(1.0, 0.0)], execution_id="initial")
    paused = mission.submit_human_command(HumanCommand("pause", HumanCommandType.PAUSE))
    paused_step = mission.advance_one_step()
    resumed = mission.submit_human_command(HumanCommand("resume", HumanCommandType.RESUME))
    resumed_start = mission.start_navigation_from_command(resumed.command, execution_id="resumed")
    override = mission.submit_human_command(HumanCommand("override", HumanCommandType.OVERRIDE, goal="victim_b"))
    stale_step = mission.advance_one_step()
    override_start = mission.start_navigation_from_command(override.command, execution_id="override")
    stopped = mission.submit_human_command(HumanCommand("stop", HumanCommandType.STOP))
    stopped_step = mission.advance_one_step()

    assert ready.navigation is not None and ready.navigation.status is NavigationStatus.READY
    assert paused.command is not None and paused.command.status is CommandStatus.APPLIED
    assert paused_step.navigation is not None and paused_step.navigation.status is NavigationStatus.PAUSED
    assert resumed_start.navigation is not None and resumed_start.navigation.status is NavigationStatus.READY
    assert stale_step.navigation is not None and stale_step.navigation.status is NavigationStatus.STALE_STATE
    assert override_start.navigation is not None and override_start.navigation.symbolic_goal == "victim_b"
    assert stopped.command is not None and stopped_step.navigation is not None
    assert stopped_step.navigation.status is NavigationStatus.STOPPED


def test_each_step_is_safety_gated_and_no_safe_path_stays_stationary(monkeypatch: pytest.MonkeyPatch) -> None:
    mission = OfflineMission(environment())
    ready, _ = begin(mission, [(1.0, 0.0)], execution_id="step")
    calls: list[object] = []
    original_step = mission.environment.step

    def record_step(action: object):
        calls.append(action)
        return original_step(action)

    monkeypatch.setattr(mission.environment, "step", record_step)
    advanced = mission.advance_one_step()
    blocked = OfflineMission(environment(blocked=frozenset({(0, 1), (1, 1), (2, 1)})))
    no_path, _ = begin(blocked, [(1.0, 0.0)], execution_id="no-path")

    assert ready.navigation is not None and ready.navigation.status is NavigationStatus.READY
    assert advanced.navigation is not None and advanced.navigation.moved
    assert len(calls) == 1
    assert no_path.navigation is not None and no_path.navigation.status is NavigationStatus.NO_SAFE_PATH
    assert not no_path.moved and blocked.environment.state.position == (1, 0)


def test_explicit_d070_replan_is_zero_movement_and_event_execution_replay_protected() -> None:
    mission = OfflineMission(environment())
    ready, _ = begin(mission, [(1.0, 0.0)], execution_id="source")
    replacement = environment(blocked=frozenset({(0, 0)}))
    replanned = mission.replan_after_environment_change(
        replacement,
        source_execution_id="source",
        event_id="event-1",
        new_execution_id="replacement",
        trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED,
    )
    duplicate = mission.replan_after_environment_change(
        replacement,
        source_execution_id="source",
        event_id="event-1",
        new_execution_id="replacement-2",
        trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED,
    )

    assert ready.navigation is not None and ready.navigation.symbolic_goal == "victim_a"
    assert replanned.replan is not None and replanned.replan.status is NavigationStatus.READY
    assert replanned.navigation is not None and not replanned.navigation.moved
    assert replanned.navigation.symbolic_goal == "victim_a"
    assert duplicate.replan is not None and duplicate.replan.status is NavigationStatus.ALREADY_CONSUMED


def test_malformed_provenance_invalid_runtime_and_invalid_candidates_fail_closed() -> None:
    mission = OfflineMission(environment())
    malformed = canonical_epochs(1)
    malformed.metadata = None
    malformed_result = mission.begin_from_epochs(
        malformed,
        RecordingCspDecoder([(1.0, 0.0)]),
        IdentityPlattCalibrator(),
        candidate_a="victim_a",
        candidate_b="victim_b",
        execution_id="malformed",
    )
    invalid_runtime = mission.begin_from_epochs(
        canonical_epochs(1), object(), object(), candidate_a="victim_a", candidate_b="victim_b"
    )
    invalid_candidates = mission.begin_from_epochs(
        canonical_epochs(1), RecordingCspDecoder([(1.0, 0.0)]), IdentityPlattCalibrator(),
        candidate_a="victim_a", candidate_b="missing"
    )

    assert malformed_result.stage is MissionStage.REJECTED
    assert invalid_runtime.stage is MissionStage.REJECTED
    assert invalid_candidates.stage is MissionStage.REJECTED
    assert mission.navigation_runtime.session is None and mission.environment.state.position == (1, 0)


def test_offline_mission_has_no_hidden_workers_retries_or_complete_route_execution() -> None:
    source = Path(OfflineMission.__module__.replace(".", "/") + ".py")
    source = Path(__file__).parents[1] / source
    text = source.read_text(encoding="utf-8")

    forbidden = ("threading", "asyncio", "Timer(", "while ", "retry")
    assert not any(token in text for token in forbidden)
    assert "ground_truth" not in text and "intended_goal" not in text
    assert "mne.BaseEpochs" in text and "OfflineEpochReplay" in text


def test_offline_replay_contract_rejects_malformed_epoch_metadata_before_decoder_execution() -> None:
    malformed = canonical_epochs(1)
    malformed.metadata.loc[0, "event_sample"] = -1

    with pytest.raises(ValueError):
        OfflineEpochReplay(malformed)
