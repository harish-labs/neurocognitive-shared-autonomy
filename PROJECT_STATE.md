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
M4-T05 Controlled Replanning After Environment Change is accepted and merged.

Current module:
None — M4 core autonomy implementation is closed; next boundary is M5 human interaction.

Current task:
None

Task status:
NO ACTIVE IMPLEMENTATION TASK

Canonical branch:
main

Latest accepted task-branch software commit:
e8183ccebc9c2f67a1b33347b9ef12d25ddbcbfe

Latest accepted software task:
M4-T05 — Controlled Replanning After Environment Change

Latest governance close commit:
3d5f10752cbb0b03a77e1a633584ccb2fa8b0909

Latest approved scientific/architectural decision commit:
5f3a1ed66ee1140766cc73c174dbcab790110596

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
M4-T05 — Controlled Replanning After Environment Change
```

M4-T05 accepted verification:

```text
pytest tests/test_replanning.py -> 13 passed
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py -> 84 passed
pytest -> 214 passed, 1 pre-existing non-failing PyTorch warning
```

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, certified safety, or human-subject result claim is authorized.

---

# 3. CURRENT AUTONOMY STATE

```text
SAR environment/risk map: PASS
Risk-aware A*: PASS
Hard safety controller: PASS
Planner -> safety -> environment execution integration: PASS
Controlled replanning after explicit environment change: PASS
Offline EEG -> full-system execution: NOT STARTED
Human interaction layer: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
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
D-066 uses explicit fresh replacement snapshots and one replan attempt per unique environment-change event
unchanged-map retries and duplicate-event retries are rejected
```

---

# 4. M4 MILESTONE STATE

Core M4 implementation is now accepted:

```text
2D Gymnasium SAR environment: PASS
canonical risk map / blocked-cell distinction: PASS
risk-aware A* / Manhattan heuristic: PASS
hard safety authority: PASS
planner-safety-environment execution ordering: PASS
explicit NO_SAFE_PATH handling: PASS
controlled replanning after explicit environment change: PASS
pause/stop enforcement within safety/execution/replanning paths: PASS
```

No reportable claim that these components improve task success or safety is authorized until the corresponding experiment protocol is approved and run.

---

# 5. NEXT ARCHITECTURAL BOUNDARY

The next implementation family is M5 human interaction / shared-autonomy integration.

The shared-autonomy decision policy already exists from M1-T09, but the separate human interaction layer is not implemented.

Before authorizing the next task, freeze or explicitly ticket the required command semantics for:

```text
CONFIRM request association / identifiers
stale confirmation rejection
duplicate command handling
OVERRIDE goal validation and authority boundary
PAUSE / STOP propagation
RESUME behavior if included
```

Do not allow Codex to invent these interaction semantics independently.

---

# 6. CURRENT SCIENTIFIC BLOCKERS

Core M4 planning/safety implementation:

```text
None.
```

M5 human interaction:

```text
Requires a narrow approved interaction contract/ticket before implementation.
```

Experimental analysis remains unresolved:

```text
U-034 — Final A/B/C/D component matrix
U-035 — Robustness perturbation levels
U-036 — Final inferential-statistics policy
```

---

# 7. CLAIM STATUS

Authorized implementation claims include that the accepted EEG, Bayesian/shared-autonomy/adaptation modules and M4-T01 through M4-T05 software components have been implemented and unit/regression tested under their approved tickets.

Authorized M4 claim:

```text
the simulated autonomy stack includes a deterministic 2D environment, risk-aware A*, a separate hard-safety controller, safety-gated execution, and event-bounded controlled replanning while preserving the same human-approved goal
```

Not authorized:

```text
claims that any decoder is above chance in a reportable experiment
claims that calibration/Bayesian/shared autonomy/adaptation improves outcomes
claims that planning/replanning/safety improves task outcomes
cross-subject generalization claims
live EEG / physical robot / certified real-world safety claims
```

---

# 8. NEXT ACTION

```text
Project Owner + ChatGPT review and freeze the narrow M5 human-interaction command contract.
Then ChatGPT creates the next explicit CURRENT_TASK.md ticket.
Codex must not start another module before that authorization.
```
