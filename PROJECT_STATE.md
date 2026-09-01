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
EEG decoding, calibration, Bayesian goal inference, uncertainty/shared-autonomy policy, and prior personalization through M1-T10 are accepted and merged. M4-T01 SAR Environment + Risk Map and M4-T02 Risk-Aware A* Planner are accepted and merged. M4-T03 Safety Controller is authorized and not yet implemented.

Current Module:
Safety Controller / Hard Constraint Enforcement

Current Task ID:
M4-T03

Task Status:
ACTIVE / NOT STARTED

Canonical Branch:
main

Latest Accepted Software Commit:
c224a4dfb3684d0d4555d7a606a90dc822571c11

Latest Accepted Software Task:
M4-T02 — Risk-Aware A* Planner

Latest Approved Scientific-Decision Commit:
fdef1d5afaf7d13aaffb0e8d5b39379497ee7442

Latest Governance / Task-Authorization Commit:
622b441be6714b5acb2d596d75acc560c4bd54a3

Latest Valid Experiment:
None yet

Last Updated:
2026-09-01
```

---

# 2. ACCEPTED IMPLEMENTATION SEQUENCE

Canonical `main` contains accepted implementation through:

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
M4-T01 — 2D Search & Rescue Environment + Risk Map
M4-T02 — Risk-Aware A* Planner
```

Accepted M4-T02 canonical software commit:

```text
c224a4dfb3684d0d4555d7a606a90dc822571c11
```

The current authorized task is:

```text
M4-T03 — Safety Controller / Hard Constraint Enforcement
```

M4-T03 is authorized but has not yet been implemented, tested, reviewed, accepted, or merged.

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, human-subject result, or certified real-world safety claim is authorized.

---

# 3. APPROVED DECISIONS NOW OPERATIONALIZED / AVAILABLE

Preprocessing / epoch decisions D-031 through D-039 remain operational.

Split / evaluation decisions D-040 through D-042 remain operational.

CSP+LDA decisions D-043 and D-044 remain operational.

EEGNet decisions D-045 through D-047 remain operational.

Calibration decisions D-048 through D-050 remain operational.

Bayesian / goal-mapping decisions D-051 through D-054 remain operationalized by M1-T08.

Shared-autonomy / uncertainty decisions D-055 through D-057 remain operationalized by M1-T09.

Adaptation decisions D-058 through D-060 remain operationalized by M1-T10.

Planning / safety decisions D-061 through D-065 are approved. M4-T01 operationalizes environment/risk representation; M4-T02 operationalizes risk-aware planning. M4-T03 is authorized to operationalize hard transition safety checks.

```text
D-061:
FREE 0.00 / LOW 0.25 / MODERATE 0.50 / HIGH 0.75 / PROHIBITED 1.00
blocked cells remain separate hard obstacles

D-062:
fixed risk semantics
no map-dependent normalization
destination-cell additive risk
start cell not charged again

D-063:
lambda = 2.0
step cost = 1.0 + 2.0 * risk(destination)
Manhattan heuristic

D-064:
planner excludes and safety rejects risk >= 1.00
HIGH 0.75 remains soft/traversable
blocked cells independently prohibited

D-065:
no safe route -> explicit NO_SAFE_PATH
no automatic constraint relaxation or goal substitution
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
| SAR Environment / Risk Map | PASS | `5310743539675744b284bafdf24789fc2025816d` | M4-T01 accepted and merged |
| Risk-Aware A* Planner | PASS | `c224a4dfb3684d0d4555d7a606a90dc822571c11` | M4-T02 accepted and merged |
| Safety Controller | AUTHORIZED / NOT STARTED | — | M4-T03 active |
| Planner/Safety/Environment Integration | NOT STARTED | — | requires accepted M4-T03 |
| Reportable Evaluation | NOT STARTED | — | no reportable experiment yet |

---

# 5. M4-T02 VERIFIED SOFTWARE

Canonical accepted files:

```text
src/autonomy/planner.py
tests/test_planner.py
```

Accepted behavior:

```text
deterministic four-connected A*
fixed neighbor expansion order UP / DOWN / LEFT / RIGHT
stable priority-queue tie breaking
Manhattan heuristic
explicit approved goal input
blocked cells excluded from valid paths
risk >= 1.00 excluded from valid paths
HIGH 0.75 remains traversable soft risk
lambda = 2.0
step_cost = 1.0 + 2.0*risk(destination)
start risk not double charged
path and action reconstruction
movement/risk/path cost decomposition
SUCCESS / INVALID_START / INVALID_GOAL / NO_SAFE_PATH
planner does not mutate environment state or call env.step()
WAIT not used as an A* progress edge
```

Final reviewed verification reported from the accepted branch:

```text
pytest tests/test_planner.py -> 18 passed
pytest tests/test_environment.py tests/test_planner.py -> 38 passed
pytest -> 168 passed, 1 pre-existing non-failing PyTorch warning
```

The PyTorch warning remains unchanged and non-failing.

---

# 6. CURRENT M4-T03 AUTHORIZATION

M4-T03 is authorized to implement only:

```text
separate safety-controller authority layer
single proposed-action safety evaluation
emergency-stop highest-priority halt
pause halt
fail-safe current-state validation
invalid-action rejection
out-of-bounds rejection
blocked-cell rejection / replan-required flag
prohibited-hazard rejection / replan-required flag
HIGH 0.75 remains safety-permitted
WAIT approval only when state/control permit
explicit structured safety decisions
no action substitution
no env.step() execution
no automatic replanning
focused safety tests and full regression execution
```

M4-T03 must not implement:

```text
full planner -> safety -> environment execution loop
automatic replanning
shared-autonomy integration
EEG/Bayesian integration
OVERRIDE goal-selection logic
UI
reportable experiments
real-world safety claims
```

The detailed active ticket is authoritative in `CURRENT_TASK.md`.

---

# 7. CURRENT SCIENTIFIC BLOCKERS

## Planning / Safety

```text
None unresolved for M4-T03 primary hard-safety implementation.
```

## Experimental Analysis

```text
U-034 — Final A/B/C/D component matrix
U-035 — Robustness perturbation levels
U-036 — Final inferential-statistics policy
```

These experimental-analysis decisions do not block M4-T03 unit implementation.

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
SAR environment/risk map: PASS
Risk-aware A* planner: PASS
Safety controller: AUTHORIZED / NOT STARTED
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
A/B/C/D comparison: BLOCKED by U-034 and end-to-end implementation state
Robustness/ablations: BLOCKED by U-035 and implementation state
Cross-subject model evaluation: NOT STARTED
```

No empirical performance conclusion is currently authorized.

---

# 10. CURRENT CLAIM STATUS

Authorized implementation claims:

```text
EEGBCI loader/inspection/preprocessing/split pipeline implemented and verified
CSP+LDA and EEGNet baselines implemented and verified under approved leakage controls
model-specific calibration implemented and verified under approved leakage controls
binary goal-evidence mapping and bounded sequential Bayesian inference implemented
uncertainty/shared-autonomy policy implemented
bounded explicit-feedback prior personalization implemented
deterministic Gymnasium-compatible SAR environment implemented
risk-aware A* planner implemented under D-061 through D-065
```

Not authorized:

```text
EEGNet outperforms CSP+LDA
calibration improves reliability
Bayesian inference improves goal inference
shared autonomy improves task success or safety
adaptation improves performance
risk-aware planning improves outcomes
safety controller improves safety outcomes
cross-subject generalization claims
live EEG / physical robot / certified real-world safety claims
```

---

# 11. NEXT ACTION

The current authorized next action is:

```text
Codex implements M4-T03 exactly as defined in CURRENT_TASK.md on a task branch from current main.
Codex runs focused safety tests, combined autonomy tests, and full regression tests.
Codex commits and pushes the task branch.
Codex stops and reports for ChatGPT scientific review.
```

Do not begin full planner/safety/environment integration until M4-T03 has been reviewed and accepted.
