"""Fail-closed, JSON-ready M7 result and provenance structures."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import json
from typing import Any, Mapping

from src.evaluation.conditions import ABLATIONS, ConditionId
from src.evaluation.robustness import R1_SEVERITIES, R2_SEVERITIES


class SchemaError(ValueError):
    """Raised when experiment provenance is incomplete or protected."""


class ExperimentStatus(str, Enum):
    DEVELOPMENT_ONLY = "DEVELOPMENT_ONLY"
    VALID = "VALID"
    INVALID = "INVALID"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"


PROTECTED_SPLITS = frozenset({"test", "final_test", "protected_test", "protected_final_test"})
ALLOWED_M7_T01_SPLITS = frozenset({"synthetic", "development", "train", "training", "validation"})
DECODER_FAMILIES = frozenset({"csp_lda", "eegnet"})


@dataclass(frozen=True)
class ExperimentProvenance:
    experiment_family: str
    experiment_id: str
    condition: str
    ablation: str | None
    decoder_family: str
    split: str
    evaluation_track: str
    subject_key: str
    seeds: Mapping[str, int]
    perturbation_family: str | None
    perturbation_severity: float | None
    perturbation_selection_rule: str | None
    selected_indices: tuple[int, ...]
    effective_operational_configuration: Mapping[str, Any]
    scientific_policy_ids: tuple[str, ...]
    input_provenance: tuple[Mapping[str, Any], ...]
    software_git_sha: str
    status: ExperimentStatus = ExperimentStatus.DEVELOPMENT_ONLY

    def validate(self, *, m7_t01: bool = True) -> None:
        required_strings = (
            "experiment_family", "experiment_id", "condition", "decoder_family", "split",
            "evaluation_track", "subject_key", "software_git_sha",
        )
        if any(not isinstance(getattr(self, name), str) or not getattr(self, name) for name in required_strings):
            raise SchemaError("Required provenance strings must be non-empty.")
        if self.decoder_family not in DECODER_FAMILIES:
            raise SchemaError("decoder_family must be 'csp_lda' or 'eegnet'.")
        if self.experiment_family not in {f"E{index}" for index in range(1, 10)}:
            raise SchemaError("experiment_family must be one of E1 through E9.")
        if self.condition not in {item.value for item in ConditionId}:
            raise SchemaError("condition must identify frozen principal condition A, B, C, or D.")
        if self.ablation is not None and self.ablation not in ABLATIONS:
            raise SchemaError("ablation must be a registered component-ablation key when supplied.")
        normalized_split = self.split.lower()
        if m7_t01 and normalized_split not in ALLOWED_M7_T01_SPLITS:
            raise SchemaError("M7-T01 may use only synthetic/development/training/validation inputs.")
        if m7_t01 and normalized_split in PROTECTED_SPLITS:
            raise SchemaError("Protected final-test execution/access is forbidden in M7-T01.")
        if self.status is not ExperimentStatus.DEVELOPMENT_ONLY and m7_t01:
            raise SchemaError("M7-T01 result records must be DEVELOPMENT_ONLY.")
        if not isinstance(self.seeds, Mapping) or any(
            not isinstance(key, str) or not key or isinstance(value, bool) or not isinstance(value, int) or value < 0
            for key, value in self.seeds.items()
        ):
            raise SchemaError("Seeds must be a mapping of non-empty names to non-negative integers.")
        if not self.scientific_policy_ids or any(not isinstance(item, str) or not item for item in self.scientific_policy_ids):
            raise SchemaError("At least one scientific-policy identifier is required.")
        if self.perturbation_family is None:
            if self.perturbation_severity is not None or self.perturbation_selection_rule is not None or self.selected_indices:
                raise SchemaError("Unperturbed records cannot carry severity, selection rule, or selected indices.")
        else:
            if not isinstance(self.perturbation_selection_rule, str) or not self.perturbation_selection_rule:
                raise SchemaError("Perturbation provenance requires a selection rule.")
            allowed = {
                "R1_EVIDENCE_FLATTENING": R1_SEVERITIES,
                "R2_CONTRADICTORY_EVIDENCE": R2_SEVERITIES,
            }
            if self.perturbation_family not in allowed or self.perturbation_severity not in allowed[self.perturbation_family]:
                raise SchemaError("Perturbation family/severity must match frozen D-078 values.")
            if self.perturbation_family == "R2_CONTRADICTORY_EVIDENCE" and not self.seeds:
                raise SchemaError("R2 perturbation provenance requires a recorded seed.")
        if (
            not isinstance(self.selected_indices, tuple)
            or len(set(self.selected_indices)) != len(self.selected_indices)
            or any(isinstance(index, bool) or not isinstance(index, int) or index < 0 for index in self.selected_indices)
        ):
            raise SchemaError("selected_indices must be unique non-negative integer indices.")
        if not isinstance(self.effective_operational_configuration, Mapping):
            raise SchemaError("Effective operational configuration must be a mapping.")
        if not isinstance(self.input_provenance, tuple) or any(not isinstance(item, Mapping) for item in self.input_provenance):
            raise SchemaError("input_provenance must be an explicit tuple of mappings.")
        _ensure_json_ready(self)


@dataclass(frozen=True)
class ExperimentResult:
    provenance: ExperimentProvenance
    metric_definitions: Mapping[str, Mapping[str, Any]]
    subject_level_metrics: tuple[Mapping[str, Any], ...]
    aggregate_metrics: Mapping[str, Any]
    statistical_outputs: Mapping[str, Any]

    def validate(self, *, m7_t01: bool = True) -> None:
        if not isinstance(self.provenance, ExperimentProvenance):
            raise SchemaError("ExperimentResult requires ExperimentProvenance.")
        self.provenance.validate(m7_t01=m7_t01)
        if not isinstance(self.metric_definitions, Mapping) or not self.metric_definitions:
            raise SchemaError("Metric definitions with units and denominators are required.")
        for name, definition in self.metric_definitions.items():
            if not isinstance(name, str) or not name or not isinstance(definition, Mapping):
                raise SchemaError("Metric definitions must be named mappings.")
            if "evaluation_unit" not in definition or "denominator" not in definition:
                raise SchemaError("Each metric definition must state evaluation_unit and denominator.")
        if not isinstance(self.subject_level_metrics, tuple):
            raise SchemaError("subject_level_metrics must be an explicit tuple.")
        if not isinstance(self.aggregate_metrics, Mapping) or not isinstance(self.statistical_outputs, Mapping):
            raise SchemaError("Aggregate metrics and statistical outputs must be mappings.")
        _ensure_json_ready(self)

    def to_json(self, *, m7_t01: bool = True) -> str:
        self.validate(m7_t01=m7_t01)
        return json.dumps(_plain(self), sort_keys=True, separators=(",", ":"), allow_nan=False)


def _plain(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _plain(item) for key, item in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    return value


def _ensure_json_ready(value: Any) -> None:
    try:
        json.dumps(_plain(value), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise SchemaError("Result/provenance fields must be finite and JSON serializable.") from exc
