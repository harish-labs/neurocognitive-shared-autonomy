from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.eeg import loader


class FakeMontage:
    def __init__(self, name: str) -> None:
        self.name = name


class FakeAnnotations:
    def __init__(self, descriptions: list[str]) -> None:
        self.description = np.array(descriptions, dtype=object)


class FakeRaw:
    def __init__(
        self,
        *,
        channel_count: int = loader.EXPECTED_CHANNEL_COUNT,
        sfreq: float = loader.EXPECTED_SAMPLING_FREQUENCY,
        annotations: list[str] | None = None,
        n_times: int = 20000,
    ) -> None:
        self.ch_names = [f"Fc{i}." for i in range(channel_count)]
        self.info = {"sfreq": sfreq}
        self.annotations = FakeAnnotations(annotations or ["T0", "T1", "T2"])
        self.n_times = n_times
        self._montage = None

    def set_montage(self, montage: FakeMontage) -> None:
        self._montage = montage

    def get_montage(self) -> FakeMontage | None:
        return self._montage


def test_validate_subject_ids_deduplicates_and_preserves_order() -> None:
    assert loader.validate_subject_ids([1, 2, 2, 3]) == [1, 2, 3]


@pytest.mark.parametrize("subject_ids", ([0], [110], [True], ["1"]))
def test_validate_subject_ids_rejects_invalid_values(subject_ids: list[object]) -> None:
    with pytest.raises(loader.LoaderValidationError):
        loader.validate_subject_ids(subject_ids)  # type: ignore[arg-type]


def test_validate_run_ids_defaults_to_approved_runs() -> None:
    assert loader.validate_run_ids(None) == [4, 8, 12]


def test_validate_run_ids_rejects_out_of_scope_runs() -> None:
    with pytest.raises(loader.LoaderValidationError):
        loader.validate_run_ids([4, 3])


def test_load_subject_recordings_uses_expected_mne_workflow(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    seen: dict[str, object] = {}
    fake_raws = [FakeRaw(), FakeRaw()]

    def fake_load_data(subjects: int, runs: list[int], *, path: str, update_path: bool, verbose: str | None) -> list[str]:
        seen["load_data"] = {
            "subjects": subjects,
            "runs": runs,
            "path": path,
            "update_path": update_path,
            "verbose": verbose,
        }
        return [str(tmp_path / "S001R04.edf"), str(tmp_path / "S001R08.edf")]

    def fake_read_raw_edf(file_path: Path, *, preload: bool, verbose: str | None) -> FakeRaw:
        seen.setdefault("read_raw_edf", []).append(
            {"file_path": str(file_path), "preload": preload, "verbose": verbose}
        )
        return fake_raws.pop(0)

    def fake_standardize(raw: FakeRaw) -> None:
        seen["standardize_calls"] = int(seen.get("standardize_calls", 0)) + 1
        raw.ch_names = [name.replace(".", "").upper() for name in raw.ch_names]

    def fake_make_standard_montage(name: str) -> FakeMontage:
        seen["montage_name"] = name
        return FakeMontage(name)

    monkeypatch.setattr(loader.eegbci, "load_data", fake_load_data)
    monkeypatch.setattr(loader, "read_raw_edf", fake_read_raw_edf)
    monkeypatch.setattr(loader.eegbci, "standardize", fake_standardize)
    monkeypatch.setattr(loader.mne.channels, "make_standard_montage", fake_make_standard_montage)

    recordings = loader.load_subject_recordings(
        1,
        run_ids=[4, 8],
        data_path=tmp_path,
        preload=True,
    )

    assert len(recordings) == 2
    assert seen["load_data"] == {
        "subjects": 1,
        "runs": [4, 8],
        "path": str(tmp_path.resolve()),
        "update_path": False,
        "verbose": "ERROR",
    }
    assert seen["montage_name"] == loader.DEFAULT_MONTAGE_NAME
    assert seen["standardize_calls"] == 2
    assert recordings[0].summary.run_id == 4
    assert recordings[1].summary.run_id == 8
    assert recordings[0].summary.channel_count == loader.EXPECTED_CHANNEL_COUNT
    assert recordings[0].summary.annotations == ("T0", "T1", "T2")
    assert recordings[0].summary.file_path == (tmp_path / "S001R04.edf").resolve()


def test_load_subject_recordings_rejects_sampling_frequency_mismatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        loader.eegbci,
        "load_data",
        lambda *args, **kwargs: [str(tmp_path / "S001R04.edf")],
    )
    monkeypatch.setattr(
        loader,
        "read_raw_edf",
        lambda *args, **kwargs: FakeRaw(sfreq=128.0),
    )
    monkeypatch.setattr(
        loader.eegbci,
        "standardize",
        lambda raw: None,
    )
    monkeypatch.setattr(
        loader.mne.channels,
        "make_standard_montage",
        lambda name: FakeMontage(name),
    )

    with pytest.raises(loader.LoaderValidationError, match="sampling frequency"):
        loader.load_subject_recordings(1, run_ids=[4], data_path=tmp_path)


def test_format_recording_report_includes_required_metadata(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        loader.eegbci,
        "load_data",
        lambda *args, **kwargs: [str(tmp_path / "S001R04.edf")],
    )
    monkeypatch.setattr(loader, "read_raw_edf", lambda *args, **kwargs: FakeRaw())
    monkeypatch.setattr(loader.eegbci, "standardize", lambda raw: None)
    monkeypatch.setattr(
        loader.mne.channels,
        "make_standard_montage",
        lambda name: FakeMontage(name),
    )

    recording = loader.load_subject_recordings(1, run_ids=[4], data_path=tmp_path)[0]
    report = loader.format_recording_report(recording)

    assert "Subject 1" in report
    assert "Run 4" in report
    assert "Channels 64" in report
    assert "Sampling 160.0 Hz" in report
    assert "Annotations [T0, T1, T2]" in report
    assert f"Montage {loader.DEFAULT_MONTAGE_NAME}" in report
