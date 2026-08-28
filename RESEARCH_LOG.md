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

**Status:** REVIEWED

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

Implication:

The initial decoder may use Left-vs-Right motor imagery.

T0 handling remains a methodological decision.

---

## R-002 — Classical Motor-Imagery Baseline

**Status:** REVIEWED

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

---

## R-003 — EEGNet / Compact CNN

**Status:** REVIEWED

The project includes EEGNet or a scientifically accurate compact EEG CNN.

Key issue:

The implementation name must match the actual architecture.

If the model materially differs from EEGNet:

```text
call it a compact EEG CNN inspired by EEGNet
```

rather than falsely claiming exact reproduction.

---

## R-004 — Calibration

**Status:** DECISION REQUIRED

Core observation:

```text
classification accuracy ≠ calibrated confidence
```

Candidate methods:

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

Open questions:

- which calibration method;
- which partition fits it;
- how reliability bins are defined;
- how cross-subject calibration is handled.

Linked unresolved decisions:

```text
U-016
U-017
U-018
```

---

## R-005 — Decoder Probability vs Bayesian Likelihood

**Status:** DECISION REQUIRED

Critical distinction:

Decoder output:

\[
P(C \mid EEG)
\]

Bayesian goal model requires:

\[
P(E \mid G)
\]

These are not automatically identical.

Implication:

A Goal-Evidence Adapter must define the semantics.

Potential approaches require explicit modeling and should not be invented during coding.

Linked unresolved decision:

```text
U-020
```

---

## R-006 — Sequential Bayesian Goal Inference

**Status:** REVIEWED / PARTIALLY OPEN

Core update:

\[
P(G \mid E_{1:t})
\propto
P(E_t \mid G)
P(G \mid E_{1:t-1})
\]

Generic Bayesian inference can be implemented and verified with synthetic likelihoods independently of the real EEG-to-goal mapping.

Open questions:

- final prior policy;
- evidence independence assumptions;
- stopping/commitment rule;
- reset semantics in final interaction protocol.

---

## R-007 — Posterior Entropy

**Status:** REVIEWED

Initial uncertainty measure:

\[
H(P)=-\sum_i p_i \log p_i
\]

Interpretation:

```text
high entropy
→ diffuse belief

low entropy
→ concentrated belief
```

Important caveat:

```text
low entropy does not imply correctness
```

A confidently wrong posterior remains a critical failure mode.

---

## R-008 — Binary EEG to Multi-Goal SAR

**Status:** DECISION REQUIRED

Problem:

```text
initial EEG decoder = binary
SAR world = potentially multiple goals
```

Preserved alternatives:

```text
A. two active selectable goals at a time
B. hierarchical / sequential binary selection
C. EEG controls an abstract binary priority
D. later multiclass EEG
```

Do not permanently hard-code T1/T2 to specific victims without an approved interaction protocol.

Linked unresolved decision:

```text
U-019
```

---

## R-009 — Shared-Autonomy Thresholds

**Status:** DECISION REQUIRED

Conceptual modes:

```text
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

Old numeric thresholds discussed during planning are examples only.

Open questions:

- confidence vs entropy policy;
- threshold values;
- hysteresis;
- prolonged ambiguity;
- confirmation burden.

Linked decisions:

```text
U-023
U-024
U-025
```

---

## R-010 — Adaptation

**Status:** DECISION REQUIRED

Potential bounded targets:

```text
user-specific priors
decoder reliability
confidence thresholds
evidence weights
```

Required properties:

```text
bounded
logged
subject-isolated
resettable
leakage-safe
switchable
```

Do not claim formal adaptive control unless implemented.

---

## R-011 — A* and Risk-Aware Planning

**Status:** PARTIALLY REVIEWED

Approved planner:

```text
A*
```

Initial grid:

```text
four-connected
```

Initial heuristic:

```text
Manhattan distance
```

Conceptual risk-aware cost:

\[
J = distance + \lambda \cdot risk
\]

Open:

- risk scale;
- normalization;
- \(\lambda\);
- prohibited hazards.

---

## R-012 — Safety Architecture

**Status:** REVIEWED / PARTIALLY OPEN

Core sequence:

```text
planner proposes
→ safety checks
→ environment executes only if approved
```

Hard safety and soft risk must remain separate.

Core hard-safety candidates:

```text
map boundary
blocked cells
invalid actions
pause
emergency stop
prohibited hazards
```

The prohibited-hazard policy remains unresolved.

---

## R-013 — Experimental Comparison Logic

**Status:** REVIEWED / PARTIALLY OPEN

Principal comparison:

```text
A — Direct EEG
B — Confidence-aware
C — Bayesian shared autonomy
D — Full system
```

Required principle:

Each system must be defined explicitly before experiments.

Do not allow component leakage between conditions.

Ablations should isolate:

```text
calibration
Bayes
uncertainty
safety
adaptation
```

---

## R-014 — Cross-Subject Generalization

**Status:** DECISION REQUIRED

Core leakage constraint:

```text
train_subjects ∩ test_subjects = ∅
```

Possible protocols:

```text
leave-one-subject-out
grouped K-fold
fixed held-out subject groups
```

The final protocol is unresolved.

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

# 4. OPEN RESEARCH QUEUE

Priority open questions:

```text
[ ] Final EEG preprocessing configuration
[ ] T0 handling
[ ] Final data split strategy
[ ] Cross-subject protocol
[ ] Calibration method / split
[ ] Binary EEG → multi-goal protocol
[ ] Goal-evidence likelihood semantics
[ ] Bayesian commitment rule
[ ] Shared-autonomy thresholds
[ ] Adaptation mechanism
[ ] Risk scale and λ
[ ] Prohibited-hazard rule
[ ] Final A/B/C/D matrix
[ ] Robustness perturbation definitions
[ ] Statistical-analysis plan
```

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
