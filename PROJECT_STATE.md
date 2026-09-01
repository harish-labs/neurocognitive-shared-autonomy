# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Last updated:** 2026-09-01

---

# 1. STATUS AT A GLANCE

```text
Project phase:
M1-T01 through M1-T10 accepted and merged.
M4-T01 through M4-T05 accepted and merged.
M5-T01 through M5-T02 accepted and merged.
D-069 Interruptible Navigation Execution Contract approved.
M5-T03 Human-Authority-Aware Stepwise Navigation Runtime authorized and not yet implemented.

Current module:
Human-authority-aware stepwise execution integration

Current task:
M5-T03

Task status:
ACTIVE / NOT STARTED

Canonical branch:
main

Latest accepted task-branch software commit:
fb2e088d27f9e5513d5a63c162a7ab802ddf7f52

Latest accepted software task:
M5-T02 — Shared-Autonomy / Human-Interaction Authorization Bridge

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
```

Total accepted implementation tasks: 17. M5-T03 is authorized but not accepted yet.

---

# 3. CURRENT M5 STATE

```text
Shared-autonomy decision policy: PASS
Human command / confirmation state layer: PASS
Shared-autonomy -> human-interaction authorization bridge: PASS
D-069 interruptible execution contract: APPROVED
Fresh authorization -> stepwise navigation runtime: AUTHORIZED / NOT STARTED
D-066 replacement-snapshot stepwise replanning integration: NOT STARTED
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
```

D-069 runtime boundary:

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

# 4. D-069 AUTHORITY SUMMARY

```text
one environment step maximum per advance call
start_navigation performs zero movement
new runtime layer; accepted M4 whole-route executor/replanner stay unchanged
movement requires fresh accepted M5 authorization
unique caller-supplied execution_id
exact symbolic key -> current environment coordinate only
PAUSE invalidates old executable plan; RESUME replans fresh from current position
STOP terminates current navigation session
OVERRIDE invalidates old goal/path before any further movement
active confirmation/HOLD prevents movement despite stored historical goal
runtime never synthesizes/processes human commands
safety checked immediately before every environment step
safety requires_replan -> explicit hold; no unchanged-map retry
hidden map mutation or unexpected state movement -> fail closed
D-066 stepwise replacement-snapshot replanning reserved for later task
synchronous deterministic control only
```

Accepted authority remains `STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > shared-autonomy policy`; safety retains low-level movement veto.

---

# 5. M5-T02 ACCEPTED VERIFICATION

```text
focused -> 54 passed
adjacent -> 100 passed
full -> 256 passed, 1 known PyTorch warning
```

---

# 6. KNOWN OPERATIONAL ISSUE

`requirements.txt` currently omits `pandas` and `scikit-learn`, although accepted pre-M5 modules/tests require them. This remains separate maintenance and is not authorized in M5-T03.

---

# 7. CURRENT BLOCKERS

M5-T03:

```text
None under approved D-069 at authorization time.
```

Implementation must STOP if accepted interfaces require modification or another authority decision emerges.

M5-T04 remains deliberately unapproved. It will be the separately reviewed D-066 replacement-snapshot + human-aware stepwise replanning boundary after M5-T03 passes.

Experimental unresolved items remain U-034 final A/B/C/D matrix, U-035 robustness perturbation levels, and U-036 inferential-statistics policy. They do not block M5-T03.

---

# 8. CLAIM STATUS

Authorized implementation claims remain limited to accepted work through M5-T02.

M5-T03 is authorized but NOT implemented/verified yet. Do not claim runtime interruptible navigation exists until accepted code and tests are reviewed.

No end-to-end EEG-driven mission execution, reportable system improvement, live EEG, physical robot, or certified real-world safety claim is authorized.

---

# 9. NEXT ACTION

Codex implements M5-T03 exactly as `CURRENT_TASK.md` on a new branch from current canonical `main`, runs focused/adjacent/full regressions, commits/pushes, and STOPS for ChatGPT review.

Do not merge automatically. Do not begin M5-T04, M6, UI, experiments, or dependency maintenance.
