from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
import numpy as np
import pytest
import mne

matplotlib.use("Agg")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.eeg.loader import LoadedRecording, RecordingSummary
from src.eeg.visualization import (
    VisualizationValidationError,
    extract_annotation_overview,
    extract_recording_metadata,
    inspect_recording,
    plot_annotation_overview,
    plot_psd,
    plot_raw_traces,
    plot_sensor_layout,
    save_figure,
)


def make_loaded_recording() -> LoadedRecording:
    sfreq = 160.0
    channel_names = ["Fp1", "Fp2", "C3", "C4"]
    info = mne.create_info(channel_names, sfreq=sfreq, ch_types="eeg")
    data = np.vstack(
        [
            np.sin(np.linspace(0, 12, 1600)),
            np.cos(np.linspace(0, 10, 1600)),
            np.sin(np.linspace(0, 20, 1600)),
            np.cos(np.linspace(0, 18, 1600)),
        ]
    )
    raw = mne.io.RawArray(data, info, verbose="ERROR")
    raw.set_montage(mne.channels.make_standard_montage("standard_1005"))
    raw.set_annotations(
        mne.Annotations(
            onset=[0.5, 2.0, 3.5],
            duration=[0.0, 0.0, 0.0],
            description=["T0", "T1", "T2"],
        )
    )
    summary = RecordingSummary(
        subject_id=1,
        run_id=4,
        file_path=Path("synthetic.edf"),
        channel_count=len(channel_names),
        sampling_frequency=sfreq,
        duration_seconds=raw.n_times / sfreq,
        annotations=("T0", "T1", "T2"),
        montage_name="standard_1005",
    )
    return LoadedRecording(raw=raw, summary=summary)


def test_extract_recording_metadata_returns_expected_fields() -> None:
    recording = make_loaded_recording()
    metadata = extract_recording_metadata(recording)

    assert metadata.subject_id == 1
    assert metadata.run_id == 4
    assert metadata.channel_count == 4
    assert metadata.sampling_frequency == 160.0
    assert metadata.annotation_descriptions == ("T0", "T1", "T2")


def test_extract_annotation_overview_preserves_t0_t1_t2() -> None:
    recording = make_loaded_recording()
    overview = extract_annotation_overview(recording)

    assert overview.event_count == 3
    assert overview.descriptions == ("T0", "T1", "T2")
    assert [event.description for event in overview.events] == ["T0", "T1", "T2"]


def test_plot_functions_return_usable_figures() -> None:
    recording = make_loaded_recording()

    trace_figure = plot_raw_traces(recording, duration_seconds=2.0, max_channels=2)
    psd_figure = plot_psd(recording, fmin=0.0, fmax=40.0, max_channels=2)
    sensor_figure = plot_sensor_layout(recording)
    annotation_figure = plot_annotation_overview(recording)

    assert trace_figure.axes
    assert psd_figure.axes
    assert sensor_figure.axes
    assert annotation_figure.axes


def test_invalid_input_is_rejected() -> None:
    with pytest.raises(VisualizationValidationError):
        plot_raw_traces("not-a-raw")  # type: ignore[arg-type]


def test_save_figure_writes_expected_file(tmp_path: Path) -> None:
    recording = make_loaded_recording()
    figure = plot_raw_traces(recording, duration_seconds=1.0, max_channels=2)

    saved_path = save_figure(figure, tmp_path / "trace.png")

    assert saved_path.exists()
    assert saved_path.name == "trace.png"


def test_inspect_recording_saves_three_figures_and_does_not_mutate_raw(tmp_path: Path) -> None:
    recording = make_loaded_recording()
    raw = recording.raw
    original_data = raw.get_data().copy()
    original_channels = list(raw.ch_names)
    original_annotation_descriptions = raw.annotations.description.tolist()
    original_montage = raw.get_montage()

    artifacts = inspect_recording(recording, output_dir=tmp_path, trace_duration_seconds=1.0, trace_channels=2)

    assert artifacts.annotation_figure.axes
    assert len(artifacts.saved_paths) == 4
    assert all(path.exists() for path in artifacts.saved_paths)
    assert any(path.name.endswith("_annotations.png") for path in artifacts.saved_paths)
    np.testing.assert_allclose(raw.get_data(), original_data)
    assert raw.ch_names == original_channels
    assert raw.annotations.description.tolist() == original_annotation_descriptions
    assert raw.get_montage() is not None
    assert raw.get_montage().ch_names == original_montage.ch_names
