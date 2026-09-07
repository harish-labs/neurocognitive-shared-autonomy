"""Deterministic replay of accepted offline EEG epochs under D-074."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import mne
import numpy as np
import pandas as pd

from src.eeg.splits import TRIAL_KEY_COLUMNS

REQUIRED_REPLAY_COLUMNS = (
    "trial_index",
    "subject_id",
    "run_id",
    "source_file",
    "event_code",
    "semantic_label",
    "event_sample",
)
_EVENT_LABELS = {"T1": "left", "T2": "right"}


class ReplayValidationError(ValueError):
    """Raised when accepted epoch provenance cannot support deterministic replay."""


@dataclass(frozen=True)
class ReplayObservation:
    """One immutable-provenance offline epoch observation."""

    epoch_data: np.ndarray
    subject_id: int
    run_id: int
    trial_index: int
    source_file: str
    event_code: str
    semantic_label: str
    event_sample: int
    replay_index: int
    canonical_trial_identity: tuple[int, int, str, int, str]


class OfflineEpochReplay:
    """Validate then replay accepted epochs in their supplied order, synchronously."""

    def __init__(self, epochs: mne.BaseEpochs) -> None:
        self._observations = self._validate_and_build(epochs)

    def __len__(self) -> int:
        return len(self._observations)

    def __iter__(self) -> Iterator[ReplayObservation]:
        return iter(self._observations)

    @staticmethod
    def _validate_and_build(epochs: mne.BaseEpochs) -> tuple[ReplayObservation, ...]:
        if not isinstance(epochs, mne.BaseEpochs) or len(epochs) == 0:
            raise ReplayValidationError("Replay requires a non-empty accepted MNE Epochs object.")

        metadata = epochs.metadata
        if metadata is None:
            raise ReplayValidationError("Replay requires preserved epoch metadata.")
        if not isinstance(metadata, pd.DataFrame) or len(metadata) != len(epochs):
            raise ReplayValidationError("Replay metadata row count must match the epoch count.")

        missing = [column for column in REQUIRED_REPLAY_COLUMNS if column not in metadata.columns]
        if missing:
            raise ReplayValidationError(
                "Replay metadata is missing required provenance columns: " + ", ".join(missing) + "."
            )

        data = epochs.get_data().copy()
        if data.shape[0] != len(metadata) or not np.isfinite(data).all():
            raise ReplayValidationError("Replay epoch data must be finite and aligned with metadata.")

        rows = metadata.loc[:, REQUIRED_REPLAY_COLUMNS].to_dict("records")
        identities: set[tuple[int, int, str, int, str]] = set()
        observations: list[ReplayObservation] = []
        for replay_index, row in enumerate(rows):
            subject_id = _positive_integer(row["subject_id"], "subject_id")
            run_id = _positive_integer(row["run_id"], "run_id")
            trial_index = _nonnegative_integer(row["trial_index"], "trial_index")
            event_sample = _nonnegative_integer(row["event_sample"], "event_sample")
            source_file = _required_text(row["source_file"], "source_file")
            event_code = _required_text(row["event_code"], "event_code")
            semantic_label = _required_text(row["semantic_label"], "semantic_label")
            if event_code not in _EVENT_LABELS:
                raise ReplayValidationError("Replay only accepts canonical T1/T2 event codes.")
            if semantic_label != _EVENT_LABELS[event_code]:
                raise ReplayValidationError("Replay semantic labels must match canonical T1/T2 semantics.")

            identity_values = {
                "subject_id": subject_id,
                "run_id": run_id,
                "source_file": source_file,
                "event_sample": event_sample,
                "event_code": event_code,
            }
            identity = tuple(identity_values[column] for column in TRIAL_KEY_COLUMNS)
            if identity in identities:
                raise ReplayValidationError("Replay input contains duplicate canonical original-trial identities.")
            identities.add(identity)

            epoch_data = data[replay_index].copy()
            epoch_data.setflags(write=False)
            observations.append(
                ReplayObservation(
                    epoch_data=epoch_data,
                    subject_id=subject_id,
                    run_id=run_id,
                    trial_index=trial_index,
                    source_file=source_file,
                    event_code=event_code,
                    semantic_label=semantic_label,
                    event_sample=event_sample,
                    replay_index=replay_index,
                    canonical_trial_identity=identity,
                )
            )
        return tuple(observations)


def _required_text(value: object, field_name: str) -> str:
    if value is None or pd.isna(value):
        raise ReplayValidationError(f"Replay provenance field '{field_name}' must be present.")
    text = str(value)
    if not text.strip():
        raise ReplayValidationError(f"Replay provenance field '{field_name}' must be non-empty.")
    return text


def _positive_integer(value: object, field_name: str) -> int:
    integer = _integer(value, field_name)
    if integer <= 0:
        raise ReplayValidationError(f"Replay provenance field '{field_name}' must be positive.")
    return integer


def _nonnegative_integer(value: object, field_name: str) -> int:
    integer = _integer(value, field_name)
    if integer < 0:
        raise ReplayValidationError(f"Replay provenance field '{field_name}' must be non-negative.")
    return integer


def _integer(value: object, field_name: str) -> int:
    if value is None or pd.isna(value) or isinstance(value, bool):
        raise ReplayValidationError(f"Replay provenance field '{field_name}' must be an integer.")
    try:
        integer = int(value)
    except (TypeError, ValueError) as error:
        raise ReplayValidationError(f"Replay provenance field '{field_name}' must be an integer.") from error
    if integer != value:
        raise ReplayValidationError(f"Replay provenance field '{field_name}' must be an integer.")
    return integer
