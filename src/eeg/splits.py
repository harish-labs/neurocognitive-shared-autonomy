from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

import pandas as pd

WITHIN_SUBJECT_SPLIT_VERSION = "m1-t04-within-subject-v1"
CROSS_SUBJECT_SPLIT_VERSION = "m1-t04-cross-subject-v1"
APPROVED_SPLIT_SEED = 42
FULL_ELIGIBLE_SUBJECT_COUNT = 109
TRAIN_SUBJECT_COUNT = 76
VALIDATION_SUBJECT_COUNT = 16
FINAL_TEST_SUBJECT_COUNT = 17
WITHIN_SUBJECT_PARTITIONS = ("train", "validation", "test")
LEFT_RIGHT_LABELS = ("left", "right")
REQUIRED_METADATA_COLUMNS = (
    "subject_id",
    "run_id",
    "source_file",
    "event_code",
    "semantic_label",
    "event_sample",
    "trial_index",
)
TRIAL_KEY_COLUMNS = ("subject_id", "run_id", "source_file", "event_sample", "event_code")


class SplitManifestError(ValueError):
    """Raised when split-manifest generation cannot satisfy the approved contract."""


@dataclass(frozen=True)
class WithinSubjectSplitManifest:
    version: str
    split_seed: int
    split_strategy: str
    original_trial_key_columns: tuple[str, ...]
    eligible_subject_ids: tuple[int, ...]
    partition_trial_keys: dict[str, tuple[str, ...]]
    partition_counts: dict[str, int]
    subject_partition_counts: dict[int, dict[str, int]]
    semantic_label_counts: dict[int, dict[str, dict[str, int]]]


@dataclass(frozen=True)
class CrossSubjectSplitManifest:
    version: str
    split_seed: int
    split_strategy: str
    eligible_subject_ids: tuple[int, ...]
    train_subject_ids: tuple[int, ...]
    validation_subject_ids: tuple[int, ...]
    final_test_subject_ids: tuple[int, ...]
    protected_final_test_subject_ids: tuple[int, ...]
    partition_counts: dict[str, int]


def _normalize_epoch_metadata(epoch_metadata: pd.DataFrame) -> pd.DataFrame:
    missing = [column for column in REQUIRED_METADATA_COLUMNS if column not in epoch_metadata.columns]
    if missing:
        raise SplitManifestError(
            "Epoch metadata is missing required provenance columns: " + ", ".join(missing) + "."
        )

    metadata = epoch_metadata.loc[:, REQUIRED_METADATA_COLUMNS].copy()
    if metadata.empty:
        raise SplitManifestError("Epoch metadata is empty; no approved split can be generated.")

    for column in ("subject_id", "run_id", "event_sample", "trial_index"):
        if metadata[column].isnull().any():
            raise SplitManifestError(f"Epoch metadata column '{column}' contains null values.")
        metadata[column] = metadata[column].astype(int)

    if metadata["semantic_label"].isnull().any():
        raise SplitManifestError("Epoch metadata column 'semantic_label' contains null values.")
    metadata["semantic_label"] = metadata["semantic_label"].astype(str)
    metadata["event_code"] = metadata["event_code"].astype(str)
    metadata["source_file"] = metadata["source_file"].fillna("").astype(str)

    invalid_labels = sorted(set(metadata["semantic_label"]) - set(LEFT_RIGHT_LABELS))
    if invalid_labels:
        raise SplitManifestError(
            "Split manifests only support canonical binary left/right epochs. "
            f"Found unsupported labels: {', '.join(invalid_labels)}."
        )

    metadata["trial_key"] = metadata.apply(_compose_trial_key, axis=1)
    return metadata


def _compose_trial_key(row: pd.Series) -> str:
    return "|".join(str(row[column]) for column in TRIAL_KEY_COLUMNS)


def _stable_partition_counts(total_count: int) -> dict[str, int]:
    if total_count < len(WITHIN_SUBJECT_PARTITIONS):
        raise SplitManifestError(
            "Approved 60/20/20 splitting requires at least three retained trials per class."
        )

    train_count = round(total_count * 0.6)
    validation_count = round(total_count * 0.2)
    test_count = total_count - train_count - validation_count

    counts = {"train": train_count, "validation": validation_count, "test": test_count}
    if any(count <= 0 for count in counts.values()):
        raise SplitManifestError(
            "Approved 60/20/20 splitting produced an empty partition; report this subject instead."
        )
    return counts


def build_within_subject_split_manifest(
    epoch_metadata: pd.DataFrame,
    *,
    split_seed: int = APPROVED_SPLIT_SEED,
) -> WithinSubjectSplitManifest:
    metadata = _normalize_epoch_metadata(epoch_metadata)
    trial_rows = (
        metadata.drop_duplicates(subset=["trial_key"])
        .loc[:, ["trial_key", "subject_id", "semantic_label"]]
        .sort_values(["subject_id", "semantic_label", "trial_key"])
        .reset_index(drop=True)
    )

    partition_trial_keys: dict[str, list[str]] = {name: [] for name in WITHIN_SUBJECT_PARTITIONS}
    subject_partition_counts: dict[int, dict[str, int]] = {}
    semantic_label_counts: dict[int, dict[str, dict[str, int]]] = {}
    eligible_subject_ids: list[int] = []

    for subject_id in sorted(trial_rows["subject_id"].unique().tolist()):
        subject_trials = trial_rows.loc[trial_rows["subject_id"] == subject_id].reset_index(drop=True)
        eligible_subject_ids.append(int(subject_id))
        subject_partition_counts[int(subject_id)] = {name: 0 for name in WITHIN_SUBJECT_PARTITIONS}
        semantic_label_counts[int(subject_id)] = {
            name: {label: 0 for label in LEFT_RIGHT_LABELS} for name in WITHIN_SUBJECT_PARTITIONS
        }

        for semantic_label in LEFT_RIGHT_LABELS:
            label_trials = (
                subject_trials.loc[subject_trials["semantic_label"] == semantic_label, "trial_key"]
                .sort_values()
                .sample(frac=1.0, random_state=split_seed)
                .tolist()
            )
            if not label_trials:
                raise SplitManifestError(
                    f"Subject {subject_id} is missing retained '{semantic_label}' trials."
                )

            label_partition_counts = _stable_partition_counts(len(label_trials))
            train_stop = label_partition_counts["train"]
            validation_stop = train_stop + label_partition_counts["validation"]
            per_partition = {
                "train": label_trials[:train_stop],
                "validation": label_trials[train_stop:validation_stop],
                "test": label_trials[validation_stop:],
            }

            for partition_name, keys in per_partition.items():
                if len(keys) != label_partition_counts[partition_name]:
                    raise SplitManifestError(
                        f"Deterministic class split failed for subject {subject_id} label {semantic_label}."
                    )
                partition_trial_keys[partition_name].extend(keys)
                subject_partition_counts[int(subject_id)][partition_name] += len(keys)
                semantic_label_counts[int(subject_id)][partition_name][semantic_label] = len(keys)

    frozen_partition_trial_keys = {
        name: tuple(sorted(keys)) for name, keys in partition_trial_keys.items()
    }
    partition_counts = {name: len(keys) for name, keys in frozen_partition_trial_keys.items()}

    return WithinSubjectSplitManifest(
        version=WITHIN_SUBJECT_SPLIT_VERSION,
        split_seed=split_seed,
        split_strategy="within_subject_original_trial_stratified_60_20_20",
        original_trial_key_columns=TRIAL_KEY_COLUMNS,
        eligible_subject_ids=tuple(eligible_subject_ids),
        partition_trial_keys=frozen_partition_trial_keys,
        partition_counts=partition_counts,
        subject_partition_counts=subject_partition_counts,
        semantic_label_counts=semantic_label_counts,
    )


def assign_within_subject_partitions(
    epoch_metadata: pd.DataFrame,
    manifest: WithinSubjectSplitManifest,
) -> pd.DataFrame:
    metadata = _normalize_epoch_metadata(epoch_metadata)
    partition_by_trial_key: dict[str, str] = {}
    for partition_name, trial_keys in manifest.partition_trial_keys.items():
        for trial_key in trial_keys:
            if trial_key in partition_by_trial_key:
                raise SplitManifestError(f"Trial key {trial_key!r} appears in more than one partition.")
            partition_by_trial_key[trial_key] = partition_name

    assigned = metadata.copy()
    assigned["partition"] = assigned["trial_key"].map(partition_by_trial_key)
    if assigned["partition"].isnull().any():
        missing_count = int(assigned["partition"].isnull().sum())
        raise SplitManifestError(f"{missing_count} rows were not covered by the within-subject manifest.")
    return assigned


def build_cross_subject_split_manifest(
    eligible_subject_ids: list[int] | tuple[int, ...],
    *,
    split_seed: int = APPROVED_SPLIT_SEED,
) -> CrossSubjectSplitManifest:
    if split_seed != APPROVED_SPLIT_SEED:
        raise SplitManifestError(
            f"Canonical cross-subject manifests must use the approved fixed seed {APPROVED_SPLIT_SEED}."
        )

    frozen_subject_ids = tuple(sorted({int(subject_id) for subject_id in eligible_subject_ids}))
    if len(frozen_subject_ids) != FULL_ELIGIBLE_SUBJECT_COUNT:
        raise SplitManifestError(
            "Approved cross-subject manifest requires exactly 109 eligible subjects. "
            f"Received {len(frozen_subject_ids)} eligible subjects."
        )

    shuffled = (
        pd.Series(frozen_subject_ids, dtype=int)
        .sample(frac=1.0, random_state=split_seed)
        .tolist()
    )
    train_subject_ids = tuple(sorted(shuffled[:TRAIN_SUBJECT_COUNT]))
    validation_subject_ids = tuple(
        sorted(shuffled[TRAIN_SUBJECT_COUNT : TRAIN_SUBJECT_COUNT + VALIDATION_SUBJECT_COUNT])
    )
    final_test_subject_ids = tuple(sorted(shuffled[-FINAL_TEST_SUBJECT_COUNT:]))

    partitions = {
        "train": set(train_subject_ids),
        "validation": set(validation_subject_ids),
        "final_test": set(final_test_subject_ids),
    }
    if len(partitions["train"] | partitions["validation"] | partitions["final_test"]) != FULL_ELIGIBLE_SUBJECT_COUNT:
        raise SplitManifestError("Cross-subject partitions are not disjoint across the full eligible cohort.")

    return CrossSubjectSplitManifest(
        version=CROSS_SUBJECT_SPLIT_VERSION,
        split_seed=split_seed,
        split_strategy="cross_subject_fixed_subject_held_out_70_15_15",
        eligible_subject_ids=frozen_subject_ids,
        train_subject_ids=train_subject_ids,
        validation_subject_ids=validation_subject_ids,
        final_test_subject_ids=final_test_subject_ids,
        protected_final_test_subject_ids=final_test_subject_ids,
        partition_counts={
            "train": len(train_subject_ids),
            "validation": len(validation_subject_ids),
            "final_test": len(final_test_subject_ids),
        },
    )


def assign_cross_subject_partitions(
    epoch_metadata: pd.DataFrame,
    manifest: CrossSubjectSplitManifest,
) -> pd.DataFrame:
    metadata = _normalize_epoch_metadata(epoch_metadata)
    partition_by_subject_id = {
        subject_id: "train" for subject_id in manifest.train_subject_ids
    }
    partition_by_subject_id.update(
        {subject_id: "validation" for subject_id in manifest.validation_subject_ids}
    )
    partition_by_subject_id.update(
        {subject_id: "final_test" for subject_id in manifest.final_test_subject_ids}
    )

    assigned = metadata.copy()
    assigned["partition"] = assigned["subject_id"].map(partition_by_subject_id)
    if assigned["partition"].isnull().any():
        missing_subjects = sorted(
            {int(subject_id) for subject_id in assigned.loc[assigned["partition"].isnull(), "subject_id"].tolist()}
        )
        raise SplitManifestError(
            "Cross-subject manifest did not cover all provided subject IDs: "
            + ", ".join(str(subject_id) for subject_id in missing_subjects)
            + "."
        )
    return assigned


def save_split_manifest(
    manifest: WithinSubjectSplitManifest | CrossSubjectSplitManifest,
    output_path: str | Path,
) -> Path:
    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(manifest)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_within_subject_split_manifest(path: str | Path) -> WithinSubjectSplitManifest:
    payload = _load_manifest_payload(path)
    return WithinSubjectSplitManifest(
        version=str(payload["version"]),
        split_seed=int(payload["split_seed"]),
        split_strategy=str(payload["split_strategy"]),
        original_trial_key_columns=tuple(payload["original_trial_key_columns"]),
        eligible_subject_ids=tuple(int(subject_id) for subject_id in payload["eligible_subject_ids"]),
        partition_trial_keys={
            str(name): tuple(str(key) for key in keys)
            for name, keys in payload["partition_trial_keys"].items()
        },
        partition_counts={str(name): int(count) for name, count in payload["partition_counts"].items()},
        subject_partition_counts={
            int(subject_id): {str(name): int(count) for name, count in counts.items()}
            for subject_id, counts in payload["subject_partition_counts"].items()
        },
        semantic_label_counts={
            int(subject_id): {
                str(partition_name): {str(label): int(count) for label, count in label_counts.items()}
                for partition_name, label_counts in partition_counts.items()
            }
            for subject_id, partition_counts in payload["semantic_label_counts"].items()
        },
    )


def load_cross_subject_split_manifest(path: str | Path) -> CrossSubjectSplitManifest:
    payload = _load_manifest_payload(path)
    return CrossSubjectSplitManifest(
        version=str(payload["version"]),
        split_seed=int(payload["split_seed"]),
        split_strategy=str(payload["split_strategy"]),
        eligible_subject_ids=tuple(int(subject_id) for subject_id in payload["eligible_subject_ids"]),
        train_subject_ids=tuple(int(subject_id) for subject_id in payload["train_subject_ids"]),
        validation_subject_ids=tuple(int(subject_id) for subject_id in payload["validation_subject_ids"]),
        final_test_subject_ids=tuple(int(subject_id) for subject_id in payload["final_test_subject_ids"]),
        protected_final_test_subject_ids=tuple(
            int(subject_id) for subject_id in payload["protected_final_test_subject_ids"]
        ),
        partition_counts={str(name): int(count) for name, count in payload["partition_counts"].items()},
    )


def _load_manifest_payload(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path).expanduser().resolve()
    return json.loads(manifest_path.read_text(encoding="utf-8"))
