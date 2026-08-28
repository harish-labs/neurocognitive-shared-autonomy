# DECISIONS.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Approved Decision Register

**Purpose:** Record explicit, approved scientific, architectural, implementation, and governance decisions  
**Rule:** A suggestion is not a decision until explicitly approved  
**Authority:** Subordinate to `MASTER_PROJECT_SPEC.md`; authoritative for approved decisions that do not conflict with the Master Specification

---

# 1. DECISION STATUS LABELS

Use:

```text
APPROVED
SUPERSEDED
REJECTED
UNRESOLVED
```

Only `APPROVED` decisions authorize implementation.

---

# 2. APPROVED DECISIONS

## D-001 — Project Application

**Status:** APPROVED

```text
Search & Rescue
```

Rationale:

Use Search & Rescue as the application layer for studying uncertain EEG intent, shared autonomy, planning, and safety.

---

## D-002 — Project Title

**Status:** APPROVED

**NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

## D-003 — Core Responsibility Principle

**Status:** APPROVED

> **Human determines WHAT intended objective is selected. AI determines HOW to achieve it safely.**

---

## D-004 — Project Form

**Status:** APPROVED

```text
Software-only
No required physical hardware
No required 3D simulation
```

---

## D-005 — EEG Dataset

**Status:** APPROVED

```text
PhysioNet EEG Motor Movement/Imagery Database
EEGMMIDB / EEGBCI
```

Access through MNE-Python.

---

## D-006 — Initial EEG Runs

**Status:** APPROVED

```text
4
8
12
```

These correspond to motor-imagery Left-vs-Right fist runs.

---

## D-007 — Initial EEG Task

**Status:** APPROVED

```text
Left-hand motor imagery
vs
Right-hand motor imagery
```

---

## D-008 — EEG Mode

**Status:** APPROVED

```text
Public prerecorded EEG
Offline EEG Replay
Simulated Real-Time BCI
```

No live EEG claim.

---

## D-009 — Classical Baseline

**Status:** APPROVED

```text
CSP + LDA
```

A classical baseline is mandatory.

---

## D-010 — Neural Decoder

**Status:** APPROVED

```text
EEGNet
```

or, if materially modified:

```text
Compact EEG CNN inspired by EEGNet
```

The name must match the actual implementation.

---

## D-011 — Probability Calibration

**Status:** APPROVED

Probability calibration is part of the core methodological architecture.

The exact calibration method remains unresolved.

---

## D-012 — Bayesian Inference

**Status:** APPROVED

Use sequential Bayesian goal inference with explicit:

```text
prior
likelihood
posterior
```

---

## D-013 — Bayesian Likelihood Boundary

**Status:** APPROVED

Decoder probability:

```text
P(class | EEG)
```

must not automatically be treated as:

```text
P(evidence | goal)
```

An explicit Goal-Evidence Adapter / probability model is required.

---

## D-014 — Primary Uncertainty Measure

**Status:** APPROVED

Initial system-level uncertainty measure:

```text
Shannon entropy of the Bayesian goal posterior
```

---

## D-015 — Shared Autonomy

**Status:** APPROVED

Shared-autonomy behavior is a core component.

Conceptual states:

```text
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

Exact thresholds remain unresolved.

---

## D-016 — Human Controls

**Status:** APPROVED

Required controls:

```text
CONFIRM
OVERRIDE
PAUSE
STOP
```

Human stop cannot be bypassed by model confidence.

---

## D-017 — SAR Environment

**Status:** APPROVED

```text
Simple 2D technical environment
Single agent
Static-first
```

---

## D-018 — Initial Action Space

**Status:** APPROVED

```text
UP
DOWN
LEFT
RIGHT
WAIT
```

No diagonal movement in the core.

---

## D-019 — Core Planner

**Status:** APPROVED

```text
A*
```

Initial heuristic for the four-connected grid:

```text
Manhattan distance
```

---

## D-020 — Planning / Intent Separation

**Status:** APPROVED

The planner receives an already approved goal.

The planner does not infer human intent.

---

## D-021 — Safety Architecture

**Status:** APPROVED

```text
planner proposes
→ safety controller checks
→ environment executes only if approved
```

Hard safety constraints remain separate from soft risk cost.

---

## D-022 — UI

**Status:** APPROVED

```text
Streamlit
```

is used as a presentation/dashboard layer only.

Core scientific logic must run headlessly.

---

## D-023 — Core Development Stack

**Status:** APPROVED

```text
Python
MNE-Python
NumPy
Pandas
scikit-learn
PyTorch
Gymnasium
Matplotlib
Streamlit
YAML
Git / GitHub
```

---

## D-024 — Development Workflow

**Status:** APPROVED

```text
ChatGPT = Project Brain / Research Director
Project Owner = final authority
Codex = implementation engineer
Git/GitHub = persistent technical source of truth
```

---

## D-025 — Codex Repository Instruction File

**Status:** APPROVED

```text
AGENTS.md
```

Any superseded implementation-agent instruction file is obsolete.

---

## D-026 — Core Development Loop

**Status:** APPROVED

```text
DESIGN
→ APPROVE
→ IMPLEMENT
→ RUN
→ VERIFY
→ REVIEW
→ COMMIT
→ NEXT
```

---

## D-027 — A/B/C/D Evaluation Structure

**Status:** APPROVED CONCEPTUALLY

Principal comparison:

```text
A — Direct EEG
B — Confidence-aware
C — Bayesian shared autonomy
D — Full system
```

Exact component membership for each condition must be frozen before final experiments.

---

## D-028 — Negative Results

**Status:** APPROVED

Negative and mixed results must be preserved.

The project does not guarantee that the full system outperforms all baselines.

---

## D-029 — Claim Discipline

**Status:** APPROVED

Do not fabricate or pre-state:

```text
accuracy
F1
ECE
Brier Score
Bayesian improvement
task-success improvement
safety improvement
latency improvement
```

Only valid experiments may support these claims.

---

# 3. UNRESOLVED DECISIONS

The following remain explicitly unresolved.

## EEG / Signal Processing

```text
U-001 — Exact band-pass filter
U-002 — EEG reference
U-003 — Epoch interval
U-004 — Baseline correction
U-005 — Artifact-handling policy
U-006 — T0 handling
U-007 — Channel reduction, if any
U-008 — Resampling, if any
U-009 — Processed-data format
```

## Data Split / Validation

```text
U-010 — Final train/validation/test protocol
U-011 — Final cross-subject protocol
U-012 — Final held-out subject strategy
```

## Models

```text
U-013 — Final CSP configuration
U-014 — Final EEGNet architecture details
U-015 — Final training hyperparameters
```

## Calibration

```text
U-016 — Final calibration method
U-017 — Calibration fitting partition
U-018 — Reliability-diagram binning
```

## Bayesian / Goal Mapping

```text
U-019 — Binary EEG → multi-goal interaction protocol
U-020 — Decoder posterior → goal likelihood construction
U-021 — Prior policy
U-022 — Bayesian stopping / commitment rule
```

## Shared Autonomy

```text
U-023 — Confidence / entropy thresholds
U-024 — Exact proceed / confirm / defer policy
U-025 — Prolonged-uncertainty fallback
```

## Adaptation

```text
U-026 — Exact adaptation mechanism
U-027 — Update formula
U-028 — Bounds / warm-up / reset
```

## Planning / Safety

```text
U-029 — Environmental risk values
U-030 — Risk normalization
U-031 — Risk weight λ
U-032 — Prohibited-hazard threshold
U-033 — Final no-safe-path policy
```

## Experimental Analysis

```text
U-034 — Final A/B/C/D component matrix
U-035 — Robustness perturbation levels
U-036 — Final inferential-statistics policy
```

---

# 4. DECISION ENTRY TEMPLATE

Use:

```text
## D-XXX — <Decision Name>

Status:
APPROVED / SUPERSEDED / REJECTED / UNRESOLVED

Date:
YYYY-MM-DD

Decision:
<exact approved statement>

Context:
<why the decision was needed>

Alternatives considered:
- ...
- ...

Rationale:
<why this option was selected>

Affected documents/modules:
- ...

Implementation consequence:
<what Codex is now authorized to do>

Approved by:
Project Owner
```

---

# 5. CHANGE RULE

If an approved decision changes:

```text
1. keep the original entry;
2. mark it SUPERSEDED;
3. add the new decision with a new ID;
4. reference the old decision;
5. update MASTER_PROJECT_SPEC.md if the change affects the project's constitution;
6. update affected numbered documents;
7. create a new Codex implementation ticket if required.
```

Never erase decision history.
