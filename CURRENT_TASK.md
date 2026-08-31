# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex  
**Current status:** ACTIVE  
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / EEGNet  
**Task ID:** M1-T06  
**Task title:** EEGNet / Compact CNN  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch verified:** `main`  
**Canonical main commit verified:** `792843762b82c030dbdce568f7b4c93ceeebac7d`  
**Task branch:** `task/m1-t06-eegnet-compact-cnn`  
**Authorization basis:** Project Owner explicit approval of M1-T06 implementation after D-045, D-046, and D-047  
**Authorized on:** 2026-08-31

---

# 1. TASK AUTHORIZATION

This file authorizes exactly one active Codex implementation ticket:

```text
M1-T06 — EEGNet / Compact CNN
```

This authorization is limited strictly to the approved EEGNet / compact CNN model, training, inference, targeted tests, and a bounded real-data smoke verification using the already accepted M1-T03 epochs and M1-T04 split semantics.

Completed, scientifically reviewed, accepted, and merged on canonical `main` before this ticket:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
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
- accepted M1-T03 through M1-T05 source/tests on canonical `main`

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
11. src/models/csp_lda.py
12. accepted M1-T03/M1-T04/M1-T05 tests
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
Module 5 — EEGNet / Compact CNN
```

Primary objective:

> Implement the smallest leakage-safe EEGNet / compact CNN model, training, and inference module that consumes approved epochs plus accepted partition assignments and exposes stable class probabilities without using protected test data for fitting, tuning, or checkpoint selection.

---

# 4. GOVERNING DECISIONS

This task is governed by:

```text
D-040 — separate within-subject and cross-subject evaluation tracks
D-041 — primary cross-subject protocol is subject-held-out
D-042 — fixed seed-42 protected final-test subject strategy
D-045 — final EEGNet architecture
D-046 — final EEGNet training hyperparameters
D-047 — EEGNet pooling and depthwise max-norm supplement
```

Approved EEGNet architecture and training for this task:

```text
- input batch × 1 × 64 × time
- all 64 channels
- native 160 Hz
- full canonical -1.0 s to +4.0 s epoch
- no CSP-only +1.0 s to +2.0 s crop
- F1 = 8
- temporal kernel length 64 with same padding
- no bias before BatchNorm
- depthwise spatial convolution across all 64 channels
- depth multiplier D = 2
- max-norm depthwise constraint where supported
- BatchNorm + ELU + average pooling
- separable convolution with F2 = 16 and temporal kernel 16
- BatchNorm + ELU + average pooling
- dropout 0.5
- flatten + dense 2 logits
- explicit class order ("left", "right")
- softmax probability output
- two-class cross-entropy
- Adam, lr 1e-3, weight_decay 0
- batch size 32
- maximum 200 epochs
- early stopping patience 20
- checkpoint selection by validation balanced accuracy
- earliest checkpoint wins exact validation balanced-accuracy ties
- random seed 42
- shuffle training partition only
- no class weighting or learning-rate scheduler
- no extra normalization, augmentation, channel selection, resampling, or filtering
- test/final-test never influence fitting, tuning, selection, or early stopping
```

---

# 5. ALLOWED FILES

Codex may modify or create only the smallest set of files required for this task, expected to be limited to:

```text
src/models/eegnet.py
tests/test_eegnet.py
CURRENT_TASK.md
requirements.txt
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
src/models/calibration.py
src/models/inference.py
src/cognition/*
src/autonomy/*
src/app/*
src/eeg/preprocessing.py
src/eeg/epochs.py
src/eeg/splits.py
src/models/csp_lda.py
PROJECT_STATE.md
DECISIONS.md
MASTER_PROJECT_SPEC.md
```

Do not implement any of the following in M1-T06:

```text
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

Do not use CSP crop logic in EEGNet.
Do not use test or final-test data for model selection.
Do not merge branches in this task.

---

# 7. REQUIRED BEHAVIOR

Required behavior:

```text
1. Consume canonical M1-T03 binary left/right epochs.
2. Operate on accepted M1-T04 partition assignments.
3. Keep within-subject and cross-subject evaluation paths separate.
4. Preserve full canonical -1.0 s to +4.0 s EEGNet input epochs.
5. Preserve all 64 channels and native 160 Hz.
6. Fit EEGNet only on the training partition.
7. Use validation only for early stopping and checkpoint selection.
8. Select the checkpoint by validation balanced accuracy, earliest on exact ties.
9. Keep protected test/final-test partitions isolated from fitting and selection.
10. Expose deterministic predict and softmax probability output with stable class order.
11. Use the same fixed architecture and training hyperparameters for both evaluation tracks.
```

---

# 8. TESTS

Codex must add targeted automated tests where practical.

Required coverage includes:

```text
- tensor/input shape contract
- full canonical epoch usage without CSP crop
- training-only fitting
- validation-only checkpoint selection
- earliest-checkpoint tie behavior
- protected test/final-test isolation
- explicit class order and softmax probability output
- compatibility with accepted within-subject and cross-subject partition assignments
```

Testing rule:

```text
run targeted EEGNet tests
+
run relevant M1-T03/M1-T04 regressions
```

---

# 9. MANUAL / SCIENTIFIC CHECKS

If feasible, Codex should smoke-check the implemented EEGNet path on real cached subject 1 runs 4, 8, and 12 using the accepted within-subject split manifest.

Manual/scientific checks should include:

```text
- full canonical epoch length is preserved
- training uses only the train partition
- validation-only checkpoint selection runs
- test partition is evaluated only after checkpoint freeze
- probabilities are well-formed and class order is explicit
```

If cross-subject real-data smoke verification is not justified within this task, report that honestly.

---

# 10. ACCEPTANCE CRITERIA

M1-T06 may be reported as implementation-complete only if all of the following are true:

```text
- the EEGNet / compact CNN baseline is implemented within scope
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
