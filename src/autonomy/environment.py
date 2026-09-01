"""Deterministic 2D Search & Rescue environment mechanics and canonical risk map."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Mapping

import gymnasium as gym
import numpy as np
from gymnasium import spaces

Coordinate = tuple[int, int]


class EnvironmentError(ValueError):
    """Raised when a SAR environment configuration or operation is invalid."""


class Action(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    WAIT = 4


class RiskLevel(float, Enum):
    FREE = 0.00
    LOW = 0.25
    MODERATE = 0.50
    HIGH = 0.75
    PROHIBITED = 1.00


ACTION_DELTAS: dict[Action, Coordinate] = {
    Action.UP: (-1, 0),
    Action.DOWN: (1, 0),
    Action.LEFT: (0, -1),
    Action.RIGHT: (0, 1),
    Action.WAIT: (0, 0),
}
CANONICAL_RISK_VALUES = frozenset(float(level.value) for level in RiskLevel)


@dataclass(frozen=True)
class EnvironmentConfig:
    rows: int
    columns: int
    start: Coordinate
    goals: Mapping[str, Coordinate]
    blocked_cells: frozenset[Coordinate] = field(default_factory=frozenset)
    risk_map: Mapping[Coordinate, float] = field(default_factory=dict)


@dataclass(frozen=True)
class EnvironmentState:
    position: Coordinate
    terminated: bool
    reached_goal: str | None


class SearchRescueEnvironment(gym.Env[np.ndarray, int]):
    """Static world mechanics, deliberately independent of planner and safety policy."""

    metadata = {"render_modes": []}

    def __init__(self, config: EnvironmentConfig) -> None:
        super().__init__()
        self.config = _validate_config(config)
        self._last_seed: int | None = None
        self._state = self._initial_state()
        self.action_space = spaces.Discrete(len(Action))
        self.observation_space = spaces.Box(
            low=np.array((0, 0), dtype=np.int64),
            high=np.array((config.rows - 1, config.columns - 1), dtype=np.int64),
            dtype=np.int64,
        )

    @property
    def state(self) -> EnvironmentState:
        return self._state

    @property
    def last_seed(self) -> int | None:
        return self._last_seed

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, object] | None = None,
    ) -> tuple[np.ndarray, dict[str, object]]:
        """Restore the static start state using Gymnasium reset conventions."""
        super().reset(seed=seed)
        self._last_seed = seed
        self._state = self._initial_state()
        return self._observation(), self._info()

    def step(self, action: int | Action | str) -> tuple[np.ndarray, float, bool, bool, dict[str, object]]:
        """Apply raw grid mechanics; planners and safety control remain external."""
        normalized_action = _validate_action(action)
        previous = self._state
        if previous.terminated:
            raise EnvironmentError("Cannot transition a terminated environment; call reset first.")

        delta = ACTION_DELTAS[normalized_action]
        candidate = (previous.position[0] + delta[0], previous.position[1] + delta[1])
        structural_block = not self.in_bounds(candidate) or candidate in self.config.blocked_cells
        destination = previous.position if structural_block else candidate
        reached_goal = self._goal_at(destination)
        self._state = EnvironmentState(
            position=destination,
            terminated=reached_goal is not None,
            reached_goal=reached_goal,
        )
        return (
            self._observation(),
            0.0,
            self._state.terminated,
            False,
            self._info(
                action=normalized_action,
                previous_position=previous.position,
                moved=destination != previous.position,
                blocked_by_structure=structural_block,
            ),
        )

    def in_bounds(self, coordinate: Coordinate) -> bool:
        return 0 <= coordinate[0] < self.config.rows and 0 <= coordinate[1] < self.config.columns

    def risk_at(self, coordinate: Coordinate) -> float:
        self._require_in_bounds(coordinate)
        return float(self.config.risk_map.get(coordinate, RiskLevel.FREE.value))

    def is_blocked(self, coordinate: Coordinate) -> bool:
        self._require_in_bounds(coordinate)
        return coordinate in self.config.blocked_cells

    def is_prohibited(self, coordinate: Coordinate) -> bool:
        """Expose D-064 map semantics without implementing future safety enforcement."""
        return self.risk_at(coordinate) >= RiskLevel.PROHIBITED.value

    def _initial_state(self) -> EnvironmentState:
        return EnvironmentState(position=self.config.start, terminated=False, reached_goal=None)

    def _goal_at(self, coordinate: Coordinate) -> str | None:
        for name, position in self.config.goals.items():
            if position == coordinate:
                return name
        return None

    def _observation(self) -> np.ndarray:
        return np.asarray(self._state.position, dtype=np.int64)

    def _info(
        self,
        *,
        action: Action | None = None,
        previous_position: Coordinate | None = None,
        moved: bool | None = None,
        blocked_by_structure: bool | None = None,
    ) -> dict[str, object]:
        return {
            "position": self._state.position,
            "reached_goal": self._state.reached_goal,
            "destination_risk": self.risk_at(self._state.position),
            "action": action.name if action is not None else None,
            "previous_position": previous_position,
            "moved": moved,
            "blocked_by_structure": blocked_by_structure,
        }

    def _require_in_bounds(self, coordinate: Coordinate) -> None:
        if not _is_coordinate(coordinate) or not self.in_bounds(coordinate):
            raise EnvironmentError(f"Coordinate {coordinate!r} is outside the configured grid.")


def _validate_config(config: EnvironmentConfig) -> EnvironmentConfig:
    if not isinstance(config, EnvironmentConfig):
        raise EnvironmentError("Environment requires an EnvironmentConfig.")
    if not isinstance(config.rows, int) or not isinstance(config.columns, int) or config.rows <= 0 or config.columns <= 0:
        raise EnvironmentError("Grid rows and columns must be positive integers.")
    _require_coordinate(config.start, "Start")
    if not config.goals:
        raise EnvironmentError("At least one named goal is required.")
    for label, coordinate in [("Start", config.start), *[(f"Goal {name!r}", value) for name, value in config.goals.items()]]:
        _require_coordinate(coordinate, label)
        if not _in_bounds(config.rows, config.columns, coordinate):
            raise EnvironmentError(f"{label} is outside the configured grid.")
    for coordinate in config.blocked_cells:
        _require_coordinate(coordinate, "Blocked cell")
        if not _in_bounds(config.rows, config.columns, coordinate):
            raise EnvironmentError("Blocked cell is outside the configured grid.")
    if config.start in config.blocked_cells:
        raise EnvironmentError("Start cannot be a blocked cell.")
    for coordinate, risk in config.risk_map.items():
        _require_coordinate(coordinate, "Risk-map coordinate")
        if not _in_bounds(config.rows, config.columns, coordinate):
            raise EnvironmentError("Risk-map coordinate is outside the configured grid.")
        try:
            normalized_risk = float(risk)
        except (TypeError, ValueError) as exc:
            raise EnvironmentError("Risk values must be numeric canonical risk values.") from exc
        if normalized_risk not in CANONICAL_RISK_VALUES:
            raise EnvironmentError("Risk values must be exactly one of 0.00, 0.25, 0.50, 0.75, or 1.00.")
    return config


def _validate_action(action: int | Action | str) -> Action:
    try:
        if isinstance(action, Action):
            return action
        if isinstance(action, str):
            return Action[action.upper()]
        if isinstance(action, (bool, np.bool_)):
            raise ValueError
        return Action(int(action))
    except (KeyError, TypeError, ValueError) as exc:
        raise EnvironmentError("Action must be one of UP, DOWN, LEFT, RIGHT, or WAIT.") from exc


def _is_coordinate(value: object) -> bool:
    return isinstance(value, tuple) and len(value) == 2 and all(isinstance(item, int) for item in value)


def _in_bounds(rows: int, columns: int, coordinate: Coordinate) -> bool:
    return 0 <= coordinate[0] < rows and 0 <= coordinate[1] < columns


def _require_coordinate(value: object, label: str) -> None:
    if not _is_coordinate(value):
        raise EnvironmentError(f"{label} must use the (row, column) integer coordinate convention.")
