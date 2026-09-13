"""D-081 fixed-intent EEG episode construction and immutable provenance."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


D081_POLICY_ID = "D-081"
D081_EPISODE_MANIFEST_VERSION = "m7-d081-fixed-intent-episodes-v1"
D081_EPISODE_BLOCK_SIZE = 5
D081_GROUPING_KEY = ("subject_id", "run_id", "semantic_label")
D081_ORDERING_RULE = "event_sample_then_canonical_trial_index_then_identity"
D081_E9_ORDERING_RULE = "run_id_then_first_event_sample_then_episode_id"
REQUIRED_SOURCE_COLUMNS = (
    "subject_id",
    "run_id",
    "source_file",
    "event_code",
    "semantic_label",
    "event_sample",
    "trial_index",
)
ALLOWED_CLASSES = ("left", "right")
CONDITION_SOURCE_POSITIONS: Mapping[str, tuple[int, ...]] = {
    "A": (1,),
    "B": (1,),
    "C": (1, 2, 3, 4, 5),
    "D": (1, 2, 3, 4, 5),
}


class EpisodeConstructionError(ValueError):
    """Raised when D-081 construction or provenance validation fails closed."""


@dataclass(frozen=True)
class SourceTrial:
    canonical_trial_id: str
    subject_id: int
    run_id: int
    intended_class: str
    event_code: str
    event_sample: int
    canonical_trial_index: int
    source_file: str


@dataclass(frozen=True)
class FixedIntentEpisode:
    episode_id: str
    subject_id: int
    run_id: int
    intended_class: str
    episode_block_index: int
    source_trials: tuple[SourceTrial, ...]

    @property
    def source_trial_ids(self) -> tuple[str, ...]:
        return tuple(item.canonical_trial_id for item in self.source_trials)

    @property
    def source_event_samples(self) -> tuple[int, ...]:
        return tuple(item.event_sample for item in self.source_trials)

    @property
    def source_trial_indices(self) -> tuple[int, ...]:
        return tuple(item.canonical_trial_index for item in self.source_trials)


@dataclass(frozen=True)
class TailExclusion:
    subject_id: int
    run_id: int
    intended_class: str
    excluded_count: int
    source_trials: tuple[SourceTrial, ...]
    reason: str = "incomplete_same_class_tail_fewer_than_five"
    eligible_for_single_trial_e1_e2: bool = True


@dataclass(frozen=True)
class EpisodeManifest:
    manifest_version: str
    policy_ids: tuple[str, ...]
    grouping_key: tuple[str, ...]
    ordering_rule: str
    block_size: int
    overlap: bool
    source_trial_reuse: bool
    incomplete_tail_policy: str
    ab_first_observation_rule: str
    cd_source_order_rule: str
    e9_ordering_rule: str
    source_table_sha256: str
    source_trial_count: int
    sequential_source_trial_count: int
    tail_source_trial_count: int
    episode_count: int
    episodes: tuple[FixedIntentEpisode, ...]
    tail_exclusions: tuple[TailExclusion, ...]
    per_subject_episode_counts: Mapping[str, int]
    per_run_episode_counts: Mapping[str, int]
    per_class_episode_counts: Mapping[str, int]
    protected_outcomes_computed: bool
    scientific_interpretation: str


def construct_episode_manifest(source_metadata: pd.DataFrame) -> EpisodeManifest:
    """Construct D-081 episodes from provenance/labels only; no prediction API is accepted."""

    metadata = _validated_source_metadata(source_metadata)
    ordered_source = tuple(_source_trial(row) for _, row in metadata.iterrows())
    source_hash = _mapping_sha256({"source_trials": [asdict(item) for item in ordered_source]})
    episodes: list[FixedIntentEpisode] = []
    tails: list[TailExclusion] = []

    for (subject_id, run_id, intended_class), group in metadata.groupby(
        list(D081_GROUPING_KEY), sort=False, observed=True
    ):
        trials = tuple(_source_trial(row) for _, row in group.iterrows())
        complete_count = len(trials) // D081_EPISODE_BLOCK_SIZE
        for block_index in range(complete_count):
            start = block_index * D081_EPISODE_BLOCK_SIZE
            block = trials[start : start + D081_EPISODE_BLOCK_SIZE]
            episodes.append(
                FixedIntentEpisode(
                    episode_id=_episode_id(int(subject_id), int(run_id), str(intended_class), block_index, block),
                    subject_id=int(subject_id),
                    run_id=int(run_id),
                    intended_class=str(intended_class),
                    episode_block_index=block_index,
                    source_trials=block,
                )
            )
        tail = trials[complete_count * D081_EPISODE_BLOCK_SIZE :]
        if tail:
            tails.append(
                TailExclusion(
                    subject_id=int(subject_id),
                    run_id=int(run_id),
                    intended_class=str(intended_class),
                    excluded_count=len(tail),
                    source_trials=tail,
                )
            )

    manifest = EpisodeManifest(
        manifest_version=D081_EPISODE_MANIFEST_VERSION,
        policy_ids=("D-051", "D-052", "D-053", "D-054", "D-074", "D-077", "D-078", "D-080", "D-081", "D-082"),
        grouping_key=D081_GROUPING_KEY,
        ordering_rule=D081_ORDERING_RULE,
        block_size=D081_EPISODE_BLOCK_SIZE,
        overlap=False,
        source_trial_reuse=False,
        incomplete_tail_policy="exclude_record_and_retain_for_e1_e2",
        ab_first_observation_rule="A_and_B_use_source_position_1",
        cd_source_order_rule="C_and_D_receive_positions_1_through_5_in_frozen_order",
        e9_ordering_rule=D081_E9_ORDERING_RULE,
        source_table_sha256=source_hash,
        source_trial_count=len(ordered_source),
        sequential_source_trial_count=sum(len(item.source_trials) for item in episodes),
        tail_source_trial_count=sum(item.excluded_count for item in tails),
        episode_count=len(episodes),
        episodes=tuple(episodes),
        tail_exclusions=tuple(tails),
        per_subject_episode_counts=_counts(episodes, lambda item: str(item.subject_id)),
        per_run_episode_counts=_counts(episodes, lambda item: str(item.run_id)),
        per_class_episode_counts=_counts(episodes, lambda item: item.intended_class),
        protected_outcomes_computed=False,
        scientific_interpretation=(
            "deterministic offline repeated-trial construction for one fixed intended binary choice; "
            "not a natural continuous EEG session or live/online BCI accumulation"
        ),
    )
    validate_episode_manifest(manifest)
    return manifest


def validate_episode_manifest(manifest: EpisodeManifest) -> None:
    if not isinstance(manifest, EpisodeManifest):
        raise EpisodeConstructionError("D-081 validation requires EpisodeManifest.")
    if manifest.manifest_version != D081_EPISODE_MANIFEST_VERSION or D081_POLICY_ID not in manifest.policy_ids:
        raise EpisodeConstructionError("Episode manifest version/policy does not match D-081.")
    if manifest.grouping_key != D081_GROUPING_KEY or manifest.ordering_rule != D081_ORDERING_RULE:
        raise EpisodeConstructionError("D-081 grouping or ordering rule changed.")
    if manifest.block_size != 5 or manifest.overlap or manifest.source_trial_reuse:
        raise EpisodeConstructionError("D-081 requires non-overlapping five-trial blocks without reuse.")
    if manifest.protected_outcomes_computed:
        raise EpisodeConstructionError("Episode-manifest construction must not compute protected outcomes.")
    declared_source_ids = [
        trial.canonical_trial_id for episode in manifest.episodes for trial in episode.source_trials
    ] + [trial.canonical_trial_id for tail in manifest.tail_exclusions for trial in tail.source_trials]
    if len(set(declared_source_ids)) != len(declared_source_ids):
        raise EpisodeConstructionError("A source trial was reused across episodes or tails.")
    episode_ids: list[str] = []
    used_ids: list[str] = []
    tail_ids: list[str] = []
    for episode in manifest.episodes:
        episode_ids.append(episode.episode_id)
        if len(episode.source_trials) != D081_EPISODE_BLOCK_SIZE:
            raise EpisodeConstructionError("Every D-081 sequential episode must contain exactly five source trials.")
        if {item.subject_id for item in episode.source_trials} != {episode.subject_id}:
            raise EpisodeConstructionError("A D-081 episode cannot mix subjects.")
        if {item.run_id for item in episode.source_trials} != {episode.run_id}:
            raise EpisodeConstructionError("A D-081 episode cannot mix runs.")
        if {item.intended_class for item in episode.source_trials} != {episode.intended_class}:
            raise EpisodeConstructionError("A D-081 episode cannot mix intended classes.")
        order = tuple((item.event_sample, item.canonical_trial_index, item.canonical_trial_id) for item in episode.source_trials)
        if order != tuple(sorted(order)):
            raise EpisodeConstructionError("Episode source trials are not in canonical acquisition order.")
        expected_id = _episode_id(
            episode.subject_id,
            episode.run_id,
            episode.intended_class,
            episode.episode_block_index,
            episode.source_trials,
        )
        if episode.episode_id != expected_id:
            raise EpisodeConstructionError("Episode ID is unstable or inconsistent with source provenance.")
        used_ids.extend(episode.source_trial_ids)
    for tail in manifest.tail_exclusions:
        if not 0 < tail.excluded_count < D081_EPISODE_BLOCK_SIZE or tail.excluded_count != len(tail.source_trials):
            raise EpisodeConstructionError("Tail exclusions must contain one to four source trials.")
        if not tail.eligible_for_single_trial_e1_e2:
            raise EpisodeConstructionError("D-081 tail trials must remain eligible for valid E1/E2 analyses.")
        if {item.subject_id for item in tail.source_trials} != {tail.subject_id}:
            raise EpisodeConstructionError("A tail exclusion cannot mix subjects.")
        if {item.run_id for item in tail.source_trials} != {tail.run_id}:
            raise EpisodeConstructionError("A tail exclusion cannot mix runs.")
        if {item.intended_class for item in tail.source_trials} != {tail.intended_class}:
            raise EpisodeConstructionError("A tail exclusion cannot mix intended classes.")
        tail_ids.extend(item.canonical_trial_id for item in tail.source_trials)
    if len(set(episode_ids)) != len(episode_ids):
        raise EpisodeConstructionError("Episode IDs must be unique.")
    accounted = used_ids + tail_ids
    if len(set(accounted)) != len(accounted):
        raise EpisodeConstructionError("A source trial was reused across episodes or tails.")
    if len(accounted) != manifest.source_trial_count:
        raise EpisodeConstructionError("Every source trial must be accounted for exactly once.")
    if len(used_ids) != manifest.sequential_source_trial_count or len(tail_ids) != manifest.tail_source_trial_count:
        raise EpisodeConstructionError("Episode/tail source counts do not match manifest provenance.")
    if len(manifest.episodes) != manifest.episode_count:
        raise EpisodeConstructionError("Episode count does not match manifest contents.")


def condition_source_trials(episode: FixedIntentEpisode, condition_id: str) -> tuple[SourceTrial, ...]:
    """Return only the D-081 paired source slice for an A/B/C/D condition."""

    validate_fixed_episode(episode)
    condition = str(condition_id).upper()
    if condition not in CONDITION_SOURCE_POSITIONS:
        raise EpisodeConstructionError("condition_id must be one of A/B/C/D.")
    return tuple(episode.source_trials[position - 1] for position in CONDITION_SOURCE_POSITIONS[condition])


def order_episodes_for_e9(episodes: Sequence[FixedIntentEpisode]) -> tuple[FixedIntentEpisode, ...]:
    validated = tuple(episodes)
    for episode in validated:
        validate_fixed_episode(episode)
    if len({item.episode_id for item in validated}) != len(validated):
        raise EpisodeConstructionError("E9 episode stream contains duplicate episode IDs.")
    return tuple(sorted(validated, key=lambda item: (item.run_id, item.source_trials[0].event_sample, item.episode_id)))


def validate_fixed_episode(episode: FixedIntentEpisode) -> None:
    probe = EpisodeManifest(
        D081_EPISODE_MANIFEST_VERSION,
        (D081_POLICY_ID,),
        D081_GROUPING_KEY,
        D081_ORDERING_RULE,
        5,
        False,
        False,
        "exclude_record_and_retain_for_e1_e2",
        "A_and_B_use_source_position_1",
        "C_and_D_receive_positions_1_through_5_in_frozen_order",
        D081_E9_ORDERING_RULE,
        "0" * 64,
        5,
        5,
        0,
        1,
        (episode,),
        (),
        {str(episode.subject_id): 1},
        {str(episode.run_id): 1},
        {episode.intended_class: 1},
        False,
        "validation probe",
    )
    validate_episode_manifest(probe)


def episode_manifest_mapping(manifest: EpisodeManifest) -> dict[str, Any]:
    validate_episode_manifest(manifest)
    return _plain(asdict(manifest))


def freeze_episode_manifest(manifest: EpisodeManifest, path: str | Path) -> str:
    validate_episode_manifest(manifest)
    destination = Path(path).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(episode_manifest_mapping(manifest), sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    if destination.exists() and destination.read_text(encoding="utf-8") != text:
        raise EpisodeConstructionError("Frozen episode manifest already exists with different content.")
    if not destination.exists():
        destination.write_text(text, encoding="utf-8", newline="\n")
    return _file_sha256(destination)


def load_episode_manifest(path: str | Path) -> EpisodeManifest:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    manifest = episode_manifest_from_mapping(payload)
    validate_episode_manifest(manifest)
    return manifest


def episode_manifest_from_mapping(payload: Mapping[str, Any]) -> EpisodeManifest:
    def source(item: Mapping[str, Any]) -> SourceTrial:
        return SourceTrial(
            canonical_trial_id=str(item["canonical_trial_id"]),
            subject_id=int(item["subject_id"]),
            run_id=int(item["run_id"]),
            intended_class=str(item["intended_class"]),
            event_code=str(item["event_code"]),
            event_sample=int(item["event_sample"]),
            canonical_trial_index=int(item["canonical_trial_index"]),
            source_file=str(item["source_file"]),
        )

    episodes = tuple(
        FixedIntentEpisode(
            episode_id=str(item["episode_id"]),
            subject_id=int(item["subject_id"]),
            run_id=int(item["run_id"]),
            intended_class=str(item["intended_class"]),
            episode_block_index=int(item["episode_block_index"]),
            source_trials=tuple(source(trial) for trial in item["source_trials"]),
        )
        for item in payload["episodes"]
    )
    tails = tuple(
        TailExclusion(
            subject_id=int(item["subject_id"]),
            run_id=int(item["run_id"]),
            intended_class=str(item["intended_class"]),
            excluded_count=int(item["excluded_count"]),
            source_trials=tuple(source(trial) for trial in item["source_trials"]),
            reason=str(item["reason"]),
            eligible_for_single_trial_e1_e2=bool(item["eligible_for_single_trial_e1_e2"]),
        )
        for item in payload["tail_exclusions"]
    )
    return EpisodeManifest(
        manifest_version=str(payload["manifest_version"]),
        policy_ids=tuple(str(item) for item in payload["policy_ids"]),
        grouping_key=tuple(str(item) for item in payload["grouping_key"]),
        ordering_rule=str(payload["ordering_rule"]),
        block_size=int(payload["block_size"]),
        overlap=bool(payload["overlap"]),
        source_trial_reuse=bool(payload["source_trial_reuse"]),
        incomplete_tail_policy=str(payload["incomplete_tail_policy"]),
        ab_first_observation_rule=str(payload["ab_first_observation_rule"]),
        cd_source_order_rule=str(payload["cd_source_order_rule"]),
        e9_ordering_rule=str(payload["e9_ordering_rule"]),
        source_table_sha256=str(payload["source_table_sha256"]),
        source_trial_count=int(payload["source_trial_count"]),
        sequential_source_trial_count=int(payload["sequential_source_trial_count"]),
        tail_source_trial_count=int(payload["tail_source_trial_count"]),
        episode_count=int(payload["episode_count"]),
        episodes=episodes,
        tail_exclusions=tails,
        per_subject_episode_counts={str(key): int(value) for key, value in payload["per_subject_episode_counts"].items()},
        per_run_episode_counts={str(key): int(value) for key, value in payload["per_run_episode_counts"].items()},
        per_class_episode_counts={str(key): int(value) for key, value in payload["per_class_episode_counts"].items()},
        protected_outcomes_computed=bool(payload["protected_outcomes_computed"]),
        scientific_interpretation=str(payload["scientific_interpretation"]),
    )


def _validated_source_metadata(value: object) -> pd.DataFrame:
    if not isinstance(value, pd.DataFrame) or value.empty:
        raise EpisodeConstructionError("Episode construction requires a non-empty source metadata table.")
    missing = [column for column in REQUIRED_SOURCE_COLUMNS if column not in value.columns]
    if missing:
        raise EpisodeConstructionError("Missing required D-081 provenance: " + ", ".join(missing) + ".")
    metadata = value.loc[:, REQUIRED_SOURCE_COLUMNS].copy()
    for column in ("subject_id", "run_id", "event_sample", "trial_index"):
        if metadata[column].isnull().any():
            raise EpisodeConstructionError(f"D-081 provenance column {column} contains null values.")
        try:
            numeric = pd.to_numeric(metadata[column], errors="raise")
        except (TypeError, ValueError) as error:
            raise EpisodeConstructionError(f"D-081 provenance column {column} must contain integers.") from error
        if any(float(item) != int(item) for item in numeric):
            raise EpisodeConstructionError(f"D-081 provenance column {column} must contain integers.")
        metadata[column] = numeric.astype(int)
    if (metadata[["subject_id", "run_id"]] <= 0).any().any():
        raise EpisodeConstructionError("subject_id and run_id must be positive integers.")
    if (metadata[["event_sample", "trial_index"]] < 0).any().any():
        raise EpisodeConstructionError("event_sample and trial_index must be non-negative integers.")
    metadata["semantic_label"] = metadata["semantic_label"].astype(str).str.lower()
    if set(metadata["semantic_label"]) - set(ALLOWED_CLASSES):
        raise EpisodeConstructionError("D-081 permits only left/right intended classes.")
    metadata["event_code"] = metadata["event_code"].astype(str)
    mismatched = ((metadata["semantic_label"] == "left") & (metadata["event_code"] != "T1")) | (
        (metadata["semantic_label"] == "right") & (metadata["event_code"] != "T2")
    )
    if mismatched.any():
        raise EpisodeConstructionError("Intended class and EEGBCI event code are inconsistent.")
    metadata["source_file"] = metadata["source_file"].astype(str)
    if (metadata["source_file"].str.len() == 0).any():
        raise EpisodeConstructionError("Every source trial requires source_file provenance.")
    metadata["canonical_trial_id"] = metadata.apply(_canonical_trial_id, axis=1)
    if metadata["canonical_trial_id"].duplicated().any():
        raise EpisodeConstructionError("Canonical source trial identities must be unique.")
    metadata["_class_order"] = metadata["semantic_label"].map({"left": 0, "right": 1})
    return metadata.sort_values(
        ["subject_id", "run_id", "_class_order", "event_sample", "trial_index", "canonical_trial_id"],
        kind="stable",
    ).reset_index(drop=True)


def _canonical_trial_id(row: pd.Series) -> str:
    return (
        f"s{int(row['subject_id']):03d}-r{int(row['run_id']):02d}-"
        f"{str(row['event_code']).lower()}-sample{int(row['event_sample']):09d}-"
        f"trial{int(row['trial_index']):04d}"
    )


def _source_trial(row: pd.Series) -> SourceTrial:
    return SourceTrial(
        canonical_trial_id=str(row["canonical_trial_id"]),
        subject_id=int(row["subject_id"]),
        run_id=int(row["run_id"]),
        intended_class=str(row["semantic_label"]),
        event_code=str(row["event_code"]),
        event_sample=int(row["event_sample"]),
        canonical_trial_index=int(row["trial_index"]),
        source_file=str(row["source_file"]),
    )


def _episode_id(
    subject_id: int,
    run_id: int,
    intended_class: str,
    block_index: int,
    trials: Sequence[SourceTrial],
) -> str:
    digest = sha256("|".join(item.canonical_trial_id for item in trials).encode("utf-8")).hexdigest()[:16]
    return f"d081-s{subject_id:03d}-r{run_id:02d}-{intended_class}-b{block_index:03d}-{digest}"


def _counts(episodes: Sequence[FixedIntentEpisode], key) -> dict[str, int]:
    result: dict[str, int] = {}
    for episode in episodes:
        name = key(episode)
        result[name] = result.get(name, 0) + 1
    return dict(sorted(result.items()))


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    return value


def _mapping_sha256(payload: Mapping[str, Any]) -> str:
    text = json.dumps(_plain(payload), sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256(text.encode("utf-8")).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
