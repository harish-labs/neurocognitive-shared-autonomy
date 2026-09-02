# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Last updated:** 2026-09-02

---

# 1. STATUS AT A GLANCE

```text
Project phase:
M1-T01 through M1-T10 accepted and merged.
M4-T01 through M4-T05 accepted and merged.
M5-T01 through M5-T03 accepted and merged.
D-069 Interruptible Navigation Execution Contract approved and implemented through M5-T03.
D-070 Stepwise Replacement-Snapshot Replanning Contract approved.
M5-T04 Stepwise Replacement-Snapshot Replanning Integration authorized and not yet implemented.

Current module:
M5 shared-autonomy / human-interaction integration

Current task:
M5-T04

Task status:
ACTIVE / NOT STARTED

Canonical branch:
main

Latest accepted task-branch software commit:
c45ef7e36136007f79f2881a1ebbf7afd2fcbbc6

Latest accepted software task:
M5-T03 — Human-Authority-Aware Stepwise Navigation Runtime

Latest approved scientific/architectural decision:
D-070 — Stepwise Replacement-Snapshot Replanning Contract

Latest valid reportable experiment:
None yet
```

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, certified safety, or human-subject result claim is authorized.

---

# 2. ACCEPTED IMPLEMENTATION SEQUENCE

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
M1-T07 — Probability Calibration
M1-T08 — Bayesian Goal Inference
M1-T09 — Uncertainty / Shared-Autonomy Policy
M1-T10 — Adaptation / Prior Personalization
M4-T01 — 2D Search & Rescue Environment + Risk Map
M4-T02 — Risk-Aware A* Planner
M4-T03 — Safety Controller / Hard Constraint Enforcement
M4-T04 — Planner → Safety → Environment Execution Integration
M4-T05 — Controlled Replanning After Environment Change
M5-T01 — Human Command & Confirmation State Layer
M5-T02 — Shared-Autonomy / Human-Interaction Authorization Bridge
M5-T03 — Human-Authority-Aware Stepwise Navigation Runtime
```

Total accepted implementation tasks: 18. M5-T04 is authorized but not accepted yet.

---

# 3. CURRENT M5 STATE

```text
Shared-autonomy decision policy: PASS
Human command / confirmation state layer: PASS
Shared-autonomy -> human-interaction authorization bridge: PASS
Fresh authorization -> human-authority-aware stepwise navigation runtime: PASS
D-070 stepwise replacement-snapshot replanning contract: APPROVED
D-066 replacement-snapshot stepwise replanning integration: AUTHORIZED / NOT STARTED
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
```

Accepted D-069 execution boundary remains:

```text
fresh accepted authorization
        ↓
exact current symbolic goal resolution
        ↓
fresh A* plan, zero movement at start
        ↓
one-step control cycle
        ↓
current human authority check
        ↓
safety check
        ↓
at most one environment transition
```

D-070 adds the replacement transition:

```text
source execution
+ explicit valid replan trigger
+ unique event_id
+ validated changed replacement snapshot
+ new execution_id
        ↓
human authority recheck
        ↓
one fresh A* invocation maximum for that event
        ↓
zero-movement replacement READY session
        ↓
ordinary D-069 advance_one_step execution
```

---

# 4. D-070 AUTHORITY SUMMARY

```text
M5-T04 extends NavigationRuntime; accepted M4 replanner/executor remain unchanged
M5 runtime must not call ControlledReplanningCoordinator.replan or whole-route execute
replan operation performs zero environment movement and zero safety checks
accepted triggers only: explicit ENVIRONMENT_CHANGED or genuine prior REPLAN_REQUIRED + new changed snapshot
new changed validated snapshot is mandatory; unchanged-map retry forbidden
unique event_id; at most one actual planner invocation per event
pre-planner invalid requests do not consume event
once planner invocation begins, event is consumed regardless of planner outcome
replacement route requires a new unique execution_id; old execution cannot replay
same exact human-approved symbolic goal is preserved
replacement snapshot preserves dimensions, goal mapping, current position, and goal coordinate
only blocked_cells and/or risk_map may change and at least one must actually change
STOP / PAUSE / active confirmation / changed goal prevent unauthorized replan
changed-while-paused continuation requires explicit RESUME + replacement event/snapshot + new execution ID
safety REPLAN_REQUIRED alone does not permit unchanged-map retry
replacement plan uses full D-069 plan integrity, including wrong-terminal-goal protection
NO_SAFE_PATH holds with zero movement and no same-event retry
successful replacement session advances only through ordinary advance_one_step
multiple changes require new event IDs, replacement snapshots, and execution IDs
no hidden environment mutation or async/background retry infrastructure
```

Human authority remains `STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > shared-autonomy policy`; safety retains low-level movement veto.

---

# 5. M5-T03 ACCEPTED VERIFICATION

Independent exact-candidate verification:

```text
focused -> 95 passed in 0.48s
adjacent -> 133 passed in 0.34s
full -> 271 passed, 1 warning in 29.66s
```

The warning is the known non-failing PyTorch `padding='same'` warning from the accepted EEGNet/calibration path.

---

# 6. KNOWN OPERATIONAL ISSUE

`requirements.txt` currently omits `pandas` and `scikit-learn`, although accepted pre-M5 modules/tests require them. Clean verification may install them only into the test environment. Dependency-manifest maintenance remains separately unauthorized.

---

# 7. CURRENT BLOCKERS

M5-T04:

```text
None under approved D-070 at authorization time.
```

Implementation must STOP if an accepted interface requires modification or another scientific/architectural decision emerges.

Experimental unresolved items remain:

```text
U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
```

These do not block M5-T04.

---

# 8. CLAIM STATUS

Authorized implementation claims remain limited to accepted work through M5-T03.

D-070 is an approved architecture contract. M5-T04 is authorized but NOT implemented/verified yet. Do not claim stepwise replacement-snapshot replanning integration exists until accepted code and tests are reviewed.

Do not claim end-to-end EEG-driven mission execution, reportable system improvement, live EEG, physical robot, or certified real-world safety.

---

# 9. NEXT ACTION

Codex implements M5-T04 exactly as `CURRENT_TASK.md` on a task branch from current canonical `main`, runs focused/adjacent/full regressions, commits/pushes, and STOPS for ChatGPT review.

Do not merge automatically. Do not begin M6, UI, experiments, or dependency maintenance.
