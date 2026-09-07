"""Synchronous D-074 through D-076 replay-to-decoder runtime boundary."""

from __future__ import annotations

from dataclasses import dataclass

import mne
import numpy as np
import pandas as pd

from src.eeg.replay import REQUIRED_REPLAY_COLUMNS, ReplayObservation
from src.eeg.splits import TRIAL_KEY_COLUMNS
from src.models.calibration import (
    CSP_LDA_MODEL_FAMILY,
    EEGNET_MODEL_FAMILY,
    PlattScalingCalibrator,
    TemperatureScalingCalibrator,
)
from src.models.csp_lda import CspLdaDecoder
from src.models.eegnet import EEGNetDecoder

CLASS_LABELS = ("left", "right")


class RuntimeAdapterError(ValueError):
    """Raised when replay evidence cannot safely reach a decoder runtime path."""


@dataclass(frozen=True)
class DecodedReplayObservation:
    """Immutable calibrated decoder evidence for one accepted replay observation."""

    replay_index: int
    canonical_trial_identity: tuple[int, int, str, int, str]
    subject_id: int
    run_id: int
    trial_index: int
    source_file: str
    event_code: str
    semantic_label: str
    event_sample: int
    model_family: str
    class_labels: tuple[str, str]
    raw_decoder_output: np.ndarray
    calibrated_probabilities: np.ndarray


def decode_replay_observation(
    replay_observation: ReplayObservation,
    source_epochs: mne.BaseEpochs,
    decoder: CspLdaDecoder | EEGNetDecoder,
    calibrator: PlattScalingCalibrator | TemperatureScalingCalibrator,
) -> DecodedReplayObservation:
    """Decode one replay observation through its approved decoder/calibrator pair."""

    single_epoch = _matching_source_epoch(replay_observation, source_epochs)
    model_family = _validate_runtime_pair(decoder, calibrator)

    if model_family == CSP_LDA_MODEL_FAMILY:
        raw_output = decoder.predict_proba(single_epoch)
    else:
        raw_output = decoder.predict_logits(single_epoch)
    raw_output = _validated_row(raw_output, "Decoder raw output")

    calibrated = calibrator.predict_proba(raw_output)
    calibrated = _validated_probabilities(calibrated)

    return DecodedReplayObservation(
        replay_index=replay_observation.replay_index,
        canonical_trial_identity=replay_observation.canonical_trial_identity,
        subject_id=replay_observation.subject_id,
        run_id=replay_observation.run_id,
        trial_index=replay_observation.trial_index,
        source_file=replay_observation.source_file,
        event_code=replay_observation.event_code,
        semantic_label=replay_observation.semantic_label,
        event_sample=replay_observation.event_sample,
        model_family=model_family,
        class_labels=CLASS_LABELS,
        raw_decoder_output=_readonly_copy(raw_output),
        calibrated_probabilities=_readonly_copy(calibrated),
    )


def _matching_source_epoch(
    replay_observation: ReplayObservation,
    source_epochs: mne.BaseEpochs,
) -> mne.BaseEpochs:
    if not isinstance(replay_observation, ReplayObservation):
        raise RuntimeAdapterError("Runtime input must be a ReplayObservation.")
    if not isinstance(source_epochs, mne.BaseEpochs) or len(source_epochs) == 0:
        raise RuntimeAdapterError("Canonical source must be a non-empty MNE Epochs object.")

    metadata = source_epochs.metadata
    if not isinstance(metadata, pd.DataFrame) or len(metadata) != len(source_epochs):
        raise RuntimeAdapterError("Canonical source epochs must have aligned metadata.")
    missing = [column for column in REQUIRED_REPLAY_COLUMNS if column not in metadata.columns]
    if missing:
        raise RuntimeAdapterError("Canonical source metadata is missing required replay provenance.")

    expected_identity = _canonical_identity_from_observation(replay_observation)
    if replay_observation.canonical_trial_identity != expected_identity:
        raise RuntimeAdapterError("Replay observation canonical identity is inconsistent with its provenance.")

    matching_positions = [
        position
        for position, row in enumerate(metadata.loc[:, REQUIRED_REPLAY_COLUMNS].to_dict("records"))
        if _canonical_identity_from_row(row) == expected_identity
    ]
    if len(matching_positions) != 1:
        raise RuntimeAdapterError("Replay observation must match exactly one canonical source epoch.")

    position = matching_positions[0]
    source_row = metadata.iloc[position]
    _verify_provenance(replay_observation, source_row)
    source_data = source_epochs.get_data(copy=True)[position]
    if not np.array_equal(source_data, replay_observation.epoch_data):
        raise RuntimeAdapterError("Replay observation data differs from its canonical source epoch.")

    return source_epochs[[position]].copy()


def _validate_runtime_pair(
    decoder: object,
    calibrator: object,
) -> str:
    if isinstance(decoder, CspLdaDecoder) and isinstance(calibrator, PlattScalingCalibrator):
        model_family = CSP_LDA_MODEL_FAMILY
    elif isinstance(decoder, EEGNetDecoder) and isinstance(calibrator, TemperatureScalingCalibrator):
        model_family = EEGNET_MODEL_FAMILY
    else:
        raise RuntimeAdapterError("Unsupported decoder/calibrator runtime pairing.")

    if tuple(decoder.class_labels) != CLASS_LABELS:
        raise RuntimeAdapterError("Decoder must preserve the approved class order ('left', 'right').")
    if tuple(calibrator.class_labels) != CLASS_LABELS:
        raise RuntimeAdapterError("Calibrator must preserve the approved class order ('left', 'right').")
    if calibrator.model_family != model_family:
        raise RuntimeAdapterError("Calibrator model family is incompatible with the decoder.")
    return model_family


def _canonical_identity_from_observation(
    observation: ReplayObservation) -> tuple[int, int, str, int, str]:
    return (
        observation.subject_id,
        observation.run_id,
        observation.source_file,
        observation.event_sample,
        observation.event_code,
    )


def _canonical_identity_from_row(row: dict[str, object]) -> tuple[int, int, str, int, str]:
    return tuple(row[column] for column in TRIAL_KEY_COLUMNS)  # type: ignore[return-value]


def _verify_provenance(replay_observation: ReplayObservation, source_row: pd.Series) -> None:
    for field in REQUIRED_REPLAY_COLUMNS:
        if source_row[field] != getattr(replay_observation, field):
            raise RuntimeAdapterError("Replay provenance differs from its canonical source epoch.")


def _validated_row(values: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if array.shape != (1, len(CLASS_LABELS)):
        raise RuntimeAdapterError(f"{name} must have shape (1, 2).")
    if not np.isfinite(array).all():
        raise RuntimeAdapterError(f"{name} must be finite.")
    return array


def _validated_probabilities(values: np.ndarray) -> np.ndarray:
    probabilities = _validated_row(values, "Calibrated probabilities")
    if (probabilities < 0.0).any() or (probabilities > 1.0).any():
        raise RuntimeAdapterError("Calibrated probabilities must be within [0, 1].")
    if not np.isclose(probabilities.sum(), 1.0, rtol=1e-7, atol=1e-6):
        raise RuntimeAdapterError("Calibrated probabilities must sum to one.")
    return probabilities


def _readonly_copy(values: np.ndarray) -> np.ndarray:
    copied = np.asarray(values, dtype=np.float64).copy()
    copied.setflags(write=False)
    return copied
