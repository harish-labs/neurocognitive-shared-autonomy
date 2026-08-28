# 18_METRICS_AND_EVALUATION.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Metrics, Mathematical Definitions, Aggregation Rules, Statistical Reporting, and Evaluation Framework

**Document ID:** I-02  
**Document class:** Experiments & Evaluation / Metrics Specification  
**Authority level:** Subordinate to all Master Authority, Scenario, Architecture, Data, Neuroscience, ML, Bayesian, Shared-Autonomy, Planning, Safety, Implementation, Repository, and Experimental Design documents  
**Status:** Authoritative metrics baseline; any still-unapproved metric formulation remains explicitly unresolved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND METRIC-INTEGRITY RULE

This document defines **what the project measures, how each metric is calculated, how results are aggregated, and how metrics should be interpreted**.

It must remain consistent with all previously approved project documents, especially:

- `17_EXPERIMENTAL_DESIGN.md`
- `08_EEG_SIGNAL_PROCESSING_AND_ML.md`
- `09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md`
- `10_BAYESIAN_GOAL_INFERENCE.md`
- `12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`
- `13_AUTONOMOUS_PLANNING_AND_CONTROL.md`
- `14_SAFETY_CRITICAL_CONTROL.md`

If this document conflicts with a higher-authority document, the higher-authority document wins.

The central evaluation rule is:

> **A metric is meaningful only if its denominator, averaging method, evaluation unit, and experimental condition are explicit.**

Do not report numbers without defining what they measure.

---

# 1. PURPOSE OF THIS DOCUMENT

This document defines metrics for five levels of the system:

```text
Level 1 — EEG decoding
Level 2 — Probability calibration
Level 3 — Bayesian goal inference / uncertainty
Level 4 — Shared autonomy / human interaction
Level 5 — Planning / safety / full-system task performance
```

The project must keep these levels separate.

A good EEG metric does not automatically imply a good autonomous-system outcome.

---

# 2. METRIC GROUPS

The project uses the following metric groups:

```text
M1 — EEG classification metrics
M2 — Calibration metrics
M3 — Bayesian / uncertainty metrics
M4 — Shared-autonomy / human-interaction metrics
M5 — Planning metrics
M6 — Safety metrics
M7 — Full-system task metrics
M8 — Cross-subject / robustness aggregation
M9 — Adaptation metrics, if implemented
```

---

# 3. EVALUATION UNIT

Before calculating any metric, define the evaluation unit.

Possible units include:

```text
EEG trial
subject
fold
evidence sequence
goal-selection episode
navigation episode
full system episode
random seed
```

Metrics must not mix these units without explanation.

---

# 4. M1 — EEG CLASSIFICATION METRICS

The approved core EEG metrics are:

- accuracy;
- balanced accuracy;
- precision;
- recall;
- F1;
- confusion matrix.

Optional:

- ROC-AUC if later justified.

---

# 5. ACCURACY

For \(N\) evaluated EEG trials:

\[
Accuracy
=
\frac{\text{Number of correct predictions}}{N}
\]

For the binary Left-vs-Right task:

```text
correct Left
+
correct Right
```

divided by total evaluated trials.

Accuracy should not be the only reported EEG metric.

---

# 6. BALANCED ACCURACY

Balanced accuracy is:

\[
BalancedAccuracy
=
\frac{Recall_{Left}+Recall_{Right}}{2}
\]

For a binary problem, this gives equal importance to both classes.

It is useful if the number of Left and Right trials differs.

---

# 7. PRECISION

For a selected class:

\[
Precision
=
\frac{TP}{TP+FP}
\]

For example, treating Right as the positive class:

- \(TP\): Right correctly predicted as Right;
- \(FP\): Left incorrectly predicted as Right.

Precision should be reported with its class/averaging convention.

---

# 8. RECALL

\[
Recall
=
\frac{TP}{TP+FN}
\]

Recall is also called sensitivity for the selected positive class.

For multi-class-style aggregation of the binary task, report the averaging method.

---

# 9. F1 SCORE

\[
F1
=
2
\frac{Precision \times Recall}
{Precision+Recall}
\]

F1 balances precision and recall.

It is useful when class balance is imperfect.

---

# 10. PRECISION / RECALL / F1 AVERAGING

Possible aggregation conventions include:

- macro average;
- weighted average;
- per-class reporting.

The exact final reporting convention is **not yet locked**.

Recommended minimum:

```text
per-class values
+
macro F1
```

or another explicitly approved convention.

Do not report “F1” without stating the averaging strategy.

---

# 11. CONFUSION MATRIX

For the current task, class order must be explicit.

Recommended order:

```text
Left
Right
```

Conceptually:

| True \ Predicted | Left | Right |
|---|---:|---:|
| Left | measured | measured |
| Right | measured | measured |

The confusion matrix helps identify class-specific bias.

---

# 12. ROC-AUC — OPTIONAL

For binary classification, ROC-AUC may be calculated from probability scores.

Status:

> **Optional, not mandatory.**

Use only if:

- probability outputs are valid;
- its interpretation adds useful information.

Do not add ROC-AUC only to increase metric count.

---

# 13. M2 — CALIBRATION METRICS

Required calibration metrics:

- reliability diagram;
- Expected Calibration Error;
- Brier Score.

Optional:

- negative log-likelihood.

---

# 14. CONFIDENCE FOR CALIBRATION

For a prediction:

\[
confidence_i
=
\max_c p_i(c)
\]

This confidence is compared against correctness for reliability analysis.

Class-specific calibration may also be inspected if useful.

---

# 15. RELIABILITY DIAGRAM

Predictions are grouped into confidence bins.

For bin \(B_m\):

\[
conf(B_m)
=
\frac{1}{|B_m|}
\sum_{i\in B_m} confidence_i
\]

and:

\[
acc(B_m)
=
\frac{1}{|B_m|}
\sum_{i\in B_m}
\mathbf{1}(\hat{y}_i=y_i)
\]

A perfectly calibrated bin would satisfy approximately:

\[
acc(B_m)=conf(B_m)
\]

---

# 16. RELIABILITY BINNING — UNRESOLVED

Still unresolved:

- number of bins;
- equal-width vs equal-frequency/adaptive bins.

The final chosen binning rule must be fixed before reportable calibration comparisons.

---

# 17. EXPECTED CALIBRATION ERROR — ECE

A common ECE definition is:

\[
ECE
=
\sum_{m=1}^{M}
\frac{|B_m|}{N}
\left|
acc(B_m)-conf(B_m)
\right|
\]

Lower values indicate better calibration under the chosen binning procedure.

ECE must always be interpreted together with the binning definition.

---

# 18. BRIER SCORE

For a binary positive-class probability \(p_i\) and label \(y_i\in\{0,1\}\):

\[
Brier
=
\frac{1}{N}
\sum_{i=1}^{N}
(p_i-y_i)^2
\]

Lower is better.

The selected positive class must be documented.

If a multiclass formulation is ever used later, its exact definition must be separately documented.

---

# 19. NEGATIVE LOG-LIKELIHOOD — OPTIONAL

For the true label probability \(p_i(y_i)\):

\[
NLL
=
-\frac{1}{N}
\sum_i
\log p_i(y_i)
\]

NLL strongly penalizes confident wrong predictions.

Status:

> optional unless later approved.

---

# 20. RAW VS CALIBRATED REPORTING

Calibration evaluation should compare:

```text
Raw
vs
Calibrated
```

using the same held-out predictions.

Minimum report:

```text
ECE raw
ECE calibrated
Brier raw
Brier calibrated
```

A calibration method should not be called beneficial solely because one metric improves if another materially worsens.

---

# 21. M3 — BAYESIAN GOAL-INFERENCE METRICS

Core metrics include:

- goal inference accuracy;
- posterior confidence;
- entropy;
- decision latency;
- wrong-goal commitment;
- number of evidence updates;
- posterior trajectory.

---

# 22. GOAL INFERENCE ACCURACY

For controlled episodes with an evaluation-only true goal:

\[
GoalInferenceAccuracy
=
\frac{
\text{episodes where inferred/selected goal matches true goal}
}{
\text{evaluated episodes}
}
\]

The exact point of evaluation must be explicit:

- final posterior leader;
- committed goal;
- or both.

These are different.

---

# 23. FINAL POSTERIOR LEADER

At the end of an inference sequence:

\[
\hat{G}
=
\arg\max_g P(G=g\mid E_{1:T})
\]

This may be evaluated against the controlled true goal.

Do not confuse this with the actual committed goal if the shared-autonomy policy deferred or requested confirmation.

---

# 24. POSTERIOR CONFIDENCE

\[
C_t
=
\max_g P(G=g\mid E_{1:t})
\]

This measures the concentration of belief in the leading hypothesis.

It does not mean objective correctness.

---

# 25. ENTROPY

The approved initial uncertainty metric is:

\[
H(P_t)
=
-\sum_g P_t(g)\log P_t(g)
\]

Higher entropy generally means greater uncertainty.

Lower entropy means a more concentrated posterior.

---

# 26. NORMALIZED ENTROPY — OPTIONAL

For \(K\) hypotheses:

\[
H_{norm}(P)
=
\frac{H(P)}{\log K}
\]

Status:

> optional and still unresolved.

This is useful if \(K\) changes across experiments.

---

# 27. WRONG-GOAL COMMITMENT

A wrong-goal commitment occurs when:

```text
system commits/approves goal G
```

and:

```text
G != controlled true goal
```

Define:

\[
WrongGoalRate
=
\frac{
\text{wrong committed episodes}
}{
\text{episodes with goal commitment}
}
\]

An alternative denominator could use all evaluated episodes.

The final denominator convention is **not yet locked** and must be frozen before reporting.

---

# 28. DECISION LATENCY

Decision latency may be measured as:

```text
number of evidence updates
```

or:

```text
simulated replay time
```

until a goal reaches the approved decision state.

Recommended primary discrete form:

\[
DecisionLatencyUpdates
=
t_{decision}
\]

where \(t_{decision}\) is the number of evidence updates required.

If simulated time is also used, report it separately.

---

# 29. EVIDENCE-UPDATES-TO-COMMITMENT

For committed episodes:

```text
count of accepted EEG evidence updates
before commitment
```

This is useful for comparing:

- direct control;
- Bayesian accumulation;
- uncertainty-aware systems.

---

# 30. POSTERIOR-TRAJECTORY METRIC

For the true goal \(G^*\), preserve:

\[
P(G^*\mid E_{1:t})
\]

over time.

This is best treated as a trajectory/figure rather than reduced to one mandatory scalar.

---

# 31. POSTERIOR LEADER SWITCHES — OPTIONAL

Potential diagnostic:

```text
number of times the highest-probability goal changes
during one selection episode
```

Status:

> optional.

Useful for conflicting-evidence analysis.

---

# 32. M4 — SHARED-AUTONOMY / HUMAN-INTERACTION METRICS

Core measures include:

- confirmation count;
- override count;
- deferral count;
- pause count;
- stop count;
- human intervention count;
- autonomy state distribution;
- decision latency.

---

# 33. CONFIRMATION COUNT

For each episode:

```text
number of explicit confirmation requests/actions
```

Possible aggregate:

\[
MeanConfirmations
=
\frac{\sum_e confirmations_e}{N_{episodes}}
\]

---

# 34. CONFIRMATION RATE

A possible normalized metric:

\[
ConfirmationRate
=
\frac{
\text{episodes requiring confirmation}
}{
\text{evaluated episodes}
}
\]

or:

\[
\frac{\text{confirmation events}}{\text{selection events}}
\]

The final denominator must be explicitly selected.

---

# 35. OVERRIDE COUNT

Count:

```text
human override events
```

per episode and across experiments.

Overrides should be separated from:

- safety overrides.

---

# 36. DEFERRAL COUNT

A deferral occurs when the controller intentionally avoids commitment due to insufficient confidence/uncertainty.

Possible reporting:

- deferrals per episode;
- episodes containing at least one deferral;
- total defer states.

The final preferred formulation is not yet locked.

---

# 37. HUMAN INTERVENTION COUNT

Conceptually:

\[
HumanInterventions
=
Confirmations
+
Overrides
+
Pauses
+
Stops
\]

However, whether all these should be combined into one headline metric is unresolved.

Recommended:

> preserve individual counts even if an aggregate is also reported.

---

# 38. CONFIRMATION BURDEN

The project may use:

```text
confirmation burden
```

as a descriptive metric based on confirmation frequency.

It must not be called measured cognitive workload unless a real human-subject study is performed.

---

# 39. AUTONOMY STATE DISTRIBUTION

Potential diagnostic:

```text
percentage of time/decisions in:
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

Useful for understanding overly conservative or permissive policies.

---

# 40. M5 — PLANNING METRICS

Core planning measures may include:

- planning success;
- path length;
- movement cost;
- risk cost;
- total path cost;
- path efficiency;
- replanning count;
- planning runtime.

---

# 41. PLANNING SUCCESS

\[
PlanningSuccess
=
\frac{
\text{planning requests returning a valid path}
}{
\text{valid planning requests}
}
\]

Invalid-start/invalid-goal configuration errors should be reported separately rather than treated as ordinary planning failures unless the experiment explicitly includes them.

---

# 42. PATH LENGTH

For the approved 4-connected grid:

\[
PathLength
=
\text{number of movement steps from start to goal}
\]

The treatment of `WAIT` is unresolved.

Recommended:

```text
navigation path length excludes WAIT
```

while WAIT contributes to completion time/interaction latency.

This recommendation must still be approved before final reporting.

---

# 43. MOVEMENT COST

If each orthogonal move costs 1:

\[
MovementCost
=
\sum_{steps} 1
\]

If a different movement model is approved, update this definition.

---

# 44. RISK COST

Conceptually:

\[
RiskCost
=
\sum_{cell\in path} r(cell)
\]

or:

\[
\lambda
\sum_{cell\in path}r(cell)
\]

depending on whether the project wants to report:

- raw risk exposure;
- weighted planner risk contribution.

Recommended:

> report both separately if useful.

The final risk formulation remains unresolved until the hazard policy is approved.

---

# 45. TOTAL PATH COST

Under the approved conceptual model:

\[
J
=
MovementCost
+
\lambda \cdot RiskExposure
\]

The exact implementation depends on final risk semantics.

---

# 46. PATH EFFICIENCY — UNRESOLVED

Path efficiency has not yet been formally locked.

One candidate definition is:

\[
PathEfficiency
=
\frac{
ReferenceOptimalCost
}{
ActualPathCost
}
\]

which lies in \((0,1]\) when actual cost is no better than the reference optimum.

Another possibility is a distance-only efficiency ratio.

No final formula is approved.

This metric must remain unresolved until the final cost reference is selected.

---

# 47. REPLANNING COUNT

For each episode:

```text
number of times a new plan is generated after initial planning
```

Reasons should be preserved:

- blocked route;
- hazard change;
- safety rejection;
- goal change.

---

# 48. PLANNING RUNTIME

Measure wall-clock runtime for planning calls if useful.

Report hardware/environment context.

This is a secondary metric, not a central research outcome.

---

# 49. M6 — SAFETY METRICS

Core safety measures:

- unsafe action attempts;
- executed safety violations;
- hazard entries;
- safety overrides;
- emergency stops;
- no-safe-path events;
- replans caused by safety.

---

# 50. UNSAFE ACTION ATTEMPT

An unsafe action attempt is:

> a proposed action that would violate a hard safety rule if executed.

Count:

```text
UnsafeAttempts
```

per episode.

---

# 51. EXECUTED SAFETY VIOLATION

An executed safety violation is:

> a hard-constraint-violating action that actually reaches the environment.

Count:

```text
ExecutedViolations
```

This is one of the strongest safety metrics.

---

# 52. SAFETY VIOLATION RATE

Candidate definition:

\[
SafetyViolationRate
=
\frac{
ExecutedViolations
}{
TotalExecutedActions
}
\]

Alternative denominator:

```text
unsafe attempts
```

would answer a different question.

The final denominator is **not yet locked**.

Recommended reporting:

- raw count;
- denominator;
- normalized rate.

---

# 53. SAFETY OVERRIDE

Count each event where:

```text
planner proposes
→ safety rejects/modifies action
```

This is separate from human override.

---

# 54. SAFETY INTERVENTION RATE

Candidate:

\[
SafetyInterventionRate
=
\frac{
SafetyInterventions
}{
TotalProposedActions
}
\]

Status:

> candidate until final normalization policy is approved.

---

# 55. HAZARD ENTRY

Hazard entry must distinguish:

```text
allowed risk-zone entry
```

from:

```text
prohibited-hazard violation
```

These are not equivalent.

---

# 56. RISK EXPOSURE

If risk values are defined:

\[
RiskExposure
=
\sum_{visited\ cells} r(cell)
\]

The exact treatment of repeated visits or time spent in one cell remains to be frozen.

---

# 57. NO-SAFE-PATH EVENTS

Count episodes/requests where no route satisfying hard constraints exists.

This is not automatically a safety failure.

It may represent correct fail-safe behavior.

---

# 58. EMERGENCY-STOP SUCCESS

For tests where emergency stop is issued:

\[
EmergencyStopSuccess
=
\mathbf{1}(
\text{no movement after stop}
)
\]

Across multiple tests:

\[
EmergencyStopSuccessRate
=
\frac{\text{successful stop tests}}{\text{stop tests}}
\]

---

# 59. M7 — FULL-SYSTEM TASK METRICS

Core full-system metrics:

- task success;
- wrong-goal commitment;
- completion time;
- decision latency;
- path length;
- human interventions;
- safety violations.

---

# 60. TASK SUCCESS

The simplest episode-level definition is:

```text
correct intended goal approved
AND
agent reaches that goal
AND
episode does not terminate in failure
```

However, whether a soft-risk exposure affects success is unresolved.

Recommended core binary definition:

\[
TaskSuccess
=
\mathbf{1}(
correct\ goal\ reached
)
\]

with safety reported separately.

This avoids hiding unsafe behavior inside one combined metric.

---

# 61. TASK SUCCESS RATE

\[
TaskSuccessRate
=
\frac{
SuccessfulEpisodes
}{
EvaluatedEpisodes
}
\]

The episode inclusion criteria must be defined in each experiment.

---

# 62. COMPLETION TIME

Possible forms:

```text
environment steps
```

or:

```text
simulated replay/runtime time
```

Recommended:

- report environment steps for deterministic system comparison;
- optionally report simulated/real wall-clock time separately.

Exact final convention remains to be frozen.

---

# 63. TOTAL EPISODE STEPS

May include:

- movement actions;
- WAIT actions;
- evidence-acquisition steps.

The final definition must explicitly state which are included.

Do not use “completion time” if the metric is actually just movement count.

---

# 64. END-TO-END DECISION LATENCY

Possible:

```text
from first EEG evidence
to approved goal
```

This is distinct from:

```text
navigation completion time
```

Both may be reported.

---

# 65. SYSTEM UTILITY — NOT CURRENTLY LOCKED

The project could theoretically create one composite score combining:

- success;
- safety;
- latency;
- interventions.

No such composite utility is currently approved.

Recommended:

> report interpretable metrics separately rather than hiding trade-offs inside one arbitrary score.

---

# 66. M8 — CROSS-SUBJECT AGGREGATION

Cross-subject results must preserve individual-subject performance.

Recommended outputs:

```text
subject metric
mean
standard deviation
median optionally
range / distribution plot
```

The exact final summary statistics are not yet locked.

---

# 67. MACRO SUBJECT AVERAGE

For \(S\) subjects:

\[
MacroSubjectMean
=
\frac{1}{S}
\sum_{s=1}^{S}
metric_s
\]

This gives each subject equal weight.

This is often preferable when subject trial counts differ.

---

# 68. POOLED TRIAL METRIC

Alternatively, all trials may be pooled before computing a metric.

This weights subjects with more trials more heavily.

Therefore:

```text
macro subject average
```

and:

```text
pooled-trial metric
```

answer different questions.

Recommended:

> preserve subject-wise metrics and report macro aggregation as the primary cross-subject summary unless later decided otherwise.

---

# 69. STANDARD DEVIATION

For subject-wise or seed-wise metrics, standard deviation may summarize variability.

Use the appropriate sample/population convention consistently.

Exact reporting format can be standardized later.

---

# 70. MEDIAN / IQR — OPTIONAL

For skewed subject-level results, median and interquartile range may be useful.

Status:

> optional.

Do not add automatically unless they improve interpretation.

---

# 71. FOLD AGGREGATION

For K-fold or grouped cross-validation:

- compute metrics per fold;
- preserve fold IDs;
- aggregate only after all folds are valid.

Do not average a mix of development and final folds.

---

# 72. SEED AGGREGATION

If multiple random seeds are used:

```text
metric per seed
```

must be preserved.

Recommended final reporting:

```text
mean ± standard deviation
```

or another explicitly chosen summary.

Do not report only the best seed.

---

# 73. M9 — ADAPTATION METRICS

Only applicable if a concrete adaptation mechanism is implemented.

Potential measures:

- pre-adaptation wrong-goal rate;
- post-adaptation wrong-goal rate;
- confirmation rate;
- decision latency;
- parameter change;
- number of adaptation updates;
- subject-specific benefit/harm.

---

# 74. ADAPTATION IMPROVEMENT

A possible paired difference:

\[
\Delta metric
=
metric_{after}
-
metric_{before}
\]

Interpretation depends on the metric.

Example:

```text
negative Δ wrong-goal rate
```

would indicate improvement.

The exact adaptation comparison protocol remains unresolved.

---

# 75. ADAPTATION STABILITY

Potential diagnostics:

- number of parameter updates;
- parameter range;
- oscillation;
- bound hits.

These help identify unstable adaptation.

---

# 76. ROBUSTNESS METRICS

Across degradation/noise levels, track:

```text
EEG accuracy
ECE
Brier
entropy
wrong-goal rate
deferrals
decision latency
task success
safety violations
```

The goal is to measure degradation, not only performance at one noise level.

---

# 77. ROBUSTNESS SLOPE — OPTIONAL

A possible summary could estimate:

```text
change in metric per unit noise severity
```

Status:

> optional and dependent on the final noise model.

Not currently required.

---

# 78. ABLATION REPORTING

For each ablation:

```text
Full
vs
Full - component
```

report the same core metric set where meaningful.

Potential differences:

\[
\Delta M
=
M_{full}
-
M_{ablation}
\]

Interpretation depends on whether higher or lower values are better.

---

# 79. METRIC DIRECTION TABLE

| Metric | Better Direction |
|---|---|
| Accuracy | Higher |
| Balanced Accuracy | Higher |
| F1 | Higher |
| ECE | Lower |
| Brier Score | Lower |
| Wrong-goal rate | Lower |
| Entropy | Context-dependent |
| Decision latency | Usually lower, but trade-off |
| Confirmation count | Usually lower, but trade-off |
| Task success | Higher |
| Path length | Lower when comparable |
| Risk exposure | Lower |
| Unsafe attempts | Lower |
| Executed violations | Lower |
| Safety overrides | Context-dependent |
| Replanning count | Context-dependent |

Some metrics do not have a universally “better” direction.

---

# 80. ENTROPY INTERPRETATION

Lower entropy is not automatically better.

Example:

```text
low entropy + wrong goal
```

is dangerous overconfidence.

Therefore entropy must be interpreted with:

- correctness;
- calibration;
- commitment outcome.

---

# 81. CONFIRMATION INTERPRETATION

Fewer confirmations are not automatically better.

Example:

```text
zero confirmations
+
many wrong commitments
```

is poor performance.

Confirmation must be interpreted with:

- wrong-goal rate;
- latency;
- task success.

---

# 82. SAFETY OVERRIDE INTERPRETATION

More safety overrides can mean:

- stronger protection;
- poor planner behavior;
- overly restrictive policy.

Therefore count and context both matter.

---

# 83. PATH LENGTH INTERPRETATION

A longer route may be preferable if it reduces simulated risk.

Therefore compare:

```text
path length
risk exposure
total cost
```

together.

---

# 84. FULL-SYSTEM REPORTING SHOULD SHOW TRADE-OFFS

The project should not compress all results into:

```text
System D = best
```

Instead show trade-offs such as:

```text
lower wrong-goal rate
higher decision latency
more confirmations
lower safety violations
```

This is more scientifically credible.

---

# 85. STATISTICAL REPORTING

At minimum, report:

- sample count;
- evaluation unit;
- mean/median as appropriate;
- variability;
- subject-wise/fold-wise/seed-wise results where relevant.

Statistical significance testing remains optional until explicitly approved.

---

# 86. EFFECT SIZE — OPTIONAL

If formal statistical comparison is added, effect size should be considered.

Exact effect-size metric depends on:

- paired vs unpaired design;
- metric distribution;
- sample structure.

No effect-size method is currently locked.

---

# 87. CONFIDENCE INTERVALS — OPTIONAL

Confidence intervals may be useful for:

- subject-level averages;
- seed averages.

Method remains unresolved.

No bootstrap procedure is currently approved.

---

# 88. P-VALUE RULE

If hypothesis tests are later used:

- state test;
- state assumptions;
- report exact p-value;
- do not use p-value as the only evidence;
- consider effect magnitude.

---

# 89. MULTIPLE COMPARISONS

If many tests are run, a multiple-comparison correction may become necessary.

No correction method is currently locked.

---

# 90. METRIC IMPLEMENTATION FILES

Primary files:

```text
src/evaluation/eeg_metrics.py
src/evaluation/autonomy_metrics.py
```

Calibration metrics may also be placed in a dedicated helper if required.

---

# 91. EEG METRICS FILE RESPONSIBILITY

`eeg_metrics.py` should own:

- classification metrics;
- confusion matrix;
- ECE;
- Brier;
- reliability-bin computation.

It should not know about:

- A*;
- safety;
- human interaction.

---

# 92. AUTONOMY METRICS FILE RESPONSIBILITY

`autonomy_metrics.py` should own:

- goal inference outcomes;
- decision latency;
- intervention counts;
- task success;
- path metrics;
- safety metrics.

It must use structured logs rather than UI state.

---

# 93. METRIC TESTS

Every metric function should have small deterministic tests.

Examples:

## Accuracy

Known labels/predictions.

## F1

Known confusion counts.

## ECE

Known confidence bins.

## Brier

Analytically checkable probabilities.

## Entropy

Uniform and concentrated distributions.

## Task success

Synthetic episode record.

## Safety violations

Synthetic action log.

---

# 94. NO MANUAL METRIC CALCULATION FOR FINAL RESULTS

Spreadsheets may be used for inspection.

Final reportable metrics should come from reproducible code.

---

# 95. MACHINE-READABLE RESULT TABLES

Every summary table shown in the final report should ideally come from:

```text
CSV / JSON
```

saved by the evaluation pipeline.

---

# 96. METRIC NAMING

Use consistent names.

Example:

```text
balanced_accuracy
brier_score
wrong_goal_rate
decision_latency_updates
task_success_rate
unsafe_action_attempts
executed_safety_violations
```

Avoid changing names across experiments.

---

# 97. DENOMINATOR LOGGING

Any normalized rate must preserve its denominator.

Example:

```text
wrong_goal_count = 4
committed_episodes = 50
wrong_goal_rate = 0.08
```

This prevents misleading rates.

---

# 98. INVALID / MISSING CASES

If a metric is undefined:

- return/report `NA` or equivalent;
- explain why.

Example:

```text
precision denominator = 0
```

Do not silently convert every undefined value to zero.

---

# 99. EXCLUDED EPISODES

If episodes are excluded from a metric:

- record exclusion count;
- record reason;
- preserve original experiment record.

Do not silently remove difficult episodes.

---

# 100. METRIC VERSIONING

If a metric definition changes during development:

```text
metric_version
```

or the corresponding code/config/Git commit must make the change traceable.

Do not compare results calculated under different formulas without noting the difference.

---

# 101. REPORTING PRECISION

Use consistent decimal precision in final tables.

Do not imply more precision than the experiment supports.

Example:

```text
0.8437
```

may be excessive if only a small number of episodes exist.

Final display precision can be standardized later.

---

# 102. PERCENT VS FRACTION

Internally, metrics may use:

```text
0–1
```

fractions.

Final reports may display:

```text
0–100%
```

percentages.

Do not mix both formats within one column/table.

---

# 103. OPEN METRIC DECISIONS — MUST REMAIN OPEN

The following are still unresolved:

1. final precision/recall/F1 averaging convention;
2. reliability-diagram bin count;
3. reliability binning strategy;
4. normalized entropy on/off;
5. wrong-goal-rate denominator;
6. path-efficiency formula;
7. WAIT treatment in path length;
8. completion-time definition;
9. risk-exposure formula details;
10. safety-violation-rate denominator;
11. human-intervention aggregate formula;
12. primary cross-subject aggregation rule;
13. number of seeds/folds for final aggregation;
14. confidence intervals/statistical tests;
15. adaptation comparison metrics;
16. final report decimal precision.

No implementation agent may silently choose these as scientific standards.

---

# 104. DECISIONS REQUIRED BEFORE FINAL METRIC REPORTING

Explicitly approve:

1. EEG metric averaging convention;
2. calibration binning;
3. entropy reporting;
4. wrong-goal denominator;
5. task-success definition;
6. path-efficiency formula;
7. risk-exposure definition;
8. completion-time definition;
9. safety normalized rates;
10. subject/fold/seed aggregation;
11. statistical-analysis plan;
12. adaptation metrics if adaptation exists.

Record these in `DECISIONS.md`.

---

# 105. ACCEPTANCE CRITERIA — METRIC IMPLEMENTATION

The metrics layer is valid when:

1. formulas are explicit;
2. evaluation units are explicit;
3. denominators are preserved;
4. class/hypothesis order is preserved;
5. undefined cases are handled clearly;
6. metric functions are tested;
7. subject/fold/seed metadata remain available;
8. final calculations come from machine-readable logs;
9. metric definitions do not change silently;
10. reportable tables can be regenerated;
11. negative outcomes are not hidden;
12. metrics remain interpretable at the correct system level.

---

# 106. ACCEPTANCE CRITERIA — FINAL EVALUATION

Final evaluation is valid when:

1. EEG decoding metrics are reported separately from system metrics;
2. calibration is reported separately from accuracy;
3. posterior confidence and entropy are not treated as correctness;
4. wrong-goal commitment is distinct from temporary wrong posterior;
5. confirmation/deferral trade-offs are visible;
6. planning cost is separated from hard safety;
7. task success and safety are both reported;
8. cross-subject variability is preserved;
9. seed/fold variability is preserved where used;
10. all headline claims map to reproducible metrics.

---

# 107. CURRENT METRICS & EVALUATION SUMMARY

The project evaluates performance at multiple distinct levels. EEG decoding is measured using accuracy, balanced accuracy, precision, recall, F1, and confusion matrices. Probability reliability is evaluated separately through reliability diagrams, Expected Calibration Error, and Brier Score. Bayesian intent inference is assessed through goal inference accuracy, posterior confidence, entropy, wrong-goal commitment, and evidence updates/decision latency. Shared autonomy is evaluated through confirmation, override, deferral, pause, stop, and intervention counts. Planning is evaluated through path success, path length, path cost, risk exposure, and replanning. Safety is evaluated through unsafe action attempts, executed safety violations, safety overrides, hazard entry, emergency-stop success, and no-safe-path events. Full-system evaluation combines task success, wrong-goal commitment, decision latency, human intervention, navigation efficiency, and safety outcomes while keeping each metric individually interpretable. Cross-subject, seed, fold, robustness, and adaptation results must preserve their underlying evaluation units rather than being collapsed into misleading single numbers. Several normalization/aggregation formulas—especially path efficiency, wrong-goal denominator, reliability binning, completion time, safety rates, and cross-subject aggregation—remain explicitly unresolved until final experiment decisions are approved.

---

# 108. NEXT DOCUMENT

The next planned document is:

**`19_TESTING_AND_VERIFICATION.md` — Unit Testing, Integration Testing, Scientific Verification, Regression Testing, and End-to-End Validation**

That document should define:

- unit-test strategy;
- integration-test strategy;
- mathematical tests;
- leakage tests;
- dataset tests;
- model-interface tests;
- Bayesian analytical tests;
- planner/safety tests;
- shared-autonomy state-machine tests;
- end-to-end replay tests;
- regression tests;
- test fixtures;
- pass/fail criteria;
- manual verification gates;
- and what constitutes scientifically valid verification.

It must clearly distinguish:

```text
software correctness
```

from:

```text
scientific validity
```

and require both.
