from __future__ import annotations

from pathlib import Path
import sys

import mne
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.eeg.loader import LoadedRecording, RecordingSummary
from src.eeg.preprocessing import (
    H_FREQ,
    L_FREQ,
    REFERENCE,
    PreprocessingValidationError,
    preprocess_recording,
)


def make_recording(*, sfreq: float = 160.0) -> LoadedRecording:
    n_times = int(sfreq * 20.0)
    rng = np.random.default_rng(7)
    data = rng.normal(scale=1e-6, size=(64, n_times))
    montage = mne.channels.make_standard_montage("standard_1005")
    channel_names = montage.ch_names[:64]
    info = mne.create_info(channel_names, sfreq=sfreq, ch_types="eeg")
    raw = mne.io.RawArray(data, info, verbose="ERROR")
    raw.set_montage(montage)
    raw.set_annotations(mne.Annotations([1.0, 8.0, 15.0], [0.0, 0.0, 0.0], ["T0", "T1", "T2"]))
    return LoadedRecording(
        raw=raw,
        summary=RecordingSummary(
            subject_id=1,
            run_id=4,
            file_path=Path("subject_1_run_4.edf"),
            channel_count=64,
            sampling_frequency=sfreq,
            duration_seconds=20.0,
            annotations=("T0", "T1", "T2"),
            montage_name="standard_1005",
        ),
    )


def test_preprocess_recording_applies_approved_parameters() -> None:
    recording = make_recording()
    preprocessed = preprocess_recording(recording)

    assert preprocessed.summary.l_freq == L_FREQ
    assert preprocessed.summary.h_freq == H_FREQ
    assert preprocessed.summary.reference == REFERENCE
    assert preprocessed.summary.channel_count == 64
    assert preprocessed.summary.sampling_frequency == 160.0
    assert tuple(preprocessed.raw.ch_names) == tuple(recording.raw.ch_names)


def test_preprocess_recording_preserves_sampling_rate_and_finite_values() -> None:
    preprocessed = preprocess_recording(make_recording())
    data = preprocessed.raw.get_data()

    assert float(preprocessed.raw.info["sfreq"]) == 160.0
    assert np.isfinite(data).all()


def test_preprocess_recording_rejects_unapproved_sampling_frequency() -> None:
    with pytest.raises(PreprocessingValidationError, match="Expected sampling frequency"):
        preprocess_recording(make_recording(sfreq=128.0))
