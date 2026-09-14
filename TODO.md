# TODO.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Controlled Project Backlog

**Purpose:** Track future work without confusing backlog items with approved active scope  
**Current stage:** M1–M7 complete; M7-T02 R03 remains PASS / ACCEPTED / MERGED / CLOSED. M8-T01 is ACTIVE / AUTHORIZED.
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
[x] Record D-058 through D-060 adaptation decisions
[x] Complete, accept, and merge M1-T10 Adaptation / Prior Personalization
[x] Reconcile M1-T10 governance close with no active task
```

## M7 close

```text
[x] Execute the authorized M7-T02 pre-final QC/manifest work
[x] Record D-084 Full - Bayes and Full - uncertainty execution rules
[x] Freeze artifacts/manifests and execute E1–E9 under the approved contract
[x] Complete scientific review, acceptance, fast-forward merge, and governance close
[x] Preserve v1–v4 immutable invalid audit artifacts and v5 as the accepted reportable result
[x] Preserve negative/mixed/non-significant findings and claim boundaries
```

M8-T01 is now the only active task. M8 may consume accepted results but may not rerun protected experiments or modify `results/m7/**` or accepted M1–M7 scientific/runtime code.

---

# 3. COMPLETED CORE IMPLEMENTATION

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
[x] subject/pair-specific prior personalization
[x] alpha 1/1 pseudo-count initialization
[x] 3-event warm-up
[x] bounded [0.25,0.75] personalized prior
[x] adaptation ON/OFF behavior
[x] explicit personalization reset
[x] traceable explicit-feedback update records
[x] fresh Bayesian episode custom initial-prior interface
[x] mid-sequence custom-prior injection rejection
[x] M1-T10 regression bundle reported: 124 passed, 1 warning
[x] M1-T10 corrected bounded adaptation -> Bayes smoke
```

Synthetic smoke evidence is integration-only and supports no efficacy claim.

---

# 4. HISTORICAL NEXT ITEMS — IMPLEMENTED / NOT ACTIVE AUTHORITY

Potential next work must be scientifically narrowed and explicitly approved before implementation.

```text
[x] Project Owner authorized consolidated M8-T01
[x] U-029 through U-033 resolved by D-061 through D-065
[x] 2D Search & Rescue environment implemented and accepted in M4
[x] A* / risk-aware planning implemented and accepted in M4
[x] Explicit safety-controller behavior implemented and accepted in M4
[x] Run reportable decoder/calibration/Bayesian/shared-autonomy/adaptation evaluation only under approved experiment tasks/protocols
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
[x] U-026 — Adaptation mechanism resolved by D-058
[x] U-027 — Update formula resolved by D-059
[x] U-028 — Bounds / warm-up / reset resolved by D-060
```

## Planning / safety

```text
[x] U-029 — Environmental risk values resolved by D-061
[x] U-030 — Risk normalization resolved by D-062
[x] U-031 — Risk weight lambda resolved by D-063
[x] U-032 — Prohibited-hazard threshold resolved by D-064
[x] U-033 — No-safe-path behavior resolved by D-065
```

## Experiments

```text
[x] U-034 — Exact A/B/C/D component matrix resolved by D-077
[x] U-035 — Robustness perturbation levels resolved by D-078
[x] U-036 — Inferential-statistics policy resolved by D-079
[x] Post-QC cohort/allocation resolved by D-082 and frozen for accepted M7 execution
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
[x] Verify adaptation feedback isolation, warm-up, bounds, reset, and traceability
[x] Verify personalized prior initializes a fresh Bayesian episode only
[x] Verify default [0.5,0.5] Bayes prior remains unchanged when no custom prior supplied
[x] Verify custom prior does not alter Bayesian evidence-update mathematics
[ ] Run reportable within-subject decoder evaluation
[x] Run reportable cross-subject decoder evaluation
[x] Run reportable calibration evaluation
[x] Run reportable Bayesian inference evaluation
[x] Run reportable shared-autonomy evaluation
[x] Run reportable adaptation evaluation
[x] Conduct failure-taxonomy audit after reportable evaluation
```

---

# 7. MILESTONE — ADAPTATION

Core M1-T10 prior-personalization implementation is accepted.

```text
[x] subject-specific candidate-pair adaptation state
[x] explicit-feedback-only updates
[x] update formula
[x] warm-up / bounds / reset
[x] adaptation ON/OFF
[x] traceable update records
[x] fresh-Bayesian-episode prior handoff
[x] analytical / integration tests
[x] Adaptation OFF/ON experiment completed in accepted M7 E9
```

D-058 through D-060 are operationalized by M1-T10. This does not establish that adaptation improves performance.

---

# 8. MILESTONE — SAR / A* / SAFETY (COMPLETED)

```text
[x] 2D Gymnasium environment
[x] Map configuration
[x] UP / DOWN / LEFT / RIGHT / WAIT
[x] A* with Manhattan heuristic
[x] Blocked cells
[x] Basic hard safety
[x] Pause / stop blocking
[x] Replanning
[x] No-path handling
[x] Safety logs
```

Risk-aware planning and prohibited-hazard behavior are governed by D-061 through D-065 and implemented only under separately authorized task scope.

---

# 9. MILESTONE — END-TO-END OFFLINE EEG REPLAY (COMPLETED)

```text
[x] Offline EEG replay
[x] Decoder integration
[x] Calibration integration
[x] Goal-evidence adapter integration
[x] Bayes integration
[x] Entropy/shared-autonomy core policy modules available
[x] Adaptation prior-personalization module available
[x] Planner integration
[x] Safety integration
[x] Full mission replay
[x] End-to-end logs
[x] Manual review
```

This must remain labeled offline EEG replay / simulated real-time BCI unless hardware is explicitly approved later.

---

# 10. MILESTONE — EXPERIMENTS

```text
[x] E1 EEG decoding
[x] E2 calibration
[x] E3 Bayesian inference
[x] E4 uncertainty/shared autonomy
[x] E5 planning/safety
[x] E6 A/B/C/D comparison
[x] E7 ablations / robustness
[x] E8 cross-subject
[x] E9 adaptation
[x] Statistical analysis
[x] Failure taxonomy categories (v5 schema does not aggregate category counts)
[x] Result traceability
```

Negative or mixed results are valid. Do not tune protected test data to improve outcomes.

---

# 11. PRESENTATION / DOCUMENTATION — M8-T01 ACTIVE

```text
[x] Streamlit dashboard candidate implemented
[x] Technical architecture figure generated under `results/m8/figures/`
[x] EEG evidence presented from accepted E1 tables
[x] Calibration figure/data presentation sourced from accepted E2 tables
[x] Posterior / entropy deterministic demo visualization (explicitly non-empirical)
[x] SAR route figure generated from deterministic production-code demo
[x] A/B/C/D table sourced from accepted E6 tables
[x] Failure/limitation visualization and narrative sourced from accepted evidence
[x] Final README candidate updated
[x] Final technical report candidate created
[x] Portfolio / resume candidate wording limited to validated claims
[x] Runnable demo, recording script, and storyboard (no fabricated video file)

Candidate implementation is complete but remains subject to ChatGPT scientific/repository review. M8 is not accepted, merged, or closed.
```

---

# 12. OPTIONAL / FUTURE — ONLY AFTER CORE

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

# 13. DONE — GOVERNANCE / IMPLEMENTATION CLOSES

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
[x] D-058 through D-060 adaptation decisions recorded
[x] M1-T10 Adaptation / Prior Personalization accepted and merged
[x] M1-T10 governance close recorded with no active implementation task
[x] M7-T01 Consolidated Experiment & Evaluation Harness accepted and merged
[x] M7-T02 Frozen Final Experiment Execution & Scientific Audit accepted, fast-forward merged, and closed
[x] M7 — Experiments / Ablations / Robustness COMPLETE / PASS / CLOSED
```

---

# 14. TODO DISCIPLINE

```text
backlog item -> TODO.md
approved scientific choice -> DECISIONS.md
active implementation -> CURRENT_TASK.md
accepted implementation -> PROJECT_STATE.md
reportable experiment -> EXPERIMENT_LOG.md
```

Do not blur these roles.
