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
M5-T02 Shared-Autonomy / Human-Interaction Authorization Bridge accepted and merged.
D-068 Shared-Autonomy to Human-Interaction Authorization Contract approved.

Current module:
None — M5-T02 is closed; next boundary is interruptible human-authority-aware execution integration.

Current task:
None

Task status:
NO ACTIVE IMPLEMENTATION TASK

Canonical branch:
main

Latest accepted task-branch software commit:
fb2e088d27f9e5513d5a63c162a7ab802ddf7f52

Latest accepted software task:
M5-T02 — Shared-Autonomy / Human-Interaction Authorization Bridge

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
M5-T02 — Shared-Autonomy / Human-Interaction Authorization Bridge
```

Total accepted implementation tasks: 17.

---

# 3. M5-T02 ACCEPTED STATE

Accepted software commit:

```text
fb2e088d27f9e5513d5a63c162a7ab802ddf7f52
```

Accepted scope:

```text
src/control/interaction_bridge.py
src/control/human_interaction.py
tests/test_interaction_bridge.py
tests/test_human_interaction.py
```

Accepted behavior:

```text
SharedAutonomyDecision routes only into deterministic authorization state
exact current symbolic goal-registry keys only
PROCEED cannot bypass PAUSE / STOP / active confirmation
valid PROCEED adopts only an exact symbolic policy-approved goal
CONFIRM opens one explicit caller-ID request and never autonomously approves
CONFIRM may open while paused but cannot clear pause; STOP blocks registration
WAITING / DEFER preserve state and hold
human_action is never re-synthesized as a duplicate HumanCommand
conflicting human-authority/controller state fails closed
forged/inconsistent SharedAutonomyDecision values fail closed
no planner/safety/environment/executor/replanning/EEG/model/adaptation/UI integration
```

Accepted verification:

```text
python -m pytest tests/test_interaction_bridge.py tests/test_human_interaction.py tests/test_shared_autonomy.py
-> 54 passed

python -m pytest tests/test_shared_autonomy.py tests/test_human_interaction.py tests/test_interaction_bridge.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py
-> 100 passed

python -m pytest
-> 256 passed, 1 warning
```

The warning is the already-known non-failing PyTorch `padding='same'` warning from the accepted EEGNet/calibration path.

Verification used a temporary GitHub Actions environment rooted at the accepted M5-T02 code. `pandas` and `scikit-learn` were installed only into that verification environment because `requirements.txt` still omits those pre-existing dependencies. No verification workflow or dependency change was merged into `main`.

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
Shared-autonomy -> human-interaction authorization bridge: PASS
Human-authority-aware interruptible execution integration: NOT STARTED
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
policy bridge cannot synthesize duplicate human commands
```

---

# 5. KNOWN OPERATIONAL ISSUE

`requirements.txt` currently omits `pandas` and `scikit-learn`, although accepted pre-M5 modules/tests require them.

This remains a separate maintenance issue and was not changed in M5-T02.

---

# 6. CURRENT SCIENTIFIC / ARCHITECTURAL BLOCKERS

M5-T02:

```text
None — task accepted and merged.
```

Next M5 execution integration:

```text
Not yet authorized.
The current accepted executor consumes a complete planned route synchronously, while D-067 requires runtime PAUSE / STOP / OVERRIDE precedence.
A separately reviewed contract is required for interruptible stepwise execution and current-environment symbolic-goal-to-coordinate resolution before Codex implementation.
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
the software now includes a deterministic D-068 authorization bridge from accepted shared-autonomy decisions into human-interaction goal/confirmation state, with exact symbolic-goal validation, human-command duplicate-path protection, and no direct movement execution
```

Not authorized:

```text
runtime interruptible human-command-to-navigation integration implemented
end-to-end EEG-driven mission execution implemented
any reportable improvement in task success, safety, calibration, intent inference, or shared autonomy
cross-subject generalization claims
live EEG / physical robot / certified real-world safety claims
```

---

# 8. NEXT ACTION

```text
No Codex task is currently authorized.
Project Owner + ChatGPT must review and freeze the next narrow M5 execution-integration contract before creating another CURRENT_TASK.md ticket.
Do not automatically begin M5-T03, full-system EEG integration, UI, experiments, or dependency maintenance.
```
