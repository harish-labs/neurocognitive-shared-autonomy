import types

from src.evaluation.final_runner import _robustness, _statistics


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
