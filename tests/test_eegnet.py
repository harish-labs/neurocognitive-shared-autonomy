from __future__ import annotations

from pathlib import Path
import sys

import mne
import numpy as np
import pandas as pd
import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.eeg.splits import (
    FULL_ELIGIBLE_SUBJECT_COUNT,
    assign_cross_subject_partitions,
    assign_within_subject_partitions,
    build_cross_subject_split_manifest,
    build_within_subject_split_manifest,
)
from src.models import eegnet

CANONICAL_N_TIMES = int(
    round((eegnet.EPOCH_TMAX - eegnet.EPOCH_TMIN) * eegnet.EXPECTED_SAMPLING_FREQUENCY)
) + 1


def make_partitioned_epochs() -> mne.Epochs:
    sfreq = eegnet.EXPECTED_SAMPLING_FREQUENCY
    info = mne.create_info([f"EEG{i:02d}" for i in range(64)], sfreq=sfreq, ch_types="eeg")
    events: list[list[int]] = []
    metadata_rows: list[dict[str, object]] = []
    data_rows: list[np.ndarray] = []
    partition_plan = (
        ("train", "left", "T1", 8),
        ("train", "right", "T2", 8),
        ("validation", "left", "T1", 4),
        ("validation", "right", "T2", 4),
        ("test", "left", "T1", 4),
        ("test", "right", "T2", 4),
        ("final_test", "left", "T1", 4),
        ("final_test", "right", "T2", 4),
    )

    rng = np.random.default_rng(13)
    sample_cursor = 1_000
    trial_index = 0
    early_start = int((0.0 - eegnet.EPOCH_TMIN) * sfreq)
    early_stop = early_start + 32
    late_start = int((3.0 - eegnet.EPOCH_TMIN) * sfreq)
    late_stop = late_start + 32

    for partition, semantic_label, event_code, count in partition_plan:
        amplitude = 3.0 if semantic_label == "left" else -3.0
        for example_index in range(count):
            epoch = rng.normal(scale=0.05, size=(64, CANONICAL_N_TIMES)).astype(np.float32)
            epoch[0:4, early_start:early_stop] += amplitude
            epoch[4:8, late_start:late_stop] -= amplitude
            events.append([sample_cursor, 0, 2 if semantic_label == "left" else 3])
            metadata_rows.append(
                {
                    "partition": partition,
                    "semantic_label": semantic_label,
                    "subject_id": 1 if partition != "final_test" else 2,
                    "run_id": 4 if example_index % 2 == 0 else 8,
                    "source_file": f"{partition}_{semantic_label}.edf",
                    "event_code": event_code,
                    "event_sample": sample_cursor,
                    "trial_index": trial_index,
                }
            )
            data_rows.append(epoch)
            sample_cursor += CANONICAL_N_TIMES + 10
            trial_index += 1

    return mne.EpochsArray(
        data=np.asarray(data_rows),
        info=info,
        events=np.asarray(events),
        event_id={"left": 2, "right": 3},
        tmin=eegnet.EPOCH_TMIN,
        metadata=pd.DataFrame(metadata_rows),
        verbose="ERROR",
    )


def make_within_subject_epochs() -> mne.Epochs:
    epochs = make_partitioned_epochs()
    metadata_rows: list[dict[str, object]] = []
    data_rows: list[np.ndarray] = []
    events: list[list[int]] = []
    sample_cursor = 200
    trial_index = 0

    for run_id, base_sample in zip((4, 8, 12), (200, 10_200, 20_200), strict=True):
        for semantic_label, event_code in (("left", "T1"), ("right", "T2")) * 3:
            epoch = epochs.get_data(copy=True)[trial_index].copy()
            data_rows.append(epoch)
            events.append([sample_cursor, 0, 2 if semantic_label == "left" else 3])
            metadata_rows.append(
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
            sample_cursor += CANONICAL_N_TIMES + 5
            trial_index += 1

    within_subject_epochs = mne.EpochsArray(
        data=np.asarray(data_rows),
        info=epochs.info,
        events=np.asarray(events),
        event_id={"left": 2, "right": 3},
        tmin=eegnet.EPOCH_TMIN,
        metadata=pd.DataFrame(metadata_rows),
        verbose="ERROR",
    )
    manifest = build_within_subject_split_manifest(within_subject_epochs.metadata)
    within_subject_epochs.metadata = assign_within_subject_partitions(
        within_subject_epochs.metadata,
        manifest,
    ).reset_index(drop=True)
    return within_subject_epochs


def make_cross_subject_epochs() -> mne.Epochs:
    base_epochs = make_partitioned_epochs()
    rng = np.random.default_rng(23)
    events: list[list[int]] = []
    metadata_rows: list[dict[str, object]] = []
    data_rows: list[np.ndarray] = []
    sample_cursor = 500

    for subject_id in range(1, FULL_ELIGIBLE_SUBJECT_COUNT + 1):
        for semantic_label, event_code in (("left", "T1"), ("right", "T2")):
            epoch = rng.normal(scale=0.04, size=(64, CANONICAL_N_TIMES)).astype(np.float32)
            amplitude = 2.5 if semantic_label == "left" else -2.5
            epoch[0:4, 160:208] += amplitude
            epoch[4:8, 640:688] -= amplitude
            data_rows.append(epoch)
            events.append([sample_cursor, 0, 2 if semantic_label == "left" else 3])
            metadata_rows.append(
                {
                    "subject_id": subject_id,
                    "run_id": 4,
                    "source_file": f"subject_{subject_id}_run_4.edf",
                    "event_code": event_code,
                    "semantic_label": semantic_label,
                    "event_sample": sample_cursor,
                    "trial_index": 0 if semantic_label == "left" else 1,
                }
            )
            sample_cursor += CANONICAL_N_TIMES + 5

    cross_subject_epochs = mne.EpochsArray(
        data=np.asarray(data_rows),
        info=base_epochs.info,
        events=np.asarray(events),
        event_id={"left": 2, "right": 3},
        tmin=eegnet.EPOCH_TMIN,
        metadata=pd.DataFrame(metadata_rows),
        verbose="ERROR",
    )
    manifest = build_cross_subject_split_manifest(list(range(1, FULL_ELIGIBLE_SUBJECT_COUNT + 1)))
    cross_subject_epochs.metadata = assign_cross_subject_partitions(
        cross_subject_epochs.metadata,
        manifest,
    ).reset_index(drop=True)
    return cross_subject_epochs


def test_eegnet_forward_returns_two_logits_for_canonical_input() -> None:
    model = eegnet.EEGNetModel(n_times=CANONICAL_N_TIMES)
    inputs = torch.randn(3, 1, 64, CANONICAL_N_TIMES)

    logits = model(inputs)

    assert logits.shape == (3, 2)
    assert torch.isfinite(logits).all()


def test_fit_eegnet_rejects_csp_only_cropped_epochs() -> None:
    epochs = make_partitioned_epochs().copy().crop(tmin=1.0, tmax=2.0)

    with pytest.raises(eegnet.EEGNetError, match="no CSP-only crop"):
        eegnet.fit_eegnet(epochs)


def test_fit_eegnet_uses_training_partition_only_and_shuffles_train_loader(monkeypatch) -> None:
    epochs = make_partitioned_epochs()
    seen_loaders: list[tuple[str, int, bool]] = []
    original_build_data_loader = eegnet._build_data_loader

    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 1)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 1)

    def spy_build_data_loader(epoch_subset, *, label_column, partition_name, shuffle):
        seen_loaders.append((partition_name, len(epoch_subset), shuffle))
        return original_build_data_loader(
            epoch_subset,
            label_column=label_column,
            partition_name=partition_name,
            shuffle=shuffle,
        )

    monkeypatch.setattr(eegnet, "_build_data_loader", spy_build_data_loader)

    eegnet.fit_eegnet(epochs)

    assert seen_loaders[0] == ("train", 16, True)
    assert seen_loaders[1] == ("validation", 8, False)
    assert ("test", 8, False) in seen_loaders
    assert ("final_test", 8, False) in seen_loaders


def test_fit_eegnet_selects_validation_checkpoint_and_keeps_earliest_tie(monkeypatch) -> None:
    epochs = make_partitioned_epochs()
    validation_predictions = iter(
        (
            np.asarray([1, 1, 1, 0], dtype=np.int64),
            np.asarray([0, 1, 1, 1], dtype=np.int64),
            np.asarray([0, 1, 1, 1], dtype=np.int64),
            np.asarray([0, 1, 1, 0], dtype=np.int64),
        )
    )
    validation_truth = np.asarray([0, 0, 1, 1], dtype=np.int64)

    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 4)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 10)
    monkeypatch.setattr(eegnet, "_run_training_epoch", lambda *args, **kwargs: 0.1)

    def fake_evaluate_partition(model, *, loader, loss_function, device, partition_name):
        if partition_name == "validation" and len(getattr(fake_evaluate_partition, "seen", [])) < 4:
            fake_evaluate_partition.seen = getattr(fake_evaluate_partition, "seen", []) + [partition_name]
            predicted = next(validation_predictions)
            probabilities = np.zeros((4, 2), dtype=np.float32)
            probabilities[np.arange(4), predicted] = 1.0
            return eegnet._PartitionPredictions(
                partition_name=partition_name,
                loss=0.1,
                true_label_indices=validation_truth,
                predicted_label_indices=predicted,
                probabilities=probabilities,
            )
        perfect_truth = np.asarray([0, 1], dtype=np.int64)
        perfect_probabilities = np.asarray([[0.9, 0.1], [0.1, 0.9]], dtype=np.float32)
        return eegnet._PartitionPredictions(
            partition_name=partition_name,
            loss=0.1,
            true_label_indices=perfect_truth,
            predicted_label_indices=perfect_truth,
            probabilities=perfect_probabilities,
        )

    monkeypatch.setattr(eegnet, "_evaluate_partition", fake_evaluate_partition)

    result = eegnet.fit_eegnet(epochs)

    assert result.selected_epoch_index == 2
    assert result.best_validation_balanced_accuracy == 0.75
    assert [epoch.validation_balanced_accuracy for epoch in result.history] == [0.25, 0.75, 0.75, 0.5]


def test_predict_proba_preserves_softmax_normalization_and_class_order(monkeypatch) -> None:
    epochs = make_partitioned_epochs()
    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 2)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 2)

    result = eegnet.fit_eegnet(epochs)
    test_epochs = epochs[epochs.metadata["partition"] == "test"]
    probabilities = result.decoder.predict_proba(test_epochs)
    predictions = result.decoder.predict(test_epochs)

    assert result.decoder.class_labels == ("left", "right")
    assert probabilities.shape == (len(test_epochs), 2)
    np.testing.assert_allclose(probabilities.sum(axis=1), np.ones(len(test_epochs)), atol=1e-6)
    assert set(predictions.tolist()) <= {"left", "right"}


def test_fit_eegnet_keeps_final_test_out_of_selection(monkeypatch) -> None:
    baseline_epochs = make_partitioned_epochs()
    poisoned_epochs = make_partitioned_epochs()
    poisoned_data = poisoned_epochs.get_data(copy=True)
    final_test_mask = poisoned_epochs.metadata["partition"] == "final_test"
    poisoned_data[final_test_mask.to_numpy(), :, :] *= -50.0
    poisoned_epochs = mne.EpochsArray(
        data=poisoned_data,
        info=poisoned_epochs.info,
        events=poisoned_epochs.events,
        event_id=poisoned_epochs.event_id,
        tmin=poisoned_epochs.tmin,
        metadata=poisoned_epochs.metadata.copy(),
        verbose="ERROR",
    )

    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 2)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 2)

    baseline = eegnet.fit_eegnet(baseline_epochs)
    poisoned = eegnet.fit_eegnet(poisoned_epochs)

    assert baseline.selected_epoch_index == poisoned.selected_epoch_index
    assert baseline.best_validation_balanced_accuracy == poisoned.best_validation_balanced_accuracy
    assert baseline.history == poisoned.history


def test_fit_eegnet_accepts_within_subject_manifest_assignments(monkeypatch) -> None:
    epochs = make_within_subject_epochs()
    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 1)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 1)

    result = eegnet.fit_eegnet(epochs)

    assert result.selected_epoch_index == 1
    assert {metric.partition_name for metric in result.partition_metrics} >= {"validation", "test"}


def test_fit_eegnet_accepts_cross_subject_manifest_assignments(monkeypatch) -> None:
    epochs = make_cross_subject_epochs()
    monkeypatch.setattr(eegnet, "MAX_EPOCHS", 1)
    monkeypatch.setattr(eegnet, "EARLY_STOPPING_PATIENCE", 1)

    result = eegnet.fit_eegnet(epochs)

    assert result.selected_epoch_index == 1
    assert {metric.partition_name for metric in result.partition_metrics} >= {"validation", "final_test"}

