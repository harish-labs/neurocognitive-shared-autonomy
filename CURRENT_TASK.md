# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Current status:** ACTIVE
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / Decoders / Calibration / Bayesian Goal Inference
**Task ID:** M1-T08
**Task title:** Bayesian Goal Inference
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Repository instructions:** `AGENTS.md`
**Canonical branch:** `main` at `2cb9208a5f16d5f67fe5830caf1f0837f6ada6d8`
**Task branch:** `task/m1-t08-bayesian-goal-inference`
**Last updated:** 2026-08-31

---

# 1. AUTHORIZED SCOPE

Implement only the approved M1-T08 Bayesian goal-inference core under D-051 through D-054.

Allowed files:

```text
src/cognitive/bayes.py
tests/test_bayes.py
CURRENT_TASK.md
src/cognitive/__init__.py only if necessary
```

Required behavior:

```text
- exactly two active candidates per binary decision episode: candidate A and candidate B
- calibrated "left" evidence supports candidate A; calibrated "right" evidence supports candidate B
- use calibrated binary probabilities directly as candidate likelihood weights
- update posterior by previous posterior x evidence likelihood, then normalize
- initialize and reset every episode to prior [0.5, 0.5]
- commit candidate A or B when posterior is >= 0.90
- accept at most 5 evidence updates per episode
- after the fifth non-committing update, return UNCOMMITTED / DEFER
- do not force-select a posterior argmax
- preserve the binary protocol; multi-goal interaction is a sequence of separate binary episodes
- validate evidence is finite, non-negative, and exactly binary
- preserve the separation of intent inference from planner and safety concerns
```

Required verification:

```text
pytest tests/test_bayes.py tests/test_calibration.py tests/test_eegnet.py tests/test_csp_lda.py tests/test_splits.py tests/test_epochs.py tests/test_preprocessing.py tests/test_loader.py
```

A bounded synthetic calibrated-probability to Bayesian-episode smoke check is allowed as integration evidence only.

---

# 2. EXPLICITLY OUT OF SCOPE

Do not implement or modify:

```text
DECISIONS.md
MASTER_PROJECT_SPEC.md
PROJECT_STATE.md
TODO.md
EXPERIMENT_LOG.md
entropy thresholds
shared-autonomy policy
adaptation
planner
safety controller
SAR environment
replay
Streamlit/UI
reportable experiments
U-023 or later decisions
```

Do not merge this task branch. Stop after tests, bounded synthetic smoke verification, commit, push, and report for scientific review.
