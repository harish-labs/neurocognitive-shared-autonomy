# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex  
**Current status:** READY / NOT STARTED  
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / CSP+LDA  
**Task ID:** M1-T01  
**Task title:** PhysioNet EEGBCI Data Loader  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`

---

# 1. TASK OBJECTIVE

Implement a clean, minimal MNE-Python loader for the PhysioNet EEG Motor Movement/Imagery Database.

Initial support:

```text
Configurable subject IDs
Runs 4, 8, 12
```

The task must stop at data loading and validation.

Do not implement preprocessing, epoching, CSP, LDA, EEGNet, calibration, Bayesian inference, autonomy, or UI.

---

# 2. READ FIRST

Codex must read, in this order:

```text
1. MASTER_PROJECT_SPEC.md
2. AGENTS.md
3. PROJECT_STATE.md
4. 06_DATASET_AND_DATA_PIPELINE.md
5. 16_REPOSITORY_AND_CODE_ARCHITECTURE.md
6. DECISIONS.md
```

If any required file conflicts with `MASTER_PROJECT_SPEC.md`, stop and report the conflict.

---

# 3. APPROVED DATASET

Dataset:

```text
PhysioNet EEG Motor Movement/Imagery Database
EEGMMIDB / EEGBCI
```

Access:

```text
MNE-Python
mne.datasets.eegbci.load_data
```

Initial runs:

```text
4
8
12
```

Expected run semantics:

```text
T0 = rest
T1 = imagined left fist
T2 = imagined right fist
```

Expected dataset characteristics:

```text
64 EEG channels
160 Hz
EDF+
```

Do not silently reinterpret T0/T1/T2.

---

# 4. ALLOWED FILES

Preferred files:

```text
src/eeg/loader.py
tests/test_loader.py
```

If repository bootstrapping is required, the minimum necessary supporting files may be proposed, but Codex must not silently expand scope.

Potentially acceptable with explicit necessity:

```text
src/eeg/__init__.py
src/__init__.py
requirements.txt
```

---

# 5. FORBIDDEN FILES / MODULES

Do not implement or modify scientific downstream modules in this task:

```text
src/eeg/preprocessing.py
src/eeg/epochs.py
src/models/*
src/cognition/*
src/autonomy/*
src/evaluation/*
src/app/*
```

Do not change:

```text
MASTER_PROJECT_SPEC.md
AGENTS.md
```

unless the Project Owner explicitly authorizes it.

---

# 6. REQUIREMENTS

The loader must:

1. accept configurable subject IDs;
2. support runs 4, 8, and 12 initially;
3. download through official MNE EEGBCI utilities;
4. rely on MNE-compatible local caching;
5. load EDF files;
6. standardize EEGBCI channel names using the supported MNE helper or equivalent;
7. attach an appropriate montage;
8. expose or print:
   - subject ID;
   - run IDs;
   - number of channels;
   - sampling frequency;
   - recording duration;
   - annotations;
9. provide basic input validation;
10. provide useful error messages;
11. preserve raw data semantics;
12. avoid modifying original source data;
13. write unit tests where practical.

---

# 7. MONTAGE RULE

The project requires an appropriate EEG montage.

The exact montage name is not scientifically locked in the project specification.

Codex may use the standard MNE-compatible montage appropriate for EEGBCI only if it can justify it from MNE/PhysioNet conventions.

If there is ambiguity:

```text
STOP
→ report the candidate montage(s)
→ explain why
→ request approval
```

Do not silently invent electrode locations.

---

# 8. OUT OF SCOPE

Do not implement:

```text
filtering
re-referencing
artifact rejection
baseline correction
resampling
epoching
T0 removal
class encoding
train/test split
CSP
LDA
EEGNet
calibration
Bayesian inference
entropy
shared autonomy
planning
safety
Streamlit
```

---

# 9. SCIENTIFIC CONSTRAINTS

Preserve:

```text
Runs 4 / 8 / 12
T0 / T1 / T2 annotations
original 160 Hz sampling rate
all expected EEG channels
subject/run provenance
```

The loader must not make downstream scientific decisions.

---

# 10. TEST REQUIREMENTS

Where practical, tests should cover:

```text
valid subject input
valid run input
invalid subject/run handling
returned MNE Raw object(s)
non-zero duration
expected sampling frequency
presence of annotations
channel-name standardization
montage availability
```

Network-dependent tests should be clearly separated or marked appropriately.

Do not claim tests passed unless actually executed.

---

# 11. MANUAL VERIFICATION CHECKLIST

After Codex completes the implementation, the Project Owner should manually verify:

```text
[ ] Correct subject loaded
[ ] Runs 4 / 8 / 12 loaded
[ ] 64 EEG channels are present
[ ] Sampling frequency is 160 Hz
[ ] Recording duration is plausible
[ ] T0 / T1 / T2 annotations are visible
[ ] Channel names are standardized
[ ] Montage is attached correctly
[ ] No preprocessing has been applied
```

Do not proceed to preprocessing until this check passes.

---

# 12. ACCEPTANCE CRITERIA

Task status may be `PASS` only if:

```text
loader implemented
+
tests added where practical
+
tests actually run
+
real EEG loading demonstrated
+
required metadata printed/reported
+
manual verification checklist identified
+
no downstream scope added
```

---

# 13. STOP CONDITIONS

Stop and report `BLOCKED` if:

- EEGBCI data cannot be retrieved through MNE;
- channel standardization fails;
- montage choice is scientifically ambiguous;
- dataset semantics conflict with project documentation;
- required implementation would modify forbidden modules;
- dependency or environment problems prevent verification.

---

# 14. COMPLETION REPORT FORMAT

Codex must report:

```text
Status:
Files created:
Files modified:
Implementation completed:
Tests added:
Tests executed:
Test results:
Exact installation command:
Exact run command:
Expected output:
Artifacts / cache paths:
Manual checks:
Known limitations:
Open blockers:
Suggested Git commit message:
```

---

# 15. DO NOT CONTINUE

After this loader task is complete:

```text
STOP
```

Do not begin preprocessing or any later module until a new `CURRENT_TASK.md` is approved.
