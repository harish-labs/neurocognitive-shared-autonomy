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
M4-T04 Planner → Safety → Environment Execution Integration is accepted and merged.
D-066 runtime environment-change / controlled-replanning contract is approved.
M4-T05 Controlled Replanning After Environment Change is authorized and not yet implemented.

Current module:
Controlled replanning after explicit environment change

Current task:
M4-T05

Task status:
ACTIVE / NOT STARTED

Canonical branch:
main

Latest accepted task-branch software commit:
1a7ccde578083b3386183a97ca876714afb68e30

Latest accepted software task:
M4-T04 — Planner → Safety → Environment Execution Integration

Latest approved scientific/architectural decision commit:
5f3a1ed66ee1140766cc73c174dbcab790110596

Latest task-authorization commit:
36a37cdada61f4681c7723a20510368fd7b3febd

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
M4-T04 — Planner → Safety → Environment Execution Integration
```

M4-T04 accepted verification:

```text
pytest tests/test_execution.py -> 13 passed
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py tests/test_execution.py -> 71 passed
pytest -> 201 passed, 1 pre-existing non-failing PyTorch warning
```

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, certified safety, or human-subject result claim is authorized.

---

# 3. CURRENT AUTONOMY STATE

```text
SAR environment/risk map: PASS
Risk-aware A*: PASS
Hard safety controller: PASS
Planner -> safety -> environment execution integration: PASS
Controlled replanning after explicit environment change: AUTHORIZED / NOT STARTED
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable autonomy experiments: NOT STARTED
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
successful planner output is structurally validated before execution
malformed or substituted plans fail closed with zero movement
```

---

# 4. D-066 — CONTROLLED REPLANNING CONTRACT

Approved 2026-09-01:

```text
each relevant runtime environment change is supplied as a new immutable validated replacement environment/map snapshot
replacement snapshot preserves the current agent (row,column) as its start
replacement snapshot preserves the same named goal mapping and same human-approved goal
replanning occurs only after explicit ENVIRONMENT_CHANGED, or a safety requires_replan=True outcome together with a new changed snapshot
unchanged-map retries are forbidden
one environment-change event ID permits at most one replan attempt
another replan requires another explicit event and new validated snapshot
replacement NO_SAFE_PATH -> hold position and stop
PAUSE/STOP remain higher priority and do not themselves create a replan event
no goal substitution, hard-safety relaxation, stochastic hazard invention, or hidden map mutation
```

Canonical decision commit:

```text
5f3a1ed66ee1140766cc73c174dbcab790110596
```

---

# 5. CURRENT M4-T05 AUTHORIZATION

M4-T05 is authorized to implement only a controlled replanning coordinator, primarily in:

```text
src/autonomy/replanning.py
tests/test_replanning.py
```

Required high-level behavior:

```text
validate explicit replan trigger
validate unique event ID
validate replacement environment is a distinct fresh snapshot
validate same grid and named goals
validate replacement start equals current old-environment position
validate blocked/risk map genuinely changed
preserve exact approved goal
consume each event at most once
invoke accepted PlannerSafetyEnvironmentExecutor exactly once on the replacement snapshot
never auto-retry after NO_SAFE_PATH / HALTED / SAFETY_REJECTED / invalid result
```

M4-T05 must not modify accepted environment/planner/safety/execution semantics unless a genuine blocker is reported and reviewed.

---

# 6. CURRENT SCIENTIFIC BLOCKERS

Planning / safety implementation:

```text
None currently unresolved for M4-T05; D-066 resolves the runtime replanning contract needed for this task.
```

Experimental analysis remains unresolved:

```text
U-034 — Final A/B/C/D component matrix
U-035 — Robustness perturbation levels
U-036 — Final inferential-statistics policy
```

These do not block M4-T05 implementation, but they must be resolved before the corresponding reportable comparison/robustness/inferential experiments.

---

# 7. CLAIM STATUS

Authorized implementation claims include that accepted M1-T01 through M1-T10 and M4-T01 through M4-T04 components have been implemented and unit/regression tested under their approved tickets.

Authorized M4-T04 claim:

```text
the simulated execution layer enforces planner -> safety -> environment ordering for one fixed approved goal and fails closed on malformed planner output
```

Not yet authorized:

```text
claim that controlled replanning is implemented before M4-T05 is reviewed and accepted
claims that dynamic replanning improves task success or safety
claims that any decoder is above chance in a reportable experiment
claims that calibration/Bayesian/shared autonomy/adaptation improves outcomes
cross-subject generalization claims
live EEG / physical robot / certified real-world safety claims
```

---

# 8. NEXT ACTION

```text
Codex implements M4-T05 exactly as defined in CURRENT_TASK.md on a task branch from current main.
It must run focused replanning tests, combined autonomy regression tests, and the full test suite.
It must commit/push and stop for ChatGPT scientific review.
No merge and no next task before review.
```
