# TODO.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Controlled Project Backlog

**Purpose:** Track future work without confusing backlog items with approved active scope  
**Current stage:** EEG decoding and probability calibration through M1-T07 accepted and merged; no active task authorized  
**Active task authority:** `CURRENT_TASK.md`  
**Current project truth:** `PROJECT_STATE.md`

---

# 1. TODO RULES

A TODO entry is not automatically authorized.

Use categories:

```text
NOW
NEXT
BLOCKED
VALIDATION
DOCUMENTATION
OPTIONAL
FUTURE
DONE
```

Only `CURRENT_TASK.md` authorizes active Codex implementation.

---

# 2. NOW

## Repository / live state

```text
[x] Create / initialize project repository
[x] Add core governance files
[x] Record M1-T03 preprocessing decisions D-031 through D-039
[x] Record split/evaluation decisions D-040 through D-042
[x] Complete, accept, and merge M1-T04 split manifest
[x] Record D-043 and D-044 for final CSP configuration/selection
[x] Complete, accept, and merge M1-T05 CSP+LDA baseline
[x] Record D-045 and D-046 for final EEGNet architecture/training
[x] Record D-047 pooling/max-norm supplement
[x] Complete, review, accept, and merge M1-T06 EEGNet / Compact CNN
[x] Record D-048 through D-050 for final calibration methodology
[x] Complete, review, accept, and merge M1-T07 Probability Calibration
[x] Reconcile M1-T07 governance close with no active task
```

## Current authorization

```text
[ ] Wait for next explicitly approved CURRENT_TASK.md
[ ] Do not begin another implementation module without a narrow approved ticket
[ ] Do not treat smoke-test calibration metrics as reportable calibration-quality evidence
```

---

# 3. COMPLETED EEG / CALIBRATION IMPLEMENTATION

```text
[x] PhysioNet EEGBCI loader
[x] Subject/run configuration for runs 4 / 8 / 12
[x] EDF loading and channel standardization
[x] standard_1005 montage
[x] EEG visualization / inspection
[x] 7–30 Hz preprocessing
[x] average EEG reference
[x] canonical -1.0 s to +4.0 s epochs
[x] T0 exclusion from binary training data with provenance preserved
[x] 150 µV peak-to-peak rejection policy
[x] all 64 channels / native 160 Hz
[x] MNE Epochs + *-epo.fif contract
[x] leakage-safe within-subject split
[x] protected cross-subject split manifest contract
[x] CSP+LDA baseline
[x] validation-balanced-accuracy CSP component selection
[x] CSP probability output
[x] EEGNet architecture/training baseline
[x] validation-only EEGNet checkpoint selection
[x] protected test/final-test isolation
[x] EEGNet softmax probability output
[x] M1-T06 BatchNorm shape-inference reviewer fix
[x] model-specific calibration methods
[x] validation-only calibration fitting
[x] identity / no-calibration baseline
[x] fixed 10-bin equal-width reliability/ECE utilities
[x] Brier Score utility
[x] class order ("left", "right") preserved through calibration
[x] M1-T07 final targeted regression bundle: 59 passed, 1 warning
[x] subject-1 M1-T07 bounded real-data smoke execution
```

Subject-1 calibration smoke evidence is integration-only and supports no efficacy or generalizable calibration-quality claim.

---

# 4. NEXT — NOT AUTHORIZED YET

Potential next work must be narrowed and explicitly approved before implementation.

```text
[ ] Decide the next single implementation task
[ ] Resolve Bayesian / goal-mapping decisions U-019 through U-022 before implementing that layer
[ ] Consider unified decoder interface only if required by the next approved module
[ ] Run reportable classical-vs-EEGNet evaluation only under an approved experiment task/protocol
[ ] Run reportable calibration evaluation only under an approved experiment task/protocol
```

Do not infer authorization from this list.

---

# 5. BLOCKED — SCIENTIFIC DECISIONS

## Bayesian / goal mapping

```text
[ ] U-019 — Decide binary EEG -> multi-goal interaction protocol
[ ] U-020 — Define decoder posterior -> goal-likelihood semantics
[ ] U-021 — Decide prior policy
[ ] U-022 — Decide Bayesian stopping / commitment rule
```

## Shared autonomy

```text
[ ] U-023 — Decide confidence / entropy thresholds
[ ] U-024 — Freeze exact PROCEED / CONFIRM / DEFER policy
[ ] U-025 — Decide prolonged-uncertainty fallback
```

## Adaptation

```text
[ ] U-026 — Select exact adaptation mechanism
[ ] U-027 — Define update formula
[ ] U-028 — Define bounds / warm-up / reset
```

## Planning / safety

```text
[ ] U-029 — Define environmental risk values
[ ] U-030 — Define risk normalization
[ ] U-031 — Select risk weight lambda
[ ] U-032 — Define prohibited-hazard threshold
[ ] U-033 — Define final no-safe-path behavior
```

## Experiments

```text
[ ] U-034 — Freeze exact A/B/C/D component matrix
[ ] U-035 — Freeze robustness perturbation levels
[ ] U-036 — Freeze inferential-statistics policy
[ ] If eligible cross-subject cohort != 109, obtain reviewer decision before freezing a different final manifest
```

Calibration U-016 through U-018 are resolved and implemented.

---

# 6. EEG / MODEL / CALIBRATION VALIDATION TODO

```text
[x] Verify loader metadata / annotations on real subject 1 runs 4/8/12
[x] Verify montage
[x] Verify preprocessing/epoch contract
[x] Verify split leakage assertions
[x] Verify CSP train-only fitting
[x] Verify CSP component selection uses validation balanced accuracy only
[x] Verify EEGNet full canonical epoch and no CSP-only crop
[x] Verify EEGNet train-only gradient updates
[x] Verify EEGNet validation-only checkpoint selection
[x] Verify protected test/final-test does not affect EEGNet selection
[x] Verify decoder class order ("left", "right")
[x] Verify BatchNorm state is not contaminated by shape inference
[x] Verify EEGNet temperature scaling is validation-only
[x] Verify CSP+LDA Platt scaling is validation-only
[x] Verify protected test/final-test does not influence calibrator fitting
[x] Verify identity calibration baseline
[x] Verify 10 equal-width ECE bins over [0,1]
[x] Verify Brier Score
[ ] Run reportable within-subject decoder evaluation
[ ] Run reportable cross-subject decoder evaluation
[ ] Compare CSP+LDA and EEGNet under the approved E1 protocol
[ ] Run reportable calibration evaluation
[ ] Conduct failure analysis after reportable evaluation
```

---

# 7. MILESTONE — BAYES / UNCERTAINTY

Not authorized until its required decisions and task are approved.

```text
[ ] Goal-evidence adapter
[ ] Generic Bayesian core
[ ] Analytical Bayes tests
[ ] Entropy
[ ] Analytical entropy tests
[ ] Synthetic cognitive integration tests
```

Blocked where applicable:

```text
[ ] Real decoder -> goal evidence mapping
[ ] Final commitment rule
[ ] Final adaptation update
```

---

# 8. MILESTONE — SAR / A* / SAFETY

```text
[ ] 2D Gymnasium environment
[ ] Map configuration
[ ] UP / DOWN / LEFT / RIGHT / WAIT
[ ] A*
[ ] Manhattan heuristic
[ ] Blocked cells
[ ] Basic hard safety
[ ] Pause / stop blocking
[ ] Replanning
[ ] No-path handling
[ ] Safety logs
```

Blocked pending approved risk policy:

```text
[ ] Risk-aware path cost
[ ] Prohibited hazards
```

---

# 9. MILESTONE — SHARED AUTONOMY

```text
[ ] Candidate goal representation
[ ] Approved goal representation
[ ] Human confirm
[ ] Human override
[ ] Pause
[ ] Stop
[ ] Shared-autonomy state machine
[ ] Policy logging
[ ] State-transition tests
```

Blocked pending U-023 through U-025.

---

# 10. MILESTONE — END-TO-END OFFLINE EEG REPLAY

```text
[ ] Offline EEG replay
[ ] Decoder integration
[ ] Calibration integration
[ ] Goal-evidence adapter
[ ] Bayes integration
[ ] Entropy integration
[ ] Shared-autonomy integration
[ ] Planner integration
[ ] Safety integration
[ ] Full mission replay
[ ] End-to-end logs
[ ] Manual review
```

This must remain labeled offline EEG replay / simulated real-time BCI unless hardware is explicitly approved later.

---

# 11. MILESTONE — EXPERIMENTS

```text
[ ] E1 EEG decoding
[ ] E2 calibration
[ ] E3 Bayesian inference
[ ] E4 uncertainty/shared autonomy
[ ] E5 planning/safety
[ ] E6 A/B/C/D comparison
[ ] E7 ablations
[ ] E7 robustness
[ ] E8 cross-subject
[ ] E9 adaptation if implemented
[ ] Statistical analysis
[ ] Failure taxonomy
[ ] Result traceability
```

Negative or mixed results are valid. Do not tune protected test data to improve outcomes.

---

# 12. PRESENTATION / DOCUMENTATION

```text
[ ] Streamlit dashboard
[ ] Technical architecture figure
[ ] EEG figure
[ ] Calibration figure
[ ] Posterior / entropy figure
[ ] SAR route figure
[ ] A/B/C/D table
[ ] Failure-case visualization
[ ] Final README update
[ ] Final technical report update
[ ] Portfolio / resume updates only with validated claims
[ ] Demo video
```

---

# 13. OPTIONAL / FUTURE — ONLY AFTER CORE

```text
[ ] Live EEG
[ ] Human-subject study
[ ] Hierarchical multi-goal selection
[ ] Multiclass EEG
[ ] Stronger domain adaptation
[ ] Advanced uncertainty / OOD detection
[ ] Dynamic Bayesian model
[ ] ROS2 / Gazebo
[ ] Formal safety
[ ] Physical robot
[ ] RL comparison
[ ] SNN / neuromorphic comparison
```

These are not current requirements or authorization.

---

# 14. DONE — GOVERNANCE / IMPLEMENTATION CLOSES

```text
[x] MASTER_PROJECT_SPEC.md and governance framework established
[x] D-031 through D-039 preprocessing/epoch decisions recorded
[x] D-040 through D-042 split/evaluation decisions recorded
[x] M1-T04 split manifest accepted and merged
[x] D-043 and D-044 CSP configuration/selection recorded
[x] M1-T05 CSP+LDA accepted and merged
[x] D-045 and D-046 EEGNet architecture/training recorded
[x] D-047 EEGNet pooling/max-norm supplement recorded
[x] M1-T06 EEGNet / Compact CNN accepted and merged
[x] D-048 through D-050 calibration decisions recorded
[x] M1-T07 Probability Calibration accepted and merged
[x] M1-T07 governance close recorded with no active implementation task
```

---

# 15. TODO DISCIPLINE

```text
backlog item -> TODO.md
approved scientific choice -> DECISIONS.md
active implementation -> CURRENT_TASK.md
accepted implementation -> PROJECT_STATE.md
reportable experiment -> EXPERIMENT_LOG.md
```

Do not blur these roles.
