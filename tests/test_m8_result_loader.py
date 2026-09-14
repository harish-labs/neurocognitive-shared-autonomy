from __future__ import annotations

import json
import shutil
from pathlib import Path
from types import MappingProxyType

import pytest

from src.app.result_loader import (
    ACCEPTED_MANIFEST_RELATIVE_PATH,
    ACCEPTED_MANIFEST_SHA256,
    ACCEPTED_RESULT_RELATIVE_PATH,
    ACCEPTED_RESULT_SHA256,
    ResultIntegrityError,
    headline_metrics,
    is_accepted_result_path,
    load_presentation_data,
    repository_root,
)


def test_accepted_result_and_manifest_load_with_verified_identity() -> None:
    data = load_presentation_data()
    assert data.result_sha256 == ACCEPTED_RESULT_SHA256
    assert data.manifest_sha256 == ACCEPTED_MANIFEST_SHA256
    assert data.protected_subject_count == 10
    assert data.sequential_subject_count == 8
    assert isinstance(data.result, MappingProxyType)


def test_superseded_result_path_is_not_accepted() -> None:
    root = repository_root()
    assert is_accepted_result_path(root / ACCEPTED_RESULT_RELATIVE_PATH)
    assert not is_accepted_result_path(root / "results/m7/final/m7-final-results-v4.json")


def test_headlines_are_derived_from_accepted_tables() -> None:
    metrics = headline_metrics(load_presentation_data())
    assert metrics["eeg_trials"] == 303
    assert metrics["csp_d_success"] == 32
    assert metrics["eegnet_d_success"] == 36
    assert metrics["system_episode_count"] == 38
    assert metrics["eegnet_holm_p"] == pytest.approx(0.0625)


def test_missing_accepted_result_fails_clearly(tmp_path: Path) -> None:
    with pytest.raises(ResultIntegrityError, match="missing"):
        load_presentation_data(tmp_path)


def test_malformed_schema_fails_when_hash_check_is_explicitly_disabled(tmp_path: Path) -> None:
    source = repository_root()
    result_path = tmp_path / ACCEPTED_RESULT_RELATIVE_PATH
    manifest_path = tmp_path / ACCEPTED_MANIFEST_RELATIVE_PATH
    result_path.parent.mkdir(parents=True)
    manifest_path.parent.mkdir(parents=True)
    result_path.write_text(json.dumps({"schema_version": "wrong"}), encoding="utf-8")
    shutil.copy2(source / ACCEPTED_MANIFEST_RELATIVE_PATH, manifest_path)
    tables = tmp_path / "results/m7/tables"
    shutil.copytree(source / "results/m7/tables", tables)
    with pytest.raises(ResultIntegrityError, match="missing required sections"):
        load_presentation_data(tmp_path, verify_hashes=False)


def test_hash_mismatch_fails_before_presentation(tmp_path: Path) -> None:
    source = repository_root()
    result_path = tmp_path / ACCEPTED_RESULT_RELATIVE_PATH
    manifest_path = tmp_path / ACCEPTED_MANIFEST_RELATIVE_PATH
    result_path.parent.mkdir(parents=True)
    manifest_path.parent.mkdir(parents=True)
    shutil.copy2(source / ACCEPTED_RESULT_RELATIVE_PATH, result_path)
    shutil.copy2(source / ACCEPTED_MANIFEST_RELATIVE_PATH, manifest_path)
    result_path.write_text(result_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(ResultIntegrityError, match="hash mismatch"):
        load_presentation_data(tmp_path)
