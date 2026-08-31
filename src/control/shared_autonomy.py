"""Approved binary shared-autonomy policy without execution dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from src.cognitive import bayes, uncertainty

CONFIRMATION_THRESHOLD = 0.75


class SharedAutonomyError(ValueError):
    """Raised when a policy input is inconsistent with the approved binary protocol."""


class AutonomyMode(str, Enum):
    """The policy outputs authorized by D-015 and D-055 through D-057."""

    WAITING = "WAITING"
    PROCEED = "PROCEED"
    CONFIRM = "CONFIRM"
    DEFER = "DEFER"
    PAUSE = "PAUSE"
    STOP = "STOP"


class HumanAction(str, Enum):
    """The human authority hooks covered by the current narrow policy task."""

    NONE = "NONE"
    PAUSE = "PAUSE"
    STOP = "STOP"
    OVERRIDE = "OVERRIDE"


@dataclass(frozen=True)
class SharedAutonomyDecision:
    """A non-executing policy decision for one binary Bayesian episode snapshot."""

    mode: AutonomyMode
    candidate_goal: str | None
    approved_goal: str | None
    requires_human_confirmation: bool
    holds_position: bool
    requests_human_input: bool
    human_action: HumanAction
    posterior_confidence: float
    entropy_bits: float
    update_count: int
    reason: str


def decide_shared_autonomy(
    episode_result: bayes.BayesianEpisodeResult,
    uncertainty_estimate: uncertainty.BinaryUncertainty,
    *,
    human_action: HumanAction = HumanAction.NONE,
) -> SharedAutonomyDecision:
    """Apply the approved posterior thresholds with immediate human authority precedence."""
    _validate_inputs(episode_result, uncertainty_estimate, human_action)

    if human_action is HumanAction.STOP:
        return _human_precedence_decision(
            AutonomyMode.STOP,
            human_action,
            episode_result,
            uncertainty_estimate,
            "Human STOP takes precedence over the normal confidence policy.",
        )
    if human_action is HumanAction.PAUSE:
        return _human_precedence_decision(
            AutonomyMode.PAUSE,
            human_action,
            episode_result,
            uncertainty_estimate,
            "Human PAUSE takes precedence over the normal confidence policy.",
        )
    if human_action is HumanAction.OVERRIDE:
        return _human_precedence_decision(
            AutonomyMode.WAITING,
            human_action,
            episode_result,
            uncertainty_estimate,
            "Human OVERRIDE takes precedence; correction and reset transitions are outside this policy.",
        )

    confidence = float(max(episode_result.posterior))
    leader = episode_result.candidate_names[int(np.argmax(episode_result.posterior))]
    if confidence >= bayes.COMMITMENT_THRESHOLD:
        return _decision(
            mode=AutonomyMode.PROCEED,
            candidate_goal=leader,
            approved_goal=leader,
            requires_human_confirmation=False,
            holds_position=False,
            requests_human_input=False,
            episode_result=episode_result,
            uncertainty_estimate=uncertainty_estimate,
            reason="Leading posterior reached the approved PROCEED threshold.",
        )
    if episode_result.update_count < bayes.MAX_EVIDENCE_UPDATES:
        return _decision(
            mode=AutonomyMode.WAITING,
            candidate_goal=None,
            approved_goal=None,
            requires_human_confirmation=False,
            holds_position=True,
            requests_human_input=False,
            episode_result=episode_result,
            uncertainty_estimate=uncertainty_estimate,
            reason="Below the PROCEED threshold before the approved five-update horizon.",
        )
    if confidence >= CONFIRMATION_THRESHOLD:
        return _decision(
            mode=AutonomyMode.CONFIRM,
            candidate_goal=leader,
            approved_goal=None,
            requires_human_confirmation=True,
            holds_position=True,
            requests_human_input=True,
            episode_result=episode_result,
            uncertainty_estimate=uncertainty_estimate,
            reason="Five updates exhausted with intermediate posterior confidence.",
        )
    return _decision(
        mode=AutonomyMode.DEFER,
        candidate_goal=None,
        approved_goal=None,
        requires_human_confirmation=False,
        holds_position=True,
        requests_human_input=True,
        episode_result=episode_result,
        uncertainty_estimate=uncertainty_estimate,
        reason="Five updates exhausted below the approved CONFIRM threshold.",
    )


def _validate_inputs(
    episode_result: bayes.BayesianEpisodeResult,
    uncertainty_estimate: uncertainty.BinaryUncertainty,
    human_action: HumanAction,
) -> None:
    if not isinstance(episode_result, bayes.BayesianEpisodeResult):
        raise SharedAutonomyError("Policy requires an accepted BayesianEpisodeResult.")
    if not isinstance(uncertainty_estimate, uncertainty.BinaryUncertainty):
        raise SharedAutonomyError("Policy requires a BinaryUncertainty estimate.")
    if not isinstance(human_action, HumanAction):
        raise SharedAutonomyError("Human action must be a HumanAction value.")
    if len(episode_result.candidate_names) != 2 or len(set(episode_result.candidate_names)) != 2:
        raise SharedAutonomyError("Policy requires exactly two distinct candidate goals.")
    if not isinstance(episode_result.update_count, int) or not 0 <= episode_result.update_count <= bayes.MAX_EVIDENCE_UPDATES:
        raise SharedAutonomyError("Bayesian update count must be between zero and the approved five-update limit.")

    posterior = uncertainty.validate_binary_posterior(episode_result.posterior)
    uncertainty_estimate.validate()
    if not np.allclose(posterior, uncertainty_estimate.posterior, rtol=0.0, atol=1e-12):
        raise SharedAutonomyError("Uncertainty must be computed from the same Bayesian posterior.")


def _human_precedence_decision(
    mode: AutonomyMode,
    human_action: HumanAction,
    episode_result: bayes.BayesianEpisodeResult,
    uncertainty_estimate: uncertainty.BinaryUncertainty,
    reason: str,
) -> SharedAutonomyDecision:
    return _decision(
        mode=mode,
        candidate_goal=None,
        approved_goal=None,
        requires_human_confirmation=False,
        holds_position=True,
        requests_human_input=False,
        episode_result=episode_result,
        uncertainty_estimate=uncertainty_estimate,
        reason=reason,
        human_action=human_action,
    )


def _decision(
    *,
    mode: AutonomyMode,
    candidate_goal: str | None,
    approved_goal: str | None,
    requires_human_confirmation: bool,
    holds_position: bool,
    requests_human_input: bool,
    episode_result: bayes.BayesianEpisodeResult,
    uncertainty_estimate: uncertainty.BinaryUncertainty,
    reason: str,
    human_action: HumanAction = HumanAction.NONE,
) -> SharedAutonomyDecision:
    return SharedAutonomyDecision(
        mode=mode,
        candidate_goal=candidate_goal,
        approved_goal=approved_goal,
        requires_human_confirmation=requires_human_confirmation,
        holds_position=holds_position,
        requests_human_input=requests_human_input,
        human_action=human_action,
        posterior_confidence=float(max(episode_result.posterior)),
        entropy_bits=uncertainty_estimate.entropy_bits,
        update_count=episode_result.update_count,
        reason=reason,
    )
