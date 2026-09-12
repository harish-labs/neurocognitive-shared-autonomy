"""Caller-driven composition of the accepted offline EEG mission boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterator

import mne

from src.autonomy.environment import SearchRescueEnvironment
from src.cognitive.replay_episode import BayesianReplayEpisodeResult, ReplayEpisodeIntegrationError, run_bayesian_replay_episode
from src.control.human_interaction import CommandResult, HumanCommand, HumanInteractionController
from src.control.intent_navigation_bridge import IntentNavigationResult, IntentNavigationStatus, authorize_episode_navigation
from src.control.navigation_runtime import NavigationResult, NavigationRuntime, NavigationStatus, ReplanResult
from src.eeg.replay import OfflineEpochReplay, ReplayObservation, ReplayValidationError
from src.models.calibration import PlattScalingCalibrator, TemperatureScalingCalibrator
from src.models.csp_lda import CspLdaDecoder
from src.models.eegnet import EEGNetDecoder
from src.models.runtime_adapter import DecodedReplayObservation, RuntimeAdapterError, decode_replay_observation


class MissionStage(str, Enum):
    """The caller-visible accepted boundary that produced a mission result."""

    EPISODE = "EPISODE"
    COMMAND = "COMMAND"
    NAVIGATION = "NAVIGATION"
    STEP = "STEP"
    REPLAN = "REPLAN"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class OfflineMissionResult:
    """Immutable audit result from one explicit offline mission operation."""

    stage: MissionStage
    replay_episode: BayesianReplayEpisodeResult | None
    intent_navigation: IntentNavigationResult | None
    command: CommandResult | None
    navigation: NavigationResult | None
    replan: ReplanResult | None
    moved: bool
    reason: str


class OfflineMission:
    """Synchronous mission session with explicit caller control between every action."""

    def __init__(
        self,
        environment: SearchRescueEnvironment,
        *,
        controller: HumanInteractionController | None = None,
        navigation_runtime: NavigationRuntime | None = None,
    ) -> None:
        if not isinstance(environment, SearchRescueEnvironment):
            raise ValueError("OfflineMission requires an accepted SearchRescueEnvironment.")
        self._environment = environment
        self._controller = HumanInteractionController() if controller is None else controller
        self._navigation_runtime = NavigationRuntime() if navigation_runtime is None else navigation_runtime
        if not isinstance(self._controller, HumanInteractionController) or not isinstance(
            self._navigation_runtime, NavigationRuntime
        ):
            raise ValueError("OfflineMission requires accepted human-interaction and navigation runtimes.")
        self._latest_episode: BayesianReplayEpisodeResult | None = None
        self._latest_intent: IntentNavigationResult | None = None

    @property
    def controller(self) -> HumanInteractionController:
        return self._controller

    @property
    def navigation_runtime(self) -> NavigationRuntime:
        return self._navigation_runtime

    @property
    def environment(self) -> SearchRescueEnvironment:
        return self._environment

    def begin_from_epochs(
        self,
        epochs: mne.BaseEpochs,
        decoder: CspLdaDecoder | EEGNetDecoder,
        calibrator: PlattScalingCalibrator | TemperatureScalingCalibrator,
        *,
        candidate_a: object,
        candidate_b: object,
        confirmation_request_id: object | None = None,
        execution_id: object | None = None,
    ) -> OfflineMissionResult:
        """Run one bounded replay episode and optionally establish a zero-movement plan."""

        if not _valid_candidates(candidate_a, candidate_b, self._environment):
            return _rejected("Mission candidates must be two distinct current symbolic environment-goal keys.")
        try:
            replay = OfflineEpochReplay(epochs)
            episode = run_bayesian_replay_episode(
                self._decoded_observations(replay, epochs, decoder, calibrator),
                candidate_a=candidate_a,
                candidate_b=candidate_b,
            )
        except (ReplayValidationError, RuntimeAdapterError, ReplayEpisodeIntegrationError, TypeError, ValueError) as error:
            return _rejected(str(error))

        self._latest_episode = episode
        intent = authorize_episode_navigation(
            episode,
            self._controller,
            self._environment,
            self._navigation_runtime,
            confirmation_request_id=confirmation_request_id,
            execution_id=execution_id,
        )
        self._latest_intent = intent
        return OfflineMissionResult(
            stage=MissionStage.EPISODE,
            replay_episode=episode,
            intent_navigation=intent,
            command=None,
            navigation=intent.navigation,
            replan=None,
            moved=False,
            reason=intent.reason,
        )

    def submit_human_command(self, command: HumanCommand) -> OfflineMissionResult:
        """Process exactly one caller-supplied human command through the accepted controller."""

        result = self._controller.handle_command(command, valid_goals=self._environment.config.goals)
        return OfflineMissionResult(
            stage=MissionStage.COMMAND,
            replay_episode=self._latest_episode,
            intent_navigation=self._latest_intent,
            command=result,
            navigation=None,
            replan=None,
            moved=False,
            reason=result.reason,
        )

    def start_navigation_from_command(
        self,
        command_result: CommandResult,
        *,
        execution_id: object,
    ) -> OfflineMissionResult:
        """Use an already-applied explicit human command as the existing fresh start source."""

        navigation = self._navigation_runtime.start_navigation(
            self._environment,
            self._controller,
            command_result,
            execution_id=execution_id,
        )
        return OfflineMissionResult(
            stage=MissionStage.NAVIGATION,
            replay_episode=self._latest_episode,
            intent_navigation=self._latest_intent,
            command=command_result,
            navigation=navigation,
            replan=None,
            moved=navigation.moved,
            reason=navigation.reason,
        )

    def advance_one_step(self) -> OfflineMissionResult:
        """Delegate exactly one caller-requested, safety-gated navigation step."""

        navigation = self._navigation_runtime.advance_one_step(self._environment, self._controller)
        return OfflineMissionResult(
            stage=MissionStage.STEP,
            replay_episode=self._latest_episode,
            intent_navigation=self._latest_intent,
            command=None,
            navigation=navigation,
            replan=None,
            moved=navigation.moved,
            reason=navigation.reason,
        )

    def replan_after_environment_change(
        self,
        replacement_environment: SearchRescueEnvironment,
        *,
        source_execution_id: object,
        event_id: object,
        new_execution_id: object,
        trigger: object,
        prior_result: NavigationResult | None = None,
        resume_result: CommandResult | None = None,
    ) -> OfflineMissionResult:
        """Delegate one caller-supplied D-070 replacement-snapshot replan request."""

        replan = self._navigation_runtime.replan_after_environment_change(
            self._environment,
            replacement_environment,
            self._controller,
            source_execution_id=source_execution_id,
            event_id=event_id,
            new_execution_id=new_execution_id,
            trigger=trigger,
            prior_result=prior_result,
            resume_result=resume_result,
        )
        if replan.status is NavigationStatus.READY:
            self._environment = replacement_environment
        return OfflineMissionResult(
            stage=MissionStage.REPLAN,
            replay_episode=self._latest_episode,
            intent_navigation=self._latest_intent,
            command=resume_result,
            navigation=replan.navigation_result,
            replan=replan,
            moved=False,
            reason=replan.reason,
        )

    @staticmethod
    def _decoded_observations(
        replay: OfflineEpochReplay,
        epochs: mne.BaseEpochs,
        decoder: CspLdaDecoder | EEGNetDecoder,
        calibrator: PlattScalingCalibrator | TemperatureScalingCalibrator,
    ) -> Iterator[DecodedReplayObservation]:
        for observation in replay:
            yield decode_replay_observation(observation, epochs, decoder, calibrator)


def _valid_candidates(candidate_a: object, candidate_b: object, environment: SearchRescueEnvironment) -> bool:
    return (
        isinstance(candidate_a, str)
        and isinstance(candidate_b, str)
        and bool(candidate_a)
        and bool(candidate_b)
        and candidate_a != candidate_b
        and candidate_a in environment.config.goals
        and candidate_b in environment.config.goals
    )


def _rejected(reason: str) -> OfflineMissionResult:
    return OfflineMissionResult(
        stage=MissionStage.REJECTED,
        replay_episode=None,
        intent_navigation=None,
        command=None,
        navigation=None,
        replan=None,
        moved=False,
        reason=reason,
    )
