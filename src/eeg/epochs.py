from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import mne
import numpy as np
import pandas as pd

from src.eeg.loader import LoadedRecording
from src.eeg.preprocessing import PreprocessedRecording, preprocess_recording

EVENT_CODE_MAP = {"T0": 1, "T1": 2, "T2": 3}
BINARY_EVENT_ID = {"left": EVENT_CODE_MAP["T1"], "right": EVENT_CODE_MAP["T2"]}
SEMANTIC_LABELS = {EVENT_CODE_MAP["T0"]: "rest", EVENT_CODE_MAP["T1"]: "left", EVENT_CODE_MAP["T2"]: "right"}
EPOCH_TMIN = -1.0
EPOCH_TMAX = 4.0
BASELINE = None
REJECT_THRESHOLD_UV = 150.0
REJECT_THRESHOLD_V = REJECT_THRESHOLD_UV * 1e-6


class EpochingValidationError(ValueError):
    """Raised when event extraction or epoch creation violates approved constraints."""


@dataclass(frozen=True)
class RejectedEpoch:
    subject_id: int | None
    run_id: int | None
    source_file: Path | None
    event_code: str
    semantic_label: str
    event_sample: int
    event_time_seconds: float
    reason: str
    reject_threshold_uv: float


@dataclass(frozen=True)
class EpochExtractionResult:
    epochs: mne.Epochs
    labels: tuple[str, ...]
    rejection_log: tuple[RejectedEpoch, ...]
    t0_event_count: int
    t1_event_count: int
    t2_event_count: int
    source_file: Path | None


def _coerce_preprocessed_recording(
    recording: LoadedRecording | PreprocessedRecording,
) -> tuple[mne.io.BaseRaw, int | None, int | None, Path | None]:
    if isinstance(recording, PreprocessedRecording):
        return (
            recording.raw,
            recording.summary.subject_id,
            recording.summary.run_id,
            recording.summary.source_file,
        )
    if isinstance(recording, LoadedRecording):
        preprocessed = preprocess_recording(recording)
        return (
            preprocessed.raw,
            preprocessed.summary.subject_id,
            preprocessed.summary.run_id,
            preprocessed.summary.source_file,
        )
    raise EpochingValidationError(
        f"Expected a LoadedRecording or PreprocessedRecording. Got {type(recording)!r}."
    )


def extract_eegbci_events(
    recording: LoadedRecording | PreprocessedRecording,
) -> tuple[np.ndarray, dict[str, int]]:
    raw, _, _, _ = _coerce_preprocessed_recording(recording)
    events, event_id = mne.events_from_annotations(raw, event_id=EVENT_CODE_MAP, verbose="ERROR")
    missing = [name for name in EVENT_CODE_MAP if name not in event_id]
    if missing:
        raise EpochingValidationError(f"Missing expected EEGBCI annotations: {', '.join(missing)}.")
    return events, event_id


def extract_events_from_raw(raw: mne.io.BaseRaw) -> tuple[np.ndarray, dict[str, int]]:
    events, event_id = mne.events_from_annotations(raw, event_id=EVENT_CODE_MAP, verbose="ERROR")
    missing = [name for name in EVENT_CODE_MAP if name not in event_id]
    if missing:
        raise EpochingValidationError(f"Missing expected EEGBCI annotations: {', '.join(missing)}.")
    return events, event_id


def _build_metadata(
    *,
    events: np.ndarray,
    subject_id: int | None,
    run_id: int | None,
    source_file: Path | None,
    sfreq: float,
) -> pd.DataFrame:
    id_to_code = {value: key for key, value in EVENT_CODE_MAP.items()}
    rows: list[dict[str, object]] = []
    for trial_index, event in enumerate(events):
        event_sample = int(event[0])
        event_code_id = int(event[2])
        semantic_label = SEMANTIC_LABELS[event_code_id]
        rows.append(
            {
                "trial_index": trial_index,
                "subject_id": subject_id,
                "run_id": run_id,
                "source_file": str(source_file) if source_file is not None else None,
                "event_code": id_to_code[event_code_id],
                "semantic_label": semantic_label,
                "event_sample": event_sample,
                "event_time_seconds": event_sample / sfreq,
                "channel_count": None,
                "sampling_frequency": sfreq,
                "epoch_tmin": EPOCH_TMIN,
                "epoch_tmax": EPOCH_TMAX,
                "baseline_applied": False,
            }
        )
    return pd.DataFrame(rows)


def create_motor_imagery_epochs(
    recording: LoadedRecording | PreprocessedRecording,
    *,
    reject_threshold_uv: float = REJECT_THRESHOLD_UV,
) -> EpochExtractionResult:
    if reject_threshold_uv != REJECT_THRESHOLD_UV:
        raise EpochingValidationError(
            f"M1-T03 only authorizes a {REJECT_THRESHOLD_UV:g} µV epoch peak-to-peak rejection threshold."
        )

    raw, subject_id, run_id, source_file = _coerce_preprocessed_recording(recording)
    events, _ = extract_events_from_raw(raw)
    sfreq = float(raw.info["sfreq"])
    metadata = _build_metadata(
        events=events,
        subject_id=subject_id,
        run_id=run_id,
        source_file=source_file,
        sfreq=sfreq,
    )
    metadata["channel_count"] = len(raw.ch_names)

    t0_mask = metadata["event_code"] == "T0"
    binary_mask = metadata["event_code"].isin(["T1", "T2"])
    binary_events = events[binary_mask.to_numpy()]
    binary_metadata = metadata.loc[binary_mask].reset_index(drop=True)

    if binary_events.size == 0:
        raise EpochingValidationError("No T1/T2 events were available for binary epoching.")

    epochs = mne.Epochs(
        raw,
        binary_events,
        event_id=BINARY_EVENT_ID,
        tmin=EPOCH_TMIN,
        tmax=EPOCH_TMAX,
        baseline=BASELINE,
        preload=True,
        metadata=binary_metadata,
        reject={"eeg": REJECT_THRESHOLD_V},
        reject_by_annotation=False,
        verbose="ERROR",
    )

    kept_metadata = epochs.metadata
    if kept_metadata is None:
        raise EpochingValidationError("Epoch metadata was not preserved.")
    kept_metadata = kept_metadata.reset_index(drop=True)

    rejection_log: list[RejectedEpoch] = []
    for event, row, drop_reasons in zip(binary_events, binary_metadata.to_dict("records"), epochs.drop_log):
        if not drop_reasons:
            continue
        rejection_log.append(
            RejectedEpoch(
                subject_id=subject_id,
                run_id=run_id,
                source_file=source_file,
                event_code=str(row["event_code"]),
                semantic_label=str(row["semantic_label"]),
                event_sample=int(event[0]),
                event_time_seconds=float(row["event_time_seconds"]),
                reason="; ".join(drop_reasons),
                reject_threshold_uv=REJECT_THRESHOLD_UV,
            )
        )

    if len(epochs) > 0:
        epoch_data = epochs.get_data()
        if np.isnan(epoch_data).any() or not np.isfinite(epoch_data).all():
            raise EpochingValidationError("Epoch data contains non-finite values.")

    labels = tuple(str(label) for label in kept_metadata["semantic_label"].tolist())
    if any(label not in ("left", "right") for label in labels):
        raise EpochingValidationError("Binary epochs include an unapproved label.")

    return EpochExtractionResult(
        epochs=epochs,
        labels=labels,
        rejection_log=tuple(rejection_log),
        t0_event_count=int(t0_mask.sum()),
        t1_event_count=int((metadata["event_code"] == "T1").sum()),
        t2_event_count=int((metadata["event_code"] == "T2").sum()),
        source_file=source_file,
    )


def save_epochs(epochs: mne.Epochs, output_path: str | Path, *, overwrite: bool = False) -> Path:
    path = Path(output_path).expanduser().resolve()
    if not path.name.endswith("-epo.fif"):
        raise EpochingValidationError("Persisted epochs must use the *-epo.fif naming convention.")
    path.parent.mkdir(parents=True, exist_ok=True)
    epochs.save(path, overwrite=overwrite, verbose="ERROR")
    return path
