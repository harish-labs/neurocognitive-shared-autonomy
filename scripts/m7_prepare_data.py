"""Resumable M7-T02 public EEG download/preprocessing utility; computes no outcomes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.evaluation.final_data import (
    load_subject_audit,
    prepare_and_audit_subject,
    subject_audit_path,
    subject_epoch_path,
    write_subject_audit,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-subject", type=int, required=True)
    parser.add_argument("--end-subject", type=int, required=True)
    parser.add_argument("--raw-data-path", default="data/raw/mne_data")
    parser.add_argument("--processed-directory", default="data/processed/m7_prefinal")
    arguments = parser.parse_args()
    if not 1 <= arguments.start_subject <= arguments.end_subject <= 109:
        parser.error("subject range must satisfy 1 <= start <= end <= 109")
    processed = Path(arguments.processed_directory).resolve()
    for subject_id in range(arguments.start_subject, arguments.end_subject + 1):
        path = subject_epoch_path(processed, subject_id)
        audit_path = subject_audit_path(processed, subject_id)
        if audit_path.is_file():
            audit = load_subject_audit(processed, subject_id)
            if audit.eligible and not path.is_file():
                raise RuntimeError(f"Eligible subject {subject_id} has an audit but no epoch artifact.")
            print(json.dumps({"subject_id": subject_id, "status": "already_audited", "eligible": audit.eligible, "path": str(path) if path.is_file() else None}), flush=True)
            continue
        audit = prepare_and_audit_subject(
            subject_id=subject_id,
            raw_data_path=arguments.raw_data_path,
            processed_directory=processed,
        )
        write_subject_audit(audit, processed)
        print(
            json.dumps(
                {
                    "subject_id": subject_id,
                    "status": "prepared",
                    "retained_binary_epochs": audit.retained_binary_epochs,
                    "retained_left_epochs": audit.retained_left_epochs,
                    "retained_right_epochs": audit.retained_right_epochs,
                    "rejected_binary_epochs": audit.rejected_binary_epochs,
                    "sha256": audit.processed_epoch_sha256,
                    "eligible": audit.eligible,
                    "exclusion_reason": audit.exclusion_reason,
                },
                sort_keys=True,
            ),
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
