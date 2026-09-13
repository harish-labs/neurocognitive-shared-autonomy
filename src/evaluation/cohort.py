"""D-082 post-QC cohort and deterministic cross-subject allocation manifests."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
from math import floor
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


SOURCE_SUBJECT_IDS = tuple(range(1, 110))
SOURCE_POPULATION_COUNT = 109
D082_SPLIT_SEED = 42
D082_QC_MANIFEST_VERSION = "m7-d082-qc-eligibility-v1"
D082_SPLIT_MANIFEST_VERSION = "m7-d082-cross-subject-v1"
D082_SHUFFLE_METHOD = "pandas.Series.sample(frac=1.0, random_state=42) after ascending sort"
D082_ALLOCATION_METHOD = "floor_quotas_then_largest_fractional_remainder"
D082_TIE_BREAK_ORDER = ("final_test", "validation", "train")
D082_PARTITION_PROPORTIONS = {"train": 0.70, "validation": 0.15, "final_test": 0.15}
D082_POLICY_IDS = ("D-035", "D-040", "D-041", "D-042", "D-082", "D-083")


class CohortManifestError(ValueError):
    """Raised when a D-082 cohort or split contract is violated."""


@dataclass(frozen=True)
class SubjectEligibilityRecord:
    subject_id: int
    requested_runs: tuple[int, ...]
    loaded_runs: tuple[int, ...]
    raw_t1_count: int
    raw_t2_count: int
    candidate_binary_epochs: int
    retained_t1_count: int
    retained_t2_count: int
    rejected_epoch_count: int
    rejection_reasons: Mapping[str, int]
    eligible: bool
    exclusion_reason: str | None
    within_subject_feasible: bool
    within_subject_infeasibility_reason: str | None
    source_files: tuple[str, ...]
    source_sha256: tuple[str, ...]


@dataclass(frozen=True)
class QCEligibilityManifest:
    manifest_version: str
    source_population_count: int
    source_subject_ids: tuple[int, ...]
    dataset_id: str
    dataset_source: str
    preprocessing_qc_policy_ids: tuple[str, ...]
    reject_threshold_uv: float
    no_ica: bool
    no_automatic_interpolation: bool
    eligibility_rule: str
    generating_code_sha: str
    subjects: tuple[SubjectEligibilityRecord, ...]
    eligible_subject_ids: tuple[int, ...]
    excluded_subject_ids: tuple[int, ...]
    excluded_subject_reasons: Mapping[str, str]
    actual_eligible_count: int
    excluded_count: int
    manifest_sha256: str


@dataclass(frozen=True)
class D082CrossSubjectSplitManifest:
    manifest_version: str
    policy_ids: tuple[str, ...]
    source_population_count: int
    actual_eligible_count: int
    eligible_subject_ids: tuple[int, ...]
    excluded_subject_ids: tuple[int, ...]
    excluded_subject_reasons: Mapping[str, str]
    qc_manifest_sha256: str
    split_seed: int
    shuffle_method: str
    shuffled_eligible_subject_ids: tuple[int, ...]
    allocation_method: str
    tie_break_order: tuple[str, ...]
    ideal_quotas: Mapping[str, float]
    floor_counts: Mapping[str, int]
    fractional_remainders: Mapping[str, float]
    partition_counts: Mapping[str, int]
    train_subject_ids: tuple[int, ...]
    validation_subject_ids: tuple[int, ...]
    final_test_subject_ids: tuple[int, ...]
    protected_final_test_subject_ids: tuple[int, ...]
    generating_code_sha: str
    manifest_sha256: str


def allocation_counts(n_subjects: int) -> tuple[dict[str, float], dict[str, int], dict[str, float], dict[str, int]]:
    if isinstance(n_subjects, bool) or not isinstance(n_subjects, int) or n_subjects <= 0:
        raise CohortManifestError("Eligible subject count must be a positive integer.")
    ideals = {name: proportion * n_subjects for name, proportion in D082_PARTITION_PROPORTIONS.items()}
    floors = {name: floor(value) for name, value in ideals.items()}
    remainders = {name: ideals[name] - floors[name] for name in ideals}
    counts = dict(floors)
    remaining = n_subjects - sum(counts.values())
    tie_rank = {name: index for index, name in enumerate(D082_TIE_BREAK_ORDER)}
    order = sorted(counts, key=lambda name: (-remainders[name], tie_rank[name]))
    for name in order[:remaining]:
        counts[name] += 1
    if sum(counts.values()) != n_subjects:
        raise CohortManifestError("Largest-remainder allocation did not consume the eligible cohort.")
    return ideals, floors, remainders, counts


def build_split_manifest(
    qc_manifest: QCEligibilityManifest,
    *,
    generating_code_sha: str,
    qc_manifest_file_sha256: str | None = None,
    split_seed: int = D082_SPLIT_SEED,
) -> D082CrossSubjectSplitManifest:
    validate_qc_manifest(qc_manifest)
    if split_seed != D082_SPLIT_SEED:
        raise CohortManifestError("D-082 requires split seed 42.")
    eligible = tuple(sorted(qc_manifest.eligible_subject_ids))
    shuffled = tuple(
        int(value)
        for value in pd.Series(eligible, dtype=int).sample(frac=1.0, random_state=split_seed).tolist()
    )
    ideals, floors, remainders, counts = allocation_counts(len(eligible))
    train_stop = counts["train"]
    validation_stop = train_stop + counts["validation"]
    manifest = D082CrossSubjectSplitManifest(
        manifest_version=D082_SPLIT_MANIFEST_VERSION,
        policy_ids=D082_POLICY_IDS,
        source_population_count=SOURCE_POPULATION_COUNT,
        actual_eligible_count=len(eligible),
        eligible_subject_ids=eligible,
        excluded_subject_ids=qc_manifest.excluded_subject_ids,
        excluded_subject_reasons=dict(qc_manifest.excluded_subject_reasons),
        qc_manifest_sha256=(qc_manifest.manifest_sha256 if qc_manifest_file_sha256 is None else _sha256_text(qc_manifest_file_sha256, "qc_manifest_file_sha256")),
        split_seed=split_seed,
        shuffle_method=D082_SHUFFLE_METHOD,
        shuffled_eligible_subject_ids=shuffled,
        allocation_method=D082_ALLOCATION_METHOD,
        tie_break_order=D082_TIE_BREAK_ORDER,
        ideal_quotas=ideals,
        floor_counts=floors,
        fractional_remainders=remainders,
        partition_counts=counts,
        train_subject_ids=shuffled[:train_stop],
        validation_subject_ids=shuffled[train_stop:validation_stop],
        final_test_subject_ids=shuffled[validation_stop:],
        protected_final_test_subject_ids=shuffled[validation_stop:],
        generating_code_sha=_required_text(generating_code_sha, "generating_code_sha"),
        manifest_sha256="",
    )
    manifest = replace(manifest, manifest_sha256=_content_hash(asdict(manifest)))
    validate_split_manifest(manifest)
    return manifest


def build_qc_manifest(
    records: Sequence[SubjectEligibilityRecord],
    *,
    dataset_id: str,
    dataset_source: str,
    generating_code_sha: str,
    reject_threshold_uv: float,
) -> QCEligibilityManifest:
    ordered = tuple(sorted(records, key=lambda item: item.subject_id))
    if tuple(item.subject_id for item in ordered) != SOURCE_SUBJECT_IDS:
        raise CohortManifestError("QC manifest must contain each source subject 1..109 exactly once.")
    eligible = tuple(item.subject_id for item in ordered if item.eligible)
    excluded = tuple(item.subject_id for item in ordered if not item.eligible)
    reasons = {str(item.subject_id): str(item.exclusion_reason) for item in ordered if not item.eligible}
    manifest = QCEligibilityManifest(
        manifest_version=D082_QC_MANIFEST_VERSION,
        source_population_count=SOURCE_POPULATION_COUNT,
        source_subject_ids=SOURCE_SUBJECT_IDS,
        dataset_id=_required_text(dataset_id, "dataset_id"),
        dataset_source=_required_text(dataset_source, "dataset_source"),
        preprocessing_qc_policy_ids=("D-031", "D-032", "D-033", "D-034", "D-035", "D-036", "D-037", "D-038", "D-039", "D-082", "D-083"),
        reject_threshold_uv=float(reject_threshold_uv),
        no_ica=True,
        no_automatic_interpolation=True,
        eligibility_rule="D-083: retained_t1_count>=1 AND retained_t2_count>=1; QC counts only",
        generating_code_sha=_required_text(generating_code_sha, "generating_code_sha"),
        subjects=ordered,
        eligible_subject_ids=eligible,
        excluded_subject_ids=excluded,
        excluded_subject_reasons=reasons,
        actual_eligible_count=len(eligible),
        excluded_count=len(excluded),
        manifest_sha256="",
    )
    manifest = replace(manifest, manifest_sha256=_content_hash(asdict(manifest)))
    validate_qc_manifest(manifest)
    return manifest


def validate_qc_manifest(manifest: QCEligibilityManifest) -> None:
    if not isinstance(manifest, QCEligibilityManifest) or manifest.manifest_version != D082_QC_MANIFEST_VERSION:
        raise CohortManifestError("Unexpected D-082 QC manifest type/version.")
    if manifest.source_population_count != SOURCE_POPULATION_COUNT or manifest.source_subject_ids != SOURCE_SUBJECT_IDS:
        raise CohortManifestError("D-082 QC source population must be subjects 1..109.")
    if manifest.reject_threshold_uv != 150.0 or not manifest.no_ica or not manifest.no_automatic_interpolation:
        raise CohortManifestError("D-035 QC policy changed; 150 µV/no-ICA/no-interpolation is required.")
    ids = tuple(item.subject_id for item in manifest.subjects)
    if ids != SOURCE_SUBJECT_IDS:
        raise CohortManifestError("QC records must be sorted and complete for subjects 1..109.")
    for item in manifest.subjects:
        if item.eligible != (item.retained_t1_count > 0 and item.retained_t2_count > 0):
            raise CohortManifestError("D-083 eligibility requires at least one retained trial in each class.")
        expected_within = item.retained_t1_count >= 3 and item.retained_t2_count >= 3
        if item.within_subject_feasible != expected_within:
            raise CohortManifestError("D-040 within-subject feasibility must be tracked separately at three trials per class.")
        if expected_within != (item.within_subject_infeasibility_reason is None):
            raise CohortManifestError("Within-subject feasibility reason is inconsistent.")
        if item.eligible and item.exclusion_reason is not None:
            raise CohortManifestError("Eligible subjects cannot have exclusion reasons.")
        if not item.eligible and not item.exclusion_reason:
            raise CohortManifestError("Excluded subjects require an exact reason.")
        if item.candidate_binary_epochs != item.raw_t1_count + item.raw_t2_count:
            raise CohortManifestError("Candidate count must equal raw T1 plus raw T2 counts.")
        if item.candidate_binary_epochs != item.retained_t1_count + item.retained_t2_count + item.rejected_epoch_count:
            raise CohortManifestError("Retained and rejected counts must reconcile to candidates.")
    if manifest.actual_eligible_count != len(manifest.eligible_subject_ids):
        raise CohortManifestError("Actual eligible count is inconsistent.")
    if manifest.excluded_count != len(manifest.excluded_subject_ids):
        raise CohortManifestError("Excluded count is inconsistent.")
    if set(manifest.eligible_subject_ids) | set(manifest.excluded_subject_ids) != set(SOURCE_SUBJECT_IDS):
        raise CohortManifestError("Eligible and excluded subjects must exhaust the source population.")
    _verify_hash(asdict(manifest), manifest.manifest_sha256, "QC")


def validate_split_manifest(manifest: D082CrossSubjectSplitManifest) -> None:
    if not isinstance(manifest, D082CrossSubjectSplitManifest) or manifest.manifest_version != D082_SPLIT_MANIFEST_VERSION:
        raise CohortManifestError("Unexpected D-082 split manifest type/version.")
    if manifest.policy_ids != D082_POLICY_IDS or manifest.source_population_count != SOURCE_POPULATION_COUNT:
        raise CohortManifestError("Split manifest policy/source identifiers changed.")
    if manifest.split_seed != D082_SPLIT_SEED or manifest.shuffle_method != D082_SHUFFLE_METHOD:
        raise CohortManifestError("D-082 seed/shuffle method changed.")
    if manifest.allocation_method != D082_ALLOCATION_METHOD or manifest.tie_break_order != D082_TIE_BREAK_ORDER:
        raise CohortManifestError("D-082 allocation or tie-break rule changed.")
    eligible = set(manifest.eligible_subject_ids)
    excluded = set(manifest.excluded_subject_ids)
    partitions = (set(manifest.train_subject_ids), set(manifest.validation_subject_ids), set(manifest.final_test_subject_ids))
    if any(partitions[i] & partitions[j] for i in range(3) for j in range(i + 1, 3)):
        raise CohortManifestError("D-082 partitions overlap.")
    if set().union(*partitions) != eligible or excluded & set().union(*partitions):
        raise CohortManifestError("D-082 partitions must exhaust eligible subjects and exclude ineligible subjects.")
    if eligible & excluded or eligible | excluded != set(SOURCE_SUBJECT_IDS):
        raise CohortManifestError("Eligible/excluded split does not exhaust the 109-source population.")
    if manifest.actual_eligible_count != len(eligible) or dict(manifest.partition_counts) != {
        "train": len(manifest.train_subject_ids),
        "validation": len(manifest.validation_subject_ids),
        "final_test": len(manifest.final_test_subject_ids),
    }:
        raise CohortManifestError("D-082 counts are inconsistent with subject membership.")
    ideals, floors, remainders, counts = allocation_counts(len(eligible))
    if dict(manifest.ideal_quotas) != ideals or dict(manifest.floor_counts) != floors or dict(manifest.fractional_remainders) != remainders or dict(manifest.partition_counts) != counts:
        raise CohortManifestError("D-082 quota/allocation calculations changed.")
    expected_shuffle = tuple(int(value) for value in pd.Series(tuple(sorted(eligible)), dtype=int).sample(frac=1.0, random_state=42).tolist())
    if manifest.shuffled_eligible_subject_ids != expected_shuffle:
        raise CohortManifestError("D-082 shuffled identity sequence is not reproducible.")
    train_stop = counts["train"]
    validation_stop = train_stop + counts["validation"]
    if manifest.train_subject_ids != expected_shuffle[:train_stop] or manifest.validation_subject_ids != expected_shuffle[train_stop:validation_stop] or manifest.final_test_subject_ids != expected_shuffle[validation_stop:]:
        raise CohortManifestError("Partitions are not contiguous blocks of the single D-082 shuffle.")
    if manifest.protected_final_test_subject_ids != manifest.final_test_subject_ids:
        raise CohortManifestError("Protected final IDs must equal final-test IDs.")
    _verify_hash(asdict(manifest), manifest.manifest_sha256, "split")


def write_immutable_manifest(manifest: QCEligibilityManifest | D082CrossSubjectSplitManifest, path: str | Path) -> str:
    if isinstance(manifest, QCEligibilityManifest):
        validate_qc_manifest(manifest)
    elif isinstance(manifest, D082CrossSubjectSplitManifest):
        validate_split_manifest(manifest)
    else:
        raise CohortManifestError("Unsupported manifest type.")
    destination = Path(path).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(asdict(manifest), sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    if destination.exists() and destination.read_text(encoding="utf-8") != rendered:
        raise CohortManifestError(f"Frozen manifest already exists with different content: {destination}.")
    if not destination.exists():
        destination.write_text(rendered, encoding="utf-8", newline="\n")
    return sha256(destination.read_bytes()).hexdigest()


def qc_manifest_from_mapping(payload: Mapping[str, Any]) -> QCEligibilityManifest:
    records = tuple(SubjectEligibilityRecord(**{
        **item,
        "requested_runs": tuple(item["requested_runs"]),
        "loaded_runs": tuple(item["loaded_runs"]),
        "rejection_reasons": dict(item["rejection_reasons"]),
        "source_files": tuple(item["source_files"]),
        "source_sha256": tuple(item["source_sha256"]),
    }) for item in payload["subjects"])
    manifest = QCEligibilityManifest(
        **{key: value for key, value in payload.items() if key not in {"subjects", "source_subject_ids", "preprocessing_qc_policy_ids", "eligible_subject_ids", "excluded_subject_ids", "excluded_subject_reasons"}},
        source_subject_ids=tuple(payload["source_subject_ids"]),
        preprocessing_qc_policy_ids=tuple(payload["preprocessing_qc_policy_ids"]),
        subjects=records,
        eligible_subject_ids=tuple(payload["eligible_subject_ids"]),
        excluded_subject_ids=tuple(payload["excluded_subject_ids"]),
        excluded_subject_reasons=dict(payload["excluded_subject_reasons"]),
    )
    validate_qc_manifest(manifest)
    return manifest


def split_manifest_from_mapping(payload: Mapping[str, Any]) -> D082CrossSubjectSplitManifest:
    tuple_fields = {"policy_ids", "eligible_subject_ids", "excluded_subject_ids", "shuffled_eligible_subject_ids", "tie_break_order", "train_subject_ids", "validation_subject_ids", "final_test_subject_ids", "protected_final_test_subject_ids"}
    mapping_fields = {"excluded_subject_reasons", "ideal_quotas", "floor_counts", "fractional_remainders", "partition_counts"}
    values = {key: (tuple(value) if key in tuple_fields else dict(value) if key in mapping_fields else value) for key, value in payload.items()}
    manifest = D082CrossSubjectSplitManifest(**values)
    validate_split_manifest(manifest)
    return manifest


def _content_hash(payload: Mapping[str, Any]) -> str:
    content = dict(payload)
    content["manifest_sha256"] = ""
    return sha256(json.dumps(content, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _verify_hash(payload: Mapping[str, Any], observed: str, label: str) -> None:
    if len(observed) != 64 or observed != _content_hash(payload):
        raise CohortManifestError(f"D-082 {label} manifest content hash mismatch.")


def _required_text(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CohortManifestError(f"{name} must be non-empty.")
    return value


def _sha256_text(value: str, name: str) -> str:
    value = _required_text(value, name)
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise CohortManifestError(f"{name} must be a lowercase SHA-256 digest.")
    return value
