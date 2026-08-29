# TODO.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Controlled Project Backlog

**Purpose:** Track future work without confusing backlog items with approved active scope  
**Current stage:** M1 loader and visualization completed; no active task authorized  
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
```

## Current authorization

```text
[ ] Wait for next approved CURRENT_TASK.md
[ ] Do not begin preprocessing or epoching without approval
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
```

Then, only after scientific preprocessing decisions are approved:

```text
[ ] Implement preprocessing
[ ] Implement event extraction
[ ] Implement epoching
[ ] Preserve provenance
[ ] Implement leakage-safe split
[ ] Implement CSP+LDA
[ ] Evaluate classical baseline
```

---

# 4. BLOCKED — SCIENTIFIC DECISIONS

## EEG

```text
[ ] Decide exact filter band
[ ] Decide EEG reference
[ ] Decide epoch interval
[ ] Decide baseline correction
[ ] Decide artifact handling
[ ] Decide T0 handling
[ ] Decide channel reduction, if any
[ ] Decide resampling, if any
[ ] Decide processed-data format
```

## Evaluation

```text
[ ] Freeze train/validation/test protocol
[ ] Freeze cross-subject protocol
[ ] Freeze held-out-subject strategy
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
[ ] Preprocessing
[ ] Event extraction
[ ] Epoching
[ ] Data provenance
[ ] Split manifest
[ ] Leakage assertions
[ ] CSP
[ ] LDA
[ ] Prediction probability interface
[ ] Baseline metrics
[ ] Manual scientific review
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
[ ] Verify all splits for leakage
[ ] Verify CSP train-only fitting
[ ] Verify calibrator does not see test labels
[ ] Verify decoder class order
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
