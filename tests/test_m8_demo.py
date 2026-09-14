from src.app.demo_fixture import build_demo_trace


def test_demo_is_deterministic_and_explicitly_non_empirical() -> None:
    first = build_demo_trace()
    second = build_demo_trace()
    assert first == second
    assert first["fixture_kind"] == "DETERMINISTIC_EXPLANATORY_DEMO_NOT_EMPIRICAL"
    assert first["decision"]["approved_goal"] == "victim_a"
    assert first["plan"]["status"] == "SUCCESS"
    assert first["plan"]["path"][-1] == (1, 4)
