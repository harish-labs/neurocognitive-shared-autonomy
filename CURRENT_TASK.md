# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### No Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no task is currently authorized  
**Current status:** NO ACTIVE TASK  
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / Decoders / Calibration / Bayesian Goal Inference / Shared-Autonomy Policy / Prior Personalization  
**Task ID:** NONE AUTHORIZED  
**Task title:** Awaiting next approved implementation ticket  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-08-31

---

# 1. CURRENT AUTHORIZATION STATE

There is currently no active implementation task authorized for Codex.

Completed, scientifically reviewed, accepted, and merged on canonical `main`:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
M1-T07 — Probability Calibration
M1-T08 — Bayesian Goal Inference
M1-T09 — Uncertainty & Shared-Autonomy Policy
M1-T10 — Adaptation / Prior Personalization
```

Do not begin another implementation module until a new narrow `CURRENT_TASK.md` ticket is explicitly approved by the Project Owner.

---

# 2. CLOSED TASK RECORD — M1-T10

```text
Task ID:
M1-T10

Task title:
Adaptation / Prior Personalization

Final status:
PASS / ACCEPTED / MERGED

Task branch:
task/m1-t10-prior-personalization

Accepted task-branch head / canonical software commit:
9aeb3477c0bb7304bca3ad2753eaa3a75a59511c
```

M1-T10 operationalizes approved D-058 through D-060.

Accepted behavior:

```text
subject-specific, candidate-pair-specific prior personalization
order-independent stable candidate-pair identity
alpha_A = 1 / alpha_B = 1 initialization
explicit human-approved CONFIRM / corrected OVERRIDE feedback only
PAUSE / STOP / unresolved DEFER / autonomous PROCEED without explicit feedback do not adapt
3-valid-feedback warm-up
adaptation OFF and warm-up use [0.5,0.5]
post-warm-up adaptive prior bounded to [0.25,0.75]
explicit reset returns alpha 1/1, update_count 0, prior [0.5,0.5]
traceable update records keyed by anonymous subject and candidate pair
personalized prior may initialize a fresh Bayesian episode only
mid-sequence custom-prior injection is rejected
default Bayesian episode prior remains [0.5,0.5]
Bayesian evidence-update mathematics remain unchanged
no threshold adaptation, evidence weighting, model retraining, planner, safety, environment, replay, or UI implemented
```

Accepted regression evidence reported from the task branch:

```text
124 passed, 1 warning
```

The warning is the previously reviewed non-failing PyTorch EEGNet `padding='same'` warning.

Corrected bounded synthetic integration smoke:

```text
adaptation OFF -> (0.5, 0.5)
three valid explicit feedback events -> personalized prior (0.75, 0.25)
fresh Bayesian episode initial posterior -> (0.75, 0.25)
after evidence (0.8, 0.2) -> posterior approximately (0.9230769231, 0.0769230769)
```

This smoke is integration evidence only. It does not establish personalization benefit, improved decoding, improved intent inference, task success, or safety.

Implementation-path note:

```text
The cognitive/adaptation specification names src/cognition/adaptation.py.
The established repository package is src/cognitive/.
M1-T10 therefore uses src/cognitive/adaptation.py without changing the scientific architecture.
```

---

# 3. NEXT GOVERNANCE GATE

The next unresolved scientific boundary begins at U-029 planning/safety.

Before any further implementation:

```text
1. Identify one narrow next module.
2. Check MASTER_PROJECT_SPEC.md.
3. Check CURRENT_TASK.md.
4. Check PROJECT_STATE.md.
5. Check DECISIONS.md.
6. Check relevant technical documentation and accepted code/tests.
7. Resolve any blocking scientific/architectural decision.
8. Record any newly approved decision in DECISIONS.md.
9. Obtain explicit Project Owner approval for exactly one narrow task.
10. Only then activate CURRENT_TASK.md and begin implementation.
```

U-029 and later unresolved decisions remain unauthorized.

Until a new task is explicitly approved:

```text
STOP
STATUS = NO ACTIVE TASK
```
