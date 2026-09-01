# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex.  
**Current status:** ACTIVE / NOT STARTED  
**Current milestone:** M5 — Shared Autonomy + Human Interaction  
**Task ID:** M5-T03  
**Task title:** Human-Authority-Aware Stepwise Navigation Runtime  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Approved decision baseline:** D-069 plus all prior accepted decisions  
**Last updated:** 2026-09-01

---

# 1. CLOSED TASK RECORD — M5-T02

```text
Task ID: M5-T02
Task title: Shared-Autonomy / Human-Interaction Authorization Bridge
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Accepted software commit:
fb2e088d27f9e5513d5a63c162a7ab802ddf7f52
Verification:
focused -> 54 passed
adjacent -> 100 passed
full -> 256 passed, 1 known non-failing PyTorch warning
```

---

# 2. OBJECTIVE

Implement only the deterministic D-069 runtime boundary:

```text
fresh accepted goal authorization
        ↓
exact current symbolic-goal -> coordinate resolution
        ↓
fresh A* plan, zero movement at start
        ↓
advance one step
        ↓
current human authority check
        ↓
safety check
        ↓
at most one environment.step()
```

M5-T03 makes runtime navigation interruptible between every simulated move while preserving accepted M4 planner/safety/environment semantics and D-067/D-068 human authority.

M5-T03 does NOT integrate D-066 replacement-snapshot stepwise replanning. Replan-required holds and returns explicitly for a later task.

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
14. src/control/interaction_bridge.py
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

Preserve all prior decisions. D-069 is authoritative for this task, especially D-064 through D-069.

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

Safety retains veto authority over each low-level move.

---

# 5. ALLOWED FILES

Primary authorized files:

```text
src/control/navigation_runtime.py
tests/test_navigation_runtime.py
```

Only if genuinely required for exports:

```text
src/control/__init__.py
```

Do not modify accepted implementations in:

```text
src/control/shared_autonomy.py
src/control/interaction_bridge.py
src/control/human_interaction.py
src/autonomy/environment.py
src/autonomy/planner.py
src/autonomy/safety.py
src/autonomy/execution.py
src/autonomy/replanning.py
src/cognition/*
src/models/*
src/eeg/*
```

If an accepted interface defect makes the task impossible without modifying those files: STOP / BLOCKED and report it.

Do not modify `requirements.txt`.

---

# 6. RUNTIME API BOUNDARY

Implement a small deterministic coordinator in `src/control/navigation_runtime.py`.

Exact names may follow repository style, but expose separate operations equivalent to:

```text
start_navigation(...)
advance_one_step(...)
```

`start_navigation`:

- accepts current environment, HumanInteractionController, caller-supplied execution_id, and one fresh accepted M5 authorization result;
- validates the authorization source and controller state;
- resolves exact symbolic goal to current environment coordinate;
- plans from current environment position;
- records a read-only active navigation session/plan state;
- performs ZERO `environment.step()` calls.

`advance_one_step`:

- rechecks current human authority and stale state;
- proposes only the next action from the active valid plan;
- calls SafetyController.check immediately before movement;
- performs AT MOST ONE environment.step();
- returns an immutable auditable result;
- never loops over the remaining route.

---

# 7. ACCEPTED FRESH AUTHORIZATION SOURCES

Navigation start is allowed only from one of:

```text
A. InteractionBridgeResult:
   status == AUTHORIZED
   policy_goal_adopted == True

B. CommandResult for CONFIRM:
   status == APPLIED
   accepted/applied
   exact controller-approved candidate now present

C. CommandResult for OVERRIDE:
   status == APPLIED
   accepted/applied
   exact new controller-approved goal now present

D. CommandResult for RESUME:
   status == APPLIED
   accepted/applied
   stopped == False
   paused == False
   approved goal exists
   requires_fresh_execution == True
```

Reject/hold all other result types/statuses, including WAITING, DEFER, WAITING_FOR_CONFIRMATION, HOLD, PAUSE, STOP, stale/invalid commands, duplicates/ALREADY_CONSUMED, and repeated PROCEED with `policy_goal_adopted=False`.

The runtime MUST NOT call `handle_command()` and MUST NOT synthesize human commands.

---

# 8. EXECUTION IDENTITY

Each attempt requires a caller-supplied unique non-empty string `execution_id`.

```text
malformed/empty ID -> reject without movement
active/consumed/closed ID reuse -> explicit ALREADY_CONSUMED-style result
one ID identifies exactly one navigation attempt
closed attempt cannot be replayed
no hidden ID generation
```

---

# 9. EXACT SYMBOLIC GOAL RESOLUTION

At `start_navigation`:

```text
symbolic goal == controller.state.approved_goal
symbolic goal is non-empty string
symbolic goal exactly in environment.config.goals KEYS
coordinate = environment.config.goals[symbolic_goal]
```

Forbidden: value/substr/fuzzy matching, fallback/nearest/planner-preferred alternative, or hard-coded Left/Right -> victim mapping.

Coordinate resolution occurs only at this execution boundary.

Because the current environment terminates on entry to any configured goal cell, fail closed before execution if a successful planned path would enter a different configured goal coordinate before the approved goal. Do not silently treat that other goal as success and do not invent a route workaround in this task.

---

# 10. PLAN VALIDATION / ZERO-MOVEMENT START

`start_navigation` must:

- use accepted `RiskAwareAStarPlanner`;
- plan exactly from `environment.state.position` to resolved approved coordinate;
- map planner NO_SAFE_PATH to explicit stationary NO_SAFE_PATH;
- fail closed on malformed/inconsistent SUCCESS output;
- reject a plan whose start/goal/path/actions do not reconstruct the exact request;
- perform no safety call and no environment transition merely by planning.

Do not call `PlannerSafetyEnvironmentExecutor.execute()` because it would violate D-069 stepwise execution.

---

# 11. HUMAN AUTHORITY BEFORE EVERY STEP

Before every `advance_one_step` movement:

```text
STOPPED -> close/STOP, zero movement
PAUSED -> close/invalidate executable plan, zero movement
active confirmation -> HOLD/close stale executable authorization, zero movement
approved symbolic goal changed -> close old attempt, zero movement
approved goal missing -> close/reject, zero movement
```

An old path never continues after PAUSE, STOP, OVERRIDE, or newly active confirmation.

RESUME starts a NEW navigation attempt with a new execution_id and a fresh plan from current position. Never replay queued old movement.

---

# 12. STALE ENVIRONMENT / STATE PROTECTION

At start capture a deterministic structural snapshot/signature sufficient to detect changes to at least:

```text
grid rows/columns
exact symbolic goal mapping
blocked cells
risk map
expected current position
```

Before each step, current map/config must still equal the recorded snapshot and current position must equal session expectation. Hidden map mutation or external movement fails closed before transition. Do not reconcile automatically.

---

# 13. SAFETY BEFORE EVERY ENVIRONMENT TRANSITION

For one proposed next action, call `SafetyController.check()` using actual current position and current interaction pause/stop state.

```text
APPROVED + approved_action -> exactly one environment.step(approved_action)
HALTED -> zero movement, close/hold
REJECTED -> zero movement
REPLAN_REQUIRED / requires_replan=True -> zero movement, explicit REPLAN_REQUIRED/HOLD
```

Never bypass safety.

---

# 14. STEP RESULT / SESSION STATE

Use immutable results/session state sufficient to audit at least:

```text
status
execution_id
symbolic approved goal
resolved goal coordinate
immutable plan/path representation or identity
proposed action, if any
safety decision, if any
position before
position after
moved
active/closed state
requires_replan
remaining action count or next index
reason
```

Recommended statuses: READY, STEP_EXECUTED, GOAL_REACHED, NO_SAFE_PATH, PAUSED, STOPPED, HOLD, REPLAN_REQUIRED, SAFETY_REJECTED, STALE_STATE, INVALID_AUTHORIZATION, INVALID_GOAL_OR_PLAN, ALREADY_CONSUMED. Exact naming may differ if explicit/deterministic.

---

# 15. COMPLETION

Success only when the environment reaches the exact approved symbolic goal/coordinate.

Do not report success merely because `environment.state.terminated` is true. Verify `reached_goal` equals the exact symbolic approved goal.

After completion the execution_id is closed/consumed and cannot execute again.

---

# 16. REPLAN BOUNDARY

M5-T03 does not perform D-066 replacement-snapshot replanning.

If safety returns `requires_replan=True`:

```text
no movement
return REPLAN_REQUIRED
close/hold current executable attempt
do not plan again against unchanged environment
do not invoke ControlledReplanningCoordinator automatically
```

A later M5-T04 separately integrates explicit environment-change snapshots with stepwise human-aware execution.

---

# 17. REQUIRED TESTS

Cover at least:

```text
start performs zero movement
exact PROCEED authorization starts plan
repeated non-adopting PROCEED cannot start
applied CONFIRM can start exact confirmed goal
applied OVERRIDE can start exact new goal
applied RESUME starts fresh plan from current state
stale/invalid/duplicate command results cannot start
exact symbolic key resolution only
symbolic/controller/environment mismatch fails closed
malformed planner SUCCESS fails closed
path crossing another configured terminal goal fails closed before movement
each advance performs at most one environment.step
safety checked immediately before every executed step
PAUSE between steps prevents next movement and closes old plan
STOP between steps prevents all future movement in session
OVERRIDE between steps prevents next old-goal action
active confirmation between steps prevents next old-goal action
RESUME never replays old queued action
stale map/config mutation fails before movement
external unexpected position change fails before movement
safety REJECTED causes zero movement
safety REPLAN_REQUIRED causes zero movement and no unchanged-map retry
NO_SAFE_PATH stationary
exact approved goal completion only
execution_id duplicate/replay protected
no HumanInteractionController.handle_command call from runtime
no PlannerSafetyEnvironmentExecutor.execute call
no ControlledReplanningCoordinator call
no EEG/model/Bayesian/adaptation/UI imports
identical fresh controllers/environments/input sequences deterministic
```

---

# 18. REGRESSION REQUIREMENT

Run at minimum:

```text
python -m pytest tests/test_navigation_runtime.py tests/test_interaction_bridge.py tests/test_human_interaction.py tests/test_planner.py tests/test_safety.py

python -m pytest tests/test_navigation_runtime.py tests/test_interaction_bridge.py tests/test_human_interaction.py tests/test_planner.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py tests/test_shared_autonomy.py

python -m pytest
```

Report exact counts/warnings. In a clean environment, the known pre-existing `requirements.txt` omission of `pandas` and `scikit-learn` may be handled only by installing them into the verification environment. Do not modify dependency files.

---

# 19. OUT OF SCOPE

No shared-autonomy/Bayesian threshold changes; EEG/model/calibration integration; binary EEG multi-goal mapping changes; adaptation; D-066 replacement-snapshot stepwise replanning; automatic unchanged-map retry; modification of accepted whole-route executor/replanner; async/background processing; UI; logging/metrics infrastructure; experiments/claims; dependency maintenance; physical robot/live EEG.

---

# 20. ACCEPTANCE / STOP

PASS only if start causes zero movement; each advance performs at most one safety-approved environment transition; PAUSE/STOP/OVERRIDE/active-confirmation authority is rechecked before every move; old queued movement cannot replay; exact symbolic-goal authority is preserved through completion; stale environment/state fails closed; safety cannot be bypassed; replan-required causes no unchanged-map retry; and accepted M4/M5 modules remain unchanged with regressions passing.

STOP/BLOCKED if an accepted interface must change, D-069 is insufficient, or another architectural decision is required.

After implementation/tests/commit/push: STOP. Do not merge and do not begin M5-T04/M6/UI/experiments/maintenance.
