# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Current status:** ACTIVE IMPLEMENTATION TASK
**Current milestone:** M6 Bayesian Episode Integration
**Task ID:** M6-T03
**Task title:** Calibrated EEG Evidence -> Bayesian Decision Episode
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical branch:** `task/m6-t03-bayesian-episode-integration`
**Authorization base:** `a7224a55ab5f71d0bef7e22e6919ce5912140d85`

---

# 1. ACTIVE TASK - M6-T03

```text
Task ID: M6-T03
Task title: Calibrated EEG Evidence -> Bayesian Decision Episode
Status: AUTHORIZED / IMPLEMENTATION NOT STARTED
Governing decisions: D-074, D-075, D-076 and existing accepted Bayesian decisions
```

## Authorized input boundary

```text
ordered DecodedReplayObservation sequence
explicit candidate_a
explicit candidate_b
```

## Authorized integration

```text
DecodedReplayObservation
-> validated calibrated probability row
-> binary_goal_evidence_from_calibrated_probabilities(...)
-> BinaryGoalEvidence
-> BinaryBayesianGoalEpisode.accept_evidence(...)
-> BayesianEpisodeResult
```

Use the existing accepted Bayesian implementation in `src/cognitive/bayes.py`. Do not independently reimplement Bayesian mathematics.

## Approved episode semantics

```text
class order = ("left", "right")
left -> candidate A
right -> candidate B
initial prior = (0.5, 0.5)
commitment threshold = 0.90
maximum evidence updates = 5
unresolved after update 5 = DEFER
no forced argmax
stop immediately on COMMITTED
```

Consume observations in strictly increasing `replay_index` order; reject duplicate replay indices and duplicate canonical trial identities; consume at most five accepted observations; do not automatically start another episode; preserve deterministic provenance.

## Explicitly out of scope

```text
decoder execution, calibration execution, candidate selection, arbitrary K-goal inference, entropy/shared-autonomy integration, CONFIRM policy, human authorization, STOP/PAUSE/OVERRIDE behavior, mission-goal authorization, navigation, planning, safety/environment execution, adaptation, experiments, UI, and src/cognitive/uncertainty.py integration.
```

Preserve offline prerecorded EEG / simulated real-time BCI only, no live EEG, unresolved U-034/U-035/U-036, and no new dependency. Do not start M6-T04.

## Required verification

Focused M6-T03 tests, relevant Bayesian regressions, M6-T02/runtime-adapter regression tests, full pytest, deterministic ordering/provenance checks, fail-closed validation checks, and `git diff --check`.

Stop if implementation requires a new scientific, dataset-semantic, Bayesian, dependency, replay, calibration, or downstream M6-T04 decision.