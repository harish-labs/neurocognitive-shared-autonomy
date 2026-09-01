# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex  
**Current status:** ACTIVE / NOT STARTED  
**Current milestone:** M4 — 2D Search & Rescue / A* / Safety  
**Task ID:** M4-T01  
**Task title:** 2D Search & Rescue Environment + Risk Map  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Authorized from governance commit:** `fdef1d5afaf7d13aaffb0e8d5b39379497ee7442`  
**Last updated:** 2026-09-01

---

# 1. TASK OBJECTIVE

Implement only the deterministic 2D Search & Rescue environment and canonical risk-map representation required by the approved architecture and D-061 through D-065.

This task establishes world state and environment transitions only.

Do **not** implement A* planning or the safety controller in M4-T01.

---

# 2. READ FIRST

Codex must read, in this order:

```text
1. MASTER_PROJECT_SPEC.md
2. AGENTS.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. docs/03_SEARCH_AND_RESCUE_SCENARIO.md
6. docs/04_SYSTEM_ARCHITECTURE.md
7. docs/05_TECHNOLOGY_STACK.md
8. docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md
9. docs/14_SAFETY_CRITICAL_CONTROL.md
10. docs/15_IMPLEMENTATION_BLUEPRINT.md
11. docs/16_REPOSITORY_AND_CODE_ARCHITECTURE.md
12. docs/19_TESTING_AND_VERIFICATION.md
```

If repository paths differ, inspect the actual repository and preserve the approved architecture rather than inventing a new package structure.

---

# 3. GOVERNING APPROVED DECISIONS

M4-T01 must preserve:

```text
D-003 — Human determines WHAT; AI determines HOW safely
D-017 — simple 2D, single-agent, static-first SAR environment
D-018 — action space UP / DOWN / LEFT / RIGHT / WAIT
D-019 — A* is the later approved planner; do not implement it here
D-021 — planner -> safety -> environment execution architecture; do not collapse layers
D-061 — canonical environmental risk values
D-062 — fixed normalization / destination-cell additive risk semantics
D-063 — lambda = 2.0 is approved for later planner use; environment may expose risk but must not perform planning
D-064 — risk >= 1.00 is prohibited; blocked cells remain a distinct hard category
D-065 — NO_SAFE_PATH policy is approved for later planner/safety integration; do not implement planner fallback here
```

Canonical risk scale:

```text
FREE       = 0.00
LOW        = 0.25
MODERATE   = 0.50
HIGH       = 0.75
PROHIBITED = 1.00
```

---

# 4. ALLOWED FILES

Primary authorized files:

```text
src/autonomy/environment.py
tests/test_environment.py
```

Only if required by the repository/package structure:

```text
src/autonomy/__init__.py
requirements.txt
```

`requirements.txt` may add Gymnasium only if it is not already available through the project environment and is required for this implementation.

Do not modify unrelated EEG, model, cognitive, calibration, or shared-autonomy implementation files.

---

# 5. REQUIRED ENVIRONMENT MODEL

Implement a small deterministic 2D grid environment compatible with the approved Gymnasium direction.

Minimum state/configuration must support:

```text
grid dimensions
agent start/current position
one or more named goal positions
blocked cells
risk map using only D-061 canonical values
current termination state
seeded reset where applicable
```

The environment must preserve a single coordinate convention consistently across state, actions, tests, and returned information.

Preferred convention from the planning specification:

```text
(row, column)
```

Do not silently mix `(x, y)` with `(row, column)`.

---

# 6. ACTION SEMANTICS

Supported actions only:

```text
UP
DOWN
LEFT
RIGHT
WAIT
```

Conceptually:

```text
UP    -> (r-1, c)
DOWN  -> (r+1, c)
LEFT  -> (r, c-1)
RIGHT -> (r, c+1)
WAIT  -> (r, c)
```

The environment must expose deterministic action/state-transition semantics suitable for later safety-controller integration.

M4-T01 must not create low-level EEG joystick control; these are environment actions only.

---

# 7. RISK / HAZARD REPRESENTATION

The environment must validate and expose canonical cell risk values exactly as approved:

```text
0.00
0.25
0.50
0.75
1.00
```

Requirements:

```text
- no per-map normalization
- no adaptive rescaling
- blocked cells are represented separately from risk values
- PROHIBITED risk = 1.00 is explicitly identifiable
- HIGH risk = 0.75 remains a distinct value and must not be silently converted to blocked
- risk metadata must be queryable by later planner/safety code
```

Do not apply lambda or compute A* path cost in this environment task.

---

# 8. TRANSITION BOUNDARY FOR THIS TASK

Because the final architecture requires the safety controller to authorize execution, M4-T01 must keep environment mechanics separable from safety policy.

The environment may provide deterministic transition helpers and must reject structurally invalid environment operations such as malformed actions/configuration.

Do **not** implement the future safety controller's policy logic in `environment.py`.

In particular, do not add autonomous policy decisions, goal substitution, planner behavior, Bayesian logic, or shared-autonomy thresholds here.

---

# 9. RESET / TERMINATION

At minimum:

```text
reset restores the configured start state deterministically
reaching a configured goal may terminate the environment episode
WAIT leaves position unchanged
state returned after each transition is internally consistent
```

Do not invent rescue physiology, triage mechanics, reward shaping, dynamic hazards, stochastic movement, or multi-agent behavior.

---

# 10. VALIDATION REQUIREMENTS

Reject or clearly fail on invalid configuration, including where practical:

```text
non-positive grid dimensions
start outside grid
start on blocked cell
blocked cell outside grid
goal outside grid
invalid risk-map coordinate
risk value outside the approved canonical set
invalid/unknown action
```

Do not silently coerce arbitrary risk values into the nearest approved level.

---

# 11. TEST REQUIREMENTS

Add focused deterministic tests covering at least:

```text
reset to configured start
UP/DOWN/LEFT/RIGHT transitions
WAIT transition
coordinate convention consistency
goal/termination behavior
blocked-cell representation distinct from risk
risk values 0.00 / 0.25 / 0.50 / 0.75 / 1.00 preserved exactly
invalid arbitrary risk value rejected
PROHIBITED = 1.00 identifiable without converting HIGH = 0.75 to prohibited
invalid action rejected
invalid map coordinates/config rejected
seeded reset deterministic where seed is exposed
```

Tests must not pretend that planner or safety behavior exists yet.

---

# 12. REGRESSION REQUIREMENT

Run the new environment tests plus the existing accepted suite sufficiently to demonstrate M4-T01 does not break M1-T01 through M1-T10.

At minimum report:

```text
pytest tests/test_environment.py
pytest
```

If the full suite cannot run because of an environment/dependency issue, report the exact blocker rather than claiming PASS.

---

# 13. OUT OF SCOPE / FORBIDDEN

Do not implement in M4-T01:

```text
A* planner
Manhattan-search algorithm
lambda-weighted path selection
path replanning
safety controller
PROHIBITED transition rejection as a separate safety authority layer
NO_SAFE_PATH planner policy
autonomous goal switching
shared-autonomy integration
EEG integration
offline replay
Streamlit/UI
reward optimization or reinforcement learning
dynamic hazards
multi-agent simulation
3D simulation
```

The environment may expose enough map/state information for these later modules, but must not absorb them.

---

# 14. ACCEPTANCE CRITERIA

Task may be reported `PASS` only if:

```text
2D deterministic SAR environment implemented
approved five-level risk representation implemented exactly
blocked cells remain distinct from risk
approved action space implemented exactly
configuration validation implemented
focused tests added and passed
full existing regression suite executed and reported
no planner/safety/shared-autonomy scope added
no scientific values beyond D-061 through D-065 invented
```

---

# 15. STOP CONDITIONS

Stop and report `BLOCKED` if:

```text
existing repository structure makes the prescribed module location materially ambiguous
Gymnasium dependency cannot be installed/used in the accepted environment
an approved environment/risk decision conflicts with actual canonical code
implementation would require changing D-061 through D-065
implementation would require planner or safety policy to make the environment valid
```

Do not redesign the architecture to bypass a blocker.

---

# 16. COMPLETION REPORT

Codex must report:

```text
Status
Branch
Commit SHA
Files created
Files modified
Implementation completed
Tests added
Tests executed
Exact test results
Dependency changes
Manual checks
Known limitations
Open blockers
Scope confirmation
```

After implementing, testing, committing, and pushing the task branch:

```text
STOP
```

Do not merge and do not begin M4-T02 until ChatGPT scientific review and Project Owner acceptance.
