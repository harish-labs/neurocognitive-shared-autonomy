# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex  
**Current status:** ACTIVE  
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / CSP+LDA  
**Task ID:** M1-T04  
**Task title:** EEG Split Manifest  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch verified:** `main`  
**Canonical main commit verified:** `52448319cfac9948c9c94f7a33de425b3d22b5b4`  
**Task branch:** `task/m1-t04-eeg-split-manifest`  
**Authorization basis:** Project Owner explicit approval of M1-T04 implementation plus D-040 through D-042 in `DECISIONS.md`  
**Authorized on:** 2026-08-31

---

# 1. TASK AUTHORIZATION

This file explicitly authorizes exactly one active implementation ticket:

```text
M1-T04 — EEG Split Manifest
```

Completed, scientifically reviewed, and merged before this ticket:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
```

This ticket is limited to implementing leakage-safe split-manifest utilities required to operationalize D-040, D-041, and D-042.

Do not implement CSP/LDA, EEGNet, calibration, Bayesian inference, shared autonomy, planning, safety, replay integration, or experiments in this ticket.

---

# 2. READ FIRST

Codex must read, in this order:

```text
1. MASTER_PROJECT_SPEC.md
2. CURRENT_TASK.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. AGENTS.md
6. docs/06_DATASET_AND_DATA_PIPELINE.md
7. docs/17_EXPERIMENTAL_DESIGN.md
8. docs/18_METRICS_AND_EVALUATION.md
9. accepted M1-T03 preprocessing/epoching source and tests
```

If any required file conflicts with `MASTER_PROJECT_SPEC.md`, the explicit Project Owner approval, or D-040 through D-042:

```text
STOP
STATUS = BLOCKED
REPORT THE CONFLICT
```

---

# 3. APPROVED SPLIT CONTRACT — LOCKED

Implement exactly the approved split/evaluation contract.

## Within-subject

```text
60% train
20% validation
20% test
```

Rules:

- deterministic;
- class-stratified;
- grouping unit is the original trial;
- no original trial or any derived window from that trial may cross partitions;
- if retained class counts cannot support the approved stratified split, report the condition and stop rather than silently substituting another scientific rule.

## Cross-subject

Primary protocol:

```text
70% train subjects
15% validation subjects
15% final test subjects
```

Rules:

- each subject belongs to exactly one partition;
- no trial from a validation or final-test subject may appear in training;
- subject assignment uses one deterministic shuffle with fixed seed 42;
- freeze the resulting subject IDs in a versioned split manifest before model fitting;
- for a full eligible EEGBCI cohort of 109 subjects, use exactly 76 train / 16 validation / 17 final-test subjects;
- every trial from a subject stays in that subject partition;
- final-test subjects must not be used for CSP fitting, EEGNet training, hyperparameter selection, calibration fitting, threshold tuning, or learned adaptation;
- if preprocessing/QC produces an eligible subject cohort size other than 109, STOP and report the eligible count for reviewer decision. Do not invent another allocation rule.

Within-subject and cross-subject protocols/results must remain explicitly separate.

---

# 4. IMPLEMENTATION SCOPE

Implement the smallest module(s) necessary to:

```text
- build deterministic within-subject partition assignments from accepted trial metadata;
- build the approved deterministic 109-subject cross-subject assignment;
- persist/reload a versioned split manifest in a transparent repository-compatible format;
- preserve subject IDs, trial IDs, labels, partition names, seed, protocol/version information, and provenance sufficient for leakage auditing;
- validate partition disjointness and completeness;
- detect original-trial / derived-window leakage;
- expose protected final-test membership so later model code cannot accidentally fit on final-test subjects/trials;
- reproduce an identical manifest from identical eligible inputs and approved seed.
```

The implementation must consume accepted M1-T03 metadata/contracts rather than redefining EEG semantics.

---

# 5. FORBIDDEN SCOPE

Do not implement or resolve:

```text
U-013 — Final CSP configuration
U-014 — Final EEGNet architecture details
U-015 — Final training hyperparameters
U-016/U-017/U-018 — Calibration choices
U-019 onward — Bayesian, shared-autonomy, adaptation, planning/safety, and experimental-analysis decisions
```

Do not train models or produce performance claims in M1-T04.

---

# 6. REQUIRED TESTS

Add targeted automated tests covering at minimum:

```text
- deterministic within-subject splits;
- class stratification;
- approved 60/20/20 behavior where mathematically supported;
- original-trial grouping and derived-window leakage prevention;
- deterministic seed-42 cross-subject assignment;
- exact 76/16/17 subject counts for a 109-subject eligible cohort;
- subject disjointness and completeness;
- every trial follows its subject partition in cross-subject mode;
- final-test protection metadata/contract;
- manifest persistence and reproducible reload;
- manifest version/provenance fields;
- explicit failure for unsupported eligible cross-subject cohort sizes other than 109;
- relevant regression compatibility with accepted M1-T03 outputs.
```

Do not claim tests passed unless they were actually executed.

---

# 7. ACCEPTANCE CRITERIA

M1-T04 may be reported complete only if:

```text
- D-040/D-041/D-042 are implemented without reinterpretation;
- no later scientific decision is silently resolved;
- leakage checks are explicit and tested;
- manifests are deterministic and auditable;
- the 109-subject cross-subject manifest uses exactly 76/16/17 with seed 42;
- unsupported eligible cohort sizes stop for reviewer decision;
- targeted tests and relevant regression tests are executed and reported;
- no CSP/LDA or later model implementation is included.
```

After implementation, tests, and self-review:

```text
STOP
WAIT FOR CHATGPT SCIENTIFIC / CODE REVIEW
```

Do not merge automatically.

---

# 8. DELIVERABLE REPORT

Report:

```text
1. Task status: PASS / PARTIAL / BLOCKED / FAIL
2. Files created/modified
3. Exact split/manifest behavior implemented
4. Tests added
5. Tests executed and exact commands
6. Test results
7. Manifest/artifact examples generated, if any
8. Leakage checks performed
9. Known limitations
10. Open blockers
11. Suggested commit / PR message
```

Then stop.
