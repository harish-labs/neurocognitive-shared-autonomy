# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex  
**Current status:** ACTIVE  
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / CSP+LDA  
**Task ID:** M1-T03  
**Task title:** EEG Preprocessing & Epochs  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch verified:** `main`  
**Canonical main commit verified:** `b8ff7772efc43f75e8a863723b30fb717661e5cd`  
**Task branch:** `task/m1-t03-eeg-preprocessing-epochs`  
**Authorization basis:** Project Owner explicit approval of M1-T03 implementation, plus approved preprocessing decisions D-031 through D-039 in `DECISIONS.md`  
**Authorized on:** 2026-08-30

---

# 1. TASK AUTHORIZATION

This file now explicitly authorizes exactly one active Codex implementation ticket:

```text
M1-T03 — EEG Preprocessing & Epochs
```

This authorization is limited strictly to implementing the approved M1 preprocessing and epoching pipeline for the PhysioNet EEGBCI Left-vs-Right motor-imagery task using runs 4, 8, and 12.

This ticket does not authorize work on any later module.

Completed and merged on canonical `main` before this ticket:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
```

Latest verified canonical main commit at task activation:

```text
b8ff7772efc43f75e8a863723b30fb717661e5cd
Clarify M1-T03 governance commit labels (#8)
```

Verified before activation:

- `MASTER_PROJECT_SPEC.md`
- `CURRENT_TASK.md` previous blocked state
- `PROJECT_STATE.md`
- `DECISIONS.md`
- `AGENTS.md`
- `docs/06_DATASET_AND_DATA_PIPELINE.md`
- `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`
- `docs/15_IMPLEMENTATION_BLUEPRINT.md`
- `src/eeg/loader.py`
- `tests/test_loader.py`

Verification result:

- canonical `main` is consistent with approved decisions D-031 through D-039 for the M1 preprocessing/epoching scope;
- the methodology documents already reflect those approved decisions;
- loader and loader tests remain consistent with the approved dataset/run/channel/montage assumptions;
- downstream scientific decisions remain unresolved and therefore out of scope.

---

# 2. READ FIRST

Codex must read, in this order:

```text
1. MASTER_PROJECT_SPEC.md
2. AGENTS.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. docs/06_DATASET_AND_DATA_PIPELINE.md
6. docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md
7. docs/15_IMPLEMENTATION_BLUEPRINT.md
8. src/eeg/loader.py
9. tests/test_loader.py
```

If any required file conflicts with `MASTER_PROJECT_SPEC.md`, the explicit Project Owner approval, or D-031 through D-039:

```text
STOP
STATUS = BLOCKED
REPORT THE CONFLICT
```

---

# 3. MODULE

```text
Module 3 — EEG Preprocessing / Epochs
```

Primary objective:

> Implement the approved M1 preprocessing and epoching pipeline that converts validated continuous EEGBCI runs 4, 8, and 12 into canonical Left/Right motor-imagery MNE Epochs with preserved provenance and auditable rejection logging.

---

# 4. ALLOWED FILES

Codex may modify or create only the smallest set of files required for this task, expected to be limited to:

```text
src/eeg/preprocessing.py
src/eeg/epochs.py
tests/test_preprocessing.py
tests/test_epochs.py
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

# 5. FORBIDDEN FILES / FORBIDDEN SCOPE

Do not implement or modify:

```text
src/models/csp_lda.py
src/models/eegnet.py
src/models/inference.py
src/models/calibration.py
src/cognition/*
src/autonomy/*
src/app/*
PROJECT_STATE.md
DECISIONS.md
MASTER_PROJECT_SPEC.md
```

Do not implement any of the following in M1-T03:

```text
CSP + LDA
Dataset splitting
Calibration
EEGNet / compact CNN
Bayesian goal inference
Goal mapping
Shared autonomy
Safety controller
A* planner
Replay integration
```

Do not resolve any later unresolved decision by code.

---

# 6. APPROVED SCIENTIFIC PARAMETERS — LOCKED FOR THIS TASK

Codex is authorized to implement exactly these approved parameters and no unapproved alternative:

```text
Band-pass filter: 7–30 Hz
EEG reference: average EEG reference
Canonical epoch window: -1.0 s to +4.0 s relative to cue onset
Baseline correction: None
ICA: forbidden
Automatic bad-channel interpolation: forbidden
Artifact rejection: reject epochs with EEG peak-to-peak amplitude >150 µV
Rejection accounting: required; log rejected epochs and reason/threshold
T0 handling: exclude from binary model epochs; preserve raw annotations/provenance
Channels: preserve all 64 validated EEG channels
Resampling: forbidden; preserve native 160 Hz
Canonical output: MNE Epochs
Persistence format when saved: MNE FIF using *-epo.fif naming
```

Important boundary:

```text
Initial CSP crop +1.0 s to +2.0 s is approved for the later CSP stage only.
Do not implement CSP cropping as a replacement for the canonical stored epoch in M1-T03.
```

---

# 7. REQUIRED BEHAVIOR

Codex must implement only what is necessary to satisfy this task.

Required behavior:

```text
1. Accept validated Raw EEG from the existing loader path.
2. Apply only the approved 7–30 Hz band-pass filtering.
3. Apply the approved average EEG reference explicitly.
4. Preserve all 64 validated EEG channels.
5. Preserve the native validated 160 Hz sampling rate.
6. Extract events from source annotations without changing raw annotation meaning.
7. Map T1 to left imagery and T2 to right imagery for runs 4/8/12.
8. Exclude T0 from the binary model epoch set while preserving raw provenance/annotation information.
9. Construct canonical cue-relative epochs from -1.0 s to +4.0 s.
10. Use baseline=None explicitly.
11. Reject epochs whose EEG peak-to-peak amplitude exceeds 150 µV.
12. Retain explicit rejection accounting with auditable metadata.
13. Validate epoch counts, labels, finite values, channel order, and metadata alignment.
14. Expose canonical processed output as MNE Epochs.
15. If persisted, save epochs using *-epo.fif naming.
```

Preserve provenance sufficient to identify at minimum:

```text
subject_id
run_id
source_file
event_code
semantic_label
event timing / trial identity where available
channel order
sampling frequency
preprocessing configuration used
rejection status / reason where applicable
```

---

# 8. TESTS

Codex must add targeted automated tests where practical.

Required test coverage includes:

```text
- preprocessing parameter validation
- no silent resampling
- channel order preservation
- event extraction / T1-T2 mapping for runs 4/8/12
- T0 excluded from binary epoch output
- canonical epoch timing
- baseline=None behavior is explicit
- rejection behavior for >150 µV peak-to-peak epochs
- rejection logging/accounting
- finite output data
- label and metadata alignment
```

Testing rule:

```text
run targeted tests for the new module(s)
+
run relevant regression tests for loader compatibility
```

Do not claim tests passed unless they were actually executed.

---

# 9. MANUAL / SCIENTIFIC CHECKS

If feasible, Codex should inspect real subject 1 runs 4, 8, and 12 after implementation and before claiming task completion.

Manual/scientific checks should include:

```text
- filtered signal plausibility
- event counts for T0 / T1 / T2
- left/right class counts after T0 exclusion
- epoch shape and timing plausibility
- preserved 64-channel order
- preserved 160 Hz sampling
- rejection counts and reasons
- no unexpected empty epoch set
```

If real-data inspection is not feasible in the current environment, report that honestly and stop short of claiming full scientific acceptance.

---

# 10. ACCEPTANCE CRITERIA

M1-T03 may be reported as complete only if all of the following are true:

```text
- approved preprocessing and epoching scope is implemented
- no later module was implemented
- targeted tests were added
- targeted tests were executed
- loader regression coverage was executed
- canonical output is MNE Epochs
- T0 is excluded from binary model epochs but preserved in raw provenance
- rejection logging is present
- no unapproved preprocessing step was introduced
- real-data inspection for subject 1 runs 4/8/12 was attempted and reported accurately
- any ambiguity or unresolved downstream decision is preserved rather than guessed
```

After meeting the criteria:

```text
STOP
WAIT FOR SCIENTIFIC / REVIEWER ACCEPTANCE
```

Do not merge automatically.

---

# 11. STOP CONDITIONS

Codex must stop and report `BLOCKED` if any of the following occurs:

```text
- a required scientific parameter appears ambiguous despite D-031 through D-039
- implementation requires changing files outside the allowed scope
- the real codebase conflicts with the approved T0/T1/T2 semantics
- loader assumptions about channels, montage, or sampling frequency do not hold in real data
- rejection/provenance requirements cannot be satisfied cleanly within the approved module boundaries
- any later unresolved decision becomes necessary to continue validly
```

Examples of unresolved later decisions that remain blocked and must not be implemented here:

```text
- final train/validation/test protocol
- final CSP configuration
- EEGNet architecture/hyperparameters
- calibration method or fitting partition
- Bayesian likelihood semantics
- binary EEG-to-multi-goal mapping
- autonomy thresholds
```

---

# 12. DELIVERABLE REPORT FORMAT

After implementation, Codex must report:

```text
1. Task status: PASS / PARTIAL / BLOCKED / FAIL
2. Files created
3. Files modified
4. Exact implementation completed
5. Tests added
6. Tests executed
7. Test results
8. Exact commands used
9. Output files / artifacts created
10. Manual checks performed
11. Known limitations
12. Open blockers
13. Suggested Git commit message
```

---

# 13. DO NOT CONTINUE

Once M1-T03 is implemented, tested, and reviewed for this task:

```text
STOP
```

Do not proceed to CSP/LDA, dataset splitting, calibration, EEGNet, or any later module without a new explicit task ticket.
