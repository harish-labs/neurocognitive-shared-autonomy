from __future__ import annotations

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.autonomy.environment import Action, EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.safety import InterventionType, SafetyController, SafetyStatus


def make_environment(
    *,
    blocked_cells: frozenset[tuple[int, int]] = frozenset(),
    risk_map: dict[tuple[int, int], float] | None = None,
) -> SearchRescueEnvironment:
    return SearchRescueEnvironment(
        EnvironmentConfig(
            rows=3,
            columns=4,
            start=(1, 1),
            goals={"goal": (0, 3)},
            blocked_cells=blocked_cells,
            risk_map={} if risk_map is None else risk_map,
        )
    )


def check(
    environment: SearchRescueEnvironment,
    *,
    proposed_action: object = Action.RIGHT,
    **kwargs: object,
):
    return SafetyController().check(environment, current_position=(1, 1), proposed_action=proposed_action, **kwargs)


def test_valid_free_move_is_approved_without_substitution() -> None:
    decision = check(make_environment())

    assert decision.status is SafetyStatus.APPROVED
    assert decision.safe
    assert decision.approved_action is Action.RIGHT
    assert decision.intervention_type is InterventionType.NONE
    assert decision.proposed_next_position == (1, 2)
    assert not decision.requires_replan


def test_high_risk_move_remains_safety_permitted() -> None:
    decision = check(make_environment(risk_map={(1, 2): 0.75}))

    assert decision.status is SafetyStatus.APPROVED
    assert decision.approved_action is Action.RIGHT


def test_wait_on_valid_state_is_approved_without_replan() -> None:
    decision = check(make_environment(), proposed_action=Action.WAIT)

    assert decision.status is SafetyStatus.APPROVED
    assert decision.approved_action is Action.WAIT
    assert decision.proposed_next_position == decision.current_position
    assert not decision.requires_replan


def test_emergency_stop_overrides_pause_and_lower_priority_conditions() -> None:
    decision = check(
        make_environment(blocked_cells=frozenset({(1, 2)})),
        paused=True,
        emergency_stop=True,
    )

    assert decision.status is SafetyStatus.HALTED
    assert decision.intervention_type is InterventionType.EMERGENCY_STOP
    assert_not_approved(decision)
    assert not decision.requires_replan


def test_pause_overrides_blocked_and_prohibited_checks() -> None:
    decision = check(
        make_environment(blocked_cells=frozenset({(1, 2)}), risk_map={(1, 2): 1.0}),
        paused=True,
    )

    assert decision.status is SafetyStatus.HALTED
    assert decision.intervention_type is InterventionType.PAUSED
    assert_not_approved(decision)
    assert not decision.requires_replan


@pytest.mark.parametrize(
    "current_position",
    (("bad", 1), (4, 1), (1, 2), (1, 3)),
)
def test_invalid_blocked_and_prohibited_current_state_halts(current_position: object) -> None:
    env = make_environment(blocked_cells=frozenset({(1, 2)}), risk_map={(1, 3): 1.0})
    decision = SafetyController().check(env, current_position=current_position, proposed_action=Action.RIGHT)

    assert decision.status is SafetyStatus.HALTED
    assert decision.intervention_type is InterventionType.INVALID_STATE
    assert_not_approved(decision)


@pytest.mark.parametrize("invalid_action", ("RIGHT", "DIAGONAL", 8, 1.0, True))
def test_invalid_actions_are_rejected_without_coercion(invalid_action: object) -> None:
    decision = check(make_environment(), proposed_action=invalid_action)

    assert decision.status is SafetyStatus.REJECTED
    assert decision.intervention_type is InterventionType.INVALID_ACTION
    assert_not_approved(decision)
    assert not decision.requires_replan


def test_numeric_gymnasium_action_is_accepted_only_when_exact() -> None:
    decision = check(make_environment(), proposed_action=int(Action.RIGHT))

    assert decision.status is SafetyStatus.APPROVED
    assert decision.approved_action is Action.RIGHT


def test_out_of_bounds_is_rejected_before_any_risk_lookup() -> None:
    env = make_environment()
    decision = SafetyController().check(env, current_position=(0, 0), proposed_action=Action.UP)

    assert decision.status is SafetyStatus.REJECTED
    assert decision.intervention_type is InterventionType.OUT_OF_BOUNDS
    assert decision.proposed_next_position == (-1, 0)
    assert decision.requires_replan
    assert_not_approved(decision)


def test_blocked_destination_requires_replan() -> None:
    decision = check(make_environment(blocked_cells=frozenset({(1, 2)})))

    assert decision.status is SafetyStatus.REPLAN_REQUIRED
    assert decision.intervention_type is InterventionType.BLOCKED_CELL
    assert decision.requires_replan
    assert_not_approved(decision)


def test_prohibited_destination_requires_replan() -> None:
    decision = check(make_environment(risk_map={(1, 2): 1.0}))

    assert decision.status is SafetyStatus.REPLAN_REQUIRED
    assert decision.intervention_type is InterventionType.PROHIBITED_HAZARD
    assert decision.requires_replan
    assert_not_approved(decision)


def test_check_does_not_mutate_environment_or_call_step(monkeypatch: pytest.MonkeyPatch) -> None:
    env = make_environment()
    initial_state = env.state

    def fail_step(*args: object, **kwargs: object) -> None:
        raise AssertionError("SafetyController must not execute the environment.")

    monkeypatch.setattr(env, "step", fail_step)
    decision = check(env)

    assert decision.status is SafetyStatus.APPROVED
    assert env.state == initial_state


def test_identical_request_produces_identical_decision() -> None:
    env = make_environment()
    controller = SafetyController()

    first = controller.check(env, current_position=(1, 1), proposed_action=Action.RIGHT)
    second = controller.check(env, current_position=(1, 1), proposed_action=Action.RIGHT)

    assert first == second


def assert_not_approved(decision: object) -> None:
    assert getattr(decision, "safe") is False
    assert getattr(decision, "approved_action") is None
