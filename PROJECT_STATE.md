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
M5-T01 through M5-T04 accepted and merged.
D-069 Interruptible Navigation Execution Contract approved and implemented through M5-T03.
D-070 Stepwise Replacement-Snapshot Replanning Contract approved and implemented through M5-T04.
Pre-M6 audit remediation has begun: PRE-M6-R01 is active.

Current module:
Pre-M6 remediation: M4 wrong-terminal route protection

Current task:
PRE-M6-R01 — M4 Wrong-Terminal Route Protection

Task status:
ACTIVE IMPLEMENTATION TASK

Canonical branch:
main

Latest accepted task-branch software commit:
12a5230c0e4c3adcf83a687dfe5e5155e4f446e1

Latest accepted software task:
M5-T04 — Stepwise Replacement-Snapshot Replanning Integration

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
M5-T04 — Stepwise Replacement-Snapshot Replanning Integration
```

Total accepted implementation tasks: 19.

---

# 3. CURRENT M5 STATE

```text
Shared-autonomy decision policy: PASS
Human command / confirmation state layer: PASS
Shared-autonomy -> human-interaction authorization bridge: PASS
Fresh authorization -> human-authority-aware stepwise navigation runtime: PASS
D-066 replacement-snapshot stepwise replanning integration: PASS
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
```

Accepted runtime boundary now includes:

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
        ↓
explicit changed replacement snapshot when D-066/D-070 replanning is needed
        ↓
zero-movement fresh replacement plan
        ↓
new execution identity
        ↓
resume ordinary one-step authority + safety gating
```

---

# 4. M5-T04 ACCEPTED BEHAVIOR

```text
NavigationRuntime provides stepwise replacement-snapshot replanning under D-070
replan itself performs zero environment movement and zero safety checks
accepted triggers are explicit ENVIRONMENT_CHANGED or genuine REPLAN_REQUIRED plus a new changed snapshot
event_id is caller-supplied, replay-protected, and permits at most one actual planner invocation
invalid pre-planner requests do not consume the event
once planner invocation begins, the event remains consumed regardless of planning outcome
replacement route uses a new execution_id and cannot resurrect the old route
same exact human-approved symbolic goal is preserved
replacement snapshot preserves grid size, goal registry, approved-goal coordinate, and current agent position
only blocked_cells and/or risk_map may change and at least one must genuinely differ
STOP, PAUSE, active confirmation, changed approved goal, stale source state, and invalid snapshots fail closed before planning
changed-while-paused continuation requires valid RESUME semantics and never replays queued old movement
safety REPLAN_REQUIRED cannot retry an unchanged map
NO_SAFE_PATH is explicit and stationary with no same-event retry
replacement planner output preserves D-069 integrity and wrong-terminal-goal protection
successful replan creates a zero-movement READY replacement NavigationSession
movement after replanning occurs only through advance_one_step()
accepted M4 whole-route executor/replanner remain unchanged and are not invoked by the M5 stepwise replan path
```

Accepted authority remains `STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > shared-autonomy policy`; safety retains low-level movement veto.

---

# 5. M5-T04 ACCEPTED VERIFICATION

Independent exact-candidate verification in GitHub Actions:

```text
focused -> 105 passed in 0.52s
adjacent -> 143 passed in 0.36s
full -> 281 passed, 1 warning in 26.83s
```

The warning is the known non-failing PyTorch `padding='same'` warning from the accepted EEGNet/calibration path.

---

# 6. KNOWN OPERATIONAL ISSUE

`requirements.txt` currently omits `pandas` and `scikit-learn`, although accepted pre-M5 modules/tests require them. Clean verification installed them only into the test environment. This dependency-manifest maintenance remains separately unauthorized.

---

# 7. CURRENT BLOCKERS / NEXT REVIEW

PRE-M6-R01 is the only active implementation task. It remediates M4 whole-route execution/replanning so a route that crosses a different configured terminal before the already-approved goal fails closed before safety or movement. The task must not be marked accepted or closed until separate review.

The next architectural review remains the offline EEG-to-full-system integration boundary. No M6 task is authorized yet.

Before authorization, preserve at least:

```text
public prerecorded EEG / offline replay / simulated real-time BCI only
accepted decoder, calibration, Bayesian, uncertainty, shared-autonomy, and human-command semantics
binary EEG evidence must not be silently converted into a fabricated direct multi-goal decoder
human WHAT authority remains explicit
fresh navigation authorization remains required
D-069 stepwise navigation remains authoritative
D-070 event-bounded replacement-snapshot replanning remains authoritative
safety veto remains mandatory before every environment transition
no UI, reportable experiments, logging infrastructure, hardware integration, or dependency maintenance without separate authorization
```

Experimental unresolved items remain U-034 final A/B/C/D matrix, U-035 robustness perturbation levels, and U-036 inferential-statistics policy.

---

# 8. CLAIM STATUS

Authorized implementation claims now extend through accepted M5-T04 human-authority-aware simulated stepwise navigation with explicit event-bounded replacement-snapshot replanning.

Do not claim end-to-end EEG-driven mission execution, reportable system improvement, live EEG, physical robot, human-subject results, or certified real-world safety.

---

# 9. NEXT ACTION

ChatGPT + Project Owner review the exact offline EEG-to-full-system integration architecture before any M6 implementation authorization.

Do not begin M6, UI, experiments, logging infrastructure, hardware integration, or dependency maintenance automatically.
