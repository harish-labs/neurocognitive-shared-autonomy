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
EEG decoding, calibration, binary Bayesian goal inference, uncertainty/shared-autonomy policy, and prior-personalization implementation through M1-T10 are accepted and merged.

Current Module:
No active coding task authorized

Current Task ID:
NONE AUTHORIZED

Task Status:
NO ACTIVE TASK

Canonical Branch:
main

Latest Accepted Software Commit:
9aeb3477c0bb7304bca3ad2753eaa3a75a59511c

Latest Accepted Software Task:
M1-T10 — Adaptation / Prior Personalization

Latest Approved Scientific-Decision Commit:
eae232531bf0daa4d80653caa6ae1237a70b782d

Latest Valid Experiment:
None yet

Last Updated:
2026-08-31
```

---

# 2. ACCEPTED IMPLEMENTATION SEQUENCE

Canonical `main` contains ten accepted M1 implementation tasks:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
M1-T07 — Probability Calibration
M1-T08 — Bayesian Goal Inference
M1-T09 — Uncertainty & Shared-Autonomy Policy
M1-T10 — Adaptation / Prior Personalization
```

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, or human-subject result claim is authorized.

---

# 3. APPROVED DECISIONS NOW OPERATIONALIZED

Preprocessing / epoch decisions D-031 through D-039 remain operational.

Split / evaluation decisions D-040 through D-042 remain operational.

CSP+LDA decisions D-043 and D-044 remain operational.

EEGNet decisions D-045 through D-047 remain operational.

Calibration decisions D-048 through D-050 remain operational.

Bayesian / goal-mapping decisions D-051 through D-054 remain operationalized by M1-T08.

Shared-autonomy / uncertainty decisions D-055 through D-057 remain operationalized by M1-T09.

Adaptation decisions D-058 through D-060 are now operationalized by M1-T10:

```text
subject-specific, candidate-pair-specific prior personalization only
counts update only from explicit human-approved final choices
accepted CONFIRM and explicitly corrected OVERRIDE may update
PAUSE / STOP / unresolved DEFER / autonomous PROCEED without explicit feedback do not update
initial alpha values = 1 / 1
3-valid-feedback warm-up
adaptation OFF and warm-up return [0.5,0.5]
post-warm-up prior bounded to [0.25,0.75]
explicit reset returns alpha 1/1, count 0, prior [0.5,0.5]
no decay/forgetting
traceable updates isolated by anonymous subject and stable candidate pair
personalized prior may initialize a fresh Bayesian episode only
mid-sequence custom prior injection rejected
Bayesian likelihood/update math, decoder/calibration, and D-055 through D-057 policy unchanged
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
| Uncertainty / Shared-Autonomy Policy | PASS | `7fd4e4c5824199764567f4d8cc71127063a477be` | M1-T09 accepted |
| Adaptation / Prior Personalization | PASS | `9aeb3477c0bb7304bca3ad2753eaa3a75a59511c` | M1-T10 accepted |
| SAR / Planning / Safety | NOT STARTED / BLOCKED | — | U-029 through U-033 unresolved where applicable |
| Reportable Evaluation | NOT STARTED | — | no reportable experiment yet |

---

# 5. M1-T10 VERIFIED SOFTWARE

```text
src/cognitive/adaptation.py implemented
src/cognitive/bayes.py supports validated optional initial priors at new-episode boundaries
tests/test_adaptation.py implemented
tests/test_bayes.py extended for personalized-prior initialization
accepted task-branch head / canonical software commit:
9aeb3477c0bb7304bca3ad2753eaa3a75a59511c
```

Accepted behavior:

```text
new personalization state starts alpha 1/1, update_count 0
order-independent candidate-pair identity with subject isolation
explicit accepted CONFIRM / corrected OVERRIDE updates only
3-event warm-up before non-uniform prior applies
prior bounds preserve normalized [0.25,0.75] limits
adaptation OFF always returns [0.5,0.5]
reset restores initial state and uniform prior
trace records retain explicit source observation provenance
fresh Bayesian episodes may receive a validated custom initial prior
default Bayesian initial prior remains [0.5,0.5]
custom prior cannot be injected during an active Bayesian evidence sequence
Bayesian evidence update remains posterior proportional to prior/posterior times likelihood
no threshold adaptation, evidence weighting, decoder retraining, planner, safety, or environment execution dependency
```

Final reviewed regression evidence reported from the task branch:

```text
124 passed, 1 warning
```

The warning is the existing non-failing PyTorch EEGNet `padding='same'` warning and is not an acceptance blocker.

Architecture-path note:

```text
The specification names src/cognition/adaptation.py.
The established repository package is src/cognitive/.
The accepted implementation uses src/cognitive/adaptation.py without changing the scientific architecture.
```

---

# 6. M1-T10 SYNTHETIC INTEGRATION SMOKE

```text
Adaptation OFF -> (0.5, 0.5)
Three valid explicit feedback events -> personalized prior (0.75, 0.25)
Fresh Bayesian episode initial posterior -> (0.75, 0.25)
After evidence (0.8, 0.2) -> posterior approximately (0.9230769231, 0.0769230769)
```

Interpretation rule:

> This is synthetic integration evidence only. It does not establish adaptation benefit, improved intent decoding, improved task success, improved safety, or human-performance benefit.

No reportable adaptation experiment has yet been run.

---

# 7. CURRENT SCIENTIFIC BLOCKERS

## Bayesian / Goal Mapping

```text
None currently unresolved.
```

## Shared Autonomy / Uncertainty Policy

```text
None currently unresolved.
```

## Adaptation

```text
None currently unresolved.
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
Bayesian posterior -> entropy/shared-autonomy policy: PASS
Explicit-feedback prior personalization -> fresh Bayesian initial prior: PASS
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
Adaptation experiment: NOT STARTED
Planning/safety experiment: NOT STARTED
A/B/C/D comparison: BLOCKED
Robustness/ablations: BLOCKED
Cross-subject model evaluation: NOT STARTED
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
binary goal-evidence mapping and bounded sequential Bayesian goal inference are implemented under D-051 through D-054
binary Shannon entropy and PROCEED/CONFIRM/DEFER policy are implemented under D-055 through D-057
human PAUSE/STOP/OVERRIDE precedence hooks are implemented at the non-executing policy layer
subject/pair-specific bounded prior personalization is implemented under D-058 through D-060
personalized priors can initialize fresh Bayesian episodes while leaving Bayes update mathematics unchanged
synthetic integration examples execute as expected
```

Not authorized:

```text
EEGNet outperforms CSP+LDA
either decoder is above chance in a reportable experiment
calibration improves reliability
Bayesian inference improves intent inference or goal selection
shared autonomy improves task success or safety
adaptation/personalization improves performance
cross-subject generalization claims
live EEG or physical-robot claims
```

---

# 11. NEXT GOVERNANCE GATE

No next implementation task is authorized.

The next unresolved scientific boundary begins at U-029 planning/safety.

Before the next task:

```text
1. identify one narrow next module
2. check MASTER_PROJECT_SPEC.md
3. check CURRENT_TASK.md
4. check PROJECT_STATE.md
5. check DECISIONS.md
6. check relevant technical documentation and accepted code/tests
7. resolve any blocking scientific/architectural decision
8. record any newly approved decision
9. obtain explicit Project Owner approval
10. activate exactly one CURRENT_TASK.md ticket
```

Do not implement U-029 or later unresolved work until explicitly approved.
