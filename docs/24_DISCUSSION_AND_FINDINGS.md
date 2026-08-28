# 24_DISCUSSION_AND_FINDINGS.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Discussion, Findings, Interpretation, Trade-offs, Failure Analysis, and Scientific Synthesis

**Document ID:** L-02  
**Document class:** Results / Discussion / Scientific Synthesis  
**Status:** Pre-results discussion framework — contains **no fabricated findings**  
**Authority level:** Subordinate to `MASTER_PROJECT_SPEC.md`, approved methodology, experimental-design, metrics, testing, limitations, literature, and `23_RESULTS_AND_ANALYSIS.md`  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. PURPOSE

This document defines how the project’s final findings must be interpreted and discussed after valid experiments are completed.

It must answer:

- What did the project actually demonstrate?
- Which hypotheses were supported?
- Which components helped?
- Which components did not help?
- What trade-offs appeared?
- Where did the system fail?
- How do results relate to literature?
- What conclusions are justified?
- What conclusions are not justified?

This document currently contains **discussion structure only**.

No numerical findings are authorized until real experiments are executed.

---

# 1. DISCUSSION PRINCIPLE

The final discussion must not simply repeat tables and figures.

It should explain:

```text
what happened
why it may have happened
what it means
what trade-off it introduced
how confident we are in that interpretation
what remains uncertain
```

The discussion must connect all system layers rather than treating them as unrelated experiments.

---

# 2. CENTRAL FINDING TO BE EVALUATED

The project is designed around one main systems question:

> **Does uncertainty-aware shared autonomy make EEG-based control more reliable and safer than directly converting uncertain EEG predictions into autonomous decisions?**

The final discussion must answer this using actual A/B/C/D results.

Until those results exist, the answer remains:

```text
UNDETERMINED
```

---

# 3. DISCUSSION STRUCTURE

The final discussion should follow this sequence:

```text
1. Overall finding
2. EEG decoding
3. Probability calibration
4. Bayesian goal inference
5. Uncertainty behavior
6. Shared autonomy
7. Planning and safety
8. A/B/C/D comparison
9. Robustness
10. Cross-subject behavior
11. Adaptation
12. Failure cases
13. Trade-offs
14. Relation to literature
15. Limitations
16. Scientific contribution
17. Practical significance
18. Final answer to research question
```

---

# 4. OVERALL FINDING

Final template:

> **Overall, the experiments showed that [TBD].**

This statement must be supported by:

- valid experiment IDs;
- A/B/C/D comparison;
- core metrics;
- robustness/failure evidence.

Do not write a positive overall conclusion simply because the architecture was designed to improve reliability.

---

# 5. FINDING 1 — EEG DECODING

The first discussion section should interpret:

```text
CSP + LDA
vs
EEGNet / compact CNN
```

Questions:

1. Which model performed better overall?
2. Was the difference consistent across subjects?
3. Did the neural model justify its additional complexity?
4. Were there difficult subjects?
5. Did class-wise errors show directional bias?

---

# 6. POSSIBLE EEG FINDINGS

All of the following are scientifically valid possibilities:

```text
EEGNet clearly outperforms CSP+LDA
CSP+LDA outperforms EEGNet
both are similar
performance depends strongly on subject
```

The discussion must follow the data.

---

# 7. INTERPRETING CSP+LDA PERFORMANCE

If CSP+LDA performs strongly, possible interpretation:

- motor-imagery structure is sufficiently captured by spatial variance features;
- classical models remain competitive;
- lower complexity may be advantageous;
- deep learning is not automatically necessary.

If CSP+LDA performs poorly, investigate:

- preprocessing;
- covariance stability;
- subject variability;
- component selection;
- split design.

Do not assume the model itself is the only cause.

---

# 8. INTERPRETING EEGNET PERFORMANCE

If EEGNet performs strongly, discuss:

- learned spatial-temporal representations;
- compact neural architecture;
- probability quality;
- cross-subject consistency.

If EEGNet performs weakly, consider:

- limited data;
- hyperparameter sensitivity;
- subject variability;
- overfitting;
- preprocessing mismatch.

Do not automatically increase model complexity.

---

# 9. MODEL SELECTION FINDING

The final model selected for downstream integration should be justified using more than accuracy.

Consider:

```text
balanced accuracy
F1
probability calibration
stability
cross-subject behavior
computational simplicity
```

Final finding template:

> **The downstream decoder was selected because [TBD].**

---

# 10. FINDING 2 — PROBABILITY CALIBRATION

The calibration discussion should answer:

1. Were raw probabilities overconfident or underconfident?
2. Did calibration reduce ECE?
3. Did calibration improve Brier Score?
4. Did classification accuracy remain unchanged?
5. Did calibration improve downstream Bayesian behavior?

---

# 11. CALIBRATION INTERPRETATION

A strong calibration finding might be:

> The classifier’s discrimination performance changed little, but its probability estimates became more consistent with observed correctness.

This is more meaningful for this project than simply improving class labels because downstream Bayes and uncertainty depend on probabilities.

---

# 12. CALIBRATION FAILURE FINDING

Calibration may:

```text
improve ECE
but worsen Brier
```

or:

```text
help one model
but not another
```

or:

```text
provide negligible benefit
```

These are valid outcomes.

Do not force calibration into the final system if evidence shows no meaningful benefit.

---

# 13. FINDING 3 — BAYESIAN GOAL INFERENCE

The Bayesian discussion should focus on:

- sequential evidence integration;
- posterior stability;
- wrong-goal recovery;
- confidence accumulation;
- latency.

Core question:

> **Did sequential belief updating improve goal-level decision reliability relative to single-observation control?**

---

# 14. BAYESIAN POSITIVE FINDING

If Bayesian accumulation reduces wrong-goal decisions:

Possible explanation:

- isolated noisy decoder outputs are smoothed by sequential evidence;
- belief does not react as strongly to a single transient mistake;
- repeated consistent evidence increases confidence.

This should be demonstrated using posterior trajectories.

---

# 15. BAYESIAN TRADE-OFF

The likely central trade-off to evaluate is:

```text
more evidence accumulation
→ potentially better stability
→ potentially greater decision latency
```

The final discussion must quantify both sides.

---

# 16. BAYESIAN FAILURE FINDING

Important negative outcomes include:

```text
early wrong evidence dominates posterior
posterior becomes confidently wrong
correlated evidence creates overconfidence
Bayes adds latency without meaningful reliability gain
```

These must be discussed explicitly if observed.

---

# 17. BAYESIAN RECOVERY

A valuable qualitative finding is whether the posterior can recover after misleading evidence.

Discuss:

- number of observations required;
- whether recovery occurred before commitment;
- effect of prior;
- effect of calibration.

---

# 18. FINDING 4 — UNCERTAINTY

The uncertainty discussion must distinguish:

```text
uncertainty as a numerical quantity
```

from:

```text
uncertainty changing system behavior
```

The project only deserves the term **uncertainty-aware** if behavior changes.

---

# 19. ENTROPY FINDING

Analyze whether entropy behaved sensibly:

```text
ambiguous posterior → higher entropy
concentrated posterior → lower entropy
```

Then test whether:

```text
wrong decisions
```

were associated with unusually low or high entropy.

---

# 20. CONFIDENTLY WRONG FAILURE

A major failure case is:

```text
wrong goal
+
low entropy
```

This is dangerous because the system is confident but incorrect.

If observed, discuss:

- decoder overconfidence;
- calibration limits;
- correlated evidence;
- likelihood-model limitations;
- threshold sensitivity.

---

# 21. FINDING 5 — SHARED AUTONOMY

The shared-autonomy discussion should answer:

1. Did uncertainty gating reduce premature commitment?
2. How often did the system ask for confirmation?
3. How often did it defer?
4. How often did human override occur?
5. Did intervention burden become excessive?
6. Did safety improve at the cost of speed?

---

# 22. SHARED-AUTONOMY SUCCESS

A useful success pattern would be:

```text
lower wrong-goal commitment
+
manageable confirmation burden
+
acceptable latency
```

This would support the core architecture.

But all three dimensions matter.

---

# 23. OVER-CONSERVATIVE SYSTEM

A system may appear safe by:

```text
constantly deferring
constantly asking confirmation
rarely acting autonomously
```

This must not be interpreted as strong shared autonomy.

Discuss whether the system became too conservative.

---

# 24. OVER-PERMISSIVE SYSTEM

The opposite failure is:

```text
too many automatic proceeds
too few confirmations
high wrong-goal commitment
```

This suggests thresholds/policy may be too permissive.

---

# 25. HUMAN-AUTONOMY BALANCE

The final discussion should analyze:

```text
autonomy
vs
human control burden
vs
wrong-goal risk
```

The goal is **appropriate autonomy**, not maximum autonomy.

---

# 26. FINDING 6 — PLANNING

Planning discussion should answer:

- Did A* reliably find valid routes?
- Did replanning work after path blockage?
- Did risk-aware cost change route choice?
- What was the path-length/risk trade-off?
- Were no-path cases handled correctly?

---

# 27. PLANNING IS NOT THE MAIN NOVELTY

If A* performs correctly, the correct discussion is:

> A* provided a reliable and interpretable navigation layer.

Do not overstate it as a novel path-planning contribution.

---

# 28. RISK-AWARE PLANNING FINDING

If increasing \(\lambda\) reduces risk exposure while increasing path length:

Discuss this as an interpretable trade-off.

Do not say:

> “The planner found the safest route”

unless the risk model mathematically supports that claim.

---

# 29. FINDING 7 — SAFETY

Safety discussion should focus on explicit tested constraints.

Examples:

```text
blocked-cell rejection
out-of-bounds rejection
pause enforcement
emergency stop
prohibited-hazard rejection
```

---

# 30. SAFETY SUCCESS

If all tested hard constraints are enforced:

Correct interpretation:

> The safety controller successfully enforced the specified simulated safety constraints.

Do not escalate this into a real-world safety claim.

---

# 31. SAFETY INTERVENTION ANALYSIS

Discuss:

```text
how often the planner proposed unsafe actions
how often safety intervened
how often replanning was required
whether intervention harmed task completion
```

High safety intervention count may indicate either:

- useful protection;
- weak planner/risk policy.

Interpret carefully.

---

# 32. FINDING 8 — A/B/C/D SYSTEM COMPARISON

The principal discussion should compare:

```text
A — Direct EEG
B — Confidence-aware
C — Bayesian shared autonomy
D — Full system
```

The key question is how each additional layer affects downstream behavior.

---

# 33. SYSTEM A — DIRECT EEG

Interpret System A as the simplest baseline.

Questions:

- How often did direct decoder errors become wrong decisions?
- Was it fast?
- Was it unstable?
- How often did it create downstream failure?

Do not intentionally weaken System A.

---

# 34. SYSTEM B — CONFIDENCE-AWARE

Key question:

> Does adding confidence/uncertainty gating improve direct control without Bayesian accumulation?

Possible finding:

```text
wrong commitments ↓
deferrals ↑
latency ↑
```

---

# 35. SYSTEM C — BAYESIAN SHARED AUTONOMY

Key question:

> Does sequential belief accumulation improve goal reliability and navigation decisions?

Possible trade-offs:

```text
goal accuracy ↑
latency ↑
human interventions ↓ or ↑
```

Actual results must determine the conclusion.

---

# 36. SYSTEM D — FULL SYSTEM

System D combines the approved full architecture.

Do not call it “best” automatically.

It may be:

- best overall;
- best on safety but slower;
- best on reliability but more intervention-heavy;
- only marginally better;
- worse on some metrics.

---

# 37. SYSTEM-LEVEL TRADE-OFF TABLE

Final discussion should synthesize:

| System | Reliability | Latency | Human Burden | Safety | Task Performance |
|---|---|---|---|---|---|
| A | TBD | TBD | TBD | TBD | TBD |
| B | TBD | TBD | TBD | TBD | TBD |
| C | TBD | TBD | TBD | TBD | TBD |
| D | TBD | TBD | TBD | TBD | TBD |

Use descriptive interpretation in addition to numbers.

---

# 38. MAIN SYSTEM FINDING TEMPLATE

> **Compared with direct EEG control, the uncertainty-aware shared-autonomy architecture [TBD], while introducing [TBD trade-off].**

Do not finalize until valid results exist.

---

# 39. FINDING 9 — ABLATIONS

Ablations should help answer:

```text
Which component actually contributed?
```

Examples:

```text
Full - calibration
Full - Bayes
Full - uncertainty
Full - safety
Full - adaptation
```

---

# 40. ABLATION INTERPRETATION

If removing a component changes little:

Possible interpretations:

- component adds limited value;
- metric insensitive;
- implementation weak;
- dataset insufficient;
- interaction effects.

Do not automatically conclude the component is useless.

---

# 41. COMPONENT INTERACTIONS

Some components may only help when paired.

Example:

```text
calibration
may matter mainly because
Bayesian inference consumes probabilities
```

Therefore a one-component ablation may reveal interaction effects.

---

# 42. FINDING 10 — ROBUSTNESS

Robustness discussion should analyze degradation under:

- noisier evidence;
- probability perturbation;
- contradictory evidence;
- environmental hazards;
- blocked paths.

---

# 43. GRACEFUL DEGRADATION

A central robustness question:

> Does the system fail gradually and visibly, or suddenly and confidently?

A good uncertainty-aware system should ideally:

```text
uncertainty ↑
deferral ↑
wrong automatic commitment ↓
```

as evidence quality decreases.

This remains a hypothesis.

---

# 44. ROBUSTNESS FAILURE

Poor robustness may appear as:

```text
entropy fails to increase
wrong commitments remain high
Bayes becomes confidently wrong
system becomes unusably conservative
```

These results are important.

---

# 45. FINDING 11 — CROSS-SUBJECT GENERALIZATION

Cross-subject findings should discuss:

- mean performance;
- variance;
- difficult subjects;
- generalization gap;
- calibration shift.

Do not hide subject heterogeneity inside one average.

---

# 46. GENERALIZATION GAP

Compare where appropriate:

```text
within-subject performance
vs
cross-subject performance
```

If performance drops substantially, discuss:

- inter-subject EEG variability;
- personalization need;
- calibration/generalization challenge.

---

# 47. FINDING 12 — ADAPTATION

Only discuss adaptation if a real approved mechanism is implemented.

Questions:

- Did personalization help?
- For which subjects?
- Did it reduce interventions?
- Did it cause instability?
- Did it overfit?

---

# 48. ADAPTATION TRADE-OFF

Possible valid result:

```text
adaptation helps some subjects
but harms others
```

This is scientifically interesting.

Do not average it away without subject-level analysis.

---

# 49. FAILURE ANALYSIS

Failure analysis is mandatory.

The final discussion should include representative failures from each layer.

---

# 50. EEG FAILURE

Possible:

```text
wrong high-confidence class
ambiguous probability
subject-specific failure
```

Trace downstream consequences.

---

# 51. CALIBRATION FAILURE

Possible:

```text
confidence remains overconfident
calibration helps aggregate ECE but fails on specific subject
```

Discuss distribution shift.

---

# 52. BAYESIAN FAILURE

Possible:

```text
wrong early evidence causes posterior lock-in
recovery too slow
```

Discuss sequence assumptions and commitment policy.

---

# 53. SHARED-AUTONOMY FAILURE

Possible:

```text
too many confirmations
premature proceed
stale confirmation
override timing issue
```

---

# 54. PLANNING FAILURE

Possible:

```text
no path
risk policy chooses inefficient route
replanning repeatedly fails
```

---

# 55. SAFETY FAILURE

Any executed hard-constraint violation is a major implementation finding.

It should trigger:

```text
debugging
experiment invalidation if necessary
retesting
```

Do not present known safety-control bugs as acceptable final behavior.

---

# 56. END-TO-END FAILURE TRACE

Use:

```text
EEG
→ decoder
→ calibration
→ goal evidence
→ posterior
→ entropy
→ autonomy
→ goal approval
→ planner
→ safety
→ outcome
```

This trace should identify the earliest meaningful failure point.

---

# 57. FAILURE RECOVERABILITY

Classify failures where useful as:

```text
recoverable
non-recoverable
prevented by human intervention
prevented by safety
```

This helps characterize system resilience.

---

# 58. TRADE-OFF 1 — RELIABILITY VS LATENCY

More evidence accumulation and confirmation may improve reliability but delay action.

This is expected to be one of the most important system trade-offs.

---

# 59. TRADE-OFF 2 — AUTONOMY VS HUMAN BURDEN

More aggressive autonomy may reduce human interaction but increase wrong decisions.

More conservative autonomy may reduce errors but require more confirmation.

The final discussion should quantify this balance.

---

# 60. TRADE-OFF 3 — SAFETY VS EFFICIENCY

Risk-aware planning and safety constraints may:

```text
increase path length
increase completion time
reduce simulated hazard exposure
```

This is a meaningful trade-off, not automatically a weakness.

---

# 61. TRADE-OFF 4 — MODEL COMPLEXITY VS PERFORMANCE

EEGNet may provide better decoding or calibration.

If the gain is small, CSP+LDA may remain attractive because of:

- simplicity;
- interpretability;
- lower training complexity.

---

# 62. TRADE-OFF 5 — PERSONALIZATION VS GENERALIZATION

Adaptation may improve one user while reducing generality.

Discuss whether the final system is:

```text
general
personalized
or hybrid
```

based on actual implementation.

---

# 63. RELATION TO MOTOR-IMAGERY BCI LITERATURE

Compare final EEG findings against the literature carefully.

Appropriate interpretation:

> The observed subject variability is consistent with known challenges in motor-imagery BCI.

Avoid claiming exact numerical superiority over published systems unless protocols are directly comparable.

---

# 64. RELATION TO CSP / EEGNET LITERATURE

Discuss whether the project confirms the practical usefulness of:

```text
classical spatial filtering
compact neural decoding
```

under this dataset/protocol.

Do not overgeneralize beyond the evaluated data.

---

# 65. RELATION TO CALIBRATION LITERATURE

If raw neural probabilities are overconfident, this would align with broader neural-network calibration literature.

If calibration improves reliability, connect this to the need for reliable confidence in downstream decision systems.

---

# 66. RELATION TO SHARED-AUTONOMY LITERATURE

If goal-level probabilistic assistance improves reliability, relate it to shared-autonomy research that models uncertain user goals.

The project's specific contribution remains the use of EEG-derived evidence in this architecture.

---

# 67. RELATION TO BCI SHARED CONTROL

If the shared-autonomy layer reduces consequences of noisy BCI predictions, this supports the broader BCI-shared-control principle that low-bandwidth/noisy neural commands can benefit from autonomous assistance.

---

# 68. RELATION TO ADAPTIVE BCI

If personalization helps, discuss it as system-side adaptation consistent with adaptive BCI motivation.

Do not claim full human-machine co-adaptation because the EEG is prerecorded.

---

# 69. SCIENTIFIC CONTRIBUTION

The project should not claim invention of:

```text
CSP
LDA
EEGNet
Bayesian inference
entropy
A*
shared autonomy
```

The contribution is the disciplined integration and evaluation of these components around the central system question.

---

# 70. POTENTIAL CONTRIBUTION STATEMENT

Final template:

> **The project contributes an experimentally structured software framework that integrates motor-imagery EEG decoding, probability calibration, Bayesian latent-goal inference, uncertainty-aware shared autonomy, autonomous planning, and explicit simulated safety control within a reproducible Search & Rescue environment.**

This is an architectural contribution.

Performance claims must be added only after evidence exists.

---

# 71. PRACTICAL SIGNIFICANCE

Practical significance should be judged by:

- reliability improvement;
- reduced wrong-goal commitment;
- manageable intervention burden;
- robust behavior under noisy evidence;
- safety constraint enforcement.

Do not equate statistical significance with practical usefulness.

---

# 72. LIMITATIONS TO REVISIT IN DISCUSSION

The final discussion must explicitly revisit:

```text
offline prerecorded EEG
binary motor imagery
public-dataset/task mismatch
subject variability
goal-mapping abstraction
Bayesian likelihood assumptions
simplified uncertainty
simple 2D simulation
simulated safety
no human-subject study
no physical robot
```

---

# 73. LIMITATION IMPACT

Do more than list limitations.

Explain how each may affect interpretation.

Example:

> Because EEG was prerecorded, the evaluation cannot capture feedback-driven changes in user behavior during live shared control.

---

# 74. INTERNAL VALIDITY DISCUSSION

Discuss:

- leakage prevention;
- fair baselines;
- fixed configurations;
- ablations;
- test-set protection.

If any compromise occurred, state it.

---

# 75. CONSTRUCT VALIDITY DISCUSSION

Clarify operational meanings:

```text
intent = constrained BCI control objective
uncertainty = posterior entropy
safety = explicit simulated constraint enforcement
cognition = computational latent-intent belief process
```

---

# 76. EXTERNAL VALIDITY DISCUSSION

State clearly that findings may not transfer directly to:

- other datasets;
- live EEG;
- clinical users;
- physical robots;
- real disaster environments.

---

# 77. REPRODUCIBILITY DISCUSSION

Discuss whether final results were reproducible from:

```text
Git commit
config
split
seed
model
artifacts
```

Any deviations should be disclosed.

---

# 78. HYPOTHESIS DISCUSSION

For each hypothesis from the research-question document, assign:

```text
SUPPORTED
PARTIALLY SUPPORTED
NOT SUPPORTED
INCONCLUSIVE
```

Then justify using actual experiments.

---

# 79. FINDINGS SUMMARY TABLE

Final template:

| Finding ID | Finding | Supporting Experiment | Evidence | Interpretation |
|---|---|---|---|---|
| F1 | TBD | TBD | TBD | TBD |
| F2 | TBD | TBD | TBD | TBD |
| F3 | TBD | TBD | TBD | TBD |
| F4 | TBD | TBD | TBD | TBD |

Do not fill until real findings exist.

---

# 80. STRONG FINDING REQUIREMENT

A strong finding should have:

```text
clear question
controlled experiment
appropriate metric
reproducible evidence
reasonable interpretation
stated limitation
```

---

# 81. FINDINGS THAT SHOULD NOT BE CLAIMED

Do not claim:

```text
the system understands human thought
the system is clinically validated
the system is real-time
the system guarantees safety
the system is ready for rescue deployment
the Bayesian model represents human cognition
```

---

# 82. DISCUSSION WRITING STYLE

Use precise scientific wording.

Prefer:

```text
suggests
indicates
under the evaluated conditions
was associated with
reduced measured simulated violations
```

Avoid:

```text
proves
guarantees
understands
always
perfect
```

unless mathematically and experimentally justified.

---

# 83. RESULTS VS DISCUSSION BOUNDARY

`23_RESULTS_AND_ANALYSIS.md` should primarily answer:

```text
WHAT happened?
```

This document should answer:

```text
WHAT does it mean?
WHY might it have happened?
WHAT are the trade-offs?
HOW does it relate to the research question?
```

Do not duplicate every table unnecessarily.

---

# 84. DISCUSSION OF NULL RESULTS

If a component shows no measurable benefit:

Discuss possibilities such as:

- already strong baseline;
- weak signal;
- insufficient sample;
- poor parameterization;
- metric mismatch;
- component truly adds little value.

Do not automatically attribute null results to experimental failure.

---

# 85. DISCUSSION OF UNEXPECTED RESULTS

Unexpected findings should be investigated before interpretation.

Procedure:

```text
verify experiment validity
→ inspect logs
→ reproduce
→ confirm result
→ then interpret
```

Do not build a narrative around a potentially invalid run.

---

# 86. DISCUSSION OF OUTLIERS

Subject-level outliers should be:

- retained;
- inspected;
- reported;
- explained cautiously.

Do not remove difficult subjects merely to improve average performance.

---

# 87. DISCUSSION OF STATISTICAL SIGNIFICANCE

If inferential statistics are used:

Do not write:

> “X is important because p < 0.05.”

Discuss:

- effect magnitude;
- confidence interval;
- practical significance;
- sample structure.

---

# 88. DISCUSSION OF SYSTEM D

If System D performs best overall, explain which components appear to contribute using ablations.

If System D does not perform best, discuss:

- whether complexity is justified;
- which simpler system is competitive;
- where full architecture may still offer qualitative advantages.

---

# 89. DISCUSSION OF SCIENTIFIC VALUE EVEN IF FULL SYSTEM DOES NOT WIN

The project remains scientifically useful if it reveals:

- where uncertainty handling helps;
- where it does not;
- how EEG errors propagate;
- how safety intercepts failures;
- what trade-offs shared autonomy creates.

The value is in understanding the system, not forcing a predetermined winner.

---

# 90. FINAL ANSWER TO PRIMARY RESEARCH QUESTION

Final template:

> **Under the evaluated offline EEG and simulated Search & Rescue conditions, uncertainty-aware shared autonomy [TBD: improved / partially improved / did not improve / produced mixed effects on] the reliability and safety of EEG-based intent control compared with direct control. The principal observed benefits were [TBD], while the main costs or limitations were [TBD].**

This sentence must not be completed until valid experiments exist.

---

# 91. CONCLUSION DISCIPLINE

The final conclusion should be narrower than the evidence.

If the experiment demonstrates:

```text
lower wrong-goal commitment in a 2D simulation
```

do not conclude:

```text
reliable real-world BCI autonomy
```

---

# 92. DISCUSSION ARTIFACT REQUIREMENTS

For each major discussed finding preserve:

```text
experiment ID
table/figure
raw artifact
metric definition
configuration
Git commit
```

Discussion statements should remain traceable.

---

# 93. CURRENT FINDINGS STATUS

At the time this document is generated:

```text
Confirmed empirical findings:
NONE YET

EEG findings:
PENDING

Calibration findings:
PENDING

Bayesian findings:
PENDING

Uncertainty findings:
PENDING

Shared-autonomy findings:
PENDING

Planning findings:
PENDING

Safety findings:
PENDING

A/B/C/D findings:
PENDING

Robustness findings:
PENDING

Cross-subject findings:
PENDING

Adaptation findings:
PENDING
```

No empirical finding is authorized until experiments are executed.

---

# 94. COMPLETION CRITERIA

This document becomes the final Discussion & Findings document only when:

1. valid experimental results exist;
2. the main research question is answered;
3. all major hypotheses are evaluated;
4. A/B/C/D findings are interpreted;
5. ablations are analyzed;
6. trade-offs are explained;
7. failure cases are included;
8. literature connections are accurate;
9. limitations are incorporated;
10. every major finding is traceable to evidence;
11. no unsupported claims remain;
12. no placeholder `TBD` remains in final findings sections.

---

# 95. CURRENT DISCUSSION SUMMARY

The project's discussion framework is designed to interpret the complete evidence chain rather than isolated model scores. Final findings must explain how EEG decoding quality affects probability reliability, how calibrated evidence affects sequential Bayesian belief, how posterior uncertainty changes shared-autonomy behavior, how goal approval affects planning, how safety intercepts invalid actions, and how all of these factors influence mission-level outcomes. The analysis must explicitly report trade-offs such as reliability versus latency, autonomy versus human intervention, and safety versus navigation efficiency. Negative results, difficult subjects, overconfident errors, excessive deferral, no-path cases, and adaptation failures are all valid findings and must remain visible. The strongest final contribution will come from understanding when uncertainty-aware shared autonomy helps, when it does not, and why—rather than simply declaring the full system superior.
