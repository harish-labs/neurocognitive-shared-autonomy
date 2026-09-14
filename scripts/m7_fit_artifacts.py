"""Fit and freeze M7-T02 decoder/calibrator artifacts without final-subject access."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import subprocess

from src.evaluation.cohort import split_manifest_from_mapping
from src.evaluation.final_artifacts import fit_and_freeze_cross_subject_artifacts
from src.evaluation.final_contract import sha256_file, write_immutable_json
from src.evaluation.final_data import build_cross_train_validation_epochs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split-manifest", default="results/m7/manifest/m7-d082-cross-subject-v1.json")
    parser.add_argument("--processed-directory", default="data/processed/m7_prefinal")
    parser.add_argument("--artifact-directory", default="models/checkpoints/m7-t02")
    parser.add_argument("--output", default="results/m7/manifest/m7-artifacts-v1.json")
    parser.add_argument("--code-sha")
    arguments = parser.parse_args()

    code_sha = arguments.code_sha or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, encoding="utf-8"
    ).strip()
    split_path = Path(arguments.split_manifest).resolve()
    split_hash = sha256_file(split_path)
    split = split_manifest_from_mapping(json.loads(split_path.read_text(encoding="utf-8")))
    epochs = build_cross_train_validation_epochs(arguments.processed_directory, split)
    bundle = fit_and_freeze_cross_subject_artifacts(
        epochs,
        split_manifest=split,
        output_directory=arguments.artifact_directory,
        code_sha=code_sha,
    )
    payload = {
        "schema_version": "m7-t02-artifacts-v1",
        "software_sha": code_sha,
        "split_manifest_path": str(split_path),
        "split_manifest_sha256": split_hash,
        "protected_final_subject_ids": list(split.final_test_subject_ids),
        "fit_subject_ids": list(split.train_subject_ids + split.validation_subject_ids),
        "artifact_records": [asdict(record) for record in bundle.records],
    }
    output = Path(arguments.output).resolve()
    artifact_manifest_hash = write_immutable_json(payload, output)
    print(
        json.dumps(
            {
                "artifact_manifest_path": str(output),
                "artifact_manifest_sha256": artifact_manifest_hash,
                "artifact_ids": [record.artifact_id for record in bundle.records],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
