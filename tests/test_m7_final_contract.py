from dataclasses import replace
import json

import pandas as pd
import pytest

from src.evaluation.final_contract import (
    EXPECTED_EXPERIMENT_FAMILIES,
    FULL_SYSTEM_MISSION_MAP,
    OPERATIONAL_SEED,
    SCENARIOS,
    ArtifactRecord,
    FinalContractError,
    authorize_final_access,
    build_final_manifest,
    canonical_cross_subject_manifest,
    canonical_qc_manifest,
    freeze_final_manifest,
    require_final_subject,
    sha256_file,
    validate_cross_subject_split,
    validate_fit_subjects,
    write_cross_subject_manifest,
)
from src.evaluation.cohort import write_immutable_manifest
from src.evaluation.episodes import (
    build_sequential_participation_manifest,
    construct_episode_manifest,
    freeze_episode_manifest,
    freeze_sequential_participation_manifest,
)


def _artifacts(tmp_path, split, *, code_sha="prefinal-sha"):
    records = []
    for family in ("csp_lda", "eegnet"):
        for artifact_type in ("decoder", "calibrator"):
            path = tmp_path / f"{family}-{artifact_type}.artifact"
            path.write_bytes(f"{family}:{artifact_type}".encode())
            records.append(
                ArtifactRecord(
                    artifact_id=f"{family}-{artifact_type}-v1",
                    decoder_family=family,
                    artifact_type=artifact_type,
                    local_path=str(path),
                    sha256=sha256_file(path),
                    code_sha=code_sha,
                    training_subject_ids=split.train_subject_ids,
                    validation_subject_ids=split.validation_subject_ids,
                    fit_partition=("train_with_validation_selection" if artifact_type == "decoder" else "validation"),
                    selection_rule="approved-validation-only-selection",
                    seed=(42 if family == "eegnet" else None),
                    configuration={"test_fixture": True},
                )
            )
    return tuple(records)


def _episodes(tmp_path):
    rows = []
    for index in range(5):
        rows.append(
            {
                "subject_id": 2,
                "run_id": 4,
                "source_file": "S002R04.edf",
                "event_code": "T1",
                "semantic_label": "left",
                "event_sample": 160 * (index + 1),
                "trial_index": index,
            }
        )
    manifest = construct_episode_manifest(pd.DataFrame(rows))
    path = tmp_path / "episodes.json"
    return manifest, path, freeze_episode_manifest(manifest, path)


def _participation(tmp_path, episodes, split, split_hash):
    manifest = build_sequential_participation_manifest(
        episodes,
        split_manifest_sha256=split_hash,
        partition_name="final_test",
        frozen_partition_subject_ids=split.final_test_subject_ids,
    )
    path = tmp_path / "participation.json"
    return manifest, path, freeze_sequential_participation_manifest(manifest, path)


def _split(tmp_path):
    qc_path = tmp_path / "qc.json"
    qc_hash = write_immutable_manifest(canonical_qc_manifest(), qc_path)
    return canonical_cross_subject_manifest(qc_manifest_file_sha256=qc_hash), qc_path, qc_hash


def test_canonical_split_gate_is_exact_disjoint_and_deterministic(tmp_path):
    first = canonical_cross_subject_manifest()
    second = canonical_cross_subject_manifest()
    validate_cross_subject_split(first)
    assert first == second
    assert len(first.eligible_subject_ids) == 109
    assert first.partition_counts == {"train": 76, "validation": 16, "final_test": 17}
    assert first.final_test_subject_ids == first.protected_final_test_subject_ids
    assert not (set(first.train_subject_ids) & set(first.validation_subject_ids))
    assert not (set(first.train_subject_ids) & set(first.final_test_subject_ids))


def test_fitting_hooks_fail_closed_for_protected_or_partial_subject_sets():
    split = canonical_cross_subject_manifest()
    assert validate_fit_subjects(split.train_subject_ids, split_name="train", split_manifest=split) == split.train_subject_ids
    assert validate_fit_subjects(split.validation_subject_ids, split_name="validation", split_manifest=split) == split.validation_subject_ids
    with pytest.raises(FinalContractError, match="only frozen train or validation"):
        validate_fit_subjects(split.final_test_subject_ids, split_name="final_test", split_manifest=split)
    with pytest.raises(FinalContractError, match="exactly match"):
        validate_fit_subjects(split.train_subject_ids[:-1], split_name="train", split_manifest=split)


def test_final_manifest_freezes_and_authorizes_only_verified_artifacts(tmp_path):
    split, qc_path, qc_hash = _split(tmp_path)
    split_path = tmp_path / "cross-subject.json"
    split_hash = write_cross_subject_manifest(split, split_path)
    episodes, episode_path, episode_hash = _episodes(tmp_path)
    participation, participation_path, participation_hash = _participation(tmp_path, episodes, split, split_hash)
    manifest = build_final_manifest(
        software_sha="prefinal-sha",
        governance_sha="governance-sha",
        qc_manifest_path=str(qc_path),
        qc_manifest_sha256=qc_hash,
        split_manifest_path=str(split_path),
        split_manifest_sha256=split_hash,
        split_manifest=split,
        episode_manifest_path=str(episode_path),
        episode_manifest_sha256=episode_hash,
        episode_manifest=episodes,
        participation_manifest_path=str(participation_path),
        participation_manifest_sha256=participation_hash,
        participation_manifest=participation,
        artifacts=_artifacts(tmp_path, split),
    )
    manifest_path = tmp_path / "final-manifest.json"
    first_hash = freeze_final_manifest(manifest, manifest_path)
    assert freeze_final_manifest(manifest, manifest_path) == first_hash
    authorization = authorize_final_access(manifest_path)
    assert authorization.manifest_sha256 == first_hash
    assert authorization.final_subject_ids == split.final_test_subject_ids
    require_final_subject(split.final_test_subject_ids[0], authorization)
    with pytest.raises(FinalContractError, match="not in the frozen"):
        require_final_subject(split.train_subject_ids[0], authorization)
    with pytest.raises(FinalContractError, match="different content"):
        freeze_final_manifest(replace(manifest, software_sha="changed"), manifest_path)


def test_final_authorization_rejects_tampered_artifact(tmp_path):
    split, qc_path, qc_hash = _split(tmp_path)
    split_path = tmp_path / "cross-subject.json"
    split_hash = write_cross_subject_manifest(split, split_path)
    episodes, episode_path, episode_hash = _episodes(tmp_path)
    participation, participation_path, participation_hash = _participation(tmp_path, episodes, split, split_hash)
    artifacts = _artifacts(tmp_path, split)
    manifest_path = tmp_path / "final-manifest.json"
    freeze_final_manifest(
        build_final_manifest(
            software_sha="prefinal-sha",
            governance_sha="governance-sha",
            qc_manifest_path=str(qc_path),
            qc_manifest_sha256=qc_hash,
            split_manifest_path=str(split_path),
            split_manifest_sha256=split_hash,
            split_manifest=split,
            episode_manifest_path=str(episode_path),
            episode_manifest_sha256=episode_hash,
            episode_manifest=episodes,
            participation_manifest_path=str(participation_path),
            participation_manifest_sha256=participation_hash,
            participation_manifest=participation,
            artifacts=artifacts,
        ),
        manifest_path,
    )
    with open(artifacts[0].local_path, "ab") as stream:
        stream.write(b"tamper")
    with pytest.raises(FinalContractError, match="artifact hash"):
        authorize_final_access(manifest_path)


def test_manifest_contains_exact_execution_families_map_and_seed(tmp_path):
    split, qc_path, qc_hash = _split(tmp_path)
    split_path = tmp_path / "split.json"
    split_hash = write_cross_subject_manifest(split, split_path)
    episodes, episode_path, episode_hash = _episodes(tmp_path)
    participation, participation_path, participation_hash = _participation(tmp_path, episodes, split, split_hash)
    manifest = build_final_manifest(
        software_sha="prefinal-sha",
        governance_sha="governance-sha",
        qc_manifest_path=str(qc_path),
        qc_manifest_sha256=qc_hash,
        split_manifest_path=str(split_path),
        split_manifest_sha256=split_hash,
        split_manifest=split,
        episode_manifest_path=str(episode_path),
        episode_manifest_sha256=episode_hash,
        episode_manifest=episodes,
        participation_manifest_path=str(participation_path),
        participation_manifest_sha256=participation_hash,
        participation_manifest=participation,
        artifacts=_artifacts(tmp_path, split),
    )
    payload = json.loads(json.dumps(manifest, default=lambda value: value.__dict__))
    assert manifest.experiment_families == EXPECTED_EXPERIMENT_FAMILIES
    assert manifest.r2_seed == manifest.bootstrap_seed == OPERATIONAL_SEED
    assert manifest.full_system_mission_map == FULL_SYSTEM_MISSION_MAP
    assert tuple(item.scenario_id for item in SCENARIOS) == ("S1", "S2", "S3", "S4", "S5", "S6", "S7")
    assert payload["protected_access_status"] == "NOT_ACCESSED_AT_FREEZE"
    assert payload["episode_manifest_version"] == "m7-d081-fixed-intent-episodes-v1"
    assert payload["statistical_policy_ids"] == ["D-079", "D-080", "D-081", "D-082", "D-083"]
    assert payload["protected_data_prefetch_audit"]["protected_outcomes_observed"] is False
