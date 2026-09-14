"""Freeze the D-084 final execution contract before protected outcome access."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from src.evaluation.cohort import split_manifest_from_mapping
from src.evaluation.episodes import load_episode_manifest, sequential_participation_manifest_from_mapping
from src.evaluation.final_contract import (
    ArtifactRecord,
    build_final_manifest,
    freeze_final_manifest,
    sha256_file,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qc", default="results/m7/manifest/m7-d082-qc-eligibility-v1.json")
    parser.add_argument("--split", default="results/m7/manifest/m7-d082-cross-subject-v1.json")
    parser.add_argument("--episodes", default="results/m7/manifest/m7-d081-fixed-intent-episodes-v1.json")
    parser.add_argument("--participation", default="results/m7/manifest/m7-d083-final-sequential-participation-v1.json")
    parser.add_argument("--artifacts", default="results/m7/manifest/m7-artifacts-v1.json")
    parser.add_argument("--output", default="results/m7/manifest/m7-final-execution-v5-d084.json")
    parser.add_argument("--governance-sha", required=True)
    parser.add_argument("--software-sha")
    arguments = parser.parse_args()
    software_sha = arguments.software_sha or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, encoding="utf-8"
    ).strip()
    qc_path, split_path, episode_path, participation_path, artifact_path = (
        Path(arguments.qc).resolve(), Path(arguments.split).resolve(), Path(arguments.episodes).resolve(),
        Path(arguments.participation).resolve(), Path(arguments.artifacts).resolve(),
    )
    split = split_manifest_from_mapping(json.loads(split_path.read_text(encoding="utf-8")))
    episodes = load_episode_manifest(episode_path)
    participation = sequential_participation_manifest_from_mapping(json.loads(participation_path.read_text(encoding="utf-8")))
    artifact_payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    records = tuple(ArtifactRecord(**item) for item in artifact_payload["artifact_records"])
    manifest = build_final_manifest(
        software_sha=software_sha, governance_sha=arguments.governance_sha,
        qc_manifest_path=str(qc_path), qc_manifest_sha256=sha256_file(qc_path),
        split_manifest_path=str(split_path), split_manifest_sha256=sha256_file(split_path), split_manifest=split,
        episode_manifest_path=str(episode_path), episode_manifest_sha256=sha256_file(episode_path), episode_manifest=episodes,
        participation_manifest_path=str(participation_path), participation_manifest_sha256=sha256_file(participation_path),
        participation_manifest=participation, artifacts=records,
    )
    output = Path(arguments.output).resolve()
    manifest_hash = freeze_final_manifest(manifest, output)
    print(json.dumps({"path": str(output), "sha256": manifest_hash, "software_sha": software_sha}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
