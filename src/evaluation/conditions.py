"""Frozen D-077 principal conditions and component-ablation definitions."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from types import MappingProxyType
from typing import Mapping


class ConditionError(ValueError):
    """Raised when an experiment condition would violate the frozen registry."""


class ConditionId(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


@dataclass(frozen=True)
class ComponentSet:
    frozen_decoder_evidence: bool
    calibration: bool
    evidence_horizon: int
    sequential_bayes: bool
    uncertainty_gating: bool
    human_confirm_defer: bool
    astar_navigation: bool
    same_risk_model: bool
    hard_safety: bool
    human_emergency_authority: bool
    adaptation: bool


@dataclass(frozen=True)
class ConditionDefinition:
    condition_id: ConditionId
    name: str
    components: ComponentSet
    calibration_mode: str
    decision_rule: str


PRINCIPAL_CONDITIONS: Mapping[ConditionId, ConditionDefinition] = MappingProxyType({
    ConditionId.A: ConditionDefinition(
        ConditionId.A,
        "Direct EEG",
        ComponentSet(True, False, 1, False, False, False, True, True, True, True, False),
        "identity",
        "first_evidence_argmax",
    ),
    ConditionId.B: ConditionDefinition(
        ConditionId.B,
        "Confidence-Aware",
        ComponentSet(True, True, 1, False, True, True, True, True, True, True, False),
        "model_specific",
        "single_evidence_d055_d057_thresholds",
    ),
    ConditionId.C: ConditionDefinition(
        ConditionId.C,
        "Bayesian Shared Autonomy",
        ComponentSet(True, True, 5, True, True, True, True, True, True, True, False),
        "model_specific",
        "d053_d057_sequential",
    ),
    ConditionId.D: ConditionDefinition(
        ConditionId.D,
        "Full System",
        ComponentSet(True, True, 5, True, True, True, True, True, True, True, True),
        "model_specific",
        "d053_d060_sequential_adaptive_prior",
    ),
})


@dataclass(frozen=True)
class AblationDefinition:
    name: str
    removed_component: str | None
    components: ComponentSet


def _ablation(name: str, field: str | None) -> AblationDefinition:
    full = PRINCIPAL_CONDITIONS[ConditionId.D].components
    if field is None:
        return AblationDefinition(name, None, full)
    if field not in {"calibration", "sequential_bayes", "uncertainty_gating", "hard_safety", "adaptation"}:
        raise ConditionError(f"Unsupported ablation component {field!r}.")
    return AblationDefinition(name, field, replace(full, **{field: False}))


ABLATIONS: Mapping[str, AblationDefinition] = MappingProxyType({
    "full": _ablation("Full", None),
    "full_minus_calibration": _ablation("Full - calibration", "calibration"),
    "full_minus_bayes": _ablation("Full - Bayes", "sequential_bayes"),
    "full_minus_uncertainty": _ablation("Full - uncertainty", "uncertainty_gating"),
    "full_minus_safety": _ablation("Full - safety", "hard_safety"),
    "full_minus_adaptation": _ablation("Full - adaptation", "adaptation"),
})


def get_condition(condition_id: ConditionId | str) -> ConditionDefinition:
    try:
        key = condition_id if isinstance(condition_id, ConditionId) else ConditionId(condition_id)
    except (TypeError, ValueError) as exc:
        raise ConditionError(f"Unknown principal condition {condition_id!r}.") from exc
    return PRINCIPAL_CONDITIONS[key]
