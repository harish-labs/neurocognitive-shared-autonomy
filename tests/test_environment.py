from __future__ import annotations

from pathlib import Path
import sys

import gymnasium as gym
import numpy as np
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

    first_observation, first_info = env.reset(seed=42)
    second_observation, second_info = env.reset(seed=42)

    assert isinstance(env, gym.Env)
    assert np.array_equal(first_observation, second_observation)
    assert np.array_equal(first_observation, np.array((1, 1), dtype=np.int64))
    assert first_info == second_info
    assert first_info["position"] == (1, 1)
    assert env.last_seed == 42


def test_gymnasium_spaces_match_action_and_observation_contracts() -> None:
    env = make_environment()
    observation, _ = env.reset()

    assert env.action_space == gym.spaces.Discrete(5)
    assert [environment.Action(index).name for index in range(env.action_space.n)] == ["UP", "DOWN", "LEFT", "RIGHT", "WAIT"]
    assert env.action_space.contains(environment.Action.WAIT)
    assert env.observation_space.contains(observation)
    assert env.observation_space.shape == (2,)
    assert env.observation_space.dtype == np.dtype(np.int64)


@pytest.mark.parametrize(
    ("action", "expected"),
    ((environment.Action.UP, (0, 1)), (environment.Action.DOWN, (2, 1)), (environment.Action.LEFT, (1, 0)), (environment.Action.RIGHT, (1, 2))),
)
def test_cardinal_actions_follow_row_column_convention(action: environment.Action, expected: tuple[int, int]) -> None:
    env = environment.SearchRescueEnvironment(
        environment.EnvironmentConfig(rows=3, columns=4, start=(1, 1), goals={"victim-a": (0, 2)})
    )
    observation, reward, terminated, truncated, info = env.step(action)

    assert np.array_equal(observation, np.array(expected, dtype=np.int64))
    assert reward == 0.0
    assert not terminated
    assert not truncated
    assert not info["blocked_by_structure"]
    assert info["action"] == action.name


def test_blocked_transition_preserves_position() -> None:
    observation, reward, terminated, truncated, info = make_environment().step(environment.Action.DOWN)

    assert np.array_equal(observation, np.array((1, 1), dtype=np.int64))
    assert reward == 0.0
    assert not terminated
    assert not truncated
    assert info["blocked_by_structure"]
    assert not info["moved"]


def test_wait_preserves_position() -> None:
    observation, reward, terminated, truncated, info = make_environment().step(environment.Action.WAIT)

    assert np.array_equal(observation, np.array((1, 1), dtype=np.int64))
    assert reward == 0.0
    assert not terminated
    assert not truncated
    assert not info["moved"]


def test_entering_goal_terminates_episode() -> None:
    env = make_environment()
    env.step(environment.Action.UP)
    observation, reward, terminated, truncated, info = env.step(environment.Action.RIGHT)

    assert np.array_equal(observation, np.array((0, 2), dtype=np.int64))
    assert reward == 0.0
    assert terminated
    assert not truncated
    assert info["reached_goal"] == "victim-a"
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
    observation, reward, terminated, truncated, info = env.step(environment.Action.RIGHT)

    assert np.array_equal(observation, np.array((1, 3), dtype=np.int64))
    assert reward == 0.0
    assert not terminated
    assert not truncated
    assert info["moved"]
    assert info["destination_risk"] == 1.0


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
