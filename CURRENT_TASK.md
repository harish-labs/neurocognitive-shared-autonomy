# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Current status:** ACTIVE
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / Decoders / Calibration / Bayesian Goal Inference / Shared-Autonomy Policy
**Task ID:** M1-T09
**Task title:** Uncertainty & Shared-Autonomy Policy
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Repository instructions:** `AGENTS.md`
**Canonical branch:** `main` at `a5e2379c6cf4d843ab1d326b0b8c54372609b9d3`
**Task branch:** `task/m1-t09-shared-autonomy-policy`
**Last updated:** 2026-08-31

---

# 1. AUTHORIZED SCOPE

Implement only M1-T09 under D-055 through D-057 while preserving D-014, D-015, and D-016.

Allowed files:

```text
src/cognitive/uncertainty.py
src/control/shared_autonomy.py
tests/test_uncertainty.py
tests/test_shared_autonomy.py
CURRENT_TASK.md
__init__.py only if necessary
```

Required behavior:

```text
- binary Bayesian-posterior Shannon entropy in bits is the explicit uncertainty measure
- posterior thresholds are authoritative; entropy cannot select a contradictory action
- posterior >= 0.90 -> PROCEED
- before update 5 and below 0.90 -> WAITING only
- at update 5: >= 0.90 -> PROCEED; >= 0.75 and < 0.90 -> CONFIRM; < 0.75 -> DEFER
- CONFIRM requires explicit human approval and must not silently approve a candidate
- DEFER never selects an argmax or authorizes movement; it holds position and requests explicit human input
- PAUSE, STOP, and OVERRIDE take precedence over the normal confidence policy
- no reset, resume, corrected-goal, movement, planner, safety, or adaptation transition is implemented
```

Required verification:

```text
pytest tests/test_uncertainty.py tests/test_shared_autonomy.py tests/test_bayes.py tests/test_calibration.py tests/test_eegnet.py tests/test_csp_lda.py tests/test_splits.py tests/test_epochs.py tests/test_preprocessing.py tests/test_loader.py
```

A bounded synthetic handoff from a Bayesian episode result through entropy to the shared-autonomy decision is allowed as integration evidence only.

---

# 2. EXPLICITLY OUT OF SCOPE

Do not modify:

```text
DECISIONS.md
MASTER_PROJECT_SPEC.md
PROJECT_STATE.md
TODO.md
EXPERIMENT_LOG.md
```

Do not implement planner, A*, safety controller, environment movement, adaptation, replay, UI/Streamlit, reportable experiments, or U-026 and later decisions.

Do not merge this branch. Stop after testing, bounded synthetic smoke verification, commit, push, and report for scientific review.
