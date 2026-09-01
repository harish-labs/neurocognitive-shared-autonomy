"""Deterministic 2D Search & Rescue environment mechanics and canonical risk map."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


Coordinate = tuple[int, int]


class EnvironmentError(ValueError):
    """Raised when a SAR environment configuration or operation is invalid."""


class Action(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    WAIT = "WAIT"


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


@dataclass(frozen=True)
class TransitionResult:
    previous_state: EnvironmentState
    state: EnvironmentState
    action: Action
    moved: bool
    blocked_by_structure: bool
    destination_risk: float


class SearchRescueEnvironment:
    """Static world mechanics, deliberately independent of planner and safety policy."""

    def __init__(self, config: EnvironmentConfig) -> None:
        self.config = _validate_config(config)
        self._last_seed: int | None = None
        self._state = self._initial_state()

    @property
    def state(self) -> EnvironmentState:
        return self._state

    @property
    def last_seed(self) -> int | None:
        return self._last_seed

    def reset(self, *, seed: int | None = None) -> EnvironmentState:
        """Restore the static configured start state; the seed is retained for reproducibility."""
        if seed is not None and not isinstance(seed, int):
            raise EnvironmentError("Reset seed must be an integer or None.")
        self._last_seed = seed
        self._state = self._initial_state()
        return self._state

    def step(self, action: Action | str) -> TransitionResult:
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
        return TransitionResult(
            previous_state=previous,
            state=self._state,
            action=normalized_action,
            moved=destination != previous.position,
            blocked_by_structure=structural_block,
            destination_risk=self.risk_at(destination),
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


def _validate_action(action: Action | str) -> Action:
    try:
        return action if isinstance(action, Action) else Action(str(action))
    except ValueError as exc:
        raise EnvironmentError("Action must be one of UP, DOWN, LEFT, RIGHT, or WAIT.") from exc


def _is_coordinate(value: object) -> bool:
    return isinstance(value, tuple) and len(value) == 2 and all(isinstance(item, int) for item in value)


def _in_bounds(rows: int, columns: int, coordinate: Coordinate) -> bool:
    return 0 <= coordinate[0] < rows and 0 <= coordinate[1] < columns


def _require_coordinate(value: object, label: str) -> None:
    if not _is_coordinate(value):
        raise EnvironmentError(f"{label} must use the (row, column) integer coordinate convention.")
