# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### No Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no task is currently authorized  
**Current status:** NO ACTIVE TASK  
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / Decoders / Calibration  
**Task ID:** NONE AUTHORIZED  
**Task title:** Awaiting next approved implementation ticket  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-08-31

---

# 1. CURRENT AUTHORIZATION STATE

There is currently no active implementation task authorized for Codex.

Completed, scientifically reviewed, accepted, and merged on canonical `main`:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
M1-T07 — Probability Calibration
```

Do not begin another implementation module until a new narrow `CURRENT_TASK.md` ticket is explicitly approved by the Project Owner.

---

# 2. CLOSED TASK RECORD — M1-T07

```text
Task ID:
M1-T07

Task title:
Probability Calibration

Final status:
PASS / ACCEPTED / MERGED

Task branch:
task/m1-t07-probability-calibration

Accepted task-branch head / canonical software commit:
b6a2932372b3b8047f4629b52e5a1822ce4fd057
```

M1-T07 implements the approved probability-calibration layer under D-048, D-049, and D-050.

Accepted implementation behavior:

```text
EEGNet -> temperature scaling
CSP+LDA -> sigmoid / Platt-style calibration
identity / no-calibration baseline retained
validation partition only for calibrator fitting
train remains decoder/model-fitting partition
test/final_test excluded from calibrator fitting, calibration-method choice, tuning, and binning
class order preserved as ("left", "right")
ECE/reliability diagram uses exactly 10 equal-width bins over [0,1]
Brier Score reported alongside ECE
within-subject and cross-subject tracks remain separate
```

Accepted regression bundle:

```text
59 passed, 1 warning
```

The warning is the previously reviewed non-failing PyTorch `padding='same'` warning from EEGNet tests.

Bounded subject-1 smoke verification using runs 4/8/12:

```text
retained epochs: 13
train / validation / test: 7 / 3 / 3
CSP calibrator: platt_scaling
EEGNet calibrator: temperature_scaling
CSP selected components: 4
EEGNet selected epoch: 1
```

This smoke run is integration evidence only. Its calibration metrics are not reportable evidence of generalizable calibration quality or model efficacy.

No Bayesian goal mapping, Bayesian inference, shared-autonomy policy, adaptation, planning, safety, replay, or later module was implemented in M1-T07.

---

# 3. NEXT GOVERNANCE GATE

Before any further implementation:

```text
1. Identify the next narrow implementation task.
2. Check MASTER_PROJECT_SPEC.md.
3. Check CURRENT_TASK.md.
4. Check PROJECT_STATE.md.
5. Check DECISIONS.md.
6. Check relevant technical documentation and accepted code/tests.
7. Resolve any blocking scientific/architectural decision.
8. Record any new approved decision in DECISIONS.md.
9. Obtain explicit Project Owner approval for exactly one narrow task.
10. Only then activate CURRENT_TASK.md and begin implementation.
```

Until that happens:

```text
STOP
STATUS = NO ACTIVE TASK
```
