from __future__ import annotations

import mne
import numpy as np
import pandas as pd
import pytest

from src.eeg.replay import OfflineEpochReplay
from src.models.calibration import PlattScalingCalibrator, TemperatureScalingCalibrator
from src.models.csp_lda import CspLdaDecoder
from src.models.eegnet import EEGNetDecoder
from src.models.runtime_adapter import RuntimeAdapterError, decode_replay_observation


class RecordingCspDecoder(CspLdaDecoder):
    def __init__(self, output: np.ndarray, class_labels: tuple[str, ...] = ("left", "right")) -> None:
        self.output = output
        self.class_labels = class_labels
        self.received_epochs: mne.BaseEpochs | None = None

    def predict_proba(self, epochs: mne.BaseEpochs) -> np.ndarray:
        self.received_epochs = epochs
        return self.output


class RecordingEegNetDecoder(EEGNetDecoder):
    def __init__(self, output: np.ndarray, class_labels: tuple[str, ...] = ("left", "right")) -> None:
        self.output = output
        self.class_labels = class_labels
        self.received_epochs: mne.BaseEpochs | None = None
        self.predict_proba_called = False

    def predict_logits(self, epochs: mne.BaseEpochs) -> np.ndarray:
        self.received_epochs = epochs
        return self.output

    def predict_proba(self, epochs: mne.BaseEpochs) -> np.ndarray:
        self.predict_proba_called = True
        raise AssertionError("EEGNet runtime adapter must use logits before temperature scaling.")


class RecordingPlattCalibrator(PlattScalingCalibrator):
    def __init__(self, output: np.ndarray, **kwargs: object) -> None:
        super().__init__(slope=1.0, intercept=0.0, **kwargs)
        object.__setattr__(self, "output", output)
        object.__setattr__(self, "received_values", None)

    def predict_proba(self, probabilities: np.ndarray) -> np.ndarray:
        object.__setattr__(self, "received_values", probabilities)
        return self.output


class RecordingTemperatureCalibrator(TemperatureScalingCalibrator):
    def __init__(self, output: np.ndarray, **kwargs: object) -> None:
        super().__init__(temperature=1.0, **kwargs)
        object.__setattr__(self, "output", output)
        object.__setattr__(self, "received_values", None)

    def predict_proba(self, logits: np.ndarray) -> np.ndarray:
        object.__setattr__(self, "received_values", logits)
        return self.output


def make_epochs(count: int = 2) -> mne.EpochsArray:
    data = np.arange(count * 64 * 801, dtype=float).reshape(count, 64, 801)
    rows = []
    events = []
    for index in range(count):
        event_code, label, event_id = ("T1", "left", 2) if index % 2 == 0 else ("T2", "right", 3)
        sample = 100 + (index * 1000)
        rows.append(
            {
                "trial_index": index,
                "subject_id": 1,
                "run_id": 4,
                "source_file": "subject_1_run_4.edf",
                "event_code": event_code,
                "semantic_label": label,
                "event_sample": sample,
            }
        )
        events.append([sample, 0, event_id])
    return mne.EpochsArray(
        data,
        mne.create_info([f"EEG {index:03d}" for index in range(64)], 160.0, "eeg"),
        events=np.asarray(events),
        event_id={"left": 2, "right": 3},
        tmin=-1.0,
        metadata=pd.DataFrame(rows),
        verbose="ERROR",
    )


def test_csp_runtime_path_preserves_exact_provenance_and_source_structure() -> None:
    epochs = make_epochs()
    observation = tuple(OfflineEpochReplay(epochs))[1]
    original_source = epochs.get_data(copy=True)
    decoder = RecordingCspDecoder(np.asarray([[0.2, 0.8]]))
    calibrator = RecordingPlattCalibrator(np.asarray([[0.25, 0.75]]))

    decoded = decode_replay_observation(observation, epochs, decoder, calibrator)

    assert decoded.replay_index == observation.replay_index
    assert decoded.canonical_trial_identity == observation.canonical_trial_identity
    assert decoded.trial_index == observation.trial_index
    assert decoded.model_family == "csp_lda"
    assert decoded.class_labels == ("left", "right")
    np.testing.assert_array_equal(decoded.raw_decoder_output, [[0.2, 0.8]])
    np.testing.assert_array_equal(decoded.calibrated_probabilities, [[0.25, 0.75]])
    assert not decoded.raw_decoder_output.flags.writeable
    assert not decoded.calibrated_probabilities.flags.writeable
    assert decoder.received_epochs is not None
    assert decoder.received_epochs.ch_names == epochs.ch_names
    assert decoder.received_epochs.info["sfreq"] == epochs.info["sfreq"]
    assert decoder.received_epochs.tmin == epochs.tmin
    assert decoder.received_epochs.tmax == epochs.tmax
    np.testing.assert_array_equal(decoder.received_epochs.get_data(), epochs.get_data()[[1]])
    np.testing.assert_array_equal(epochs.get_data(), original_source)
    np.testing.assert_array_equal(calibrator.received_values, [[0.2, 0.8]])


def test_eegnet_runtime_path_uses_logits_before_temperature_scaling() -> None:
    epochs = make_epochs()
    observation = next(iter(OfflineEpochReplay(epochs)))
    decoder = RecordingEegNetDecoder(np.asarray([[2.0, -1.0]]))
    calibrator = RecordingTemperatureCalibrator(np.asarray([[0.95, 0.05]]))

    decoded = decode_replay_observation(observation, epochs, decoder, calibrator)

    assert decoded.model_family == "eegnet"
    np.testing.assert_array_equal(decoded.raw_decoder_output, [[2.0, -1.0]])
    np.testing.assert_array_equal(calibrator.received_values, [[2.0, -1.0]])
    assert not decoder.predict_proba_called


@pytest.mark.parametrize(
    "change",
    [
        lambda epochs: _replace_metadata_column(epochs, "trial_index", [9, 1]),
        lambda epochs: _replace_metadata_column(epochs, "semantic_label", ["right", "right"]),
        lambda epochs: epochs._data.__setitem__((0, 0, 0), -1.0),
    ],
)
def test_replay_source_mismatch_fails_closed(change) -> None:
    epochs = make_epochs()
    observation = next(iter(OfflineEpochReplay(epochs)))
    change(epochs)
    with pytest.raises(RuntimeAdapterError, match="provenance|data"):
        decode_replay_observation(
            observation,
            epochs,
            RecordingCspDecoder(np.asarray([[0.2, 0.8]])),
            RecordingPlattCalibrator(np.asarray([[0.2, 0.8]])),
        )


def test_no_source_match_and_ambiguous_source_match_fail_closed() -> None:
    epochs = make_epochs()
    observation = next(iter(OfflineEpochReplay(epochs)))
    unmatched = make_epochs()
    unmatched.metadata.loc[0, "event_sample"] = 999
    with pytest.raises(RuntimeAdapterError, match="exactly one"):
        decode_replay_observation(
            observation,
            unmatched,
            RecordingCspDecoder(np.asarray([[0.2, 0.8]])),
            RecordingPlattCalibrator(np.asarray([[0.2, 0.8]])),
        )

    ambiguous = make_epochs()
    ambiguous.metadata.loc[1, ["event_sample", "event_code", "semantic_label"]] = [100, "T1", "left"]
    with pytest.raises(RuntimeAdapterError, match="exactly one"):
        decode_replay_observation(
            observation,
            ambiguous,
            RecordingCspDecoder(np.asarray([[0.2, 0.8]])),
            RecordingPlattCalibrator(np.asarray([[0.2, 0.8]])),
        )


@pytest.mark.parametrize(
    ("decoder", "calibrator", "message"),
    [
        (RecordingCspDecoder(np.asarray([[0.2, 0.8]])), RecordingTemperatureCalibrator(np.asarray([[0.2, 0.8]])), "pairing"),
        (RecordingEegNetDecoder(np.asarray([[0.2, 0.8]])), RecordingPlattCalibrator(np.asarray([[0.2, 0.8]])), "pairing"),
        (object(), RecordingPlattCalibrator(np.asarray([[0.2, 0.8]])), "pairing"),
        (RecordingCspDecoder(np.asarray([[0.2, 0.8]])), object(), "pairing"),
        (RecordingCspDecoder(np.asarray([[0.2, 0.8]]), ("right", "left")), RecordingPlattCalibrator(np.asarray([[0.2, 0.8]])), "class order"),
        (RecordingCspDecoder(np.asarray([[0.2, 0.8]])), RecordingPlattCalibrator(np.asarray([[0.2, 0.8]]), class_labels=("right", "left")), "class order"),
        (RecordingCspDecoder(np.asarray([[0.2, 0.8]])), RecordingPlattCalibrator(np.asarray([[0.2, 0.8]]), model_family="eegnet"), "model family"),
    ],
)
def test_invalid_runtime_pairs_and_class_contracts_fail_closed(decoder, calibrator, message: str) -> None:
    epochs = make_epochs()
    observation = next(iter(OfflineEpochReplay(epochs)))
    with pytest.raises(RuntimeAdapterError, match=message):
        decode_replay_observation(observation, epochs, decoder, calibrator)


@pytest.mark.parametrize(
    "raw_output",
    [
        np.asarray([0.2, 0.8]),
        np.asarray([[0.2, 0.8], [0.3, 0.7]]),
        np.asarray([[0.1, 0.2, 0.7]]),
        np.asarray([[np.nan, 0.8]]),
    ],
)
def test_malformed_raw_output_fails_closed(raw_output: np.ndarray) -> None:
    epochs = make_epochs()
    with pytest.raises(RuntimeAdapterError, match="raw output"):
        decode_replay_observation(
            next(iter(OfflineEpochReplay(epochs))),
            epochs,
            RecordingCspDecoder(raw_output),
            RecordingPlattCalibrator(np.asarray([[0.2, 0.8]])),
        )


@pytest.mark.parametrize(
    "calibrated_output",
    [
        np.asarray([0.2, 0.8]),
        np.asarray([[0.2, 0.8], [0.3, 0.7]]),
        np.asarray([[0.1, 0.2, 0.7]]),
        np.asarray([[np.nan, 0.8]]),
        np.asarray([[-0.1, 1.1]]),
        np.asarray([[1.1, 0.0]]),
        np.asarray([[0.2, 0.2]]),
    ],
)
def test_malformed_calibrated_output_fails_closed(calibrated_output: np.ndarray) -> None:
    epochs = make_epochs()
    with pytest.raises(RuntimeAdapterError, match="Calibrated probabilities"):
        decode_replay_observation(
            next(iter(OfflineEpochReplay(epochs))),
            epochs,
            RecordingCspDecoder(np.asarray([[0.2, 0.8]])),
            RecordingPlattCalibrator(calibrated_output),
        )


def _replace_metadata_column(epochs: mne.BaseEpochs, column: str, values: list[object]) -> None:
    metadata = epochs.metadata.copy()
    metadata[column] = values
    epochs.metadata = metadata
