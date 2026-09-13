from dataclasses import replace
import json

import pandas as pd
import pytest

from src.eeg.epochs import REJECT_THRESHOLD_UV
from src.evaluation import cohort
from src.evaluation.cohort import (
    CohortManifestError,
    SOURCE_SUBJECT_IDS,
    SubjectEligibilityRecord,
    allocation_counts,
    build_qc_manifest,
    build_split_manifest,
    validate_qc_manifest,
    validate_split_manifest,
    write_immutable_manifest,
)
from src.evaluation.episodes import construct_episode_manifest
from src.evaluation.statistics import SubjectMetric, paired_subject_inference


def _records(excluded=()):
    excluded = set(excluded)
    return tuple(
        SubjectEligibilityRecord(
            subject_id=subject_id,
            requested_runs=(4, 8, 12),
            loaded_runs=(4, 8, 12),
            raw_t1_count=15,
            raw_t2_count=15,
            candidate_binary_epochs=30,
            retained_t1_count=0 if subject_id in excluded else 15,
            retained_t2_count=0 if subject_id in excluded else 15,
            rejected_epoch_count=30 if subject_id in excluded else 0,
            rejection_reasons={"EEG peak-to-peak": 30} if subject_id in excluded else {},
            eligible=subject_id not in excluded,
            exclusion_reason="all_binary_epochs_rejected_under_fixed_qc" if subject_id in excluded else None,
            within_subject_feasible=subject_id not in excluded,
            within_subject_infeasibility_reason="fewer_than_three_retained_trials_per_class" if subject_id in excluded else None,
            source_files=(f"S{subject_id:03d}R04.edf",),
            source_sha256=("0" * 64,),
        )
        for subject_id in SOURCE_SUBJECT_IDS
    )


def _qc(excluded=()):
    return build_qc_manifest(
        _records(excluded),
        dataset_id="EEGBCI-1.0.0",
        dataset_source="public-fixture",
        generating_code_sha="fixture-sha",
        reject_threshold_uv=REJECT_THRESHOLD_UV,
    )


def test_d082_qc_policy_is_fixed_and_actual_cohort_may_be_below_109():
    qc = _qc((4, 56, 60, 86))
    validate_qc_manifest(qc)
    assert qc.reject_threshold_uv == 150.0
    assert qc.no_ica and qc.no_automatic_interpolation
    assert qc.actual_eligible_count == 105
    assert qc.excluded_subject_ids == (4, 56, 60, 86)
    with pytest.raises(CohortManifestError, match="150"):
        validate_qc_manifest(replace(qc, reject_threshold_uv=151.0))


def test_d083_cross_subject_eligibility_accepts_one_per_class_without_within_or_episode_requirement():
    records = list(_records())
    original = records[0]
    records[0] = replace(
        original,
        raw_t1_count=1,
        raw_t2_count=1,
        candidate_binary_epochs=2,
        retained_t1_count=1,
        retained_t2_count=1,
        eligible=True,
        within_subject_feasible=False,
        within_subject_infeasibility_reason="fewer_than_three_retained_trials_per_class",
    )
    qc = build_qc_manifest(records, dataset_id="fixture", dataset_source="fixture", generating_code_sha="sha", reject_threshold_uv=150.0)
    assert 1 in qc.eligible_subject_ids
    assert qc.subjects[0].within_subject_feasible is False
    assert "D-083" in qc.preprocessing_qc_policy_ids


@pytest.mark.parametrize(("left", "right"), [(0, 1), (1, 0), (0, 0)])
def test_d083_excludes_zero_in_either_class_and_uses_no_performance_field(left, right):
    records = list(_records())
    original = records[0]
    records[0] = replace(
        original,
        raw_t1_count=left,
        raw_t2_count=right,
        candidate_binary_epochs=left + right,
        retained_t1_count=left,
        retained_t2_count=right,
        eligible=False,
        exclusion_reason="one_binary_class_absent_after_fixed_qc",
        within_subject_feasible=False,
        within_subject_infeasibility_reason="fewer_than_three_retained_trials_per_class",
    )
    qc = build_qc_manifest(records, dataset_id="fixture", dataset_source="fixture", generating_code_sha="sha", reject_threshold_uv=150.0)
    assert 1 in qc.excluded_subject_ids
    assert not hasattr(qc.subjects[0], "decoder_performance")


@pytest.mark.parametrize(
    ("n_subjects", "expected"),
    [(1, {"train": 1, "validation": 0, "final_test": 0}), (7, {"train": 5, "validation": 1, "final_test": 1}), (105, {"train": 73, "validation": 16, "final_test": 16}), (109, {"train": 76, "validation": 16, "final_test": 17})],
)
def test_largest_remainder_allocation_consumes_multiple_n(n_subjects, expected):
    _, _, _, counts = allocation_counts(n_subjects)
    assert counts == expected
    assert sum(counts.values()) == n_subjects


def test_exact_remainder_tie_prefers_final_then_validation():
    ideals, floors, remainders, counts = allocation_counts(105)
    assert ideals == {"train": 73.5, "validation": 15.75, "final_test": 15.75}
    assert floors == {"train": 73, "validation": 15, "final_test": 15}
    assert remainders["final_test"] == remainders["validation"] == 0.75
    assert counts == {"train": 73, "validation": 16, "final_test": 16}


def test_seed42_shuffle_is_sorted_input_reproducible_disjoint_and_exhaustive():
    qc = _qc((4, 56, 60, 86))
    first = build_split_manifest(qc, generating_code_sha="fixture-sha")
    second = build_split_manifest(qc, generating_code_sha="fixture-sha")
    validate_split_manifest(first)
    assert first == second
    expected = tuple(pd.Series(tuple(sorted(qc.eligible_subject_ids)), dtype=int).sample(frac=1.0, random_state=42))
    assert first.shuffled_eligible_subject_ids == expected
    partitions = [set(first.train_subject_ids), set(first.validation_subject_ids), set(first.final_test_subject_ids)]
    assert not partitions[0] & partitions[1]
    assert not partitions[0] & partitions[2]
    assert not partitions[1] & partitions[2]
    assert set().union(*partitions) == set(qc.eligible_subject_ids)
    assert not set(qc.excluded_subject_ids) & set().union(*partitions)
    assert first.actual_eligible_count == 105
    assert first.partition_counts == {"train": 73, "validation": 16, "final_test": 16}
    assert first.excluded_subject_reasons["4"] == "all_binary_epochs_rejected_under_fixed_qc"


def test_historical_provisional_final_membership_is_not_hard_coded():
    split = build_split_manifest(_qc((4,)), generating_code_sha="fixture-sha")
    historical = {2, 3, 15, 21, 22, 24, 52, 53, 61, 72, 75, 83, 87, 88, 93, 100, 103}
    assert set(split.final_test_subject_ids) != historical
    assert not hasattr(split, "replace_subject")
    assert not hasattr(cohort, "replace_subject")


def test_frozen_manifest_rejects_mutation_and_records_hashes(tmp_path):
    split = build_split_manifest(_qc((4, 56, 60, 86)), generating_code_sha="fixture-sha")
    path = tmp_path / "split.json"
    first_file_hash = write_immutable_manifest(split, path)
    assert len(first_file_hash) == 64
    assert json.loads(path.read_text())["manifest_sha256"] == split.manifest_sha256
    changed = replace(split, generating_code_sha="changed", manifest_sha256=split.manifest_sha256)
    with pytest.raises(CohortManifestError):
        write_immutable_manifest(changed, path)


def test_d079_exact_sign_flip_uses_actual_final_n():
    n_final = allocation_counts(105)[3]["final_test"]
    a = tuple(SubjectMetric(str(i), 0.0, 2) for i in range(n_final))
    b = tuple(SubjectMetric(str(i), 1.0, 2) for i in range(n_final))
    result = paired_subject_inference(a, b, bootstrap_seed=42)
    assert result.subject_count == n_final == 16
    assert result.permutation_assignments == 2 ** n_final


def test_d081_episode_input_can_be_restricted_to_frozen_partition():
    split = build_split_manifest(_qc((4, 56, 60, 86)), generating_code_sha="fixture-sha")
    subject_id = split.final_test_subject_ids[0]
    rows = [
        {"subject_id": subject_id, "run_id": 4, "source_file": "source.edf", "event_code": "T1", "semantic_label": "left", "event_sample": 160 * index, "trial_index": index}
        for index in range(5)
    ]
    episodes = construct_episode_manifest(pd.DataFrame(rows))
    assert {episode.subject_id for episode in episodes.episodes} <= set(split.final_test_subject_ids)
