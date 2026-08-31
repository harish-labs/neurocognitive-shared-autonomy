# TODO.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Controlled Project Backlog

**Purpose:** Track future work without confusing backlog items with approved active scope  
**Current stage:** M1 loader, visualization, preprocessing/epochs, split manifest, and CSP+LDA baseline completed; no active task authorized  
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

## Repository / Live State

```text
[x] Create / initialize project repository
[x] Add MASTER_PROJECT_SPEC.md
[x] Add AGENTS.md
[x] Add PROJECT_STATE.md
[x] Add CURRENT_TASK.md
[x] Add DECISIONS.md
[x] Add RESEARCH_LOG.md
[x] Add EXPERIMENT_LOG.md
[x] Add TODO.md
[x] Establish Git history
[x] Record approved M1-T03 preprocessing decisions U-001 through U-009
[x] Reconcile docs/06, docs/08, and docs/15 to D-031 through D-039
[x] Record D-040 through D-042 and reconcile split/evaluation methodology
[x] Complete, accept, and squash-merge M1-T04 through PR #13
[x] Reconcile M1-T04 governance close with no active task
[x] Record D-043 and D-044 for final CSP configuration and selection rule
[x] Complete, accept, and squash-merge M1-T05
[x] Reconcile M1-T05 governance close with no active task
```

## Current authorization

```text
[ ] Wait for next approved CURRENT_TASK.md
[ ] Do not begin CSP/LDA or any later module without an active implementation ticket
[x] Resolve U-013 and record the approved CSP rule set
```

---

# 3. NEXT

Completed:

```text
[x] Implement PhysioNet EEGBCI loader
[x] Support configurable subject IDs
[x] Support runs 4 / 8 / 12
[x] Use MNE download/cache utilities
[x] Load EDF
[x] Standardize channel names
[x] Attach appropriate montage
[x] Print metadata / annotations
[x] Add validation/error handling
[x] Add tests where practical
[x] Run tests
[x] Manually verify real EEG metadata
[x] Commit accepted loader
[x] EEG visualization / inspection
[x] Verify annotations visually
[x] Verify montage
[x] Inspect raw EEG
[x] Inspect PSD / basic signal properties
[x] Inspect sensor layout
[x] Inspect annotation overview
[x] Approve M1 preprocessing parameters
```

Accepted M1 implementation now includes preprocessing, epochs, provenance, and leakage-safe split manifests. Remaining work requires separate explicit authorization:

```text
[x] Implement preprocessing
[x] Implement event extraction
[x] Implement epoching
[x] Preserve provenance
[x] Implement leakage-safe split
[x] Resolve U-013 — Final CSP configuration
[x] Implement CSP+LDA
[ ] Evaluate classical baseline
```

---

# 4. BLOCKED — SCIENTIFIC DECISIONS

## EEG — resolved for initial M1 preprocessing

```text
[x] Decide exact filter band — 7–30 Hz
[x] Decide EEG reference — average EEG reference
[x] Decide epoch interval — -1.0 to +4.0 s; CSP crop +1.0 to +2.0 s
[x] Decide baseline correction — baseline=None
[x] Decide artifact handling — no ICA/interpolation; reject >150 µV peak-to-peak and log
[x] Decide T0 handling — exclude from binary training; preserve annotations/provenance
[x] Decide channel reduction, if any — retain all 64; no reduction
[x] Decide resampling, if any — none; retain 160 Hz
[x] Decide processed-data format — MNE Epochs; persisted `*-epo.fif`
```

These choices are recorded as D-031 through D-039 in `DECISIONS.md`.

## Evaluation

```text
[x] Freeze train/validation/test protocol — D-040
[x] Freeze cross-subject protocol — D-041
[x] Freeze held-out-subject strategy — D-042
[x] Implement deterministic split manifests and leakage assertions — M1-T04
```

## Calibration

```text
[ ] Select calibration method
[ ] Select calibration fitting partition
[ ] Freeze reliability-diagram binning
```

## Bayesian / Goal Mapping

```text
[ ] Decide binary EEG → multi-goal interaction
[ ] Define decoder posterior → goal likelihood semantics
[ ] Decide prior policy
[ ] Decide Bayesian stopping / commitment rule
```

## Shared Autonomy

```text
[ ] Decide confidence / entropy thresholds
[ ] Freeze proceed / confirm / defer behavior
[ ] Decide prolonged-uncertainty fallback
```

## Adaptation

```text
[ ] Select exact adaptation mechanism
[ ] Define update rule
[ ] Define bounds
[ ] Define warm-up / reset behavior
```

## Planning / Safety

```text
[ ] Define environmental risk values
[ ] Define risk normalization
[ ] Select risk λ
[ ] Define prohibited-hazard threshold
[ ] Define no-safe-path behavior
```

## Experiments

```text
[ ] Freeze exact A/B/C/D component matrix
[ ] Freeze robustness perturbation levels
[ ] Freeze statistical-analysis plan
```

---

# 5. MILESTONE M0 — INFRASTRUCTURE

```text
[ ] Repository structure
[ ] requirements.txt / environment specification
[ ] config.yaml
[ ] src/config.py validation
[ ] shared schemas
[ ] logging conventions
[ ] experiment IDs
[ ] artifact naming
[ ] test scaffold
[ ] seed / reproducibility utilities
[ ] Git workflow
```

---

# 6. MILESTONE M1 — EEG + CSP/LDA

```text
[x] Loader
[x] Visualization
[x] Preprocessing parameters approved
[x] Preprocessing
[x] Event extraction
[x] Epoching
[x] Data provenance
[x] Split manifest
[x] Leakage assertions
[x] CSP
[x] LDA
[x] Prediction probability interface
[ ] Baseline metrics
[x] Manual scientific review — completed for M1-T01 through M1-T05
```

---

# 7. MILESTONE M2 — EEGNET

```text
[ ] Finalize architecture
[ ] Dataset wrapper
[ ] Training pipeline
[ ] Validation
[ ] Checkpointing
[ ] Probability output
[ ] Subject-wise metrics
[ ] Compare with CSP+LDA
[ ] Failure analysis
```

---

# 8. MILESTONE M3 — CALIBRATION / BAYES / UNCERTAINTY

```text
[ ] Calibration metrics
[ ] Reliability diagrams
[ ] Calibrator
[ ] Generic Bayesian core
[ ] Analytical Bayes tests
[ ] Entropy
[ ] Analytical entropy tests
[ ] GoalEvidence interface
[ ] Adaptation interface
[ ] Synthetic cognitive integration tests
```

Blocked until approved where applicable:

```text
[ ] Real decoder → goal evidence mapping
[ ] Final calibrator choice
[ ] Final commitment rule
[ ] Final adaptation update
```

---

# 9. MILESTONE M4 — SAR / A* / SAFETY

```text
[ ] 2D Gymnasium environment
[ ] Map configuration
[ ] UP/DOWN/LEFT/RIGHT/WAIT
[ ] A*
[ ] Manhattan heuristic
[ ] Blocked cells
[ ] Basic hard safety
[ ] Pause / stop blocking
[ ] Replanning
[ ] No-path handling
[ ] Safety logs
```

Blocked pending risk decisions:

```text
[ ] Risk-aware path cost
[ ] Prohibited hazards
```

---

# 10. MILESTONE M5 — SHARED AUTONOMY

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

Blocked pending policy decisions:

```text
[ ] Final confidence thresholds
[ ] Final proceed / confirm / defer rules
```

---

# 11. MILESTONE M6 — END-TO-END EEG REPLAY

```text
[ ] Offline EEG replay
[ ] Decoder integration
[ ] Calibration integration
[ ] Goal-evidence adapter
[ ] Bayes integration
[ ] Entropy integration
[ ] Shared autonomy integration
[ ] Planner integration
[ ] Safety integration
[ ] Full mission replay
[ ] End-to-end logs
[ ] Manual review
```

---

# 12. MILESTONE M7 — EXPERIMENTS

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

---

# 13. MILESTONE M8 — PRESENTATION

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
[ ] Portfolio update
[ ] Resume bullets update
[ ] Demo video
```

---

# 14. VALIDATION TODO

```text
[ ] Verify T1/T2 semantics from real loaded data
[ ] Verify channel names
[ ] Verify montage
[x] Verify implemented split manifests for subject/original-trial/derived-window leakage
[x] Verify CSP train-only fitting
[ ] Verify calibrator does not see test labels
[x] Verify decoder class order
[ ] Verify Bayesian hypothesis order
[ ] Verify entropy analytically
[ ] Verify A* optimality on controlled maps
[ ] Verify safety blocks invalid actions
[ ] Verify human stop dominates
[ ] Verify uncertainty changes behavior
[ ] Verify replay is labeled offline/simulated
```

---

# 15. DOCUMENTATION TODO

Core numbered documentation is complete through:

```text
25_FUTURE_WORK.md
```

Generated portfolio/report artifacts:

```text
FINAL_TECHNICAL_REPORT.md
GITHUB_README.md
PORTFOLIO_AND_RESUME_POSITIONING.md
```

Remaining documentation work is primarily **updating these artifacts with real implementation/results**, not generating new theory documents.

Later:

```text
[ ] Update FINAL_TECHNICAL_REPORT.md with real results
[ ] Update GITHUB_README.md with tested commands
[ ] Update PORTFOLIO_AND_RESUME_POSITIONING.md with validated metrics
[ ] Final consistency scan across all docs
[ ] Remove/archive any superseded implementation-agent instruction file
```

---

# 16. OPTIONAL — ONLY AFTER CORE

```text
[ ] Live EEG
[ ] Human-subject study
[ ] Hierarchical multi-goal selection
[ ] Multiclass EEG
[ ] Stronger domain adaptation
[ ] Advanced uncertainty
[ ] Dynamic Bayesian model
[ ] ROS2
[ ] Gazebo
[ ] Formal safety
[ ] Physical robot
[ ] RL comparison
[ ] SNN / neuromorphic comparison
```

These are not current requirements.

---

# 17. FUTURE RESEARCH

Potential research directions:

```text
[ ] Cross-subject generalization
[ ] Few-shot personalization
[ ] Distribution-shift calibration
[ ] OOD detection
[ ] Dynamic SAR
[ ] Human trust / workload study
[ ] Error-related potentials
[ ] Multimodal BCI
[ ] Intent-change detection
[ ] Formal runtime assurance
```

---

# 18. DONE — DOCUMENTATION / GOVERNANCE

```text
[x] Master Project Specification
[x] Project Concept & Problem Definition
[x] Objectives, Scope & Research Questions
[x] Search & Rescue Scenario
[x] System Architecture
[x] Technology Stack
[x] Dataset & Data Pipeline
[x] Neuroscience & BCI Foundations
[x] EEG Signal Processing & Machine Learning
[x] Probability Calibration & Uncertainty
[x] Bayesian Goal Inference
[x] Cognitive & Adaptive Model
[x] Shared Autonomy & Human-AI Interaction
[x] Autonomous Planning & Control
[x] Safety-Critical Control
[x] Implementation Blueprint
[x] Repository & Code Architecture
[x] Experimental Design
[x] Metrics & Evaluation
[x] Testing & Verification
[x] Limitations, Ethics & Scientific Validity
[x] Literature & Scientific Foundation
[x] AI-Assisted Development Workflow — Codex aligned
[x] AGENTS.md — Codex Instructions
[x] PROJECT_STATE.md
[x] Results & Analysis framework
[x] Discussion & Findings framework
[x] Future Work
[x] Final Technical Report framework
[x] GitHub README framework
[x] Resume & Portfolio Positioning
[x] CURRENT_TASK.md template / first task
[x] DECISIONS.md
[x] RESEARCH_LOG.md
[x] EXPERIMENT_LOG.md
[x] TODO.md
[x] M1-T03 preprocessing decisions D-031 through D-039 recorded
[x] Split decisions D-040 through D-042 recorded and methodology reconciled
[x] M1-T04 split manifest accepted and squash-merged through PR #13
[x] M1-T04 governance close recorded with no active implementation task
[x] D-043 and D-044 recorded for the approved CSP configuration and selection rule
[x] M1-T05 CSP+LDA baseline accepted and squash-merged
[x] M1-T05 governance close recorded with no active implementation task
```

---

# 19. TODO DISCIPLINE

When an item becomes active:

```text
TODO.md
→ CURRENT_TASK.md
```

When it becomes an approved scientific choice:

```text
RESEARCH_LOG.md
→ DECISIONS.md
```

When implementation is accepted:

```text
PROJECT_STATE.md
```

When an experiment runs:

```text
EXPERIMENT_LOG.md
```

This separation must remain intact.
