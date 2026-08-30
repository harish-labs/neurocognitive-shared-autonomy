# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is **actually true now** about the project  
**Update rule:** Update after every accepted implementation task, verified experiment, major blocker, approved scientific decision, or accepted architectural change  
**Do not use for:** speculative ideas, unapproved methodology, literature notes, hypothetical results, or future features  
**Workflow:** **ChatGPT + Project Owner + Codex + Git/GitHub**  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. HOW TO USE THIS FILE

This file answers one question:

> **What is actually true about the project right now?**

Use:

```text
MASTER_PROJECT_SPEC.md
→ what the project IS

DECISIONS.md
→ what has been explicitly DECIDED

CURRENT_TASK.md
→ what is being DONE NOW

PROJECT_STATE.md
→ what is ACTUALLY TRUE NOW

EXPERIMENT_LOG.md
→ what has actually been RUN

RESEARCH_LOG.md
→ what has been RESEARCHED / LEARNED

TODO.md
→ what MAY be done later

AGENTS.md
→ how Codex must operate in the repository
```

Do not blur these roles.

---

# 1. STATUS AT A GLANCE

```text
Project Phase:
M1 active — loader, visualization, preprocessing, and epochs verified; split decisions approved

Current Milestone:
M1 — EEG Dataset / Loader / Epochs / CSP+LDA

Current Module:
No active coding task authorized

Current Task ID:
NONE AUTHORIZED

Task Status:
PENDING APPROVAL

Canonical Branch:
main

Latest Accepted Software Commit:
1af72b5deb9981f469a4394859aac49add65e2a7

Latest Approved Scientific-Decision Commit:
ea00a631b60967cfece65b42e00e7b36c4efac7d

Latest Valid Experiment:
None yet

Last Updated:
2026-08-30

Updated By:
ChatGPT + Project Owner
```

Allowed operational statuses:

```text
NOT STARTED
IN PROGRESS
PARTIAL
PARTIAL-BLOCKED
BLOCKED
PASS
FAIL
```

---

# 2. CURRENT PROJECT PHASE

Current state:

> **M1-T01, M1-T02, and M1-T03 are completed, merged, scientifically reviewed, and verified on canonical `main`. The repository has a verified EEGBCI loader, visualization/inspection module, and approved preprocessing/epoch extraction pipeline. U-001 through U-009 are resolved as D-031 through D-039. U-010 through U-012 are resolved as D-040 through D-042. No dataset-splitting implementation is currently authorized.**

Do not mark coding milestones complete until code has been:

```text
implemented
+
run
+
tested
+
verified
```

---

# 3. CURRENT DEVELOPMENT WORKFLOW

The approved implementation workflow is:

```text
ChatGPT
    ↓
Project Brain / Research Director

Project Owner
    ↓
Final approval authority

Codex
    ↓
Implementation engineer

Tests / Experiments
    ↓

ChatGPT Review
    ↓

Project Owner Acceptance
    ↓

Git / GitHub + Live State Files
```

Repository-level Codex instructions:

```text
AGENTS.md
```

---

# 4. CURRENT DOCUMENTATION STATUS

## Generated core documents

```text
MASTER_PROJECT_SPEC.md
01_PROJECT_CONCEPT_AND_PROBLEM.md
02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md
03_SEARCH_AND_RESCUE_SCENARIO.md
04_SYSTEM_ARCHITECTURE.md
05_TECHNOLOGY_STACK.md
06_DATASET_AND_DATA_PIPELINE.md
07_NEUROSCIENCE_AND_BCI_FOUNDATIONS.md
08_EEG_SIGNAL_PROCESSING_AND_ML.md
09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md
10_BAYESIAN_GOAL_INFERENCE.md
11_COGNITIVE_AND_ADAPTIVE_MODEL.md
12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md
13_AUTONOMOUS_PLANNING_AND_CONTROL.md
14_SAFETY_CRITICAL_CONTROL.md
15_IMPLEMENTATION_BLUEPRINT.md
16_REPOSITORY_AND_CODE_ARCHITECTURE.md
17_EXPERIMENTAL_DESIGN.md
18_METRICS_AND_EVALUATION.md
19_TESTING_AND_VERIFICATION.md
20_LIMITATIONS_ETHICS_AND_VALIDITY.md
21_LITERATURE_AND_SCIENTIFIC_FOUNDATION.md
22_AI_DEVELOPMENT_WORKFLOW.md
23_RESULTS_AND_ANALYSIS.md
24_DISCUSSION_AND_FINDINGS.md
AGENTS.md
```

## Current decision-alignment status

`DECISIONS.md` resolves U-001 through U-009 as D-031 through D-039 and U-010 through U-012 as D-040 through D-042.

The approved preprocessing and split/evaluation methodology is aligned on canonical project documents, including:

```text
docs/06_DATASET_AND_DATA_PIPELINE.md
docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md
docs/15_IMPLEMENTATION_BLUEPRINT.md
docs/17_EXPERIMENTAL_DESIGN.md
docs/18_METRICS_AND_EVALUATION.md
```

No active implementation ticket exists. A narrow split-manifest implementation still requires explicit Project Owner authorization in `CURRENT_TASK.md`.

## Next numbered scientific document

```text
25_FUTURE_WORK.md
```

---

# 5. CURRENT MILESTONE MODEL

The implementation milestone sequence remains:

```text
M0 — Infrastructure / Repository / Contracts
M1 — EEG Dataset / Loader / Epochs / CSP+LDA
M2 — EEGNet / Neural Decoder
M3 — Calibration / Bayesian Inference / Uncertainty / Adaptation Framework
M4 — 2D SAR Environment / A* / Safety
M5 — Shared Autonomy / Human Interaction
M6 — End-to-End Real EEG Replay Integration
M7 — Experiments / A-B-C-D / Ablations / Robustness / Cross-Subject
M8 — Streamlit / Results Presentation / GitHub / Portfolio
```

Current milestone:

```text
M1 — EEG Dataset / Loader / Epochs / CSP+LDA
```

---

# 6. ACTIVE TASK

Current active coding task:

```text
None authorized
```

`CURRENT_TASK.md` records that M1-T03 is closed and no implementation ticket is active.

---

# 7. NEXT CANDIDATE IMPLEMENTATION TASK

> **A narrow M1 split-manifest / leakage-safe dataset-splitting task is the next candidate implementation task. D-040 through D-042 and the relevant methodology are aligned, but a new `CURRENT_TASK.md` implementation ticket must still be explicitly approved before coding begins.**

Do not begin dataset splitting, CSP/LDA, or later work until that authorization exists.

---

# 8. IMPLEMENTATION STATUS MATRIX

| Module | Component | Status | Automated Tests | Manual Verification | Latest Artifact / Commit | Notes |
|---|---|---|---|---|---|---|
| 0 | Config / Infrastructure | NOT STARTED | No | No | — | M0 pending |
| 1 | EEG Data Loader | PASS | Yes | Yes | `9b241681dfc986f53f5f8c0fcf40a3e3cea496e7` | M1-T01 completed and merged |
| 2 | EEG Visualization / Inspection | PASS | Yes | Yes | `9b241681dfc986f53f5f8c0fcf40a3e3cea496e7` | M1-T02 completed and merged |
| 3 | EEG Preprocessing / Epochs | PASS | Yes | Yes | `1af72b5deb9981f469a4394859aac49add65e2a7` | M1-T03 completed, reviewed, and merged |
| 4 | CSP + LDA | NOT STARTED | No | No | — | Depends on valid epochs/split |
| 5 | EEGNet / Compact CNN | NOT STARTED | No | No | — | |
| 6 | Unified Decoder Interface | NOT STARTED | No | No | — | |
| 7 | Probability Calibration | PARTIAL-BLOCKED | No | No | — | Metrics can precede final method |
| 8 | Bayesian Goal Inference | NOT STARTED | No | No | — | Generic synthetic core can proceed independently |
| 9 | Uncertainty / Entropy | NOT STARTED | No | No | — | Threshold policy unresolved |
| 10 | Adaptation / Personalization | BLOCKED | No | No | — | Exact mechanism unresolved |
| 11 | 2D SAR Environment | NOT STARTED | No | No | — | |
| 12 | A* Planner | NOT STARTED | No | No | — | Risk parameters unresolved |
| 13 | Safety Controller | NOT STARTED | No | No | — | Hard basic safety can precede hazard threshold |
| 14 | Shared-Autonomy Controller | PARTIAL-BLOCKED | No | No | — | Interface possible; thresholds unresolved |
| 15 | Human Interaction Layer | NOT STARTED | No | No | — | |
| 16 | Offline EEG Replay | NOT STARTED | No | No | — | |
| 17 | Streamlit Dashboard | NOT STARTED | No | No | — | Build after core |
| 18 | Experiment Logger | NOT STARTED | No | No | — | |
| 19 | EEG / Model Evaluation | NOT STARTED | No | No | — | |
| 20 | Full System Evaluation | BLOCKED | No | No | — | Final protocol required |

---

# 9. CURRENTLY VERIFIED SOFTWARE COMPONENTS

Current state:

```text
EEG Data Loader:
- src/eeg/loader.py implemented
- tests/test_loader.py implemented
- 10 loader tests passed
- real EEGBCI subject 1 runs 4 / 8 / 12 loaded successfully
- 64 channels, 160 Hz, T0/T1/T2, and standard_1005 montage verified

EEG Visualization / Inspection:
- src/eeg/visualization.py implemented
- tests/test_visualization.py implemented
- loader + visualization regression coverage passed at acceptance
- real subject 1 runs 4 / 8 / 12 inspected with raw traces, PSD, sensors, and annotation overview

EEG Preprocessing / Epochs:
- src/eeg/preprocessing.py and src/eeg/epochs.py implemented
- tests/test_preprocessing.py and tests/test_epochs.py implemented
- final targeted preprocessing/epoch review: 9 passed
- final loader regression review: 10 passed
- real subject 1 runs 4 / 8 / 12 smoke-verified
- 7–30 Hz filter, average reference, 64-channel order, 160 Hz, -1.0-to-4.0 s epochs, baseline=None, T0 exclusion, 150 µV rejection with reason/threshold provenance, and *-epo.fif persistence contract verified
- high real-data rejection counts were preserved as an observation, not used to change D-035
```

No software component may be listed as verified until actual code has been executed and checked.

---

# 10. CURRENTLY IMPLEMENTED BUT UNVERIFIED

Current state:

```text
None.
```

If code exists later but has not passed verification, list it here rather than marking it `PASS`.

Template:

```text
Component:
Implementation status:
Missing tests:
Missing manual check:
Known risk:
Next verification action:
```

---

# 11. CURRENT SCIENTIFIC BLOCKERS

The following decisions remain unresolved unless a later approved entry in `DECISIONS.md` supersedes this list.

## EEG / preprocessing

The initial M1 preprocessing decisions are resolved in D-031 through D-039:

```text
band-pass: 7–30 Hz
EEG reference: average EEG reference
canonical epoch: -1.0 s to +4.0 s
initial CSP crop: +1.0 s to +2.0 s
baseline: None
artifact policy: no ICA/interpolation; reject >150 µV peak-to-peak and log
T0: exclude from binary training; preserve annotations/provenance
channels: preserve all 64; no reduction
resampling: none; preserve 160 Hz
processed representation: MNE Epochs; persisted `*-epo.fif`
```

These are no longer scientific blockers for M1-T03, but the affected numbered documents must be reconciled before implementation authorization.

## Evaluation

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

If preprocessing/QC yields an eligible subject cohort size other than 109, D-042 requires reviewer decision before the final subject manifest is frozen.

## Models / calibration

```text
- exact CSP configuration
- final EEGNet / compact CNN architecture details
- final training hyperparameters
- calibration method
- calibration fitting partition
- reliability-diagram binning strategy
```

## Bayesian / cognition

```text
- binary EEG → multi-goal SAR interaction protocol
- exact P(class|EEG) → P(E|G) likelihood construction
- Bayesian stopping / commitment rule
- prior policy
- evidence sequence / reset semantics where not already fixed
```

## Shared autonomy

```text
- confidence / entropy thresholds
- exact PROCEED / CONFIRM / DEFER policy
- whether confirmation is mandatory in particular states
- fallback after prolonged uncertainty
```

## Adaptation

```text
- exact adaptation target
- update formula
- bounds
- warm-up
- decay
- feedback semantics
```

## Planning / safety

```text
- environmental risk values
- risk normalization
- λ
- prohibited-hazard threshold
- final no-safe-path policy
```

## Experiments

```text
- final A/B/C/D component matrix
- final robustness perturbation severities
- final inferential-statistics plan
```

These unresolved items must remain visible.

---

# 12. CURRENT TECHNICAL BLOCKERS

Current state:

```text
M1-T03 has no open implementation blocker after acceptance.
Split-manifest implementation is not active.
```

The next split-manifest task is blocked only by the absence of a separately approved active `CURRENT_TASK.md` ticket. Do not invent technical blockers before actual implementation.

---

# 13. LOCKED / APPROVED PROJECT DECISIONS

The following are currently fixed unless explicitly changed through approved change control.

## Project identity

```text
Application:
Search & Rescue

Project title:
NeuroCognitive Shared Autonomy for Search & Rescue —
EEG-Based Intent Decoding with Bayesian Goal Inference
and Uncertainty-Aware Adaptive Control
```

## Core principle

> **Human determines WHAT intended objective is selected. AI determines HOW to achieve it safely.**

## EEG

```text
Dataset:
PhysioNet EEG Motor Movement/Imagery Database

Access:
MNE-Python

Initial motor-imagery runs:
4, 8, 12

Initial task:
Left vs Right motor imagery

EEG mode:
Public prerecorded EEG only

Loader montage:
standard_1005
```

## Initial M1 preprocessing / epoching

```text
Band-pass:
7–30 Hz

EEG reference:
average EEG reference

Canonical epoch:
-1.0 s to +4.0 s relative to cue onset

Initial CSP training crop:
+1.0 s to +2.0 s relative to cue onset

Baseline correction:
None

Artifact handling:
no ICA
no automatic bad-channel interpolation
reject epoch if EEG peak-to-peak amplitude >150 µV
log rejected epochs/reasons

T0 handling:
exclude from binary epoch/training dataset
preserve raw annotations/provenance

Channels:
all 64 validated EEG channels
no reduction in M1-T03

Resampling:
none
preserve native 160 Hz

Canonical processed representation:
MNE Epochs

Persisted processed epochs:
MNE FIF `*-epo.fif`
```

## Split / validation protocol

```text
Within-subject:
deterministic class-stratified 60/20/20 at original-trial level

Primary cross-subject:
fixed subject-held-out 70/15/15

Held-out assignment:
seed 42
versioned frozen subject manifest before model fitting
for a full eligible 109-subject cohort: 76 train / 16 validation / 17 final test

Protection:
no subject, original-trial, or derived-window leakage across protected partitions
final-test subjects are excluded from fitting/tuning/calibration/adaptation
```

## Dataset semantics

```text
T0 = rest
T1 = imagined left fist
T2 = imagined right fist
```

## Core models

```text
Mandatory classical baseline:
CSP + LDA

Neural decoder:
EEGNet / scientifically accurate compact EEG CNN
```

## Probability / cognition

```text
Calibration:
Required conceptually

Bayesian inference:
Required

Primary uncertainty:
Posterior entropy
```

## Autonomy

```text
Shared autonomy:
Required

Human controls:
CONFIRM
OVERRIDE
PAUSE
STOP
```

## Search & Rescue

```text
Simulation:
Simple 2D technical environment

Agent count:
Single agent

Planner:
A*

Actions:
UP
DOWN
LEFT
RIGHT
WAIT

Physical robot:
Not required

3D:
Not required
```

## Safety

```text
Separate safety controller:
Required

Planner proposes
→ safety authorizes
→ environment executes
```

## UI

```text
Streamlit:
Presentation layer only

Core system:
Must run headlessly
```

## Development

```text
ChatGPT:
Project Brain / Research Director

Project Owner:
Final authority

Codex:
Implementation engineer

Git / GitHub:
Persistent technical source of truth

Codex repository instructions:
AGENTS.md
```

---

# 14. CURRENT DATASET STATE

```text
Dataset identity:
PhysioNet EEGMMIDB / EEGBCI

Subjects available:
109

Channels:
64

Sampling frequency:
160 Hz

Runs available:
14

Current initial runs:
4, 8, 12

Current initial subject subset:
subject 1 verified for loader and inspection smoke checks

Local dataset cache:
VERIFIED

Real EEG successfully loaded:
YES

Channel names standardized:
YES

Montage attached:
YES

Montage manually verified:
YES

Annotations inspected:
YES

T0/T1/T2 manually verified:
YES

Real EEG inspection successfully generated:
YES
```

Update only after actual execution.

---

# 15. CURRENT EEG PIPELINE STATE

```text
Loader:
PASS

Dataset caching:
PASS

Channel standardization:
PASS

Montage:
PASS

Visualization:
PASS

Preprocessing:
PASS — accepted in M1-T03

Event extraction:
PASS — accepted in M1-T03

Epoching:
PASS — accepted in M1-T03

T0 handling:
APPROVED — exclude from binary training; preserve annotations/provenance

Channel policy:
APPROVED — all 64 channels; no reduction

Sampling policy:
APPROVED — no resampling; preserve 160 Hz

Processed representation:
APPROVED — MNE Epochs; persisted `*-epo.fif`

Train/validation/test split:
APPROVED — D-040; implementation not started

Cross-subject split:
APPROVED — D-041/D-042; implementation not started

CSP+LDA:
NOT STARTED

EEGNet:
NOT STARTED

Unified decoder interface:
NOT STARTED

Calibration metrics:
NOT STARTED

Final calibrator:
METHOD UNRESOLVED
```

---

# 16. CURRENT COGNITIVE / BAYESIAN STATE

```text
Generic Bayesian core:
NOT STARTED

GoalEvidence interface:
DESIGNED CONCEPTUALLY

Real EEG → GoalEvidence adapter:
BLOCKED

Binary EEG → multi-goal protocol:
UNRESOLVED

Likelihood semantics:
UNRESOLVED

Posterior belief:
NOT STARTED

Entropy:
NOT STARTED

Normalized entropy:
OPTIONAL / UNRESOLVED

Commitment rule:
UNRESOLVED

Confidence thresholds:
UNRESOLVED

Adaptation:
MECHANISM UNRESOLVED
```

---

# 17. CURRENT SHARED-AUTONOMY STATE

```text
Shared-autonomy controller:
NOT STARTED

Conceptual modes:
PROCEED
CONFIRM
DEFER
PAUSE
STOP

Exact thresholds:
UNRESOLVED

Candidate goal vs approved goal:
ARCHITECTURALLY DEFINED

Human confirmation:
NOT STARTED

Human override:
NOT STARTED

Pause:
NOT STARTED

Emergency stop:
NOT STARTED
```

---

# 18. CURRENT AUTONOMY / SAR STATE

```text
2D SAR environment:
NOT STARTED

Single rescue agent:
DESIGN APPROVED

UP / DOWN / LEFT / RIGHT / WAIT:
DESIGN APPROVED

A*:
NOT STARTED

Manhattan heuristic:
DESIGN APPROVED FOR 4-CONNECTED CORE

Risk-aware cost:
DESIGNED CONCEPTUALLY

Risk values:
UNRESOLVED

Risk λ:
UNRESOLVED

Blocked paths:
DESIGN APPROVED

Hazard areas:
DESIGN APPROVED

Final prohibited-hazard rule:
UNRESOLVED

Replanning:
NOT STARTED

No-path handling:
NOT STARTED
```

---

# 19. CURRENT SAFETY STATE

```text
Safety module:
NOT STARTED

Out-of-bounds rejection:
PLANNED

Blocked-cell rejection:
PLANNED

Invalid-action rejection:
PLANNED

Pause movement blocking:
PLANNED

Emergency-stop movement blocking:
PLANNED

Prohibited-hazard rejection:
POLICY UNRESOLVED

Safety logging:
PLANNED

Safety bypass prevention:
PLANNED
```

No simulated safety claim is authorized until these behaviors are implemented and tested.

---

# 20. CURRENT INTEGRATION STATE

```text
EEG loader → preprocessing / epochs:
PASS for the accepted M1-T03 path

Preprocessing / epochs → split manifest:
NOT STARTED / NOT AUTHORIZED

Split manifest → decoder:
NOT STARTED

Decoder → calibration:
NOT STARTED

Calibration → goal evidence:
BLOCKED

Goal evidence → Bayes:
NOT STARTED

Bayes → entropy:
NOT STARTED

Entropy → shared autonomy:
NOT STARTED

Shared autonomy → approved goal:
NOT STARTED

Approved goal → planner:
NOT STARTED

Planner → safety:
NOT STARTED

Safety → environment:
NOT STARTED

Offline EEG replay → full system:
NOT STARTED
```

---

# 21. CURRENT EXPERIMENT STATE

```text
E1 — EEG decoding:
NOT STARTED

E2 — Calibration:
NOT STARTED

E3 — Bayesian inference:
NOT STARTED

E4 — Uncertainty / Shared Autonomy:
NOT STARTED

E5 — Planning / Safety:
NOT STARTED

E6 — A/B/C/D system comparison:
BLOCKED

E7 — Robustness / Ablations:
BLOCKED

E8 — Cross-subject evaluation:
PROTOCOL APPROVED / IMPLEMENTATION NOT STARTED

E9 — Adaptation:
BLOCKED
```

---

# 22. CURRENT RESULTS STATE

```text
EEG decoder results:
NONE

Calibration results:
NONE

Bayesian results:
NONE

Uncertainty results:
NONE

Shared-autonomy results:
NONE

Planning results:
NONE

Safety results:
NONE

A/B/C/D results:
NONE

Ablation results:
NONE

Robustness results:
NONE

Cross-subject results:
NONE

Adaptation results:
NONE
```

`23_RESULTS_AND_ANALYSIS.md` is currently an analysis framework only.

`24_DISCUSSION_AND_FINDINGS.md` is currently a discussion framework only.

No empirical performance conclusion is authorized.

---

# 23. CURRENT TESTING STATE

```text
Testing framework:
MANDATORY, exact package choice not yet frozen

Unit tests:
PASS

Integration tests:
NOT STARTED

Real-data smoke tests:
PASS

Leakage tests:
NOT STARTED

Calibration metric tests:
NOT STARTED

Bayesian analytical tests:
NOT STARTED

Entropy tests:
NOT STARTED

Environment tests:
NOT STARTED

Planner tests:
NOT STARTED

Safety tests:
NOT STARTED

Shared-autonomy tests:
NOT STARTED

Replay tests:
NOT STARTED

End-to-end tests:
NOT STARTED

Regression suite:
NOT STARTED
```

---

# 24. CURRENT VALID SOFTWARE ARTIFACTS

Only code-generated or experiment-generated artifacts belong here.

| Artifact ID | Type | Path | Task / Experiment | Validity | Commit | Notes |
|---|---|---|---|---|---|---|
| M1-T01-LOADER | Source + test | `src/eeg/loader.py`; `tests/test_loader.py` | M1-T01 | VALID | `9b241681dfc986f53f5f8c0fcf40a3e3cea496e7` | Accepted loader implementation; real subject 1 runs 4/8/12 verified |
| M1-T02-VISUALIZATION | Source + test + figures | `src/eeg/visualization.py`; `tests/test_visualization.py`; `results/figures/m1_t02_subject1/` | M1-T02 | VALID | `9b241681dfc986f53f5f8c0fcf40a3e3cea496e7` | Accepted inspection implementation; subject 1 runs 4/8/12 verified with traces, PSD, sensors, and annotations |

Documentation files are not software result artifacts.

---

# 25. CURRENT MODEL ARTIFACTS

| Model ID | Model | Dataset / Split | Checkpoint | Evaluation | Commit | Notes |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | No trained models yet |

---

# 26. CURRENT VALID EXPERIMENTS

| Experiment ID | Purpose | Status | Artifact | Commit | Notes |
|---|---|---|---|---|---|
| — | — | — | — | — | No experiments executed yet |

---

# 27. INVALID / SUPERSEDED EXPERIMENTS

Do not delete invalid history.

Template:

| Experiment ID | Reason Invalid / Superseded | Evidence | Action |
|---|---|---|---|
| — | — | — | — |

Possible invalidation reasons:

```text
subject leakage
trial leakage
test-set tuning
wrong T1/T2 mapping
wrong class order
calibration leakage
wrong configuration
unreproducible run
scientifically invalid likelihood
```

---

# 28. CURRENT MANUAL VERIFICATION QUEUE

Completed loader/inspection verification:

```text
[x] Load real PhysioNet EEG through MNE
[x] Verify configured subject
[x] Verify runs 4 / 8 / 12
[x] Verify 64 channels
[x] Verify 160 Hz
[x] Verify plausible duration
[x] Inspect annotations
[x] Verify T0 / T1 / T2 semantics
[x] Inspect standardized channel names
[x] Verify montage attachment
[x] Visually confirm montage plausibility
[x] Generate raw-trace inspection output
[x] Generate PSD inspection output
[x] Generate sensor/montage inspection output
[x] Generate annotation-overview inspection output
```

Next governance gate:

```text
[ ] Reconcile docs/06, docs/08, and docs/15 with D-031 through D-039
[ ] Review and merge documentation-only reconciliation
[ ] Approve a new M1-T03 CURRENT_TASK.md implementation ticket
```

---

# 29. CURRENT RISKS

| Risk | Severity | Mitigation | Owner | Status |
|---|---|---|---|---|
| Scientific parameter guessed by Codex | High | `AGENTS.md` stop conditions + `DECISIONS.md` | ChatGPT / Project Owner | Active |
| Binary EEG → multi-goal mapping unresolved | High | Keep Goal-Evidence Adapter blocked | ChatGPT / Project Owner | Active |
| Invalid probability semantics in Bayes | High | Require explicit likelihood model | ChatGPT / Project Owner | Active |
| Data leakage | High | Split manifests + automated leakage tests | Codex / ChatGPT Review | Active |
| Test-set tuning | High | Protect final test split | All | Active |
| Scope drift | Medium | Narrow `CURRENT_TASK.md` tickets | All | Active |
| AI-generated code accepted without review | High | Run tests + independent review | Project Owner / ChatGPT | Active |
| Documentation/code drift | Medium | Update state and decisions after acceptance | All | Active |

---

# 30. CURRENT TECHNICAL DEBT

Current state:

```text
No material software technical debt recorded for merged M1-T01 / M1-T02.
Documentation alignment for D-031 through D-039 is an active governance blocker, not software debt.
```

Only actual implementation debt belongs here.

Examples later may include:

```text
temporary path handling
missing manifest
weak test coverage
duplicated helper
unfinished migration
```

Unresolved methodology is not technical debt.

---

# 31. CURRENT SCIENTIFIC DEBT

Use this section only for methodology that has been intentionally deferred but must be resolved before final experiments.

Current scientific-decision backlog:

```text
- calibration method freeze
- goal-selection protocol
- Bayesian likelihood semantics
- shared-autonomy thresholds
- adaptation mechanism
- risk model / λ
- final A/B/C/D definitions
- final statistics plan
```

Initial M1 preprocessing parameters are no longer in the scientific-decision backlog; they are approved as D-031 through D-039.

---

# 32. RECENT ACCEPTED DOCUMENTATION WORK

Most recent completed documentation/governance artifacts:

```text
22_AI_DEVELOPMENT_WORKFLOW.md
    Regenerated for ChatGPT + Project Owner + Codex + Git/GitHub

AGENTS.md
    Codex repository instruction authority

23_RESULTS_AND_ANALYSIS.md
    Pre-results analysis framework

24_DISCUSSION_AND_FINDINGS.md
    Pre-results scientific discussion framework

DECISIONS.md
    D-031 through D-039 record the approved initial M1 preprocessing/epoching parameters

PROJECT_STATE.md
    Live state reconciled to those approvals while preserving the implementation gate
```

These are documentation milestones, not software milestones.

---

# 33. NEXT NUMBERED DOCUMENT

Current planned next numbered scientific document:

```text
25_FUTURE_WORK.md
```

This should remain separate from implementation state.

Future-work items must not automatically become approved core scope.

---

# 34. CURRENT CLAIM STATUS

Currently authorized:

```text
- project architecture is designed
- scientific methodology is specified
- dataset and core algorithms are selected
- initial M1 preprocessing parameters are approved
- evaluation framework is defined
- Codex governance is defined
```

Not yet authorized:

```text
- model performance claims
- calibration improvement claims
- Bayesian reliability improvement claims
- wrong-goal reduction claims
- task-success improvement claims
- safety improvement claims
- cross-subject generalization claims
- adaptation improvement claims
```

No experiments exist yet.

---

# 35. CURRENT PROJECT LIMITATIONS

Preserve:

```text
public prerecorded EEG
offline replay
binary motor imagery
no live EEG
no physical robot
no real human-subject study
simple 2D SAR simulation
simulated safety only
no clinical claims
no unrestricted thought decoding
```

These boundaries must remain visible as the project develops.

---

# 36. STATE UPDATE PROTOCOL

After each accepted Codex task:

1. update `Project Phase` if needed;
2. update `Current Milestone`;
3. update active module;
4. update the implementation matrix;
5. add verified components;
6. add/remove blockers;
7. record artifacts;
8. record latest accepted commit;
9. update manual checks;
10. update test status;
11. update next candidate task;
12. update `Last Updated`.

Also update this file after an approved scientific decision or major governance change, without rewriting unrelated historical sections unnecessarily.

---

# 37. WHEN NOT TO UPDATE THIS FILE

Do not update `PROJECT_STATE.md` merely because:

- ChatGPT suggested an approach;
- a method was researched;
- Codex generated code but did not run it;
- a test is planned;
- an experiment is planned;
- a future feature sounds useful;
- a parameter is being discussed.

This file tracks accepted current reality.

---

# 38. PASS RULE

A module may be marked:

```text
PASS
```

only when its current acceptance criteria have been satisfied.

Depending on module, this includes:

```text
implementation
tests
test execution
manual scientific checks
review
```

Code existence alone is not `PASS`.

---

# 39. BLOCKED RULE

Use:

```text
BLOCKED
```

when scientific, governance, or technical progress cannot continue validly.

Example:

```text
Module:
Goal-Evidence Adapter

Status:
BLOCKED

Reason:
Binary EEG-to-goal protocol and likelihood semantics unresolved.

Implementation:
Not authorized.
```

This is a correct state.

---

# 40. FAIL RULE

Use:

```text
FAIL
```

when implementation or verification contradicts requirements.

Example:

```text
Loader:
FAIL

Reason:
Expected EEGBCI T1/T2 semantics were not reproduced.

Action:
Do not proceed to preprocessing.
```

A failure must not be hidden by marking the task partial.

---

# 41. MINIMAL ACCEPTED-TASK UPDATE EXAMPLE

After the loader passes:

```text
Current Milestone:
M1 — EEG Data + CSP/LDA

Current Module:
1 — EEG Data Loader

Task Status:
PASS

Verified:
- configurable EEGBCI subject loading
- runs 4 / 8 / 12
- 64 channels
- 160 Hz
- annotations present
- standardized channel names
- montage manually verified

Tests:
PASS

Manual Verification:
PASS

Latest Accepted Commit:
<commit>

Next Candidate Task:
EEG visualization / inspection
```

Only write this after it really happens.

---

# 42. SCIENTIFIC-BLOCK UPDATE EXAMPLE

Historical example of how to represent an unresolved preprocessing gate:

```text
Current Module:
3 — EEG Preprocessing / Epochs

Status:
BLOCKED

Blocking decisions:
- filter band
- reference
- epoch interval
- artifact policy

Implementation:
No scientific preprocessing performed.

Next required action:
ChatGPT scientific review + Project Owner approval + DECISIONS.md update.
```

For the current state, those example preprocessing decisions are resolved as D-031 through D-039; the remaining M1-T03 gate is documentation reconciliation plus explicit implementation authorization.

---

# 43. EXPERIMENT UPDATE EXAMPLE

After a real reportable experiment:

```text
Experiment ID:
E1-CSP-001

Validity:
VALID

Git Commit:
<commit>

Subjects:
<ids>

Runs:
4, 8, 12

Split:
<manifest>

Artifacts:
<paths>

Metrics:
<actual values>

Added to:
EXPERIMENT_LOG.md

Result status:
Eligible for analysis
```

Never use placeholders as real experiment entries.

---

# 44. SOURCE-OF-TRUTH INTEGRITY RULES

`PROJECT_STATE.md` must never:

- fabricate implementation completion;
- fabricate test success;
- fabricate experiment metrics;
- convert a recommendation into a decision;
- hide an unresolved scientific issue;
- mark unverified code as `PASS`;
- silently change project architecture;
- silently resolve conflicts;
- claim a result from a smoke test;
- become stale after a major accepted change.

---

# 45. CURRENT PROJECT STATE SUMMARY

The project currently has three accepted and merged M1 software tasks on canonical `main`: M1-T01 (PhysioNet EEGBCI loader), M1-T02 (EEG visualization/inspection), and M1-T03 (EEG preprocessing/epochs). M1-T03 is accepted at commit `1af72b5deb9981f469a4394859aac49add65e2a7`; final review reported 9 targeted preprocessing/epoch tests and 10 loader regression tests passing, plus real subject 1 smoke checks on runs 4/8/12. Those smoke checks are implementation verification, not model-performance results.

The Project Owner approved U-010 through U-012, recorded as D-040 through D-042 at commit `ea00a631b60967cfece65b42e00e7b36c4efac7d`: separate within-subject and cross-subject evaluation tracks, deterministic class-stratified 60/20/20 within-subject splitting at original-trial level, fixed 70/15/15 subject-held-out primary cross-subject evaluation, and a seed-42 frozen subject manifest with 76/16/17 subjects when the full 109-subject cohort is eligible. The split/evaluation methodology is reconciled to those decisions. No dataset-splitting implementation is authorized yet; a separate narrow `CURRENT_TASK.md` ticket remains required. The project remains an offline prerecorded EEG system rather than live EEG.
