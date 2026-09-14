"""Fail-closed access to the immutable, accepted M7 result package.

This module is intentionally unable to execute experiments, fit models, or select
alternate result versions.  It validates and exposes the single accepted v5
artifact and its frozen manifest as recursively immutable Python objects.
"""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

ACCEPTED_RESULT_RELATIVE_PATH = Path("results/m7/final/m7-final-results-v5.json")
ACCEPTED_MANIFEST_RELATIVE_PATH = Path(
    "results/m7/manifest/m7-final-execution-v6-d084-r03-final.json"
)
ACCEPTED_RESULT_SHA256 = "b5c7cc2efdbbbab53c65d54aa77542a2e69a71c42d5bdc670e2fd8c34af2dd9b"
ACCEPTED_MANIFEST_SHA256 = "f837258312adf17ec1a04079c71c5461838a4aff5096541acd993bb94da24306"
ACCEPTED_SOFTWARE_SHA = "a1a696204a8b06263efa8bb57abc610af3f7361e"
ACCEPTED_RESULT_SCHEMA = "m7-t02-results-v4"
ACCEPTED_MANIFEST_RESULT_SCHEMA = "m7-final-results-v1"
REQUIRED_EXPERIMENTS = tuple(f"E{i}" for i in range(1, 10))
TABLE_FILES = (
    "e1_decoder_performance.csv",
    "e2_calibration.csv",
    "e2_calibration_reliability.csv",
    "e6_abcd.csv",
    "e7_ablations.csv",
    "e7_r1_robustness.csv",
    "e7_r2_robustness.csv",
    "e8_subject_wise.csv",
    "e9_adaptation_trajectory.csv",
    "d079_statistics.csv",
    "failure_taxonomy.csv",
)


class ResultIntegrityError(RuntimeError):
    """Raised when an accepted result, manifest, schema, or provenance check fails."""


@dataclass(frozen=True)
class PresentationData:
    """Recursively immutable accepted data plus its verified provenance."""

    repository_root: Path
    result_path: Path
    manifest_path: Path
    result_sha256: str
    manifest_sha256: str
    result: Mapping[str, Any]
    manifest: Mapping[str, Any]
    tables: Mapping[str, tuple[Mapping[str, str], ...]]

    @property
    def protected_subject_count(self) -> int:
        return len(self.result["protected_final_subject_ids"])

    @property
    def sequential_subject_count(self) -> int:
        return len(self.result["sequential_subject_ids"])


def repository_root() -> Path:
    """Return the repository root from this presentation module's fixed location."""
    return Path(__file__).resolve().parents[2]


def is_accepted_result_path(path: str | Path, *, root: str | Path | None = None) -> bool:
    """Return true only for the canonical accepted v5 path under ``root``."""
    base = Path(root).resolve() if root is not None else repository_root()
    return Path(path).resolve() == (base / ACCEPTED_RESULT_RELATIVE_PATH).resolve()


def load_presentation_data(
    root: str | Path | None = None,
    *,
    verify_hashes: bool = True,
) -> PresentationData:
    """Load and validate the only accepted M7 package without running science code."""
    base = Path(root).resolve() if root is not None else repository_root()
    result_path = base / ACCEPTED_RESULT_RELATIVE_PATH
    manifest_path = base / ACCEPTED_MANIFEST_RELATIVE_PATH
    result_hash = _required_hash(result_path, "accepted result")
    manifest_hash = _required_hash(manifest_path, "accepted execution manifest")
    if verify_hashes and result_hash != ACCEPTED_RESULT_SHA256:
        raise ResultIntegrityError(
            f"Accepted result hash mismatch: expected {ACCEPTED_RESULT_SHA256}, got {result_hash}."
        )
    if verify_hashes and manifest_hash != ACCEPTED_MANIFEST_SHA256:
        raise ResultIntegrityError(
            f"Accepted manifest hash mismatch: expected {ACCEPTED_MANIFEST_SHA256}, got {manifest_hash}."
        )

    result = _read_json(result_path, "accepted result")
    manifest = _read_json(manifest_path, "accepted execution manifest")
    _validate_result(result)
    _validate_manifest(manifest)
    _validate_cross_provenance(result, manifest)

    tables_dir = base / "results/m7/tables"
    tables = {name: _read_csv(tables_dir / name) for name in TABLE_FILES}
    _validate_tables(tables, result)
    return PresentationData(
        repository_root=base,
        result_path=result_path,
        manifest_path=manifest_path,
        result_sha256=result_hash,
        manifest_sha256=manifest_hash,
        result=_freeze(result),
        manifest=_freeze(manifest),
        tables=_freeze(tables),
    )


def headline_metrics(data: PresentationData) -> Mapping[str, Any]:
    """Return dashboard/report headline values directly from accepted tables."""
    e1 = {row["decoder_family"]: row for row in data.tables["e1_decoder_performance.csv"]}
    e2 = {
        (row["decoder_family"], row["calibration_mode"]): row
        for row in data.tables["e2_calibration.csv"]
    }
    e6 = {
        (row["decoder_family"], row["condition"]): row
        for row in data.tables["e6_abcd.csv"]
    }
    stats = {row["decoder_family"]: row for row in data.tables["d079_statistics.csv"]}
    return MappingProxyType(
        {
            "protected_subjects": data.protected_subject_count,
            "sequential_subjects": data.sequential_subject_count,
            "eeg_trials": int(e1["csp_lda"]["sample_count"]),
            "csp_accuracy": float(e1["csp_lda"]["accuracy"]),
            "eegnet_accuracy": float(e1["eegnet"]["accuracy"]),
            "csp_ece_raw": float(e2[("csp_lda", "identity")]["ece"]),
            "csp_ece_calibrated": float(e2[("csp_lda", "calibrated")]["ece"]),
            "eegnet_ece_raw": float(e2[("eegnet", "identity")]["ece"]),
            "eegnet_ece_calibrated": float(e2[("eegnet", "calibrated")]["ece"]),
            "csp_d_success": int(e6[("csp_lda", "D")]["success_count"]),
            "eegnet_d_success": int(e6[("eegnet", "D")]["success_count"]),
            "system_episode_count": int(e6[("csp_lda", "D")]["episode_count"]),
            "csp_holm_p": float(stats["csp_lda"]["holm_adjusted_p_value"]),
            "eegnet_holm_p": float(stats["eegnet"]["holm_adjusted_p_value"]),
        }
    )


def _required_hash(path: Path, label: str) -> str:
    if not path.is_file():
        raise ResultIntegrityError(f"Required {label} is missing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ResultIntegrityError(f"Could not parse {label} at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ResultIntegrityError(f"{label.capitalize()} must be a JSON object.")
    return value


def _read_csv(path: Path) -> tuple[dict[str, str], ...]:
    if not path.is_file():
        raise ResultIntegrityError(f"Required accepted table is missing: {path}")
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = tuple(dict(row) for row in csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as exc:
        raise ResultIntegrityError(f"Could not parse accepted table {path}: {exc}") from exc
    if not rows:
        raise ResultIntegrityError(f"Accepted table is empty: {path}")
    return rows


def _validate_result(result: Mapping[str, Any]) -> None:
    missing = [key for key in (*REQUIRED_EXPERIMENTS, "statistics", "failure_taxonomy") if key not in result]
    if missing:
        raise ResultIntegrityError(f"Accepted result is missing required sections: {', '.join(missing)}")
    if result.get("schema_version") != ACCEPTED_RESULT_SCHEMA:
        raise ResultIntegrityError(
            f"Unexpected result schema {result.get('schema_version')!r}; expected {ACCEPTED_RESULT_SCHEMA!r}."
        )
    protected = result.get("protected_final_subject_ids")
    sequential = result.get("sequential_subject_ids")
    if not isinstance(protected, list) or len(protected) != 10 or len(set(protected)) != 10:
        raise ResultIntegrityError("Accepted E1/E2/E8 protected cohort must contain 10 unique subjects.")
    if not isinstance(sequential, list) or len(sequential) != 8 or len(set(sequential)) != 8:
        raise ResultIntegrityError("Accepted sequential cohort must contain 8 unique subjects.")
    if not set(sequential).issubset(protected):
        raise ResultIntegrityError("Sequential subjects must be a subset of the protected cohort.")


def _validate_manifest(manifest: Mapping[str, Any]) -> None:
    if manifest.get("software_sha") != ACCEPTED_SOFTWARE_SHA:
        raise ResultIntegrityError("Execution manifest does not identify the accepted software SHA.")
    if manifest.get("result_schema_version") != ACCEPTED_MANIFEST_RESULT_SCHEMA:
        raise ResultIntegrityError("Execution manifest has an unexpected frozen result contract version.")
    families = manifest.get("experiment_families")
    if not isinstance(families, list) or not set(REQUIRED_EXPERIMENTS).issubset(families):
        raise ResultIntegrityError("Execution manifest does not freeze all E1–E9 families.")


def _validate_cross_provenance(result: Mapping[str, Any], manifest: Mapping[str, Any]) -> None:
    access = result.get("first_protected_outcome_access")
    if not isinstance(access, dict):
        raise ResultIntegrityError("Accepted result lacks protected-access provenance.")
    if access.get("authorization_manifest_sha256") != ACCEPTED_MANIFEST_SHA256:
        raise ResultIntegrityError("Result is not bound to the accepted execution manifest hash.")
    if access.get("software_sha") != ACCEPTED_SOFTWARE_SHA:
        raise ResultIntegrityError("Result is not bound to the accepted software SHA.")
    split = manifest.get("split_manifest")
    if not isinstance(split, dict) or split.get("partition_counts", {}).get("final_test") != 10:
        raise ResultIntegrityError("Manifest final-test cohort count is not the accepted n=10.")


def _validate_tables(tables: Mapping[str, tuple[dict[str, str], ...]], result: Mapping[str, Any]) -> None:
    e1 = tables["e1_decoder_performance.csv"]
    if {row.get("decoder_family") for row in e1} != {"csp_lda", "eegnet"}:
        raise ResultIntegrityError("E1 table must contain exactly the two accepted decoder families.")
    if {int(row["sample_count"]) for row in e1} != {303}:
        raise ResultIntegrityError("E1 table must preserve the accepted 303-trial evaluation.")
    e6 = tables["e6_abcd.csv"]
    if {row.get("condition") for row in e6} != {"A", "B", "C", "D"}:
        raise ResultIntegrityError("E6 table must preserve all A/B/C/D conditions.")
    if {int(row["episode_count"]) for row in e6} != {38}:
        raise ResultIntegrityError("E6 table must preserve the accepted 38 sequential episodes.")
    if len(result["protected_final_subject_ids"]) != 10 or len(result["sequential_subject_ids"]) != 8:
        raise ResultIntegrityError("Accepted cohort sizes changed during table validation.")


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value
