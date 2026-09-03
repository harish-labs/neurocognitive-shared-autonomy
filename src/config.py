"""Validated operational configuration for future system composition.

Approved scientific policy remains owned by its existing domain modules and is
deliberately absent from this runtime-only boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from src.eeg.loader import EEGBCI_SUBJECT_MAX, EEGBCI_SUBJECT_MIN, APPROVED_RUNS


PROJECT_NAME = "neurocognitive-shared-autonomy"


class ConfigurationError(ValueError):
    """Raised when runtime composition configuration is invalid or unsupported."""


@dataclass(frozen=True)
class ProjectRuntimeConfig:
    name: str


@dataclass(frozen=True)
class DatasetRuntimeConfig:
    cache_path: Path
    subjects: tuple[int, ...]
    runs: tuple[int, ...]
    preload: bool


@dataclass(frozen=True)
class ArtifactRuntimeConfig:
    split_manifest: Path | None
    decoder: Path | None
    calibrator: Path | None


@dataclass(frozen=True)
class ReplayRuntimeConfig:
    source: Path | None


@dataclass(frozen=True)
class RuntimeSettings:
    device: str
    adaptation_enabled: bool
    seed: int


@dataclass(frozen=True)
class EnvironmentRuntimeConfig:
    map_path: Path | None


@dataclass(frozen=True)
class OutputRuntimeConfig:
    directory: Path


@dataclass(frozen=True)
class RuntimeConfiguration:
    """Immutable, operational-only configuration loaded from one YAML file."""

    project: ProjectRuntimeConfig
    dataset: DatasetRuntimeConfig
    artifacts: ArtifactRuntimeConfig
    replay: ReplayRuntimeConfig
    runtime: RuntimeSettings
    environment: EnvironmentRuntimeConfig
    output: OutputRuntimeConfig

    def to_dict(self) -> dict[str, object]:
        """Return a deterministic, serializable operational configuration snapshot."""
        return {
            "project": {"name": self.project.name},
            "dataset": {
                "cache_path": str(self.dataset.cache_path),
                "subjects": list(self.dataset.subjects),
                "runs": list(self.dataset.runs),
                "preload": self.dataset.preload,
            },
            "artifacts": {
                "split_manifest": _path_value(self.artifacts.split_manifest),
                "decoder": _path_value(self.artifacts.decoder),
                "calibrator": _path_value(self.artifacts.calibrator),
            },
            "replay": {"source": _path_value(self.replay.source)},
            "runtime": {
                "device": self.runtime.device,
                "adaptation_enabled": self.runtime.adaptation_enabled,
                "seed": self.runtime.seed,
            },
            "environment": {"map": _path_value(self.environment.map_path)},
            "output": {"directory": str(self.output.directory)},
        }


_TOP_LEVEL_SECTIONS = frozenset(
    {"project", "dataset", "artifacts", "replay", "runtime", "environment", "output"}
)
_SECTION_FIELDS = {
    "project": frozenset({"name"}),
    "dataset": frozenset({"cache_path", "subjects", "runs", "preload"}),
    "artifacts": frozenset({"split_manifest", "decoder", "calibrator"}),
    "replay": frozenset({"source"}),
    "runtime": frozenset({"device", "adaptation_enabled", "seed"}),
    "environment": frozenset({"map"}),
    "output": frozenset({"directory"}),
}
_LOCKED_POLICY_SECTIONS = frozenset(
    {
        "adaptation",
        "bayesian",
        "calibration",
        "csp_lda",
        "eeg",
        "eegnet",
        "planner",
        "preprocessing",
        "safety",
        "shared_autonomy",
    }
)


def load_runtime_config(config_path: str | Path = "config.yaml") -> RuntimeConfiguration:
    """Load one D-072 operational configuration using PyYAML safe loading."""
    path = Path(config_path).expanduser().resolve()
    try:
        with path.open("r", encoding="utf-8") as stream:
            payload = yaml.safe_load(stream)
    except OSError as exc:
        raise ConfigurationError(f"Unable to read configuration file {path}.") from exc
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"Configuration file {path} is not valid YAML.") from exc

    root = _mapping(payload, "root configuration")
    _validate_keys(root, _TOP_LEVEL_SECTIONS, "root configuration")
    parent = path.parent

    project = _section(root, "project")
    dataset = _section(root, "dataset")
    artifacts = _section(root, "artifacts")
    replay = _section(root, "replay")
    runtime = _section(root, "runtime")
    environment = _section(root, "environment")
    output = _section(root, "output")

    name = _non_empty_string(project["name"], "project.name")
    if name != PROJECT_NAME:
        raise ConfigurationError(f"project.name must be exactly {PROJECT_NAME!r}.")

    return RuntimeConfiguration(
        project=ProjectRuntimeConfig(name=name),
        dataset=DatasetRuntimeConfig(
            cache_path=_required_path(dataset["cache_path"], parent, "dataset.cache_path"),
            subjects=_identifiers(
                dataset["subjects"],
                "dataset.subjects",
                minimum=EEGBCI_SUBJECT_MIN,
                maximum=EEGBCI_SUBJECT_MAX,
            ),
            runs=_run_ids(dataset["runs"]),
            preload=_boolean(dataset["preload"], "dataset.preload"),
        ),
        artifacts=ArtifactRuntimeConfig(
            split_manifest=_optional_path(artifacts["split_manifest"], parent, "artifacts.split_manifest"),
            decoder=_optional_path(artifacts["decoder"], parent, "artifacts.decoder"),
            calibrator=_optional_path(artifacts["calibrator"], parent, "artifacts.calibrator"),
        ),
        replay=ReplayRuntimeConfig(source=_optional_path(replay["source"], parent, "replay.source")),
        runtime=RuntimeSettings(
            device=_non_empty_string(runtime["device"], "runtime.device"),
            adaptation_enabled=_boolean(runtime["adaptation_enabled"], "runtime.adaptation_enabled"),
            seed=_non_negative_integer(runtime["seed"], "runtime.seed"),
        ),
        environment=EnvironmentRuntimeConfig(
            map_path=_optional_path(environment["map"], parent, "environment.map")
        ),
        output=OutputRuntimeConfig(directory=_required_path(output["directory"], parent, "output.directory")),
    )


def _section(root: Mapping[str, object], name: str) -> Mapping[str, object]:
    if name not in root:
        raise ConfigurationError(f"root configuration is missing required section {name!r}.")
    section = _mapping(root[name], name)
    _validate_keys(section, _SECTION_FIELDS[name], name)
    missing = _SECTION_FIELDS[name] - set(section)
    if missing:
        raise ConfigurationError(f"{name} is missing required key(s): {', '.join(sorted(missing))}.")
    return section


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ConfigurationError(f"{label} must be a mapping.")
    if not all(isinstance(key, str) for key in value):
        raise ConfigurationError(f"{label} keys must be strings.")
    return value


def _validate_keys(mapping: Mapping[str, object], allowed: frozenset[str], label: str) -> None:
    for key in mapping:
        if key in _LOCKED_POLICY_SECTIONS:
            raise ConfigurationError(
                f"{key!r} is governed scientific policy and is not runtime configurable."
            )
    unknown = set(mapping) - allowed
    if unknown:
        raise ConfigurationError(f"{label} contains unsupported key(s): {', '.join(sorted(unknown))}.")


def _identifiers(value: object, label: str, *, minimum: int, maximum: int) -> tuple[int, ...]:
    if not isinstance(value, list) or not value:
        raise ConfigurationError(f"{label} must be a non-empty list of integers.")
    if any(isinstance(item, bool) or not isinstance(item, int) for item in value):
        raise ConfigurationError(f"{label} must contain integers, not booleans or other values.")
    if len(set(value)) != len(value):
        raise ConfigurationError(f"{label} must not contain duplicate values.")
    if any(not minimum <= item <= maximum for item in value):
        raise ConfigurationError(f"{label} values must be between {minimum} and {maximum}.")
    return tuple(value)


def _run_ids(value: object) -> tuple[int, ...]:
    runs = _identifiers(value, "dataset.runs", minimum=min(APPROVED_RUNS), maximum=max(APPROVED_RUNS))
    invalid = set(runs) - set(APPROVED_RUNS)
    if invalid:
        raise ConfigurationError("dataset.runs must use only the approved runs: 4, 8, 12.")
    return runs


def _boolean(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise ConfigurationError(f"{label} must be a boolean.")
    return value


def _non_negative_integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ConfigurationError(f"{label} must be a non-negative integer.")
    return value


def _non_empty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{label} must be a non-empty string.")
    return value


def _required_path(value: object, parent: Path, label: str) -> Path:
    if value is None:
        raise ConfigurationError(f"{label} must not be null.")
    return _path(value, parent, label)


def _optional_path(value: object, parent: Path, label: str) -> Path | None:
    return None if value is None else _path(value, parent, label)


def _path(value: object, parent: Path, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ConfigurationError(f"{label} must be a non-empty path string or null where optional.")
    path = Path(value).expanduser()
    return (path if path.is_absolute() else parent / path).resolve()


def _path_value(path: Path | None) -> str | None:
    return None if path is None else str(path)
