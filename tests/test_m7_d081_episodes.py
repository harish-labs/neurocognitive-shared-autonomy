from dataclasses import replace

import pandas as pd
import pytest

from src.evaluation.episodes import (
    EpisodeConstructionError,
    build_sequential_participation_manifest,
    condition_source_trials,
    construct_episode_manifest,
    freeze_episode_manifest,
    order_episodes_for_e9,
    validate_episode_manifest,
)


def _rows(*, subject=2, run=4, label="left", count=12, offset=0):
    code = "T1" if label == "left" else "T2"
    return [
        {
            "subject_id": subject,
            "run_id": run,
            "source_file": f"S{subject:03d}R{run:02d}.edf",
            "event_code": code,
            "semantic_label": label,
            "event_sample": offset + (count - index) * 160,
            "trial_index": offset + index,
        }
        for index in range(count)
    ]


def test_d081_groups_subject_run_class_orders_and_builds_nonoverlapping_blocks():
    rows = _rows(subject=2, run=4, label="left", count=12)
    rows += _rows(subject=2, run=4, label="right", count=5, offset=100)
    rows += _rows(subject=2, run=8, label="left", count=5, offset=200)
    rows += _rows(subject=3, run=4, label="left", count=5, offset=300)
    manifest = construct_episode_manifest(pd.DataFrame(reversed(rows)))
    assert manifest.episode_count == 5
    assert manifest.per_subject_episode_counts == {"2": 4, "3": 1}
    assert manifest.per_run_episode_counts == {"4": 4, "8": 1}
    assert manifest.per_class_episode_counts == {"left": 4, "right": 1}
    for episode in manifest.episodes:
        assert len(episode.source_trials) == 5
        assert len({item.subject_id for item in episode.source_trials}) == 1
        assert len({item.run_id for item in episode.source_trials}) == 1
        assert len({item.intended_class for item in episode.source_trials}) == 1
        assert list(episode.source_event_samples) == sorted(episode.source_event_samples)
    ids = [item.canonical_trial_id for episode in manifest.episodes for item in episode.source_trials]
    assert len(ids) == len(set(ids)) == 25


def test_d081_tail_is_recorded_and_remains_available_for_single_trial_e1_e2():
    source = pd.DataFrame(_rows(count=12))
    manifest = construct_episode_manifest(source)
    assert manifest.episode_count == 2
    assert manifest.sequential_source_trial_count == 10
    assert manifest.tail_source_trial_count == 2
    assert len(manifest.tail_exclusions) == 1
    tail = manifest.tail_exclusions[0]
    assert tail.excluded_count == 2
    assert tail.eligible_for_single_trial_e1_e2 is True
    assert manifest.source_trial_count == len(source) == 12


def test_ab_use_same_first_source_and_cd_use_identical_five_in_order():
    episode = construct_episode_manifest(pd.DataFrame(_rows(count=5))).episodes[0]
    a = condition_source_trials(episode, "A")
    b = condition_source_trials(episode, "B")
    c = condition_source_trials(episode, "C")
    d = condition_source_trials(episode, "D")
    assert a == b == (episode.source_trials[0],)
    assert c == d == episode.source_trials


def test_episode_ids_and_manifest_freeze_are_deterministic(tmp_path):
    table = pd.DataFrame(_rows(count=10))
    first = construct_episode_manifest(table.sample(frac=1.0, random_state=1))
    second = construct_episode_manifest(table.sample(frac=1.0, random_state=9))
    assert first == second
    assert len({item.episode_id for item in first.episodes}) == 2
    path = tmp_path / "episodes.json"
    first_hash = freeze_episode_manifest(first, path)
    assert freeze_episode_manifest(second, path) == first_hash
    with pytest.raises(EpisodeConstructionError, match="different content"):
        freeze_episode_manifest(construct_episode_manifest(pd.DataFrame(_rows(count=11))), path)


def test_fail_closed_for_missing_malformed_or_duplicate_provenance():
    table = pd.DataFrame(_rows(count=5))
    with pytest.raises(EpisodeConstructionError, match="Missing required"):
        construct_episode_manifest(table.drop(columns="event_sample"))
    bad = table.copy()
    bad.loc[0, "event_sample"] = -1
    with pytest.raises(EpisodeConstructionError, match="non-negative"):
        construct_episode_manifest(bad)
    duplicate = pd.concat([table, table.iloc[[0]]], ignore_index=True)
    with pytest.raises(EpisodeConstructionError, match="identities must be unique"):
        construct_episode_manifest(duplicate)


def test_manifest_validation_rejects_mixed_subject_run_class_short_episode_and_reuse():
    manifest = construct_episode_manifest(pd.DataFrame(_rows(count=10)))
    first, second = manifest.episodes
    mixed_subject = replace(first, source_trials=(replace(first.source_trials[0], subject_id=3), *first.source_trials[1:]))
    with pytest.raises(EpisodeConstructionError, match="mix subjects"):
        validate_episode_manifest(replace(manifest, episodes=(mixed_subject, second)))
    mixed_run = replace(first, source_trials=(replace(first.source_trials[0], run_id=8), *first.source_trials[1:]))
    with pytest.raises(EpisodeConstructionError, match="mix runs"):
        validate_episode_manifest(replace(manifest, episodes=(mixed_run, second)))
    mixed_class = replace(first, source_trials=(replace(first.source_trials[0], intended_class="right"), *first.source_trials[1:]))
    with pytest.raises(EpisodeConstructionError, match="mix intended classes"):
        validate_episode_manifest(replace(manifest, episodes=(mixed_class, second)))
    with pytest.raises(EpisodeConstructionError, match="exactly five"):
        validate_episode_manifest(replace(manifest, episodes=(replace(first, source_trials=first.source_trials[:4]), second)))
    reused = replace(second, source_trials=(first.source_trials[0], *second.source_trials[1:]))
    with pytest.raises(EpisodeConstructionError, match="reused"):
        validate_episode_manifest(replace(manifest, episodes=(first, reused)))


def test_e9_order_is_run_then_first_event_then_episode_id():
    rows = _rows(run=8, count=5, offset=1000) + _rows(run=4, count=10, offset=0)
    episodes = construct_episode_manifest(pd.DataFrame(rows)).episodes
    ordered = order_episodes_for_e9(tuple(reversed(episodes)))
    assert [item.run_id for item in ordered] == [4, 4, 8]
    assert [item.source_trials[0].event_sample for item in ordered[:2]] == sorted(
        item.source_trials[0].event_sample for item in ordered[:2]
    )


def test_episode_manifest_construction_does_not_read_prediction_or_outcome_columns():
    class Poison:
        def __str__(self):
            raise AssertionError("outcome field was accessed")

    table = pd.DataFrame(_rows(count=5))
    table["decoder_probability"] = [Poison()] * 5
    table["correctness"] = [Poison()] * 5
    manifest = construct_episode_manifest(table)
    assert manifest.protected_outcomes_computed is False


def test_mixed_labels_form_separate_episodes_never_one_sequence():
    manifest = construct_episode_manifest(pd.DataFrame(_rows(label="left", count=5) + _rows(label="right", count=5, offset=100)))
    assert [item.intended_class for item in manifest.episodes] == ["left", "right"]
    assert all(len({trial.intended_class for trial in item.source_trials}) == 1 for item in manifest.episodes)


def test_d083_participation_is_post_split_balanced_and_never_replaces_subjects():
    rows = _rows(subject=1, label="left", count=5)
    rows += _rows(subject=1, label="right", count=5, offset=100)
    rows += _rows(subject=2, label="left", count=5, offset=200)
    rows += _rows(subject=3, label="left", count=4, offset=300)
    episodes = construct_episode_manifest(pd.DataFrame(rows))
    participation = build_sequential_participation_manifest(
        episodes,
        split_manifest_sha256="a" * 64,
        partition_name="final_test",
        frozen_partition_subject_ids=(1, 2, 3),
    )
    assert participation.included_subject_ids == (1,)
    assert participation.excluded_subject_ids == (2, 3)
    assert participation.frozen_partition_subject_ids == (1, 2, 3)
    assert participation.no_replacement is True
    by_subject = {item.subject_id: item for item in participation.records}
    assert by_subject[2].exclusion_reason == "valid_d081_episodes_for_only_one_intended_class"
    assert by_subject[3].exclusion_reason == "no_valid_d081_t1_or_t2_episode"
