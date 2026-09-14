"""D-084 execution-layer semantics for the two sequential E7 ablations."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

import numpy as np

from src.cognitive.bayes import INITIAL_PRIOR
from src.cognitive.uncertainty import estimate_binary_uncertainty
from src.control.shared_autonomy import AutonomyMode, CONFIRMATION_THRESHOLD


D084_POLICY_ID = "D-084"
PROCEED_THRESHOLD = 0.90
EXACT_EVIDENCE_HORIZON = 5

D084_ABLATION_SEMANTICS: Mapping[str, Mapping[str, object]] = MappingProxyType(
    {
        "full_minus_bayes": {
            "policy_id": D084_POLICY_ID,
            "aggregation": "cumulative_arithmetic_mean_of_calibrated_binary_evidence",
            "evidence_horizon": "up_to_5",
            "uncertainty_gating": True,
            "proceed_threshold": PROCEED_THRESHOLD,
            "final_confirm_interval": (CONFIRMATION_THRESHOLD, PROCEED_THRESHOLD),
            "final_defer_below": CONFIRMATION_THRESHOLD,
            "entropy_role": "descriptive_only",
        },
        "full_minus_uncertainty": {
            "policy_id": D084_POLICY_ID,
            "aggregation": "d053_sequential_bayesian_posterior",
            "evidence_horizon": "exactly_5",
            "uncertainty_gating": False,
            "autonomous_modes_removed": ("PROCEED", "CONFIRM", "DEFER"),
            "final_commitment": "posterior_argmax_after_observation_5",
            "tie_break": "stable_candidate_order_a_before_b",
            "entropy_role": "descriptive_only",
        },
    }
)


class AblationSemanticsError(ValueError):
    """Raised when D-084 evaluation semantics would be violated."""


@dataclass(frozen=True)
class D084AblationDecision:
    ablation_id: str
    candidate_names: tuple[str, str]
    accepted_evidence_count: int
    posterior: tuple[float, float]
    entropy_bits: float
    autonomy_mode: str
    candidate_goal: str | None
    committed_goal: str | None
    tie_break_applied: bool
    posterior_history: tuple[tuple[float, float], ...]


def evaluate_full_minus_bayes(
    calibrated_evidence: object,
    *,
    candidate_names: tuple[str, str],
) -> D084AblationDecision:
    """Apply D-084's non-Bayesian running-mean policy to up to five observations."""

    evidence = _validated_evidence(calibrated_evidence, exact_five=False)
    candidates = _validated_candidates(candidate_names)
    running_total = np.zeros(2, dtype=np.float64)
    history: list[tuple[float, float]] = []
    for index, row in enumerate(evidence, start=1):
        running_total += row
        posterior = running_total / index
        history.append(_as_pair(posterior))
        leader_index = int(np.argmax(posterior))
        leader = candidates[leader_index]
        confidence = float(posterior[leader_index])
        if confidence >= PROCEED_THRESHOLD:
            return _decision(
                "full_minus_bayes", candidates, index, posterior, AutonomyMode.PROCEED, leader, leader, False, history
            )
        if index == EXACT_EVIDENCE_HORIZON:
            if confidence >= CONFIRMATION_THRESHOLD:
                return _decision(
                    "full_minus_bayes", candidates, index, posterior, AutonomyMode.CONFIRM, leader, None, False, history
                )
            return _decision(
                "full_minus_bayes", candidates, index, posterior, AutonomyMode.DEFER, None, None, False, history
            )
    raise AblationSemanticsError("D-084 Full - Bayes requires at least one observation and at most five observations.")


def evaluate_full_minus_uncertainty(
    calibrated_evidence: object,
    *,
    candidate_names: tuple[str, str],
    initial_prior: tuple[float, float] = INITIAL_PRIOR,
) -> D084AblationDecision:
    """Apply five D-053 updates without early uncertainty-gated commitment."""

    evidence = _validated_evidence(calibrated_evidence, exact_five=True)
    candidates = _validated_candidates(candidate_names)
    posterior = _validated_prior(initial_prior)
    history: list[tuple[float, float]] = []
    for row in evidence:
        unnormalized = posterior * row
        total = float(unnormalized.sum())
        if not np.isfinite(total) or total <= 0.0:
            raise AblationSemanticsError("D-053 update produced invalid normalization mass.")
        posterior = unnormalized / total
        history.append(_as_pair(posterior))
    tie_break = bool(np.isclose(posterior[0], posterior[1], rtol=0.0, atol=1e-12))
    leader = candidates[0 if tie_break else int(np.argmax(posterior))]
    return _decision(
        "full_minus_uncertainty",
        candidates,
        EXACT_EVIDENCE_HORIZON,
        posterior,
        AutonomyMode.PROCEED,
        leader,
        leader,
        tie_break,
        history,
    )


def _decision(
    ablation_id: str,
    candidates: tuple[str, str],
    count: int,
    posterior: np.ndarray,
    mode: AutonomyMode,
    candidate_goal: str | None,
    committed_goal: str | None,
    tie_break: bool,
    history: list[tuple[float, float]],
) -> D084AblationDecision:
    uncertainty = estimate_binary_uncertainty(posterior)
    return D084AblationDecision(
        ablation_id=ablation_id,
        candidate_names=candidates,
        accepted_evidence_count=count,
        posterior=_as_pair(posterior),
        entropy_bits=uncertainty.entropy_bits,
        autonomy_mode=mode.value,
        candidate_goal=candidate_goal,
        committed_goal=committed_goal,
        tie_break_applied=tie_break,
        posterior_history=tuple(history),
    )


def _validated_evidence(value: object, *, exact_five: bool) -> np.ndarray:
    evidence = np.asarray(value, dtype=np.float64)
    if evidence.ndim != 2 or evidence.shape[1] != 2:
        raise AblationSemanticsError("Calibrated evidence must be a non-empty normalized (n, 2) array.")
    if len(evidence) == 0 or len(evidence) > EXACT_EVIDENCE_HORIZON or (exact_five and len(evidence) != EXACT_EVIDENCE_HORIZON):
        requirement = "exactly five" if exact_five else "between one and five"
        raise AblationSemanticsError(f"D-084 requires {requirement} observations.")
    if not np.isfinite(evidence).all() or (evidence < 0.0).any() or (evidence > 1.0).any():
        raise AblationSemanticsError("Calibrated evidence must be finite probabilities in [0, 1].")
    if not np.allclose(evidence.sum(axis=1), 1.0, rtol=0.0, atol=1e-8):
        raise AblationSemanticsError("Every calibrated evidence vector must be normalized.")
    return evidence


def _validated_candidates(value: object) -> tuple[str, str]:
    if not isinstance(value, tuple) or len(value) != 2:
        raise AblationSemanticsError("D-084 requires an ordered pair of candidates.")
    candidates = (str(value[0]), str(value[1]))
    if not all(candidates) or candidates[0] == candidates[1]:
        raise AblationSemanticsError("Candidates must be distinct non-empty names.")
    return candidates


def _validated_prior(value: object) -> np.ndarray:
    prior = np.asarray(value, dtype=np.float64)
    if prior.shape != (2,) or not np.isfinite(prior).all() or (prior < 0.0).any() or not np.isclose(prior.sum(), 1.0):
        raise AblationSemanticsError("Initial prior must be a normalized binary probability vector.")
    return prior


def _as_pair(value: np.ndarray) -> tuple[float, float]:
    return (float(value[0]), float(value[1]))
