from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import mne
from mne.datasets import eegbci
from mne.io import BaseRaw, read_raw_edf

APPROVED_RUNS: tuple[int, ...] = (4, 8, 12)
EXPECTED_CHANNEL_COUNT = 64
EXPECTED_SAMPLING_FREQUENCY = 160.0
EEGBCI_SUBJECT_MIN = 1
EEGBCI_SUBJECT_MAX = 109
DEFAULT_MONTAGE_NAME = "standard_1005"


class LoaderValidationError(ValueError):
    """Raised when loader inputs or loaded metadata fail validation."""


@dataclass(frozen=True)
class RecordingSummary:
    subject_id: int
    run_id: int
    file_path: Path
    channel_count: int
    sampling_frequency: float
    duration_seconds: float
    annotations: tuple[str, ...]
    montage_name: str


@dataclass(frozen=True)
class LoadedRecording:
    raw: BaseRaw
    summary: RecordingSummary


def _normalize_int_list(
    values: Sequence[int] | Iterable[int],
    *,
    label: str,
) -> list[int]:
    normalized = list(values)
    if not normalized:
        raise LoaderValidationError(f"{label} must not be empty.")

    result: list[int] = []
    for value in normalized:
        if isinstance(value, bool) or not isinstance(value, int):
            raise LoaderValidationError(f"{label} must contain integers. Got {value!r}.")
        result.append(value)
    return result


def validate_subject_ids(subject_ids: Sequence[int] | Iterable[int]) -> list[int]:
    normalized = _normalize_int_list(subject_ids, label="subject_ids")

    deduplicated: list[int] = []
    seen: set[int] = set()
    for subject_id in normalized:
        if not EEGBCI_SUBJECT_MIN <= subject_id <= EEGBCI_SUBJECT_MAX:
            raise LoaderValidationError(
                f"subject_ids must be between {EEGBCI_SUBJECT_MIN} and {EEGBCI_SUBJECT_MAX}. "
                f"Got {subject_id}."
            )
        if subject_id not in seen:
            deduplicated.append(subject_id)
            seen.add(subject_id)
    return deduplicated


def validate_run_ids(run_ids: Sequence[int] | Iterable[int] | None) -> list[int]:
    if run_ids is None:
        return list(APPROVED_RUNS)

    normalized = _normalize_int_list(run_ids, label="run_ids")
    invalid_runs = [run_id for run_id in normalized if run_id not in APPROVED_RUNS]
    if invalid_runs:
        allowed = ", ".join(str(run_id) for run_id in APPROVED_RUNS)
        invalid = ", ".join(str(run_id) for run_id in invalid_runs)
        raise LoaderValidationError(
            f"run_ids must be limited to the approved runs: {allowed}. Got invalid run(s): {invalid}."
        )

    deduplicated: list[int] = []
    seen: set[int] = set()
    for run_id in normalized:
        if run_id not in seen:
            deduplicated.append(run_id)
            seen.add(run_id)
    return deduplicated


def default_data_path() -> Path:
    return Path("data/raw/mne_data").resolve()


def _prepare_data_path(data_path: str | Path | None) -> Path:
    resolved = Path(data_path) if data_path is not None else default_data_path()
    resolved = resolved.expanduser().resolve()
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def _build_summary(
    *,
    subject_id: int,
    run_id: int,
    file_path: Path,
    raw: BaseRaw,
    montage_name: str,
) -> RecordingSummary:
    channel_count = len(raw.ch_names)
    if channel_count != EXPECTED_CHANNEL_COUNT:
        raise LoaderValidationError(
            f"Expected {EXPECTED_CHANNEL_COUNT} channels for subject {subject_id}, run {run_id}, "
            f"but found {channel_count}."
        )

    sampling_frequency = float(raw.info["sfreq"])
    if sampling_frequency != EXPECTED_SAMPLING_FREQUENCY:
        raise LoaderValidationError(
            f"Expected sampling frequency {EXPECTED_SAMPLING_FREQUENCY} Hz for subject {subject_id}, "
            f"run {run_id}, but found {sampling_frequency} Hz."
        )

    annotations = tuple(sorted(set(raw.annotations.description.tolist())))
    if not annotations:
        raise LoaderValidationError(
            f"No annotations were found for subject {subject_id}, run {run_id}."
        )

    montage = raw.get_montage()
    if montage is None:
        raise LoaderValidationError(
            f"Montage was not attached for subject {subject_id}, run {run_id}."
        )

    duration_seconds = raw.n_times / sampling_frequency
    return RecordingSummary(
        subject_id=subject_id,
        run_id=run_id,
        file_path=file_path,
        channel_count=channel_count,
        sampling_frequency=sampling_frequency,
        duration_seconds=duration_seconds,
        annotations=annotations,
        montage_name=montage_name,
    )


def load_subject_recordings(
    subject_id: int,
    *,
    run_ids: Sequence[int] | Iterable[int] | None = None,
    data_path: str | Path | None = None,
    preload: bool = False,
    montage_name: str = DEFAULT_MONTAGE_NAME,
    verbose: str | None = "ERROR",
) -> list[LoadedRecording]:
    subject_id = validate_subject_ids([subject_id])[0]
    validated_runs = validate_run_ids(run_ids)
    resolved_data_path = _prepare_data_path(data_path)

    file_paths = eegbci.load_data(
        subject_id,
        validated_runs,
        path=str(resolved_data_path),
        update_path=False,
        verbose=verbose,
    )
    if len(file_paths) != len(validated_runs):
        raise LoaderValidationError(
            f"MNE returned {len(file_paths)} file(s) for {len(validated_runs)} requested run(s)."
        )

    montage = mne.channels.make_standard_montage(montage_name)
    recordings: list[LoadedRecording] = []
    for run_id, file_path_str in zip(validated_runs, file_paths):
        file_path = Path(file_path_str).resolve()
        raw = read_raw_edf(file_path, preload=preload, verbose=verbose)
        eegbci.standardize(raw)
        raw.set_montage(montage)
        summary = _build_summary(
            subject_id=subject_id,
            run_id=run_id,
            file_path=file_path,
            raw=raw,
            montage_name=montage_name,
        )
        recordings.append(LoadedRecording(raw=raw, summary=summary))

    return recordings


def load_multiple_subjects(
    subject_ids: Sequence[int] | Iterable[int],
    *,
    run_ids: Sequence[int] | Iterable[int] | None = None,
    data_path: str | Path | None = None,
    preload: bool = False,
    montage_name: str = DEFAULT_MONTAGE_NAME,
    verbose: str | None = "ERROR",
) -> list[LoadedRecording]:
    validated_subjects = validate_subject_ids(subject_ids)
    loaded: list[LoadedRecording] = []
    for subject_id in validated_subjects:
        loaded.extend(
            load_subject_recordings(
                subject_id,
                run_ids=run_ids,
                data_path=data_path,
                preload=preload,
                montage_name=montage_name,
                verbose=verbose,
            )
        )
    return loaded


def format_recording_report(recording: LoadedRecording) -> str:
    summary = recording.summary
    annotations = ", ".join(summary.annotations)
    run_ids = summary.run_id
    return (
        f"Subject {summary.subject_id} | Run {run_ids} | Channels {summary.channel_count} | "
        f"Sampling {summary.sampling_frequency:.1f} Hz | Duration {summary.duration_seconds:.2f} s | "
        f"Annotations [{annotations}] | Montage {summary.montage_name} | File {summary.file_path}"
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Load and validate PhysioNet EEGBCI motor-imagery EDF recordings."
    )
    parser.add_argument(
        "--subjects",
        nargs="+",
        type=int,
        required=True,
        help="One or more EEGBCI subject IDs (1-109).",
    )
    parser.add_argument(
        "--runs",
        nargs="+",
        type=int,
        default=list(APPROVED_RUNS),
        help="Approved EEGBCI run IDs. Defaults to 4 8 12.",
    )
    parser.add_argument(
        "--data-path",
        type=Path,
        default=default_data_path(),
        help="Directory for the MNE EEGBCI cache.",
    )
    parser.add_argument(
        "--preload",
        action="store_true",
        help="Load raw signal samples into memory.",
    )
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    try:
        recordings = load_multiple_subjects(
            args.subjects,
            run_ids=args.runs,
            data_path=args.data_path,
            preload=args.preload,
        )
    except LoaderValidationError as exc:
        parser.exit(status=1, message=f"Loader validation error: {exc}\n")
    except OSError as exc:
        parser.exit(status=1, message=f"Loader I/O error: {exc}\n")

    for recording in recordings:
        print(format_recording_report(recording))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
