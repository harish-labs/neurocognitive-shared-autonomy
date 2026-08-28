# 23_RESULTS_AND_ANALYSIS.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Results, Analysis & Scientific Interpretation Framework

**Document ID:** L-01  
**Document class:** Results / Analysis / Scientific Interpretation  
**Status:** Pre-results authoritative framework — contains **no fabricated experimental results**  
**Authority level:** Subordinate to `MASTER_PROJECT_SPEC.md`, approved methodology, experimental-design, metrics, testing, validity, and decision documents  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. PURPOSE

This document defines how project results must be:

- collected;
- organized;
- compared;
- analyzed;
- visualized;
- interpreted;
- connected to research questions;
- and reported responsibly.

This document is intentionally written **before final experiments are executed**.

Therefore it contains:

```text
NO invented accuracy
NO invented F1
NO invented calibration improvement
NO invented Bayesian improvement
NO invented task-success improvement
NO invented safety improvement
```

Actual numerical results must be inserted only after valid experiments are executed and logged.

---

# 1. CENTRAL ANALYSIS QUESTION

The project is not evaluated only as an EEG classifier.

The main system-level question is:

> **Can uncertainty-aware shared autonomy improve the reliability and safety of EEG-based intent control compared with direct brain-computer control in the controlled Search & Rescue simulation?**

The analysis must therefore connect:

```text
EEG decoding
→ confidence quality
→ Bayesian belief
→ uncertainty
→ autonomy decisions
→ navigation
→ safety
→ mission outcome
```

---

# 2. ANALYSIS PHILOSOPHY

The final analysis must distinguish four different questions:

## 2.1 Can EEG intent be decoded?

Evaluate decoder performance.

## 2.2 Can decoder confidence be trusted?

Evaluate calibration.

## 2.3 Can evidence accumulated over time produce more useful goal beliefs?

Evaluate Bayesian inference and uncertainty.

## 2.4 Does the complete decision architecture improve system behavior?

Evaluate shared autonomy, planning, safety, and mission outcomes.

A strong classifier alone does not prove a strong autonomous system.

---

# 3. RESULT LEVELS

Results should be organized into four levels.

```text
LEVEL 1 — EEG / ML
LEVEL 2 — Probability / Cognitive Inference
LEVEL 3 — Shared Autonomy / Decision Behaviour
LEVEL 4 — Search & Rescue System Performance
```

Each level must be analyzed separately before discussing end-to-end conclusions.

---

# 4. LEVEL 1 — EEG / MACHINE-LEARNING RESULTS

The first result section evaluates:

```text
CSP + LDA
EEGNet / compact CNN
```

Primary questions:

- Can Left vs Right motor imagery be discriminated?
- How does the classical baseline compare with the neural model?
- How much does performance vary between subjects?
- Does performance generalize under the approved held-out protocol?

---

# 5. EEG RESULT TABLE

Final report template:

| Model | Accuracy | Balanced Accuracy | Precision | Recall | F1 | AUROC | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| CSP + LDA | TBD | TBD | TBD | TBD | TBD | TBD | |
| EEGNet / Compact CNN | TBD | TBD | TBD | TBD | TBD | TBD | |

Do not populate until valid evaluation exists.

---

# 6. CONFUSION MATRICES

For each principal decoder, preserve:

```text
true Left → predicted Left
true Left → predicted Right
true Right → predicted Left
true Right → predicted Right
```

The confusion matrix is important because overall accuracy can hide directional asymmetry.

---

# 7. SUBJECT-LEVEL EEG ANALYSIS

Aggregate performance alone is insufficient.

Where supported by the final evaluation protocol, analyze:

```text
per-subject accuracy
per-subject balanced accuracy
per-subject F1
subject variability
failure subjects
```

Useful visualization:

```text
subject ID
vs
performance
```

Do not hide poor-performing subjects.

---

# 8. CLASSICAL VS NEURAL INTERPRETATION

Possible valid outcomes include:

```text
EEGNet > CSP+LDA
CSP+LDA > EEGNet
approximately equivalent
different models work better for different subjects
```

Do not assume EEGNet must win.

If CSP+LDA performs better, report it directly.

---

# 9. LEVEL 2 — CALIBRATION RESULTS

Classification correctness and probability reliability are separate.

The calibration section should evaluate:

```text
raw probability
vs
calibrated probability
```

using the final approved calibration method.

---

# 10. CALIBRATION METRICS

Primary calibration metrics may include:

```text
ECE
Brier Score
reliability diagram
```

Additional metrics may be reported only if justified.

---

# 11. CALIBRATION RESULT TABLE

| Model | Condition | ECE | Brier Score | Accuracy | Notes |
|---|---|---:|---:|---:|---|
| CSP+LDA | Raw | TBD | TBD | TBD | |
| CSP+LDA | Calibrated | TBD | TBD | TBD | |
| EEGNet | Raw | TBD | TBD | TBD | |
| EEGNet | Calibrated | TBD | TBD | TBD | |

Calibration should not be declared beneficial solely because one metric changes slightly.

---

# 12. RELIABILITY DIAGRAM

Plot:

```text
predicted confidence
vs
empirical accuracy
```

Include the ideal calibration line.

Interpret:

- overconfidence;
- underconfidence;
- well-calibrated regions;
- sparse bins.

---

# 13. CALIBRATION INTERPRETATION

A useful result would be:

```text
similar classification accuracy
+
better probability reliability
```

because downstream Bayesian/shared-autonomy modules depend on probabilities.

Do not claim calibration improves classification unless it actually does.

---

# 14. LEVEL 2 — BAYESIAN GOAL-INFERENCE RESULTS

The Bayesian layer must be analyzed as a sequential belief process.

For each episode/trial sequence, preserve:

```text
time step
incoming evidence
prior
likelihood
posterior
entropy
selected/leading hypothesis
```

---

# 15. BAYESIAN TRAJECTORY VISUALIZATION

Plot:

```text
time
vs
P(G1), P(G2), ... P(GK)
```

alongside:

```text
entropy
```

This should reveal whether evidence:

- converges;
- oscillates;
- remains ambiguous;
- becomes confidently wrong.

---

# 16. BAYESIAN ANALYSIS QUESTIONS

Evaluate:

1. Does sequential evidence stabilize the inferred goal?
2. How many evidence steps are typically needed?
3. Does uncertainty decrease when evidence is consistent?
4. What happens when evidence is contradictory?
5. What happens when early evidence is wrong?
6. Can the posterior recover?
7. Does calibration affect posterior behavior?

---

# 17. BAYESIAN PERFORMANCE METRICS

Depending on the final approved protocol:

```text
goal inference accuracy
wrong-goal commitment rate
time / evidence steps to commitment
posterior probability of true goal
entropy at commitment
recovery after misleading evidence
```

Only metrics defined in the approved metrics document should become headline results.

---

# 18. DIRECT VS SEQUENTIAL INFERENCE

One key comparison is conceptually:

```text
single decoder prediction
vs
sequential Bayesian belief
```

The analysis should determine whether evidence accumulation improves decision reliability.

Do not assume it does.

---

# 19. FAILURE MODE — CONFIDENTLY WRONG BAYESIAN BELIEF

A particularly important failure is:

```text
low entropy
+
wrong goal
```

This must be explicitly measured/reported if observed.

Low entropy means concentrated belief.

It does not guarantee correctness.

---

# 20. UNCERTAINTY RESULTS

The primary uncertainty signal is posterior entropy:

\[
H(P)=-\sum_g P(g)\log P(g)
\]

Analyze its relationship with:

```text
correctness
ambiguity
confirmation requests
deferrals
wrong-goal commitments
```

---

# 21. UNCERTAINTY DISTRIBUTION

Useful comparison:

```text
entropy when inference correct
vs
entropy when inference incorrect
```

If incorrect predictions frequently have low entropy, the uncertainty mechanism has an important limitation.

---

# 22. LEVEL 3 — SHARED-AUTONOMY RESULTS

The shared-autonomy layer should be evaluated through actual behavioral consequences.

Relevant modes include:

```text
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

Exact threshold values must come from the approved configuration.

---

# 23. SHARED-AUTONOMY BEHAVIOR TABLE

| Metric | Value |
|---|---:|
| Automatic proceeds | TBD |
| Confirmation requests | TBD |
| Deferrals | TBD |
| Human overrides | TBD |
| Pauses | TBD |
| Emergency stops | TBD |
| Wrong autonomous commitments | TBD |

Counts should be accompanied by normalized rates where appropriate.

---

# 24. HUMAN-BURDEN ANALYSIS

Shared autonomy should not be judged only by success.

Measure interaction burden where possible:

```text
confirmation count
override count
decision delay
number of interventions
```

A system that never makes mistakes because it asks the human about every action is not necessarily useful autonomy.

---

# 25. AUTONOMY TRADE-OFF

Analyze the trade-off between:

```text
automation
vs
human intervention
vs
wrong commitment
```

The desired behavior is not simply:

```text
maximum autonomy
```

but:

```text
appropriate autonomy under uncertainty
```

---

# 26. LEVEL 4 — PLANNING RESULTS

A* planning should be evaluated separately from intent inference.

Potential metrics:

```text
path length
path cost
planning success
planning time
replanning count
risk exposure
```

Do not attribute planner failures to EEG unless causally connected.

---

# 27. RISK-AWARE PLANNING ANALYSIS

Compare, where approved:

```text
shortest-path behavior
vs
risk-aware behavior
```

Expected trade-off:

```text
possibly longer route
for
reduced risk exposure
```

But this must be demonstrated experimentally.

---

# 28. SAFETY RESULTS

The safety layer should be evaluated using deliberately constructed failure conditions.

Examples:

```text
attempted out-of-bounds move
attempted blocked-cell entry
attempted prohibited-hazard entry
movement during pause
movement during emergency stop
```

---

# 29. SAFETY RESULT TABLE

| Safety Test | Attempts | Correctly Blocked | Failures | Pass Rate |
|---|---:|---:|---:|---:|
| Out of bounds | TBD | TBD | TBD | TBD |
| Blocked cell | TBD | TBD | TBD | TBD |
| Prohibited hazard | TBD | TBD | TBD | TBD |
| Movement while paused | TBD | TBD | TBD | TBD |
| Movement after emergency stop | TBD | TBD | TBD | TBD |

This evaluates simulated constraint enforcement, not real-world robotic safety.

---

# 30. SEARCH & RESCUE MISSION RESULTS

End-to-end evaluation should report mission-level behavior.

Potential metrics:

```text
task success rate
correct-goal completion
wrong-goal commitment rate
mission completion time
path length
risk exposure
safety interventions
human interventions
replanning
```

---

# 31. PRINCIPAL SYSTEM COMPARISON

The project should preserve the principal comparison:

```text
A — Direct EEG
B — Confidence-aware
C — Bayesian shared autonomy
D — Full system
```

The exact final component matrix must be frozen before experiments.

---

# 32. SYSTEM COMPARISON TABLE

| Metric | A Direct EEG | B Confidence-Aware | C Bayesian Shared Autonomy | D Full System |
|---|---:|---:|---:|---:|
| Task success | TBD | TBD | TBD | TBD |
| Correct-goal completion | TBD | TBD | TBD | TBD |
| Wrong-goal commitment | TBD | TBD | TBD | TBD |
| Human interventions | TBD | TBD | TBD | TBD |
| Decision latency | TBD | TBD | TBD | TBD |
| Risk exposure | TBD | TBD | TBD | TBD |
| Safety violations | TBD | TBD | TBD | TBD |
| Path cost | TBD | TBD | TBD | TBD |

Do not pre-label D as “best.”

---

# 33. MOST IMPORTANT SYSTEM QUESTION

The strongest analysis is not:

> Which system has the highest EEG accuracy?

It is:

> **How does increasingly structured uncertainty handling change downstream autonomous behavior?**

That is what A/B/C/D should expose.

---

# 34. ABLATION ANALYSIS

The architecture should support:

```text
Full
Full - calibration
Full - Bayes
Full - uncertainty gating
Full - safety
Full - adaptation
```

Only execute scientifically meaningful ablations.

---

# 35. ABLATION RESULT TABLE

| Variant | Task Success | Wrong Goal | Human Burden | Risk | Safety Failures |
|---|---:|---:|---:|---:|---:|
| Full | TBD | TBD | TBD | TBD | TBD |
| - Calibration | TBD | TBD | TBD | TBD | TBD |
| - Bayes | TBD | TBD | TBD | TBD | TBD |
| - Uncertainty | TBD | TBD | TBD | TBD | TBD |
| - Safety | TBD | TBD | TBD | TBD | TBD |
| - Adaptation | TBD | TBD | TBD | TBD | TBD |

Do not interpret an ablation causally if multiple components changed simultaneously.

---

# 36. ROBUSTNESS ANALYSIS

Robustness experiments should deliberately degrade evidence according to an approved perturbation model.

Potential analyses:

```text
decoder corruption
probability noise
evidence ambiguity
contradictory evidence
environmental hazards
blocked routes
```

Exact severity levels remain governed by the experiment specification.

---

# 37. ROBUSTNESS CURVE

Useful plot:

```text
degradation severity
vs
task success / wrong-goal commitment / intervention rate
```

A robust shared-autonomy system may degrade more gracefully than direct control.

This is a hypothesis, not a guaranteed result.

---

# 38. CROSS-SUBJECT ANALYSIS

If the final evaluation includes held-out subjects, report:

```text
aggregate performance
distribution across subjects
median
spread
worst cases
best cases
```

Do not report only the mean.

---

# 39. ADAPTATION ANALYSIS

If adaptation is implemented, compare:

```text
adaptation OFF
vs
adaptation ON
```

Possible metrics:

```text
goal inference accuracy
wrong commitment
confirmation burden
task success
subject-level change
```

Do not claim personalization if only global tuning is used.

---

# 40. LATENCY ANALYSIS

Because the project is simulated-real-time rather than live acquisition, latency must be interpreted carefully.

Possible measured components:

```text
decoder inference time
Bayesian update time
planning time
safety-check time
system decision time
```

Do not report prerecorded replay timing as live EEG acquisition latency.

---

# 41. FAILURE-CASE ANALYSIS

The final report must include failure cases.

Important categories:

```text
EEG misclassification
overconfident wrong decoder output
miscalibration
Bayesian convergence to wrong goal
persistent ambiguity
excessive confirmation
incorrect/inefficient route
safety rejection
unreachable goal
adaptation failure
```

A strong technical report explains where the system fails.

---

# 42. FAILURE CASE TEMPLATE

```text
Failure ID:
Episode:
True goal:
Decoder behavior:
Calibrated evidence:
Posterior trajectory:
Entropy:
Autonomy decision:
Planner behavior:
Safety behavior:
Outcome:
Likely cause:
Recoverable:
Relevant artifact:
```

---

# 43. CAUSAL ATTRIBUTION RULE

Do not say:

> “The EEG model caused mission failure”

unless the event chain demonstrates that.

Instead trace:

```text
EEG error
→ evidence
→ posterior
→ autonomy decision
→ goal
→ planner
→ outcome
```

This modular traceability is a major benefit of the architecture.

---

# 44. STATISTICAL ANALYSIS

Final statistical procedures must be selected before final inferential claims.

Possible analyses may include:

```text
confidence intervals
paired comparisons
non-parametric paired tests
effect sizes
subject-level analysis
bootstrap intervals
```

The exact statistical-analysis policy remains subject to approval.

Do not select tests after seeing results solely to obtain significance.

---

# 45. UNIT OF ANALYSIS

Before statistical testing, explicitly define the unit:

```text
trial
subject
episode
mission
```

Do not treat correlated repeated observations as independent without justification.

---

# 46. EFFECT SIZE

Where statistical comparisons are performed, report effect size where appropriate.

Do not rely only on:

```text
p < 0.05
```

Practical/system relevance matters.

---

# 47. CONFIDENCE INTERVALS

Where feasible, report uncertainty around key aggregate metrics.

Examples:

```text
task success
wrong-goal commitment
decoder accuracy
intervention rate
```

Exact interval methodology must be documented.

---

# 48. MULTIPLE COMPARISONS

If many statistical hypotheses are tested, the final analysis must consider multiplicity.

Do not generate dozens of post-hoc comparisons and selectively report significant ones.

---

# 49. FIGURE PLAN

Recommended final figures:

```text
Figure 1 — System architecture
Figure 2 — EEG preprocessing / example trial
Figure 3 — CSP+LDA vs EEGNet performance
Figure 4 — Calibration reliability diagram
Figure 5 — Bayesian posterior + entropy trajectory
Figure 6 — Shared-autonomy state example
Figure 7 — Search & Rescue path example
Figure 8 — A/B/C/D system comparison
Figure 9 — Robustness curve
Figure 10 — Subject-level performance distribution
```

Only include figures that contribute to the argument.

---

# 50. TABLE PLAN

Recommended final tables:

```text
Table 1 — Dataset / experimental configuration
Table 2 — EEG decoder metrics
Table 3 — Calibration metrics
Table 4 — Bayesian inference metrics
Table 5 — Shared-autonomy behavior
Table 6 — Planning/safety metrics
Table 7 — A/B/C/D comparison
Table 8 — Ablations
Table 9 — Robustness
Table 10 — Failure cases / limitations summary
```

---

# 51. RESULT TRACEABILITY

Every headline result must trace to:

```text
Experiment ID
Git commit
configuration
data split
model/checkpoint
artifact
metric computation
```

No traceability → no headline claim.

---

# 52. RAW VS DERIVED RESULTS

Preserve distinction between:

## Raw outputs

```text
predictions
probabilities
posteriors
entropy
actions
paths
safety events
```

## Derived metrics

```text
accuracy
ECE
task success
wrong-goal rate
risk exposure
```

Do not save only final summary numbers.

---

# 53. RESULT VALIDITY STATUS

Each experiment should be labeled:

```text
VALID
INVALID
SUPERSEDED
EXPLORATORY
```

Only valid experiments may support final claims.

---

# 54. INVALID RESULT CONDITIONS

Mark a result invalid if:

- subject leakage exists;
- trial leakage exists;
- test labels influenced calibration/tuning;
- wrong event mapping was used;
- class ordering was wrong;
- configuration is unrecoverable;
- implementation was scientifically incorrect;
- required artifacts are missing.

Do not quietly delete invalid runs.

---

# 55. EXPLORATORY RESULTS

Exploratory runs may help development.

They must not automatically become final evidence.

Examples:

```text
small subject subset
temporary split
temporary threshold
synthetic likelihood
smoke-test environment
```

Label them clearly.

---

# 56. INTERPRETATION RULE — CORRELATION VS CAUSATION

If two metrics change together, do not automatically claim one caused the other.

Example:

```text
lower entropy
+
higher success
```

does not by itself prove entropy reduction caused success.

Use controlled comparisons/ablations where possible.

---

# 57. INTERPRETATION RULE — ABSENCE OF IMPROVEMENT

If the full system does not improve a metric:

```text
report it
```

Possible interpretation:

- component unnecessary;
- implementation weak;
- dataset limitation;
- threshold problem;
- metric insensitive;
- trade-off elsewhere.

Do not hide the result.

---

# 58. INTERPRETATION RULE — TRADE-OFFS

A component can help one metric while hurting another.

Examples:

```text
safety ↑
path length ↑
```

```text
confirmation ↑
wrong commitment ↓
```

```text
Bayesian accumulation ↑ reliability
decision latency ↑
```

These trade-offs are scientifically valuable.

---

# 59. INTERPRETATION RULE — CLASSIFIER VS SYSTEM

Do not equate:

```text
higher EEG accuracy
```

with:

```text
better mission performance
```

The project explicitly tests whether system architecture changes the consequences of imperfect decoding.

---

# 60. INTERPRETATION RULE — CALIBRATION

If calibration improves ECE but not accuracy:

Correct:

> Probability reliability improved while discrimination performance remained approximately unchanged.

Incorrect:

> The classifier became more accurate.

---

# 61. INTERPRETATION RULE — BAYES

If Bayesian accumulation reduces wrong commitment:

Correct:

> Sequential evidence accumulation was associated with fewer wrong-goal commitments under the tested protocol.

Avoid:

> Bayesian reasoning understands the user's intention.

---

# 62. INTERPRETATION RULE — SAFETY

If the safety controller blocks all tested invalid moves:

Correct:

> The implemented safety layer successfully enforced the tested simulated constraints.

Incorrect:

> The rescue system is proven safe.

---

# 63. INTERPRETATION RULE — SIMULATION

If missions succeed in the 2D environment:

Correct:

> The system completed the tested simulated Search & Rescue tasks.

Incorrect:

> The system can perform real disaster rescue.

---

# 64. INTERPRETATION RULE — ADAPTATION

If adaptation improves results:

Correct:

> The tested system-side personalization mechanism improved [metric] under the evaluated protocol.

Do not claim:

> The BCI learns the user's brain

unless the implemented mechanism scientifically supports that statement.

---

# 65. DISCUSSION STRUCTURE

The final discussion should follow:

```text
1. Main finding
2. EEG decoder findings
3. Calibration findings
4. Bayesian inference findings
5. Shared-autonomy findings
6. Planning/safety findings
7. A/B/C/D comparison
8. Trade-offs
9. Failure cases
10. Relation to literature
11. Limitations
12. Future work
```

---

# 66. RESEARCH-QUESTION MAPPING

Every research question from:

```text
02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md
```

must eventually map to:

```text
experiment
→ metric
→ result
→ interpretation
```

Final analysis should not introduce major research questions that were never part of the approved project.

---

# 67. HYPOTHESIS OUTCOMES

For every hypothesis, use one of:

```text
SUPPORTED
PARTIALLY SUPPORTED
NOT SUPPORTED
INCONCLUSIVE
```

Do not force binary success/failure if evidence is mixed.

---

# 68. RESULT WRITING TEMPLATE

For each major result:

```text
Question:
Experiment:
Comparison:
Metric:
Observed result:
Statistical evidence:
Interpretation:
Limitation:
Artifact:
```

This prevents vague reporting.

---

# 69. EXAMPLE — PLACEHOLDER ONLY

```text
Question:
Did calibration improve probability reliability?

Experiment:
E2

Comparison:
Raw vs calibrated decoder probabilities

Metric:
ECE and Brier Score

Observed result:
TBD

Interpretation:
TBD after execution

Limitation:
Dependent on approved calibration split/method.
```

Do not replace TBD until real results exist.

---

# 70. WHAT COUNTS AS A STRONG PROJECT RESULT

The project does not require every component to outperform every baseline.

A scientifically strong result can be:

```text
CSP+LDA competitive with EEGNet
+
calibration improves confidence reliability
+
Bayesian accumulation reduces unstable decisions
+
uncertainty gating reduces wrong autonomous commitment
+
safety prevents tested invalid actions
+
trade-offs are measured honestly
```

But this is an example of the **type of evidence chain**, not a predicted outcome.

---

# 71. WHAT WOULD WEAKEN THE ANALYSIS

Avoid:

- reporting only accuracy;
- hiding subject variability;
- showing only successful missions;
- selecting thresholds after inspecting test outcomes;
- presenting screenshots without metrics;
- claiming novelty from standard algorithms;
- treating entropy as correctness;
- treating simulation as real-world validation;
- ignoring human-intervention burden;
- omitting negative results.

---

# 72. RESULT REPRODUCIBILITY CHECKLIST

Before a result enters the final report:

```text
[ ] Experiment ID exists
[ ] Git commit recorded
[ ] Config snapshot exists
[ ] Dataset subjects/runs recorded
[ ] Split recorded
[ ] Seed recorded where relevant
[ ] Model/checkpoint identified
[ ] Calibration state identified
[ ] Raw outputs preserved
[ ] Metric script/version known
[ ] Result artifact exists
[ ] Validity status = VALID
```

---

# 73. FINAL CLAIM CHECKLIST

Before writing a conclusion:

```text
[ ] Claim is supported by actual experiment
[ ] Comparison is fair
[ ] Test set was protected
[ ] Result is reproducible
[ ] Statistical wording is appropriate
[ ] Simulation boundary is stated
[ ] No clinical/real-rescue implication
[ ] Failure cases considered
[ ] Relevant limitation stated
```

---

# 74. RESULTS DIRECTORY RECOMMENDATION

Recommended organization:

```text
results/
├── eeg/
├── calibration/
├── bayesian/
├── shared_autonomy/
├── planning/
├── safety/
├── system_comparison/
├── ablations/
├── robustness/
├── subject_analysis/
└── final/
```

Each experiment should retain a unique ID.

---

# 75. FINAL RESULTS PACKAGE

The final results package should contain:

```text
summary tables
machine-readable metrics
figures
experiment configs
validity status
failure cases
statistical outputs
artifact manifest
```

Do not rely only on a notebook or screenshots.

---

# 76. CURRENT RESULTS STATUS

At the time this document is generated:

```text
EEG decoder results:
NOT YET GENERATED

Calibration results:
NOT YET GENERATED

Bayesian results:
NOT YET GENERATED

Shared-autonomy results:
NOT YET GENERATED

Planning results:
NOT YET GENERATED

Safety results:
NOT YET GENERATED

A/B/C/D comparison:
NOT YET GENERATED

Ablations:
NOT YET GENERATED

Robustness:
NOT YET GENERATED

Cross-subject results:
NOT YET GENERATED

Adaptation results:
NOT YET GENERATED
```

This is intentional.

The project is currently defining the framework that future experiments must satisfy.

---

# 77. FINAL ANALYSIS PRINCIPLE

The final analysis must tell a coherent evidence chain:

```text
How well was EEG decoded?
        ↓
Were the probabilities reliable?
        ↓
How did evidence alter goal belief?
        ↓
How uncertain was that belief?
        ↓
How did uncertainty change autonomy?
        ↓
What goal was approved?
        ↓
How did the planner act?
        ↓
Did safety intervene?
        ↓
What happened to the mission?
```

This chain is more important than any isolated model score.

---

# 78. COMPLETION CRITERIA FOR THIS DOCUMENT

This document becomes a completed **results document** only after:

1. approved experiments are executed;
2. valid artifacts exist;
3. result tables are populated;
4. figures are generated;
5. statistical analysis is completed where appropriate;
6. failure cases are documented;
7. hypotheses are evaluated;
8. interpretations are cross-checked against limitations;
9. every headline claim is traceable;
10. no TBD placeholder remains in the final-report sections.

Until then, it remains the authoritative **Results & Analysis Framework**.

---

# 79. CURRENT CONCLUSION

No scientific performance conclusion is currently authorized because the project has not yet produced validated experimental results.

The correct current statement is:

> **The project has established the methodology and analysis framework required to evaluate EEG decoding, probability calibration, Bayesian goal inference, uncertainty-aware shared autonomy, planning, safety, and end-to-end Search & Rescue performance. Actual conclusions will be derived only from reproducible experiments executed under the approved protocol.**
