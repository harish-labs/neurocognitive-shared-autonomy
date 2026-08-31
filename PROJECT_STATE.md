# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project  
**Update rule:** Update after every accepted implementation task, verified experiment, major blocker, approved scientific decision, or accepted architectural change  
**Do not use for:** speculative ideas, unapproved methodology, literature notes, hypothetical results, or future features  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. SOURCE-OF-TRUTH USE

```text
MASTER_PROJECT_SPEC.md -> what the project IS
DECISIONS.md            -> what has been explicitly DECIDED
CURRENT_TASK.md         -> what is being DONE NOW
PROJECT_STATE.md        -> what is ACTUALLY TRUE NOW
EXPERIMENT_LOG.md       -> what has actually been RUN as a reportable experiment
RESEARCH_LOG.md         -> unresolved scientific/research reasoning
TODO.md                 -> backlog; not authorization
AGENTS.md               -> Codex implementation rules
```

GitHub is the canonical implementation/state source of truth.

---

# 1. STATUS AT A GLANCE

```text
Project Phase:
EEG decoding and probability-calibration implementation through M1-T07 is accepted and merged.

Current Module:
No active coding task authorized

Current Task ID:
NONE AUTHORIZED

Task Status:
NO ACTIVE TASK

Canonical Branch:
main

Latest Accepted Software Commit:
b6a2932372b3b8047f4629b52e5a1822ce4fd057

Latest Accepted Software Task:
M1-T07 — Probability Calibration

Latest Approved Scientific-Decision Commit:
7b5f28095b3faa123bf942532a69e443847924a9

Latest Valid Experiment:
None yet

Last Updated:
2026-08-31

Updated By:
ChatGPT + Project Owner + Codex
```

---

# 2. CURRENT PROJECT PHASE

The project currently has seven accepted and merged M1 implementation tasks on canonical `main`:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
M1-T07 — Probability Calibration
```

The repository now contains:

```text
verified EEGBCI loading and inspection
accepted preprocessing and epoch extraction
deterministic leakage-safe within-subject and cross-subject split utilities
accepted CSP+LDA baseline
accepted EEGNet / compact CNN baseline
stable binary left/right probability outputs from both decoder families
accepted model-specific probability calibration
fixed reliability-bin, ECE, and Brier utilities
```

No implementation task is currently authorized.

The project remains an **offline prerecorded EEG** system. No live EEG, physical robot, or real human-subject claim is authorized.

---

# 3. APPROVED DECISIONS NOW OPERATIONALIZED

Preprocessing / epoch decisions D-031 through D-039 remain operational.

Split/evaluation decisions D-040 through D-042 remain operational.

CSP+LDA decisions D-043 and D-044 remain operational.

EEGNet architecture/training decisions D-045, D-046, and D-047 remain operational.

Calibration decisions D-048 through D-050 are now operationalized by M1-T07:

```text
EEGNet -> temperature scaling
CSP+LDA -> sigmoid / Platt-style calibration
identity / no-calibration remains an experimental baseline
calibration remains model-specific
validation partition only for calibrator fitting
train remains decoder/model-fitting partition
test/final_test remain protected from fitting, calibration-method choice, tuning, and binning
primary reliability diagram / ECE: 10 equal-width bins over [0,1]
Brier Score reported alongside ECE
```

---

# 4. IMPLEMENTATION STATUS MATRIX

| Component | Status | Latest Accepted Commit | Notes |
|---|---|---|---|
| EEG Data Loader | PASS | `9b241681dfc986f53f5f8c0fcf40a3e3cea496e7` | EEGBCI loading verified |
| EEG Visualization / Inspection | PASS | `9b241681dfc986f53f5f8c0fcf40a3e3cea496e7` | inspection verified |
| EEG Preprocessing / Epochs | PASS | `1af72b5deb9981f469a4394859aac49add65e2a7` | accepted pipeline |
| EEG Split Manifest / Leakage Assertions | PASS | `3b33477166db6889747dabc8d4be21403b480735` | leakage-safe split utilities |
| CSP + LDA | PASS | `d7597efb8db7c8d77aecbd87f9cf2366dd02b484` | accepted classical baseline |
| EEGNet / Compact CNN | PASS | `6b526d76acb53cd4f632ba87c975b4ede9e89a9c` | accepted neural baseline |
| Probability Calibration | PASS | `b6a2932372b3b8047f4629b52e5a1822ce4fd057` | M1-T07 accepted |
| Unified Decoder Interface | NOT STARTED | — | separate authorization required if needed |
| Bayesian Goal Inference | NOT STARTED | — | U-019 through U-022 unresolved |
| Uncertainty / Entropy policy | NOT STARTED | — | later policy decisions unresolved |
| Adaptation / Personalization | BLOCKED | — | U-026 through U-028 unresolved |
| SAR / Planning / Safety / Shared Autonomy | NOT STARTED / BLOCKED | — | later milestones require their decisions |
| Reportable EEG / Calibration Evaluation | NOT STARTED | — | no reportable experiment yet |

---

# 5. M1-T07 VERIFIED SOFTWARE

```text
src/models/calibration.py implemented
tests/test_calibration.py implemented
accepted task-branch head / canonical software commit b6a2932372b3b8047f4629b52e5a1822ce4fd057
```

Accepted behavior:

```text
TemperatureScalingCalibrator for EEGNet
PlattScalingCalibrator for CSP+LDA
IdentityCalibrator baseline
validation-only calibrator fitting
protected test/final-test isolation
approved class order ("left", "right")
probability normalization checks
10 fixed equal-width reliability bins over [0,1]
ECE calculation
binary Brier Score using the fixed right-class convention
```

Final reviewed regression evidence:

```text
59 passed, 1 warning
```

The warning is the existing non-failing PyTorch `padding='same'` warning from EEGNet tests and is not an acceptance blocker.

---

# 6. M1-T07 REAL-DATA SMOKE CHECK

Real subject 1, runs 4/8/12:

```text
retained epochs: 13
partition counts: train=7, validation=3, test=3
CSP calibrator: platt_scaling
EEGNet calibrator: temperature_scaling
CSP selected components: 4
EEGNet selected epoch: 1
```

Calibration metrics were generated during this bounded smoke path, but the validation partition contains only three epochs.

Interpretation rule:

> This is integration evidence only. The observed subject-1 ECE/Brier values are not reportable evidence of generalizable calibration quality, decoder efficacy, or downstream benefit.

No reportable experiment has yet been run.

---

# 7. CURRENT SCIENTIFIC BLOCKERS

## Bayesian / Goal Mapping

```text
U-019 — Binary EEG -> multi-goal interaction protocol
U-020 — Decoder posterior -> goal likelihood construction
U-021 — Prior policy
U-022 — Bayesian stopping / commitment rule
```

## Shared Autonomy

```text
U-023 — Confidence / entropy thresholds
U-024 — Exact proceed / confirm / defer policy
U-025 — Prolonged-uncertainty fallback
```

## Adaptation

```text
U-026 — Exact adaptation mechanism
U-027 — Update formula
U-028 — Bounds / warm-up / reset
```

## Planning / Safety

```text
U-029 — Environmental risk values
U-030 — Risk normalization
U-031 — Risk weight lambda
U-032 — Prohibited-hazard threshold
U-033 — Final no-safe-path policy
```

## Experimental Analysis

```text
U-034 — Final A/B/C/D component matrix
U-035 — Robustness perturbation levels
U-036 — Final inferential-statistics policy
```

Calibration U-016 through U-018 are resolved and implemented; they are no longer blockers.

If preprocessing/QC produces an eligible cross-subject cohort other than 109, D-042 still requires reviewer decision before freezing a different final subject manifest.

---

# 8. CURRENT TECHNICAL STATE

```text
Loader: PASS
Visualization: PASS
Preprocessing: PASS
Epoching: PASS
Within-subject split: PASS
Cross-subject split infrastructure: PASS
CSP+LDA: PASS
EEGNet: PASS
Probability calibration: PASS
Calibration metrics: PASS
Bayesian goal mapping: NOT STARTED
Bayesian inference: NOT STARTED
Entropy/shared autonomy: NOT STARTED
SAR/planning/safety: NOT STARTED
Offline replay: NOT STARTED
```

High artifact rejection in the subject-1 path remains a scientific/data-quality limitation and does not authorize changing the approved 150 µV threshold.

---

# 9. CURRENT INTEGRATION STATE

```text
EEG loader -> preprocessing/epochs: PASS
preprocessing/epochs -> split assignment: PASS
split assignment -> CSP+LDA: PASS
split assignment -> EEGNet: PASS
CSP+LDA probability output -> Platt calibration: PASS
EEGNet logits -> temperature scaling: PASS
calibration -> goal evidence: BLOCKED by U-019/U-020
Bayes -> entropy/shared autonomy: NOT STARTED
planner/safety/environment integration: NOT STARTED
offline EEG replay -> full system: NOT STARTED
```

---

# 10. CURRENT EXPERIMENT / RESULT STATE

```text
Reportable EEG decoding experiment: NOT STARTED
Reportable calibration experiment: NOT STARTED
Bayesian experiment: NOT STARTED
Shared-autonomy experiment: NOT STARTED
Planning/safety experiment: NOT STARTED
A/B/C/D comparison: BLOCKED
Robustness/ablations: BLOCKED
Cross-subject model evaluation: NOT STARTED
Adaptation experiment: BLOCKED
```

No empirical model-performance or calibration-improvement conclusion is currently authorized.

---

# 11. CURRENT CLAIM STATUS

Authorized implementation claims:

```text
EEGBCI loader/inspection/preprocessing/split pipeline has been implemented and verified
CSP+LDA baseline has been implemented and verified under approved leakage controls
EEGNet baseline has been implemented and verified under approved leakage controls
model-specific calibration has been implemented and verified under approved leakage controls
both model families preserve the fixed left/right class order
subject-1 real-data smoke execution completes through decoder and calibration paths
```

Not authorized:

```text
EEGNet outperforms CSP+LDA
either decoder is above chance in a reportable experiment
calibration improves probability reliability
one calibration method is superior to another on reportable data
Bayesian inference improves goal selection
shared autonomy improves task success or safety
cross-subject generalization claims
adaptation improvement claims
```

---

# 12. NEXT GOVERNANCE GATE

No next implementation task is authorized.

Before the next task:

```text
1. identify one narrow next module
2. check MASTER_PROJECT_SPEC.md
3. check CURRENT_TASK.md
4. check PROJECT_STATE.md
5. check DECISIONS.md
6. check relevant technical documentation and accepted code/tests
7. resolve any blocking scientific/architectural decision
8. obtain explicit Project Owner approval
9. activate exactly one CURRENT_TASK.md ticket
```

The immediate unresolved architecture boundary after calibration is the Bayesian / goal-mapping layer beginning at U-019. Do not implement it until its required scientific semantics are explicitly approved.
