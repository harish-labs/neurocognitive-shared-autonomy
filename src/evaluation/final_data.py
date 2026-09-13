"""M7-T02 dataset/QC audit and partition-isolated canonical epoch preparation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from collections import Counter
import json
from pathlib import Path
from typing import Sequence

import mne
from mne.datasets import eegbci

from src.eeg.epochs import REJECT_THRESHOLD_UV, create_motor_imagery_epochs, save_epochs
from src.eeg.loader import (
    EXPECTED_CHANNEL_COUNT,
    EXPECTED_SAMPLING_FREQUENCY,
    LoaderValidationError,
    load_subject_recordings,
)
from src.evaluation.cohort import D082CrossSubjectSplitManifest, SubjectEligibilityRecord
from src.evaluation.final_contract import FinalContractError, sha256_file, validate_cross_subject_split


APPROVED_RUNS = (4, 8, 12)
DATASET_ID = "PhysioNet EEG Motor Movement/Imagery Database / EEGBCI 1.0.0"
DATASET_SOURCE = "https://physionet.org/content/eegmmidb/1.0.0/"


@dataclass(frozen=True)
class RunAudit:
    subject_id: int
    run_id: int
    source_file: str
    source_sha256: str
    channel_count: int
    sampling_frequency: float
    annotations: tuple[str, ...]
    retained_binary_epochs: int
    retained_left_epochs: int
    retained_right_epochs: int
    rejected_binary_epochs: int
    rejection_reasons: dict[str, int]
    reject_threshold_uv: float
    t0_event_count: int
    t1_event_count: int
    t2_event_count: int


@dataclass(frozen=True)
class SubjectAudit:
    subject_id: int
    requested_run_ids: tuple[int, ...]
    loaded_run_ids: tuple[int, ...]
    run_audits: tuple[RunAudit, ...]
    retained_binary_epochs: int
    retained_left_epochs: int
    retained_right_epochs: int
    rejected_binary_epochs: int
    processed_epoch_path: str
    processed_epoch_sha256: str
    eligible: bool
    exclusion_reason: str | None
    within_subject_feasible: bool
    within_subject_infeasibility_reason: str | None


@dataclass(frozen=True)
class DatasetAudit:
    dataset_id: str
    dataset_source: str
    runs: tuple[int, ...]
    class_order: tuple[str, str]
    t0_policy: str
    preprocessing_policy_ids: tuple[str, ...]
    subject_audits: tuple[SubjectAudit, ...]
    eligible_subject_ids: tuple[int, ...]
    eligible_subject_count: int
    raw_file_count: int
    processed_subject_count: int


def prepare_and_audit_dataset(
    *,
    subject_ids: Sequence[int],
    raw_data_path: str | Path,
    processed_directory: str | Path,
) -> DatasetAudit:
    """Prepare isolated per-subject epochs; no decoder or outcome is computed."""

    normalized = tuple(int(subject_id) for subject_id in subject_ids)
    if normalized != tuple(range(1, 110)):
        raise FinalContractError("M7-T02 dataset audit requires the exact ordered 109-subject cohort.")
    subjects = tuple(
        prepare_and_audit_subject(
            subject_id=subject_id,
            raw_data_path=raw_data_path,
            processed_directory=processed_directory,
        )
        for subject_id in normalized
    )
    eligible = tuple(subject.subject_id for subject in subjects if subject.eligible)
    return DatasetAudit(
        dataset_id=DATASET_ID,
        dataset_source=DATASET_SOURCE,
        runs=APPROVED_RUNS,
        class_order=("left", "right"),
        t0_policy="excluded_from_binary_epochs_preserved_in_raw_annotations_and_audit_counts",
        preprocessing_policy_ids=tuple(f"D-{index:03d}" for index in range(31, 40)),
        subject_audits=subjects,
        eligible_subject_ids=eligible,
        eligible_subject_count=len(eligible),
        raw_file_count=sum(len(subject.run_audits) for subject in subjects),
        processed_subject_count=len(subjects),
    )


def prepare_and_audit_subject(
    *,
    subject_id: int,
    raw_data_path: str | Path,
    processed_directory: str | Path,
) -> SubjectAudit:
    destination = subject_epoch_path(processed_directory, subject_id)
    try:
        recordings = load_subject_recordings(
            subject_id,
            run_ids=APPROVED_RUNS,
            data_path=raw_data_path,
            preload=False,
            verbose="ERROR",
        )
    except LoaderValidationError as exc:
        return _audit_source_validation_failure(
            subject_id=subject_id,
            raw_data_path=raw_data_path,
            error=str(exc),
        )
    run_epochs: list[mne.BaseEpochs] = []
    audits: list[RunAudit] = []
    for recording in recordings:
        extraction = create_motor_imagery_epochs(recording)
        labels = tuple(str(value) for value in extraction.labels)
        rejection_reasons = Counter(item.reason for item in extraction.rejection_log)
        if len(extraction.epochs) > 0:
            run_epochs.append(extraction.epochs)
        audits.append(
            RunAudit(
                subject_id=subject_id,
                run_id=recording.summary.run_id,
                source_file=str(recording.summary.file_path),
                source_sha256=sha256_file(recording.summary.file_path),
                channel_count=recording.summary.channel_count,
                sampling_frequency=recording.summary.sampling_frequency,
                annotations=recording.summary.annotations,
                retained_binary_epochs=len(labels),
                retained_left_epochs=labels.count("left"),
                retained_right_epochs=labels.count("right"),
                rejected_binary_epochs=len(extraction.rejection_log),
                rejection_reasons=dict(sorted(rejection_reasons.items())),
                reject_threshold_uv=REJECT_THRESHOLD_UV,
                t0_event_count=extraction.t0_event_count,
                t1_event_count=extraction.t1_event_count,
                t2_event_count=extraction.t2_event_count,
            )
        )
    if not run_epochs:
        return SubjectAudit(
            subject_id=subject_id,
            requested_run_ids=APPROVED_RUNS,
            loaded_run_ids=tuple(item.run_id for item in audits),
            run_audits=tuple(audits),
            retained_binary_epochs=0,
            retained_left_epochs=0,
            retained_right_epochs=0,
            rejected_binary_epochs=sum(item.rejected_binary_epochs for item in audits),
            processed_epoch_path="",
            processed_epoch_sha256="",
            eligible=False,
            exclusion_reason="all_binary_epochs_rejected_under_fixed_qc",
            within_subject_feasible=False,
            within_subject_infeasibility_reason="fewer_than_three_retained_trials_per_class",
        )
    epochs = (
        run_epochs[0].copy()
        if len(run_epochs) == 1
        else mne.concatenate_epochs(run_epochs, add_offset=True, verbose="ERROR")
    )
    _validate_subject_epochs(epochs, subject_id)
    save_epochs(epochs, destination, overwrite=True)
    left = sum(item.retained_left_epochs for item in audits)
    right = sum(item.retained_right_epochs for item in audits)
    eligible = left > 0 and right > 0
    within_subject_feasible = left >= 3 and right >= 3
    if eligible:
        exclusion_reason = None
    elif left == 0 and right == 0:
        exclusion_reason = "all_binary_epochs_rejected_under_fixed_qc"
    else:
        exclusion_reason = "one_binary_class_absent_after_fixed_qc"
    return SubjectAudit(
        subject_id=subject_id,
        requested_run_ids=APPROVED_RUNS,
        loaded_run_ids=tuple(item.run_id for item in audits),
        run_audits=tuple(audits),
        retained_binary_epochs=len(epochs),
        retained_left_epochs=left,
        retained_right_epochs=right,
        rejected_binary_epochs=sum(item.rejected_binary_epochs for item in audits),
        processed_epoch_path=str(destination),
        processed_epoch_sha256=sha256_file(destination),
        eligible=eligible,
        exclusion_reason=exclusion_reason,
        within_subject_feasible=within_subject_feasible,
        within_subject_infeasibility_reason=(None if within_subject_feasible else "fewer_than_three_retained_trials_per_class"),
    )


def subject_epoch_path(directory: str | Path, subject_id: int) -> Path:
    return Path(directory).resolve() / f"m7-subject-{int(subject_id):03d}-epo.fif"


def _audit_source_validation_failure(
    *,
    subject_id: int,
    raw_data_path: str | Path,
    error: str,
) -> SubjectAudit:
    """Record a fixed source-contract exclusion without weakening preprocessing."""

    file_paths = eegbci.load_data(
        subject_id,
        APPROVED_RUNS,
        path=str(Path(raw_data_path).resolve()),
        update_path=False,
        verbose="ERROR",
    )
    audits: list[RunAudit] = []
    for run_id, file_path_value in zip(APPROVED_RUNS, file_paths):
        file_path = Path(file_path_value).resolve()
        raw = mne.io.read_raw_edf(file_path, preload=False, verbose="ERROR")
        annotations = tuple(sorted(set(str(value) for value in raw.annotations.description)))
        t0 = sum(str(value) == "T0" for value in raw.annotations.description)
        t1 = sum(str(value) == "T1" for value in raw.annotations.description)
        t2 = sum(str(value) == "T2" for value in raw.annotations.description)
        rejected = t1 + t2
        audits.append(
            RunAudit(
                subject_id=subject_id,
                run_id=run_id,
                source_file=str(file_path),
                source_sha256=sha256_file(file_path),
                channel_count=len(raw.ch_names),
                sampling_frequency=float(raw.info["sfreq"]),
                annotations=annotations,
                retained_binary_epochs=0,
                retained_left_epochs=0,
                retained_right_epochs=0,
                rejected_binary_epochs=rejected,
                rejection_reasons={"source_validation_failed": rejected},
                reject_threshold_uv=REJECT_THRESHOLD_UV,
                t0_event_count=t0,
                t1_event_count=t1,
                t2_event_count=t2,
            )
        )
    return SubjectAudit(
        subject_id=subject_id,
        requested_run_ids=APPROVED_RUNS,
        loaded_run_ids=APPROVED_RUNS,
        run_audits=tuple(audits),
        retained_binary_epochs=0,
        retained_left_epochs=0,
        retained_right_epochs=0,
        rejected_binary_epochs=sum(item.rejected_binary_epochs for item in audits),
        processed_epoch_path="",
        processed_epoch_sha256="",
        eligible=False,
        exclusion_reason=f"source_validation_failed:{error}",
        within_subject_feasible=False,
        within_subject_infeasibility_reason="fewer_than_three_retained_trials_per_class",
    )


def load_subject_epochs(directory: str | Path, subject_id: int) -> mne.BaseEpochs:
    path = subject_epoch_path(directory, subject_id)
    if not path.is_file():
        raise FinalContractError(f"Prepared subject epoch artifact is missing: {path}.")
    epochs = mne.read_epochs(path, preload=True, verbose="ERROR")
    _validate_subject_epochs(epochs, int(subject_id))
    return epochs


def build_cross_train_validation_epochs(
    *,
    processed_directory: str | Path,
    split_manifest: D082CrossSubjectSplitManifest,
) -> mne.BaseEpochs:
    validate_cross_subject_split(split_manifest)
    epochs_by_subject: list[mne.BaseEpochs] = []
    partition_by_subject = {
        **{subject_id: "train" for subject_id in split_manifest.train_subject_ids},
        **{subject_id: "validation" for subject_id in split_manifest.validation_subject_ids},
    }
    for subject_id in (*split_manifest.train_subject_ids, *split_manifest.validation_subject_ids):
        epochs = load_subject_epochs(processed_directory, subject_id)
        if epochs.metadata is None:
            raise FinalContractError("Canonical epochs lost required metadata.")
        metadata = epochs.metadata.copy()
        metadata["partition"] = partition_by_subject[subject_id]
        epochs.metadata = metadata
        epochs_by_subject.append(epochs)
    combined = mne.concatenate_epochs(epochs_by_subject, add_offset=True, verbose="ERROR")
    observed_subjects = set(int(value) for value in combined.metadata["subject_id"])
    expected_subjects = set(partition_by_subject)
    if observed_subjects != expected_subjects or observed_subjects & set(split_manifest.final_test_subject_ids):
        raise FinalContractError("Cross-subject fitting epochs do not match the frozen train/validation cohort.")
    return combined


def dataset_audit_mapping(audit: DatasetAudit) -> dict[str, object]:
    return asdict(audit)


def subject_audit_path(directory: str | Path, subject_id: int) -> Path:
    return Path(directory).resolve() / "audit" / f"m7-subject-{int(subject_id):03d}-qc.json"


def write_subject_audit(audit: SubjectAudit, directory: str | Path) -> Path:
    path = subject_audit_path(directory, audit.subject_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(asdict(audit), sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    path.write_text(rendered, encoding="utf-8", newline="\n")
    return path


def load_subject_audit(directory: str | Path, subject_id: int) -> SubjectAudit:
    payload = json.loads(subject_audit_path(directory, subject_id).read_text(encoding="utf-8"))
    left = int(payload["retained_left_epochs"])
    right = int(payload["retained_right_epochs"])
    payload.setdefault("within_subject_feasible", left >= 3 and right >= 3)
    payload.setdefault(
        "within_subject_infeasibility_reason",
        None if left >= 3 and right >= 3 else "fewer_than_three_retained_trials_per_class",
    )
    run_audits = tuple(
        RunAudit(
            **{key: value for key, value in item.items() if key not in {"annotations", "rejection_reasons"}},
            annotations=tuple(item["annotations"]),
            rejection_reasons={str(key): int(value) for key, value in item["rejection_reasons"].items()},
        )
        for item in payload["run_audits"]
    )
    return SubjectAudit(
        **{key: value for key, value in payload.items() if key not in {"requested_run_ids", "loaded_run_ids", "run_audits"}},
        requested_run_ids=tuple(payload["requested_run_ids"]),
        loaded_run_ids=tuple(payload["loaded_run_ids"]),
        run_audits=run_audits,
    )


def subject_eligibility_record(audit: SubjectAudit) -> SubjectEligibilityRecord:
    reasons: Counter[str] = Counter()
    for run in audit.run_audits:
        reasons.update(run.rejection_reasons)
    return SubjectEligibilityRecord(
        subject_id=audit.subject_id,
        requested_runs=audit.requested_run_ids,
        loaded_runs=audit.loaded_run_ids,
        raw_t1_count=sum(item.t1_event_count for item in audit.run_audits),
        raw_t2_count=sum(item.t2_event_count for item in audit.run_audits),
        candidate_binary_epochs=sum(item.t1_event_count + item.t2_event_count for item in audit.run_audits),
        retained_t1_count=audit.retained_left_epochs,
        retained_t2_count=audit.retained_right_epochs,
        rejected_epoch_count=audit.rejected_binary_epochs,
        rejection_reasons=dict(sorted(reasons.items())),
        eligible=audit.eligible,
        exclusion_reason=audit.exclusion_reason,
        within_subject_feasible=audit.within_subject_feasible,
        within_subject_infeasibility_reason=audit.within_subject_infeasibility_reason,
        source_files=tuple(Path(item.source_file).name for item in audit.run_audits),
        source_sha256=tuple(item.source_sha256 for item in audit.run_audits),
    )


def _validate_subject_epochs(epochs: mne.BaseEpochs, subject_id: int) -> None:
    if len(epochs.ch_names) != EXPECTED_CHANNEL_COUNT or float(epochs.info["sfreq"]) != EXPECTED_SAMPLING_FREQUENCY:
        raise FinalContractError("Prepared epochs violate the accepted 64-channel/160-Hz contract.")
    if epochs.metadata is None or len(epochs.metadata) != len(epochs):
        raise FinalContractError("Prepared epochs require aligned provenance metadata.")
    if set(epochs.metadata["semantic_label"].astype(str)) - {"left", "right"}:
        raise FinalContractError("Prepared binary epochs contain a non-T1/T2 label.")
    if set(int(value) for value in epochs.metadata["subject_id"]) != {subject_id}:
        raise FinalContractError("Prepared subject epochs mix subject identities.")
    observed_runs = set(int(value) for value in epochs.metadata["run_id"])
    if not observed_runs or not observed_runs.issubset(set(APPROVED_RUNS)):
        raise FinalContractError("Prepared subject epochs may contain only approved runs 4/8/12.")
