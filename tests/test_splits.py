from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.eeg.splits import (
    APPROVED_SPLIT_SEED,
    FINAL_TEST_SUBJECT_COUNT,
    FULL_ELIGIBLE_SUBJECT_COUNT,
    TRAIN_SUBJECT_COUNT,
    VALIDATION_SUBJECT_COUNT,
    CrossSubjectSplitManifest,
    SplitManifestError,
    WithinSubjectSplitManifest,
    assign_cross_subject_partitions,
    assign_within_subject_partitions,
    build_cross_subject_split_manifest,
    build_within_subject_split_manifest,
    load_cross_subject_split_manifest,
    load_within_subject_split_manifest,
    save_split_manifest,
)


def make_within_subject_epoch_metadata() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for run_id, base_sample in zip((4, 8, 12), (160, 10_160, 20_160), strict=True):
        for trial_index, (semantic_label, event_code) in enumerate(
            (
                ("left", "T1"),
                ("right", "T2"),
                ("left", "T1"),
                ("right", "T2"),
                ("left", "T1"),
                ("right", "T2"),
            )
        ):
            rows.append(
                {
                    "subject_id": 1,
                    "run_id": run_id,
                    "source_file": f"subject_1_run_{run_id}.edf",
                    "event_code": event_code,
                    "semantic_label": semantic_label,
                    "event_sample": base_sample + (trial_index * 160),
                    "trial_index": trial_index,
                }
            )
    return pd.DataFrame(rows)


def make_cross_subject_epoch_metadata(subject_count: int = FULL_ELIGIBLE_SUBJECT_COUNT) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for subject_id in range(1, subject_count + 1):
        for run_id, event_sample in ((4, 160), (8, 320)):
            for semantic_label, event_code, trial_index in (("left", "T1", 0), ("right", "T2", 1)):
                rows.append(
                    {
                        "subject_id": subject_id,
                        "run_id": run_id,
                        "source_file": f"subject_{subject_id}_run_{run_id}.edf",
                        "event_code": event_code,
                        "semantic_label": semantic_label,
                        "event_sample": event_sample + (trial_index * 80),
                        "trial_index": trial_index,
                    }
                )
    return pd.DataFrame(rows)


def test_build_within_subject_split_manifest_is_deterministic_and_stratified() -> None:
    metadata = make_within_subject_epoch_metadata()

    manifest_a = build_within_subject_split_manifest(metadata)
    manifest_b = build_within_subject_split_manifest(metadata)

    assert manifest_a == manifest_b
    assert manifest_a.split_seed == APPROVED_SPLIT_SEED
    assert manifest_a.partition_counts == {"train": 10, "validation": 4, "test": 4}
    assert manifest_a.semantic_label_counts[1]["train"] == {"left": 5, "right": 5}
    assert manifest_a.semantic_label_counts[1]["validation"] == {"left": 2, "right": 2}
    assert manifest_a.semantic_label_counts[1]["test"] == {"left": 2, "right": 2}


def test_assign_within_subject_partitions_prevents_trial_leakage() -> None:
    metadata = make_within_subject_epoch_metadata()
    derived_windows = pd.concat([metadata, metadata.copy()], ignore_index=True)
    derived_windows["window_index"] = [0] * len(metadata) + [1] * len(metadata)

    manifest = build_within_subject_split_manifest(metadata)
    assigned = assign_within_subject_partitions(derived_windows, manifest)

    partition_counts = assigned.groupby("trial_key")["partition"].nunique()
    assert partition_counts.eq(1).all()
    assert set(assigned["partition"]) == {"train", "validation", "test"}


def test_build_within_subject_split_manifest_reports_unsupported_small_class_counts() -> None:
    metadata = make_within_subject_epoch_metadata().iloc[:4].copy()

    with pytest.raises(SplitManifestError, match="at least three retained trials per class"):
        build_within_subject_split_manifest(metadata)


def test_within_subject_manifest_round_trip_is_reproducible(tmp_path: Path) -> None:
    metadata = make_within_subject_epoch_metadata()
    manifest = build_within_subject_split_manifest(metadata)

    output_path = save_split_manifest(manifest, tmp_path / "within_subject_split_manifest.json")
    reloaded = load_within_subject_split_manifest(output_path)

    assert reloaded == manifest


def test_build_cross_subject_split_manifest_uses_approved_109_subject_counts() -> None:
    manifest = build_cross_subject_split_manifest(list(range(1, FULL_ELIGIBLE_SUBJECT_COUNT + 1)))

    assert manifest.partition_counts == {
        "train": TRAIN_SUBJECT_COUNT,
        "validation": VALIDATION_SUBJECT_COUNT,
        "final_test": FINAL_TEST_SUBJECT_COUNT,
    }
    assert len(set(manifest.train_subject_ids) & set(manifest.validation_subject_ids)) == 0
    assert len(set(manifest.train_subject_ids) & set(manifest.final_test_subject_ids)) == 0
    assert len(set(manifest.validation_subject_ids) & set(manifest.final_test_subject_ids)) == 0
    assert manifest.protected_final_test_subject_ids == manifest.final_test_subject_ids


def test_assign_cross_subject_partitions_preserves_subject_integrity_and_protects_final_test() -> None:
    metadata = make_cross_subject_epoch_metadata()
    manifest = build_cross_subject_split_manifest(list(range(1, FULL_ELIGIBLE_SUBJECT_COUNT + 1)))

    assigned = assign_cross_subject_partitions(metadata, manifest)
    per_subject_partition_count = assigned.groupby("subject_id")["partition"].nunique()

    assert per_subject_partition_count.eq(1).all()
    final_test_subjects = set(
        assigned.loc[assigned["partition"] == "final_test", "subject_id"].astype(int).tolist()
    )
    assert final_test_subjects == set(manifest.protected_final_test_subject_ids)


def test_cross_subject_manifest_round_trip_is_reproducible(tmp_path: Path) -> None:
    manifest = build_cross_subject_split_manifest(list(range(1, FULL_ELIGIBLE_SUBJECT_COUNT + 1)))

    output_path = save_split_manifest(manifest, tmp_path / "cross_subject_split_manifest.json")
    reloaded = load_cross_subject_split_manifest(output_path)

    assert reloaded == manifest


def test_build_cross_subject_split_manifest_stops_for_non_109_cohort() -> None:
    with pytest.raises(SplitManifestError, match="exactly 109 eligible subjects"):
        build_cross_subject_split_manifest(list(range(1, 109)))


def test_cross_subject_manifest_is_deterministic() -> None:
    manifest_a = build_cross_subject_split_manifest(list(range(1, FULL_ELIGIBLE_SUBJECT_COUNT + 1)))
    manifest_b = build_cross_subject_split_manifest(list(range(1, FULL_ELIGIBLE_SUBJECT_COUNT + 1)))

    assert manifest_a == manifest_b
