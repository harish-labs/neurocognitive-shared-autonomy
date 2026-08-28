# 09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Probability Calibration, Confidence Reliability, Entropy-Based Uncertainty, and Autonomy-Gating Methodology

**Document ID:** E-02  
**Document class:** Machine Learning / Probabilistic Decision Methodology  
**Authority level:** Subordinate to the Master Authority Documents, Scenario Specification, System Architecture, Technology Stack, Dataset/Data Pipeline Specification, Neuroscience/BCI Foundations, and EEG Signal Processing & ML Methodology  
**Status:** Authoritative calibration/uncertainty baseline; the exact calibration method and autonomy thresholds remain explicitly unresolved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND NON-ASSUMPTION RULE

This document defines the project's methodology for:

- distinguishing raw classifier confidence from trustworthy probability;
- probability calibration;
- calibration evaluation;
- uncertainty estimation;
- confidence-state interpretation;
- and using uncertainty to regulate shared autonomy.

It must remain consistent with:

1. `MASTER_PROJECT_SPEC.md`
2. `01_PROJECT_CONCEPT_AND_PROBLEM.md`
3. `02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md`
4. `03_SEARCH_AND_RESCUE_SCENARIO.md`
5. `04_SYSTEM_ARCHITECTURE.md`
6. `05_TECHNOLOGY_STACK.md`
7. `06_DATASET_AND_DATA_PIPELINE.md`
8. `07_NEUROSCIENCE_AND_BCI_FOUNDATIONS.md`
9. `08_EEG_SIGNAL_PROCESSING_AND_ML.md`

If this document conflicts with a higher-authority project document, the higher-authority document wins.

This document must **not** silently finalize any of the following:

- the exact calibration technique;
- the exact calibration-data partition;
- the exact confidence thresholds;
- the exact number of confidence bands;
- the exact posterior commitment threshold;
- the exact Bayesian likelihood mapping;
- the exact adaptation mechanism;
- the exact binary EEG-to-multiple-goal mapping.

Those remain open until explicitly approved.

---

# 1. PURPOSE OF THIS DOCUMENT

This document answers:

> **Why are raw EEG classifier probabilities not automatically trustworthy?**

> **What does probability calibration mean in this project?**

> **How will calibration be measured?**

> **How is uncertainty computed from model/belief probabilities?**

> **How does uncertainty change system behavior?**

> **What distinguishes confidence-aware control from Bayesian shared autonomy?**

The calibration/uncertainty layer exists because the downstream autonomous system must make decisions based not only on:

```text
which class won?
```

but also on:

```text
how trustworthy is the probability?
how uncertain is the current belief?
should autonomy proceed at all?
```

---

# 2. LOCATION IN THE COMPLETE ARCHITECTURE

The relevant architecture is:

```text
EEG epoch
        ↓
CSP+LDA or EEGNet
        ↓
raw class probabilities
        ↓
probability calibration
        ↓
calibrated EEG evidence
        ↓
goal-mapping policy
        ↓
sequential Bayesian goal inference
        ↓
posterior belief
        ↓
uncertainty / entropy
        ↓
shared-autonomy policy
        ↓
PROCEED / CONFIRM / DEFER / PAUSE / STOP
```

This document covers:

```text
raw probabilities
→ calibration
→ uncertainty representation
→ confidence-state output
```

It does not define the full Bayesian goal-inference model; that belongs in the next document.

---

# 3. RAW CLASSIFIER PROBABILITY IS NOT THE SAME AS RELIABILITY

Suppose the EEG decoder outputs:

```text
P(left)  = 0.90
P(right) = 0.10
```

This does **not** automatically mean:

> the decoder will be correct 90% of the time whenever it outputs 0.90.

A model can be:

- overconfident;
- underconfident;
- differently calibrated across subjects;
- differently calibrated across runs;
- differently calibrated under distribution shift.

Therefore the project must empirically test whether predicted probabilities correspond to observed correctness.

---

# 4. CLASSIFICATION ACCURACY AND CALIBRATION ARE DIFFERENT

A model can have:

- high accuracy and poor calibration;
- moderate accuracy and good calibration;
- lower accuracy but more trustworthy confidence estimates.

Example conceptual comparison:

```text
Model A
Accuracy: high
Confidence: often 0.99 even when wrong

Model B
Accuracy: slightly lower
Confidence: better aligned with actual correctness
```

For a shared-autonomy system, Model B may sometimes be more useful because the system needs to know **when not to trust itself**.

Therefore calibration must be evaluated separately from classification accuracy.

---

# 5. FORMAL IDEA OF CALIBRATION

A perfectly calibrated classifier satisfies the idea:

> Among predictions assigned confidence \(p\), approximately a fraction \(p\) should be correct.

Conceptually:

\[
P(Y=\hat{Y}\mid \hat{P}=p) \approx p
\]

For example:

```text
predictions made with confidence ≈ 0.80
```

should be correct approximately:

```text
80% of the time
```

under the evaluated data distribution.

Perfect calibration is an ideal reference, not a guarantee.

---

# 6. WHY CALIBRATION MATTERS MORE IN THIS PROJECT THAN IN A NORMAL CLASSIFIER

The decoder probability affects downstream autonomy.

If the model is strongly overconfident:

```text
incorrect EEG evidence
+
high confidence
→ premature goal commitment
→ autonomous action toward wrong target
```

If the model is underconfident:

```text
correct EEG evidence
+
low confidence
→ excessive deferral
→ unnecessary confirmations
→ slower task completion
```

Therefore probability reliability influences:

- commitment;
- deferral;
- human workload;
- wrong-goal rate;
- safety;
- task latency.

Calibration is not an optional cosmetic metric.

---

# 7. CALIBRATION INPUT

The calibration module receives:

```text
raw decoder probability vector
true class label for calibration/evaluation data
model ID
trial ID
subject ID
split metadata
```

For the current binary task:

\[
\mathbf{p}_{raw}
=
[P(left),P(right)]
\]

The calibration module does not receive:

- Search & Rescue true goal during normal inference;
- future evidence;
- test labels during fitting.

---

# 8. CALIBRATION OUTPUT

The output is:

\[
\mathbf{p}_{cal}
=
[P_{cal}(left),P_{cal}(right)]
\]

with:

\[
0 \le P_{cal}(c) \le 1
\]

and:

\[
\sum_c P_{cal}(c) \approx 1
\]

The calibrated output is then passed to the downstream goal-mapping/Bayesian layer.

---

# 9. CALIBRATION MUST REMAIN MODEL-SPECIFIC

CSP+LDA and EEGNet may have different probability characteristics.

Therefore calibration should be associated with the decoder that produced the raw probabilities.

Conceptually:

```text
CSP+LDA
→ raw probabilities
→ CSP+LDA calibrator

EEGNet
→ raw probabilities
→ EEGNet calibrator
```

Do not assume one calibrator can automatically be reused across unrelated model families.

---

# 10. CALIBRATION FITTING DATA — CRITICAL LEAKAGE BOUNDARY

Calibration is itself a fitted transformation when the chosen method learns parameters.

Therefore:

> **The final test set must not be used to fit the calibrator.**

A valid conceptual pattern is:

```text
training data
→ model fitting

validation / dedicated calibration data
→ calibrator fitting / selection

final test data
→ untouched evaluation
```

The exact calibration split remains unresolved.

---

# 11. POSSIBLE CALIBRATION-PARTITION STRATEGIES

The project has not yet approved one strategy.

Valid candidates may include:

## Strategy A — Dedicated calibration split

```text
Train
Calibration
Test
```

Strength:

- conceptually clean.

Cost:

- reduces effective training data.

---

## Strategy B — Validation split doubles as calibration split

```text
Train
Validation/Calibration
Test
```

Strength:

- efficient.

Risk:

- must avoid repeatedly tuning many choices on the same validation data.

---

## Strategy C — Cross-validated / out-of-fold calibration evidence

Generate out-of-fold predictions on training data, then fit calibration without touching test data.

Strength:

- uses data efficiently.

Cost:

- more implementation complexity.

No strategy is currently locked.

---

# 12. CALIBRATION METHODS — CANDIDATES ONLY

The exact method remains unresolved.

Possible candidates include:

## 12.1 Temperature scaling

Commonly applied to neural logits.

Conceptually:

\[
p_i =
\frac{\exp(z_i/T)}
{\sum_j \exp(z_j/T)}
\]

where:

- \(z_i\) = logits;
- \(T>0\) = learned temperature.

Properties:

- simple;
- preserves class ranking;
- often useful for neural networks.

Status:

> candidate, not approved.

---

## 12.2 Platt-style / sigmoid calibration

Fits a logistic mapping from model scores to calibrated probability.

Can be relevant to some classical models.

Status:

> candidate, not approved.

---

## 12.3 Isotonic regression

Fits a monotonic non-parametric mapping.

Potential benefit:

- flexible calibration shape.

Potential risk:

- can overfit when calibration data are limited.

Status:

> candidate, not approved.

---

## 12.4 Other justified method

Another method may be selected if:

- scientifically appropriate;
- compatible with data volume;
- implementation is reproducible;
- test data remain untouched.

---

# 13. CALIBRATION METHOD SELECTION RULE

Do not select a method because it makes the final test metrics look best.

Method selection should consider:

- model family;
- amount of calibration data;
- validation calibration error;
- stability;
- simplicity;
- interpretability;
- downstream behavior.

The selected method must be documented before final test interpretation.

---

# 14. CALIBRATION CAN BE “NO CALIBRATION”

A valid experimental baseline is:

```text
identity calibration
```

meaning:

```text
p_cal = p_raw
```

This represents the uncalibrated condition.

It is important because the project needs to test whether calibration actually adds value.

---

# 15. RELIABILITY DIAGRAM

A reliability diagram compares predicted confidence against empirical accuracy.

Conceptually:

1. group predictions into confidence bins;
2. compute average confidence in each bin;
3. compute actual accuracy in each bin;
4. compare the two.

Ideal:

```text
confidence ≈ empirical accuracy
```

A reliability diagram can reveal:

- overconfidence;
- underconfidence;
- local calibration errors.

---

# 16. BINNING CAUTION

Reliability diagrams and ECE depend on binning choices.

Potential binning approaches include:

- equal-width bins;
- equal-frequency/adaptive bins.

The exact binning method is not yet locked.

The final methodology must record:

- number of bins;
- binning strategy.

Do not manipulate bin choices to make calibration appear better.

---

# 17. EXPECTED CALIBRATION ERROR — ECE

ECE summarizes calibration gap across bins.

A common form is:

\[
ECE
=
\sum_{m=1}^{M}
\frac{|B_m|}{n}
\left|
acc(B_m)-conf(B_m)
\right|
\]

where:

- \(B_m\) is confidence bin \(m\);
- \(acc(B_m)\) is empirical accuracy;
- \(conf(B_m)\) is mean predicted confidence.

Lower ECE generally indicates better calibration under the chosen binning scheme.

---

# 18. ECE LIMITATIONS

ECE is useful but imperfect.

It depends on:

- bin count;
- binning method;
- sample size.

Therefore the project should not claim calibration quality using ECE alone.

It should be paired with:

- reliability diagram;
- Brier Score;
- possibly additional justified measures.

---

# 19. BRIER SCORE

For binary classification, the Brier Score measures squared error between predicted probability and observed outcome.

One common binary form is:

\[
BS
=
\frac{1}{N}
\sum_{i=1}^{N}
(p_i-y_i)^2
\]

where:

- \(p_i\) = predicted probability for the positive class;
- \(y_i \in \{0,1\}\).

Lower is better.

The Brier Score reflects both:

- calibration;
- discrimination/probability quality.

It is not identical to ECE.

---

# 20. LOG LOSS — OPTIONAL

Negative log-likelihood / log loss may also be useful:

\[
NLL
=
-\frac{1}{N}
\sum_i
\log p(y_i)
\]

It strongly penalizes confident wrong predictions.

It is optional unless later included in the Metrics document.

---

# 21. PRIMARY CALIBRATION EVALUATION SET

The final calibration evaluation should be performed on data not used to fit calibration parameters.

At minimum, compare:

```text
raw probabilities
vs
calibrated probabilities
```

using:

- reliability diagrams;
- ECE;
- Brier Score.

Optional:

- NLL.

---

# 22. SUBJECT-WISE CALIBRATION

Calibration may differ substantially across subjects.

Where the final protocol permits, preserve:

- per-subject ECE;
- per-subject Brier Score;
- subject-level reliability behavior.

Do not assume one aggregate calibration result represents every participant.

---

# 23. CROSS-SUBJECT CALIBRATION

A calibrator fitted on one subject distribution may not remain calibrated on unseen subjects.

This is scientifically important.

Cross-subject evaluation may therefore examine:

```text
decoder generalization
+
calibration generalization
```

The exact protocol remains unresolved.

---

# 24. RAW CONFIDENCE DEFINITION

For binary classification, a simple class-confidence value may be:

\[
C_{raw} = \max(\mathbf{p}_{raw})
\]

After calibration:

\[
C_{cal} = \max(\mathbf{p}_{cal})
\]

However:

> **maximum class probability is not the complete uncertainty representation of the final system.**

The Bayesian layer maintains a posterior over intent hypotheses, and entropy is computed on that posterior.

---

# 25. DECODER CONFIDENCE VS BAYESIAN BELIEF CONFIDENCE

The project must distinguish:

## Decoder confidence

How strongly the EEG classifier favors Left vs Right for one observation.

Example:

```text
[0.80, 0.20]
```

## Bayesian posterior confidence

How strongly accumulated evidence favors a goal/intention hypothesis after multiple observations.

Example:

```text
after several updates:
P(goal A)=0.93
P(goal B)=0.07
```

These are not the same quantity.

---

# 26. UNCERTAINTY LAYERS

The project contains multiple uncertainty concepts.

## 26.1 Signal uncertainty / variability

Noise and variability in EEG.

Not represented by one mandatory scalar at this stage.

---

## 26.2 Decoder predictive uncertainty

Ambiguity in raw/calibrated class probabilities.

Example:

```text
[0.51, 0.49]
```

is highly ambiguous.

---

## 26.3 Bayesian goal uncertainty

Ambiguity in the posterior over candidate goal/intention hypotheses.

This is the primary uncertainty state used for shared-autonomy decisions.

---

## 26.4 Environmental uncertainty/risk

Hazard/risk information used in planning/safety.

This is separate from EEG uncertainty.

---

# 27. APPROVED INITIAL UNCERTAINTY MEASURE — ENTROPY

The approved initial uncertainty measure is Shannon entropy:

\[
H(P)
=
-\sum_{g}P(g)\log P(g)
\]

For a binary posterior:

```text
[0.50, 0.50]
```

entropy is maximal.

For:

```text
[1.00, 0.00]
```

entropy is minimal.

Exact numerical handling of zero probabilities must be implemented safely.

---

# 28. NUMERICAL ENTROPY IMPLEMENTATION

The implementation should avoid:

```text
log(0)
```

Possible safe approaches include:

- ignoring terms where \(p=0\);
- adding a tiny numerical epsilon only for computation.

The implementation must not alter the conceptual probability distribution unnecessarily.

Unit tests must verify:

- uniform distribution → high/maximal entropy;
- concentrated distribution → low entropy;
- invalid probabilities rejected.

---

# 29. NORMALIZED ENTROPY

If the number of goal hypotheses can vary, normalized entropy may be useful:

\[
H_{norm}(P)
=
\frac{H(P)}
{\log K}
\]

where:

- \(K\) = number of hypotheses.

This gives a value conceptually bounded between 0 and 1 for valid distributions.

Status:

> **Optional / potentially useful.**

It is not yet mandatory.

For a fixed binary interface, raw entropy may be sufficient.

---

# 30. WHY ENTROPY IS PREFERRED OVER ONLY MAXIMUM PROBABILITY

Maximum probability considers only the largest class.

Entropy uses the complete distribution.

Example:

```text
Distribution A:
[0.70, 0.30]

Distribution B:
[0.70, 0.10, 0.10, 0.10]
```

Both have maximum probability 0.70, but the total uncertainty structure differs.

This becomes more relevant if the goal hypothesis space expands beyond two options.

---

# 31. CONFIDENCE STATES

The shared-autonomy architecture currently expects conceptual confidence states such as:

```text
HIGH
MEDIUM / INTERMEDIATE
LOW
```

or equivalent functional categories.

Their purpose is to drive different behaviors.

However:

> **The exact number of categories and numerical thresholds are not yet locked.**

---

# 32. CONCEPTUAL HIGH-CONFIDENCE BEHAVIOR

When evidence is sufficiently strong and uncertainty sufficiently low, the system may:

```text
PROCEED
```

with autonomous assistance toward the approved/inferred goal, depending on the final policy.

High confidence must not override:

- emergency stop;
- safety constraints;
- explicit human override.

---

# 33. CONCEPTUAL INTERMEDIATE-CONFIDENCE BEHAVIOR

When evidence is neither clearly reliable nor completely ambiguous, the system may:

```text
REQUEST CONFIRMATION
```

or:

```text
reduce autonomous commitment
```

This state supports human oversight.

---

# 34. CONCEPTUAL LOW-CONFIDENCE BEHAVIOR

When uncertainty is high, the system should avoid pretending to know the user's intent.

Possible actions include:

```text
DEFER
WAIT
PAUSE
REQUEST NEW EVIDENCE
REQUEST HUMAN INPUT
```

Exact behavior will be finalized with the shared-autonomy policy.

---

# 35. THRESHOLDS — UNRESOLVED

Earlier planning included example values such as:

```text
posterior > 0.8
```

for high confidence and:

```text
0.6–0.8
```

for an intermediate region.

Those values were explicitly examples.

They are **not authoritative**.

No Codex implementation may turn them into final constants without approval.

---

# 36. THRESHOLD SELECTION PRINCIPLE

Thresholds must be selected through a defensible process.

Potential methods may include:

- validation-set trade-off analysis;
- safety-oriented operating-point selection;
- minimizing wrong commitment under a bounded confirmation cost;
- sensitivity analysis across several thresholds.

Exact method remains unresolved.

---

# 37. THRESHOLD TUNING MUST NOT USE FINAL TEST PERFORMANCE

Do not:

```text
try thresholds on final test
→ choose the one with best result
```

Correct:

```text
training/validation experiments
→ choose policy
→ freeze threshold
→ final test evaluation
```

---

# 38. THRESHOLDS ARE SYSTEM PARAMETERS, NOT EEG MODEL PARAMETERS

The decoder answers:

```text
what class probability does the EEG model output?
```

The shared-autonomy policy answers:

```text
what confidence/uncertainty is sufficient to act?
```

These must remain separate.

Do not bury autonomy thresholds inside EEGNet.

---

# 39. CALIBRATION HANDOFF TO BAYESIAN INFERENCE

The Bayesian module should receive calibrated EEG evidence, conceptually:

```text
CalibratedEvidence:
    class_names
    raw_probabilities
    calibrated_probabilities
    calibration_method
    model_id
    trial_id
```

The next step is:

```text
calibrated Left/Right evidence
→ application goal-mapping policy
→ Bayesian likelihood/evidence representation
```

The exact mapping is not defined here.

---

# 40. CALIBRATION IS NOT BAYESIAN INFERENCE

Calibration maps:

```text
raw model score/probability
→ more reliable probability estimate
```

Bayesian inference maps:

```text
prior belief
+
new evidence
→ updated posterior belief
```

These are different operations.

Do not merge them conceptually.

---

# 41. ENTROPY SHOULD GENERALLY BE COMPUTED ON THE BAYESIAN POSTERIOR

The current architecture intends the primary shared-autonomy uncertainty measure to reflect:

> **uncertainty over the current goal/intention belief**

Therefore the main entropy calculation should generally consume the Bayesian posterior.

Decoder-level entropy may also be inspected as an auxiliary signal, but it should not silently replace posterior uncertainty.

---

# 42. DECODER ENTROPY — OPTIONAL AUXILIARY MEASURE

For a raw/calibrated binary class probability vector:

\[
H_{decoder}
=
-\sum_c p(c)\log p(c)
\]

This may help analyze individual EEG prediction ambiguity.

Status:

> optional diagnostic.

It should remain clearly distinguished from:

\[
H_{goal}
\]

computed on the Bayesian goal posterior.

---

# 43. UNCERTAINTY-AWARE BEHAVIOR REQUIREMENT

To claim the system is:

> **uncertainty-aware**

the uncertainty value must affect behavior.

Acceptable examples:

- prevent immediate commitment;
- trigger confirmation;
- cause deferral;
- cause pause;
- reduce assistance;
- demand more evidence.

Not sufficient:

```text
display entropy graph
```

while the controller behaves identically regardless of entropy.

---

# 44. UNCERTAINTY LOGGING REQUIREMENTS

Every full-system experiment should preserve, where applicable:

```text
raw EEG class probabilities
calibrated probabilities
Bayesian posterior
entropy
confidence state
autonomy decision
human confirmation/override
goal commitment
task outcome
```

This enables causal/failure analysis.

---

# 45. CALIBRATION EXPERIMENT — MINIMUM DESIGN

At minimum, for each decoder evaluated:

```text
1. produce raw probabilities
2. evaluate raw calibration
3. fit approved calibrator on non-test data
4. produce calibrated probabilities
5. evaluate calibrated calibration
6. compare
```

Metrics:

- ECE;
- Brier Score;
- reliability diagram.

Optional:

- NLL.

---

# 46. CALIBRATION ABLATION

The architecture must support:

```text
Full system with calibration
vs
Full system without calibration
```

or another scientifically controlled comparison.

The purpose is to determine whether calibration affects:

- confidence quality;
- wrong commitments;
- deferrals;
- task success;
- safety;
- human interventions.

---

# 47. UNCERTAINTY ABLATION

The architecture must support a condition in which uncertainty gating is removed or neutralized.

Conceptually:

```text
Full system
vs
Full - uncertainty gating
```

This is required by the previously approved ablation plan.

The implementation should therefore avoid making uncertainty inseparable from unrelated modules.

---

# 48. RAW CONFIDENCE BASELINE

A useful baseline is:

```text
raw max class probability
→ confidence rule
```

This can be compared with:

```text
calibrated probability
→ confidence rule
```

and later:

```text
Bayesian posterior entropy
→ shared-autonomy rule
```

This helps distinguish the value of each layer.

---

# 49. PRINCIPAL SYSTEM CONDITIONS RELEVANT TO THIS DOCUMENT

The approved A/B/C/D framework includes:

## System A — Direct EEG

```text
decoder
→ direct commitment
```

No uncertainty-aware deferral.

## System B — Confidence-aware

```text
decoder
→ confidence/uncertainty
→ act or defer
```

No sequential Bayesian goal inference.

## System C — Bayesian shared autonomy

```text
EEG evidence
→ Bayesian inference
→ autonomous navigation
```

## System D — Full

```text
EEG
+ calibration
+ Bayes
+ uncertainty
+ shared autonomy
+ safety
+ adaptation
```

The Experimental Design document will freeze the exact component inclusion so comparisons remain fair.

---

# 50. OVERCONFIDENCE FAILURE CASE

Conceptual example:

```text
True EEG class: Right
Raw model: Left 0.96
Calibrated model: Left 0.72
```

Possible consequence:

- raw-confidence system may commit strongly;
- calibrated system may request more evidence/confirmation;
- Bayesian system may recover if later evidence supports Right.

This is an example pattern only, not a project result.

---

# 51. UNDERCONFIDENCE FAILURE CASE

Conceptual example:

```text
True class: Left
Raw model: Left 0.58
but model is often correct at this score range
```

A poorly calibrated low-confidence signal may cause unnecessary deferral.

Calibration can potentially reduce this issue.

Again, this is conceptual, not a measured result.

---

# 52. CALIBRATION FAILURE CASES

The project should analyze situations such as:

- calibration improves ECE but worsens Brier Score;
- calibration improves aggregate reliability but harms certain subjects;
- calibrator overfits small calibration set;
- calibration shifts probabilities without improving downstream decisions;
- neural and classical models require different calibration strategies.

Negative/mixed findings are valid.

---

# 53. UNCERTAINTY FAILURE CASES

Possible failures include:

- entropy remains low for wrong posterior;
- threshold commits too early;
- threshold defers too often;
- confidence states oscillate;
- uncertainty remains poorly sensitive to degraded EEG evidence;
- uncertainty reduces wrong goals but greatly increases task time.

These trade-offs must be measured.

---

# 54. DISTRIBUTION SHIFT

Calibration may deteriorate when evaluation data differ from calibration data.

Potential sources:

- unseen subjects;
- different EEG quality;
- different runs;
- injected noise;
- model drift.

The project should not assume calibration remains valid under every condition.

Cross-subject and robustness experiments are therefore important.

---

# 55. ROBUSTNESS EXPECTATION

A key research hypothesis is that uncertainty-aware shared autonomy may degrade more gracefully when EEG evidence quality deteriorates.

This means the desired behavior is conceptually:

```text
worse EEG evidence
→ increased uncertainty
→ more deferral / confirmation
→ fewer unjustified commitments
```

This is a hypothesis.

The experiment must be capable of disproving it.

---

# 56. NOISE INJECTION AND UNCERTAINTY

When controlled noise/perturbation is added:

- define it mathematically;
- record seed;
- record severity;
- apply consistently.

The project may then measure whether:

- ECE changes;
- Brier Score changes;
- entropy increases;
- deferral frequency changes;
- wrong-goal rate changes.

Previously discussed noise levels such as 10/20/30% remain provisional, not locked.

---

# 57. CALIBRATION UNDER NOISE

A calibrator fitted under one condition may not remain valid under a noisier condition.

This is scientifically meaningful.

The project may compare:

```text
clean calibration performance
vs
degraded-condition calibration performance
```

without retraining the calibrator on the final test perturbation.

---

# 58. ADAPTATION AND CALIBRATION — SEPARATE RESPONSIBILITIES

Calibration asks:

> Are probability magnitudes reliable?

Adaptation asks:

> Should the system change user-specific priors, thresholds, reliability estimates, or another approved parameter based on interaction history?

Do not merge adaptation into calibration.

A future adaptation module may use calibration statistics, but its mechanism remains unresolved.

---

# 59. PERSONALIZATION OF CALIBRATION — NOT CORE

Subject-specific calibration could potentially improve reliability.

However, the current project has not locked:

- per-subject calibrators;
- global calibrator;
- hybrid calibration.

This should be decided only if the experimental protocol justifies it.

---

# 60. BAYESIAN LIKELIHOOD MAPPING — NOT DEFINED HERE

A classifier output:

```text
P(left | EEG)
```

cannot be inserted into a Bayesian goal model without carefully defining what it represents relative to:

```text
P(evidence | goal)
```

The exact evidence/likelihood mapping is a key scientific issue.

This document deliberately does not invent an ad hoc formula.

The next Bayesian Goal Inference document must define it explicitly and test it with synthetic cases before end-to-end integration.

---

# 61. PROBABILITY SEMANTICS MUST BE EXPLICIT

The project must distinguish:

```text
P(class | EEG)
```

from:

```text
P(goal | evidence)
```

and from:

```text
P(evidence | goal)
```

These quantities are not interchangeable.

A future implementation must document any transformation connecting them.

---

# 62. CONFIDENCE-STATE INTERFACE

The uncertainty module should expose a stable object conceptually like:

```text
UncertaintyEstimate:
    posterior
    entropy
    normalized_entropy
    confidence_state
    threshold_policy_id
```

Optional:

```text
decoder_entropy
```

The shared-autonomy controller consumes this object.

---

# 63. CONFIDENCE POLICY SHOULD BE CONFIGURABLE

The policy should live in configuration, not scattered conditions.

Conceptual configuration:

```yaml
uncertainty:
  measure: entropy
  normalized: TBD

confidence_policy:
  type: TBD
  high_threshold: TBD
  low_threshold: TBD
```

`TBD` is intentional.

---

# 64. THRESHOLD POLICY VERSIONING

Once thresholds are approved, assign a stable policy identifier.

Example concept:

```text
confidence_policy_v001
```

Every experiment should record which policy was used.

This prevents hidden threshold changes across runs.

---

# 65. CALIBRATOR VERSIONING

Every calibrator should have a stable identity.

Conceptual manifest:

```text
calibrator_id
decoder_model_id
method
fit_split_id
fit_subjects
hyperparameters
metrics_on_validation
code_commit
```

Do not overwrite calibrators without trace.

---

# 66. CALIBRATION DATA CONTRACT

Conceptually:

```text
CalibrationRecord:
    trial_id
    subject_id
    true_label
    predicted_label
    raw_probabilities
    calibrated_probabilities
    decoder_model_id
    calibrator_id
    split_id
```

This allows later reliability analysis.

---

# 67. TESTING — CALIBRATION MODULE

Tests should verify:

- input probabilities valid;
- output probabilities valid;
- output sums to ~1;
- method can fit/save/load where applicable;
- class order preserved;
- test labels are not required during inference;
- invalid model/calibrator mismatch rejected.

---

# 68. TESTING — ECE

Using controlled synthetic cases:

## Perfect calibration-style toy case

Should produce low error.

## Strong overconfidence toy case

Should produce larger error.

Exact numerical expected values depend on binning.

Tests should focus on mathematically verifiable small examples.

---

# 69. TESTING — BRIER SCORE

Use simple binary cases with analytically known values.

Example:

```text
y = 1
p = 1.0
→ squared error = 0
```

```text
y = 1
p = 0.0
→ squared error = 1
```

Then validate batch averaging.

---

# 70. TESTING — ENTROPY

For binary probability:

```text
[0.5, 0.5]
```

entropy should be maximal.

For:

```text
[1.0, 0.0]
```

entropy should be minimal/zero within numerical tolerance.

Also test:

- invalid negative probability;
- sum not near 1;
- NaN;
- empty distribution.

---

# 71. TESTING — CONFIDENCE POLICY

Once thresholds are approved, unit tests must cover:

- high-confidence boundary;
- intermediate boundary;
- low-confidence boundary;
- exact threshold behavior;
- emergency stop precedence;
- invalid uncertainty value.

Threshold behavior must not remain ambiguous.

---

# 72. CALIBRATION IMPLEMENTATION FILE

Approved architecture suggests:

```text
src/models/calibration.py
```

Responsibilities:

- fit calibrator;
- transform probabilities;
- save/load;
- expose metadata;
- calculate/route calibration evaluation where appropriate.

It must not contain:

- Bayesian inference;
- autonomy decisions;
- Search & Rescue mapping.

---

# 73. UNCERTAINTY IMPLEMENTATION FILE

Approved architecture suggests:

```text
src/cognition/uncertainty.py
```

Responsibilities:

- validate posterior;
- compute entropy;
- optionally normalize entropy;
- map uncertainty to a confidence-state representation once policy is approved;
- expose stable output.

It must not:

- infer EEG class;
- plan a route;
- modify safety rules.

---

# 74. EVALUATION FILES

Calibration metrics may live in:

```text
src/evaluation/eeg_metrics.py
```

or a dedicated calibration-metrics module if justified.

The code should produce:

- ECE;
- Brier Score;
- reliability plot data;
- optional NLL.

The exact code organization may be refined later.

---

# 75. RELIABILITY PLOT DATA MUST BE SAVED

A rendered plot alone is insufficient.

Save the underlying:

```text
bin confidence
bin accuracy
bin count
```

where practical.

This allows the final chart to be reproduced.

---

# 76. EXPERIMENT LOGGING

Calibration/uncertainty experiments should save:

```text
experiment_id
decoder_model_id
calibrator_id
calibration method
fit split
test split
subjects
raw probabilities
calibrated probabilities
ECE
Brier Score
reliability data
entropy
confidence state
threshold policy
Git commit
```

---

# 77. MANUAL VALIDATION CHECKLIST

The project owner should manually verify:

## Calibration

- raw probability examples;
- calibrated probability examples;
- class order unchanged;
- no test fitting;
- reliability diagram makes sense;
- ECE calculation uses recorded bins;
- Brier Score implementation is correct.

## Uncertainty

- uniform posterior gives high entropy;
- concentrated posterior gives low entropy;
- entropy changes when evidence changes;
- shared-autonomy behavior actually responds to uncertainty.

---

# 78. DEVELOPMENT ORDER

Recommended order:

## Step 1 — Save raw probabilities

From CSP+LDA and EEGNet.

## Step 2 — Build calibration evaluation utilities

Implement:

- reliability diagram data;
- ECE;
- Brier Score.

## Step 3 — Establish uncalibrated baseline

Evaluate raw probabilities.

## Step 4 — Implement candidate calibrator

Only after the fitting split is approved.

## Step 5 — Evaluate raw vs calibrated

On untouched evaluation data.

## Step 6 — Implement entropy

Using synthetic posterior distributions first.

## Step 7 — Implement confidence-policy interface

Keep thresholds configurable/TBD until approved.

## Step 8 — Connect to Bayesian inference

After Bayesian likelihood mapping is formally defined.

---

# 79. CODEX TASK BOUNDARY — CALIBRATION METRICS

A suitable Codex task later would be:

> Implement calibration evaluation utilities only. Consume saved true labels and decoder probability vectors. Add reliability-bin computation, ECE, and Brier Score with unit tests using analytically checkable toy inputs. Do not choose or fit a calibration method yet. Do not change model training or autonomy logic.

This keeps the scientific decision separate from implementation.

---

# 80. CODEX TASK BOUNDARY — ENTROPY

Another suitable task:

> Implement entropy-based uncertainty for a validated probability distribution. Add optional normalized entropy support behind configuration, but do not define autonomy thresholds. Include unit tests for uniform, concentrated, invalid, and non-finite distributions. Do not implement shared-autonomy policy.

---

# 81. CALIBRATION METHOD APPROVAL CHECKLIST

Before choosing the final calibration method, review:

1. decoder model type;
2. available calibration sample size;
3. raw reliability behavior;
4. subject variability;
5. candidate method complexity;
6. validation ECE;
7. validation Brier Score;
8. stability;
9. leakage risk;
10. downstream interpretability.

The simplest method that performs adequately is preferable.

---

# 82. THRESHOLD APPROVAL CHECKLIST

Before locking confidence thresholds, review:

1. wrong-goal rate;
2. confirmation rate;
3. deferral rate;
4. decision latency;
5. task completion;
6. safety outcomes;
7. sensitivity to threshold changes;
8. robustness under noisier evidence.

A threshold should reflect an explicit trade-off, not a visually pleasing number.

---

# 83. CALIBRATION VS THRESHOLD TUNING ORDER

Preferred conceptual order:

```text
train decoder
→ freeze decoder
→ fit/select calibrator
→ evaluate calibrated probabilities
→ freeze calibration strategy
→ tune confidence policy on allowed development data
→ freeze thresholds
→ final test
```

Do not simultaneously adjust everything on the final evaluation set.

---

# 84. CLASS ORDER MUST REMAIN STABLE

For the current decoder:

```text
["left", "right"]
```

or the actual explicit chosen order.

Calibration must preserve this order.

A class-order mismatch can create scientifically catastrophic errors such as:

```text
P(left) interpreted as P(right)
```

Every calibrator/model interface must validate class names.

---

# 85. NUMERICAL STABILITY

Calibration and uncertainty code must handle:

- probability values very close to zero;
- probabilities very close to one;
- floating-point normalization;
- non-finite values.

The code must not silently clip extreme probabilities without recording/justifying the operation.

If clipping is required for log loss or numerical stability, the epsilon value must be explicit.

---

# 86. CALIBRATION PERFORMANCE MUST NOT BE OVERCLAIMED

Allowed after real experiments:

> “Calibration reduced ECE on the held-out evaluation set.”

Allowed:

> “The calibrated model produced more reliable confidence estimates under the tested protocol.”

Not allowed:

> “The probabilities are now true probabilities of human intention.”

Calibration concerns the statistical behavior of model outputs under the evaluated task/distribution.

---

# 87. UNCERTAINTY CLAIM BOUNDARIES

Allowed:

> “Posterior entropy was used as an uncertainty measure.”

Allowed:

> “Higher posterior uncertainty triggered deferral under the implemented policy.”

Not allowed:

> “The system knows when it is wrong.”

Not allowed:

> “Entropy captures all forms of uncertainty.”

Not allowed:

> “The system is provably safe because uncertainty is measured.”

---

# 88. EPISTEMIC VS ALEATORIC TERMINOLOGY — USE CAREFULLY

Advanced ML literature distinguishes:

- aleatoric uncertainty;
- epistemic uncertainty.

The current core system does **not** yet implement a rigorous decomposition of these uncertainty types.

Therefore the project should not claim such decomposition unless an explicit method is later implemented.

Current safe wording:

> **predictive uncertainty / posterior uncertainty**

rather than asserting a specific uncertainty taxonomy.

---

# 89. MONTE CARLO DROPOUT / DEEP ENSEMBLES — NOT CORE

Methods such as:

- MC dropout;
- deep ensembles;
- Bayesian neural networks;

may estimate additional uncertainty.

They are **not part of the locked core**.

Entropy of the Bayesian goal posterior is the approved initial uncertainty measure.

Do not add advanced uncertainty methods merely for complexity.

---

# 90. OOD DETECTION — NOT CORE

Formal out-of-distribution detection is not currently a required module.

Cross-subject degradation and robustness tests may reveal distribution shift, but the project does not claim an explicit OOD detector unless one is later approved and implemented.

---

# 91. CALIBRATION DOES NOT SOLVE DISTRIBUTION SHIFT

A model calibrated on one distribution may become miscalibrated under:

- unseen subjects;
- noisy inputs;
- altered preprocessing;
- changed task.

Therefore calibration is not a guarantee of universal reliability.

This limitation must appear in the final technical report.

---

# 92. SAFETY ROLE OF UNCERTAINTY

Uncertainty contributes to safety by allowing the system to avoid unjustified commitment.

However, uncertainty is only one safety mechanism.

The full project also includes a separate safety controller for:

- blocked cells;
- hazards;
- invalid actions;
- emergency stop.

Therefore:

```text
uncertainty-aware control
≠ complete safety system
```

---

# 93. HUMAN ROLE IN UNCERTAINTY MANAGEMENT

The shared-autonomy design uses the human as an authority when model uncertainty is not low enough to justify autonomous commitment.

Human actions may include:

- confirm;
- override;
- pause;
- stop.

This is a key human–AI interaction feature.

The final UI should make uncertainty visible enough for technical interpretation without requiring the human to understand calibration mathematics.

---

# 94. DECISION LATENCY TRADE-OFF

Waiting for more evidence may:

- reduce wrong commitment;
- improve posterior confidence;

but also:

- increase decision time;
- delay rescue-agent movement.

Therefore the project must measure the trade-off.

An uncertainty-aware system is not automatically superior if it defers indefinitely.

---

# 95. HUMAN-BURDEN TRADE-OFF

Excessive confirmation creates human workload.

Therefore the desired policy must balance:

```text
autonomy
vs
human intervention
vs
safety
```

The project should measure:

- confirmations;
- overrides;
- deferrals;
- completion time;
- wrong commitments.

---

# 96. CALIBRATION-TO-SYSTEM EVALUATION LINK

Calibration should eventually be evaluated at two levels.

## Level 1 — Statistical

- ECE;
- Brier Score;
- reliability diagram.

## Level 2 — System

- wrong-goal commitment;
- confirmation frequency;
- deferral;
- decision latency;
- task success;
- safety events.

It is possible for a statistical calibration improvement to produce little system-level benefit.

That would be a valid result.

---

# 97. UNCERTAINTY-TO-SYSTEM EVALUATION LINK

Similarly, entropy should be evaluated not only as a number but through its effect on:

- autonomy mode;
- commitment timing;
- wrong goals;
- human interventions;
- safety;
- task performance.

This is essential to justify the phrase:

> **uncertainty-aware adaptive control/shared autonomy**

---

# 98. ABLATION INTERPRETATION

Possible valid findings:

## Calibration helps

Better reliability and downstream decisions.

## Calibration changes little

Raw probabilities were already reasonably calibrated or thresholds dominate behavior.

## Uncertainty helps safety

Fewer wrong/unsafe commitments with more deferral.

## Uncertainty hurts task speed

More confirmations and longer completion.

## Calibration helps one model more than another

Possible because CSP+LDA and EEGNet have different score properties.

All are valid.

---

# 99. FAILURE ANALYSIS TABLE

The final results should support a table conceptually like:

| Failure Type | Raw Prob. | Calibrated Prob. | Posterior Entropy | Autonomy Response | Outcome |
|---|---:|---:|---:|---|---|
| Confident wrong decoder | measured | measured | measured | measured | measured |
| Ambiguous evidence | measured | measured | measured | measured | measured |
| Cross-subject degradation | measured | measured | measured | measured | measured |
| Noise stress | measured | measured | measured | measured | measured |

No values should be invented before experiments.

---

# 100. REPRODUCIBILITY

Every reportable calibration/uncertainty result should be reconstructable from:

```text
decoder predictions
true labels
calibration split
calibrator configuration
uncertainty configuration
confidence policy
code commit
experiment config
```

No manual spreadsheet-only calibration process should become part of the authoritative results pipeline.

---

# 101. OPEN DECISIONS

The following remain unresolved.

## 101.1 Final calibration method

Candidates remain open.

## 101.2 Calibration fitting partition

Not locked.

## 101.3 Reliability binning scheme

Not locked.

## 101.4 Number of reliability bins

Not locked.

## 101.5 Whether normalized entropy is required

Not locked.

## 101.6 Confidence-state thresholds

Not locked.

## 101.7 Threshold-selection procedure

Not locked.

## 101.8 Exact relationship between calibrated EEG class probability and Bayesian likelihood

Not locked.

## 101.9 Subject-specific versus global calibration

Not locked.

These must not be silently resolved.

---

# 102. DECISIONS TO FREEZE BEFORE FINAL SYSTEM EXPERIMENTS

Before final A/B/C/D experiments, explicitly approve and record:

1. decoder selected for each experiment;
2. calibration method;
3. calibration fitting data;
4. ECE binning definition;
5. entropy definition;
6. normalized entropy on/off;
7. confidence-state policy;
8. numerical thresholds;
9. whether thresholds differ by experiment/model;
10. how uncertainty triggers shared-autonomy actions.

These should be recorded in:

- configuration;
- `DECISIONS.md`;
- experiment logs.

---

# 103. ACCEPTANCE CRITERIA — CALIBRATION

Calibration is correctly implemented when:

1. raw probability vectors are preserved;
2. class order is preserved;
3. calibrator is fitted only on approved non-test data;
4. calibrated probabilities are valid;
5. calibrator identity is stored;
6. raw and calibrated probabilities can be compared;
7. ECE is computed reproducibly;
8. Brier Score is computed reproducibly;
9. reliability diagrams are reproducible from saved data;
10. subject/fold metadata remain traceable;
11. no final test tuning occurs;
12. calibration can be disabled for ablation.

---

# 104. ACCEPTANCE CRITERIA — UNCERTAINTY

Uncertainty is correctly implemented when:

1. posterior probabilities are validated;
2. entropy is computed correctly;
3. numerical edge cases are handled;
4. uncertainty is logged;
5. uncertainty feeds the shared-autonomy interface;
6. uncertainty can alter behavior;
7. confidence policy is configuration-driven;
8. thresholds are versioned once approved;
9. uncertainty gating can be disabled for ablation;
10. decoder confidence and Bayesian posterior uncertainty remain distinct;
11. environmental risk remains distinct from EEG/goal uncertainty.

---

# 105. CLAIM ACCEPTANCE CRITERIA

The project may claim:

> **probability-calibrated**

only if an actual calibration method is implemented and evaluated.

It may claim:

> **uncertainty-aware**

only if uncertainty is explicitly calculated and alters behavior.

It may claim:

> **confidence-dependent autonomy**

only if autonomy behavior changes according to the implemented confidence/uncertainty policy.

It may not claim:

> **Bayesian uncertainty-aware goal inference**

until the next Bayesian module is actually implemented.

---

# 106. CURRENT CALIBRATION & UNCERTAINTY SUMMARY

The NeuroCognitive Shared Autonomy project does not treat EEG classifier softmax/probability output as inherently trustworthy. Raw CSP+LDA or EEGNet class probabilities must first be evaluated for statistical reliability and, if the approved methodology supports it, transformed through a separately fitted calibration layer. Calibration is evaluated using at least reliability diagrams, Expected Calibration Error, and Brier Score, with calibration parameters fitted only on non-test data. The exact calibration method remains unresolved. After calibrated EEG evidence is converted into the appropriate goal-hypothesis representation and processed by sequential Bayesian goal inference, the system computes posterior uncertainty using Shannon entropy as the approved initial measure. That uncertainty must influence shared-autonomy behavior through configurable confidence states such as proceed, confirm, or defer. Exact numerical thresholds remain unresolved and must be selected through a defensible validation procedure rather than copied from earlier examples. Calibration quality, posterior uncertainty, wrong-goal commitment, deferral, human intervention, task latency, and safety outcomes must ultimately be evaluated together so that the system's confidence handling is assessed both statistically and behaviorally.

---

# 107. NEXT DOCUMENT

The next planned document is:

**`10_BAYESIAN_GOAL_INFERENCE.md` — Bayesian Goal / Intent Inference Methodology**

That document should define:

- latent goal/intention variable;
- prior;
- evidence;
- likelihood;
- posterior;
- sequential update;
- exact probability semantics;
- normalization;
- evidence accumulation;
- reset/commitment rules;
- synthetic test cases;
- decision latency;
- wrong-goal commitment;
- interaction with calibrated EEG probabilities;
- the unresolved binary-EEG-to-multi-goal interface;
- and the interface into uncertainty/shared autonomy.

Most importantly, it must **not invent an ad hoc likelihood mapping from `P(class|EEG)` to `P(evidence|goal)` without explicitly defining and validating the mathematics.**
