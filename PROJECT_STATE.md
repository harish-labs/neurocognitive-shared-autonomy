# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project  
**Update rule:** Update after every accepted implementation task, verified experiment, major blocker, approved scientific decision, or accepted architectural change  
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
EEG decoding, calibration, and binary Bayesian goal-inference implementation through M1-T08 is accepted and merged.

Current Module:
No active coding task authorized

Current Task ID:
NONE AUTHORIZED

Task Status:
NO ACTIVE TASK

Canonical Branch:
main

Latest Accepted Software Commit:
43fb1f10b0a78236ca01c21076a37eacf70529a9

Latest Accepted Software Task:
M1-T08 — Bayesian Goal Inference

Latest Approved Scientific-Decision Commit:
2cb9208a5f16d5f67fe5830caf1f0837f6ada6d8

Latest Valid Experiment:
None yet

Last Updated:
2026-08-31
```

---

# 2. ACCEPTED IMPLEMENTATION SEQUENCE

Canonical `main` now contains eight accepted M1 implementation tasks:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
M1-T07 — Probability Calibration
M1-T08 — Bayesian Goal Inference
```

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, or real human-subject claim is authorized.

---

# 3. APPROVED DECISIONS NOW OPERATIONALIZED

Preprocessing / epoch decisions D-031 through D-039 remain operational.

Split / evaluation decisions D-040 through D-042 remain operational.

CSP+LDA decisions D-043 and D-044 remain operational.

EEGNet decisions D-045 through D-047 remain operational.

Calibration decisions D-048 through D-050 remain operational.

Bayesian / goal-mapping decisions D-051 through D-054 are now operationalized by M1-T08:

```text
binary-choice interaction protocol only
exactly two active candidates per decision episode
left calibrated evidence -> candidate A
right calibrated evidence -> candidate B
multi-goal SAR interaction represented as a sequence of binary choices
calibrated binary probabilities used directly as candidate evidence likelihood weights
planner/safety desirability excluded from intent likelihoods
uniform baseline prior [0.5, 0.5]
commit when posterior >= 0.90
maximum 5 accepted evidence updates
if no threshold by update 5 -> DEFER / UNCOMMITTED
no forced argmax decision
new episode resets posterior to [0.5, 0.5]
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
| Bayesian Goal Inference | PASS | `43fb1f10b0a78236ca01c21076a37eacf70529a9` | M1-T08 accepted |
| Uncertainty / Entropy policy | NOT STARTED | — | U-023 through U-025 unresolved |
| Adaptation / Personalization | BLOCKED | — | U-026 through U-028 unresolved |
| SAR / Planning / Safety | NOT STARTED / BLOCKED | — | U-029 through U-033 unresolved where applicable |
| Reportable Evaluation | NOT STARTED | — | no reportable experiment yet |

---

# 5. M1-T08 VERIFIED SOFTWARE

```text
src/cognitive/bayes.py implemented
tests/test_bayes.py implemented
accepted task-branch head / canonical software commit:
43fb1f10b0a78236ca01c21076a37eacf70529a9
```

Accepted behavior:

```text
BinaryGoalEvidence maps approved left/right calibrated evidence to candidate A/B
BinaryBayesianGoalEpisode starts/reset at [0.5, 0.5]
sequential update multiplies prior/posterior by likelihood weights and normalizes
posterior stays finite/non-negative/normalized
non-binary, malformed, negative, non-finite, or reversed-class evidence is rejected
posterior >= 0.90 commits the corresponding candidate
commitment is terminal for that episode
maximum 5 accepted updates
fifth non-committing update produces DEFER with no forced argmax
new episode explicitly resets state/history/count/status
planner/safety information cannot be passed into likelihood construction through the approved API
```

Final reviewed regression evidence:

```text
77 passed, 1 warning
```

The warning is the existing non-failing PyTorch `padding='same'` warning from EEGNet tests and is not an acceptance blocker.

---

# 6. M1-T08 SYNTHETIC INTEGRATION SMOKE

```text
Evidence 1: [0.7, 0.3]
Evidence 2: [0.8, 0.2]
Result: candidate A committed on update 2
Posterior: approximately (0.9032, 0.0968)

Five repetitions of [0.55, 0.45]
Result: DEFER after update 5
No forced selection
```

Interpretation rule:

> This is synthetic integration evidence only. It does not establish that Bayesian inference improves intent decoding, task success, safety, calibration, or human performance.

No reportable Bayesian experiment has yet been run.

---

# 7. CURRENT SCIENTIFIC BLOCKERS

## Bayesian / Goal Mapping

```text
None currently unresolved.
```

## Shared Autonomy / Uncertainty Policy

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

If preprocessing/QC produces an eligible cross-subject cohort other than 109, D-042 still requires reviewer decision before freezing a different final subject manifest.

---

# 8. CURRENT TECHNICAL / INTEGRATION STATE

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
Calibration -> binary goal evidence: PASS
Binary sequential Bayesian inference: PASS
Bayesian posterior -> entropy/shared-autonomy policy: NOT STARTED
Planner/safety/environment integration: NOT STARTED
Offline replay -> full system: NOT STARTED
```

High artifact rejection observed in the subject-1 path remains a scientific/data-quality limitation and does not authorize changing the approved 150 µV threshold.

---

# 9. CURRENT EXPERIMENT / RESULT STATE

```text
Reportable EEG decoding experiment: NOT STARTED
Reportable calibration experiment: NOT STARTED
Reportable Bayesian experiment: NOT STARTED
Shared-autonomy experiment: NOT STARTED
Planning/safety experiment: NOT STARTED
A/B/C/D comparison: BLOCKED
Robustness/ablations: BLOCKED
Cross-subject model evaluation: NOT STARTED
Adaptation experiment: BLOCKED
```

No empirical performance conclusion is currently authorized.

---

# 10. CURRENT CLAIM STATUS

Authorized implementation claims:

```text
EEGBCI loader/inspection/preprocessing/split pipeline has been implemented and verified
CSP+LDA baseline has been implemented and verified under approved leakage controls
EEGNet baseline has been implemented and verified under approved leakage controls
model-specific calibration has been implemented and verified under approved leakage controls
binary goal-evidence mapping and bounded sequential Bayesian goal inference have been implemented under D-051 through D-054
synthetic Bayesian integration examples execute as expected
```

Not authorized:

```text
EEGNet outperforms CSP+LDA
either decoder is above chance in a reportable experiment
calibration improves reliability
Bayesian inference improves intent inference or goal selection
shared autonomy improves task success or safety
cross-subject generalization claims
adaptation improvement claims
```

---

# 11. NEXT GOVERNANCE GATE

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

The next unresolved scientific boundary begins at U-023 shared-autonomy / uncertainty policy. Do not implement it or any later module until the required decisions and task authorization are explicit.
