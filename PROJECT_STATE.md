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

Current module:
None — implementation paused at the next replanning/environment-change architecture boundary.

Current task:
None

Task status:
NO ACTIVE IMPLEMENTATION TASK

Canonical branch:
main

Latest accepted task-branch software commit:
1a7ccde578083b3386183a97ca876714afb68e30

Latest accepted software task:
M4-T04 — Planner → Safety → Environment Execution Integration

Latest governance close commit:
318f54804487e02cb69330b98f58637ec85e5dcc

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
Dynamic replanning loop: NOT STARTED / awaiting runtime environment-change contract
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
successful planner output is structurally validated before execution
malformed or substituted plans fail closed with zero movement
```

---

# 4. NEXT ARCHITECTURAL DECISION BOUNDARY

The implementation blueprint still expects replanning, but the accepted environment is intentionally static and M4-T04 intentionally does not implement map mutation or automatic retry loops.

Before a replanning task is authorized, freeze the runtime contract for:

```text
what qualifies as a relevant environment change
how changed blocked/risk state is represented and validated
whether replanning consumes a replacement environment snapshot or another explicit update structure
how current position and the same human-approved goal are preserved
which safety outcomes may request replanning
when a replan is actually attempted
whether retry attempts are bounded
```

D-065 already constrains the outcome:

```text
no route -> NO_SAFE_PATH / no movement
no hard-constraint relaxation
no silent goal substitution
new planning only after relevant environment change or explicit human-approved goal/control change
```

No Codex implementation is authorized until this boundary is explicitly approved and written into a new task ticket.

---

# 5. CURRENT SCIENTIFIC BLOCKERS

Planning / safety implementation:

```text
Runtime environment-change / replanning contract requires Project Owner approval before the next M4 implementation task.
```

Experimental analysis remains unresolved:

```text
U-034 — Final A/B/C/D component matrix
U-035 — Robustness perturbation levels
U-036 — Final inferential-statistics policy
```

These experimental decisions do not affect the accepted M4-T01 through M4-T04 software, but they must be resolved before the corresponding reportable comparison/robustness/inferential experiments.

---

# 6. CLAIM STATUS

Authorized implementation claims include that the accepted EEG, Bayesian/shared-autonomy/adaptation modules and M4-T01 through M4-T04 software components have been implemented and unit/regression tested under their approved tickets.

Authorized M4-T04 implementation claim:

```text
the current simulated execution layer enforces planner -> safety -> environment ordering for one fixed approved goal and fails closed on malformed planner output
```

Not authorized:

```text
claims that any decoder is above chance in a reportable experiment
claims that calibration/Bayesian/shared autonomy/adaptation improves outcomes
claims that risk-aware planning or safety improves outcomes
claims that dynamic replanning is implemented
cross-subject generalization claims
live EEG / physical robot / certified real-world safety claims
```

---

# 7. NEXT ACTION

```text
Project Owner + ChatGPT freeze the runtime environment-change / replanning contract.
Then ChatGPT records the approved decision if needed and creates the next narrow CURRENT_TASK.md ticket.
Codex must not begin another implementation module before that authorization.
```
