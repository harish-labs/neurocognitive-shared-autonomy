"""Freeze D-082 QC eligibility and deterministic split manifests after all audits exist."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from src.eeg.epochs import REJECT_THRESHOLD_UV
from src.evaluation.cohort import (
    SOURCE_SUBJECT_IDS,
    build_qc_manifest,
    build_split_manifest,
    write_immutable_manifest,
)
from src.evaluation.final_data import (
    DATASET_ID,
    DATASET_SOURCE,
    load_subject_audit,
    subject_audit_path,
    subject_eligibility_record,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed-directory", default="data/processed/m7_prefinal")
    parser.add_argument("--output-directory", default="results/m7/manifest")
    parser.add_argument("--code-sha")
    arguments = parser.parse_args()
    code_sha = arguments.code_sha or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, encoding="utf-8"
    ).strip()
    processed = Path(arguments.processed_directory).resolve()
    missing = [subject_id for subject_id in SOURCE_SUBJECT_IDS if not subject_audit_path(processed, subject_id).is_file()]
    if missing:
        raise RuntimeError("Cannot freeze D-082 before all 109 subject audits exist: " + ",".join(map(str, missing)))
    records = tuple(subject_eligibility_record(load_subject_audit(processed, subject_id)) for subject_id in SOURCE_SUBJECT_IDS)
    qc = build_qc_manifest(
        records,
        dataset_id=DATASET_ID,
        dataset_source=DATASET_SOURCE,
        generating_code_sha=code_sha,
        reject_threshold_uv=REJECT_THRESHOLD_UV,
    )
    output = Path(arguments.output_directory).resolve()
    qc_path = output / "m7-d082-qc-eligibility-v1.json"
    qc_file_hash = write_immutable_manifest(qc, qc_path)
    split = build_split_manifest(
        qc,
        generating_code_sha=code_sha,
        qc_manifest_file_sha256=qc_file_hash,
    )
    split_path = output / "m7-d082-cross-subject-v1.json"
    split_file_hash = write_immutable_manifest(split, split_path)
    print(json.dumps({
        "code_sha": code_sha,
        "source_population_count": qc.source_population_count,
        "actual_eligible_count": qc.actual_eligible_count,
        "excluded_count": qc.excluded_count,
        "excluded_subject_ids": qc.excluded_subject_ids,
        "excluded_subject_reasons": qc.excluded_subject_reasons,
        "qc_manifest_path": str(qc_path),
        "qc_manifest_content_hash": qc.manifest_sha256,
        "qc_manifest_file_hash": qc_file_hash,
        "split_manifest_path": str(split_path),
        "split_manifest_content_hash": split.manifest_sha256,
        "split_manifest_file_hash": split_file_hash,
        "ideal_quotas": split.ideal_quotas,
        "floor_counts": split.floor_counts,
        "fractional_remainders": split.fractional_remainders,
        "partition_counts": split.partition_counts,
        "train_subject_ids": split.train_subject_ids,
        "validation_subject_ids": split.validation_subject_ids,
        "final_test_subject_ids": split.final_test_subject_ids,
    }, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
