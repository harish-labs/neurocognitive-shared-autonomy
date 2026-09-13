"""Synthetic/development-only orchestration for the frozen D-077 conditions."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.cognitive.adaptation import PriorPersonalizer
from src.cognitive.bayes import COMMITMENT_THRESHOLD, INITIAL_PRIOR, BinaryBayesianGoalEpisode, EpisodeStatus, binary_goal_evidence_from_calibrated_probabilities
from src.cognitive.uncertainty import estimate_binary_uncertainty
from src.control.shared_autonomy import CONFIRMATION_THRESHOLD, AutonomyMode, decide_shared_autonomy
from src.evaluation.conditions import ConditionId, get_condition
from src.evaluation.robustness import PerturbationResult, contaminate_contradictory_evidence, flatten_evidence
from src.evaluation.schemas import ALLOWED_M7_T01_SPLITS, DECODER_FAMILIES


class ExperimentError(ValueError):
    """Raised when M7-T01 orchestration would cross an approved boundary."""


@dataclass(frozen=True)
class DevelopmentEpisodeInput:
    episode_id: str
    subject_key: str
    split: str
    decoder_family: str
    candidate_names: tuple[str, str]
    raw_probabilities: tuple[tuple[float, float], ...]
    calibrated_probabilities: tuple[tuple[float, float], ...]
    true_goal: str | None = None


@dataclass(frozen=True)
class ConditionEpisodeResult:
    episode_id: str
    subject_key: str
    condition_id: str
    condition_name: str
    decoder_family: str
    candidate_names: tuple[str, str]
    evidence_source: str
    initial_prior: tuple[float, float] | None
    accepted_evidence_count: int
    posterior: tuple[float, float]
    posterior_confidence: float
    entropy_bits: float
    autonomy_mode: str
    candidate_goal: str | None
    committed_goal: str | None
    correct_commitment: bool | None
    perturbation: PerturbationResult | None


def run_development_condition(
    episode_input: DevelopmentEpisodeInput,
    condition_id: ConditionId | str,
    *,
    perturbation_family: str | None = None,
    severity: float | None = None,
    perturbation_seed: int | None = None,
    personalizer: PriorPersonalizer | None = None,
) -> ConditionEpisodeResult:
    _validate_input(episode_input)
    condition = get_condition(condition_id)
    source = "calibrated" if condition.components.calibration else "raw_identity"
    evidence = np.asarray(
        episode_input.calibrated_probabilities if condition.components.calibration else episode_input.raw_probabilities,
        dtype=np.float64,
    )[: condition.components.evidence_horizon]
    perturbation = _perturb(evidence, perturbation_family, severity, perturbation_seed)
    if perturbation is not None:
        evidence = np.asarray(perturbation.perturbed_evidence, dtype=np.float64)

    if condition.condition_id is ConditionId.A:
        initial_prior = None
        posterior = tuple(float(value) for value in evidence[0])
        leader = episode_input.candidate_names[int(np.argmax(evidence[0]))]
        mode = AutonomyMode.PROCEED
        candidate_goal = leader
        committed_goal = leader
        accepted = 1
    elif condition.condition_id is ConditionId.B:
        initial_prior = None
        posterior = tuple(float(value) for value in evidence[0])
        confidence = max(posterior)
        entropy = estimate_binary_uncertainty(posterior)
        leader = episode_input.candidate_names[int(np.argmax(evidence[0]))]
        accepted = 1
        if confidence >= COMMITMENT_THRESHOLD:
            mode, candidate_goal, committed_goal = AutonomyMode.PROCEED, leader, leader
        elif confidence >= CONFIRMATION_THRESHOLD:
            mode, candidate_goal, committed_goal = AutonomyMode.CONFIRM, leader, None
        else:
            mode, candidate_goal, committed_goal = AutonomyMode.DEFER, None, None
    else:
        initial_prior = INITIAL_PRIOR
        if condition.components.adaptation:
            active_personalizer = personalizer or PriorPersonalizer(adaptation_enabled=True)
            if not active_personalizer.adaptation_enabled:
                raise ExperimentError("System D requires adaptation_enabled=True under D-077.")
            initial_prior = active_personalizer.initial_prior_for_new_episode(
                episode_input.subject_key, *episode_input.candidate_names
            )
        episode = BinaryBayesianGoalEpisode(
            candidate_a=episode_input.candidate_names[0],
            candidate_b=episode_input.candidate_names[1],
            initial_prior=initial_prior,
        )
        decision = None
        for row in evidence:
            update = episode.accept_evidence(binary_goal_evidence_from_calibrated_probabilities(row))
            uncertainty = estimate_binary_uncertainty(update.posterior)
            decision = decide_shared_autonomy(update, uncertainty)
            if update.status is not EpisodeStatus.PENDING:
                break
        if decision is None:
            raise ExperimentError("At least one accepted evidence observation is required.")
        posterior = episode.posterior
        mode = decision.mode
        candidate_goal = decision.candidate_goal
        committed_goal = decision.approved_goal
        accepted = episode.update_count

    uncertainty = estimate_binary_uncertainty(posterior)
    correctness = None if episode_input.true_goal is None or committed_goal is None else committed_goal == episode_input.true_goal
    return ConditionEpisodeResult(
        episode_id=episode_input.episode_id,
        subject_key=episode_input.subject_key,
        condition_id=condition.condition_id.value,
        condition_name=condition.name,
        decoder_family=episode_input.decoder_family,
        candidate_names=episode_input.candidate_names,
        evidence_source=source,
        initial_prior=initial_prior,
        accepted_evidence_count=accepted,
        posterior=posterior,
        posterior_confidence=max(posterior),
        entropy_bits=uncertainty.entropy_bits,
        autonomy_mode=mode.value,
        candidate_goal=candidate_goal,
        committed_goal=committed_goal,
        correct_commitment=correctness,
        perturbation=perturbation,
    )


def _validate_input(value: object) -> None:
    if not isinstance(value, DevelopmentEpisodeInput):
        raise ExperimentError("Orchestration requires DevelopmentEpisodeInput.")
    if not value.episode_id or not value.subject_key:
        raise ExperimentError("episode_id and anonymous subject_key are required.")
    if value.split.lower() not in ALLOWED_M7_T01_SPLITS:
        raise ExperimentError("M7-T01 refuses protected test/final-test execution.")
    if value.decoder_family not in DECODER_FAMILIES:
        raise ExperimentError("Both approved decoder-family labels are supported: csp_lda and eegnet.")
    if len(value.candidate_names) != 2 or any(not isinstance(name, str) or not name for name in value.candidate_names) or value.candidate_names[0] == value.candidate_names[1]:
        raise ExperimentError("Exactly two distinct non-empty candidate names are required.")
    if value.true_goal is not None and value.true_goal not in value.candidate_names:
        raise ExperimentError("Evaluation-only true_goal must belong to the candidate pair.")
    raw = _probabilities(value.raw_probabilities, "raw_probabilities")
    calibrated = _probabilities(value.calibrated_probabilities, "calibrated_probabilities")
    if raw.shape != calibrated.shape:
        raise ExperimentError("Raw and calibrated evidence must align observation-for-observation.")


def _probabilities(values: object, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 2 or array.shape[1] != 2 or len(array) == 0:
        raise ExperimentError(f"{name} must be a non-empty (n, 2) sequence.")
    if not np.isfinite(array).all() or (array < 0).any() or (array > 1).any() or not np.allclose(array.sum(axis=1), 1.0, rtol=0.0, atol=1e-8):
        raise ExperimentError(f"{name} must contain normalized finite binary probabilities.")
    return array


def _perturb(evidence: np.ndarray, family: str | None, severity: float | None, seed: int | None) -> PerturbationResult | None:
    if family is None:
        if severity is not None or seed is not None:
            raise ExperimentError("Unperturbed orchestration cannot carry severity or perturbation_seed.")
        return None
    if severity is None:
        raise ExperimentError("Perturbed orchestration requires severity.")
    if family == "R1":
        if seed is not None:
            raise ExperimentError("Deterministic R1 flattening does not use a random seed.")
        return flatten_evidence(evidence, severity)
    if family == "R2":
        if seed is None:
            raise ExperimentError("R2 contamination requires a recorded seed.")
        return contaminate_contradictory_evidence(evidence, severity, seed=seed)
    raise ExperimentError("perturbation_family must be None, 'R1', or 'R2'.")
