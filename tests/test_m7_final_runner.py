import types

from src.evaluation.final_runner import _ablations, _execute_full_system_mission, _robustness, _sequential_rows, _statistics, _systems


def _rows(n=20):
    rows = []
    for i in range(n):
        rows.append({
            "decoder_family": "csp_lda",
            "episode_id": f"ep-{i:03d}",
            "subject_id": (i % 4) + 1,
            "intended_goal": "victim_a" if i % 2 == 0 else "victim_b",
            "raw": [[0.8, 0.2]],
            "calibrated": [[0.8, 0.2]],
        })
    return rows


def test_r2_population_selection_is_global_and_levels_distinguishable():
    manifest = types.SimpleNamespace(r1_severities=(0.0,), r2_severities=(0.1, 0.2, 0.3, 0.4), r2_seed=42)
    result = _robustness(_rows(), manifest)
    entries = result["R2_contradictory_evidence"]["csp_lda"]
    counts = [entries[str(q)]["provenance"]["realized_count"] for q in manifest.r2_severities]
    assert counts == [2, 4, 6, 8]
    assert entries["0.4"]["provenance"]["population_size"] == 20
    assert entries["0.4"]["episode_boundaries_do_not_reset_selection"] is True
    assert len(entries["0.4"]["provenance"]["selected_observation_ids"]) == 8


def test_statistics_are_subject_level_not_pseudo_replicated():
    result = _statistics(_rows())
    comparison = result["comparisons"]["csp_lda"]["D_minus_A_correctness"]
    assert comparison["evaluation_unit"] == "subject"
    assert comparison["subject_count"] == 4
    assert comparison["bootstrap_resamples"] == 10000
    assert "csp_lda.D_minus_A_correctness" in result["holm_adjusted_p_values"]


def test_sequential_filter_excludes_subjects_57_and_84():
    manifest = types.SimpleNamespace(participation_manifest={"included_subject_ids": [89, 16, 34, 29, 31, 93, 21, 76]})
    rows = [{**_rows(1)[0], "subject_id": sid, "episode_id": f"{sid}-ep"} for sid in [89, 16, 34, 29, 31, 93, 21, 76, 57, 84]]
    filtered = _sequential_rows(rows, manifest)
    assert sorted({r["subject_id"] for r in filtered}) == [16, 21, 29, 31, 34, 76, 89, 93]
    assert 57 not in {r["subject_id"] for r in filtered}
    assert 84 not in {r["subject_id"] for r in filtered}


def test_ablation_registry_contains_distinct_safety_and_adaptation_outputs():
    rows = _rows()
    rows = [{**row, "calibrated": [[0.8, 0.2]] * 5, "raw": [[0.8, 0.2]] * 5} for row in rows]
    result = _ablations(rows)
    assert "navigation" in result["csp_lda"]["full"]
    assert "navigation" in result["csp_lda"]["full_minus_safety"]
    assert result["csp_lda"]["full"]["navigation"]["safety_enabled"] is True
    assert result["csp_lda"]["full_minus_safety"]["navigation"]["safety_enabled"] is False


def test_e6_mission_uses_frozen_two_goal_map_and_approved_goal():
    execution = _execute_full_system_mission("victim_b", safety_enabled=True)
    assert execution["mission_map"]["goals"] == {"victim_a": (1, 4), "victim_b": (0, 2)}
    assert execution["approved_goal"] == "victim_b"
    assert execution["reached_goal"] == "victim_b"
    assert execution["environment_steps"] == 3
    assert execution["final_status"] == "SUCCESS"


def test_e6_system_navigation_is_episode_mission_execution_not_scenario_aggregate():
    row = {**_rows(1)[0], "calibrated": [[1.0, 0.0]] * 5, "raw": [[1.0, 0.0]] * 5}
    result = _systems([row], systems=("A",), include_navigation=True)
    navigation = result["csp_lda"]["A"]["navigation"]
    assert navigation["mission_execution_count"] == 1
    assert navigation["environment_steps"] == 4
    assert navigation["episodes"][0]["mission_map"]["rows"] == 3


def test_safety_off_mission_ablation_preserves_emergency_stop_authority():
    full = _execute_full_system_mission("victim_a", safety_enabled=True, emergency_stop=True)
    without_safety = _execute_full_system_mission("victim_a", safety_enabled=False, emergency_stop=True)
    assert full["final_status"] == "HALTED"
    assert without_safety["final_status"] == "HALTED"
    assert full["safety_decision_count"] == 1
    assert without_safety["safety_decision_count"] == 0
