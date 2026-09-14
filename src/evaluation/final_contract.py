"""Frozen M7-T02 execution contract, leakage gates, and immutable manifests."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from src.evaluation.conditions import ABLATIONS, PRINCIPAL_CONDITIONS
from src.evaluation.ablation_semantics import D084_ABLATION_SEMANTICS
from src.evaluation.cohort import (
    D082_SPLIT_MANIFEST_VERSION,
    D082_SPLIT_SEED,
    SOURCE_SUBJECT_IDS,
    D082CrossSubjectSplitManifest,
    SubjectEligibilityRecord,
    build_qc_manifest,
    build_split_manifest,
    qc_manifest_from_mapping,
    split_manifest_from_mapping,
    validate_split_manifest,
)
from src.evaluation.episodes import (
    D081_EPISODE_MANIFEST_VERSION,
    D081_GROUPING_KEY,
    D081_ORDERING_RULE,
    D081_E9_ORDERING_RULE,
    EpisodeManifest,
    SequentialParticipationManifest,
    load_episode_manifest,
    sequential_participation_manifest_from_mapping,
    validate_episode_manifest,
    validate_sequential_participation_manifest,
)
from src.evaluation.robustness import R1_SEVERITIES, R2_SEVERITIES


M7_EXECUTION_MANIFEST_VERSION = "m7-t02-final-execution-v6-d084-r03-final"
M7_RESULT_SCHEMA_VERSION = "m7-final-results-v1"
M7_SCENARIO_VERSION = "m7-t02-s1-s7-v1"
SIMULATED_HUMAN_POLICY_ID = "m7-t02-deterministic-simulated-human-v1"
OPERATIONAL_SEED = 42
EXPECTED_EXPERIMENT_FAMILIES = tuple(f"E{index}" for index in range(1, 10))
EXPECTED_POLICY_IDS = tuple(f"D-{index:03d}" for index in range(77, 85))
FORMAL_COMPARISON_SET = (
    "csp_lda.D_minus_A_correctness",
    "eegnet.D_minus_A_correctness",
)
FINAL_REPORTING_CONTRACT: Mapping[str, Any] = {
    "source": "single_frozen_machine_readable_result_artifact",
    "tables": (
        "E1_decoder_performance",
        "E2_raw_vs_calibrated",
        "E2_calibration_reliability",
        "E6_ABCD",
        "E7_ablations",
        "E7_R1_robustness",
        "E7_R2_robustness",
        "E8_subject_wise_cross_subject",
        "E9_adaptation_trajectory",
        "D079_statistics",
        "failure_taxonomy",
    ),
    "figures": (
        "E2_calibration_reliability",
        "E7_R1_robustness",
        "E7_R2_robustness",
        "E9_adaptation_trajectory",
    ),
    "degenerate_figure_policy": "NOT_INFORMATIVE_with_machine_readable_table",
    "new_metrics_or_tests": False,
    "smoothing": False,
    "selective_plotting": False,
}
PROVENANCE_CORRECTION_PURPOSE = (
    "R03 final software-to-manifest provenance correction rerun; no tuning, model selection, "
    "metric selection, policy selection, refitting, or retraining"
)
FINAL_SPLIT_NAMES = frozenset({"final_test", "protected_final_test"})
FIT_SPLIT_NAMES = frozenset({"train", "training", "validation"})


class FinalContractError(ValueError):
    """Raised when final execution would violate a frozen scientific gate."""


@dataclass(frozen=True)
class ScenarioDefinition:
    scenario_id: str
    name: str
    rows: int
    columns: int
    start: tuple[int, int]
    goal_name: str
    goal: tuple[int, int]
    blocked_cells: tuple[tuple[int, int], ...]
    risk_cells: tuple[tuple[tuple[int, int], float], ...]
    replacement_start: tuple[int, int] | None = None
    replacement_blocked_cells: tuple[tuple[int, int], ...] = ()
    environment_change_event_id: str | None = None
    safety_probe_action: str | None = None
    inject_emergency_stop: bool = False
    expected_status: str | None = None


SCENARIOS: tuple[ScenarioDefinition, ...] = (
    ScenarioDefinition("S1", "Free-space route", 3, 4, (1, 0), "target", (0, 3), (), ()),
    ScenarioDefinition("S2", "Static obstacle", 3, 4, (1, 0), "target", (0, 3), ((1, 1),), ()),
    ScenarioDefinition(
        "S3",
        "Risk trade-off",
        3,
        5,
        (1, 0),
        "target",
        (1, 4),
        (),
        (((1, 1), 0.75), ((1, 2), 0.75), ((1, 3), 0.75)),
    ),
    ScenarioDefinition(
        "S4",
        "No safe path",
        3,
        3,
        (1, 0),
        "target",
        (1, 2),
        ((0, 1), (1, 1), (2, 1)),
        (),
        expected_status="NO_SAFE_PATH",
    ),
    ScenarioDefinition(
        "S5",
        "Dynamic blockage / replanning",
        3,
        5,
        (1, 0),
        "target",
        (1, 4),
        (),
        (),
        replacement_start=(1, 0),
        replacement_blocked_cells=((1, 1),),
        environment_change_event_id="s5-environment-change-0001",
        expected_status="SUCCESS",
    ),
    ScenarioDefinition(
        "S6",
        "Prohibited hazard",
        3,
        4,
        (1, 1),
        "target",
        (0, 3),
        (),
        (((1, 2), 1.0),),
        safety_probe_action="RIGHT",
        expected_status="REPLAN_REQUIRED",
    ),
    ScenarioDefinition(
        "S7",
        "Emergency stop",
        3,
        4,
        (1, 1),
        "target",
        (0, 3),
        (),
        (),
        inject_emergency_stop=True,
        expected_status="HALTED",
    ),
)


FULL_SYSTEM_MISSION_MAP: Mapping[str, Any] = {
    "rows": 3,
    "columns": 5,
    "start": (1, 0),
    "goals": {"victim_a": (1, 4), "victim_b": (0, 2)},
    "blocked_cells": (),
    "risk_cells": (),
    "candidate_order": ("victim_a", "victim_b"),
}


@dataclass(frozen=True)
class ArtifactRecord:
    artifact_id: str
    decoder_family: str
    artifact_type: str
    local_path: str
    sha256: str
    code_sha: str
    training_subject_ids: tuple[int, ...]
    validation_subject_ids: tuple[int, ...]
    fit_partition: str
    selection_rule: str
    seed: int | None
    configuration: Mapping[str, Any]

    def validate(self, split: D082CrossSubjectSplitManifest) -> None:
        for name in (
            "artifact_id",
            "decoder_family",
            "artifact_type",
            "local_path",
            "sha256",
            "code_sha",
            "fit_partition",
            "selection_rule",
        ):
            if not isinstance(getattr(self, name), str) or not getattr(self, name):
                raise FinalContractError(f"Artifact {name} must be a non-empty string.")
        if self.decoder_family not in {"csp_lda", "eegnet"}:
            raise FinalContractError("Artifact decoder_family must be csp_lda or eegnet.")
        if self.artifact_type not in {"decoder", "calibrator"}:
            raise FinalContractError("Artifact type must be decoder or calibrator.")
        if len(self.sha256) != 64 or any(character not in "0123456789abcdef" for character in self.sha256):
            raise FinalContractError("Artifact sha256 must be a lowercase SHA-256 digest.")
        train = set(self.training_subject_ids)
        validation = set(self.validation_subject_ids)
        final = set(split.final_test_subject_ids)
        if train != set(split.train_subject_ids) or validation != set(split.validation_subject_ids):
            raise FinalContractError("Artifact subject provenance must exactly match the frozen train/validation split.")
        if train & validation or train & final or validation & final:
            raise FinalContractError("Artifact fitting provenance contains subject leakage.")
        if self.artifact_type == "decoder" and self.fit_partition != "train_with_validation_selection":
            raise FinalContractError("Decoder artifacts require train fitting with validation-only selection.")
        if self.artifact_type == "calibrator" and self.fit_partition != "validation":
            raise FinalContractError("Calibrator artifacts must be fit on validation only.")
        if self.seed is not None and (isinstance(self.seed, bool) or not isinstance(self.seed, int) or self.seed < 0):
            raise FinalContractError("Artifact seed must be a non-negative integer when present.")
        _ensure_json_ready(asdict(self))


@dataclass(frozen=True)
class M7FinalExecutionManifest:
    manifest_version: str
    result_schema_version: str
    software_sha: str
    governance_sha: str
    qc_manifest_path: str
    qc_manifest_sha256: str
    actual_eligible_count: int
    excluded_subject_ids: tuple[int, ...]
    split_manifest_path: str
    split_manifest_sha256: str
    split_manifest: Mapping[str, Any]
    episode_manifest_path: str
    episode_manifest_sha256: str
    episode_manifest_version: str
    episode_source_table_sha256: str
    episode_count: int
    episode_construction: Mapping[str, Any]
    participation_manifest_path: str
    participation_manifest_sha256: str
    participation_manifest: Mapping[str, Any]
    artifacts: tuple[ArtifactRecord, ...]
    principal_conditions: Mapping[str, Any]
    ablations: Mapping[str, Any]
    ablation_semantics: Mapping[str, Any]
    r1_severities: tuple[float, ...]
    r2_severities: tuple[float, ...]
    r2_seed: int
    bootstrap_seed: int
    scenarios: tuple[ScenarioDefinition, ...]
    scenario_version: str
    full_system_mission_map: Mapping[str, Any]
    simulated_human_policy_id: str
    simulated_human_policy: Mapping[str, str]
    statistical_policy_ids: tuple[str, ...]
    experiment_families: tuple[str, ...]
    protected_access_status: str
    protected_data_prefetch_audit: Mapping[str, Any]
    policy_ids: tuple[str, ...]
    formal_comparison_set: tuple[str, ...]
    reporting_contract: Mapping[str, Any]
    execution_purpose: str

    def validate(self) -> D082CrossSubjectSplitManifest:
        if self.manifest_version != M7_EXECUTION_MANIFEST_VERSION:
            raise FinalContractError("Unexpected M7 final execution manifest version.")
        if self.result_schema_version != M7_RESULT_SCHEMA_VERSION:
            raise FinalContractError("Unexpected M7 final result schema version.")
        if not self.software_sha or not self.governance_sha:
            raise FinalContractError("Software and governance SHAs are required before final freeze.")
        if not self.qc_manifest_path or len(self.qc_manifest_sha256) != 64:
            raise FinalContractError("Frozen D-082 QC manifest path/hash is required.")
        if len(self.split_manifest_sha256) != 64:
            raise FinalContractError("Split manifest SHA-256 is required.")
        split = cross_subject_manifest_from_mapping(self.split_manifest)
        validate_cross_subject_split(split)
        if self.actual_eligible_count != split.actual_eligible_count:
            raise FinalContractError("Execution manifest actual eligible count differs from D-082 split.")
        if self.excluded_subject_ids != split.excluded_subject_ids:
            raise FinalContractError("Execution manifest excluded subjects differ from D-082 split.")
        if self.qc_manifest_sha256 != split.qc_manifest_sha256:
            raise FinalContractError("Execution manifest QC hash differs from D-082 split provenance.")
        if not self.episode_manifest_path or len(self.episode_manifest_sha256) != 64:
            raise FinalContractError("A frozen D-081 episode manifest path/hash is required.")
        if self.episode_manifest_version != D081_EPISODE_MANIFEST_VERSION:
            raise FinalContractError("Final manifest must include the D-081 episode-manifest version.")
        if len(self.episode_source_table_sha256) != 64 or self.episode_count <= 0:
            raise FinalContractError("D-081 episode source hash/count must be frozen before final access.")
        expected_episode_contract = {
            "grouping_key": D081_GROUPING_KEY,
            "ordering_rule": D081_ORDERING_RULE,
            "block_size": 5,
            "overlap": False,
            "source_trial_reuse": False,
            "incomplete_tail_policy": "exclude_record_and_retain_for_e1_e2",
            "ab_first_observation_rule": "A_and_B_use_source_position_1",
            "cd_source_order_rule": "C_and_D_receive_positions_1_through_5_in_frozen_order",
            "e9_ordering_rule": D081_E9_ORDERING_RULE,
        }
        if _plain(self.episode_construction) != _plain(expected_episode_contract):
            raise FinalContractError("D-081 episode construction fields changed.")
        if not self.participation_manifest_path or len(self.participation_manifest_sha256) != 64:
            raise FinalContractError("A frozen D-083 participation manifest path/hash is required.")
        participation = sequential_participation_manifest_from_mapping(self.participation_manifest)
        validate_sequential_participation_manifest(participation)
        if participation.split_manifest_sha256 != self.split_manifest_sha256:
            raise FinalContractError("D-083 participation is not bound to the frozen D-082 split.")
        if participation.frozen_partition_subject_ids != split.final_test_subject_ids:
            raise FinalContractError("D-083 participation does not preserve the frozen final partition.")
        if self.r1_severities != R1_SEVERITIES or self.r2_severities != R2_SEVERITIES:
            raise FinalContractError("Robustness severities must match D-078 exactly.")
        if self.r2_seed != OPERATIONAL_SEED or self.bootstrap_seed != OPERATIONAL_SEED:
            raise FinalContractError("M7-T02 R2 and bootstrap seeds must both equal 42.")
        if self.scenarios != SCENARIOS or self.scenario_version != M7_SCENARIO_VERSION:
            raise FinalContractError("Scenario suite must match frozen S1-S7 exactly.")
        if _plain(self.full_system_mission_map) != _plain(FULL_SYSTEM_MISSION_MAP):
            raise FinalContractError("Full-system mission map or candidate order changed.")
        if self.simulated_human_policy_id != SIMULATED_HUMAN_POLICY_ID:
            raise FinalContractError("Unexpected simulated-human policy identifier.")
        if self.experiment_families != EXPECTED_EXPERIMENT_FAMILIES:
            raise FinalContractError("Final manifest must list E1 through E9 exactly.")
        if self.statistical_policy_ids != ("D-079", "D-080", "D-081", "D-082", "D-083", "D-084"):
            raise FinalContractError("Final manifest must preserve D-079 through D-084 execution policy IDs.")
        if self.policy_ids != EXPECTED_POLICY_IDS:
            raise FinalContractError("Final manifest must bind D-077 through D-084 exactly.")
        if self.formal_comparison_set != FORMAL_COMPARISON_SET:
            raise FinalContractError("Final manifest formal comparison set changed.")
        if _plain(self.reporting_contract) != _plain(FINAL_REPORTING_CONTRACT):
            raise FinalContractError("Final manifest reporting contract changed.")
        if self.execution_purpose != PROVENANCE_CORRECTION_PURPOSE:
            raise FinalContractError("Final manifest must identify the provenance-correction rerun purpose.")
        if self.protected_access_status != "NOT_ACCESSED_AT_FREEZE":
            raise FinalContractError("The manifest must be frozen before protected outcomes are accessed.")
        if self.protected_data_prefetch_audit.get("classification") != "protected_data_prefetch_not_outcome_access":
            raise FinalContractError("D-081 protected-data-prefetch audit is required.")
        if self.protected_data_prefetch_audit.get("protected_outcomes_observed") is not False:
            raise FinalContractError("Prefetch audit must state that no protected outcome was observed.")
        if set(self.principal_conditions) != {"A", "B", "C", "D"}:
            raise FinalContractError("The final manifest must contain the exact A/B/C/D registry.")
        if set(self.ablations) != set(ABLATIONS):
            raise FinalContractError("The final manifest must contain the exact approved ablation registry.")
        if _plain(self.ablation_semantics) != _plain(D084_ABLATION_SEMANTICS):
            raise FinalContractError("Final manifest must preserve D-084 ablation execution semantics exactly.")
        artifact_keys = {(item.decoder_family, item.artifact_type) for item in self.artifacts}
        expected_artifacts = {
            ("csp_lda", "decoder"),
            ("csp_lda", "calibrator"),
            ("eegnet", "decoder"),
            ("eegnet", "calibrator"),
        }
        if artifact_keys != expected_artifacts or len(self.artifacts) != len(expected_artifacts):
            raise FinalContractError("Exactly one frozen decoder and calibrator are required per decoder family.")
        for artifact in self.artifacts:
            artifact.validate(split)
        _ensure_json_ready(manifest_to_mapping(self))
        return split


@dataclass(frozen=True)
class FinalAccessAuthorization:
    manifest_path: str
    manifest_sha256: str
    split_manifest_sha256: str
    episode_manifest_sha256: str
    participation_manifest_sha256: str
    governance_sha: str
    software_sha: str
    final_subject_ids: tuple[int, ...]


def canonical_qc_manifest():
    """Build a complete all-109 D-082 QC fixture without hard-coded split membership."""
    records = tuple(
        SubjectEligibilityRecord(
            subject_id=subject_id,
            requested_runs=(4, 8, 12),
            loaded_runs=(4, 8, 12),
            raw_t1_count=3,
            raw_t2_count=3,
            candidate_binary_epochs=6,
            retained_t1_count=3,
            retained_t2_count=3,
            rejected_epoch_count=0,
            rejection_reasons={},
            eligible=True,
            exclusion_reason=None,
            within_subject_feasible=True,
            within_subject_infeasibility_reason=None,
            source_files=(f"S{subject_id:03d}.edf",),
            source_sha256=("0" * 64,),
        )
        for subject_id in SOURCE_SUBJECT_IDS
    )
    return build_qc_manifest(
        records,
        dataset_id="test-fixture",
        dataset_source="test-fixture",
        generating_code_sha="test-fixture",
        reject_threshold_uv=150.0,
    )


def canonical_cross_subject_manifest(*, qc_manifest_file_sha256: str | None = None) -> D082CrossSubjectSplitManifest:
    """Build the historical all-109 case through the D-082 algorithm (test helper)."""

    return build_split_manifest(
        canonical_qc_manifest(),
        generating_code_sha="test-fixture",
        qc_manifest_file_sha256=qc_manifest_file_sha256,
    )


def validate_cross_subject_split(manifest: D082CrossSubjectSplitManifest) -> None:
    try:
        validate_split_manifest(manifest)
    except ValueError as exc:
        raise FinalContractError(str(exc)) from exc


def validate_fit_subjects(
    subject_ids: Sequence[int],
    *,
    split_name: str,
    split_manifest: D082CrossSubjectSplitManifest,
) -> tuple[int, ...]:
    """Fail closed if any fitting hook could consume protected final subjects."""

    validate_cross_subject_split(split_manifest)
    normalized = tuple(int(subject_id) for subject_id in subject_ids)
    if not normalized or len(set(normalized)) != len(normalized):
        raise FinalContractError("Fitting subject IDs must be non-empty and unique.")
    split_name = str(split_name).lower()
    if split_name not in FIT_SPLIT_NAMES:
        raise FinalContractError("Fitting hooks accept only frozen train or validation subjects.")
    expected = (
        set(split_manifest.train_subject_ids)
        if split_name in {"train", "training"}
        else set(split_manifest.validation_subject_ids)
    )
    if set(normalized) != expected:
        raise FinalContractError("Fitting subject IDs must exactly match their declared frozen partition.")
    if set(normalized) & set(split_manifest.final_test_subject_ids):
        raise FinalContractError("Protected final subjects cannot participate in fitting or selection.")
    return normalized


def build_final_manifest(
    *,
    software_sha: str,
    governance_sha: str,
    qc_manifest_path: str,
    qc_manifest_sha256: str,
    split_manifest_path: str,
    split_manifest_sha256: str,
    split_manifest: D082CrossSubjectSplitManifest,
    episode_manifest_path: str,
    episode_manifest_sha256: str,
    episode_manifest: EpisodeManifest,
    participation_manifest_path: str,
    participation_manifest_sha256: str,
    participation_manifest: SequentialParticipationManifest,
    artifacts: Sequence[ArtifactRecord],
) -> M7FinalExecutionManifest:
    validate_cross_subject_split(split_manifest)
    validate_episode_manifest(episode_manifest)
    validate_sequential_participation_manifest(participation_manifest)
    return M7FinalExecutionManifest(
        manifest_version=M7_EXECUTION_MANIFEST_VERSION,
        result_schema_version=M7_RESULT_SCHEMA_VERSION,
        software_sha=software_sha,
        governance_sha=governance_sha,
        qc_manifest_path=qc_manifest_path,
        qc_manifest_sha256=qc_manifest_sha256,
        actual_eligible_count=split_manifest.actual_eligible_count,
        excluded_subject_ids=split_manifest.excluded_subject_ids,
        split_manifest_path=split_manifest_path,
        split_manifest_sha256=split_manifest_sha256,
        split_manifest=asdict(split_manifest),
        episode_manifest_path=episode_manifest_path,
        episode_manifest_sha256=episode_manifest_sha256,
        episode_manifest_version=episode_manifest.manifest_version,
        episode_source_table_sha256=episode_manifest.source_table_sha256,
        episode_count=episode_manifest.episode_count,
        episode_construction={
            "grouping_key": episode_manifest.grouping_key,
            "ordering_rule": episode_manifest.ordering_rule,
            "block_size": episode_manifest.block_size,
            "overlap": episode_manifest.overlap,
            "source_trial_reuse": episode_manifest.source_trial_reuse,
            "incomplete_tail_policy": episode_manifest.incomplete_tail_policy,
            "ab_first_observation_rule": episode_manifest.ab_first_observation_rule,
            "cd_source_order_rule": episode_manifest.cd_source_order_rule,
            "e9_ordering_rule": episode_manifest.e9_ordering_rule,
        },
        participation_manifest_path=participation_manifest_path,
        participation_manifest_sha256=participation_manifest_sha256,
        participation_manifest=asdict(participation_manifest),
        artifacts=tuple(artifacts),
        principal_conditions={key.value: asdict(value) for key, value in PRINCIPAL_CONDITIONS.items()},
        ablations={key: asdict(value) for key, value in ABLATIONS.items()},
        ablation_semantics={key: dict(value) for key, value in D084_ABLATION_SEMANTICS.items()},
        r1_severities=R1_SEVERITIES,
        r2_severities=R2_SEVERITIES,
        r2_seed=OPERATIONAL_SEED,
        bootstrap_seed=OPERATIONAL_SEED,
        scenarios=SCENARIOS,
        scenario_version=M7_SCENARIO_VERSION,
        full_system_mission_map=FULL_SYSTEM_MISSION_MAP,
        simulated_human_policy_id=SIMULATED_HUMAN_POLICY_ID,
        simulated_human_policy={
            "PROCEED": "no_command",
            "CONFIRM_correct": "explicit_confirm",
            "CONFIRM_wrong": "explicit_override_to_intended_goal",
            "DEFER": "explicit_override_to_intended_goal",
            "PAUSE_STOP": "dedicated_controlled_scenarios_only",
            "interpretation": "simulated human / offline software evaluation",
        },
        statistical_policy_ids=("D-079", "D-080", "D-081", "D-082", "D-083", "D-084"),
        experiment_families=EXPECTED_EXPERIMENT_FAMILIES,
        protected_access_status="NOT_ACCESSED_AT_FREEZE",
        protected_data_prefetch_audit={
            "classification": "protected_data_prefetch_not_outcome_access",
            "reviewed_by": "Project Owner",
            "policy_id": "D-081",
            "first_disclosed_prefetch_file": "S002R04.edf",
            "first_disclosed_prefetch_timestamp_utc": "2026-09-13T09:02:12.6108033Z",
            "disclosed_subjects": (2, 3, 87, 88),
            "subject_88_disclosed_runs": (4, 8),
            "protected_outcomes_observed": False,
            "selection_or_tuning_from_prefetch": False,
        },
        policy_ids=EXPECTED_POLICY_IDS,
        formal_comparison_set=FORMAL_COMPARISON_SET,
        reporting_contract=FINAL_REPORTING_CONTRACT,
        execution_purpose=PROVENANCE_CORRECTION_PURPOSE,
    )


def write_cross_subject_manifest(manifest: D082CrossSubjectSplitManifest, path: str | Path) -> str:
    validate_cross_subject_split(manifest)
    return write_immutable_json(asdict(manifest), path)


def freeze_final_manifest(manifest: M7FinalExecutionManifest, path: str | Path) -> str:
    manifest.validate()
    return write_immutable_json(manifest_to_mapping(manifest), path)


def authorize_final_access(path: str | Path) -> FinalAccessAuthorization:
    manifest_path = Path(path).resolve()
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest = manifest_from_mapping(payload)
    split = manifest.validate()
    expected_hash = sha256_file(manifest_path)
    split_path = Path(manifest.split_manifest_path)
    if not split_path.is_absolute():
        split_path = (manifest_path.parent / split_path).resolve()
    if sha256_file(split_path) != manifest.split_manifest_sha256:
        raise FinalContractError("Frozen split manifest file/hash verification failed.")
    qc_path = Path(manifest.qc_manifest_path)
    if not qc_path.is_absolute():
        qc_path = (manifest_path.parent / qc_path).resolve()
    if sha256_file(qc_path) != manifest.qc_manifest_sha256:
        raise FinalContractError("Frozen D-082 QC manifest file/hash verification failed.")
    try:
        qc_manifest = qc_manifest_from_mapping(json.loads(qc_path.read_text(encoding="utf-8")))
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise FinalContractError("Frozen D-082 QC manifest content verification failed.") from exc
    if (
        qc_manifest.actual_eligible_count != split.actual_eligible_count
        or qc_manifest.eligible_subject_ids != split.eligible_subject_ids
        or qc_manifest.excluded_subject_ids != split.excluded_subject_ids
        or dict(qc_manifest.excluded_subject_reasons) != dict(split.excluded_subject_reasons)
    ):
        raise FinalContractError("Frozen D-082 QC and split manifests disagree.")
    episode_path = Path(manifest.episode_manifest_path)
    if not episode_path.is_absolute():
        episode_path = (manifest_path.parent / episode_path).resolve()
    if sha256_file(episode_path) != manifest.episode_manifest_sha256:
        raise FinalContractError("Frozen D-081 episode manifest file/hash verification failed.")
    episode_manifest = load_episode_manifest(episode_path)
    if (
        episode_manifest.manifest_version != manifest.episode_manifest_version
        or episode_manifest.source_table_sha256 != manifest.episode_source_table_sha256
        or episode_manifest.episode_count != manifest.episode_count
    ):
        raise FinalContractError("Final manifest does not match the frozen D-081 episode manifest.")
    participation_path = Path(manifest.participation_manifest_path)
    if not participation_path.is_absolute():
        participation_path = (manifest_path.parent / participation_path).resolve()
    if sha256_file(participation_path) != manifest.participation_manifest_sha256:
        raise FinalContractError("Frozen D-083 participation manifest file/hash verification failed.")
    participation = sequential_participation_manifest_from_mapping(
        json.loads(participation_path.read_text(encoding="utf-8"))
    )
    validate_sequential_participation_manifest(participation)
    if _plain(asdict(participation)) != _plain(manifest.participation_manifest):
        raise FinalContractError("Final manifest does not match the frozen D-083 participation manifest.")
    for artifact in manifest.artifacts:
        artifact_path = Path(artifact.local_path)
        if not artifact_path.is_absolute():
            artifact_path = (manifest_path.parent / artifact_path).resolve()
        if sha256_file(artifact_path) != artifact.sha256:
            raise FinalContractError(f"Frozen artifact hash verification failed: {artifact.artifact_id}.")
    return FinalAccessAuthorization(
        manifest_path=str(manifest_path),
        manifest_sha256=expected_hash,
        split_manifest_sha256=manifest.split_manifest_sha256,
        episode_manifest_sha256=manifest.episode_manifest_sha256,
        participation_manifest_sha256=manifest.participation_manifest_sha256,
        governance_sha=manifest.governance_sha,
        software_sha=manifest.software_sha,
        final_subject_ids=split.final_test_subject_ids,
    )


def require_final_subject(subject_id: int, authorization: FinalAccessAuthorization) -> None:
    if not isinstance(authorization, FinalAccessAuthorization):
        raise FinalContractError("Protected final access requires a verified frozen-manifest authorization.")
    if int(subject_id) not in authorization.final_subject_ids:
        raise FinalContractError("Requested subject is not in the frozen protected final cohort.")


def write_immutable_json(payload: Mapping[str, Any], path: str | Path) -> str:
    destination = Path(path).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = canonical_json(payload) + "\n"
    if destination.exists():
        existing = destination.read_text(encoding="utf-8")
        if existing != text:
            raise FinalContractError(f"Frozen manifest already exists with different content: {destination}.")
    else:
        destination.write_text(text, encoding="utf-8", newline="\n")
    return sha256_file(destination)


def canonical_json(payload: Mapping[str, Any]) -> str:
    _ensure_json_ready(payload)
    return json.dumps(_plain(payload), sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_file(path: str | Path) -> str:
    digest = sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_to_mapping(manifest: M7FinalExecutionManifest) -> dict[str, Any]:
    return _plain(asdict(manifest))


def cross_subject_manifest_from_mapping(payload: Mapping[str, Any]) -> D082CrossSubjectSplitManifest:
    try:
        return split_manifest_from_mapping(payload)
    except ValueError as exc:
        raise FinalContractError(str(exc)) from exc


def manifest_from_mapping(payload: Mapping[str, Any]) -> M7FinalExecutionManifest:
    return M7FinalExecutionManifest(
        manifest_version=str(payload["manifest_version"]),
        result_schema_version=str(payload["result_schema_version"]),
        software_sha=str(payload["software_sha"]),
        governance_sha=str(payload["governance_sha"]),
        qc_manifest_path=str(payload["qc_manifest_path"]),
        qc_manifest_sha256=str(payload["qc_manifest_sha256"]),
        actual_eligible_count=int(payload["actual_eligible_count"]),
        excluded_subject_ids=tuple(int(value) for value in payload["excluded_subject_ids"]),
        split_manifest_path=str(payload["split_manifest_path"]),
        split_manifest_sha256=str(payload["split_manifest_sha256"]),
        split_manifest=dict(payload["split_manifest"]),
        episode_manifest_path=str(payload["episode_manifest_path"]),
        episode_manifest_sha256=str(payload["episode_manifest_sha256"]),
        episode_manifest_version=str(payload["episode_manifest_version"]),
        episode_source_table_sha256=str(payload["episode_source_table_sha256"]),
        episode_count=int(payload["episode_count"]),
        episode_construction=dict(payload["episode_construction"]),
        participation_manifest_path=str(payload["participation_manifest_path"]),
        participation_manifest_sha256=str(payload["participation_manifest_sha256"]),
        participation_manifest=dict(payload["participation_manifest"]),
        artifacts=tuple(
            ArtifactRecord(
                artifact_id=str(item["artifact_id"]),
                decoder_family=str(item["decoder_family"]),
                artifact_type=str(item["artifact_type"]),
                local_path=str(item["local_path"]),
                sha256=str(item["sha256"]),
                code_sha=str(item["code_sha"]),
                training_subject_ids=tuple(int(value) for value in item["training_subject_ids"]),
                validation_subject_ids=tuple(int(value) for value in item["validation_subject_ids"]),
                fit_partition=str(item["fit_partition"]),
                selection_rule=str(item["selection_rule"]),
                seed=None if item["seed"] is None else int(item["seed"]),
                configuration=dict(item["configuration"]),
            )
            for item in payload["artifacts"]
        ),
        principal_conditions=dict(payload["principal_conditions"]),
        ablations=dict(payload["ablations"]),
        ablation_semantics=dict(payload["ablation_semantics"]),
        r1_severities=tuple(float(value) for value in payload["r1_severities"]),
        r2_severities=tuple(float(value) for value in payload["r2_severities"]),
        r2_seed=int(payload["r2_seed"]),
        bootstrap_seed=int(payload["bootstrap_seed"]),
        scenarios=tuple(_scenario_from_mapping(item) for item in payload["scenarios"]),
        scenario_version=str(payload["scenario_version"]),
        full_system_mission_map=dict(payload["full_system_mission_map"]),
        simulated_human_policy_id=str(payload["simulated_human_policy_id"]),
        simulated_human_policy=dict(payload["simulated_human_policy"]),
        statistical_policy_ids=tuple(str(value) for value in payload["statistical_policy_ids"]),
        experiment_families=tuple(str(value) for value in payload["experiment_families"]),
        protected_access_status=str(payload["protected_access_status"]),
        protected_data_prefetch_audit=dict(payload["protected_data_prefetch_audit"]),
        policy_ids=tuple(str(value) for value in payload.get("policy_ids", ())),
        formal_comparison_set=tuple(str(value) for value in payload.get("formal_comparison_set", ())),
        reporting_contract=dict(payload.get("reporting_contract", {})),
        execution_purpose=str(payload.get("execution_purpose", "")),
    )


def _scenario_from_mapping(payload: Mapping[str, Any]) -> ScenarioDefinition:
    coordinate = lambda value: None if value is None else (int(value[0]), int(value[1]))
    return ScenarioDefinition(
        scenario_id=str(payload["scenario_id"]),
        name=str(payload["name"]),
        rows=int(payload["rows"]),
        columns=int(payload["columns"]),
        start=coordinate(payload["start"]),  # type: ignore[arg-type]
        goal_name=str(payload["goal_name"]),
        goal=coordinate(payload["goal"]),  # type: ignore[arg-type]
        blocked_cells=tuple(coordinate(value) for value in payload["blocked_cells"]),  # type: ignore[arg-type]
        risk_cells=tuple(
            (coordinate(value[0]), float(value[1])) for value in payload["risk_cells"]
        ),  # type: ignore[arg-type]
        replacement_start=coordinate(payload["replacement_start"]),
        replacement_blocked_cells=tuple(
            coordinate(value) for value in payload["replacement_blocked_cells"]
        ),  # type: ignore[arg-type]
        environment_change_event_id=(
            None if payload["environment_change_event_id"] is None else str(payload["environment_change_event_id"])
        ),
        safety_probe_action=None if payload["safety_probe_action"] is None else str(payload["safety_probe_action"]),
        inject_emergency_stop=bool(payload["inject_emergency_stop"]),
        expected_status=None if payload["expected_status"] is None else str(payload["expected_status"]),
    )


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    return value


def _ensure_json_ready(value: Any) -> None:
    try:
        json.dumps(_plain(value), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise FinalContractError("Final manifest fields must be finite and JSON serializable.") from exc
