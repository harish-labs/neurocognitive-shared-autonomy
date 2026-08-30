from pathlib import Path


def replace_exact(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Expected text not found in {path}: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def replace_section(path: str, start: str, end: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"Start marker missing in {path}: {start}")
    j = text.find(end, i)
    if j < 0:
        raise SystemExit(f"End marker missing in {path}: {end}")
    p.write_text(text[:i] + new.rstrip() + "\n\n" + text[j:], encoding="utf-8")


# Guard against running against the wrong decision state.
decisions = Path("DECISIONS.md").read_text(encoding="utf-8")
for token in ("## D-040", "## D-041", "## D-042"):
    if token not in decisions:
        raise SystemExit(f"Missing approved decision {token}")

replace_section(
    "docs/06_DATASET_AND_DATA_PIPELINE.md",
    "# 36. STAGE 11 — DATASET SPLITTING",
    "---\n\n# 37. NON-NEGOTIABLE LEAKAGE RULES",
    """# 36. STAGE 11 — DATASET SPLITTING

Dataset splitting is one of the most important scientific parts of the project.

The primary split protocol is approved by D-040 through D-042.

## Within-subject evaluation

Use a deterministic, class-stratified split at the original-trial level:

```text
60% train
20% validation
20% test
```

No original trial, or any derived window from that trial, may cross partitions.

If retained class counts for a subject cannot support the approved class-stratified split, report the condition rather than silently substituting another split rule.

## Cross-subject evaluation

The primary cross-subject protocol is a fixed subject-held-out split:

```text
70% train subjects
15% validation subjects
15% final test subjects
```

A subject belongs to exactly one partition. No trial from a validation or final-test subject may appear in training.

## Held-out subject strategy

After the approved preprocessing/QC boundary:

```text
form the eligible subject list
shuffle once with fixed seed 42
freeze subject IDs in a versioned split manifest before model fitting
```

For a full eligible 109-subject EEGBCI cohort, the frozen counts are:

```text
76 train subjects
16 validation subjects
17 final test subjects
```

Final-test subjects must not be used for CSP fitting, EEGNet training, hyperparameter selection, calibration fitting, threshold tuning, or learned adaptation.

If preprocessing/QC produces an eligible cohort size other than 109, do not silently invent another count-allocation rule. Report the eligible count for reviewer decision before freezing the final subject manifest.

Within-subject and cross-subject results answer different scientific questions and must be reported separately.""",
)

replace_section(
    "docs/17_EXPERIMENTAL_DESIGN.md",
    "# 49. E8 — CROSS-SUBJECT EVALUATION",
    "# 53. WITHIN-SUBJECT VS CROSS-SUBJECT",
    """# 49. E8 — CROSS-SUBJECT EVALUATION

Cross-subject evaluation is an approved research direction and its primary protocol is frozen by D-041 and D-042.

Purpose:

> Test whether EEG decoding/confidence behavior generalizes to subjects not used in model fitting.

---

# 50. CROSS-SUBJECT RULE

The primary protocol is a fixed subject-held-out split:

```text
70% train subjects
15% validation subjects
15% final test subjects
```

If subject \(u\) is in validation or final test:

```text
no trials from subject u
```

may appear in training. Subject IDs must be disjoint across all three partitions.

---

# 51. PRIMARY CROSS-SUBJECT PROTOCOL

After the approved preprocessing/QC boundary:

```text
1. form the eligible subject list
2. apply one deterministic shuffle with seed 42
3. freeze the subject IDs in a versioned split manifest before model fitting
```

For a full eligible cohort of 109 EEGBCI subjects:

```text
76 train
16 validation
17 final test
```

Leave-one-subject-out or grouped subject K-fold may be added later only as explicitly authorized secondary analyses; they are not the primary cross-subject protocol.

If preprocessing/QC yields an eligible cohort size other than 109, the final subject-count allocation returns to reviewer decision rather than being silently redefined in code.

---

# 52. CROSS-SUBJECT CALIBRATION

Calibration must respect frozen subject boundaries where the scientific question concerns unseen subjects.

Do not:

```text
test subject labels
→ fit calibrator
→ call result cross-subject generalization
```

unless the experiment explicitly studies post-calibration personalization rather than zero-shot generalization.

The exact calibration method and fitting partition remain governed by U-016 and U-017.""",
)

replace_exact(
    "docs/18_METRICS_AND_EVALUATION.md",
    "# 66. M8 — CROSS-SUBJECT AGGREGATION\n\nCross-subject results must preserve individual-subject performance.\n\nRecommended outputs:",
    """# 66. M8 — CROSS-SUBJECT AGGREGATION

Under D-041 and D-042, the primary cross-subject evaluation uses a fixed 70/15/15 subject-held-out train/validation/final-test split with a seed-42 frozen subject manifest before model fitting. For a full eligible 109-subject cohort this corresponds to 76 train, 16 validation, and 17 final-test subjects.

Cross-subject results must preserve individual-subject performance. Final-test subject results must not be used to fit or select models, calibration, thresholds, or adaptation parameters.

Within-subject and cross-subject results must be reported separately.

Recommended outputs:""",
)

replace_exact(
    "AGENTS.md",
    """Resolved for the initial M1 preprocessing/epoching pipeline by D-031 through D-039:

```text
7–30 Hz band-pass
average EEG reference
canonical epoch -1.0 s to +4.0 s
initial CSP crop +1.0 s to +2.0 s
baseline=None
no ICA / no automatic interpolation; reject >150 µV peak-to-peak and log
exclude T0 from binary training; preserve annotations/provenance
preserve all 64 validated EEG channels
no resampling; preserve 160 Hz
canonical MNE Epochs; persisted *-epo.fif
```

Currently unresolved or change-controlled items include:

1. final train/validation/test protocol;
2. final cross-subject protocol;
3. final CSP settings;
4. final EEGNet architecture/hyperparameters;
5. calibration method;
6. calibration fitting partition;
7. calibration binning;
8. Bayesian goal-evidence likelihood construction;
9. binary EEG-to-multiple-goal interaction protocol;
10. Bayesian stopping/commitment rule;
11. confidence thresholds;
12. exact adaptation mechanism;
13. environmental risk scale;
14. risk weight \(\\lambda\);
15. prohibited-hazard threshold;
16. final A/B/C/D component matrix;
17. final statistical-analysis policy.""",
    """Resolved for the initial M1 preprocessing/epoching pipeline by D-031 through D-039:

```text
7–30 Hz band-pass
average EEG reference
canonical epoch -1.0 s to +4.0 s
initial CSP crop +1.0 s to +2.0 s
baseline=None
no ICA / no automatic interpolation; reject >150 µV peak-to-peak and log
exclude T0 from binary training; preserve annotations/provenance
preserve all 64 validated EEG channels
no resampling; preserve 160 Hz
canonical MNE Epochs; persisted *-epo.fif
```

Resolved for EEG split/evaluation by D-040 through D-042:

```text
within-subject: deterministic class-stratified 60/20/20 at original-trial level
primary cross-subject: fixed subject-held-out 70/15/15
held-out assignment: seed 42 and versioned frozen subject manifest
full eligible 109-subject cohort: 76 train / 16 validation / 17 final test
no subject, original-trial, or derived-window leakage across protected partitions
```

Currently unresolved or change-controlled items include:

1. final CSP settings;
2. final EEGNet architecture/hyperparameters;
3. calibration method;
4. calibration fitting partition;
5. calibration binning;
6. Bayesian goal-evidence likelihood construction;
7. binary EEG-to-multiple-goal interaction protocol;
8. Bayesian stopping/commitment rule;
9. confidence thresholds;
10. exact adaptation mechanism;
11. environmental risk scale;
12. risk weight \(\\lambda\);
13. prohibited-hazard threshold;
14. final A/B/C/D component matrix;
15. final statistical-analysis policy.""",
)

# Narrow PROJECT_STATE reconciliation: update stale facts without rewriting unrelated sections.
replace_exact(
    "PROJECT_STATE.md",
    "M1 active — loader and visualization verified; preprocessing decisions approved",
    "M1 active — loader, visualization, preprocessing, and epochs verified; split decisions approved",
)
replace_exact(
    "PROJECT_STATE.md",
    """Latest Prerequisite Methodology Reconciliation Commit:
d71292387d4476b8ab40841d4ed1544cba3d81b6

Latest Verified Software Commit:
9b241681dfc986f53f5f8c0fcf40a3e3cea496e7""",
    """Latest Accepted Software Commit:
1af72b5deb9981f469a4394859aac49add65e2a7

Latest Approved Scientific-Decision Commit:
ea00a631b60967cfece65b42e00e7b36c4efac7d""",
)
replace_exact(
    "PROJECT_STATE.md",
    "> **M1-T01 and M1-T02 are completed, merged, and verified on canonical `main`. The repository has a verified EEGBCI loader and a verified EEG visualization/inspection module. Project Owner approvals resolving preprocessing decisions U-001 through U-009 are recorded as D-031 through D-039 in `DECISIONS.md`, and the affected numbered methodology documents are reconciled to those decisions. No preprocessing or epoching code has been implemented or authorized yet. M1-T03 is ready for a separate explicit implementation ticket.**",
    "> **M1-T01, M1-T02, and M1-T03 are completed, merged, scientifically reviewed, and verified on canonical `main`. The repository has a verified EEGBCI loader, visualization/inspection module, and approved preprocessing/epoch extraction pipeline. U-001 through U-009 are resolved as D-031 through D-039. U-010 through U-012 are resolved as D-040 through D-042. No dataset-splitting implementation is currently authorized.**",
)
replace_exact(
    "PROJECT_STATE.md",
    "`CURRENT_TASK.md` records that scientific preprocessing decisions are approved but no implementation ticket is active.",
    "`CURRENT_TASK.md` records that M1-T03 is closed and no implementation ticket is active.",
)
replace_exact(
    "PROJECT_STATE.md",
    "> **M1-T03 preprocessing/epoching is the next candidate implementation task and its scientific/documentation prerequisites are satisfied, but it is not yet authorized. A new `CURRENT_TASK.md` implementation ticket must be explicitly approved before coding begins.**\n\nDo not begin preprocessing or epoching until that authorization exists.",
    "> **A narrow M1 split-manifest / leakage-safe dataset-splitting task is the next candidate implementation task. D-040 through D-042 and the relevant methodology are aligned, but a new `CURRENT_TASK.md` implementation ticket must still be explicitly approved before coding begins.**\n\nDo not begin dataset splitting, CSP/LDA, or later work until that authorization exists.",
)
replace_exact(
    "PROJECT_STATE.md",
    "| 3 | EEG Preprocessing / Epochs | BLOCKED | No | No | — | Scientific/docs prerequisites satisfied; active implementation ticket still required |",
    "| 3 | EEG Preprocessing / Epochs | PASS | Yes | Yes | `1af72b5deb9981f469a4394859aac49add65e2a7` | M1-T03 completed, reviewed, and merged |",
)
replace_exact(
    "PROJECT_STATE.md",
    """## Evaluation

```text
- final train/validation/test protocol
- final cross-subject protocol
- exact held-out subject strategy
- final statistical-analysis policy
```""",
    """## Evaluation

Resolved by D-040 through D-042:

```text
- within-subject deterministic class-stratified 60/20/20 split at original-trial level
- primary fixed subject-held-out 70/15/15 cross-subject split
- seed-42 frozen subject manifest; 76/16/17 subjects for a full eligible cohort of 109
```

Still unresolved:

```text
- final statistical-analysis policy
```

If preprocessing/QC yields an eligible subject cohort size other than 109, D-042 requires reviewer decision before the final subject manifest is frozen.""",
)
replace_exact(
    "PROJECT_STATE.md",
    """Preprocessing:
BLOCKED — approved parameters recorded, documentation reconciliation and active ticket still required

Event extraction:
NOT STARTED

Epoching:
BLOCKED — approved parameters recorded, documentation reconciliation and active ticket still required""",
    """Preprocessing:
PASS — accepted in M1-T03

Event extraction:
PASS — accepted in M1-T03

Epoching:
PASS — accepted in M1-T03""",
)
replace_exact(
    "PROJECT_STATE.md",
    """Train/validation/test split:
UNRESOLVED

Cross-subject split:
UNRESOLVED""",
    """Train/validation/test split:
APPROVED — D-040; implementation not started

Cross-subject split:
APPROVED — D-041/D-042; implementation not started""",
)
replace_exact(
    "PROJECT_STATE.md",
    "- split protocol freeze\n",
    "",
)

# Append a concise current-state correction instead of rewriting historical sections wholesale.
p = Path("PROJECT_STATE.md")
text = p.read_text(encoding="utf-8")
summary_marker = "# 45. CURRENT PROJECT STATE SUMMARY"
i = text.find(summary_marker)
if i < 0:
    raise SystemExit("Missing PROJECT_STATE summary marker")
new_summary = """# 45. CURRENT PROJECT STATE SUMMARY

The project currently has three accepted and merged M1 software tasks on canonical `main`: M1-T01 (PhysioNet EEGBCI loader), M1-T02 (EEG visualization/inspection), and M1-T03 (EEG preprocessing/epochs). M1-T03 is accepted at commit `1af72b5deb9981f469a4394859aac49add65e2a7`; final review reported 9 targeted preprocessing/epoch tests and 10 loader regression tests passing, plus real subject 1 smoke checks on runs 4/8/12. Those smoke checks are implementation verification, not model-performance results.

The Project Owner approved U-010 through U-012, recorded as D-040 through D-042 at commit `ea00a631b60967cfece65b42e00e7b36c4efac7d`: separate within-subject and cross-subject evaluation tracks, deterministic class-stratified 60/20/20 within-subject splitting at original-trial level, fixed 70/15/15 subject-held-out primary cross-subject evaluation, and a seed-42 frozen subject manifest with 76/16/17 subjects when the full 109-subject cohort is eligible. The split/evaluation methodology is reconciled to those decisions. No dataset-splitting implementation is authorized yet; a separate narrow `CURRENT_TASK.md` ticket remains required. The project remains an offline prerecorded EEG system rather than live EEG.
"""
p.write_text(text[:i] + new_summary, encoding="utf-8")
