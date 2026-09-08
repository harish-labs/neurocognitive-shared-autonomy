# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Last updated:** 2026-09-08

---

# 1. STATUS AT A GLANCE

```text
Project phase:
M1-T01 through M1-T10 accepted and merged.
M4-T01 through M4-T05 accepted and merged.
M5-T01 through M5-T04 accepted and merged.
PRE-M6-R01 through PRE-M6-R06 accepted and merged.
PRE-M6-R07A — Master Authority Reconciliation: PASS / ACCEPTED / MERGED.
PRE-M6-R07B — Secondary Documentation Reconciliation: PASS / ACCEPTED / MERGED.
Final Pre-M6 audit: PASS / CLOSED.
M6-T01: PASS / ACCEPTED / MERGED / CLOSED.
M6-T02: PASS / ACCEPTED / MERGED / CLOSED.
M6-R01: PASS / ACCEPTED / MERGED / CLOSED.

Current module:
M6-T03 - Calibrated EEG Evidence -> Bayesian Decision Episode

Current task:
M6-T03

Task status:
AUTHORIZED / IMPLEMENTED CANDIDATE / BLOCKED PENDING CI VERIFICATION

Canonical branch:
main

M6-T03 reviewed candidate:
fe35d8de5966a439fbde5b999bd35deedf82f7ff

M6-T03 merge authorization:
NO

M6-R01 accepted candidate:
9030350dcd5a2d210ddd284c498c97027589c11e

M6-R01 software merge:
a0dc2ebc8d4d7ad5ecdcd99449602afd701c05a9

Verification workflow:
.github/workflows/verify.yml

Latest approved scientific/architectural decision register entry:
D-076 — M6 Decoder/Calibrator Runtime Injection Contract

Latest valid reportable experiment:
None yet
```

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, certified safety, human-subject result, or end-to-end EEG-driven mission-execution claim is authorized.

D-074 approves deterministic, auditable offline replay evidence semantics: one accepted prerecorded EEG epoch/trial produces one decoder evidence observation, and a Bayesian decision episode may consume up to five accepted observations under the approved Bayesian policy. D-075 preserves canonical accepted `mne.Epochs` as the authoritative decoder structural source. D-076 requires already-instantiated, already-fitted decoder/calibrator objects and forbids loading, fitting, tuning, selection, or persistence inside M6-T02.

M6-T03 is AUTHORIZED and has reviewed candidate `fe35d8de5966a439fbde5b999bd35deedf82f7ff`. Code review is satisfactory after terminal-iterator remediation, but acceptance remains BLOCKED until the required tests execute successfully. M6-T03 merge authorization remains NO.

M6-R01 — Reproducible Python Verification CI — is PASS / ACCEPTED / MERGED / CLOSED. It added only `.github/workflows/verify.yml` and established a repository-controlled GitHub Actions path for exact-ref verification in `ubuntu-latest` with Python 3.12 using the existing `requirements.txt` and full pytest suite. It introduced no scientific, source, test, or dependency changes.

---

# 2. ACCEPTED IMPLEMENTATION SEQUENCE

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
M1-T07 — Probability Calibration
M1-T08 — Bayesian Goal Inference
M1-T09 — Uncertainty / Shared-Autonomy Policy
M1-T10 — Adaptation / Prior Personalization
M4-T01 — 2D Search & Rescue Environment + Risk Map
M4-T02 — Risk-Aware A* Planner
M4-T03 — Safety Controller / Hard Constraint Enforcement
M4-T04 — Planner → Safety → Environment Execution Integration
M4-T05 — Controlled Replanning After Environment Change
M5-T01 — Human Command & Confirmation State Layer
M5-T02 — Shared-Autonomy / Human-Interaction Authorization Bridge
M5-T03 — Human-Authority-Aware Stepwise Navigation Runtime
M5-T04 — Stepwise Replacement-Snapshot Replanning Integration
PRE-M6-R01 — M4 Wrong-Terminal Route Protection
PRE-M6-R02 — Human OVERRIDE Symbolic Goal Identity Correction
PRE-M6-R03 — Environment Snapshot Immutability and Goal Registry Hardening
PRE-M6-R04 — Adaptation Disabled-State Mutation Correction
PRE-M6-R05 — Central Runtime Composition Configuration
PRE-M6-R06 — Accepted-Code Dependency Manifest Reconciliation
M6-T01 — Deterministic Offline EEG Epoch Replay
M6-T02 — Decoder and Calibration Runtime Adapter
M6-R01 — Reproducible Python Verification CI
```

M6-T03 is the sole active implementation task and remains blocked pending CI verification. M6-T04 is not authorized.

---

# 3. CURRENT ACCEPTED RUNTIME STATE

```text
EEG loader/preprocessing/splits: PASS
CSP+LDA baseline: PASS
EEGNet / compact CNN: PASS
Probability calibration: PASS
Bayesian goal inference: PASS
Uncertainty/shared-autonomy policy: PASS
Adaptation / prior personalization: PASS
2D SAR environment + risk-aware A*: PASS
Safety controller: PASS
Planner -> safety -> environment integration: PASS
Controlled replanning: PASS
Human command/confirmation state: PASS
Shared-autonomy -> human authorization bridge: PASS
Fresh authorization -> stepwise navigation runtime: PASS
Replacement-snapshot stepwise replanning: PASS
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
```

Accepted authority remains `STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > shared-autonomy policy`; safety retains veto before every environment transition. D-069 stepwise execution and D-070 replacement-snapshot replanning remain authoritative.

---

# 4. ACCEPTED VERIFICATION STATE

M5-T04 independent verification:

```text
focused -> 105 passed in 0.52s
adjacent -> 143 passed in 0.36s
full -> 281 passed, 1 warning in 26.83s
```

PRE-M6-R06 verification:

```text
installation from requirements.txt: PASS
full pytest suite: 327 passed, 1 warning
warning: pre-existing PyTorch convolution padding warning
```

M6-T02 accepted verification:

```text
focused M6-T02 tests: 24 passed
replay/CSP+LDA/EEGNet/calibration regressions: 40 passed, 1 known warning
full pytest: 361 passed, 1 known warning
git diff --check: PASS
```

M6-T03 verification state:

```text
reviewed candidate: fe35d8de5966a439fbde5b999bd35deedf82f7ff
code review: satisfactory after terminal-iterator remediation
runtime verification: BLOCKED PENDING CI
focused M6-T03 tests: NOT YET VERIFIED
M6-T02 regression: NOT YET VERIFIED FOR THIS CANDIDATE
Bayesian regression: NOT YET VERIFIED FOR THIS CANDIDATE
full pytest: NOT YET VERIFIED FOR THIS CANDIDATE
merge authorization: NO
```

M6-R01 verification infrastructure:

```text
status: PASS / ACCEPTED / MERGED / CLOSED
accepted candidate: 9030350dcd5a2d210ddd284c498c97027589c11e
software merge: a0dc2ebc8d4d7ad5ecdcd99449602afd701c05a9
workflow: .github/workflows/verify.yml
trigger: workflow_dispatch with required ref input
runner: ubuntu-latest
Python: 3.12
dependency install: requirements.txt
verification: full pytest + git diff --check
exact 40-character SHA integrity check: enabled
```

---

# 5. PRE-M6 GOVERNANCE STATUS

PRE-M6-R07A and PRE-M6-R07B are PASS / ACCEPTED / MERGED. Final Pre-M6 audit is PASS / CLOSED.

The genuinely unresolved experimental-analysis decisions remain:

```text
U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
```

---

# 6. CLAIM / SCOPE BOUNDARIES

Preserve at least:

```text
public prerecorded EEG / offline replay / simulated real-time BCI only
no live EEG or hardware claim
human determines WHAT; AI determines HOW
accepted binary EEG evidence semantics; no fabricated direct K-goal decoder
accepted calibration/Bayesian/uncertainty/shared-autonomy/adaptation semantics
fresh navigation authorization remains required
D-069 stepwise navigation remains authoritative
D-070 event-bounded replacement-snapshot replanning remains authoritative
safety veto remains mandatory before every environment transition
no UI, reportable experiments, hardware integration, or additional M6 implementation without separate authorization
```

---

# 7. NEXT ACTION

Use `.github/workflows/verify.yml` from canonical `main` to verify the exact M6-T03 candidate:

```text
fe35d8de5966a439fbde5b999bd35deedf82f7ff
```

Required acceptance evidence remains:

```text
focused M6-T03 tests
M6-T02/runtime-adapter regression
Bayesian regression
full pytest
git diff --check
```

If all required checks pass, stop for ChatGPT review before M6-T03 merge.

M6-T04 remains NOT STARTED / NOT AUTHORIZED. U-034, U-035, and U-036 remain unresolved.
