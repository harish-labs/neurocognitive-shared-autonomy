from copy import deepcopy
import json
from pathlib import Path

import pytest

from src.evaluation.final_reporting import (
    FinalReportingError,
    compare_scientific_results,
    generate_final_reports,
    validate_final_result_contract,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
V4_RESULT = REPOSITORY_ROOT / "results" / "m7" / "final" / "m7-final-results-v4.json"


def _v4():
    return json.loads(V4_RESULT.read_text(encoding="utf-8"))


def test_r03_result_satisfies_complete_frozen_contract():
    payload = _v4()
    validate_final_result_contract(payload)
    assert len(payload["E7"]["ablations"]["csp_lda"]) == 6
    assert sum(
        len(cells)
        for cells in payload["E7"]["robustness"]["R1_evidence_flattening"]["csp_lda"].values()
    ) == 20
    assert sum(
        len(cells)
        for cells in payload["E7"]["robustness"]["R2_contradictory_evidence"]["eegnet"].values()
    ) == 20


def test_final_contract_rejects_sequential_leakage_and_missing_experiment():
    payload = _v4()
    payload["sequential_subject_ids"].append(57)
    with pytest.raises(FinalReportingError, match="sequential subject"):
        validate_final_result_contract(payload)

    payload = _v4()
    del payload["E9"]
    with pytest.raises(FinalReportingError, match="missing experiment"):
        validate_final_result_contract(payload)


def test_scientific_comparison_excludes_only_execution_provenance():
    reference = _v4()
    candidate = deepcopy(reference)
    candidate["first_protected_outcome_access"]["software_sha"] = "final-software-sha"
    candidate["first_protected_outcome_access"]["authorization_manifest_sha256"] = "a" * 64
    comparison = compare_scientific_results(reference, candidate)
    assert comparison == {
        "scientific_fields_equal": True,
        "excluded_provenance_fields": ("first_protected_outcome_access",),
        "difference_paths": (),
    }

    candidate["E6"]["csp_lda"]["A"]["success_count"] += 1
    comparison = compare_scientific_results(reference, candidate)
    assert comparison["scientific_fields_equal"] is False
    assert "$.E6.csp_lda.A.success_count" in comparison["difference_paths"]


def test_reporting_is_complete_and_byte_deterministic(tmp_path):
    first_root = tmp_path / "first" / "m7"
    second_root = tmp_path / "second" / "m7"
    first = generate_final_reports(V4_RESULT, first_root)
    second = generate_final_reports(V4_RESULT, second_root)

    assert first["source_result_sha256"] == second["source_result_sha256"]
    assert len([item for item in first["artifacts"] if item["artifact_type"] == "table"]) == 11
    assert len([item for item in first["artifacts"] if item["artifact_type"] == "figure"]) == 4
    assert all(item["status"] in {"GENERATED", "NOT_INFORMATIVE"} for item in first["artifacts"])

    first_files = {
        path.relative_to(first_root).as_posix(): path.read_bytes()
        for path in first_root.rglob("*")
        if path.is_file() and path.name != "m7-final-report-artifacts-v5.json"
    }
    second_files = {
        path.relative_to(second_root).as_posix(): path.read_bytes()
        for path in second_root.rglob("*")
        if path.is_file() and path.name != "m7-final-report-artifacts-v5.json"
    }
    assert first_files == second_files


def test_failure_table_does_not_fabricate_unavailable_counts(tmp_path):
    root = tmp_path / "m7"
    generate_final_reports(V4_RESULT, root)
    table = (root / "tables" / "failure_taxonomy.csv").read_text(encoding="utf-8")
    assert "NOT_AGGREGATED_IN_RESULT_SCHEMA" in table
    assert "provenance_manifest_artifact_failure" in table
