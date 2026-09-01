# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex, while retaining the immediately preceding accepted task record.  
**Current status:** ACTIVE / NOT STARTED  
**Current milestone:** M4 — 2D Search & Rescue / A* / Safety  
**Task ID:** M4-T02  
**Task title:** Risk-Aware A* Planner  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Canonical starting commit:** `5310743539675744b284bafdf24789fc2025816d`  
**Last updated:** 2026-09-01

---

# 1. CLOSED TASK RECORD — M4-T01

```text
Task ID:
M4-T01

Task title:
2D Search & Rescue Environment + Risk Map

Final status:
PASS / SCIENTIFICALLY ACCEPTED / MERGED

Task branch:
task/m4-t01-sar-environment-risk-map

Accepted task-branch head / canonical software commit:
5310743539675744b284bafdf24789fc2025816d
```

Accepted M4-T01 behavior:

```text
deterministic single-agent 2D grid environment
consistent (row, column) coordinates
exact action set UP / DOWN / LEFT / RIGHT / WAIT
Gymnasium-compatible Env
Discrete(5) action space
2-integer position observation space
Gymnasium reset/step contracts
neutral reward 0.0
truncated=False in the static core environment
named goal and termination behavior
blocked cells represented separately from risk
canonical risk values 0.00 / 0.25 / 0.50 / 0.75 / 1.00
HIGH 0.75 remains soft/traversable at environment-mechanics level
PROHIBITED 1.00 is identifiable but is not enforced as the safety-controller authority in environment.py
no A*, safety controller, NO_SAFE_PATH control policy, EEG integration, or UI implemented
```

Accepted verification reported from the task branch:

```text
pytest tests/test_environment.py -> 20 passed
pytest -> 150 passed, 1 pre-existing non-failing PyTorch warning
Gymnasium check_env -> passed
```

---

# 2. M4-T02 OBJECTIVE

Implement only the deterministic risk-aware A* planning module downstream of an already approved human goal.

The planner determines HOW to reach the supplied goal. It must never infer, change, rank, or substitute human intent.

M4-T02 implements:

```text
A*
Manhattan heuristic
four-connected path search
D-061 through D-064 risk/constraint semantics
path reconstruction
action reconstruction
explicit NO_SAFE_PATH planning failure
planning cost decomposition and trace metadata
```

M4-T02 does **not** implement the safety controller or execute environment transitions.

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
8. docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md
9. docs/14_SAFETY_CRITICAL_CONTROL.md
10. docs/15_IMPLEMENTATION_BLUEPRINT.md
11. docs/16_REPOSITORY_AND_CODE_ARCHITECTURE.md
12. docs/19_TESTING_AND_VERIFICATION.md
13. src/autonomy/environment.py
14. tests/test_environment.py
```

GitHub `main` is canonical. Do not use an uploaded reference copy in place of current repository code.

---

# 4. GOVERNING APPROVED DECISIONS

M4-T02 must preserve:

```text
D-003 — Human determines WHAT; AI determines HOW safely
D-017 — simple 2D, single-agent, static-first SAR environment
D-018 — environment action vocabulary UP / DOWN / LEFT / RIGHT / WAIT
D-019 — A* with Manhattan heuristic for the four-connected grid
D-020 — planner receives an already approved goal and does not infer intent
D-021 — planner proposes -> safety checks -> environment executes
D-061 — canonical environmental risk values
D-062 — no map-dependent normalization; destination-cell additive risk
D-063 — lambda = 2.0; step_cost = 1.0 + 2.0 * risk(destination)
D-064 — blocked cells and risk >= 1.00 are non-traversable for a valid plan; HIGH 0.75 remains soft risk
D-065 — if no safe route exists, return explicit NO_SAFE_PATH / UNREACHABLE; never weaken hard constraints or silently change goal
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

# 5. ALLOWED FILES

Primary authorized files:

```text
src/autonomy/planner.py
tests/test_planner.py
```

Only if necessary for exports/imports:

```text
src/autonomy/__init__.py
```

Do not modify `src/autonomy/environment.py` unless a genuine integration defect prevents the planner from consuming the already accepted M4-T01 interface. If such a defect is found, stop and report it rather than silently redesigning M4-T01.

No other source files are authorized.

---

# 6. PLANNER INPUT CONTRACT

The planner must receive explicit planning inputs and must not depend on EEG/cognitive/shared-autonomy internals.

Minimum planning request semantics:

```text
start: (row, column)
approved_goal: (row, column)
map dimensions / environment map access
blocked cells
risk map
risk lambda fixed to approved 2.0 for the primary planner
optional map_id / request_id metadata if useful and non-invasive
```

The planner may accept the immutable/configuration aspects of the accepted `SearchRescueEnvironment` or an explicit planner request derived from it, but it must not mutate environment state during planning.

Do not accept raw EEG, decoder probabilities, Bayesian posterior, uncertainty, or adaptation state as planner inputs.

---

# 7. A* SEARCH SEMANTICS

Use deterministic four-connected A*.

Movement candidates:

```text
UP    -> (r-1, c)
DOWN  -> (r+1, c)
LEFT  -> (r, c-1)
RIGHT -> (r, c+1)
```

`WAIT` is part of the environment action vocabulary but must not be expanded as a progress edge in ordinary A* path search.

A valid planner path must not contain:

```text
out-of-bounds cells
blocked cells
cells with canonical risk >= 1.00
```

HIGH risk `0.75` remains traversable and is handled through soft cost.

---

# 8. COST FUNCTION

For each entered destination cell:

```text
movement_cost_increment = 1.0
risk_exposure_increment = risk(destination_cell)
weighted_risk_cost_increment = 2.0 * risk(destination_cell)
step_cost = 1.0 + 2.0 * risk(destination_cell)
```

For the complete returned path:

```text
movement_cost = number of moves
cumulative_risk = sum of destination-cell risk over entered cells
risk_cost = 2.0 * cumulative_risk
path_cost = movement_cost + risk_cost
```

The start cell is not charged again as movement/risk exposure merely for being the start.

No per-map risk normalization, learned weighting, adaptive lambda, or hidden extra penalty is permitted.

---

# 9. HEURISTIC

Use Manhattan distance:

```text
h((r,c), goal) = abs(r-goal_r) + abs(c-goal_c)
```

The heuristic must not include hidden risk estimates.

With non-negative risk and minimum step cost 1.0, Manhattan distance remains the primary lower-bound heuristic for this four-connected planner.

---

# 10. DETERMINISM / TIE BREAKING

Equal-cost searches must resolve deterministically.

Use a fixed neighbor expansion order:

```text
UP
DOWN
LEFT
RIGHT
```

Use a stable priority-queue tie-break mechanism so repeated identical requests produce identical paths.

This is an implementation reproducibility convention only; it must not alter the scientific risk/cost model.

---

# 11. PLANNER OUTPUT CONTRACT

Return an explicit structured planning result containing at least:

```text
status
start
goal
path
actions
path_cost
movement_cost
cumulative_risk
risk_cost
expanded_nodes
```

Success path semantics:

```text
path begins with start
path ends with approved_goal
actions reconstruct every transition between consecutive path coordinates
len(actions) = max(len(path)-1, 0)
```

Minimum statuses:

```text
SUCCESS
NO_SAFE_PATH
INVALID_START
INVALID_GOAL
```

A status may use a typed enum/string representation as long as behavior is explicit and tested.

Do not silently return an empty path for every failure without a status explaining why.

---

# 12. START / GOAL VALIDATION

Before search:

Start must:

```text
be a valid (row, column) coordinate
be in bounds
not be blocked
not have risk >= 1.00
```

Goal must:

```text
be a valid (row, column) coordinate
be in bounds
not be blocked
not have risk >= 1.00
match the explicitly supplied approved goal for the request
```

The planner must not choose another goal when the supplied goal is invalid or unreachable.

If `start == goal` and the cell is valid:

```text
status = SUCCESS
path = [start]
actions = []
movement_cost = 0
cumulative_risk = 0
risk_cost = 0
path_cost = 0
```

---

# 13. NO-SAFE-PATH SEMANTICS IN THIS TASK

If A* exhausts all permitted paths without reaching the supplied approved goal:

```text
status = NO_SAFE_PATH
path = []
actions = []
```

The planner must not:

```text
relax risk >= 1.00 prohibition
ignore blocked cells
teleport
switch to another goal
execute WAIT or movement as a fallback
mutate the environment
```

Holding the agent stationary and deciding when replanning may occur belongs to later planner/safety/control integration; M4-T02 only returns the explicit planning failure.

---

# 14. ARCHITECTURAL BOUNDARY

`src/autonomy/planner.py` may depend on environment map/configuration semantics.

It must not depend on:

```text
src/eeg/*
src/models/*
src/cognitive/*
shared-autonomy thresholds
human feedback adaptation
Streamlit/UI
```

The planner must not call `env.step()` to search a route. Planning is computation over map state/configuration, not execution.

The planner must not implement safety-controller authorization records or emergency-stop behavior.

---

# 15. TEST REQUIREMENTS

Add focused tests covering at least:

```text
zero-risk shortest path
Manhattan heuristic values
path/action reconstruction
start == goal
blocked cells never appear in path
PROHIBITED risk 1.00 never appears in path
HIGH risk 0.75 remains traversable
risk-aware route trade-off: a longer lower-risk route can beat a shorter higher-risk route under lambda 2.0
cost decomposition matches movement + 2.0*cumulative_risk
start cell is not double-charged
invalid/out-of-bounds start -> INVALID_START
blocked/prohibited start -> INVALID_START
invalid/out-of-bounds goal -> INVALID_GOAL
blocked/prohibited goal -> INVALID_GOAL
fully separated goal -> NO_SAFE_PATH
planner never changes the supplied goal
deterministic identical request -> identical path and actions
planning does not mutate the environment state
WAIT is not introduced into a successful A* route
```

Use small synthetic maps with manually checkable expected results.

Do not claim system-level safety or task-performance improvement from unit tests.

---

# 16. REGRESSION REQUIREMENT

Run at minimum:

```text
pytest tests/test_planner.py
pytest tests/test_environment.py tests/test_planner.py
pytest
```

Report exact results.

The previously accepted non-failing PyTorch warning may remain if unchanged.

---

# 17. OUT OF SCOPE / FORBIDDEN

Do not implement in M4-T02:

```text
safety controller
action authorization or rejection during execution
human PAUSE / STOP execution logic
shared-controller integration
replanning triggers/event loop
map mutation/dynamic hazards
EEG replay integration
Bayesian/shared-autonomy integration
Streamlit/UI
autonomy metrics/experiments
A/B/C/D experiments
robustness perturbations
reinforcement learning
Dijkstra as an alternative production planner
multiple lambda variants or lambda tuning
3D or continuous-space planning
```

Do not modify D-061 through D-065.

---

# 18. ACCEPTANCE CRITERIA

M4-T02 may be reported `PASS` only if:

```text
deterministic A* implemented
Manhattan heuristic implemented
four-connected movement only
risk-aware step/path cost exactly follows D-062/D-063
blocked and risk >= 1.00 cells excluded from valid plans
HIGH 0.75 remains soft/traversable
structured SUCCESS / NO_SAFE_PATH / invalid-input outcomes implemented
path and action reconstruction implemented
cost decomposition exposed and correct
planner does not mutate environment or execute steps
focused planner tests pass
accepted environment tests remain passing
full regression suite is run and reported
no safety/shared-autonomy/EEG scope added
```

---

# 19. STOP CONDITIONS

Stop and report `BLOCKED` if:

```text
accepted M4-T01 environment interface cannot support planner map queries without changing scientific semantics
canonical docs/code conflict on coordinate, risk, or blocked-cell semantics
implementation requires a new risk value or lambda
implementation requires safety-controller behavior to define a valid A* result
implementation would need to modify unrelated accepted modules
```

Do not resolve such conflicts independently.

---

# 20. COMPLETION REPORT

Codex must report:

```text
Status
Branch
Commit SHA
Files created
Files modified
Planner API
Cost function implemented
Tie-breaking convention
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

Do not merge and do not begin the safety-controller task until ChatGPT scientific review and Project Owner acceptance.
