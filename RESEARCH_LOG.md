# RESEARCH_LOG.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Scientific Research, Literature Notes, Alternatives, and Open Questions

**Purpose:** Preserve scientific research findings and reasoning that may support future decisions  
**Important:** This file does not itself authorize implementation  
**Implementation authority comes from:** `MASTER_PROJECT_SPEC.md`, `DECISIONS.md`, and `CURRENT_TASK.md`

---

# 1. HOW TO USE THIS LOG

Use this file for:

- literature findings;
- methodological alternatives;
- equations;
- scientific questions;
- design comparisons;
- evidence supporting a proposed decision;
- reasons for rejecting an approach;
- unresolved scientific risks.

Do not use it for:

- fabricated experiment results;
- approved-decision replacement;
- implementation status;
- active Codex tickets.

---

# 2. ENTRY TEMPLATE

```text
## R-XXX — <Research Topic>

Date:
YYYY-MM-DD

Question:
<what are we trying to understand?>

Source / Evidence:
<papers, documentation, dataset docs, implementation evidence>

Key Findings:
- ...
- ...

Alternatives:
A. ...
B. ...
C. ...

Implications for Project:
- ...

Recommendation:
<optional>

Status:
OPEN / REVIEWED / DECISION REQUIRED / CLOSED

Linked Decision:
D-XXX or NONE
```

---

# 3. CURRENT RESEARCH THEMES

## R-001 — PhysioNet EEGBCI Dataset Semantics

**Status:** REVIEWED / RESOLVED FOR CURRENT PIPELINE

Current project understanding:

```text
Dataset:
EEG Motor Movement/Imagery Database

Subjects:
109

Channels:
64

Sampling:
160 Hz

Format:
EDF+
```

Relevant run map:

```text
1        eyes open
2        eyes closed
3/7/11   motor execution: left vs right fist
4/8/12   motor imagery: left vs right fist
5/9/13   motor execution: both fists vs feet
6/10/14  motor imagery: both fists vs feet
```

For runs 4/8/12:

```text
T0 = rest
T1 = imagined left fist
T2 = imagined right fist
```

Current decision state:
- T0 handling is resolved by D-036.
- The current primary decoder remains Left-vs-Right motor imagery.

---

## R-002 — Classical Motor-Imagery Baseline

**Status:** REVIEWED / RESOLVED FOR CURRENT BASELINE

Candidate baseline:

```text
CSP + LDA
```

Why it matters:

- established motor-imagery baseline;
- interpretable;
- lower complexity;
- useful against deep-learning overclaiming;
- makes leakage easier to inspect.

Important scientific risk:

```text
CSP must be fit within the training partition.
```

Fitting CSP before the split can leak test information.

Current decision state:
- D-043 and D-044 freeze the CSP configuration and validation-only selection rule.

---

## R-003 — EEGNet / Compact CNN

**Status:** REVIEWED / RESOLVED FOR CURRENT MODEL

The project includes EEGNet or a scientifically accurate compact EEG CNN.

Key issue:

The implementation name must match the actual architecture.

If the model materially differs from EEGNet:

```text
call it a compact EEG CNN inspired by EEGNet
```

rather than falsely claiming exact reproduction.

Current decision state:
- D-045 through D-047 freeze the approved EEGNet architecture/training details required by the current project.

---

## R-004 — Calibration

**Status:** REVIEWED / RESOLVED BY D-048 THROUGH D-050

Core observation:

```text
classification accuracy ≠ calibrated confidence
```

Candidate methods historically considered:

```text
temperature scaling
Platt / sigmoid scaling
isotonic regression
```

Core metrics:

```text
ECE
Brier Score
Reliability Diagram
```

Resolved by:

```text
D-048 — Final Calibration Method
D-049 — Calibration Fitting Partition
D-050 — Reliability-Diagram Binning
```

---

## R-005 — Decoder Probability vs Bayesian Likelihood

**Status:** REVIEWED / RESOLVED BY D-052

Critical distinction:

\[
P(C \mid EEG)
\]

and:

\[
P(E \mid G)
\]

must not be silently conflated.

Current project semantics are governed by D-051 and D-052.

---

## R-006 — Sequential Bayesian Goal Inference

**Status:** REVIEWED / RESOLVED FOR CURRENT PROJECT

Core update:

\[
P(G \mid E_{1:t})
\propto
P(E_t \mid G)
P(G \mid E_{1:t-1})
\]

Current decision state:

```text
D-051 — binary-choice interaction
D-052 — evidence likelihood weights
D-053 — baseline prior
D-054 — stopping / commitment / reset
D-055 through D-057 — uncertainty/shared-autonomy policy
D-074 — one accepted replay epoch = one evidence observation
```

No M7-blocking Bayesian decision remains open.

---

## R-007 — Posterior Entropy

**Status:** REVIEWED / RESOLVED FOR CURRENT POLICY

Initial uncertainty measure:

\[
H(P)=-\sum_i p_i \log p_i
\]

Important caveat:

```text
low entropy does not imply correctness
```

A confidently wrong posterior remains a critical failure mode. D-055 makes posterior thresholds authoritative while entropy remains the explicit uncertainty measure.

---

## R-008 — Binary EEG to Multi-Goal SAR

**Status:** REVIEWED / RESOLVED BY D-051

The approved interaction uses two currently valid candidate goals/options at each decision point and represents multi-goal SAR as a sequence of binary choices. The binary decoder must not be treated as a direct K-goal classifier.

---

## R-009 — Shared-Autonomy Thresholds

**Status:** REVIEWED / RESOLVED BY D-055 THROUGH D-057

Conceptual modes:

```text
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

The exact current thresholds and fallback behavior are no longer open research questions for the primary system.

---

## R-010 — Adaptation

**Status:** REVIEWED / RESOLVED BY D-058 THROUGH D-060

The current approved mechanism is bounded subject-specific, candidate-pair-specific prior personalization from explicit human-approved feedback only.

Required properties remain:

```text
bounded
logged
subject-isolated
resettable
leakage-safe
switchable
```

Do not claim formal adaptive control beyond what is implemented.

---

## R-011 — A* and Risk-Aware Planning

**Status:** REVIEWED / RESOLVED FOR CURRENT PROJECT

Approved planner:

```text
A*
four-connected grid
Manhattan heuristic
```

Current risk policy is governed by:

```text
D-061 — fixed normalized risk scale
D-062 — normalization/exposure aggregation
D-063 — lambda = 2.0
D-064 — PROHIBITED = 1.00 hard boundary
D-065 — no-safe-path policy
D-066 — controlled environment-change replanning
```

No M7-blocking planning/safety parameter remains open.

---

## R-012 — Safety Architecture

**Status:** REVIEWED / RESOLVED FOR CURRENT PROJECT

Core sequence:

```text
planner proposes
→ safety checks
→ environment executes only if approved
```

Hard safety and soft risk remain separate. Prohibited-hazard and no-safe-path behavior are governed by D-064 and D-065.

---

## R-013 — Experimental Comparison Logic

**Status:** REVIEWED / RESOLVED BY D-077

Principal comparison:

```text
A — Direct EEG
B — Confidence-aware
C — Bayesian shared autonomy
D — Full system
```

The final component matrix is frozen by D-077. Ablations continue to isolate calibration, Bayes, uncertainty, safety, and adaptation where applicable.

---

## R-014 — Cross-Subject Generalization

**Status:** REVIEWED / RESOLVED BY D-041 AND D-042

Core leakage constraint:

```text
train_subjects ∩ test_subjects = ∅
```

Primary protocol:
- fixed 70/15/15 subject-level train/validation/final-test split;
- deterministic seed 42 subject shuffle;
- frozen versioned split manifest;
- subject-wise reporting retained.

---

## R-015 — Negative Results

**Status:** REVIEWED

Scientifically valid outcomes include:

```text
CSP+LDA > EEGNet
calibration adds little
Bayes increases latency
adaptation harms some subjects
safety increases path length
System D does not dominate all metrics
```

The project must preserve these outcomes if observed.

---

## R-016 — M7 Robustness Design

**Status:** REVIEWED / RESOLVED BY D-078

Primary M7 robustness stress testing operates at the binary probability/evidence interface rather than inventing a physiological EEG-noise model.

Two mandatory perturbation families are frozen:

```text
R1 — evidence flattening toward [0.5,0.5]
epsilon = 0.00, 0.25, 0.50, 0.75, 1.00

R2 — contradictory-evidence swap [pA,pB] -> [pB,pA]
contamination fraction q = 0.00, 0.10, 0.20, 0.30, 0.40
```

Each perturbation must preserve labels/true-goal evaluation metadata, use deterministic/frozen selection where randomness is involved, and must not be used to refit or tune the decoder, calibrator, thresholds, or protected-test policy.

---

## R-017 — M7 Inferential Statistics

**Status:** REVIEWED / RESOLVED BY D-079

Primary inference unit for real-EEG/system comparisons:

```text
subject
```

Primary policy:

```text
two-sided tests
alpha = 0.05
paired subject-level raw effects
95% paired bootstrap confidence intervals
10,000 bootstrap resamples with fixed seed
paired sign-flip/permutation test
Holm correction within experiment families
```

For a 17-subject final-test cohort, exact sign-flip enumeration is feasible when all subject-level paired differences are available. Seeds and individual trials must not be treated as substitutes for independent subjects.

Deterministic planner/safety scenario validation remains primarily descriptive/exhaustive rather than being forced into artificial significance testing.

---

# 4. OPEN RESEARCH QUEUE

No currently known M7-blocking scientific decision remains unresolved after D-077 through D-079.

M7-T02 execution is additionally frozen by D-080: deterministic S1–S7 scenarios, the accepted M6 mission map, deterministic simulated-human commands through the existing authority API, operational/bootstrap/R2 seed 42, and a hard pre-final split/artifact/manifest gate. This is an offline software evaluation, not a real human-subject study. Protected final outcomes must not influence fitting, selection, calibration, thresholds, scenarios, metrics, or policy.

Current research/analysis queue is implementation- and evidence-dependent rather than parameter-decision-dependent:

```text
[ ] Observe actual decoder and calibration behavior on valid experiment outputs
[ ] Examine subject-wise failure cases and difficult subjects
[ ] Examine whether robustness degradation is graceful or pathological
[ ] Examine trade-offs among wrong-goal rate, deferral/confirmation, latency, and safety
[ ] Examine whether approved adaptation helps, harms, or has no meaningful effect by subject
[ ] Preserve unexpected, mixed, and negative results for final discussion
```

Any new scientifically meaningful ambiguity discovered during M7 must be surfaced for Project Owner approval before Codex changes methodology.

---

# 5. SOURCE QUALITY RULE

For critical methodology:

Prefer:

```text
primary papers
official dataset documentation
official library documentation
authoritative textbooks / standards
```

Avoid using unsupported model memory as the sole basis for a parameter choice.

---

# 6. RESEARCH → DECISION WORKFLOW

```text
research question
→ evidence gathered
→ alternatives compared
→ ChatGPT recommendation
→ Project Owner approval
→ DECISIONS.md entry
→ implementation ticket
```

Research is evidence.

Decision is authority.
