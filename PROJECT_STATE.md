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
Documentation Complete Enough for M1 Start

Current Milestone:
M1 — EEG Dataset / Loader / Epochs / CSP+LDA

Current Module:
1 — EEG Data Loader

Current Task ID:
M1-T01

Task Status:
NOT STARTED

Current Branch:
TBD

Latest Verified Commit:
None yet

Latest Valid Experiment:
None yet

Last Updated:
TBD

Updated By:
TBD
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

> **The project has completed enough repository and documentation setup to begin the first authorized implementation task, M1-T01. Scientific architecture, methodology, evaluation, testing, validity, literature, workflow, Codex governance, results framework, and discussion framework have been specified. Verified scientific implementation has not yet begun.**

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

## Generated ahead of sequence / now being replaced

```text
PROJECT_STATE.md
```

This document is the corrected Codex-aligned version.

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
M1-T01 — PhysioNet EEGBCI Data Loader
```

This is the current authorized task as defined by `CURRENT_TASK.md`.

---

# 7. NEXT CANDIDATE IMPLEMENTATION TASK

> **Read `MASTER_PROJECT_SPEC.md` first. We are starting Milestone 1 only. Implement a clean MNE-Python data loader for the PhysioNet EEGBCI motor-imagery dataset. Initially support configurable subject IDs and runs 4, 8 and 12. Requirements: download through MNE utilities; cache locally; load EDF files; standardize channel names; attach the appropriate montage; print subject, channel count, sampling frequency, duration and annotations; add basic validation/error handling; write unit tests where practical; do not implement preprocessing or modelling yet. After coding, tell me: (1) files created/modified, (2) installation requirements, (3) exact command to run, (4) expected output, (5) what I should manually check. Do not continue beyond the loader.**

This task is already recorded in `CURRENT_TASK.md` and is ready / not started.

---

# 8. IMPLEMENTATION STATUS MATRIX

| Module | Component | Status | Automated Tests | Manual Verification | Latest Artifact / Commit | Notes |
|---|---|---|---|---|---|---|
| 0 | Config / Infrastructure | NOT STARTED | No | No | — | M0 pending |
| 1 | EEG Data Loader | NOT STARTED | No | No | — | First implementation task |
| 2 | EEG Visualization / Inspection | NOT STARTED | No | No | — | After loader verification |
| 3 | EEG Preprocessing / Epochs | BLOCKED | No | No | — | Exact scientific parameters unresolved |
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
None.
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

```text
- exact band-pass filter
- EEG reference
- exact epoch interval
- baseline correction
- artifact-handling policy
- T0 policy
- exact channel reduction policy, if any
- resampling policy, if any
- processed-data format
```

## Evaluation

```text
- final train/validation/test protocol
- final cross-subject protocol
- exact held-out subject strategy
- final statistical-analysis policy
```

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
None observed yet because coding has not started.
```

Do not invent technical blockers before actual implementation.

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
UNRESOLVED / NOT YET SELECTED

Local dataset cache:
NOT VERIFIED

Real EEG successfully loaded:
NO

Channel names standardized:
NO

Montage attached:
NO

Montage manually verified:
NO

Annotations inspected:
NO

T0/T1/T2 manually verified:
NO
```

Update only after actual execution.

---

# 15. CURRENT EEG PIPELINE STATE

```text
Loader:
NOT STARTED

Dataset caching:
NOT STARTED

Channel standardization:
NOT STARTED

Montage:
NOT STARTED

Visualization:
NOT STARTED

Preprocessing:
BLOCKED

Event extraction:
NOT STARTED

Epoching:
BLOCKED

T0 handling:
UNRESOLVED

Train/validation/test split:
UNRESOLVED

Cross-subject split:
UNRESOLVED

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
EEG → preprocessing:
NOT STARTED

Preprocessing → decoder:
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
BLOCKED

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
NOT STARTED

Integration tests:
NOT STARTED

Real-data smoke tests:
NOT STARTED

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
| — | — | — | — | — | — | No implementation artifacts yet |

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

First implementation-stage queue:

```text
[ ] Load real PhysioNet EEG through MNE
[ ] Verify configured subject
[ ] Verify runs 4 / 8 / 12
[ ] Verify 64 channels
[ ] Verify 160 Hz
[ ] Verify plausible duration
[ ] Inspect annotations
[ ] Verify T0 / T1 / T2 semantics
[ ] Inspect standardized channel names
[ ] Verify montage attachment
[ ] Visually confirm montage plausibility
```

Do not continue to preprocessing before the loader verification gate passes.

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
None yet — implementation has not started.
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
- preprocessing freeze
- split protocol freeze
- calibration method freeze
- goal-selection protocol
- Bayesian likelihood semantics
- shared-autonomy thresholds
- adaptation mechanism
- risk model / λ
- final A/B/C/D definitions
- final statistics plan
```

These remain explicit blockers, not hidden defaults.

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

PROJECT_STATE.md
    This Codex-aligned live project-state record
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

Do not rewrite unrelated historical sections unnecessarily.

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

when scientific or technical progress cannot continue validly.

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

At the time of this Codex-aligned rewrite, the project has a mature scientific and engineering specification but **no verified software implementation or empirical results yet**. The project architecture, Search & Rescue scenario, EEG dataset, neuroscience foundations, EEG/ML pipeline, calibration, Bayesian inference, uncertainty, adaptation boundaries, shared autonomy, planning, safety, implementation blueprint, repository architecture, experiments, metrics, testing, ethics/validity, literature foundation, AI-assisted development workflow, results framework, and discussion framework have been documented. The implementation workflow is now explicitly **ChatGPT + Project Owner + Codex + Git/GitHub**, with `AGENTS.md` serving as Codex's repository-level instruction authority. The correct first coding task remains the MNE-Python PhysioNet EEGBCI loader for configurable subjects and runs 4, 8, and 12. Several scientific decisions intentionally remain unresolved and must block downstream implementation rather than being guessed.
