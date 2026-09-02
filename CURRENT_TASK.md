# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no implementation task is currently authorized.  
**Current status:** NO ACTIVE IMPLEMENTATION TASK
**Current milestone:** Pre-M6 Audit Remediation
**Task ID:** None
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-09-02

---

# 1. CLOSED TASK RECORD — M5-T04

```text
Task ID: M5-T04
Task title: Stepwise Replacement-Snapshot Replanning Integration
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Task branch: task/m5-t04-stepwise-replanning
Accepted software commit:
12a5230c0e4c3adcf83a687dfe5e5155e4f446e1
```

Accepted files:

```text
src/control/navigation_runtime.py
tests/test_navigation_replanning.py
```

Accepted D-070 behavior:

```text
NavigationRuntime.replan_after_environment_change(...) integrates D-066 replacement-snapshot replanning into the accepted D-069 stepwise runtime
replanning performs zero environment.step() calls and zero SafetyController.check() calls
accepted triggers are explicit ENVIRONMENT_CHANGED or genuine prior REPLAN_REQUIRED plus a new validated changed snapshot
caller-supplied event_id is unique and permits at most one actual planner invocation
invalid pre-planner requests do not consume event_id
once A* invocation begins, the event is consumed regardless of READY / NO_SAFE_PATH / INVALID_GOAL_OR_PLAN
replacement route uses a distinct new execution_id; source execution cannot replay
same exact human-approved symbolic goal is preserved across environment replanning
replacement snapshot preserves grid dimensions, exact goal registry, approved-goal coordinate, and current position
only blocked_cells and/or risk_map may change, and at least one must genuinely differ
STOP, PAUSE, active confirmation, approved-goal change, stale source state, or invalid replacement prevent planner invocation
changed-while-paused continuation requires valid RESUME semantics and never replays the old route
safety REPLAN_REQUIRED alone cannot retry an unchanged map
replacement planner output reuses D-069 integrity and wrong-terminal-goal checks
NO_SAFE_PATH is stationary and cannot retry using the same consumed event
successful replanning creates a zero-movement READY replacement NavigationSession
all subsequent movement remains exclusively through advance_one_step()
accepted M4 whole-route executor and ControlledReplanningCoordinator remain unchanged and are not invoked by the M5 stepwise replan path
no async/background/event-bus/retry-worker behavior was added
```

Independent exact-candidate verification was run in a clean GitHub Actions environment whose workflow parent was explicitly verified as the accepted task commit:

```text
python -m pytest tests/test_navigation_runtime.py tests/test_navigation_replanning.py tests/test_human_interaction.py tests/test_interaction_bridge.py tests/test_planner.py tests/test_safety.py
-> 105 passed in 0.52s

python -m pytest tests/test_navigation_runtime.py tests/test_navigation_replanning.py tests/test_human_interaction.py tests/test_interaction_bridge.py tests/test_planner.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py tests/test_shared_autonomy.py
-> 143 passed in 0.36s

python -m pytest
-> 281 passed, 1 warning in 26.83s
```

The warning is the already-known non-failing PyTorch `padding='same'` warning from the accepted EEGNet/calibration path.

The clean verification environment installed `pandas` and `scikit-learn` separately because `requirements.txt` still omits those pre-existing dependencies. M5-T04 did not modify `requirements.txt`.

---

# 2. CLOSED TASK RECORD — PRE-M6-R01

```text
Task ID: PRE-M6-R01
Task title: M4 Wrong-Terminal Route Protection
Phase: Pre-M6 Audit Remediation
Task branch: task/m4-remediate-wrong-terminal-goal
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Accepted software commit:
470106faee4dc6351a6826f7dd37b358941c1a13
Canonical main/software SHA:
470106faee4dc6351a6826f7dd37b358941c1a13
```

Accepted behavior:

```text
PlannerSafetyEnvironmentExecutor rejects a structurally valid planner SUCCESS route when an intermediate coordinate is another configured terminal goal different from the approved goal coordinate.
The check occurs after structural plan validation and before SafetyController.check() or environment.step().
Rejection is INVALID_GOAL_OR_PLAN with zero movement, zero executed actions, zero safety decisions, unchanged non-terminated environment state, and unchanged approved goal coordinate.
Valid multi-goal routes that do not cross another configured terminal remain executable.
ControlledReplanningCoordinator inherits the corrected fail-closed behavior through the M4 executor while retaining D-066 event-consumption behavior.
M5 NavigationRuntime, planner, risk, environment, and safety semantics were not modified.
```

Independent clean GitHub Actions verification used temporary workflow commit `d6dd594cde91c2d1f21adb465dc3a1cc08c04dd9`, whose parent was verified as the accepted candidate. Primary run `33600560760` / job `100153096772` and final evidence run `33601227845` / job `100155145125` both concluded successfully after focused, adjacent, and full pytest steps. `pandas` and `scikit-learn` were installed only in CI because the existing `requirements.txt` omission remains separately unauthorized.

PRE-M6-R01 is complete. Do not begin PRE-M6-R02 automatically. Do not begin M6.

---

# 3. NEXT ARCHITECTURAL BOUNDARY

The next project boundary is offline EEG-to-full-system integration after separate review and explicit Project Owner approval.

Before any M6 implementation ticket is created, ChatGPT and the Project Owner must review the exact end-to-end integration contract connecting the already accepted offline EEG decoding / calibration / Bayesian inference / uncertainty-aware shared autonomy / human authorization layers to the accepted M5 stepwise navigation runtime.

The review must preserve at least:

```text
offline prerecorded EEG / simulated real-time BCI only
no live EEG or hardware claim
accepted binary left/right decoder semantics and approved goal-inference rules
no fabricated direct multi-goal decoder
calibrated probabilities and Bayesian thresholds remain unchanged
human WHAT authority and confirmation/override/pause/stop precedence remain unchanged
fresh execution authorization remains required before navigation
D-069 stepwise movement and D-070 replacement-snapshot replanning remain authoritative
safety veto before every movement
no automatic scope expansion into UI, reportable experiments, logging infrastructure, or dependency maintenance
```

---

# 4. UNRESOLVED EXPERIMENTAL DECISIONS

The following remain unresolved and are not authorized by this close:

```text
U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
```
