# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no implementation task is currently authorized.  
**Current status:** NO ACTIVE IMPLEMENTATION TASK  
**Current milestone:** M4 — 2D Search & Rescue / A* / Safety  
**Task ID:** None  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-09-01

---

# 1. CLOSED TASK RECORD — M4-T05

```text
Task ID:
M4-T05

Task title:
Controlled Replanning After Environment Change

Final status:
PASS / SCIENTIFICALLY ACCEPTED / MERGED

Task branch:
task/m4-t05-controlled-replanning

Accepted task-branch head / canonical software commit:
e8183ccebc9c2f67a1b33347b9ef12d25ddbcbfe
```

Accepted M4-T05 behavior:

```text
D-066 controlled replanning contract enforced
fresh distinct SearchRescueEnvironment replacement snapshot required
same grid dimensions and named goal mapping required
replacement start/current state must equal the old environment's current agent position
same supplied human-approved goal preserved
blocked-cell and/or risk map must genuinely change
exactly two triggers: ENVIRONMENT_CHANGED and SAFETY_REPLAN_REQUIRED
SAFETY_REPLAN_REQUIRED requires a non-approved SafetyDecision with requires_replan=True
HALTED safety outcomes cannot become replan triggers
one unique event_id authorizes at most one executor attempt
unchanged-map and duplicate-event attempts fail without execution
accepted PlannerSafetyEnvironmentExecutor is reused exactly once for an authorized event
NO_SAFE_PATH / HALTED / SAFETY_REJECTED / INVALID_GOAL_OR_PLAN do not auto-retry
PAUSE / emergency stop retain precedence
HIGH 0.75 remains traversable when planner/safety permit it
blocked/prohibited constraints remain enforced
no goal substitution, hard-safety relaxation, hidden map mutation, stochastic hazard process, EEG integration, UI, logging, or experiments added
```

Accepted verification reported from the task branch:

```text
pytest tests/test_replanning.py -> 13 passed
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py -> 84 passed
pytest -> 214 passed, 1 pre-existing non-failing PyTorch warning
```

Scientific review verified before merge:

```text
branch was 1 commit ahead and 0 behind canonical main
only src/autonomy/replanning.py and tests/test_replanning.py changed
trigger validation, snapshot validation, duplicate-event rejection, one executor invocation per event, and fail-safe no-retry behavior match D-066 and the active ticket
```

---

# 2. CURRENT IMPLEMENTATION AUTHORITY

No Codex implementation task is currently authorized.

Do not begin another module from `TODO.md` or the implementation blueprint without a new narrow `CURRENT_TASK.md` ticket.

---

# 3. NEXT PROJECT BOUNDARY

The core M4 autonomy stack is now implemented and accepted:

```text
environment / risk map
risk-aware A*
hard safety controller
planner -> safety -> environment execution
controlled replanning after explicit environment change
```

Before the next implementation task, review the M5 human-interaction boundary against the approved shared-autonomy policy and human-control decisions.

Do not let Codex invent stale-confirmation handling, duplicate-command semantics, confirmation-request identifiers, override-goal validation, or resume behavior without explicit authorization.
