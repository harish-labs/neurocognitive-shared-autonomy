# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex, while retaining the immediately preceding accepted task record.  
**Current status:** ACTIVE / NOT STARTED  
**Current milestone:** M4 — 2D Search & Rescue / A* / Safety  
**Task ID:** M4-T03  
**Task title:** Safety Controller / Hard Constraint Enforcement  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Canonical starting commit:** `c224a4dfb3684d0d4555d7a606a90dc822571c11`  
**Last updated:** 2026-09-01

---

# 1. CLOSED TASK RECORD — M4-T02

```text
Task ID:
M4-T02

Task title:
Risk-Aware A* Planner

Final status:
PASS / SCIENTIFICALLY ACCEPTED / MERGED

Task branch:
task/m4-t02-risk-aware-a-star-planner

Accepted task-branch head / canonical software commit:
c224a4dfb3684d0d4555d7a606a90dc822571c11
```

Accepted M4-T02 behavior:

```text
deterministic four-connected A*
fixed neighbor order UP / DOWN / LEFT / RIGHT
stable priority-queue tie breaking
Manhattan heuristic
explicit caller-supplied approved goal
no EEG / Bayesian / shared-autonomy input
blocked cells excluded
risk >= 1.00 excluded
HIGH 0.75 remains traversable soft risk
lambda = 2.0
step_cost = 1.0 + 2.0 * risk(destination)
start cell not double charged
path/action reconstruction
movement_cost / cumulative_risk / risk_cost / path_cost decomposition
SUCCESS / INVALID_START / INVALID_GOAL / NO_SAFE_PATH outcomes
planner does not mutate or step the environment
WAIT not expanded as a search edge
no safety-controller behavior, replanning loop, execution, or UI added
```

Accepted verification reported from the task branch:

```text
pytest tests/test_planner.py -> 18 passed
pytest tests/test_environment.py tests/test_planner.py -> 38 passed
pytest -> 168 passed, 1 pre-existing non-failing PyTorch warning
```

Scientific review also verified that the branch was one clean commit ahead of canonical main and changed only:

```text
src/autonomy/planner.py
tests/test_planner.py
```

---

# 2. M4-T03 OBJECTIVE

Implement only the deterministic safety-controller authority layer that validates a proposed single environment action before execution.

The governing rule is:

```text
planner proposes
→ safety controller authorizes/rejects
→ environment executes only if approved
```

M4-T03 implements hard safety checks and explicit safety decisions only.

M4-T03 must **not** execute `env.step()`, run A* search, infer human intent, or implement the later full execution/replanning loop.

---

# 3. READ FIRST

Codex must read, in this order:

```text
1. MASTER_PROJECT_SPEC.md
2. AGENTS.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. CURRENT_TASK.md
6. docs/03_SEARCH_AND_RESCUE_SCENARIO.md
7. docs/04_SYSTEM_ARCHITECTURE.md
8. docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md
9. docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md
10. docs/14_SAFETY_CRITICAL_CONTROL.md
11. docs/15_IMPLEMENTATION_BLUEPRINT.md
12. docs/16_REPOSITORY_AND_CODE_ARCHITECTURE.md
13. docs/19_TESTING_AND_VERIFICATION.md
14. src/autonomy/environment.py
15. src/autonomy/planner.py
16. tests/test_environment.py
17. tests/test_planner.py
```

GitHub `main` is canonical.

---

# 4. GOVERNING APPROVED DECISIONS

M4-T03 must preserve:

```text
D-003 — Human determines WHAT; AI determines HOW safely
D-016 — human CONFIRM / OVERRIDE / PAUSE / STOP controls exist; human stop cannot be bypassed
D-018 — approved action vocabulary UP / DOWN / LEFT / RIGHT / WAIT
D-021 — planner proposes -> safety controller checks -> environment executes only if approved
D-056 — human PAUSE / STOP / OVERRIDE take precedence over normal autonomy policy
D-057 — unresolved uncertainty holds position; no autonomous movement
D-061 — canonical risk values
D-064 — risk >= 1.00 is prohibited; HIGH 0.75 remains traversable soft risk; blocked cells independently prohibited
D-065 — hard safety constraints must never be relaxed to obtain movement/path
```

For this task, safety enforcement is simulated software safety only; no real-world certification claim is authorized.

---

# 5. ALLOWED FILES

Primary authorized files:

```text
src/autonomy/safety.py
tests/test_safety.py
```

Only if required for package exports/imports:

```text
src/autonomy/__init__.py
```

Do not modify accepted `environment.py` or `planner.py` unless a genuine integration defect prevents the safety controller from reading their existing public semantics. If so, stop and report the blocker rather than redesigning them silently.

No unrelated source files are authorized.

---

# 6. SAFETY INPUT CONTRACT

The safety controller must evaluate one proposed action against the current environment/map state and explicit human-control state.

Minimum request/input semantics:

```text
current_position
proposed_action
environment/map access
paused: bool
emergency_stop: bool
```

The controller may derive the proposed next coordinate deterministically using the accepted action semantics.

It must not require:

```text
raw EEG
decoder probability
Bayesian posterior
entropy
adaptation state
planner path cost
Streamlit/UI state
```

The safety decision must be independent of model confidence.

---

# 7. SAFETY OUTPUT CONTRACT

Return an explicit structured immutable/read-only decision containing at least:

```text
status
proposed_action
approved_action
safe
intervention_type
reason
requires_replan
current_position
proposed_next_position
```

Recommended statuses:

```text
APPROVED
REJECTED
REPLAN_REQUIRED
HALTED
```

Recommended intervention categories, matching the safety specification:

```text
NONE
OUT_OF_BOUNDS
BLOCKED_CELL
PROHIBITED_HAZARD
PAUSED
EMERGENCY_STOP
INVALID_ACTION
INVALID_STATE
```

Exact enum class names may differ, but semantics must remain explicit and tested.

For any non-approved result:

```text
approved_action = None
```

The controller must never substitute another movement action automatically.

---

# 8. REQUIRED PRECEDENCE / CHECK ORDER

Use deterministic safety precedence:

```text
1. emergency stop
2. paused
3. current state / current position validity
4. proposed action validity
5. proposed next position within bounds
6. blocked-cell check
7. prohibited-hazard check
8. approve
```

Higher-priority conditions must dominate lower-priority ones.

Examples:

```text
emergency_stop=True + otherwise-valid RIGHT -> HALTED / EMERGENCY_STOP
paused=True + proposed blocked-cell move -> PAUSED result, not BLOCKED_CELL
out-of-bounds move -> rejected before any risk lookup outside the map
```

The exact status mapping between `REJECTED`, `REPLAN_REQUIRED`, and `HALTED` must follow the rules below.

---

# 9. HUMAN STOP / PAUSE

## Emergency stop

If `emergency_stop=True`:

```text
status = HALTED
safe = False
approved_action = None
intervention = EMERGENCY_STOP
requires_replan = False
```

No movement action, including `WAIT`, is approved while emergency stop is active.

## Pause

If `paused=True` and emergency stop is not active:

```text
status = HALTED
safe = False
approved_action = None
intervention = PAUSED
requires_replan = False
```

Pause is reversible, but M4-T03 does not implement resume/event-loop behavior.

---

# 10. CURRENT STATE VALIDATION

Before evaluating movement, current position must:

```text
be a valid (row, column) integer coordinate
be in bounds
not be blocked
not have risk >= 1.00
```

If critical current state is invalid:

```text
status = HALTED
safe = False
approved_action = None
intervention = INVALID_STATE
requires_replan = False
```

This is the fail-safe default for malformed/unsafe current state.

---

# 11. ACTION VALIDATION

Approved action vocabulary remains exactly:

```text
UP
DOWN
LEFT
RIGHT
WAIT
```

Invalid action:

```text
status = REJECTED
safe = False
approved_action = None
intervention = INVALID_ACTION
requires_replan = False
```

The controller must not coerce arbitrary values into another action.

Using the already accepted numeric Gymnasium action representation is permitted only when it maps exactly to the accepted `Action` enum.

---

# 12. WAIT SEMANTICS

If emergency stop/pause are inactive and current state is valid:

```text
WAIT
```

produces the same proposed next position as current position and is safety-approved.

WAIT must still fail if the current state itself is invalid.

WAIT does not itself request replanning.

---

# 13. OUT-OF-BOUNDS

For UP/DOWN/LEFT/RIGHT, derive the proposed next coordinate using accepted row/column deltas.

If next position is outside map bounds:

```text
status = REJECTED
safe = False
approved_action = None
intervention = OUT_OF_BOUNDS
requires_replan = True
```

The safety controller must not call a risk lookup on an out-of-bounds coordinate.

---

# 14. BLOCKED CELL

If proposed next position is in `blocked_cells`:

```text
status = REPLAN_REQUIRED
safe = False
approved_action = None
intervention = BLOCKED_CELL
requires_replan = True
```

Do not execute or substitute another move.

---

# 15. PROHIBITED HAZARD

If proposed next position has canonical risk >= 1.00:

```text
status = REPLAN_REQUIRED
safe = False
approved_action = None
intervention = PROHIBITED_HAZARD
requires_replan = True
```

HIGH risk `0.75` remains safety-permitted and must not be rejected merely because it is high soft risk.

No lower risk threshold may be invented.

---

# 16. APPROVAL

If none of the hard constraints trigger:

```text
status = APPROVED
safe = True
approved_action = proposed_action
intervention = NONE
requires_replan = False
```

The returned approved action must be exactly the proposed action; the safety controller may approve or reject, but may not optimize or substitute.

---

# 17. ARCHITECTURAL BOUNDARY

`src/autonomy/safety.py` may depend on accepted environment action/map semantics.

It must not:

```text
call environment.step()
run A*
modify environment state
modify planner output
infer or change approved goal
inspect EEG or model probabilities
inspect Bayesian posterior/entropy
adapt thresholds
perform human override goal selection
implement full replanning
implement Streamlit/UI
```

`requires_replan=True` is only a decision flag in M4-T03. A later integration task will decide how to invoke replanning.

---

# 18. TEST REQUIREMENTS

Add focused deterministic tests covering at least:

```text
valid low/free-risk move -> APPROVED
HIGH 0.75 move -> APPROVED
WAIT on valid state -> APPROVED and same next position
emergency stop overrides valid movement
emergency stop has priority over pause/lower safety conditions
pause blocks valid movement
pause has priority over blocked/prohibited checks
invalid current coordinate -> INVALID_STATE / HALTED
blocked current state -> INVALID_STATE / HALTED
prohibited current state -> INVALID_STATE / HALTED
invalid action -> INVALID_ACTION
out-of-bounds move -> OUT_OF_BOUNDS and no crash/risk lookup
blocked destination -> BLOCKED_CELL + requires_replan
prohibited destination -> PROHIBITED_HAZARD + requires_replan
approved_action is None for all non-approved outcomes
approved action is exactly proposed action for APPROVED
safety check does not mutate environment state
safety controller never calls env.step()
identical request -> identical decision
```

Use small synthetic maps and manually checkable expectations.

No unit test may be described as proof of real-world safety or system-level safety improvement.

---

# 19. REGRESSION REQUIREMENT

Run at minimum:

```text
pytest tests/test_safety.py
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py
pytest
```

Report exact results.

The existing pre-non-failing PyTorch warning may remain if unchanged.

---

# 20. OUT OF SCOPE / FORBIDDEN

Do not implement in M4-T03:

```text
full planner -> safety -> environment execution loop
automatic call to planner when requires_replan=True
replanning trigger/event manager
shared-controller integration
CONFIRM/DEFER state-machine integration
OVERRIDE goal-selection semantics
EEG replay
Bayesian integration
human-interface UI
Streamlit
logging/metrics experiment framework
A/B/C/D experiments
robustness perturbations
dynamic hazards
reinforcement learning
real-world safety claims
```

---

# 21. ACCEPTANCE CRITERIA

M4-T03 may be reported `PASS` only if:

```text
safety controller implemented as a separate authority layer
emergency stop and pause have explicit highest-priority handling
current-state fail-safe validation implemented
invalid action handled explicitly
out-of-bounds / blocked / prohibited destination checks implemented
HIGH 0.75 remains permitted
WAIT is permitted only when current state is valid and controls are not halted
structured decision and intervention outputs implemented
approved_action never substituted
requires_replan semantics implemented without invoking planner
controller does not call env.step() or mutate environment
focused tests pass
environment + planner + safety combined tests pass
full regression suite run and reported
no integration/shared-autonomy/EEG/UI scope added
```

---

# 22. STOP CONDITIONS

Stop and report `BLOCKED` if:

```text
accepted environment action/map interface cannot support safety checks without changing scientific semantics
canonical docs/decisions conflict on hard-safety precedence
implementation requires a new hazard threshold
implementation requires automatic replanning or environment execution to define a safety decision
implementation requires changes to unrelated accepted modules
```

Do not resolve such conflicts independently.

---

# 23. COMPLETION REPORT

Codex must report:

```text
Status
Branch
Commit SHA
Files created
Files modified
Safety API
Check order / precedence
Intervention/status mapping
Tests added
Tests executed
Exact test results
Manual/synthetic checks
Known limitations
Open blockers
Scope confirmation
```

After implementing, testing, committing, and pushing the task branch:

```text
STOP
```

Do not merge and do not begin planner/safety/environment integration until ChatGPT scientific review and Project Owner acceptance.
