from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from types import MappingProxyType

import pytest

import src.app.result_loader as result_loader
from src.app.result_loader import (
    ACCEPTED_MANIFEST_RELATIVE_PATH,
    ACCEPTED_MANIFEST_SHA256,
    ACCEPTED_REPORT_MANIFEST_RELATIVE_PATH,
    ACCEPTED_REPORT_MANIFEST_SHA256,
    ACCEPTED_RESULT_RELATIVE_PATH,
    ACCEPTED_RESULT_SHA256,
    ResultIntegrityError,
    headline_metrics,
    is_accepted_result_path,
    load_presentation_data,
    repository_root,
)


def test_accepted_reporting_surface_loads_with_verified_identity() -> None:
    data = load_presentation_data()
    assert data.result_sha256 == ACCEPTED_RESULT_SHA256
    assert data.manifest_sha256 == ACCEPTED_MANIFEST_SHA256
    assert data.report_manifest_sha256 == ACCEPTED_REPORT_MANIFEST_SHA256
    assert data.report_manifest["source_result_sha256"] == ACCEPTED_RESULT_SHA256
    assert data.protected_subject_count == 10
    assert data.sequential_subject_count == 8
    assert isinstance(data.result, MappingProxyType)
    assert len(data.tables) == 11
    assert len(data.reused_figures) == 4


def test_superseded_result_paths_remain_non_reportable() -> None:
    root = repository_root()
    assert is_accepted_result_path(root / ACCEPTED_RESULT_RELATIVE_PATH)
    for version in range(1, 5):
        assert not is_accepted_result_path(
            root / f"results/m7/final/m7-final-results-v{version}.json"
        )


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


def test_malformed_result_schema_fails_without_a_dashboard_bypass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_identity_files(tmp_path)
    result_path = tmp_path / ACCEPTED_RESULT_RELATIVE_PATH
    result_path.write_text(json.dumps({"schema_version": "wrong"}), encoding="utf-8")
    monkeypatch.setattr(result_loader, "ACCEPTED_RESULT_SHA256", _sha256(result_path))
    with pytest.raises(ResultIntegrityError, match="missing required sections"):
        load_presentation_data(tmp_path)


def test_result_hash_mismatch_fails_before_presentation(tmp_path: Path) -> None:
    _copy_identity_files(tmp_path)
    result_path = tmp_path / ACCEPTED_RESULT_RELATIVE_PATH
    result_path.write_bytes(result_path.read_bytes() + b"\n")
    with pytest.raises(ResultIntegrityError, match="result hash mismatch"):
        load_presentation_data(tmp_path)


def test_report_manifest_source_result_binding_is_enforced(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_reporting_surface(tmp_path)
    _rewrite_report_manifest(
        tmp_path,
        monkeypatch,
        lambda payload: payload.__setitem__("source_result_sha256", "0" * 64),
    )
    with pytest.raises(ResultIntegrityError, match="not bound"):
        load_presentation_data(tmp_path)


def test_tampered_consumed_table_fails_before_parsing(tmp_path: Path) -> None:
    _copy_reporting_surface(tmp_path)
    table = tmp_path / "results/m7/tables/e6_abcd.csv"
    table.write_bytes(table.read_bytes() + b"tampered")
    with pytest.raises(ResultIntegrityError, match="artifact hash mismatch.*e6_abcd"):
        load_presentation_data(tmp_path)


def test_required_table_missing_from_manifest_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_reporting_surface(tmp_path)

    def remove_table(payload: dict[str, object]) -> None:
        payload["artifacts"] = [
            item
            for item in payload["artifacts"]
            if item["path"] != "m7/tables/e6_abcd.csv"
        ]

    _rewrite_report_manifest(tmp_path, monkeypatch, remove_table)
    with pytest.raises(ResultIntegrityError, match="not listed.*e6_abcd"):
        load_presentation_data(tmp_path)


def test_required_table_with_incorrect_artifact_type_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _copy_reporting_surface(tmp_path)

    def change_type(payload: dict[str, object]) -> None:
        record = next(
            item
            for item in payload["artifacts"]
            if item["path"] == "m7/tables/e6_abcd.csv"
        )
        record["artifact_type"] = "figure"

    _rewrite_report_manifest(tmp_path, monkeypatch, change_type)
    with pytest.raises(ResultIntegrityError, match="unexpected type.*expected 'table'"):
        load_presentation_data(tmp_path)


def test_reused_m7_figure_integrity_is_enforced(tmp_path: Path) -> None:
    _copy_reporting_surface(tmp_path)
    figure = tmp_path / "results/m7/figures/e7_r1_robustness.png"
    figure.write_bytes(figure.read_bytes() + b"tampered")
    with pytest.raises(ResultIntegrityError, match="artifact hash mismatch.*e7_r1"):
        load_presentation_data(tmp_path)


def _copy_identity_files(target: Path) -> None:
    source = repository_root()
    for relative in (
        ACCEPTED_RESULT_RELATIVE_PATH,
        ACCEPTED_MANIFEST_RELATIVE_PATH,
        ACCEPTED_REPORT_MANIFEST_RELATIVE_PATH,
    ):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, destination)


def _copy_reporting_surface(target: Path) -> None:
    _copy_identity_files(target)
    source = repository_root()
    shutil.copytree(source / "results/m7/tables", target / "results/m7/tables")
    figures = target / "results/m7/figures"
    figures.mkdir(parents=True)
    for name in result_loader.REUSED_FIGURE_FILES:
        shutil.copy2(source / "results/m7/figures" / name, figures / name)


def _rewrite_report_manifest(
    target: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutate,
) -> None:
    path = target / ACCEPTED_REPORT_MANIFEST_RELATIVE_PATH
    payload = json.loads(path.read_text(encoding="utf-8"))
    mutate(payload)
    path.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
    monkeypatch.setattr(result_loader, "ACCEPTED_REPORT_MANIFEST_SHA256", _sha256(path))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
