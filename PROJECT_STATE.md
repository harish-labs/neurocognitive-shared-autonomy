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
M4-T01 through M4-T05 are accepted and merged; the core M4 autonomy stack is complete.
D-067 Human Interaction Command Contract is approved.
M5-T01 Human Command & Confirmation State Layer is authorized and not yet implemented.

Current module:
Human command / confirmation state layer

Current task:
M5-T01

Task status:
ACTIVE / NOT STARTED

Canonical branch:
main

Latest accepted task-branch software commit:
e8183ccebc9c2f67a1b33347b9ef12d25ddbcbfe

Latest accepted software task:
M4-T05 — Controlled Replanning After Environment Change

Latest approved scientific/architectural decision commit:
0c2ed84207f55303610d8b7c61bd9e99eea8301a

Latest task-authorization commit:
77bb58a8207af007a5f7e2a03791c0ea6e5624c9

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

# 3. CURRENT AUTONOMY / INTERACTION STATE

```text
SAR environment/risk map: PASS
Risk-aware A*: PASS
Hard safety controller: PASS
Planner -> safety -> environment execution integration: PASS
Controlled replanning after explicit environment change: PASS
Shared-autonomy decision policy: PASS (accepted M1-T09)
Human command / confirmation state layer: AUTHORIZED / NOT STARTED
Shared-autonomy -> human-command integration: NOT STARTED
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
```

Accepted control principles now include:

```text
human determines WHAT goal; AI determines HOW safely
CONFIRM is explicit human authority when required
STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > autonomous policy
safety retains veto authority over low-level movement
stale/duplicate human commands must not create repeated effects
RESUME is explicit and never replays an old queued action
OVERRIDE changes the human-approved goal but does not bypass planner/safety
```

---

# 4. M4 MILESTONE STATE

Core M4 implementation is accepted and closed:

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

# 5. D-067 — HUMAN INTERACTION CONTRACT

Approved on 2026-09-01:

```text
unique request_id for every confirmation request
CONFIRM only the exact active request; stale/consumed requests rejected
unique command_id consumed at most once
duplicate command IDs cause no repeated effect
OVERRIDE validates a currently valid mission goal and becomes human-approved goal
OVERRIDE cannot bypass planner/safety and cannot silently resume PAUSE
PAUSE preserves state and blocks movement until explicit RESUME
STOP is terminal for the interaction session until explicit reset/new episode
RESUME is valid only from PAUSED, preserves goal, and requires fresh downstream execution rather than queued-action replay
command handling is synchronous/deterministic; no background queue
```

D-067 is implemented only when M5-T01 is separately completed and accepted. Approval alone is not an implementation claim.

---

# 6. CURRENT SCIENTIFIC / ARCHITECTURAL BLOCKERS

M5-T01:

```text
No unresolved scientific blocker under D-067.
```

Later M5 integration:

```text
Not authorized yet. Integration of shared-autonomy decisions with the human-command layer must be separately reviewed after M5-T01 acceptance.
```

Experimental analysis remains unresolved:

```text
U-034 — Final A/B/C/D component matrix
U-035 — Robustness perturbation levels
U-036 — Final inferential-statistics policy
```

These do not block M5-T01.

---

# 7. CLAIM STATUS

Authorized implementation claims include that M1-T01 through M1-T10 and M4-T01 through M4-T05 have been implemented, reviewed, accepted, and regression tested under their approved tickets.

Not yet authorized as implementation claims:

```text
human command / confirmation state layer implemented
full human-interaction integration implemented
end-to-end EEG-driven mission execution implemented
any reportable performance/safety improvement
cross-subject generalization
live EEG / physical robot / certified real-world safety
```

---

# 8. NEXT ACTION

```text
Codex implements M5-T01 exactly as defined in CURRENT_TASK.md on a task branch from the current main.
Implement only the deterministic human command / confirmation state layer.
Run focused, adjacent-control, and full regression tests.
Commit/push and stop for ChatGPT scientific/architectural review.
Do not merge or begin the next M5 integration task automatically.
```
