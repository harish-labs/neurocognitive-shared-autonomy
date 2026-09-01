# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex.  
**Current status:** ACTIVE / NOT STARTED  
**Current milestone:** M4 — 2D Search & Rescue / A* / Safety  
**Task ID:** M4-T05  
**Task title:** Controlled Replanning After Environment Change  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Canonical starting commit:** `5f3a1ed66ee1140766cc73c174dbcab790110596`  
**Last updated:** 2026-09-01

---

# 1. CLOSED TASK RECORD — M4-T04

```text
Task ID: M4-T04
Task title: Planner → Safety → Environment Execution Integration
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Task branch: task/m4-t04-execution-integration
Accepted corrected task-branch head / canonical software commit:
1a7ccde578083b3386183a97ca876714afb68e30
```

Accepted M4-T04 behavior includes:

```text
one fixed already-approved goal
planner SUCCESS output fail-closed validated before movement
SafetyController.check before every env.step()
NO_SAFE_PATH / PAUSE / STOP cause no movement
malformed/substituted plans cause INVALID_GOAL_OR_PLAN with zero movement
no automatic replanning or hidden map mutation
```

Accepted verification:

```text
pytest tests/test_execution.py -> 13 passed
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py tests/test_execution.py -> 71 passed
pytest -> 201 passed, 1 pre-existing non-failing PyTorch warning
```

---

# 2. OBJECTIVE

Implement only a deterministic controlled replanning coordinator for a previously approved SAR goal after an explicit, validated runtime environment change.

The coordinator must preserve the architecture:

```text
same human-approved goal
+ current agent position
+ explicit environment-change event
+ new validated replacement environment snapshot
        ↓
controlled replan attempt
        ↓
existing planner → safety → environment executor
```

M4-T05 must not introduce spontaneous map mutation, repeated retry loops, goal substitution, or new scientific policy.

---

# 3. READ FIRST

Codex must read, in this order:

```text
1. MASTER_PROJECT_SPEC.md
2. AGENTS.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. CURRENT_TASK.md
6. docs/04_SYSTEM_ARCHITECTURE.md
7. docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md
8. docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md
9. docs/14_SAFETY_CRITICAL_CONTROL.md
10. docs/15_IMPLEMENTATION_BLUEPRINT.md
11. docs/16_REPOSITORY_AND_CODE_ARCHITECTURE.md
12. docs/19_TESTING_AND_VERIFICATION.md
13. src/autonomy/environment.py
14. src/autonomy/planner.py
15. src/autonomy/safety.py
16. src/autonomy/execution.py
17. relevant accepted tests
```

GitHub `main` is canonical.

---

# 4. GOVERNING DECISIONS

Preserve D-003, D-016, D-018 through D-021, D-056, D-057, D-061 through D-065, and especially:

```text
D-066 — Controlled Replanning / Runtime Environment-Change Contract
```

D-066 requires:

```text
new immutable validated replacement environment/map snapshot for each relevant change
preserve current (row,column) position
preserve the same human-approved goal
replan only after explicit ENVIRONMENT_CHANGED, or requires_replan=True together with a new validated snapshot
never repeatedly replan against an unchanged map
at most one replan per supplied environment-change event
another replan requires another explicit change event/new snapshot
replacement snapshot NO_SAFE_PATH -> hold and stop
PAUSE/STOP remain higher priority and do not themselves trigger replanning
no goal substitution
no hard-safety relaxation
no hidden map mutation
no invented stochastic/dynamic hazard process
```

---

# 5. ALLOWED FILES

Primary authorized files:

```text
src/autonomy/replanning.py
tests/test_replanning.py
```

Only if necessary for package exports/imports:

```text
src/autonomy/__init__.py
```

Do not modify accepted:

```text
src/autonomy/environment.py
src/autonomy/planner.py
src/autonomy/safety.py
src/autonomy/execution.py
src/control/shared_autonomy.py
```

If the accepted public interfaces cannot support this task without changing their semantics, stop and report `BLOCKED`.

---

# 6. REPLACEMENT SNAPSHOT CONTRACT

Use a fresh `SearchRescueEnvironment` instance as the replacement snapshot.

Before a replan attempt, validate that the replacement environment:

```text
is a distinct environment instance from the current environment
has the same grid rows and columns
has the same named goal mapping
contains the exact supplied approved_goal at the same configured goal coordinate
uses replacement.config.start == current_environment.state.position
therefore begins at the preserved current agent position
has a valid, non-terminated initial state at that position
preserves all accepted EnvironmentConfig validation rules
has a genuinely changed blocked-cell set and/or risk map relative to the current environment
```

Do not mutate the current environment in place.

Do not copy or carry an old terminated state into the replacement environment.

The replacement environment may subsequently advance only through the already accepted execution path after the replan is authorized.

---

# 7. REPLAN TRIGGERS

Support exactly two explicit trigger semantics:

```text
ENVIRONMENT_CHANGED
SAFETY_REPLAN_REQUIRED
```

For `ENVIRONMENT_CHANGED`:

```text
an explicit environment-change event ID is required
new validated replacement snapshot is required
no safety decision is required
```

For `SAFETY_REPLAN_REQUIRED`:

```text
an explicit environment-change event ID is required
new validated replacement snapshot is required
a SafetyDecision is required
SafetyDecision.requires_replan must be True
SafetyDecision must be non-approved
```

A safety rejection without a changed replacement snapshot must not trigger another A* search.

`PAUSED`, `EMERGENCY_STOP`, or another HALTED safety outcome must not be converted into an autonomous replan trigger.

---

# 8. ONE-ATTEMPT-PER-EVENT RULE

The coordinator must enforce that one unique environment-change event ID can authorize at most one replan attempt.

Required behavior:

```text
first valid use of event_id -> at most one executor invocation
second use of same event_id -> explicit rejection / ALREADY_CONSUMED outcome
no planner/executor invocation on duplicate event
```

The coordinator may keep a small deterministic in-memory set of consumed event IDs.

Do not implement time-based expiry, retries, backoff, queues, or asynchronous processing.

---

# 9. EXECUTION BOUNDARY

After trigger and replacement-snapshot validation, invoke the already accepted `PlannerSafetyEnvironmentExecutor` exactly once on the replacement environment and the unchanged approved goal.

Do not reproduce or fork A*, safety, or per-step execution logic inside the replanning coordinator.

Do not automatically invoke a second replan based on the returned execution result.

If the executor returns:

```text
SUCCESS -> report replanning success
NO_SAFE_PATH -> report NO_SAFE_PATH and leave the replacement agent at the preserved current position
HALTED -> report HALTED; do not retry
SAFETY_REJECTED -> report stopped/rejected; do not retry automatically
INVALID_GOAL_OR_PLAN -> fail closed; do not retry
```

If a later environment change occurs, the caller must supply a new event ID and another validated replacement snapshot.

---

# 10. RESULT / TRACE CONTRACT

Return an immutable structured result containing at least:

```text
status
event_id
trigger
approved_goal
original_position
replacement_start
replacement_environment_used
execution_result or None
consumed_event
reason
```

Recommended coordinator statuses:

```text
SUCCESS
NO_SAFE_PATH
HALTED
SAFETY_REJECTED
INVALID_CHANGE
INVALID_TRIGGER
ALREADY_CONSUMED
INVALID_GOAL_OR_PLAN
```

Exact enum names may differ if semantics remain explicit and tested.

Do not claim that a replan succeeded merely because a new path was computed; success means the accepted execution layer reaches the same approved goal.

---

# 11. PAUSE / STOP

The coordinator may accept explicit `paused` and `emergency_stop` booleans only to pass them unchanged into the accepted executor.

Rules:

```text
PAUSE/STOP do not create a replan event
if a valid change event is supplied while paused/stopped, executor safety precedence still applies and movement must halt
no retry occurs automatically after resume
another autonomous replan requires a newly authorized call/event under D-066
```

Do not implement resume state machines or human UI commands in this task.

---

# 12. TEST REQUIREMENTS

Add focused deterministic tests covering at least:

```text
valid ENVIRONMENT_CHANGED snapshot causes exactly one controlled replan
replacement start equals current old-environment position
same approved goal is preserved
same grid/goals are required
changed blocked cells can produce a new valid route
changed risk map can produce a different risk-aware route
unchanged blocked/risk map -> INVALID_CHANGE with zero executor invocation
same environment object -> INVALID_CHANGE
duplicate event_id -> ALREADY_CONSUMED with zero second executor invocation
SAFETY_REPLAN_REQUIRED requires a non-approved SafetyDecision with requires_replan=True
safety requires_replan without changed snapshot -> no replan
HALTED safety decision does not become SAFETY_REPLAN_REQUIRED
replacement snapshot with changed map but NO_SAFE_PATH -> NO_SAFE_PATH / zero movement from replacement start
hard blocked/prohibited constraints remain enforced
HIGH 0.75 remains traversable when accepted planner/safety allow it
pause/stop during a valid change event -> HALTED / no movement
no goal substitution
current environment/map is not mutated by snapshot creation or replanning
no automatic second attempt after SAFETY_REJECTED/NO_SAFE_PATH
identical valid inputs on fresh coordinator instances are deterministic
```

Use small synthetic maps with manually checkable routes.

---

# 13. REGRESSION REQUIREMENT

Run at minimum:

```text
pytest tests/test_replanning.py
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py
pytest
```

Report exact results. The pre-existing non-failing PyTorch warning may remain if unchanged.

---

# 14. OUT OF SCOPE / FORBIDDEN

Do not implement:

```text
in-place environment mutation API
automatic hazard generation
random/stochastic environment changes
time-based hazards
unlimited or multi-attempt replanning per event
replanning against an unchanged map
background/asynchronous monitoring
human goal changes or goal substitution
new safety thresholds
safety relaxation
shared-autonomy threshold changes
EEG/model/Bayesian integration
human-interface/UI behavior
Streamlit
reportable experiments or efficacy claims
RL / alternative planners
3D / continuous simulation
```

---

# 15. ACCEPTANCE CRITERIA

M4-T05 may be reported `PASS` only if:

```text
D-066 replacement-snapshot contract is enforced
current position and approved goal are preserved
map change is explicit and genuinely different
one event ID can trigger at most one replan attempt
unchanged-map retries are prevented
existing executor is reused rather than duplicated
NO_SAFE_PATH / HALT / rejection remain fail-safe and do not auto-retry
focused + combined autonomy + full regression suites pass
no out-of-scope dynamic-world or EEG behavior is added
```

---

# 16. STOP CONDITIONS

Stop and report `BLOCKED` if:

```text
accepted environment API cannot represent the replacement snapshot by using current position as the new snapshot start
accepted execution API cannot be reused without changing its semantics
implementation requires deciding a new retry policy, mutation model, or hazard process
implementation requires changing approved goal or hard safety rules
unrelated accepted modules would need modification
```

After implementing, testing, committing, and pushing the task branch:

```text
STOP
```

Do not merge and do not begin EEG/full-system integration, UI, logging, or reportable experiments until ChatGPT review and Project Owner acceptance.
