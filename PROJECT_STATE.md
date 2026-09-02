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

Current module:
M5 shared-autonomy / human-interaction integration

Current task:
None

Task status:
NO ACTIVE IMPLEMENTATION TASK

Canonical branch:
main

Latest accepted task-branch software commit:
c45ef7e36136007f79f2881a1ebbf7afd2fcbbc6

Latest accepted software task:
M5-T03 — Human-Authority-Aware Stepwise Navigation Runtime

Latest approved scientific/architectural decision:
D-069 — Interruptible Navigation Execution Contract

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

Total accepted implementation tasks: 18.

---

# 3. CURRENT M5 STATE

```text
Shared-autonomy decision policy: PASS
Human command / confirmation state layer: PASS
Shared-autonomy -> human-interaction authorization bridge: PASS
Fresh authorization -> human-authority-aware stepwise navigation runtime: PASS
D-066 replacement-snapshot stepwise replanning integration: NOT STARTED
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
```

Accepted D-069 runtime boundary:

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

---

# 4. M5-T03 ACCEPTED BEHAVIOR

```text
start_navigation performs zero movement
advance_one_step performs at most one safety-approved transition
fresh accepted authorization required to begin navigation
unique caller-supplied execution_id; consumed/closed IDs cannot replay
exact symbolic key -> current environment coordinate only
wrong-terminal-goal paths fail closed
PAUSE invalidates old executable plan; RESUME requires fresh plan/new execution ID
STOP terminates current navigation session
OVERRIDE invalidates old goal/path before further movement
active confirmation/HOLD blocks movement despite stored historical goal
stale map/config/goal/position/terminal state fails closed
safety checked immediately before every environment step
REPLAN_REQUIRED returns explicit hold/replan state with zero movement and no unchanged-map retry
no human-command synthesis/duplicate processing in runtime
accepted M4 whole-route executor/replanner remain unchanged
```

Accepted authority remains `STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > shared-autonomy policy`; safety retains low-level movement veto.

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

`requirements.txt` currently omits `pandas` and `scikit-learn`, although accepted pre-M5 modules/tests require them. Clean verification installed them only into the test environment. This dependency-manifest maintenance remains separately unauthorized.

---

# 7. CURRENT BLOCKERS / NEXT REVIEW

No active implementation blocker exists because no implementation task is currently authorized.

The next architectural review is the D-066 replacement-snapshot + D-069 stepwise runtime integration boundary, likely a future M5-T04 only after Project Owner approval.

Before authorization, freeze at least:

```text
explicit environment-change event and immutable replacement snapshot semantics
current-position and approved-goal preservation
one replan maximum per supplied change event
human authority precedence during/after replacement handling
stale session/execution invalidation
fresh planning against replacement snapshot only
no unchanged-map retry
no goal substitution or hard-safety relaxation
execution/session identity across the replan boundary
```

Experimental unresolved items remain U-034 final A/B/C/D matrix, U-035 robustness perturbation levels, and U-036 inferential-statistics policy.

---

# 8. CLAIM STATUS

Authorized implementation claims now extend through accepted M5-T03 stepwise human-authority-aware simulated navigation.

Do not claim D-066 replacement-snapshot stepwise replanning integration, end-to-end EEG-driven mission execution, reportable system improvement, live EEG, physical robot, or certified real-world safety.

---

# 9. NEXT ACTION

ChatGPT + Project Owner review the exact D-066 replacement-snapshot / D-069 stepwise navigation transition contract before any M5-T04 implementation authorization.

Do not begin M5-T04, M6, UI, experiments, or dependency maintenance automatically.
