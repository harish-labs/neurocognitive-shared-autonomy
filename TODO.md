# TODO.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Controlled Project Backlog

**Purpose:** Track future work without confusing backlog items with approved active scope  
**Current stage:** EEG decoding, calibration, binary Bayesian goal inference, and uncertainty/shared-autonomy policy through M1-T09 accepted and merged; no active task authorized  
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
[x] Record D-031 through D-039 preprocessing/epoch decisions
[x] Record D-040 through D-042 split/evaluation decisions
[x] Complete, accept, and merge M1-T04 split manifest
[x] Record D-043 and D-044 CSP decisions
[x] Complete, accept, and merge M1-T05 CSP+LDA baseline
[x] Record D-045 through D-047 EEGNet decisions
[x] Complete, accept, and merge M1-T06 EEGNet / Compact CNN
[x] Record D-048 through D-050 calibration decisions
[x] Complete, accept, and merge M1-T07 Probability Calibration
[x] Record D-051 through D-054 Bayesian / goal-mapping decisions
[x] Complete, accept, and merge M1-T08 Bayesian Goal Inference
[x] Record D-055 through D-057 uncertainty/shared-autonomy decisions
[x] Complete, accept, and merge M1-T09 Uncertainty & Shared-Autonomy Policy
[x] Reconcile M1-T09 governance close with no active task
```

## Current authorization

```text
[ ] Wait for next explicitly approved CURRENT_TASK.md
[ ] Do not begin another implementation module without a narrow approved ticket
[ ] Do not treat synthetic or bounded smoke results as reportable efficacy evidence
```

---

# 3. COMPLETED EEG / CALIBRATION / BAYES / SHARED-AUTONOMY IMPLEMENTATION

```text
[x] PhysioNet EEGBCI loader
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
[x] EEGNet / Compact CNN baseline
[x] validation-only checkpoint selection
[x] protected test/final-test isolation
[x] model-specific probability calibration
[x] EEGNet temperature scaling
[x] CSP+LDA Platt scaling
[x] identity / no-calibration baseline
[x] fixed 10-bin reliability/ECE utilities
[x] Brier Score utility
[x] fixed class order ("left", "right") through decoder/calibration paths
[x] binary calibrated evidence -> candidate A/B adapter
[x] fixed Bayesian prior [0.5, 0.5]
[x] sequential Bayesian posterior update
[x] >=0.90 commitment threshold
[x] maximum 5 accepted evidence updates
[x] DEFER without forced argmax after non-committing update 5
[x] explicit Bayesian episode reset and terminal-state handling
[x] binary Shannon entropy in bits
[x] posterior/entropy consistency validation
[x] pre-horizon WAITING policy
[x] D-055/D-056 PROCEED / CONFIRM / DEFER thresholds
[x] explicit human-confirmation requirement
[x] DEFER hold-position / human-input request representation
[x] PAUSE / STOP / OVERRIDE policy precedence hooks
[x] M1-T09 analytical tests
[x] M1-T09 regression bundle reported: 100 passed, 1 warning
[x] M1-T09 bounded synthetic Bayesian -> entropy -> shared-autonomy smoke
```

Synthetic smoke evidence is integration-only and supports no efficacy claim.

---

# 4. NEXT — NOT AUTHORIZED YET

Potential next work must be scientifically narrowed and explicitly approved before implementation.

```text
[ ] Decide the next single implementation task
[ ] Resolve U-026 through U-028 before implementing adaptation/personalization behavior
[ ] Do not implement reset/resume/corrected-goal behavior after override unless separately authorized by an approved task/decision where required
[ ] Run reportable decoder/calibration/Bayesian/shared-autonomy evaluation only under approved experiment tasks/protocols
```

Do not infer authorization from this list.

---

# 5. BLOCKED — SCIENTIFIC DECISIONS

## Bayesian / goal mapping

```text
[x] U-019 — Binary EEG -> multi-goal interaction protocol resolved by D-051
[x] U-020 — Decoder posterior -> goal-likelihood construction resolved by D-052
[x] U-021 — Prior policy resolved by D-053
[x] U-022 — Bayesian stopping / commitment rule resolved by D-054
```

## Shared autonomy / uncertainty policy

```text
[x] U-023 — Confidence / entropy thresholds resolved by D-055
[x] U-024 — Exact PROCEED / CONFIRM / DEFER policy resolved by D-056
[x] U-025 — Prolonged-uncertainty fallback resolved by D-057
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

---

# 6. VALIDATION TODO

```text
[x] Verify loader metadata / annotations on real subject 1 runs 4/8/12
[x] Verify montage
[x] Verify preprocessing/epoch contract
[x] Verify split leakage assertions
[x] Verify CSP train-only fitting
[x] Verify CSP component selection uses validation balanced accuracy only
[x] Verify EEGNet full canonical epoch and validation-only selection
[x] Verify protected test/final-test isolation for decoder/calibration paths
[x] Verify class order ("left", "right")
[x] Verify EEGNet temperature scaling is validation-only
[x] Verify CSP+LDA Platt scaling is validation-only
[x] Verify 10 equal-width ECE bins and Brier Score
[x] Verify binary goal evidence mapping left->A / right->B
[x] Verify exact Bayesian update math and normalization
[x] Verify >=0.90 commitment boundary
[x] Verify five-update DEFER behavior and no forced argmax
[x] Verify new-episode reset and terminal episode behavior
[x] Verify planner/safety data cannot enter Bayesian likelihood API
[x] Verify binary Shannon entropy analytical values
[x] Verify entropy cannot independently override posterior policy
[x] Verify PROCEED / WAITING / CONFIRM / DEFER boundaries
[x] Verify PAUSE / STOP / OVERRIDE precedence hooks
[x] Verify shared-autonomy policy has no planner/safety/environment-execution dependency
[ ] Run reportable within-subject decoder evaluation
[ ] Run reportable cross-subject decoder evaluation
[ ] Run reportable calibration evaluation
[ ] Run reportable Bayesian inference evaluation
[ ] Run reportable shared-autonomy evaluation
[ ] Conduct failure analysis after reportable evaluation
```

---

# 7. MILESTONE — UNCERTAINTY / SHARED AUTONOMY

Core non-executing M1-T09 policy layer is accepted.

```text
[x] Shannon entropy of Bayesian goal posterior
[x] Analytical entropy tests
[x] confidence / uncertainty policy
[x] PROCEED / WAITING / CONFIRM / DEFER behavior
[x] prolonged-uncertainty fallback representation
[x] PAUSE / STOP / OVERRIDE precedence hooks
[ ] corrected-goal / reset / resume state-transition behavior if later approved
[ ] full shared-autonomy execution state machine with planner/safety integration
[ ] end-to-end policy logging in replay
```

D-055 through D-057 are operationalized by M1-T09. This does not authorize later execution-layer work.

---

# 8. MILESTONE — ADAPTATION

Blocked by U-026 through U-028.

```text
[ ] adaptation mechanism
[ ] update formula
[ ] bounds / warm-up / reset
[ ] adaptation tests
[ ] adaptation experiment if later authorized
```

---

# 9. MILESTONE — SAR / A* / SAFETY

```text
[ ] 2D Gymnasium environment
[ ] Map configuration
[ ] UP / DOWN / LEFT / RIGHT / WAIT
[ ] A* with Manhattan heuristic
[ ] Blocked cells
[ ] Basic hard safety
[ ] Pause / stop blocking
[ ] Replanning
[ ] No-path handling
[ ] Safety logs
```

Risk-aware planning and prohibited-hazard behavior remain blocked where U-029 through U-033 apply.

---

# 10. MILESTONE — END-TO-END OFFLINE EEG REPLAY

```text
[ ] Offline EEG replay
[ ] Decoder integration
[ ] Calibration integration
[ ] Goal-evidence adapter integration
[ ] Bayes integration
[x] Entropy/shared-autonomy core policy modules available
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
[ ] E7 ablations / robustness
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
[ ] Hierarchical multi-goal selection beyond approved sequential binary-choice protocol
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
[x] D-043 and D-044 CSP decisions recorded
[x] M1-T05 CSP+LDA accepted and merged
[x] D-045 through D-047 EEGNet decisions recorded
[x] M1-T06 EEGNet / Compact CNN accepted and merged
[x] D-048 through D-050 calibration decisions recorded
[x] M1-T07 Probability Calibration accepted and merged
[x] D-051 through D-054 Bayesian / goal-mapping decisions recorded
[x] M1-T08 Bayesian Goal Inference accepted and merged
[x] D-055 through D-057 shared-autonomy / uncertainty decisions recorded
[x] M1-T09 Uncertainty & Shared-Autonomy Policy accepted and merged
[x] M1-T09 governance close recorded with no active implementation task
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
