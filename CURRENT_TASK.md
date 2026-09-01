# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex, while retaining the immediately preceding accepted task record.  
**Current status:** ACTIVE / NOT STARTED  
**Current milestone:** M4 — 2D Search & Rescue / A* / Safety  
**Task ID:** M4-T04  
**Task title:** Planner → Safety → Environment Execution Integration  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Canonical starting commit:** `ef7e27dfd8bf6446ddb1f0c783800b13ebbdca71`  
**Last updated:** 2026-09-01

---

# 1. CLOSED TASK RECORD — M4-T03

```text
Task ID: M4-T03
Task title: Safety Controller / Hard Constraint Enforcement
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Task branch: task/m4-t03-safety-controller
Accepted task-branch head: 6573ba90f96447081b3edfd5560d354fe2f69a6b
Canonical merge commit: ef7e27dfd8bf6446ddb1f0c783800b13ebbdca71
```

Accepted verification:

```text
pytest tests/test_safety.py -> 20 passed
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py -> 58 passed
pytest -> 188 passed, 1 pre-existing non-failing PyTorch warning
```

Accepted behavior: deterministic hard-safety authority; emergency stop > pause > invalid state > invalid action > bounds > blocked > prohibited > approve; HIGH 0.75 remains permitted; WAIT may be approved; blocked/prohibited moves request replanning; controller does not call env.step() or A*.

---

# 2. M4-T04 OBJECTIVE

Implement only the deterministic execution/orchestration layer that connects the already accepted planner, safety controller, and environment for one approved goal.

Required architecture:

```text
explicit approved goal
→ planner computes path
→ propose next action
→ safety controller checks that action
→ environment executes only an APPROVED action
```

The integration layer may iterate through the accepted path one action at a time, with a safety check before every environment step.

It must not infer or change human intent.

---

# 3. READ FIRST

Read, in order:

```text
MASTER_PROJECT_SPEC.md
AGENTS.md
PROJECT_STATE.md
DECISIONS.md
CURRENT_TASK.md
docs/04_SYSTEM_ARCHITECTURE.md
docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md
docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md
docs/14_SAFETY_CRITICAL_CONTROL.md
docs/15_IMPLEMENTATION_BLUEPRINT.md
docs/16_REPOSITORY_AND_CODE_ARCHITECTURE.md
docs/19_TESTING_AND_VERIFICATION.md
src/autonomy/environment.py
src/autonomy/planner.py
src/autonomy/safety.py
src/control/shared_autonomy.py
relevant accepted tests
```

GitHub `main` is canonical.

---

# 4. GOVERNING DECISIONS / BOUNDARIES

Preserve D-003, D-016, D-018 through D-021, D-056, D-057, and D-061 through D-065.

In particular:

```text
human determines WHAT goal; autonomy determines HOW safely
planner never changes supplied approved goal
planner proposes; safety authorizes; environment executes only approved actions
blocked cells and risk >= 1.00 are hard non-traversable
HIGH 0.75 remains soft/traversable
NO_SAFE_PATH means no movement and no goal substitution
PAUSE/STOP prevent autonomous movement
```

No live-EEG or physical-robot claim is authorized.

---

# 5. ALLOWED FILES

Primary:

```text
src/autonomy/execution.py
tests/test_execution.py
```

Only if required for exports:

```text
src/autonomy/__init__.py
```

Do not modify accepted environment/planner/safety/shared-autonomy modules unless a genuine integration defect is found; if so, stop and report the blocker.

---

# 6. REQUIRED EXECUTION API

Provide a deterministic structured execution result. Exact class/function naming may vary, but it must expose at least:

```text
status
approved_goal
planning_result
executed_actions
visited_positions
safety_decisions
final_position
terminated
reason
```

Minimum execution statuses:

```text
SUCCESS
NO_SAFE_PATH
SAFETY_REJECTED
HALTED
INVALID_GOAL_OR_PLAN
```

The integration API receives an already approved goal coordinate. It must not receive raw EEG, decoder probabilities, Bayesian posterior, entropy, or adaptation state.

---

# 7. NORMAL EXECUTION

For a valid supplied approved goal:

```text
1. plan from current environment state to approved goal using RiskAwareAStarPlanner
2. if planning status is not SUCCESS, do not move
3. for each planned action:
   a. call SafetyController.check using current environment position
   b. execute env.step(action) only when safety status is APPROVED
   c. record decision/action/new position
4. stop successfully when the environment reaches the approved goal / terminates
```

Never execute an entire planned route without per-step safety authorization.

---

# 8. NO_SAFE_PATH

If planner returns NO_SAFE_PATH:

```text
no env.step() calls
agent remains stationary
return explicit NO_SAFE_PATH
preserve supplied approved goal
```

Do not relax hard constraints or select another goal.

---

# 9. SAFETY REJECTION / HALT

If safety returns HALTED:

```text
execute no rejected action
stop integration immediately
return HALTED
```

If safety returns REJECTED or REPLAN_REQUIRED during execution:

```text
execute no rejected action
stop current route immediately
return SAFETY_REJECTED
preserve requires_replan / reason in trace
```

M4-T04 does not implement a dynamic replanning event loop. A replan flag may be surfaced, but automatic map mutation/retry loops are out of scope.

---

# 10. HUMAN CONTROL INPUT

The integration API may accept explicit:

```text
paused: bool
emergency_stop: bool
```

and pass these to the safety controller for every proposed action.

Do not invent confirmation or override-goal semantics here. Shared-autonomy decisions remain upstream; M4-T04 consumes only an already approved goal plus explicit pause/stop state.

---

# 11. TEST REQUIREMENTS

Add focused tests covering at least:

```text
successful zero-risk execution reaches approved goal
risk-aware planner route is actually followed
safety check occurs before every env.step
HIGH 0.75 route can execute if approved by planner/safety
NO_SAFE_PATH causes zero movement
emergency stop causes zero movement / HALTED
pause causes zero movement / HALTED
safety rejection prevents env.step for rejected action
blocked/prohibited action cannot be executed even if proposed
visited positions/actions/safety trace are internally consistent
approved goal is never substituted
identical inputs produce identical execution trace
environment terminates at reached goal
integration does not access EEG/model/Bayesian internals
```

Use small synthetic deterministic maps.

---

# 12. REGRESSION REQUIREMENT

Run at minimum:

```text
pytest tests/test_execution.py
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py tests/test_execution.py
pytest
```

Report exact results. The existing non-failing PyTorch warning may remain if unchanged.

---

# 13. OUT OF SCOPE / FORBIDDEN

Do not implement:

```text
dynamic hazard/map mutation
multi-step automatic replanning loop
EEG replay/full BCI integration
new shared-autonomy thresholds or decisions
confirmation UI
adaptation changes
reportable experiments/metrics
Streamlit/UI
RL or alternative planners
3D/continuous simulation
```

---

# 14. ACCEPTANCE CRITERIA

PASS only if:

```text
accepted planner -> safety -> environment order is enforced
no action executes without safety APPROVED
NO_SAFE_PATH/PAUSE/STOP cause no movement
approved goal remains fixed
execution trace is explicit and deterministic
focused + combined autonomy + full regression tests pass
no scientific values or policies are invented
```

---

# 15. STOP CONDITIONS

Stop and report BLOCKED if integration requires changing accepted planner/safety/environment semantics, adding a new scientific policy, or choosing unresolved EEG/shared-autonomy behavior.

After implementation, tests, commit, and push: STOP. Do not merge and do not start EEG/full-system integration or experiments until ChatGPT review and Project Owner acceptance.
