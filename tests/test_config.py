from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import sys

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import ConfigurationError, load_runtime_config


ROOT = Path(__file__).resolve().parents[1]


def canonical_payload() -> dict[str, object]:
    return {
        "project": {"name": "neurocognitive-shared-autonomy"},
        "dataset": {"cache_path": "data/raw", "subjects": [1], "runs": [4, 8, 12], "preload": True},
        "artifacts": {"split_manifest": None, "decoder": None, "calibrator": None},
        "replay": {"source": None},
        "runtime": {"device": "cpu", "adaptation_enabled": False, "seed": 42},
        "environment": {"map": None},
        "output": {"directory": "results"},
    }


def write_config(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "nested" / "runtime.yaml"
    path.parent.mkdir(exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def test_root_config_loads_as_typed_immutable_operational_configuration() -> None:
    config = load_runtime_config(ROOT / "config.yaml")

    assert config.project.name == "neurocognitive-shared-autonomy"
    assert config.dataset.subjects == (1,)
    assert config.dataset.runs == (4, 8, 12)
    assert config.runtime.device == "cpu"
    assert config.artifacts.decoder is None
    with pytest.raises(FrozenInstanceError):
        config.runtime.seed = 7  # type: ignore[misc]


def test_serialization_is_deterministic_operational_only_and_json_serializable() -> None:
    config = load_runtime_config(ROOT / "config.yaml")

    first = config.to_dict()
    assert first == config.to_dict()
    json.dumps(first, sort_keys=True)
    assert first["dataset"]["subjects"] == [1]  # type: ignore[index]
    serialized = json.dumps(first, sort_keys=True)
    for forbidden in ("bandpass", "sampling_frequency", "commitment_threshold", "risk_lambda", "warm_up"):
        assert forbidden not in serialized


@pytest.mark.parametrize("section, value", [("runtme", {"device": "cpu"}), ("runtime", {"devcie": "cpu"})])
def test_unknown_top_level_and_nested_keys_fail_closed(tmp_path: Path, section: str, value: object) -> None:
    payload = canonical_payload()
    payload[section] = value

    with pytest.raises(ConfigurationError, match="unsupported key"):
        load_runtime_config(write_config(tmp_path, payload))


@pytest.mark.parametrize(
    "section, value",
    [
        ("preprocessing", {"bandpass": [7, 30]}),
        ("eeg", {"sampling_frequency": 160}),
        ("bayesian", {"commitment_threshold": 0.9}),
        ("shared_autonomy", {"thresholds": 0.75}),
        ("planner", {"risk_lambda": 2.0}),
        ("adaptation", {"warm_up": 3}),
    ],
)
def test_locked_scientific_policy_sections_are_rejected_explicitly(tmp_path: Path, section: str, value: object) -> None:
    payload = canonical_payload()
    payload[section] = value

    with pytest.raises(ConfigurationError, match="governed scientific policy"):
        load_runtime_config(write_config(tmp_path, payload))


@pytest.mark.parametrize("subjects", ([], [1, 1], [0], [110], [True], ["1"]))
def test_subject_validation_rejects_invalid_values(tmp_path: Path, subjects: object) -> None:
    payload = canonical_payload()
    payload["dataset"]["subjects"] = subjects  # type: ignore[index]

    with pytest.raises(ConfigurationError):
        load_runtime_config(write_config(tmp_path, payload))


@pytest.mark.parametrize("runs", ([], [4, 4], [5], [True], ["4"]))
def test_run_validation_rejects_invalid_values(tmp_path: Path, runs: object) -> None:
    payload = canonical_payload()
    payload["dataset"]["runs"] = runs  # type: ignore[index]

    with pytest.raises(ConfigurationError):
        load_runtime_config(write_config(tmp_path, payload))


@pytest.mark.parametrize("value", ("true", "false", 0, 1))
def test_boolean_fields_are_strict(tmp_path: Path, value: object) -> None:
    payload = canonical_payload()
    payload["runtime"]["adaptation_enabled"] = value  # type: ignore[index]

    with pytest.raises(ConfigurationError, match="boolean"):
        load_runtime_config(write_config(tmp_path, payload))


@pytest.mark.parametrize("seed", (True, -1, 1.5, "42"))
def test_seed_must_be_a_non_negative_non_boolean_integer(tmp_path: Path, seed: object) -> None:
    payload = canonical_payload()
    payload["runtime"]["seed"] = seed  # type: ignore[index]

    with pytest.raises(ConfigurationError, match="non-negative integer"):
        load_runtime_config(write_config(tmp_path, payload))


def test_project_identity_relative_paths_and_optional_paths(tmp_path: Path) -> None:
    payload = canonical_payload()
    payload["dataset"]["cache_path"] = "cache"  # type: ignore[index]
    payload["artifacts"]["decoder"] = "artifacts/decoder.bin"  # type: ignore[index]
    payload["replay"]["source"] = "replay/epochs.fif"  # type: ignore[index]
    payload["environment"]["map"] = "maps/demo.yaml"  # type: ignore[index]
    config_path = write_config(tmp_path, payload)
    config = load_runtime_config(config_path)

    assert config.dataset.cache_path == (config_path.parent / "cache").resolve()
    assert config.artifacts.decoder == (config_path.parent / "artifacts/decoder.bin").resolve()
    assert config.replay.source == (config_path.parent / "replay/epochs.fif").resolve()
    assert config.environment.map_path == (config_path.parent / "maps/demo.yaml").resolve()
    assert config.artifacts.split_manifest is None
    assert config.artifacts.calibrator is None

    payload["project"]["name"] = "wrong-project"  # type: ignore[index]
    with pytest.raises(ConfigurationError, match="project.name"):
        load_runtime_config(write_config(tmp_path, payload))
