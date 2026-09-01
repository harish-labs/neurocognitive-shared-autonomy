# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Last updated:** 2026-09-01

---

# 1. STATUS AT A GLANCE

```text
Project phase:
EEG decoding/calibration/Bayesian/shared-autonomy/adaptation through M1-T10 are accepted and merged.
M4-T01 SAR Environment + Risk Map is accepted and merged.
M4-T02 Risk-Aware A* Planner is accepted and merged.
M4-T03 Safety Controller / Hard Constraint Enforcement is accepted and merged.
M4-T04 Planner → Safety → Environment Execution Integration is authorized and not started.

Current module:
Planner / Safety / Environment execution integration

Current task:
M4-T04

Task status:
ACTIVE / NOT STARTED

Canonical branch:
main

Latest accepted task-branch software commit:
6573ba90f96447081b3edfd5560d354fe2f69a6b

Latest accepted software task:
M4-T03 — Safety Controller / Hard Constraint Enforcement

Canonical M4-T03 merge commit:
ef7e27dfd8bf6446ddb1f0c783800b13ebbdca71

Latest task-authorization commit:
4f367f07b475bb7537eb1eddd8c58aa00d0849a4

Latest approved scientific-decision commit:
fdef1d5afaf7d13aaffb0e8d5b39379497ee7442

Latest valid reportable experiment:
None yet
```

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
```

M4-T03 accepted verification:

```text
pytest tests/test_safety.py -> 20 passed
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py -> 58 passed
pytest -> 188 passed, 1 pre-existing non-failing PyTorch warning
```

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, certified safety, or human-subject result claim is authorized.

---

# 3. CURRENT AUTONOMY STATE

```text
SAR environment/risk map: PASS
Risk-aware A*: PASS
Hard safety controller: PASS
Planner -> safety -> environment integration: AUTHORIZED / NOT STARTED
Dynamic replanning loop: NOT STARTED
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
```

Accepted planning/safety semantics:

```text
risk values = 0.00 / 0.25 / 0.50 / 0.75 / 1.00
blocked cells are separate hard obstacles
risk >= 1.00 is prohibited
HIGH 0.75 remains traversable soft risk
lambda = 2.0
step cost = 1.0 + 2.0 * risk(destination)
Manhattan A* on four-connected grid
NO_SAFE_PATH never relaxes hard safety or substitutes another goal
planner proposes; safety authorizes; environment executes only approved actions
emergency stop and pause block execution
```

---

# 4. CURRENT SCIENTIFIC BLOCKERS

Planning / safety:

```text
None currently unresolved for M4-T04.
```

Experimental analysis remains unresolved:

```text
U-034 — Final A/B/C/D component matrix
U-035 — Robustness perturbation levels
U-036 — Final inferential-statistics policy
```

These do not block M4-T04 implementation but must be resolved before the corresponding reportable comparison/robustness/inferential experiments.

---

# 5. CLAIM STATUS

Authorized implementation claims include that the accepted EEG, Bayesian/shared-autonomy/adaptation modules and M4-T01 through M4-T03 software components have been implemented and unit/regression tested under their approved tickets.

Not authorized:

```text
claims that any decoder is above chance in a reportable experiment
claims that calibration/Bayesian/shared autonomy/adaptation improves outcomes
claims that risk-aware planning or safety improves outcomes
cross-subject generalization claims
live EEG / physical robot / certified real-world safety claims
```

---

# 6. NEXT ACTION

```text
Codex implements M4-T04 exactly as defined in CURRENT_TASK.md on a task branch from current main.
It must integrate accepted planner -> safety -> environment execution only.
It must run focused integration tests, combined autonomy tests, and the full regression suite.
It must commit/push and stop for ChatGPT scientific review.
```
