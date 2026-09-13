import pytest

from src.control.human_interaction import HumanInteractionController
from src.evaluation.final_contract import SCENARIOS
from src.evaluation.planning_scenarios import run_frozen_scenarios
from src.evaluation.simulated_human import apply_simulated_human_policy, feedback_for_subject


def test_s1_through_s7_definitions_are_exact():
    by_id = {scenario.scenario_id: scenario for scenario in SCENARIOS}
    assert tuple(by_id) == ("S1", "S2", "S3", "S4", "S5", "S6", "S7")
    assert (by_id["S1"].rows, by_id["S1"].columns, by_id["S1"].start, by_id["S1"].goal) == (3, 4, (1, 0), (0, 3))
    assert by_id["S2"].blocked_cells == ((1, 1),)
    assert by_id["S3"].risk_cells == (((1, 1), 0.75), ((1, 2), 0.75), ((1, 3), 0.75))
    assert by_id["S4"].blocked_cells == ((0, 1), (1, 1), (2, 1))
    assert by_id["S5"].replacement_start == (1, 0)
    assert by_id["S5"].replacement_blocked_cells == ((1, 1),)
    assert by_id["S6"].risk_cells == (((1, 2), 1.0),)
    assert by_id["S6"].safety_probe_action == "RIGHT"
    assert by_id["S7"].inject_emergency_stop is True


def test_frozen_scenarios_execute_expected_safety_behaviors():
    results = {result.scenario_id: result for result in run_frozen_scenarios(safety_enabled=True)}
    assert results["S1"].reached_goal
    assert results["S2"].reached_goal
    assert results["S3"].reached_goal
    assert results["S3"].cumulative_risk == 0.0
    assert results["S4"].no_safe_path and results["S4"].path_length == 0
    assert results["S5"].replanning_count == 1 and results["S5"].environment_change_consumed
    assert results["S6"].final_status == "REPLAN_REQUIRED"
    assert results["S6"].executed_actions == ()
    assert results["S7"].emergency_stop_success and results["S7"].path_length == 0


def test_safety_off_ablation_removes_only_hard_probe_veto_and_retains_stop():
    results = {result.scenario_id: result for result in run_frozen_scenarios(safety_enabled=False)}
    assert results["S6"].executed_actions == ("RIGHT",)
    assert results["S6"].executed_hard_safety_violations == 1
    assert results["S6"].final_state == (1, 2)
    assert results["S7"].emergency_stop_success and results["S7"].executed_actions == ()


@pytest.mark.parametrize(
    ("mode", "proposal", "intended", "command", "corrected"),
    [
        ("PROCEED", "victim_a", "victim_a", None, False),
        ("CONFIRM", "victim_a", "victim_a", "CONFIRM", False),
        ("CONFIRM", "victim_b", "victim_a", "OVERRIDE", True),
        ("DEFER", None, "victim_a", "OVERRIDE", True),
    ],
)
def test_simulated_human_exact_confirm_correction_and_defer_paths(mode, proposal, intended, command, corrected):
    result = apply_simulated_human_policy(
        episode_id=f"episode-{mode}-{proposal}",
        autonomy_mode=mode,
        proposed_goal=proposal,
        intended_goal=intended,
        candidate_names=("victim_a", "victim_b"),
        controller=HumanInteractionController(),
    )
    assert result.command_type == command
    assert result.correction_applied is corrected
    assert result.final_approved_goal == intended
    feedback = feedback_for_subject(result, "anon-subject")
    if command is None:
        assert feedback is None
    else:
        assert feedback.subject_id == "anon-subject"
        assert feedback.approved_goal_id == intended
        assert feedback.source_observation_id == result.command_id


def test_simulated_human_does_not_randomly_accept_pause_or_stop_in_primary_trials():
    for mode in ("PAUSE", "STOP"):
        with pytest.raises(ValueError, match="only PROCEED, CONFIRM, or DEFER"):
            apply_simulated_human_policy(
                episode_id="primary",
                autonomy_mode=mode,
                proposed_goal=None,
                intended_goal="victim_a",
                candidate_names=("victim_a", "victim_b"),
                controller=HumanInteractionController(),
            )
