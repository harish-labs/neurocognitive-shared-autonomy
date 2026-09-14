import ast
from pathlib import Path

import src.app.demo_fixture as demo_fixture
from src.app.demo_fixture import build_demo_trace
from src.autonomy.safety import SafetyController


def test_demo_is_deterministic_complete_and_explicitly_non_empirical() -> None:
    first = build_demo_trace()
    second = build_demo_trace()
    assert first == second
    assert first["fixture_kind"] == "DETERMINISTIC_EXPLANATORY_DEMO_NOT_EMPIRICAL"
    assert first["fixture_metadata"] == {
        "source": "fixed presentation probabilities; no protected EEG accessed",
        "runtime_entry_boundary": "calibrated Left/Right probability representation passed to the accepted goal-evidence adapter",
        "decoder_invoked": False,
        "calibrator_invoked": False,
        "reportable_experiment": False,
    }
    assert first["decision"]["approved_goal"] == "victim_a"
    assert first["approved_goal"] == "victim_a"
    assert first["human_authority"]["authorization_status"] == "AUTHORIZED"
    assert first["human_authority"]["policy_goal_adopted"] is True
    assert first["human_authority"]["human_commands"] == ()
    assert first["plan"]["status"] == "SUCCESS"
    assert first["plan"]["path"][-1] == (1, 4)
    assert first["execution"]["status"] == "SUCCESS"
    assert first["execution"]["executed_actions"] == first["plan"]["actions"]
    assert first["execution"]["visited_positions"] == first["plan"]["path"]
    assert first["execution"]["terminal_position"] == (1, 4)
    assert first["execution"]["reached_goal"] == "victim_a"
    assert first["execution"]["goal_reached"] is True
    assert first["execution"]["environment_terminated"] is True
    assert first["execution"]["cumulative_risk"] == first["plan"]["cumulative_risk"]
    assert len(first["safety_decisions"]) == len(first["execution"]["executed_actions"])
    assert all(item["status"] == "APPROVED" and item["safe"] for item in first["safety_decisions"])
    assert not set(first["execution"]["visited_positions"]) & set(first["environment"]["prohibited_cells"])


def test_demo_invokes_safety_once_before_each_executed_action(monkeypatch) -> None:
    calls: list[tuple[object, object]] = []
    original = SafetyController.check

    def recording_check(self, environment, **kwargs):
        calls.append((kwargs["current_position"], kwargs["proposed_action"]))
        return original(self, environment, **kwargs)

    monkeypatch.setattr(SafetyController, "check", recording_check)
    trace = build_demo_trace()
    assert len(calls) == len(trace["execution"]["executed_actions"])
    assert [position for position, _ in calls] == list(trace["plan"]["path"][:-1])


def test_demo_has_no_protected_eeg_model_or_experiment_dependency() -> None:
    path = Path(demo_fixture.__file__)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert not any(name.startswith("src.eeg") for name in imports)
    assert not any(name.startswith("src.models") for name in imports)
    assert not any(name.startswith("src.evaluation") for name in imports)
