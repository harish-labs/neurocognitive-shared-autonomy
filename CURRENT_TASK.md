# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex  
**Current status:** ACTIVE  
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / CSP+LDA  
**Task ID:** M1-T05  
**Task title:** CSP+LDA Baseline  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch verified:** `main`  
**Canonical main commit verified:** `70dfdfa0290327f01286a59066bac57ad9c1af09`  
**Task branch:** `task/m1-t05-csp-lda-baseline`  
**Authorization basis:** Project Owner explicit approval of M1-T05 implementation after accepted M1-T04 merge and D-043 approval  
**Authorized on:** 2026-08-31

---

# 1. TASK AUTHORIZATION

This file authorizes exactly one active Codex implementation ticket:

```text
M1-T05 — CSP+LDA Baseline
```

This authorization is limited strictly to the approved classical CSP+LDA baseline operating on the already approved M1-T03 epochs and the accepted M1-T04 split manifests.

Completed, scientifically reviewed, accepted, and merged on canonical `main` before this ticket:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
```

Verified before activation:

- `MASTER_PROJECT_SPEC.md`
- `CURRENT_TASK.md`
- `PROJECT_STATE.md`
- `DECISIONS.md`
- `AGENTS.md`
- `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`
- `docs/17_EXPERIMENTAL_DESIGN.md`
- `docs/18_METRICS_AND_EVALUATION.md`
- accepted M1-T03 and M1-T04 source/tests on canonical `main`

---

# 2. READ FIRST

Codex must read, in this order:

```text
1. MASTER_PROJECT_SPEC.md
2. CURRENT_TASK.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. AGENTS.md
6. docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md
7. docs/17_EXPERIMENTAL_DESIGN.md
8. docs/18_METRICS_AND_EVALUATION.md
9. src/eeg/epochs.py
10. src/eeg/splits.py
11. accepted M1-T03/M1-T04 tests
```

If any required file conflicts with `MASTER_PROJECT_SPEC.md` or an approved Project Owner decision:

```text
STOP
STATUS = BLOCKED
REPORT THE CONFLICT
```

---

# 3. MODULE

```text
Module 4 — CSP+LDA Baseline
```

Primary objective:

> Implement the smallest leakage-safe CSP+LDA baseline module that consumes approved epochs plus accepted M1-T04 partition manifests and exposes probability outputs without fitting or tuning on protected test data.

---

# 4. GOVERNING DECISIONS

This task is governed by:

```text
D-033 — canonical epoch -1.0 s to +4.0 s; CSP crop +1.0 s to +2.0 s only for the CSP stage
D-040 — separate within-subject and cross-subject evaluation tracks
D-041 — primary cross-subject protocol is subject-held-out
D-042 — fixed seed-42 protected final-test subject strategy
D-043 — final CSP configuration
```

Approved CSP configuration for this task:

```text
- retain all 64 channels
- crop canonical epochs to +1.0 s to +2.0 s for CSP only
- evaluate CSP n_components in {2,4,6,8}
- default candidate is 4
- use log-variance CSP features
- use primary covariance regularization reg=None
- use standard LDA with probability output
- fit CSP and LDA only on training partitions
- choose n_components using validation performance only
- protected test partition must not influence fitting or tuning
```

---

# 5. ALLOWED FILES

Codex may modify or create only the smallest set of files required for this task, expected to be limited to:

```text
src/models/csp_lda.py
tests/test_csp_lda.py
CURRENT_TASK.md
```

If a minimal supporting edit is truly required in another file to complete this task validly:

```text
STOP
→ explain why
→ propose the smallest additional file change
→ wait for approval
```

---

# 6. FORBIDDEN SCOPE

Do not implement or modify:

```text
src/models/eegnet.py
src/models/calibration.py
src/models/inference.py
src/cognition/*
src/autonomy/*
src/app/*
src/eeg/preprocessing.py
src/eeg/epochs.py
src/eeg/splits.py
PROJECT_STATE.md
DECISIONS.md
MASTER_PROJECT_SPEC.md
```

Do not implement any of the following in M1-T05:

```text
EEGNet / compact CNN
probability calibration
Bayesian goal inference
goal mapping
shared autonomy
safety controller
A* planner
adaptation
end-to-end replay integration
later experiment modules
```

Do not fit on validation data or final test data.
Do not use test or final-test performance to choose `n_components`.
Do not merge branches in this task.

---

# 7. REQUIRED BEHAVIOR

Required behavior:

```text
1. Consume canonical M1-T03 binary left/right epochs.
2. Operate on accepted M1-T04 partition assignments.
3. Keep within-subject and cross-subject evaluation paths separate.
4. Apply the +1.0 s to +2.0 s crop only inside the CSP path.
5. Preserve all 64 channels.
6. Fit CSP only on the training partition for each run.
7. Fit LDA only on CSP features from the training partition.
8. Evaluate candidate n_components using validation partitions only.
9. Keep protected test/final-test partitions isolated from fitting and selection.
10. Expose deterministic `predict` and `predict_proba`.
11. Preserve stable class-order reporting.
```

---

# 8. TESTS

Codex must add targeted automated tests where practical.

Required coverage includes:

```text
- leakage safety
- training-only fitting
- CSP crop use
- candidate search over {2,4,6,8}
- deterministic selection behavior
- probability outputs and class order
- protected test isolation
- compatibility with accepted split-manifest outputs
```

Testing rule:

```text
run targeted CSP/LDA tests
+
run relevant M1-T03/M1-T04 regressions
```

---

# 9. MANUAL / SCIENTIFIC CHECKS

If feasible, Codex should smoke-check the implemented CSP+LDA baseline on real cached subject 1 runs 4, 8, and 12 using the accepted within-subject split manifest.

Manual/scientific checks should include:

```text
- crop window is exactly +1.0 s to +2.0 s in the CSP path
- only training trials are used for fitting
- validation-only selection chooses one approved candidate
- probability outputs are well-formed
- the protected test partition remains untouched during fitting/selection
```

If cross-subject real-data smoke verification is not justified within this task, report that honestly.

---

# 10. ACCEPTANCE CRITERIA

M1-T05 may be reported as implementation-complete only if all of the following are true:

```text
- the CSP+LDA baseline is implemented within scope
- no later module was implemented
- targeted tests were added
- targeted tests were executed
- relevant M1-T03/M1-T04 regressions were executed
- real-data smoke verification is reported accurately
- branch is committed and pushed
- work stops for scientific/code review
```

After meeting the criteria:

```text
STOP
WAIT FOR SCIENTIFIC / REVIEWER ACCEPTANCE
DO NOT MERGE
```
