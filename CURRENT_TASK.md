# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no implementation task is currently authorized.  
**Current status:** NO ACTIVE IMPLEMENTATION TASK  
**Current milestone:** M5 — Shared Autonomy + Human Interaction  
**Task ID:** None  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-09-02

---

# 1. CLOSED TASK RECORD — M5-T03

```text
Task ID: M5-T03
Task title: Human-Authority-Aware Stepwise Navigation Runtime
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Task branch: task/m5-t03-stepwise-navigation
Accepted software commit:
c45ef7e36136007f79f2881a1ebbf7afd2fcbbc6
```

Accepted files:

```text
src/control/navigation_runtime.py
tests/test_navigation_runtime.py
```

Accepted D-069 behavior:

```text
start_navigation performs zero environment movement
advance_one_step performs at most one environment transition
fresh accepted M5 authorization required before navigation start
caller-supplied execution_id is unique and replay-protected
symbolic approved goal resolves only by exact current EnvironmentConfig.goals key
wrong-terminal-goal paths fail closed before movement
PAUSE invalidates the old executable plan and causes zero next movement
STOP terminates the current navigation session and causes zero further movement
OVERRIDE invalidates old-goal execution before any further step
RESUME requires a new execution ID and a fresh plan from current position
active confirmation/HOLD prevents continuation from historical authorization
stale goal/map/config/position/terminal state fails closed
SafetyController.check is called immediately before every actual transition
REPLAN_REQUIRED causes zero movement and no retry against the unchanged map
runtime does not synthesize or process HumanCommand objects
accepted M4 executor and replanning implementations remain unchanged
D-066 replacement-snapshot stepwise replanning remains outside M5-T03
```

Independent verification was executed on the exact accepted task code in a temporary GitHub Actions environment whose workflow parent was verified as the accepted commit:

```text
python -m pytest tests/test_navigation_runtime.py tests/test_interaction_bridge.py tests/test_human_interaction.py tests/test_planner.py tests/test_safety.py
-> 95 passed in 0.48s

python -m pytest tests/test_navigation_runtime.py tests/test_interaction_bridge.py tests/test_human_interaction.py tests/test_planner.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py tests/test_shared_autonomy.py
-> 133 passed in 0.34s

python -m pytest
-> 271 passed, 1 warning in 29.66s
```

The warning is the already-known non-failing PyTorch `padding='same'` warning from the accepted EEGNet/calibration path.

The clean verification environment installed `pandas` and `scikit-learn` separately because `requirements.txt` still omits those pre-existing dependencies. M5-T03 did not modify `requirements.txt`.

---

# 2. IMPLEMENTATION AUTHORITY NOW

```text
No Codex implementation task is currently authorized.
```

M5-T03 is complete and merged. Do not begin M5-T04 automatically.

---

# 3. NEXT ARCHITECTURAL BOUNDARY

The next M5 boundary is the separately reviewed integration of D-066 controlled environment-change replacement snapshots with the accepted D-069 human-authority-aware stepwise navigation runtime.

Before any M5-T04 implementation ticket is created, ChatGPT and the Project Owner must review and freeze the exact transition contract for at least:

```text
explicit ENVIRONMENT_CHANGED event + immutable validated replacement snapshot
preserve current agent position and same approved symbolic goal unless human authority changes it
maximum one replan per supplied environment-change event
PAUSE / STOP / OVERRIDE / active confirmation precedence during and after replacement-snapshot handling
stale execution/session invalidation
fresh planner invocation against the replacement snapshot only
no retry against unchanged map
no goal substitution
no blocked/prohibited relaxation
no hidden map mutation
interaction between execution_id/session identity and replacement-snapshot replanning identity
```

Do not automatically begin EEG/full-system integration, UI, logging infrastructure, experiments, or dependency maintenance.

---

# 4. UNRESOLVED EXPERIMENTAL DECISIONS

The following remain unresolved and are not authorized by this close:

```text
U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
```
