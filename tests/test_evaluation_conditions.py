from dataclasses import fields

from src.evaluation.conditions import ABLATIONS, PRINCIPAL_CONDITIONS, ComponentSet, ConditionId, get_condition


def test_d077_principal_condition_registry_is_exact():
    assert [(key.value, value.name) for key, value in PRINCIPAL_CONDITIONS.items()] == [
        ("A", "Direct EEG"),
        ("B", "Confidence-Aware"),
        ("C", "Bayesian Shared Autonomy"),
        ("D", "Full System"),
    ]
    a, b, c, d = (PRINCIPAL_CONDITIONS[key].components for key in ConditionId)
    assert a == ComponentSet(True, False, 1, False, False, False, True, True, True, True, False)
    assert b == ComponentSet(True, True, 1, False, True, True, True, True, True, True, False)
    assert c == ComponentSet(True, True, 5, True, True, True, True, True, True, True, False)
    assert d == ComponentSet(True, True, 5, True, True, True, True, True, True, True, True)
    assert get_condition("D") is PRINCIPAL_CONDITIONS[ConditionId.D]


def test_each_ablation_changes_only_the_named_component():
    full = ABLATIONS["full"].components
    expected = {
        "full_minus_calibration": "calibration",
        "full_minus_bayes": "sequential_bayes",
        "full_minus_uncertainty": "uncertainty_gating",
        "full_minus_safety": "hard_safety",
        "full_minus_adaptation": "adaptation",
    }
    assert set(ABLATIONS) == {"full", *expected}
    for key, removed in expected.items():
        ablation = ABLATIONS[key]
        differences = [field.name for field in fields(ComponentSet) if getattr(full, field.name) != getattr(ablation.components, field.name)]
        assert differences == [removed]
        assert getattr(ablation.components, removed) is False
