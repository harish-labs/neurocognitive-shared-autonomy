# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex.  
**Current status:** ACTIVE / NOT STARTED  
**Current milestone:** M5 — Shared Autonomy + Human Interaction  
**Task ID:** M5-T04  
**Task title:** Stepwise Replacement-Snapshot Replanning Integration  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Approved decision baseline:** D-070 plus all prior accepted decisions  
**Last updated:** 2026-09-02

---

# 1. CLOSED TASK RECORD — M5-T03

```text
Task ID: M5-T03
Task title: Human-Authority-Aware Stepwise Navigation Runtime
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Accepted software commit:
c45ef7e36136007f79f2881a1ebbf7afd2fcbbc6
Verification:
focused -> 95 passed
adjacent -> 133 passed
full -> 271 passed, 1 known non-failing PyTorch warning
```

Canonical D-070 governance commit:

```text
a0769e08b48e6f30487b4c6da91262b7cf07fe81
```

---

# 2. OBJECTIVE

Implement only the deterministic D-070 stepwise replacement-snapshot replanning boundary inside the accepted M5 NavigationRuntime:

```text
active/closed source execution state
        +
explicit accepted replan trigger
        +
unique event_id
        +
new immutable validated replacement environment
        +
new execution_id
        ↓
recheck current human authority
        ↓
validate D-066 replacement semantics
        ↓
consume event only when actual planner invocation begins
        ↓
fresh A* against replacement snapshot
        ↓
ZERO movement during replanning
        ↓
new D-069 stepwise NavigationSession
        ↓
later advance_one_step()
        ↓
human authority + safety before each movement
```

M5-T04 integrates D-066 replacement-snapshot replanning with the accepted D-069 stepwise runtime. It must not re-enter the old whole-route M4 execution/replanning path.

---

# 3. READ FIRST

Read in order:

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
14. src/control/navigation_runtime.py
15. src/control/human_interaction.py
16. src/autonomy/environment.py
17. src/autonomy/planner.py
18. src/autonomy/safety.py
19. src/autonomy/execution.py
20. src/autonomy/replanning.py
21. relevant accepted tests
```

GitHub `main` is canonical.

---

# 4. GOVERNING DECISIONS

Preserve all prior decisions. D-070 is authoritative for this task, especially D-065 through D-070.

Authority remains:

```text
STOP
> PAUSE
> OVERRIDE
> CONFIRM / RESUME
> shared-autonomy policy
> planner
> safety
> environment execution
```

Environment-change replanning may change HOW the same approved goal is reached. It must never silently change WHAT goal is approved.

---

# 5. ALLOWED FILES

Primary authorized file:

```text
src/control/navigation_runtime.py
```

Primary test file:

```text
tests/test_navigation_runtime.py
```

A separate focused test file is authorized if it keeps the transition tests clearer:

```text
tests/test_navigation_replanning.py
```

Only if genuinely required for exports:

```text
src/control/__init__.py
```

Do not modify accepted implementations in:

```text
src/autonomy/replanning.py
src/autonomy/execution.py
src/autonomy/environment.py
src/autonomy/planner.py
src/autonomy/safety.py

src/control/human_interaction.py
src/control/interaction_bridge.py
src/control/shared_autonomy.py

src/cognition/*
src/models/*
src/eeg/*
```

If an accepted interface defect makes M5-T04 impossible without modifying those files: STOP / BLOCKED and report it.

Do not modify `requirements.txt`.

---

# 6. REQUIRED RUNTIME BOUNDARY

Extend the accepted `NavigationRuntime` with one narrow synchronous operation equivalent to:

```text
replan_after_environment_change(...)
```

Exact argument names may follow repository style, but the operation must have explicit inputs sufficient to identify:

```text
source execution attempt
current/source environment
replacement environment
HumanInteractionController
event_id
new_execution_id
replan trigger
prior NavigationResult when trigger is safety REPLAN_REQUIRED
applied RESUME result when required for changed-while-paused continuation
```

The API must not hide or generate event/execution identity internally.

The operation must return an immutable auditable result consistent with the existing NavigationResult/session model or a narrowly justified immutable companion result.

---

# 7. ZERO-MOVEMENT REPLAN

The replan operation may:

```text
validate authority
validate source execution state
validate event identity
validate replacement snapshot
invoke A* once
validate planner output
create a new NavigationSession
```

It must perform:

```text
ZERO environment.step() calls
ZERO SafetyController.check() calls
```

A successful replan prepares stepwise execution only.

All later movement must use accepted `advance_one_step()`.

Do not call:

```text
ControlledReplanningCoordinator.replan()
PlannerSafetyEnvironmentExecutor.execute()
```

from the M5 runtime.

---

# 8. AUTHORIZED TRIGGERS ONLY

Accept exactly:

```text
A. explicit ENVIRONMENT_CHANGED + new validated changed replacement snapshot

B. prior NavigationResult for the source execution where:
   status == REPLAN_REQUIRED
   requires_replan == True
   safety_decision is present and requires_replan == True
   + new validated changed replacement snapshot
```

Reject all unsupported attempts, including:

```text
SAFETY_REJECTED promoted to replan
STALE_STATE promoted to replan
NO_SAFE_PATH promoted to replan
safety requires_replan without a changed replacement snapshot
unchanged-map retry
unsupported trigger values/types
```

Do not infer or synthesize an environment event.

---

# 9. EVENT IDENTITY / ONE REPLAN PER EVENT

Every replan opportunity requires a caller-supplied unique non-empty string `event_id`.

Required semantics:

```text
malformed/empty event_id -> reject, zero movement, no planner invocation
already consumed event_id -> ALREADY_CONSUMED/no-op
one event_id -> at most one actual A* invocation
no hidden/generated event IDs
```

Do not consume the event before planner invocation for:

```text
invalid event identity
invalid trigger
invalid replacement snapshot
STOP
PAUSE
active confirmation/HOLD
approved-goal mismatch
other pre-planner authority/state validation failure
```

Once validation reaches the actual planner invocation:

```text
event_id becomes consumed exactly once
```

regardless of whether the planner result ultimately becomes:

```text
READY
NO_SAFE_PATH
INVALID_GOAL_OR_PLAN
```

A consumed event must never cause another planner invocation.

---

# 10. EXECUTION IDENTITY ACROSS REPLAN

A replacement plan is a NEW navigation attempt.

Inputs must include:

```text
source_execution_id
new_execution_id
```

Required:

```text
both are non-empty valid identifiers
new_execution_id != source_execution_id
new_execution_id not previously consumed/active/closed
source execution refers to the attempt being replaced
```

After a valid replan reaches planner invocation, the source executable attempt must not be resurrected or replayed.

A successful replacement route belongs only to `new_execution_id`.

Maintain the conceptual identity separation:

```text
command_id   -> one human command
request_id   -> one confirmation request
execution_id -> one executable route attempt
event_id     -> one environment-change/replan opportunity
```

---

# 11. SAME HUMAN-APPROVED SYMBOLIC GOAL

Ordinary environment-change replanning preserves the existing human-approved WHAT.

Required at the replan boundary:

```text
source session symbolic goal == controller.state.approved_goal
symbolic goal is a non-empty exact key in both source and replacement EnvironmentConfig.goals
source and replacement mapping for that key is identical
```

Do not request new EEG/Bayesian/shared-autonomy evidence merely because the route environment changed.

Do not perform:

```text
goal substitution
nearest goal
fallback goal
planner-preferred alternative
value/fuzzy/substring matching
hard-coded Left/Right -> victim mapping
```

OVERRIDE or another real approved-goal change is not an environment replan to the prior goal.

---

# 12. REPLACEMENT SNAPSHOT VALIDATION

The replacement must be a distinct accepted `SearchRescueEnvironment` object.

Validate at least:

```text
same rows/columns as source environment
same exact symbolic goal mapping
same approved symbolic goal and exact coordinate
replacement.config.start == current actual source position
replacement.state.position == current actual source position
replacement not terminated
current position not blocked in replacement
current position not prohibited in replacement
```

Only these map/environment conditions may differ for this transition:

```text
blocked_cells
risk_map
```

At least one must genuinely differ.

Therefore:

```text
new object + structurally unchanged map -> INVALID_CHANGE
changed goal registry -> INVALID_CHANGE / fail closed
hidden mutation -> forbidden
```

Do not relax blocked cells, D-064 prohibited threshold, or any other hard safety rule to obtain a route.

---

# 13. HUMAN AUTHORITY BEFORE PLANNER INVOCATION

Before replanning, enforce:

```text
STOP
> PAUSE
> active confirmation/HOLD
> approved-goal consistency
> event/replacement validation
> planner
```

STOP:

```text
zero movement
zero planner invocation
no replacement execution
```

PAUSE:

```text
zero movement
zero planner invocation
preserve position and approved goal
no executable replacement plan while paused
```

Active confirmation/HOLD:

```text
zero movement
zero planner invocation
```

OVERRIDE / changed approved goal:

```text
old-goal replan fails closed
no old-goal planner invocation
movement to override goal must use the accepted fresh OVERRIDE authorization/navigation-start path
```

The runtime must not call `HumanInteractionController.handle_command()` or synthesize any human command.

---

# 14. CHANGED WHILE PAUSED / RESUME

Preserve D-067 + D-070:

```text
PAUSE closes/invalidate old executable movement
an explicit environment-change event may exist while paused
no planner invocation occurs while paused
```

After an explicit applied RESUME:

```text
same approved symbolic goal
not stopped
not paused
requires_fresh_execution == True
+
pending caller-supplied event_id
+
validated replacement snapshot
+
new execution_id
```

may authorize the D-066 replacement replan.

Required:

```text
fresh A* from current position
zero movement during replan
no replay of pre-PAUSE path/action
source old execution remains closed
```

Do not use plain `start_navigation()` as a shortcut to bypass the changed-while-paused replacement event when that event/snapshot is the basis for the resumed environment.

---

# 15. SAFETY-REQUESTED REPLAN

A prior genuine M5 result with:

```text
status == REPLAN_REQUIRED
requires_replan == True
matching source execution_id
SafetyDecision.requires_replan == True
```

may authorize fresh route computation only when accompanied by a new validated changed replacement snapshot and unique event/new-execution identities.

Human reconfirmation is not required solely because the route changed, provided:

```text
controller authority still permits movement
same exact approved symbolic goal remains current
```

The safety result alone never authorizes retrying the unchanged map.

---

# 16. FRESH PLAN VALIDATION

Invoke accepted `RiskAwareAStarPlanner` at most once for a consumed event.

Plan exactly:

```text
start = current agent position
approved_goal = exact same replacement-environment coordinate for the current symbolic goal
```

Reuse D-069 plan-integrity requirements:

```text
NO_SAFE_PATH maps to explicit stationary NO_SAFE_PATH
malformed SUCCESS fails closed
start/goal/path/actions must reconstruct the exact request
path must not enter another configured terminal goal before the approved goal
no alternate goal
```

If planner reports NO_SAFE_PATH after the event is consumed:

```text
zero movement
hold/closed replacement attempt
event remains consumed
no second planner call for that event
```

---

# 17. SUCCESSFUL REPLAN

A successful replan must produce a READY-style state with:

```text
moved == False
new execution_id
same symbolic approved goal
same exact goal coordinate
fresh immutable path/actions
next_action_index == 0
expected_position == current position
replacement-environment structural signature captured
new execution active
```

Subsequent movement occurs only through:

```text
advance_one_step(replacement_environment, controller)
```

which must retain all accepted D-069 authority/staleness/safety checks.

Using the old source environment or another structurally different environment after replacement-plan activation must fail closed.

---

# 18. MULTIPLE CHANGES

Valid sequence example:

```text
execution E1
-> event C1
-> replacement plan execution E2
-> step(s)
-> event C2
-> replacement plan execution E3
```

Each new actual environment change requires:

```text
new unique event_id
new validated changed replacement snapshot
new unique execution_id
```

Never:

```text
retry consumed event
retry unchanged map
loop automatically
reuse closed execution ID
```

---

# 19. REQUIRED TESTS

Cover at least:

```text
explicit ENVIRONMENT_CHANGED can produce fresh READY replacement plan
replan performs zero environment movement
replan performs zero safety calls
old whole-route M4 replanner/executor are never invoked
valid changed blocked_cells snapshot accepted
valid changed risk_map snapshot accepted
unchanged replacement snapshot rejected
changed goal registry rejected
replacement must preserve exact current position
replacement current position blocked/prohibited rejected
invalid/empty event ID rejected without consumption/planner call
duplicate consumed event cannot replan again
one event produces at most one planner invocation
event becomes consumed once planner invocation starts even if NO_SAFE_PATH
event becomes consumed once planner invocation starts even if planner SUCCESS is malformed
invalid pre-planner request does not consume event
new execution ID required and differs from source execution ID
consumed/duplicate new execution ID rejected
same exact symbolic human-approved goal preserved
OVERRIDE/goal change prevents old-goal replan
STOP prevents planner invocation
PAUSE prevents planner invocation
active confirmation prevents planner invocation
valid applied RESUME + pending change produces fresh replacement plan from current position
changed-while-paused flow never replays old action/path
safety REPLAN_REQUIRED + new changed snapshot may replan
safety REPLAN_REQUIRED without changed snapshot cannot replan
SAFETY_REJECTED/STALE_STATE/NO_SAFE_PATH cannot be promoted to replan trigger
replacement NO_SAFE_PATH holds with zero movement and no same-event retry
malformed replacement planner SUCCESS fails closed
replacement path crossing another configured terminal goal fails closed
successful replacement session advances only through ordinary advance_one_step
old source environment after successful replacement fails closed
second genuine change requires second event/new execution ID
runtime does not call HumanInteractionController.handle_command
no async/background/event-bus/retry-worker behavior
no EEG/model/Bayesian/adaptation/UI dependencies
identical fresh inputs/controllers/environments produce deterministic results
```

---

# 20. REGRESSION REQUIREMENT

Run at minimum:

```text
python -m pytest tests/test_navigation_runtime.py tests/test_navigation_replanning.py tests/test_human_interaction.py tests/test_interaction_bridge.py tests/test_planner.py tests/test_safety.py
```

If `tests/test_navigation_replanning.py` is not created, omit only that filename and keep all other focused files.

Then:

```text
python -m pytest tests/test_navigation_runtime.py tests/test_human_interaction.py tests/test_interaction_bridge.py tests/test_planner.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py tests/test_shared_autonomy.py
```

Include `tests/test_navigation_replanning.py` in this command if it exists.

Then:

```text
python -m pytest
```

Report exact counts and warnings.

In a clean environment, the known pre-existing `requirements.txt` omission of `pandas` and `scikit-learn` may be handled only by installing them in the verification environment:

```text
python -m pip install pandas scikit-learn
```

Do not modify dependency files.

---

# 21. OUT OF SCOPE

No modification/invocation of the accepted M4 whole-route replanner/executor for M5 runtime movement; no shared-autonomy/Bayesian threshold changes; no EEG/model/calibration integration; no binary EEG multi-goal mapping change; no adaptation changes; no arbitrary goal-registry mutation through environment events; no automatic unchanged-map retry; no async/background processing; no UI; no logging/metrics infrastructure; no experiments/claims; no dependency maintenance; no physical robot/live EEG.

M6 end-to-end offline EEG replay integration is explicitly NOT authorized by this ticket.

---

# 22. ACCEPTANCE / STOP

PASS only if D-066 replacement snapshots can produce a fresh D-069 stepwise plan with zero movement; one actual planner invocation maximum per event; old execution cannot replay; new execution identity is mandatory; exact human-approved symbolic goal is preserved; STOP/PAUSE/OVERRIDE/confirmation authority prevents unauthorized replanning; safety-triggered replan requires a new changed snapshot; unchanged-map retries are impossible; and accepted M4/M5 dependencies remain unchanged with regressions passing.

STOP/BLOCKED if an accepted interface must change, D-070 is insufficient, or another scientific/architectural decision is required.

After implementation/tests/commit/push: STOP. Do not merge and do not begin M6/UI/experiments/maintenance.
