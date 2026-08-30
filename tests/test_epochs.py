from __future__ import annotations

from pathlib import Path
import sys

import mne
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.eeg.epochs import (
    EPOCH_TMAX,
    EPOCH_TMIN,
    REJECT_THRESHOLD_V,
    create_motor_imagery_epochs,
    extract_eegbci_events,
    save_epochs,
)
from src.eeg.loader import LoadedRecording, RecordingSummary
from src.eeg.preprocessing import PreprocessedRecording, PreprocessingSummary, preprocess_recording


def make_recording(*, inject_large_epoch: bool = False) -> LoadedRecording:
    sfreq = 160.0
    duration_seconds = 20.0
    n_times = int(sfreq * duration_seconds)
    data = np.zeros((64, n_times), dtype=float)
    rng = np.random.default_rng(11)
    data += rng.normal(scale=1e-6, size=data.shape)

    onsets = np.array([1.0, 8.0, 15.0])
    descriptions = ["T0", "T1", "T2"]
    if inject_large_epoch:
        start = int((onsets[2] + EPOCH_TMIN) * sfreq)
        stop = int((onsets[2] + EPOCH_TMAX) * sfreq) + 1
        midpoint = start + ((stop - start) // 2)
        data[:, start:midpoint] = -REJECT_THRESHOLD_V
        data[:, midpoint:stop] = REJECT_THRESHOLD_V

    montage = mne.channels.make_standard_montage("standard_1005")
    channel_names = montage.ch_names[:64]
    info = mne.create_info(channel_names, sfreq=sfreq, ch_types="eeg")
    raw = mne.io.RawArray(data, info, verbose="ERROR")
    raw.set_montage(montage)
    raw.set_annotations(mne.Annotations(onsets, [0.0, 0.0, 0.0], descriptions))

    return LoadedRecording(
        raw=raw,
        summary=RecordingSummary(
            subject_id=1,
            run_id=4,
            file_path=Path("subject_1_run_4.edf"),
            channel_count=64,
            sampling_frequency=sfreq,
            duration_seconds=duration_seconds,
            annotations=("T0", "T1", "T2"),
            montage_name="standard_1005",
        ),
    )


def test_extract_eegbci_events_preserves_t0_t1_t2() -> None:
    events, event_id = extract_eegbci_events(preprocess_recording(make_recording()))
    assert len(events) == 3
    assert event_id == {"T0": 1, "T1": 2, "T2": 3}


def test_create_motor_imagery_epochs_excludes_t0_and_preserves_metadata() -> None:
    result = create_motor_imagery_epochs(preprocess_recording(make_recording()))

    assert len(result.epochs) == 2
    assert result.labels == ("left", "right")
    assert result.t0_event_count == 1
    assert result.t1_event_count == 1
    assert result.t2_event_count == 1
    assert tuple(result.epochs.metadata["event_code"]) == ("T1", "T2")
    assert tuple(result.epochs.metadata["semantic_label"]) == ("left", "right")
    assert tuple(result.epochs.metadata["subject_id"]) == (1, 1)
    assert tuple(result.epochs.metadata["run_id"]) == (4, 4)
    assert all(value is False for value in result.epochs.metadata["baseline_applied"])


def test_create_motor_imagery_epochs_rejects_large_peak_to_peak_epochs() -> None:
    recording = make_recording(inject_large_epoch=True)
    preprocessed = PreprocessedRecording(
        raw=recording.raw,
        summary=PreprocessingSummary(
            subject_id=recording.summary.subject_id,
            run_id=recording.summary.run_id,
            source_file=recording.summary.file_path,
            l_freq=7.0,
            h_freq=30.0,
            reference="average",
            channel_count=recording.summary.channel_count,
            sampling_frequency=recording.summary.sampling_frequency,
        ),
    )
    result = create_motor_imagery_epochs(preprocessed)

    assert len(result.epochs) == 1
    assert result.labels == ("left",)
    assert len(result.rejection_log) == 1
    assert result.rejection_log[0].event_code == "T2"
    assert result.rejection_log[0].reason


def test_save_epochs_requires_epo_fif_suffix(tmp_path: Path) -> None:
    result = create_motor_imagery_epochs(preprocess_recording(make_recording()))

    with pytest.raises(Exception):
        save_epochs(result.epochs, tmp_path / "epochs.fif")

    output_path = save_epochs(result.epochs, tmp_path / "subject_1_run_4-epo.fif", overwrite=True)
    assert output_path.exists()
