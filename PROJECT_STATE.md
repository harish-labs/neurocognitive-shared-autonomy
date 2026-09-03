# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Last updated:** 2026-09-03

---

# 1. STATUS AT A GLANCE

```text
Project phase:
M1-T01 through M1-T10 accepted and merged.
M4-T01 through M4-T05 accepted and merged.
M5-T01 through M5-T04 accepted and merged.
D-069 Interruptible Navigation Execution Contract approved and implemented through M5-T03.
D-070 Stepwise Replacement-Snapshot Replanning Contract approved and implemented through M5-T04.
Pre-M6 audit remediation remains in progress: PRE-M6-R01 through PRE-M6-R05 are complete and PRE-M6-R06 is active.

Current module:
PRE-M6-R06 — Accepted-Code Dependency Manifest Reconciliation

Current task:
PRE-M6-R06

Task status:
ACTIVE IMPLEMENTATION TASK

Canonical branch:
main

PRE-M6-R06 authorization base:
eb5b8cd58c7a7e0a52d293e62d91870532559177

Latest accepted task-branch software commit:
2ccb665cf20666d1af7abb931a481a27d402d7e6

Latest accepted software task:
PRE-M6-R05 — Central Runtime Composition Configuration

Latest approved scientific/architectural decision:
D-073 — YAML Parser Dependency Contract

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
PRE-M6-R01 — M4 Wrong-Terminal Route Protection: PASS / MERGED
PRE-M6-R02 — Human OVERRIDE Symbolic Goal Identity Correction: PASS / MERGED
PRE-M6-R03 — Environment Snapshot Immutability and Goal Registry Hardening: PASS / MERGED
PRE-M6-R04 — Adaptation Disabled-State Mutation Correction: PASS / MERGED
PRE-M6-R05 — Central Runtime Composition Configuration: PASS / MERGED
```

Total accepted implementation tasks: 24.

PRE-M6-R06 is authorized but not yet accepted; it is therefore not included in the accepted-task count.

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

# 6. CURRENT PRE-M6-R06 REMEDIATION

The dependency manifest remains incomplete for already accepted code. Canonical `requirements.txt` currently omits direct dependencies already used by accepted modules/tests, including the previously verified `pandas`, `scikit-learn`, and `matplotlib` requirements.

PRE-M6-R06 is now explicitly authorized to audit and reconcile `requirements.txt` against direct third-party imports of accepted code/tests through PRE-M6-R05.

Scope is intentionally narrow:

```text
requirements.txt only
accepted-code direct dependencies only
no future-only dependencies
no automatic Streamlit addition while UI is unimplemented
no dependency version freezing
no new packaging/environment/lockfile policy
no production/test behavior changes
no M6 implementation
```

The task is not yet accepted. Codex must implement, install from the reconciled manifest in a clean environment where available, run the full test suite, and report actual evidence before scientific/engineering review and merge acceptance.

---

# 7. CURRENT BLOCKERS / NEXT REVIEW

PRE-M6-R01 through PRE-M6-R05 are PASS / MERGED.

PRE-M6-R06 — Accepted-Code Dependency Manifest Reconciliation is ACTIVE and separately authorized by the Project Owner. Its authorization does not alter D-073's R05-specific historical scope; it creates a new narrow remediation task for dependency reconciliation.

Before any later authorization, preserve at least:

```text
public prerecorded EEG / offline replay / simulated real-time BCI only
accepted decoder, calibration, Bayesian, uncertainty, shared-autonomy, and human-command semantics
binary EEG evidence must not be silently converted into a fabricated direct multi-goal decoder
human WHAT authority remains explicit
fresh navigation authorization remains required
D-069 stepwise navigation remains authoritative
D-070 event-bounded replacement-snapshot replanning remains authoritative
safety veto remains mandatory before every environment transition
no UI, reportable experiments, logging infrastructure, hardware integration, or unrelated dependency/packaging work without separate authorization
```

Experimental unresolved items remain U-034 final A/B/C/D matrix, U-035 robustness perturbation levels, and U-036 inferential-statistics policy.

---

# 8. CLAIM STATUS

Authorized implementation claims remain limited to accepted work through PRE-M6-R05 and M5-T04. PRE-M6-R06 is maintenance authorization only and is not yet accepted.

Do not claim end-to-end EEG-driven mission execution, reportable system improvement, live EEG, physical robot, human-subject results, or certified real-world safety.

---

# 9. NEXT ACTION

Execute only PRE-M6-R06 — Accepted-Code Dependency Manifest Reconciliation on its task branch from the recorded canonical authorization base.

After implementation, run/verify/review before acceptance.

Do not begin another remediation item automatically.

Do not begin M6 until Pre-M6 remediation is explicitly completed and the Pre-M6 audit is explicitly passed.
