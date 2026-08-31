# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex  
**Current status:** ACTIVE  
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / Decoders / Calibration  
**Task ID:** M1-T07  
**Task title:** Probability Calibration  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch verified:** `main`  
**Canonical main commit verified:** `7b5f28095b3faa123bf942532a69e443847924a9`  
**Task branch:** `task/m1-t07-probability-calibration`  
**Authorization basis:** Project Owner explicit approval of M1-T07 implementation plus D-048 through D-050 in `DECISIONS.md`  
**Authorized on:** 2026-08-31

---

# 1. TASK AUTHORIZATION

This file explicitly authorizes exactly one active implementation ticket:

```text
M1-T07 — Probability Calibration
```

Completed, scientifically reviewed, accepted, and merged before this ticket:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
```

This ticket is limited to implementing the approved probability-calibration module under D-048, D-049, and D-050 only.

Do not implement Bayesian inference, entropy/shared-autonomy policy, adaptation, planning, safety, replay integration, or later experiments in this ticket.

---

# 2. READ FIRST

Codex must read, in this order:

```text
1. MASTER_PROJECT_SPEC.md
2. CURRENT_TASK.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. AGENTS.md
6. docs/09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md
7. docs/17_EXPERIMENTAL_DESIGN.md
8. docs/18_METRICS_AND_EVALUATION.md
9. accepted src/models/csp_lda.py
10. accepted src/models/eegnet.py
```

If any required file conflicts with `MASTER_PROJECT_SPEC.md`, the explicit Project Owner approval, or D-048 through D-050:

```text
STOP
STATUS = BLOCKED
REPORT THE CONFLICT
```

---

# 3. APPROVED CALIBRATION CONTRACT — LOCKED

Implement exactly the approved calibration/evaluation contract.

## Calibration method

```text
EEGNet -> temperature scaling
CSP+LDA -> sigmoid / Platt-style calibration
identity / no-calibration -> preserved baseline
```

Rules:

- calibration remains model-specific;
- preserve class order `("left", "right")`;
- calibration fitting uses the existing `validation` partition only;
- model/decoder fitting remains on `train`;
- `test` and `final_test` must not influence calibrator fitting, method choice, tuning, or binning;
- within-subject and cross-subject evaluation remain separate.

## Reliability evaluation

```text
ECE binning -> exactly 10 equal-width bins over [0,1]
report Brier Score alongside ECE
```

Rules:

- do not tune bin count or binning strategy using protected test performance;
- keep calibration evaluation reproducible and auditable.

---

# 4. IMPLEMENTATION SCOPE

Implement the smallest module(s) necessary to:

```text
- fit the approved model-specific calibrators on validation data only;
- preserve an explicit identity / no-calibration baseline;
- transform decoder outputs into calibrated probabilities without changing class order;
- compute reliability bins, ECE, and Brier Score under the approved fixed binning rule;
- validate probability normalization and protected-partition isolation;
- consume the accepted CSP+LDA and EEGNet decoder contracts without redefining model semantics.
```

Expected file scope:

```text
src/models/calibration.py
tests/test_calibration.py
CURRENT_TASK.md
requirements.txt only if genuinely necessary
```

---

# 5. FORBIDDEN SCOPE

Do not implement or resolve:

```text
Bayesian goal mapping or inference
entropy/shared-autonomy thresholds or policy
adaptation
planning/safety
replay
later experiment modules
new train/validation/test semantics
```

Do not modify:

```text
DECISIONS.md
MASTER_PROJECT_SPEC.md
PROJECT_STATE.md
TODO.md
```

---

# 6. REQUIRED TESTS

Add targeted automated tests covering at minimum:

```text
- correct model-specific calibration method;
- validation-only calibrator fitting;
- protected test/final_test isolation;
- identity calibration;
- probability normalization;
- stable class order;
- temperature scaling behavior;
- Platt/sigmoid calibration behavior;
- ECE with exactly 10 equal-width bins over [0,1];
- Brier Score;
- compatibility with accepted CSP+LDA and EEGNet paths.
```

Run:

```text
pytest tests/test_calibration.py tests/test_eegnet.py tests/test_csp_lda.py tests/test_splits.py tests/test_epochs.py tests/test_preprocessing.py tests/test_loader.py
```

If feasible, also run a bounded real-data subject-1 smoke check and report it only as integration evidence, not model-performance evidence.

---

# 7. ACCEPTANCE CRITERIA

M1-T07 may be reported complete only if:

```text
- D-048/D-049/D-050 are implemented without reinterpretation;
- calibration fitting is validation-only and protected partitions remain excluded from fitting/selection;
- the approved model-specific methods are explicit and tested;
- identity / no-calibration remains available;
- class order is preserved as ("left", "right");
- ECE uses exactly 10 equal-width bins over [0,1];
- Brier Score is reported alongside ECE;
- targeted tests and the required regression suite are executed and reported;
- no Bayesian/shared-autonomy/planning/safety/later modules are implemented.
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
3. Exact calibration behavior implemented
4. Tests added
5. Tests executed and exact commands
6. Test results
7. Smoke/artifact examples generated, if any
8. Protected-partition checks performed
9. Known limitations
10. Open blockers
11. Suggested commit / PR message
```

Then stop.
