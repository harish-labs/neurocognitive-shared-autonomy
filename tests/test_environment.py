from __future__ import annotations

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.autonomy import environment


def make_environment() -> environment.SearchRescueEnvironment:
    return environment.SearchRescueEnvironment(
        environment.EnvironmentConfig(
            rows=3,
            columns=4,
            start=(1, 1),
            goals={"victim-a": (0, 2)},
            blocked_cells=frozenset({(2, 1)}),
            risk_map={(0, 0): 0.00, (0, 1): 0.25, (0, 2): 0.50, (0, 3): 0.75, (1, 3): 1.00},
        )
    )


def test_reset_restores_configured_start_and_seed_is_deterministic() -> None:
    env = make_environment()
    env.step(environment.Action.UP)

    first = env.reset(seed=42)
    second = env.reset(seed=42)

    assert first == second == environment.EnvironmentState((1, 1), False, None)
    assert env.last_seed == 42


@pytest.mark.parametrize(
    ("action", "expected"),
    ((environment.Action.UP, (0, 1)), (environment.Action.DOWN, (2, 1)), (environment.Action.LEFT, (1, 0)), (environment.Action.RIGHT, (1, 2))),
)
def test_cardinal_actions_follow_row_column_convention(action: environment.Action, expected: tuple[int, int]) -> None:
    env = environment.SearchRescueEnvironment(
        environment.EnvironmentConfig(rows=3, columns=4, start=(1, 1), goals={"victim-a": (0, 2)})
    )
    result = env.step(action)

    assert not result.blocked_by_structure
    assert result.state.position == expected


def test_blocked_transition_preserves_position() -> None:
    result = make_environment().step(environment.Action.DOWN)

    assert result.blocked_by_structure
    assert not result.moved
    assert result.state.position == (1, 1)


def test_wait_preserves_position() -> None:
    result = make_environment().step(environment.Action.WAIT)

    assert not result.moved
    assert result.state.position == (1, 1)


def test_entering_goal_terminates_episode() -> None:
    env = make_environment()
    env.step(environment.Action.UP)
    result = env.step(environment.Action.RIGHT)

    assert result.state.terminated
    assert result.state.reached_goal == "victim-a"
    with pytest.raises(environment.EnvironmentError, match="terminated"):
        env.step(environment.Action.WAIT)


def test_blocked_cells_remain_distinct_from_canonical_risk() -> None:
    env = make_environment()

    assert env.is_blocked((2, 1))
    assert env.risk_at((2, 1)) == 0.0
    assert not env.is_prohibited((2, 1))


def test_canonical_risk_values_are_preserved_and_prohibited_is_identifiable() -> None:
    env = make_environment()

    assert [env.risk_at((0, column)) for column in range(4)] == [0.0, 0.25, 0.5, 0.75]
    assert env.risk_at((1, 3)) == 1.0
    assert not env.is_prohibited((0, 3))
    assert env.is_prohibited((1, 3))
    assert not env.is_blocked((1, 3))


def test_raw_mechanics_do_not_apply_prohibited_risk_as_safety_policy() -> None:
    env = make_environment()
    env.step(environment.Action.RIGHT)
    result = env.step(environment.Action.RIGHT)

    assert result.state.position == (1, 3)
    assert result.moved
    assert result.destination_risk == 1.0


@pytest.mark.parametrize(
    "config",
    (
        environment.EnvironmentConfig(0, 2, (0, 0), {"goal": (0, 1)}),
        environment.EnvironmentConfig(2, 2, (2, 0), {"goal": (0, 1)}),
        environment.EnvironmentConfig(2, 2, (0, 0), {"goal": (0, 1)}, frozenset({(0, 0)})),
        environment.EnvironmentConfig(2, 2, (0, 0), {"goal": (2, 1)}),
        environment.EnvironmentConfig(2, 2, (0, 0), {"goal": (0, 1)}, frozenset({(2, 0)})),
        environment.EnvironmentConfig(2, 2, (0, 0), {"goal": (0, 1)}, risk_map={(2, 0): 0.25}),
        environment.EnvironmentConfig(2, 2, (0, 0), {"goal": (0, 1)}, risk_map={(1, 1): 0.1}),
    ),
)
def test_invalid_configuration_is_rejected(config: environment.EnvironmentConfig) -> None:
    with pytest.raises(environment.EnvironmentError):
        environment.SearchRescueEnvironment(config)


def test_invalid_action_and_query_coordinate_are_rejected() -> None:
    env = make_environment()
    with pytest.raises(environment.EnvironmentError, match="Action"):
        env.step("DIAGONAL")
    with pytest.raises(environment.EnvironmentError, match="outside"):
        env.risk_at((5, 5))
