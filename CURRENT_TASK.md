# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Current status:** ACTIVE
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / Decoders / Calibration / Bayesian Goal Inference / Shared-Autonomy Policy / Prior Personalization
**Task ID:** M1-T10
**Task title:** Adaptation / Prior Personalization
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Repository instructions:** `AGENTS.md`
**Canonical branch:** `main` at `eae232531bf0daa4d80653caa6ae1237a70b782d`
**Task branch:** `task/m1-t10-prior-personalization`
**Last updated:** 2026-08-31

---

# 1. AUTHORIZED SCOPE

Implement only M1-T10 under D-058 through D-060.

Allowed files:

```text
src/cognitive/adaptation.py
tests/test_adaptation.py
CURRENT_TASK.md
__init__.py only if necessary
```

Required behavior:

```text
- subject-specific, candidate-pair-specific initial-prior personalization only
- state is keyed by anonymous subject ID and an order-independent stable candidate pair
- update only from explicit accepted CONFIRM or explicitly corrected OVERRIDE feedback
- initial pseudo-counts are 1/1; warm-up requires 3 valid feedback events
- bound active personalized priors to [0.25, 0.75]
- adaptation OFF, warm-up, and reset return [0.5, 0.5]
- updates occur only between episodes and retain trace records
- no active Bayesian episode, evidence likelihood, decoder, calibration, threshold, planner, safety, or environment state is modified
```

Required verification:

```text
pytest tests/test_adaptation.py tests/test_shared_autonomy.py tests/test_uncertainty.py tests/test_bayes.py tests/test_calibration.py tests/test_eegnet.py tests/test_csp_lda.py tests/test_splits.py tests/test_epochs.py tests/test_preprocessing.py tests/test_loader.py
```

Do not merge this branch. Stop after testing, bounded synthetic smoke verification, commit, push, and report for scientific review.
