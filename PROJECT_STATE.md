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
EEG decoding, calibration, binary Bayesian goal inference, uncertainty/shared-autonomy policy, and prior personalization through M1-T10 are accepted and merged. M4-T01 2D SAR Environment + Risk Map is now accepted and merged. M4-T02 Risk-Aware A* Planner is authorized and not yet implemented.

Current Module:
Risk-Aware A* Planner

Current Task ID:
M4-T02

Task Status:
ACTIVE / NOT STARTED

Canonical Branch:
main

Latest Accepted Software Commit:
5310743539675744b284bafdf24789fc2025816d

Latest Accepted Software Task:
M4-T01 — 2D Search & Rescue Environment + Risk Map

Latest Approved Scientific-Decision Commit:
fdef1d5afaf7d13aaffb0e8d5b39379497ee7442

Latest Governance / Task-Authorization Commit:
66300461f172ae7c9edf168a393e525e8829ae79

Latest Valid Experiment:
None yet

Last Updated:
2026-09-01
```

---

# 2. ACCEPTED IMPLEMENTATION SEQUENCE

Canonical `main` contains the accepted M1 implementation sequence:

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

Canonical `main` now also contains:

```text
M4-T01 — 2D Search & Rescue Environment + Risk Map
```

Accepted M4-T01 canonical software commit:

```text
5310743539675744b284bafdf24789fc2025816d
```

The current authorized task is:

```text
M4-T02 — Risk-Aware A* Planner
```

M4-T02 is authorized but has not yet been implemented, tested, reviewed, accepted, or merged.

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, or human-subject result claim is authorized.

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

Planning / safety decisions D-061 through D-065 are approved. M4-T01 operationalizes the environment/risk representation portions; M4-T02 is authorized to operationalize the planner portions.

```text
D-061:
FREE 0.00
LOW 0.25
MODERATE 0.50
HIGH 0.75
PROHIBITED 1.00
blocked cells remain separate hard obstacles

D-062:
fixed canonical risk semantics
no per-map/adaptive normalization
risk contribution is destination-cell risk
path risk is additive over entered cells

D-063:
primary A* lambda = 2.0
step cost = 1.0 + 2.0 * risk(destination)
Manhattan heuristic

D-064:
blocked cells and risk >= 1.00 are excluded from valid planner paths
HIGH 0.75 remains traversable soft risk
safety controller will later independently enforce hard transition authorization

D-065:
no permitted route -> explicit NO_SAFE_PATH / UNREACHABLE
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
| Risk-Aware A* Planner | AUTHORIZED / NOT STARTED | — | M4-T02 active |
| Safety Controller | NOT STARTED | — | separate later task required |
| Planner/Safety/Environment Integration | NOT STARTED | — | requires accepted planner and safety modules |
| Reportable Evaluation | NOT STARTED | — | no reportable experiment yet |

---

# 5. M4-T01 VERIFIED SOFTWARE

Canonical accepted files:

```text
src/autonomy/__init__.py
src/autonomy/environment.py
tests/test_environment.py
requirements.txt includes gymnasium
```

Accepted behavior:

```text
deterministic 2D single-agent SAR mechanics
(row, column) coordinate convention
UP / DOWN / LEFT / RIGHT / WAIT
Gymnasium Env interface
Discrete(5) action space
position observation space
reset -> observation, info
step -> observation, reward, terminated, truncated, info
neutral reward 0.0
truncated=False for static core environment
named goals and goal termination
blocked cells separate from risk
risk values exactly 0.00 / 0.25 / 0.50 / 0.75 / 1.00
PROHIBITED 1.00 exposed without folding future safety-controller authority into environment mechanics
no planner or safety controller implemented in M4-T01
```

Final reviewed verification reported from the accepted branch:

```text
pytest tests/test_environment.py -> 20 passed
pytest -> 150 passed, 1 pre-existing PyTorch warning
Gymnasium check_env -> passed
```

The PyTorch warning is pre-existing and non-failing.

---

# 6. CURRENT M4-T02 AUTHORIZATION

M4-T02 is authorized to implement only:

```text
deterministic four-connected A*
Manhattan heuristic
approved goal as fixed planner target
blocked/risk>=1.00 exclusion from valid plans
HIGH 0.75 as soft traversable risk
step cost = 1.0 + 2.0*risk(destination)
path/action reconstruction
movement/risk/path cost decomposition
explicit SUCCESS / INVALID_START / INVALID_GOAL / NO_SAFE_PATH outcomes
deterministic tie-breaking
planner tests and full regression execution
```

M4-T02 must not implement:

```text
safety controller
action execution authorization
human STOP/PAUSE execution logic
shared-autonomy integration
replanning trigger loop
dynamic hazards
EEG/Bayesian integration
UI
reportable experiments
lambda tuning or alternative production planners
```

The detailed active ticket is authoritative in `CURRENT_TASK.md`.

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
No unresolved scientific parameter blocks M4-T02.
Safety-controller implementation remains a later separate task after M4-T02 acceptance.
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
SAR environment/risk map: PASS
Risk-aware A* planner: AUTHORIZED / NOT STARTED
Safety controller: NOT STARTED
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
EEGBCI loader/inspection/preprocessing/split pipeline has been implemented and verified
CSP+LDA baseline has been implemented and verified under approved leakage controls
EEGNet baseline has been implemented and verified under approved leakage controls
model-specific calibration has been implemented and verified under approved leakage controls
binary goal-evidence mapping and bounded sequential Bayesian goal inference are implemented
binary Shannon entropy and PROCEED/CONFIRM/DEFER policy are implemented
human PAUSE/STOP/OVERRIDE precedence hooks exist at the non-executing policy layer
subject/pair-specific bounded prior personalization is implemented
M4-T01 deterministic Gymnasium-compatible 2D SAR environment and canonical risk map are implemented and verified
```

Not authorized:

```text
EEGNet outperforms CSP+LDA
either decoder is above chance in a reportable experiment
calibration improves reliability
Bayesian inference improves intent inference or goal selection
shared autonomy improves task success or safety
adaptation/personalization improves performance
risk-aware A* is implemented or improves outcomes before M4-T02 acceptance
safety controller improves safety outcomes
cross-subject generalization claims
live EEG or physical-robot claims
```

---

# 11. NEXT ACTION

The current authorized next action is:

```text
Codex creates a task branch from current main.
Codex implements M4-T02 exactly as defined in CURRENT_TASK.md.
Codex runs focused planner tests, environment+planner regression, and full pytest.
Codex commits and pushes the task branch.
Codex stops and reports for ChatGPT scientific review.
```

Do not implement the safety-controller task until M4-T02 has been reviewed and accepted.
