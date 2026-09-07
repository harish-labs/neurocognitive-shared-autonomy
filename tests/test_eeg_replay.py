from __future__ import annotations

import mne
import numpy as np
import pandas as pd
import pytest

from src.eeg.replay import OfflineEpochReplay, ReplayValidationError


def make_epochs(count: int = 3) -> mne.EpochsArray:
    data = np.arange(count * 2 * 4, dtype=float).reshape(count, 2, 4)
    metadata_rows = []
    events = []
    for index in range(count):
        event_code, label, event_id = ("T1", "left", 2) if index % 2 == 0 else ("T2", "right", 3)
        sample = 100 + index * 160
        events.append([sample, 0, event_id])
        metadata_rows.append(
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
    return mne.EpochsArray(
        data,
        mne.create_info(["C3", "C4"], 160.0, "eeg"),
        events=np.asarray(events),
        event_id={"left": 2, "right": 3} if count > 1 else {"left": 2},
        metadata=pd.DataFrame(metadata_rows),
        verbose="ERROR",
    )


def test_replay_emits_one_ordered_observation_per_epoch() -> None:
    epochs = make_epochs()
    observations = tuple(OfflineEpochReplay(epochs))

    assert len(observations) == len(epochs)
    assert [item.replay_index for item in observations] == [0, 1, 2]
    assert [item.trial_index for item in observations] == [0, 1, 2]
    assert [item.semantic_label for item in observations] == ["left", "right", "left"]
    assert np.array_equal(observations[1].epoch_data, epochs.get_data()[1])
    assert observations[0].canonical_trial_identity == (1, 4, "subject_1_run_4.edf", 100, "T1")
    assert not observations[0].epoch_data.flags.writeable

    original_value = observations[1].epoch_data[0, 0]
    epochs._data[1, 0, 0] = -1.0
    assert observations[1].epoch_data[0, 0] == original_value


def test_replay_is_repeatable_and_ends_without_extra_observations() -> None:
    replay = OfflineEpochReplay(make_epochs(2))
    assert [item.canonical_trial_identity for item in replay] == [
        item.canonical_trial_identity for item in replay
    ]
    iterator = iter(replay)
    next(iterator)
    next(iterator)
    with pytest.raises(StopIteration):
        next(iterator)


@pytest.mark.parametrize(
    ("mutator", "message"),
    [
        (lambda epochs: setattr(epochs, "metadata", None), "metadata"),
        (lambda epochs: _drop_metadata_column(epochs, "source_file"), "missing required"),
        (lambda epochs: _replace_metadata_column(epochs, "subject_id", [None] * len(epochs)), "subject_id"),
        (lambda epochs: _replace_metadata_column(epochs, "event_code", ["T0"] * len(epochs)), "T1/T2"),
        (lambda epochs: _replace_metadata_column(epochs, "semantic_label", ["rest"] * len(epochs)), "semantics"),
        (lambda epochs: _replace_metadata_column(epochs, "event_sample", [-1] * len(epochs)), "event_sample"),
    ],
)
def test_replay_rejects_invalid_provenance(mutator, message: str) -> None:
    epochs = make_epochs(2)
    mutator(epochs)
    with pytest.raises(ReplayValidationError, match=message):
        OfflineEpochReplay(epochs)


def test_replay_rejects_duplicate_identity_and_nonfinite_data() -> None:
    duplicate_epochs = make_epochs(2)
    duplicate_epochs.metadata.loc[1, ["event_sample", "event_code"]] = [100, "T1"]
    duplicate_epochs.metadata.loc[1, "semantic_label"] = "left"
    with pytest.raises(ReplayValidationError, match="duplicate"):
        OfflineEpochReplay(duplicate_epochs)

    nonfinite_epochs = make_epochs(1)
    nonfinite_epochs._data[0, 0, 0] = np.nan
    with pytest.raises(ReplayValidationError, match="finite"):
        OfflineEpochReplay(nonfinite_epochs)


def test_replay_rejects_metadata_count_mismatch_before_iteration() -> None:
    epochs = make_epochs(2)
    epochs._metadata = epochs.metadata.iloc[:1].copy()

    with pytest.raises(ReplayValidationError, match="row count"):
        OfflineEpochReplay(epochs)


def _replace_metadata_column(epochs: mne.EpochsArray, column: str, values: list[object]) -> None:
    metadata = epochs.metadata.copy()
    metadata[column] = values
    epochs.metadata = metadata


def _drop_metadata_column(epochs: mne.EpochsArray, column: str) -> None:
    epochs.metadata = epochs.metadata.drop(columns=[column])
