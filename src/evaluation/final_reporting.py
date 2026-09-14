"""Deterministic reporting and provenance checks for the frozen M7 final result."""

from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

from src.evaluation.final_contract import canonical_json, sha256_file


DECODER_FAMILIES = ("csp_lda", "eegnet")
CONDITIONS = ("A", "B", "C", "D")
ABLATIONS = (
    "full",
    "full_minus_calibration",
    "full_minus_bayes",
    "full_minus_uncertainty",
    "full_minus_safety",
    "full_minus_adaptation",
)
FINAL_SUBJECT_IDS = (89, 16, 34, 29, 84, 57, 31, 93, 21, 76)
SEQUENTIAL_SUBJECT_IDS = (89, 16, 34, 29, 31, 93, 21, 76)
R1_SEVERITIES = ("0.0", "0.25", "0.5", "0.75", "1.0")
R2_SEVERITIES = ("0.0", "0.1", "0.2", "0.3", "0.4")
SCENARIO_IDS = tuple(f"S{index}" for index in range(1, 8))


class FinalReportingError(ValueError):
    """Raised when a final result or derived report violates the frozen contract."""


def load_final_result(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_final_result_contract(payload)
    return payload


def validate_final_result_contract(payload: Mapping[str, Any]) -> None:
    """Fail closed unless the stored result is complete under D-077--D-084."""

    missing = [name for name in (f"E{i}" for i in range(1, 10)) if name not in payload]
    if missing:
        raise FinalReportingError(f"Final result is missing experiment families: {missing}.")
    if tuple(payload.get("protected_final_subject_ids", ())) != FINAL_SUBJECT_IDS:
        raise FinalReportingError("Protected final-subject identity/order changed.")
    if tuple(payload.get("sequential_subject_ids", ())) != SEQUENTIAL_SUBJECT_IDS:
        raise FinalReportingError("Balanced sequential subject identity/order changed.")

    for name in ("E1", "E2", "E3", "E4", "E6", "E8", "E9"):
        if tuple(payload[name]) != DECODER_FAMILIES:
            raise FinalReportingError(f"{name} must contain both decoder families in frozen order.")
    for family in DECODER_FAMILIES:
        if tuple(payload["E6"][family]) != CONDITIONS:
            raise FinalReportingError("E6 must contain A/B/C/D in frozen order.")
        if int(payload["E8"][family]["subject_count"]) != len(FINAL_SUBJECT_IDS):
            raise FinalReportingError("E8 must retain all ten protected final subjects.")
        if set(map(int, payload["E8"][family]["subject_distribution"])) != set(FINAL_SUBJECT_IDS):
            raise FinalReportingError("E8 subject distribution differs from the frozen final cohort.")
        for condition in CONDITIONS:
            summary = payload["E6"][family][condition]
            if set(summary["subject_ids"]) != set(SEQUENTIAL_SUBJECT_IDS):
                raise FinalReportingError("E6 includes a subject outside the frozen sequential population.")
            _validate_mission_map(summary)

    for safety_key in ("safety_on", "safety_off"):
        if tuple(row["scenario_id"] for row in payload["E5"][safety_key]) != SCENARIO_IDS:
            raise FinalReportingError("E5 must retain the exact S1-S7 scenario suite.")

    ablations = payload["E7"]["ablations"]
    robustness = payload["E7"]["robustness"]
    for family in DECODER_FAMILIES:
        if set(ablations[family]) != set(ABLATIONS):
            raise FinalReportingError("E7 must contain the exact six-ablation registry.")
        for name in ABLATIONS:
            if set(ablations[family][name]["subject_ids"]) != set(SEQUENTIAL_SUBJECT_IDS):
                raise FinalReportingError("E7 ablation includes a nonparticipating subject.")
        _validate_robustness_family(
            robustness["R1_evidence_flattening"][family], R1_SEVERITIES, "R1"
        )
        _validate_robustness_family(
            robustness["R2_contradictory_evidence"][family], R2_SEVERITIES, "R2"
        )
        e9 = payload["E9"][family]
        if set(e9["subject_ids"]) != set(SEQUENTIAL_SUBJECT_IDS):
            raise FinalReportingError("E9 includes a subject outside the sequential population.")
        if e9["ordering_rule"] != "subject_id_then_run_id_then_first_source_event_sample_then_episode_id":
            raise FinalReportingError("E9 deterministic ordering rule changed.")

        comparison = payload["statistics"]["comparisons"][family]["D_minus_A_correctness"]
        if comparison["subject_count"] != 8 or set(map(int, comparison["subject_keys"])) != set(SEQUENTIAL_SUBJECT_IDS):
            raise FinalReportingError("D-079 comparison must use the exact eight sequential subjects.")
        if comparison["bootstrap_resamples"] != 10000 or comparison["bootstrap_seed"] != 42:
            raise FinalReportingError("D-079 bootstrap contract changed.")
        if comparison["permutation_method"] != "exact_paired_sign_flip" or comparison["permutation_assignments"] != 256:
            raise FinalReportingError("D-079 exact sign-flip contract changed.")

    expected_holm = {f"{family}.D_minus_A_correctness" for family in DECODER_FAMILIES}
    if set(payload["statistics"]["holm_adjusted_p_values"]) != expected_holm:
        raise FinalReportingError("D-079 Holm family differs from the frozen comparison family.")
    if "failure_taxonomy" not in payload or not payload["failure_taxonomy"].get("categories"):
        raise FinalReportingError("Failure taxonomy is missing.")
    if _contains_key(payload, "overall_score") or _contains_key(payload, "composite_score"):
        raise FinalReportingError("The frozen contract forbids a composite overall score.")


def compare_scientific_results(reference: Mapping[str, Any], candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Compare result science while excluding only execution-provenance identity."""

    validate_final_result_contract(reference)
    validate_final_result_contract(candidate)
    excluded = ("first_protected_outcome_access",)
    left = {key: value for key, value in reference.items() if key not in excluded}
    right = {key: value for key, value in candidate.items() if key not in excluded}
    equal = canonical_json(left) == canonical_json(right)
    differences = () if equal else tuple(_difference_paths(left, right))
    return {
        "scientific_fields_equal": equal,
        "excluded_provenance_fields": excluded,
        "difference_paths": differences,
    }


def generate_final_reports(result_path: str | Path, output_root: str | Path) -> dict[str, Any]:
    """Create deterministic tables/figures solely from one stored final-result JSON."""

    source = Path(result_path).resolve()
    result = load_final_result(source)
    root = Path(output_root).resolve()
    table_dir = root / "tables"
    figure_dir = root / "figures"
    table_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    table_specs = {
        "e1_decoder_performance.csv": _e1_rows(result),
        "e2_calibration.csv": _e2_rows(result),
        "e2_calibration_reliability.csv": _reliability_rows(result),
        "e6_abcd.csv": _system_rows(result["E6"]),
        "e7_ablations.csv": _ablation_rows(result),
        "e7_r1_robustness.csv": _robustness_rows(result, "R1_evidence_flattening"),
        "e7_r2_robustness.csv": _robustness_rows(result, "R2_contradictory_evidence"),
        "e8_subject_wise.csv": _e8_rows(result),
        "e9_adaptation_trajectory.csv": _e9_rows(result),
        "d079_statistics.csv": _statistics_rows(result),
        "failure_taxonomy.csv": _failure_rows(result),
    }
    artifacts: list[dict[str, Any]] = []
    for name, rows in table_specs.items():
        destination = table_dir / name
        _write_immutable_bytes(destination, _csv_bytes(rows))
        artifacts.append(_artifact_record(destination, root, "table", "GENERATED"))

    figure_specs = (
        ("e2_calibration_reliability.png", _plot_reliability, _reliability_rows(result)),
        ("e7_r1_robustness.png", lambda rows, path: _plot_robustness(rows, path, "R1 evidence flattening"), _robustness_rows(result, "R1_evidence_flattening")),
        ("e7_r2_robustness.png", lambda rows, path: _plot_robustness(rows, path, "R2 contradictory evidence"), _robustness_rows(result, "R2_contradictory_evidence")),
        ("e9_adaptation_trajectory.png", _plot_adaptation, _e9_rows(result)),
    )
    for name, plotter, rows in figure_specs:
        destination = figure_dir / name
        status = "GENERATED"
        if not _is_informative(rows):
            status = "NOT_INFORMATIVE"
        else:
            rendered = plotter(rows, None)
            _write_immutable_bytes(destination, rendered)
        artifacts.append(_artifact_record(destination, root, "figure", status))

    manifest = {
        "schema_version": "m7-final-report-artifacts-v1",
        "source_result_path": _relative_or_name(source, root),
        "source_result_sha256": sha256_file(source),
        "derivation": "stored_result_values_only",
        "new_metrics": False,
        "smoothing": False,
        "artifacts": artifacts,
    }
    manifest_path = root / "manifest" / "m7-final-report-artifacts-v5.json"
    _write_immutable_bytes(manifest_path, (canonical_json(manifest) + "\n").encode("utf-8"))
    return {**manifest, "report_manifest_path": _relative_or_name(manifest_path, root), "report_manifest_sha256": sha256_file(manifest_path)}


def _validate_mission_map(summary: Mapping[str, Any]) -> None:
    navigation = summary["navigation"]
    for mission in navigation["episodes"]:
        mission_map = mission["mission_map"]
        if mission_map["rows"] != 3 or mission_map["columns"] != 5 or tuple(mission_map["start"]) != (1, 0):
            raise FinalReportingError("E6 mission map geometry changed.")
        if {key: tuple(value) for key, value in mission_map["goals"].items()} != {
            "victim_a": (1, 4),
            "victim_b": (0, 2),
        }:
            raise FinalReportingError("E6 mission goals changed.")


def _validate_robustness_family(family: Mapping[str, Any], severities: Sequence[str], name: str) -> None:
    if tuple(family) != CONDITIONS:
        raise FinalReportingError(f"{name} must contain A/B/C/D.")
    if sum(len(family[condition]) for condition in CONDITIONS) != 20:
        raise FinalReportingError(f"{name} must contain 20 cells per decoder family.")
    for condition in CONDITIONS:
        if tuple(family[condition]) != tuple(severities):
            raise FinalReportingError(f"{name} severity registry changed.")
        for cell in family[condition].values():
            if set(cell["summary"]["subject_ids"]) != set(SEQUENTIAL_SUBJECT_IDS):
                raise FinalReportingError(f"{name} includes a nonparticipating subject.")
            if name == "R2" and cell.get("episode_boundaries_do_not_reset_selection") is not True:
                raise FinalReportingError("R2 population selection reset at an episode boundary.")


def _e1_rows(result):
    rows = []
    for family in DECODER_FAMILIES:
        item = result["E1"][family]["aggregate"]
        rows.append({
            "decoder_family": family,
            "sample_count": item["sample_count"],
            "correct_count": item["correct_count"],
            "accuracy": item["accuracy"],
            "balanced_accuracy": item["balanced_accuracy"],
            "macro_f1": item["macro_f1"],
            "evaluation_unit": item["evaluation_unit"],
        })
    return rows


def _e2_rows(result):
    rows = []
    for family in DECODER_FAMILIES:
        for mode in ("identity", "calibrated"):
            item = result["E2"][family][mode]
            rows.append({
                "decoder_family": family,
                "calibration_mode": mode,
                "ece": item["expected_calibration_error"],
                "brier_score": item["brier_score"],
                "bin_count": item["bin_count"],
                "positive_class_label": item["positive_class_label"],
            })
    return rows


def _reliability_rows(result):
    rows = []
    for family in DECODER_FAMILIES:
        for mode in ("identity", "calibrated"):
            for item in result["E2"][family][mode]["reliability_bins"]:
                rows.append({"decoder_family": family, "calibration_mode": mode, **item})
    return rows


def _system_rows(systems):
    rows = []
    for family in DECODER_FAMILIES:
        for condition in CONDITIONS:
            item = systems[family][condition]
            navigation = item["navigation"]
            rows.append({
                "decoder_family": family,
                "condition": condition,
                "episode_count": item["episode_count"],
                "success_count": item["success_count"],
                "success_rate": _rate(item["success_count"], item["episode_count"]),
                "committed_count": item["committed_count"],
                "wrong_all_rate": item["wrong_all_rate"],
                "wrong_committed_rate": item["wrong_committed_rate"],
                "mean_evidence_count": item["mean_evidence_count"],
                "navigation_success_count": navigation["task_navigation_success"],
                "navigation_denominator": navigation["mission_execution_count"],
                "environment_steps": navigation["environment_steps"],
                "cumulative_risk": navigation["cumulative_risk"],
                "unsafe_action_attempts": navigation["unsafe_action_attempts"],
                "executed_hard_safety_violations": navigation["executed_hard_safety_violations"],
                "replanning_count": navigation["replanning_count"],
                "no_safe_path_events": navigation["no_safe_path_events"],
                "subject_ids": "|".join(map(str, item["subject_ids"])),
            })
    return rows


def _ablation_rows(result):
    rows = []
    for family in DECODER_FAMILIES:
        for name in ABLATIONS:
            item = result["E7"]["ablations"][family][name]
            rows.append({
                "decoder_family": family,
                "ablation": name,
                "removed_component": item["removed_component"],
                "episode_count": item["episode_count"],
                "success_count": item["success_count"],
                "success_rate": _rate(item["success_count"], item["episode_count"]),
                "mean_evidence_count": item["mean_evidence_count"],
                "wrong_all_rate": item["wrong_all_rate"],
                "navigation_success_count": item["navigation"]["task_navigation_success"],
                "navigation_denominator": item["navigation"]["mission_execution_count"],
                "subject_ids": "|".join(map(str, item["subject_ids"])),
            })
    return rows


def _robustness_rows(result, family_name):
    rows = []
    source = result["E7"]["robustness"][family_name]
    for family in DECODER_FAMILIES:
        for condition in CONDITIONS:
            for severity, cell in source[family][condition].items():
                item = cell["summary"]
                provenance = cell["provenance"]
                rows.append({
                    "decoder_family": family,
                    "condition": condition,
                    "severity": float(severity),
                    "episode_count": item["episode_count"],
                    "success_count": item["success_count"],
                    "success_rate": _rate(item["success_count"], item["episode_count"]),
                    "mean_evidence_count": item["mean_evidence_count"],
                    "subject_ids": "|".join(map(str, item["subject_ids"])),
                    "population_size": provenance.get("population_size", "") if isinstance(provenance, dict) else "",
                    "realized_contamination_count": provenance.get("realized_contamination_count", "") if isinstance(provenance, dict) else "",
                    "realized_contamination_fraction": provenance.get("realized_contamination_fraction", "") if isinstance(provenance, dict) else "",
                })
    return rows


def _e8_rows(result):
    rows = []
    for family in DECODER_FAMILIES:
        for subject, item in result["E8"][family]["subject_distribution"].items():
            rows.append({"decoder_family": family, "subject_id": int(subject), **item})
    return rows


def _e9_rows(result):
    rows = []
    for family in DECODER_FAMILIES:
        for item in result["E9"][family]["trajectory"]:
            update = item["adaptation_update"] or {}
            rows.append({
                "decoder_family": family,
                "episode_index": item["episode_index"],
                "episode_id": item["episode_id"],
                "subject_id": item["subject_id"],
                "prior_victim_a": item["initial_prior"][0],
                "prior_victim_b": item["initial_prior"][1],
                "human_action": item["human_action"],
                "adaptation_updated": bool(update),
                "evidence_latency": item["evidence_latency"],
                "task_outcome": item["task_outcome"],
            })
    return rows


def _statistics_rows(result):
    rows = []
    holm = result["statistics"]["holm_adjusted_p_values"]
    for family in DECODER_FAMILIES:
        comparison_name = f"{family}.D_minus_A_correctness"
        item = result["statistics"]["comparisons"][family]["D_minus_A_correctness"]
        rows.append({
            "decoder_family": family,
            "comparison": "D_minus_A_correctness",
            "subject_count": item["subject_count"],
            "subject_keys": "|".join(item["subject_keys"]),
            "effect_mean_difference": item["raw_effect_mean_difference"],
            "ci_lower": item["ci_lower"],
            "ci_upper": item["ci_upper"],
            "bootstrap_resamples": item["bootstrap_resamples"],
            "bootstrap_seed": item["bootstrap_seed"],
            "permutation_method": item["permutation_method"],
            "permutation_assignments": item["permutation_assignments"],
            "raw_p_value": item["raw_p_value"],
            "holm_adjusted_p_value": holm[comparison_name],
        })
    return rows


def _failure_rows(result):
    taxonomy = result["failure_taxonomy"]
    return [
        {
            "category": category,
            "result_status": taxonomy["status"],
            "count": "NOT_AGGREGATED_IN_RESULT_SCHEMA",
        }
        for category in taxonomy["categories"]
    ]


def _plot_reliability(rows, _path):
    figure, axes = plt.subplots(1, 2, figsize=(9, 4), sharex=True, sharey=True)
    for axis, family in zip(axes, DECODER_FAMILIES):
        axis.plot((0.5, 1.0), (0.5, 1.0), color="0.6", linestyle="--", label="ideal")
        for mode, marker in (("identity", "o"), ("calibrated", "s")):
            selected = [row for row in rows if row["decoder_family"] == family and row["calibration_mode"] == mode and row["sample_count"]]
            axis.plot([row["mean_confidence"] for row in selected], [row["empirical_accuracy"] for row in selected], marker=marker, label=mode)
        axis.set_title(family)
        axis.set_xlabel("mean confidence")
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("empirical accuracy")
    axes[1].legend()
    return _figure_bytes(figure)


def _plot_robustness(rows, _path, title):
    figure, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=True)
    for axis, family in zip(axes, DECODER_FAMILIES):
        for condition in CONDITIONS:
            selected = [row for row in rows if row["decoder_family"] == family and row["condition"] == condition]
            axis.plot([row["severity"] for row in selected], [row["success_rate"] for row in selected], marker="o", label=condition)
        axis.set_title(family)
        axis.set_xlabel("severity")
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("episode success rate")
    axes[1].legend(title="condition")
    figure.suptitle(title)
    return _figure_bytes(figure)


def _plot_adaptation(rows, _path):
    figure, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=True)
    for axis, family in zip(axes, DECODER_FAMILIES):
        selected = [row for row in rows if row["decoder_family"] == family]
        axis.plot([row["episode_index"] for row in selected], [row["prior_victim_a"] for row in selected], marker=".", linewidth=1)
        axis.set_title(family)
        axis.set_xlabel("ordered episode index")
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("initial prior P(victim_a)")
    return _figure_bytes(figure)


def _figure_bytes(figure) -> bytes:
    buffer = io.BytesIO()
    figure.tight_layout()
    figure.savefig(
        buffer,
        format="png",
        dpi=120,
        metadata={"Software": "neurocognitive-shared-autonomy deterministic M7 reporting"},
    )
    plt.close(figure)
    return buffer.getvalue()


def _is_informative(rows: Sequence[Mapping[str, Any]]) -> bool:
    if not rows:
        return False
    value_keys = ("empirical_accuracy", "success_rate", "prior_victim_a")
    values = [row[key] for row in rows for key in value_keys if key in row and row[key] not in (None, "")]
    return len(set(values)) > 1


def _csv_bytes(rows: Sequence[Mapping[str, Any]]) -> bytes:
    if not rows:
        raise FinalReportingError("A required report table has no rows.")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def _write_immutable_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != content:
        raise FinalReportingError(f"Derived report already exists with different content: {path}.")
    if not path.exists():
        path.write_bytes(content)


def _artifact_record(path: Path, root: Path, artifact_type: str, status: str) -> dict[str, Any]:
    exists = path.exists()
    return {
        "path": _relative_or_name(path, root),
        "artifact_type": artifact_type,
        "status": status,
        "sha256": sha256_file(path) if exists else None,
    }


def _relative_or_name(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root.parent).as_posix()
    except ValueError:
        return path.name


def _rate(numerator, denominator):
    return float(numerator) / float(denominator) if denominator else None


def _contains_key(value: Any, target: str) -> bool:
    if isinstance(value, Mapping):
        return target in value or any(_contains_key(item, target) for item in value.values())
    if isinstance(value, (list, tuple)):
        return any(_contains_key(item, target) for item in value)
    return False


def _difference_paths(left: Any, right: Any, prefix: str = "$") -> Iterable[str]:
    if type(left) is not type(right):
        yield prefix
    elif isinstance(left, Mapping):
        for key in sorted(set(left) | set(right)):
            if key not in left or key not in right:
                yield f"{prefix}.{key}"
            else:
                yield from _difference_paths(left[key], right[key], f"{prefix}.{key}")
    elif isinstance(left, list):
        if len(left) != len(right):
            yield prefix
        else:
            for index, (left_item, right_item) in enumerate(zip(left, right)):
                yield from _difference_paths(left_item, right_item, f"{prefix}[{index}]")
    elif left != right:
        yield prefix


def _parse_args(argv: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", required=True)
    parser.add_argument("--output-root", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    manifest = generate_final_reports(args.result, args.output_root)
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
