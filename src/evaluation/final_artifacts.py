"""Train/validation-only creation and loading of frozen M7 decoder artifacts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import pickle
from typing import Any

import mne
import torch

from src.evaluation.cohort import D082CrossSubjectSplitManifest
from src.evaluation.final_contract import (
    ArtifactRecord,
    FinalContractError,
    sha256_file,
    validate_cross_subject_split,
    validate_fit_subjects,
)
from src.models.calibration import (
    PlattScalingCalibrator,
    TemperatureScalingCalibrator,
    fit_csp_lda_platt_scaler,
    fit_eegnet_temperature_scaler,
)
from src.models.csp_lda import CspLdaDecoder, fit_csp_lda
from src.models.eegnet import EEGNetDecoder, EEGNetModel, RANDOM_SEED, fit_eegnet


@dataclass(frozen=True)
class FrozenArtifactBundle:
    csp_decoder: CspLdaDecoder
    csp_calibrator: PlattScalingCalibrator
    eegnet_decoder: EEGNetDecoder
    eegnet_calibrator: TemperatureScalingCalibrator
    records: tuple[ArtifactRecord, ...]


def fit_and_freeze_cross_subject_artifacts(
    epochs: mne.BaseEpochs,
    *,
    split_manifest: D082CrossSubjectSplitManifest,
    output_directory: str | Path,
    code_sha: str,
) -> FrozenArtifactBundle:
    """Fit both approved decoder paths without accepting any final-subject epochs."""

    validate_cross_subject_split(split_manifest)
    _validate_fitting_epochs(epochs, split_manifest)
    destination = Path(output_directory).resolve()
    destination.mkdir(parents=True, exist_ok=True)

    csp_training = fit_csp_lda(epochs)
    csp_calibrator = fit_csp_lda_platt_scaler(csp_training.decoder, epochs)
    eegnet_training = fit_eegnet(epochs)
    eegnet_calibrator = fit_eegnet_temperature_scaler(eegnet_training.decoder, epochs)

    csp_path = destination / "cross-subject-csp-lda-v1.pkl"
    eegnet_path = destination / "cross-subject-eegnet-v1.pt"
    csp_calibrator_path = destination / "cross-subject-csp-platt-v1.json"
    eegnet_calibrator_path = destination / "cross-subject-eegnet-temperature-v1.json"

    with csp_path.open("wb") as stream:
        pickle.dump(csp_training.decoder, stream, protocol=pickle.HIGHEST_PROTOCOL)
    torch.save(
        {
            "state_dict": eegnet_training.decoder._model.state_dict(),
            "n_times": eegnet_training.decoder._model.n_times,
            "class_labels": eegnet_training.decoder.class_labels,
        },
        eegnet_path,
    )
    _write_json(
        csp_calibrator_path,
        {
            "method": csp_calibrator.method,
            "model_family": csp_calibrator.model_family,
            "fit_partition": csp_calibrator.fit_partition,
            "class_labels": csp_calibrator.class_labels,
            "slope": csp_calibrator.slope,
            "intercept": csp_calibrator.intercept,
        },
    )
    _write_json(
        eegnet_calibrator_path,
        {
            "method": eegnet_calibrator.method,
            "model_family": eegnet_calibrator.model_family,
            "fit_partition": eegnet_calibrator.fit_partition,
            "class_labels": eegnet_calibrator.class_labels,
            "temperature": eegnet_calibrator.temperature,
        },
    )

    common = {
        "code_sha": code_sha,
        "training_subject_ids": split_manifest.train_subject_ids,
        "validation_subject_ids": split_manifest.validation_subject_ids,
    }
    records = (
        ArtifactRecord(
            artifact_id="m7-cross-subject-csp-lda-decoder-v1",
            decoder_family="csp_lda",
            artifact_type="decoder",
            local_path=str(csp_path),
            sha256=sha256_file(csp_path),
            fit_partition="train_with_validation_selection",
            selection_rule="D-043/D-044 validation balanced accuracy over CSP n_components {2,4,6,8}",
            seed=None,
            configuration={
                "selected_n_components": csp_training.selected_n_components,
                "candidate_scores": [asdict(score) for score in csp_training.candidate_scores],
                "class_labels": csp_training.decoder.class_labels,
            },
            **common,
        ),
        ArtifactRecord(
            artifact_id="m7-cross-subject-csp-platt-calibrator-v1",
            decoder_family="csp_lda",
            artifact_type="calibrator",
            local_path=str(csp_calibrator_path),
            sha256=sha256_file(csp_calibrator_path),
            fit_partition="validation",
            selection_rule="D-048/D-049 fixed Platt scaling on validation partition",
            seed=None,
            configuration={"slope": csp_calibrator.slope, "intercept": csp_calibrator.intercept},
            **common,
        ),
        ArtifactRecord(
            artifact_id="m7-cross-subject-eegnet-decoder-v1",
            decoder_family="eegnet",
            artifact_type="decoder",
            local_path=str(eegnet_path),
            sha256=sha256_file(eegnet_path),
            fit_partition="train_with_validation_selection",
            selection_rule="D-045/D-046 seed-42 earliest best validation-balanced-accuracy checkpoint",
            seed=RANDOM_SEED,
            configuration={
                "selected_epoch_index": eegnet_training.selected_epoch_index,
                "best_validation_balanced_accuracy": eegnet_training.best_validation_balanced_accuracy,
                "epochs_run": len(eegnet_training.history),
                "class_labels": eegnet_training.decoder.class_labels,
                "n_times": eegnet_training.decoder._model.n_times,
            },
            **common,
        ),
        ArtifactRecord(
            artifact_id="m7-cross-subject-eegnet-temperature-calibrator-v1",
            decoder_family="eegnet",
            artifact_type="calibrator",
            local_path=str(eegnet_calibrator_path),
            sha256=sha256_file(eegnet_calibrator_path),
            fit_partition="validation",
            selection_rule="D-048/D-049 fixed temperature scaling on validation partition",
            seed=None,
            configuration={"temperature": eegnet_calibrator.temperature},
            **common,
        ),
    )
    for record in records:
        record.validate(split_manifest)
    return FrozenArtifactBundle(
        csp_decoder=csp_training.decoder,
        csp_calibrator=csp_calibrator,
        eegnet_decoder=eegnet_training.decoder,
        eegnet_calibrator=eegnet_calibrator,
        records=records,
    )


def load_frozen_cross_subject_artifacts(records: tuple[ArtifactRecord, ...]) -> FrozenArtifactBundle:
    by_key = {(record.decoder_family, record.artifact_type): record for record in records}
    if set(by_key) != {
        ("csp_lda", "decoder"),
        ("csp_lda", "calibrator"),
        ("eegnet", "decoder"),
        ("eegnet", "calibrator"),
    }:
        raise FinalContractError("Frozen artifact inventory is incomplete.")
    for record in records:
        if sha256_file(record.local_path) != record.sha256:
            raise FinalContractError(f"Frozen artifact hash mismatch: {record.artifact_id}.")

    with Path(by_key[("csp_lda", "decoder")].local_path).open("rb") as stream:
        csp_decoder = pickle.load(stream)
    if not isinstance(csp_decoder, CspLdaDecoder):
        raise FinalContractError("Frozen CSP artifact did not contain CspLdaDecoder.")
    eegnet_payload = torch.load(
        by_key[("eegnet", "decoder")].local_path,
        map_location="cpu",
        weights_only=True,
    )
    eegnet_model = EEGNetModel(n_times=int(eegnet_payload["n_times"]))
    eegnet_model.load_state_dict(eegnet_payload["state_dict"])
    eegnet_decoder = EEGNetDecoder(model=eegnet_model, class_labels=tuple(eegnet_payload["class_labels"]))

    csp_payload = _read_json(by_key[("csp_lda", "calibrator")].local_path)
    csp_calibrator = PlattScalingCalibrator(
        slope=float(csp_payload["slope"]),
        intercept=float(csp_payload["intercept"]),
        class_labels=tuple(csp_payload["class_labels"]),
    )
    eegnet_calibration_payload = _read_json(by_key[("eegnet", "calibrator")].local_path)
    eegnet_calibrator = TemperatureScalingCalibrator(
        temperature=float(eegnet_calibration_payload["temperature"]),
        class_labels=tuple(eegnet_calibration_payload["class_labels"]),
    )
    return FrozenArtifactBundle(csp_decoder, csp_calibrator, eegnet_decoder, eegnet_calibrator, records)


def _validate_fitting_epochs(epochs: mne.BaseEpochs, split_manifest: D082CrossSubjectSplitManifest) -> None:
    if not isinstance(epochs, mne.BaseEpochs) or epochs.metadata is None or len(epochs) == 0:
        raise FinalContractError("Artifact fitting requires non-empty canonical epochs with metadata.")
    metadata = epochs.metadata
    if "subject_id" not in metadata or "partition" not in metadata:
        raise FinalContractError("Artifact fitting metadata requires subject_id and partition.")
    observed_partitions = set(metadata["partition"].astype(str))
    if observed_partitions != {"train", "validation"}:
        raise FinalContractError("Artifact fitting accepts exactly train and validation partitions.")
    for partition in ("train", "validation"):
        subjects = tuple(sorted(set(int(value) for value in metadata.loc[metadata["partition"] == partition, "subject_id"])))
        validate_fit_subjects(subjects, split_name=partition, split_manifest=split_manifest)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
