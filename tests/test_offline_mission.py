from __future__ import annotations

import mne
import numpy as np
import pandas as pd
import pytest

from src.autonomy.environment import EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.safety import SafetyController
from src.control.human_interaction import CommandStatus, HumanCommand, HumanCommandType
from src.control.navigation_runtime import NavigationReplanTrigger, NavigationRuntime, NavigationStatus
from src.control.offline_mission import MissionStage, OfflineMission
from src.models.calibration import PlattScalingCalibrator
from src.models.csp_lda import CspLdaDecoder


class RecordingCspDecoder(CspLdaDecoder):
    def __init__(self, outputs: list[np.ndarray]) -> None:
        self.class_labels = ("left", "right")
        self.outputs = iter(outputs)
        self.calls = 0

    def predict_proba(self, epochs: mne.BaseEpochs) -> np.ndarray:
        self.calls += 1
        return next(self.outputs)


class RecordingPlattCalibrator(PlattScalingCalibrator):
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


def epochs(count: int = 2) -> mne.EpochsArray:
    rows = []
    events = []
    for index in range(count):
        code, label, event_id = ("T1", "left", 2) if index % 2 == 0 else ("T2", "right", 3)
        rows.append(
            {
                "trial_index": index,
                "subject_id": 1,
                "run_id": 4,
                "source_file": "source.edf",
                "event_code": code,
                "semantic_label": label,
                "event_sample": 100 + index,
            }
        )
        events.append([100 + index, 0, event_id])
    return mne.EpochsArray(
        np.arange(count * 64 * 801, dtype=float).reshape(count, 64, 801),
        mne.create_info([f"EEG {index:03d}" for index in range(64)], 160.0, "eeg"),
        events=np.asarray(events),
        event_id={"left": 2, "right": 3} if count > 1 else {"left": 2},
        tmin=-1.0,
        metadata=pd.DataFrame(rows),
        verbose="ERROR",
    )


def begin(mission: OfflineMission, values: list[tuple[float, float]], **kwargs: object):
    decoder = RecordingCspDecoder([np.asarray([value]) for value in values])
    result = mission.begin_from_epochs(
        epochs(len(values)),
        decoder,
        RecordingPlattCalibrator(),
        candidate_a="victim_a",
        candidate_b="victim_b",
        **kwargs,
    )
    return result, decoder


def test_replay_decoder_bayes_and_t04_reach_zero_movement_ready_lazily() -> None:
    mission = OfflineMission(environment())
    result, decoder = begin(mission, [(1.0, 0.0), (0.5, 0.5)], execution_id="execution-1")

    assert result.stage is MissionStage.EPISODE
    assert result.navigation is not None and result.navigation.status is NavigationStatus.READY
    assert not result.moved and mission.environment.state.position == (1, 0)
    assert result.replay_episode is not None and result.replay_episode.update_count == 1
    assert decoder.calls == 1


def test_waiting_defer_and_confirm_hold_until_explicit_command() -> None:
    waiting, _ = begin(OfflineMission(environment()), [(0.6, 0.4)])
    deferred, _ = begin(OfflineMission(environment()), [(0.5, 0.5)] * 5)
    mission = OfflineMission(environment())
    confirm, _ = begin(mission, [(0.5, 0.5)] * 4 + [(0.8, 0.2)], confirmation_request_id="request-1")

    assert waiting.navigation is deferred.navigation is confirm.navigation is None
    assert mission.controller.state.active_confirmation is not None
    command = mission.submit_human_command(HumanCommand("confirm", HumanCommandType.CONFIRM, request_id="request-1"))
    started = mission.start_navigation_from_command(command.command, execution_id="confirmed")

    assert started.navigation is not None and started.navigation.status is NavigationStatus.READY
    assert mission.environment.state.position == (1, 0)


def test_override_pause_resume_stop_and_one_step_boundary() -> None:
    mission = OfflineMission(environment())
    ready, _ = begin(mission, [(1.0, 0.0)], execution_id="initial")
    paused = mission.submit_human_command(HumanCommand("pause", HumanCommandType.PAUSE))
    paused_step = mission.advance_one_step()
    resumed = mission.submit_human_command(HumanCommand("resume", HumanCommandType.RESUME))
    resumed_start = mission.start_navigation_from_command(resumed.command, execution_id="resumed")
    stepped = mission.advance_one_step()
    override = mission.submit_human_command(HumanCommand("override", HumanCommandType.OVERRIDE, goal="victim_b"))
    stale_step = mission.advance_one_step()
    override_start = mission.start_navigation_from_command(override.command, execution_id="override")
    stopped = mission.submit_human_command(HumanCommand("stop", HumanCommandType.STOP))
    stopped_step = mission.advance_one_step()

    assert ready.navigation is not None and ready.navigation.status is NavigationStatus.READY
    assert paused_step.navigation is not None and paused_step.navigation.status is NavigationStatus.PAUSED
    assert resumed_start.navigation is not None and resumed_start.navigation.status is NavigationStatus.READY
    assert stepped.navigation is not None and stepped.navigation.moved
    assert stale_step.navigation is not None and stale_step.navigation.status is NavigationStatus.STALE_STATE
    assert override_start.navigation is not None and override_start.navigation.symbolic_goal == "victim_b"
    assert stopped.command is not None and stopped_step.navigation is not None
    assert stopped_step.navigation.status is NavigationStatus.STOPPED


def test_no_safe_path_replan_and_invalid_inputs_fail_closed() -> None:
    blocked = frozenset({(0, 1), (1, 1), (2, 1)})
    mission = OfflineMission(environment(blocked=blocked))
    no_path, _ = begin(mission, [(1.0, 0.0)], execution_id="no-path")
    duplicate = mission.start_navigation_from_command(mission.submit_human_command(HumanCommand("pause", HumanCommandType.PAUSE)).command, execution_id="no-path")
    invalid = mission.begin_from_epochs(epochs(1), object(), object(), candidate_a="victim_a", candidate_b="missing")

    assert no_path.navigation is not None and no_path.navigation.status is NavigationStatus.NO_SAFE_PATH
    assert not no_path.moved and mission.environment.state.position == (1, 0)
    assert duplicate.navigation is not None and duplicate.navigation.status is NavigationStatus.ALREADY_CONSUMED
    assert invalid.stage is MissionStage.REJECTED


def test_explicit_d070_replan_is_delegated_without_automatic_retry() -> None:
    source = environment()
    mission = OfflineMission(source)
    ready, _ = begin(mission, [(1.0, 0.0)], execution_id="source")
    replacement = environment()
    replacement_config = EnvironmentConfig(
        rows=3,
        columns=5,
        start=(1, 0),
        goals={"victim_a": (1, 4), "victim_b": (0, 2)},
        blocked_cells=frozenset({(0, 0)}),
    )
    replacement = SearchRescueEnvironment(replacement_config)
    replanned = mission.replan_after_environment_change(
        replacement,
        source_execution_id="source",
        event_id="event-1",
        new_execution_id="replacement",
        trigger=NavigationReplanTrigger.ENVIRONMENT_CHANGED,
    )

    assert ready.navigation is not None and ready.navigation.status is NavigationStatus.READY
    assert replanned.replan is not None and replanned.replan.status is NavigationStatus.READY
    assert not replanned.moved and mission.environment is replacement


def test_unresolved_episode_consumes_at_most_five_replay_observations() -> None:
    mission = OfflineMission(environment())
    result, decoder = begin(mission, [(0.5, 0.5)] * 6)

    assert result.replay_episode is not None
    assert result.replay_episode.update_count == 5
    assert decoder.calls == 5
    assert result.navigation is None and mission.environment.state.position == (1, 0)


def test_duplicate_human_command_id_is_consumed_once_without_navigation_side_effect() -> None:
    mission = OfflineMission(environment())
    command = HumanCommand("pause-1", HumanCommandType.PAUSE)
    first = mission.submit_human_command(command)
    state_after_first = mission.controller.state
    duplicate = mission.submit_human_command(command)

    assert first.command is not None and first.command.status is CommandStatus.APPLIED
    assert duplicate.command is not None and duplicate.command.status is CommandStatus.ALREADY_CONSUMED
    assert mission.controller.state == state_after_first
    assert mission.navigation_runtime.session is None and mission.environment.state.position == (1, 0)


def test_stale_confirmation_request_fails_closed_without_goal_or_navigation() -> None:
    mission = OfflineMission(environment())
    confirmed, _ = begin(
        mission,
        [(0.5, 0.5)] * 4 + [(0.8, 0.2)],
        confirmation_request_id="request-current",
    )
    stale = mission.submit_human_command(
        HumanCommand("confirm-stale", HumanCommandType.CONFIRM, request_id="request-stale")
    )

    assert confirmed.navigation is None
    assert stale.command is not None and stale.command.status is CommandStatus.STALE_REQUEST
    assert mission.controller.state.approved_goal is None
    assert mission.navigation_runtime.session is None and mission.environment.state.position == (1, 0)


def test_malformed_replay_provenance_and_invalid_runtime_dependency_fail_closed() -> None:
    mission = OfflineMission(environment())
    malformed_epochs = epochs(1)
    malformed_epochs.metadata = None
    malformed = mission.begin_from_epochs(
        malformed_epochs,
        RecordingCspDecoder([np.asarray([[1.0, 0.0]])]),
        RecordingPlattCalibrator(),
        candidate_a="victim_a",
        candidate_b="victim_b",
        execution_id="malformed",
    )
    invalid_dependency = mission.begin_from_epochs(
        epochs(1),
        object(),
        object(),
        candidate_a="victim_a",
        candidate_b="victim_b",
        execution_id="invalid-dependency",
    )

    assert malformed.stage is MissionStage.REJECTED
    assert invalid_dependency.stage is MissionStage.REJECTED
    assert mission.navigation_runtime.session is None and mission.environment.state.position == (1, 0)


def test_one_caller_advance_executes_exactly_one_environment_transition(monkeypatch: pytest.MonkeyPatch) -> None:
    mission = OfflineMission(environment())
    ready, _ = begin(mission, [(1.0, 0.0)], execution_id="step-bound")
    step_calls: list[object] = []
    original_step = mission.environment.step

    def recording_step(action: object):
        step_calls.append(action)
        return original_step(action)

    monkeypatch.setattr(mission.environment, "step", recording_step)
    advanced = mission.advance_one_step()

    assert ready.navigation is not None and ready.navigation.status is NavigationStatus.READY
    assert advanced.navigation is not None and advanced.navigation.moved
    assert len(step_calls) == 1
    assert advanced.navigation.remaining_action_count > 0
