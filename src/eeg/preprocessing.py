from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mne.io import BaseRaw

from src.eeg.loader import (
    EXPECTED_CHANNEL_COUNT,
    EXPECTED_SAMPLING_FREQUENCY,
    LoadedRecording,
)

L_FREQ = 7.0
H_FREQ = 30.0
REFERENCE = "average"


class PreprocessingValidationError(ValueError):
    """Raised when preprocessing violates the approved M1-T03 constraints."""


@dataclass(frozen=True)
class PreprocessingSummary:
    subject_id: int
    run_id: int
    source_file: Path
    l_freq: float
    h_freq: float
    reference: str
    channel_count: int
    sampling_frequency: float


@dataclass(frozen=True)
class PreprocessedRecording:
    raw: BaseRaw
    summary: PreprocessingSummary


def preprocess_recording(recording: LoadedRecording) -> PreprocessedRecording:
    raw = recording.raw.copy()
    summary = recording.summary

    if len(raw.ch_names) != EXPECTED_CHANNEL_COUNT:
        raise PreprocessingValidationError(
            f"Expected {EXPECTED_CHANNEL_COUNT} channels before preprocessing, found {len(raw.ch_names)}."
        )

    sfreq = float(raw.info["sfreq"])
    if sfreq != EXPECTED_SAMPLING_FREQUENCY:
        raise PreprocessingValidationError(
            f"Expected sampling frequency {EXPECTED_SAMPLING_FREQUENCY} Hz before preprocessing, found {sfreq} Hz."
        )

    original_channel_order = tuple(raw.ch_names)
    raw.load_data()
    raw.filter(l_freq=L_FREQ, h_freq=H_FREQ, picks="eeg", verbose="ERROR")
    raw.set_eeg_reference(ref_channels=REFERENCE, projection=False, verbose="ERROR")

    if tuple(raw.ch_names) != original_channel_order:
        raise PreprocessingValidationError("Channel order changed during preprocessing.")

    filtered_sfreq = float(raw.info["sfreq"])
    if filtered_sfreq != EXPECTED_SAMPLING_FREQUENCY:
        raise PreprocessingValidationError("Preprocessing changed the approved native sampling frequency.")

    return PreprocessedRecording(
        raw=raw,
        summary=PreprocessingSummary(
            subject_id=summary.subject_id,
            run_id=summary.run_id,
            source_file=summary.file_path,
            l_freq=L_FREQ,
            h_freq=H_FREQ,
            reference=REFERENCE,
            channel_count=len(raw.ch_names),
            sampling_frequency=filtered_sfreq,
        ),
    )
