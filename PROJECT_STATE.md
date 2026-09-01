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

Current module:
None — M5-T01 is closed; next boundary is M5 shared-autonomy / human-command integration.

Current task:
None

Task status:
NO ACTIVE IMPLEMENTATION TASK

Canonical branch:
main

Latest accepted task-branch software commit:
732cf91890e22a1a66bbe918a4b01500af5966f2

Latest accepted software task:
M5-T01 — Human Command & Confirmation State Layer

Latest approved scientific/architectural decision commit:
0c2ed84207f55303610d8b7c61bd9e99eea8301a

Latest governance close commit:
60a8fda01a3923d789a2dafa657523a234061bce

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

Total accepted implementation tasks: 16.

---

# 3. M5-T01 ACCEPTED STATE

Accepted software commit:

```text
732cf91890e22a1a66bbe918a4b01500af5966f2
```

Accepted scope:

```text
src/control/human_interaction.py
tests/test_human_interaction.py
```

Accepted behavior:

```text
D-067 command/request identity semantics enforced
CONFIRM requires exact active request and approves only its attached candidate
stale confirmations fail closed
command IDs are consumed once; duplicates do not repeat effects
OVERRIDE validates exact currently valid goals and fails closed for unsupported containers
OVERRIDE changes only human-approved goal state and never bypasses planner/safety
PAUSE preserves state
RESUME is explicit, valid only from PAUSED, preserves the approved goal, and never replays queued motion
STOP is terminal until explicit reset/new session
headless deterministic state layer only
no planner/safety/environment/EEG/Bayesian/UI integration was added in M5-T01
```

Accepted verification:

```text
python -m pytest tests/test_human_interaction.py
-> 19 passed

python -m pytest tests/test_shared_autonomy.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py tests/test_human_interaction.py
-> 77 passed

python -m pytest
-> 233 passed, 1 warning
```

The warning is the already-known non-failing PyTorch `padding='same'` warning from the accepted EEGNet/calibration path.

Verification was executed in a temporary GitHub Actions environment rooted at the accepted M5-T01 task SHA. The temporary CI workflow was not merged into `main`.

---

# 4. CURRENT AUTONOMY / INTERACTION STATE

```text
SAR environment/risk map: PASS
Risk-aware A*: PASS
Hard safety controller: PASS
Planner -> safety -> environment execution integration: PASS
Controlled replanning after explicit environment change: PASS
Shared-autonomy decision policy: PASS
Human command / confirmation state layer: PASS
Shared-autonomy -> human-command integration: NOT STARTED
Human-command -> planner/safety/execution integration: NOT STARTED
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
```

Accepted authority principles remain:

```text
human determines WHAT goal; AI determines HOW safely
STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > autonomous policy
safety retains veto authority over low-level movement
human override cannot relax hard safety
stale/duplicate human commands cannot cause repeated effects
```

---

# 5. KNOWN OPERATIONAL ISSUE

Clean-environment regression exposed a pre-existing dependency-manifest gap:

```text
requirements.txt currently omits pandas and scikit-learn
accepted pre-M5 modules/tests require them
```

For M5-T01 verification, `pandas` and `scikit-learn` were installed only in the temporary CI environment so the existing regression suite could execute. No dependency-file change was bundled into M5-T01.

This should be handled separately through a narrow maintenance/governance action; it is not evidence of an M5-T01 software regression.

---

# 6. CURRENT SCIENTIFIC / ARCHITECTURAL BLOCKERS

M5-T01:

```text
None — task accepted and merged.
```

Next M5 integration:

```text
Not yet authorized.
The exact shared-autonomy-decision -> human-command -> approved-goal/execution transition contract must be reviewed and frozen before Codex implementation.
```

Experimental analysis remains unresolved:

```text
U-034 — Final A/B/C/D component matrix
U-035 — Robustness perturbation levels
U-036 — Final inferential-statistics policy
```

---

# 7. CLAIM STATUS

Authorized implementation claim:

```text
the software now includes a deterministic human command and confirmation state layer implementing the approved D-067 CONFIRM / OVERRIDE / PAUSE / RESUME / STOP contract, with stale/duplicate protection and no direct movement execution
```

Not authorized:

```text
full human-interaction integration implemented
end-to-end EEG-driven mission execution implemented
any reportable improvement in task success, safety, calibration, intent inference, or shared autonomy
cross-subject generalization claims
live EEG / physical robot / certified real-world safety claims
```

---

# 8. NEXT ACTION

```text
No Codex task is currently authorized.
Project Owner + ChatGPT must review and freeze the next narrow M5 integration contract before creating another CURRENT_TASK.md ticket.
Do not automatically begin full-system EEG integration, UI, or experiments.
Separately address the requirements.txt dependency-manifest gap through a narrow maintenance action when approved.
```
