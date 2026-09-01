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
M5-T01 Human Command & Confirmation State Layer accepted and merged.
D-068 Shared-Autonomy to Human-Interaction Authorization Contract approved.
M5-T02 Shared-Autonomy / Human-Interaction Authorization Bridge authorized and not yet implemented.

Current module:
Shared-autonomy / human-interaction authorization integration

Current task:
M5-T02

Task status:
ACTIVE / NOT STARTED

Canonical branch:
main

Latest accepted task-branch software commit:
732cf91890e22a1a66bbe918a4b01500af5966f2

Latest accepted software task:
M5-T01 — Human Command & Confirmation State Layer

Latest approved scientific/architectural decision:
D-068 — Shared-Autonomy to Human-Interaction Authorization Contract

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
```

Total accepted implementation tasks: 16. M5-T02 is authorized but not accepted yet.

---

# 3. CURRENT M5 STATE

```text
Shared-autonomy decision policy: PASS
Human command / confirmation state layer: PASS
D-068 authorization transition contract: APPROVED
Shared-autonomy -> human-command authorization bridge: AUTHORIZED / NOT STARTED
Human-command -> planner/safety/execution integration: NOT STARTED
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
```

D-068 boundary:

```text
SharedAutonomyDecision
        ↓
exact symbolic goal validation / confirmation routing
        ↓
HumanInteractionController authorization state
        ↓
STOP — no movement in M5-T02
```

Later execution integration must resolve the approved symbolic goal against the current environment snapshot and separately support interruptible runtime human authority.

---

# 4. D-068 AUTHORITY SUMMARY

```text
M5-T02 authorization-only; no movement
exact current symbolic goal identifiers only
PROCEED cannot bypass PAUSE/STOP/active confirmation
CONFIRM creates one explicit request and cannot autonomously approve
WAITING/DEFER create no commitment
human commands processed only by HumanInteractionController; bridge never synthesizes/double-applies them
no hard-coded binary EEG -> victim mapping
coordinate resolution/runtime execution reserved for later task
```

Accepted authority remains `STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > autonomous policy`; safety retains low-level veto.

---

# 5. M5-T01 ACCEPTED VERIFICATION

```text
python -m pytest tests/test_human_interaction.py -> 19 passed
python -m pytest tests/test_shared_autonomy.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py tests/test_human_interaction.py -> 77 passed
python -m pytest -> 233 passed, 1 known PyTorch warning
```

---

# 6. KNOWN OPERATIONAL ISSUE

`requirements.txt` currently omits `pandas` and `scikit-learn` although accepted pre-M5 modules/tests require them. This remains separate maintenance and is not authorized in M5-T02.

---

# 7. CURRENT BLOCKERS

M5-T02: none under D-068.

Later M5 execution integration is not authorized and must be separately reviewed after M5-T02, especially because the current executor consumes a whole route synchronously while PAUSE/STOP/OVERRIDE require interruptible runtime authority.

Experimental unresolved items remain U-034 final A/B/C/D matrix, U-035 robustness perturbation levels, and U-036 inferential-statistics policy. They do not block M5-T02.

---

# 8. CLAIM STATUS

Implementation claims remain limited to accepted tasks through M5-T01. M5-T02, full human-interaction execution integration, end-to-end EEG-driven mission execution, efficacy/safety improvements, live EEG, physical robot, and certified real-world safety are not yet authorized claims.

---

# 9. NEXT ACTION

Codex implements M5-T02 exactly as `CURRENT_TASK.md` on a new branch from current canonical `main`, runs focused/adjacent/full regressions, commits/pushes, and STOPS for ChatGPT review. Do not merge or begin M5-T03 automatically. Do not bundle dependency maintenance, EEG/full-system integration, UI, logging, or experiments.
