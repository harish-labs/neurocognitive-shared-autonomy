from __future__ import annotations

from pathlib import Path
import sys

import mne
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.eeg.splits import (
    FULL_ELIGIBLE_SUBJECT_COUNT,
    assign_cross_subject_partitions,
    assign_within_subject_partitions,
    build_cross_subject_split_manifest,
    build_within_subject_split_manifest,
)
from src.models import csp_lda


def make_partitioned_epochs() -> mne.Epochs:
    sfreq = 160.0
    n_times = int((csp_lda.EPOCH_TMAX - csp_lda.EPOCH_TMIN) * sfreq) + 1
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

    sample_cursor = 1_000
    trial_index = 0
    rng = np.random.default_rng(5)
    crop_start = int((csp_lda.CSP_CROP_TMIN - csp_lda.EPOCH_TMIN) * sfreq)
    crop_stop = int((csp_lda.CSP_CROP_TMAX - csp_lda.EPOCH_TMIN) * sfreq) + 1
    for partition, semantic_label, event_code, count in partition_plan:
        amplitude = 4.0 if semantic_label == "left" else -4.0
        for example_index in range(count):
            epoch = rng.normal(scale=0.05, size=(64, n_times))
            epoch[0, crop_start:crop_stop] += amplitude
            epoch[1, crop_start:crop_stop] += amplitude * 0.5
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
            sample_cursor += n_times + 10
            trial_index += 1

    return mne.EpochsArray(
        data=np.asarray(data_rows),
        info=info,
        events=np.asarray(events),
        event_id={"left": 2, "right": 3},
        tmin=csp_lda.EPOCH_TMIN,
        metadata=pd.DataFrame(metadata_rows),
        verbose="ERROR",
    )


def make_within_subject_epochs() -> mne.Epochs:
    sfreq = 160.0
    n_times = int((csp_lda.EPOCH_TMAX - csp_lda.EPOCH_TMIN) * sfreq) + 1
    info = mne.create_info([f"EEG{i:02d}" for i in range(64)], sfreq=sfreq, ch_types="eeg")
    data_rows: list[np.ndarray] = []
    events: list[list[int]] = []
    metadata_rows: list[dict[str, object]] = []
    rng = np.random.default_rng(9)
    crop_start = int((csp_lda.CSP_CROP_TMIN - csp_lda.EPOCH_TMIN) * sfreq)
    crop_stop = int((csp_lda.CSP_CROP_TMAX - csp_lda.EPOCH_TMIN) * sfreq) + 1
    sample_cursor = 200
    trial_index = 0
    for run_id, base_sample in zip((4, 8, 12), (200, 10_200, 20_200), strict=True):
        for semantic_label, event_code in (("left", "T1"), ("right", "T2")) * 3:
            epoch = rng.normal(scale=0.05, size=(64, n_times))
            amplitude = 3.0 if semantic_label == "left" else -3.0
            epoch[0, crop_start:crop_stop] += amplitude
            epoch[1, crop_start:crop_stop] += amplitude * 0.5
            events.append([sample_cursor, 0, 2 if semantic_label == "left" else 3])
            metadata_rows.append(
                {
                    "subject_id": 1,
                    "run_id": run_id,
                    "source_file": f"subject_1_run_{run_id}.edf",
                    "event_code": event_code,
                    "semantic_label": semantic_label,
                    "event_sample": base_sample + trial_index * 160,
                    "trial_index": trial_index,
                }
            )
            data_rows.append(epoch)
            sample_cursor += n_times + 10
            trial_index += 1

    epochs = mne.EpochsArray(
        data=np.asarray(data_rows),
        info=info,
        events=np.asarray(events),
        event_id={"left": 2, "right": 3},
        tmin=csp_lda.EPOCH_TMIN,
        metadata=pd.DataFrame(metadata_rows),
        verbose="ERROR",
    )
    manifest = build_within_subject_split_manifest(epochs.metadata)
    epochs.metadata = assign_within_subject_partitions(epochs.metadata, manifest).reset_index(drop=True)
    return epochs


def test_crop_epochs_for_csp_uses_approved_window() -> None:
    epochs = make_partitioned_epochs()
    cropped = csp_lda.crop_epochs_for_csp(epochs)

    assert cropped.tmin == csp_lda.CSP_CROP_TMIN
    assert cropped.tmax == csp_lda.CSP_CROP_TMAX
    assert len(cropped.ch_names) == 64


def test_fit_csp_lda_uses_training_partition_only(monkeypatch) -> None:
    epochs = make_partitioned_epochs()
    train_count = int((epochs.metadata["partition"] == "train").sum())
    seen_fit_sizes: list[int] = []

    original_csp_fit = csp_lda.CSP.fit
    original_lda_fit = csp_lda.LinearDiscriminantAnalysis.fit

    def spy_csp_fit(self, X, y, **kwargs):
        seen_fit_sizes.append(len(y))
        return original_csp_fit(self, X, y, **kwargs)

    def spy_lda_fit(self, X, y, **kwargs):
        seen_fit_sizes.append(len(y))
        return original_lda_fit(self, X, y, **kwargs)

    monkeypatch.setattr(csp_lda.CSP, "fit", spy_csp_fit)
    monkeypatch.setattr(csp_lda.LinearDiscriminantAnalysis, "fit", spy_lda_fit)

    result = csp_lda.fit_csp_lda(epochs)

    assert result.selected_n_components in csp_lda.APPROVED_CSP_COMPONENT_CANDIDATES
    assert seen_fit_sizes
    assert all(size == train_count for size in seen_fit_sizes)


def test_fit_csp_lda_evaluates_all_approved_candidates_and_tie_breaks_to_default(monkeypatch) -> None:
    epochs = make_partitioned_epochs()
    seen_candidates: list[int] = []

    def spy_score(decoder, epochs_obj, **kwargs):
        seen_candidates.append(decoder._csp.n_components)  # noqa: SLF001
        return 0.5

    monkeypatch.setattr(csp_lda, "_score_decoder_on_partition", spy_score)
    result = csp_lda.fit_csp_lda(epochs)

    assert tuple(seen_candidates) == (4, 2, 6, 8)
    assert result.selected_n_components == csp_lda.DEFAULT_CSP_COMPONENT


def test_predict_proba_preserves_probability_shape_and_class_order() -> None:
    epochs = make_partitioned_epochs()
    result = csp_lda.fit_csp_lda(epochs)

    test_epochs = epochs[epochs.metadata["partition"] == "test"]
    probabilities = result.decoder.predict_proba(test_epochs)

    assert result.decoder.class_labels == ("left", "right")
    assert probabilities.shape == (len(test_epochs), 2)
    np.testing.assert_allclose(probabilities.sum(axis=1), np.ones(len(test_epochs)), atol=1e-6)


def test_final_test_partition_does_not_influence_selection() -> None:
    baseline_epochs = make_partitioned_epochs()
    poisoned_epochs = make_partitioned_epochs()
    poisoned_mask = poisoned_epochs.metadata["partition"] == "final_test"
    poisoned_data = poisoned_epochs.get_data(copy=True)
    poisoned_data[poisoned_mask.to_numpy(), :, :] *= -25.0
    poisoned_epochs = mne.EpochsArray(
        data=poisoned_data,
        info=poisoned_epochs.info,
        events=poisoned_epochs.events,
        event_id=poisoned_epochs.event_id,
        tmin=poisoned_epochs.tmin,
        metadata=poisoned_epochs.metadata.copy(),
        verbose="ERROR",
    )

    baseline = csp_lda.fit_csp_lda(baseline_epochs)
    poisoned = csp_lda.fit_csp_lda(poisoned_epochs)

    assert baseline.selected_n_components == poisoned.selected_n_components
    assert baseline.candidate_scores == poisoned.candidate_scores


def test_fit_csp_lda_accepts_within_subject_manifest_assignments() -> None:
    epochs = make_within_subject_epochs()
    result = csp_lda.fit_csp_lda(epochs)

    assert result.selected_n_components in csp_lda.APPROVED_CSP_COMPONENT_CANDIDATES
    assert {score.n_components for score in result.candidate_scores} == set(
        csp_lda.APPROVED_CSP_COMPONENT_CANDIDATES
    )


def test_fit_csp_lda_handles_cross_subject_partition_names() -> None:
    base_epochs = make_partitioned_epochs()
    metadata_rows: list[dict[str, object]] = []
    data_rows: list[np.ndarray] = []
    events: list[list[int]] = []
    rng = np.random.default_rng(17)
    sample_cursor = 500
    n_times = len(base_epochs.times)
    crop_start = int((csp_lda.CSP_CROP_TMIN - csp_lda.EPOCH_TMIN) * 160.0)
    crop_stop = int((csp_lda.CSP_CROP_TMAX - csp_lda.EPOCH_TMIN) * 160.0) + 1
    for subject_id in range(1, FULL_ELIGIBLE_SUBJECT_COUNT + 1):
        for semantic_label, event_code in (("left", "T1"), ("right", "T2")):
            epoch = rng.normal(scale=0.03, size=(64, n_times))
            amplitude = 2.5 if semantic_label == "left" else -2.5
            epoch[0, crop_start:crop_stop] += amplitude
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
            data_rows.append(epoch)
            events.append([sample_cursor, 0, 2 if semantic_label == "left" else 3])
            sample_cursor += n_times + 5

    cross_epochs = mne.EpochsArray(
        data=np.asarray(data_rows),
        info=base_epochs.info,
        events=np.asarray(events),
        event_id={"left": 2, "right": 3},
        tmin=csp_lda.EPOCH_TMIN,
        metadata=pd.DataFrame(metadata_rows),
        verbose="ERROR",
    )
    manifest = build_cross_subject_split_manifest(list(range(1, FULL_ELIGIBLE_SUBJECT_COUNT + 1)))
    cross_epochs.metadata = assign_cross_subject_partitions(cross_epochs.metadata, manifest).reset_index(drop=True)

    result = csp_lda.fit_csp_lda(cross_epochs)
    final_test_epochs = cross_epochs[cross_epochs.metadata["partition"] == "final_test"]
    probabilities = result.decoder.predict_proba(final_test_epochs[:4])

    assert result.selected_n_components in csp_lda.APPROVED_CSP_COMPONENT_CANDIDATES
    assert probabilities.shape == (4, 2)
