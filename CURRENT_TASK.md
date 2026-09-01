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

# 1. CLOSED TASK RECORD — M4-T04

```text
Task ID:
M4-T04

Task title:
Planner → Safety → Environment Execution Integration

Final status:
PASS / SCIENTIFICALLY ACCEPTED / MERGED

Task branch:
task/m4-t04-execution-integration

Initial implementation commit:
b77e04a8951e7d6d5aeb40eb4ed359e29d9ad1e3

Accepted corrected task-branch head / canonical software commit:
1a7ccde578083b3386183a97ca876714afb68e30
```

Accepted M4-T04 behavior:

```text
explicit already-approved goal is the only mission target input
planner computes one deterministic route
planner SUCCESS result is fail-closed validated before any safety check or movement
validated plan must preserve exact execution start and approved goal
validated path endpoints, action/path length, coordinates, and per-edge action reconstruction must be internally consistent
WAIT is not accepted as a route edge in a successful A* execution plan
malformed/substituted SUCCESS plans return INVALID_GOAL_OR_PLAN with zero movement
NO_SAFE_PATH returns with zero movement and preserves the supplied goal
SafetyController.check is called before every environment step
env.step() is called only for an APPROVED safety decision
HALTED stops execution immediately
REJECTED / REPLAN_REQUIRED stops the current route without executing the rejected action
HIGH 0.75 remains traversable when planner and safety permit it
execution traces record executed actions, visited positions, safety decisions, final position, termination, and reason
no automatic replanning, dynamic map mutation, goal substitution, EEG/Bayesian integration, UI, or experiments were added
```

Accepted verification reported from the corrected task branch:

```text
pytest tests/test_execution.py -> 13 passed
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py tests/test_execution.py -> 71 passed
pytest -> 201 passed, 1 pre-existing non-failing PyTorch warning
```

Scientific review verified:

```text
branch was 2 commits ahead and 0 behind canonical main before merge
only src/autonomy/execution.py and tests/test_execution.py changed
malformed SUCCESS plans are rejected before SafetyController.check or env.step()
```

---

# 2. CURRENT IMPLEMENTATION AUTHORITY

No Codex implementation task is currently authorized.

Do not begin another module from `TODO.md` or the implementation blueprint without a new narrow `CURRENT_TASK.md` ticket.

---

# 3. NEXT ARCHITECTURAL BOUNDARY TO RESOLVE

The remaining M4 blueprint includes replanning, but the accepted M4-T01 environment is intentionally static and M4-T04 explicitly forbids automatic map mutation/replanning.

Before authorizing a replanning implementation task, the Project Owner and scientific reviewer must freeze the runtime contract for **what constitutes a relevant environment change and how that changed map/state is supplied to the replanning coordinator**.

This is needed so Codex does not independently invent:

```text
dynamic hazard mutation semantics
blocked-cell update semantics
risk-map update semantics
when a safety REPLAN_REQUIRED flag triggers a new search
whether replanning uses the same environment object or a validated replacement snapshot
how current position and approved goal are preserved across a replan
replan-attempt limits or retry behavior
```

Existing approved constraints remain binding:

```text
approved goal may not be silently changed
hard blocked/prohibited constraints may not be relaxed
NO_SAFE_PATH means no movement
new planning may occur only after a relevant environment change or explicit human-approved goal/control change under D-065
```

Until this boundary is explicitly approved, implementation must stop here.
