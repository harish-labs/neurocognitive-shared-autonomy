"""Freeze D-081 episodes and D-083 final-participation after D-082 split freeze."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mne
import pandas as pd

from src.evaluation.cohort import split_manifest_from_mapping
from src.evaluation.episodes import (
    build_sequential_participation_manifest,
    construct_episode_manifest,
    freeze_episode_manifest,
    freeze_sequential_participation_manifest,
)
from src.evaluation.final_contract import sha256_file
from src.evaluation.final_data import subject_epoch_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split-manifest", default="results/m7/manifest/m7-d082-cross-subject-v1.json")
    parser.add_argument("--processed-directory", default="data/processed/m7_prefinal")
    parser.add_argument("--output-directory", default="results/m7/manifest")
    arguments = parser.parse_args()

    split_path = Path(arguments.split_manifest).resolve()
    split_hash = sha256_file(split_path)
    split = split_manifest_from_mapping(json.loads(split_path.read_text(encoding="utf-8")))
    metadata_frames: list[pd.DataFrame] = []
    for subject_id in split.eligible_subject_ids:
        epochs = mne.read_epochs(
            subject_epoch_path(arguments.processed_directory, subject_id),
            preload=False,
            verbose="ERROR",
        )
        if epochs.metadata is None:
            raise RuntimeError(f"Subject {subject_id} is missing canonical epoch metadata.")
        metadata_frames.append(epochs.metadata.copy())
    source_metadata = pd.concat(metadata_frames, ignore_index=True)
    episode_manifest = construct_episode_manifest(source_metadata)

    output = Path(arguments.output_directory).resolve()
    episode_path = output / "m7-d081-fixed-intent-episodes-v1.json"
    episode_hash = freeze_episode_manifest(episode_manifest, episode_path)
    participation = build_sequential_participation_manifest(
        episode_manifest,
        split_manifest_sha256=split_hash,
        partition_name="final_test",
        frozen_partition_subject_ids=split.final_test_subject_ids,
    )
    participation_path = output / "m7-d083-final-sequential-participation-v1.json"
    participation_hash = freeze_sequential_participation_manifest(participation, participation_path)
    print(
        json.dumps(
            {
                "split_manifest_sha256": split_hash,
                "episode_manifest_path": str(episode_path),
                "episode_manifest_sha256": episode_hash,
                "episode_count": episode_manifest.episode_count,
                "source_trial_count": episode_manifest.source_trial_count,
                "sequential_source_trial_count": episode_manifest.sequential_source_trial_count,
                "tail_source_trial_count": episode_manifest.tail_source_trial_count,
                "participation_manifest_path": str(participation_path),
                "participation_manifest_sha256": participation_hash,
                "included_subject_ids": participation.included_subject_ids,
                "excluded_subject_ids": participation.excluded_subject_ids,
                "records": [record.__dict__ for record in participation.records],
                "no_replacement": participation.no_replacement,
            },
            sort_keys=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
