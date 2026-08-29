from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import mne
import numpy as np
from matplotlib.figure import Figure
from mne.io import BaseRaw

from src.eeg.loader import LoadedRecording, load_subject_recordings

DEFAULT_TRACE_CHANNEL_COUNT = 8
DEFAULT_TRACE_DURATION_SECONDS = 10.0
DEFAULT_PSD_FMIN = 0.0
DEFAULT_PSD_FMAX = 60.0


class VisualizationValidationError(ValueError):
    """Raised when visualization inputs are invalid."""


@dataclass(frozen=True)
class AnnotationEvent:
    onset_seconds: float
    duration_seconds: float
    description: str


@dataclass(frozen=True)
class AnnotationOverview:
    subject_id: int | None
    run_id: int | None
    event_count: int
    descriptions: tuple[str, ...]
    events: tuple[AnnotationEvent, ...]


@dataclass(frozen=True)
class RecordingMetadata:
    subject_id: int | None
    run_id: int | None
    channel_count: int
    sampling_frequency: float
    duration_seconds: float
    annotation_descriptions: tuple[str, ...]
    montage_name: str | None


@dataclass(frozen=True)
class InspectionArtifacts:
    metadata: RecordingMetadata
    annotation_overview: AnnotationOverview
    raw_trace_figure: Figure
    psd_figure: Figure
    sensor_figure: Figure
    saved_paths: tuple[Path, ...]


def _coerce_loaded_recording(recording: LoadedRecording | BaseRaw) -> tuple[BaseRaw, int | None, int | None]:
    if isinstance(recording, LoadedRecording):
        return recording.raw, recording.summary.subject_id, recording.summary.run_id
    if isinstance(recording, BaseRaw):
        return recording, None, None
    raise VisualizationValidationError(
        f"Expected a LoadedRecording or MNE Raw object. Got {type(recording)!r}."
    )


def _validate_raw(recording: LoadedRecording | BaseRaw) -> tuple[BaseRaw, int | None, int | None]:
    raw, subject_id, run_id = _coerce_loaded_recording(recording)
    if len(raw.ch_names) == 0:
        raise VisualizationValidationError("Raw recording has no channels.")
    if raw.n_times <= 0:
        raise VisualizationValidationError("Raw recording has no samples.")
    if float(raw.info["sfreq"]) <= 0.0:
        raise VisualizationValidationError("Raw recording sampling frequency must be positive.")
    return raw, subject_id, run_id


def extract_recording_metadata(recording: LoadedRecording | BaseRaw) -> RecordingMetadata:
    raw, subject_id, run_id = _validate_raw(recording)
    descriptions = tuple(sorted(set(raw.annotations.description.tolist())))
    montage = raw.get_montage()
    montage_name = getattr(montage, "kind", None)
    if montage_name is None and isinstance(recording, LoadedRecording):
        montage_name = recording.summary.montage_name
    return RecordingMetadata(
        subject_id=subject_id,
        run_id=run_id,
        channel_count=len(raw.ch_names),
        sampling_frequency=float(raw.info["sfreq"]),
        duration_seconds=raw.n_times / float(raw.info["sfreq"]),
        annotation_descriptions=descriptions,
        montage_name=montage_name,
    )


def extract_annotation_overview(recording: LoadedRecording | BaseRaw) -> AnnotationOverview:
    raw, subject_id, run_id = _validate_raw(recording)
    events = tuple(
        AnnotationEvent(
            onset_seconds=float(onset),
            duration_seconds=float(duration),
            description=str(description),
        )
        for onset, duration, description in zip(
            raw.annotations.onset,
            raw.annotations.duration,
            raw.annotations.description,
        )
    )
    descriptions = tuple(sorted(set(event.description for event in events)))
    return AnnotationOverview(
        subject_id=subject_id,
        run_id=run_id,
        event_count=len(events),
        descriptions=descriptions,
        events=events,
    )


def plot_raw_traces(
    recording: LoadedRecording | BaseRaw,
    *,
    start_seconds: float = 0.0,
    duration_seconds: float = DEFAULT_TRACE_DURATION_SECONDS,
    max_channels: int = DEFAULT_TRACE_CHANNEL_COUNT,
    scale: float = 1e6,
) -> Figure:
    raw, subject_id, run_id = _validate_raw(recording)
    if start_seconds < 0.0:
        raise VisualizationValidationError("start_seconds must be non-negative.")
    if duration_seconds <= 0.0:
        raise VisualizationValidationError("duration_seconds must be positive.")
    if max_channels <= 0:
        raise VisualizationValidationError("max_channels must be positive.")

    sfreq = float(raw.info["sfreq"])
    start_sample = int(start_seconds * sfreq)
    stop_sample = min(raw.n_times, start_sample + int(duration_seconds * sfreq))
    if start_sample >= raw.n_times or stop_sample <= start_sample:
        raise VisualizationValidationError("Requested trace window is outside the recording duration.")

    channel_count = min(max_channels, len(raw.ch_names))
    data = raw.get_data(start=start_sample, stop=stop_sample, picks=list(range(channel_count)))
    times = raw.times[start_sample:stop_sample]

    fig, ax = plt.subplots(figsize=(12, 6))
    offsets = np.arange(channel_count, dtype=float) * 150.0
    for index in range(channel_count):
        ax.plot(times, data[index] * scale + offsets[index], linewidth=0.8)
    ax.set_yticks(offsets)
    ax.set_yticklabels(raw.ch_names[:channel_count])
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Channel")
    ax.set_title(f"Raw EEG Traces | Subject {subject_id or 'N/A'} | Run {run_id or 'N/A'}")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_psd(
    recording: LoadedRecording | BaseRaw,
    *,
    fmin: float = DEFAULT_PSD_FMIN,
    fmax: float = DEFAULT_PSD_FMAX,
    max_channels: int = DEFAULT_TRACE_CHANNEL_COUNT,
) -> Figure:
    raw, subject_id, run_id = _validate_raw(recording)
    if fmin < 0.0:
        raise VisualizationValidationError("fmin must be non-negative.")
    if fmax <= fmin:
        raise VisualizationValidationError("fmax must be greater than fmin.")
    if max_channels <= 0:
        raise VisualizationValidationError("max_channels must be positive.")

    picks = list(range(min(max_channels, len(raw.ch_names))))
    spectrum = raw.compute_psd(fmin=fmin, fmax=fmax, picks=picks, verbose="ERROR")
    psd, freqs = spectrum.get_data(return_freqs=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    for channel_name, channel_psd in zip(np.array(raw.ch_names)[picks], psd):
        ax.plot(freqs, channel_psd, linewidth=0.8, alpha=0.7, label=channel_name)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power Spectral Density")
    ax.set_title(f"PSD Inspection | Subject {subject_id or 'N/A'} | Run {run_id or 'N/A'}")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize="small", ncol=2)
    fig.tight_layout()
    return fig


def plot_sensor_layout(recording: LoadedRecording | BaseRaw, *, show_names: bool = False) -> Figure:
    raw, _, _ = _validate_raw(recording)
    if raw.get_montage() is None:
        raise VisualizationValidationError("Raw recording does not have an attached montage.")
    fig = raw.copy().plot_sensors(show_names=show_names, show=False)
    return fig


def plot_annotation_overview(recording: LoadedRecording | BaseRaw) -> Figure:
    overview = extract_annotation_overview(recording)
    fig, ax = plt.subplots(figsize=(12, 3))
    if overview.events:
        label_positions = {label: index for index, label in enumerate(overview.descriptions)}
        for event in overview.events:
            ax.scatter(event.onset_seconds, label_positions[event.description], s=40)
    ax.set_yticks(range(len(overview.descriptions)))
    ax.set_yticklabels(overview.descriptions)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Annotation")
    ax.set_title(
        f"Annotation Overview | Subject {overview.subject_id or 'N/A'} | Run {overview.run_id or 'N/A'}"
    )
    ax.grid(True, axis="x", alpha=0.3)
    fig.tight_layout()
    return fig


def save_figure(figure: Figure, output_path: str | Path) -> Path:
    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, bbox_inches="tight")
    return path


def inspect_recording(
    recording: LoadedRecording | BaseRaw,
    *,
    output_dir: str | Path | None = None,
    trace_duration_seconds: float = DEFAULT_TRACE_DURATION_SECONDS,
    trace_channels: int = DEFAULT_TRACE_CHANNEL_COUNT,
    psd_fmin: float = DEFAULT_PSD_FMIN,
    psd_fmax: float = DEFAULT_PSD_FMAX,
) -> InspectionArtifacts:
    metadata = extract_recording_metadata(recording)
    annotation_overview = extract_annotation_overview(recording)
    raw_trace_figure = plot_raw_traces(
        recording,
        duration_seconds=trace_duration_seconds,
        max_channels=trace_channels,
    )
    psd_figure = plot_psd(
        recording,
        fmin=psd_fmin,
        fmax=psd_fmax,
        max_channels=trace_channels,
    )
    sensor_figure = plot_sensor_layout(recording)
    saved_paths: list[Path] = []
    if output_dir is not None:
        output_root = Path(output_dir).expanduser().resolve()
        subject_part = metadata.subject_id if metadata.subject_id is not None else "unknown"
        run_part = metadata.run_id if metadata.run_id is not None else "unknown"
        saved_paths.append(save_figure(raw_trace_figure, output_root / f"subject_{subject_part}_run_{run_part}_traces.png"))
        saved_paths.append(save_figure(psd_figure, output_root / f"subject_{subject_part}_run_{run_part}_psd.png"))
        saved_paths.append(save_figure(sensor_figure, output_root / f"subject_{subject_part}_run_{run_part}_sensors.png"))
    return InspectionArtifacts(
        metadata=metadata,
        annotation_overview=annotation_overview,
        raw_trace_figure=raw_trace_figure,
        psd_figure=psd_figure,
        sensor_figure=sensor_figure,
        saved_paths=tuple(saved_paths),
    )


def format_metadata_report(metadata: RecordingMetadata) -> str:
    annotations = ", ".join(metadata.annotation_descriptions)
    return (
        f"Subject {metadata.subject_id or 'N/A'} | Run {metadata.run_id or 'N/A'} | "
        f"Channels {metadata.channel_count} | Sampling {metadata.sampling_frequency:.1f} Hz | "
        f"Duration {metadata.duration_seconds:.2f} s | Annotations [{annotations}] | "
        f"Montage {metadata.montage_name or 'unknown'}"
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect cached EEGBCI recordings without preprocessing.")
    parser.add_argument("--subject", type=int, required=True, help="EEGBCI subject ID.")
    parser.add_argument(
        "--runs",
        nargs="+",
        type=int,
        default=[4, 8, 12],
        help="Approved EEGBCI run IDs to inspect.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Optional directory where diagnostic figures will be saved.",
    )
    parser.add_argument(
        "--data-path",
        type=Path,
        default=None,
        help="Optional EEGBCI cache path passed through to the loader.",
    )
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    try:
        recordings = load_subject_recordings(
            args.subject,
            run_ids=args.runs,
            data_path=args.data_path,
            preload=False,
        )
        for recording in recordings:
            artifacts = inspect_recording(recording, output_dir=args.output_dir)
            print(format_metadata_report(artifacts.metadata))
            descriptions = ", ".join(artifacts.annotation_overview.descriptions)
            print(f"Annotation descriptions: [{descriptions}]")
            if artifacts.saved_paths:
                for saved_path in artifacts.saved_paths:
                    print(f"Saved figure: {saved_path}")
            plt.close(artifacts.raw_trace_figure)
            plt.close(artifacts.psd_figure)
            plt.close(artifacts.sensor_figure)
    except (VisualizationValidationError, OSError, RuntimeError) as exc:
        parser.exit(status=1, message=f"Visualization error: {exc}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
