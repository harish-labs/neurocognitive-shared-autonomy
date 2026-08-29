# 08_EEG_SIGNAL_PROCESSING_AND_ML.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### EEG Signal Processing, Classical Machine Learning, EEGNet, Training, Validation, and Decoder Interface Methodology

**Document ID:** E-01  
**Document class:** Machine Learning / EEG Methodology Specification  
**Authority level:** Subordinate to the Master Authority Documents, Scenario Specification, System Architecture, Technology Stack, Dataset/Data Pipeline Specification, and Neuroscience/BCI Foundations  
**Status:** Authoritative methodology baseline with approved initial M1 preprocessing choices and remaining unresolved model/evaluation choices explicitly preserved
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND NON-ASSUMPTION RULE

This document defines the approved **EEG signal-processing and machine-learning methodology**.

It must remain consistent with:

1. `MASTER_PROJECT_SPEC.md`
2. `01_PROJECT_CONCEPT_AND_PROBLEM.md`
3. `02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md`
4. `03_SEARCH_AND_RESCUE_SCENARIO.md`
5. `04_SYSTEM_ARCHITECTURE.md`
6. `05_TECHNOLOGY_STACK.md`
7. `06_DATASET_AND_DATA_PIPELINE.md`
8. `07_NEUROSCIENCE_AND_BCI_FOUNDATIONS.md`

If this document conflicts with a higher-authority project document, the higher-authority document wins.

This document must **not** silently freeze any choice that remains open in the existing authority chain.

In particular, the following are still unresolved unless later explicitly approved:

- exact band-pass filter limits;
- exact EEG reference strategy;
- exact epoch interval;
- baseline-correction policy;
- artifact-removal/rejection policy;
- reduced-channel selection;
- resampling;
- exact number of CSP components;
- exact EEGNet implementation/hyperparameters;
- optimizer and training hyperparameters;
- final within-subject/cross-subject split protocol;
- calibration method;
- calibration partition;
- probability threshold values;
- binary EEG-to-Search-&-Rescue goal mapping.

This document defines **how those choices must be made and validated**, not arbitrary final values.

---

# 1. PURPOSE OF THIS DOCUMENT

This document answers:

> **How is raw motor-imagery EEG converted into model-ready trials?**

> **What is the mandatory classical baseline?**

> **What is the neural decoder?**

> **How are the models trained and evaluated without leakage?**

> **What must the decoder output to the downstream Bayesian system?**

> **How do we compare CSP+LDA and EEGNet fairly?**

> **What engineering and scientific checks must exist before the EEG subsystem is considered valid?**

The EEG subsystem must ultimately produce:

```text
validated EEG epoch
        ↓
decoder
        ↓
class-probability vector
```

for the current binary motor-imagery task:

```text
Left-hand motor imagery
vs
Right-hand motor imagery
```

The EEG model does not directly decide the Search & Rescue goal.

---

# 2. EEG SUBSYSTEM ROLE IN THE COMPLETE PROJECT

The full project architecture is:

```text
PhysioNet motor-imagery EEG
        ↓
EEG loading
        ↓
signal preprocessing
        ↓
event extraction / epoching
        ↓
        ├─────────────────────┐
        ▼                     ▼
CSP + LDA baseline       EEGNet / compact CNN
        │                     │
        └──────────┬──────────┘
                   ↓
          unified decoder interface
                   ↓
          probability calibration
                   ↓
          Bayesian goal inference
                   ↓
              uncertainty
                   ↓
            shared autonomy
                   ↓
              planning
                   ↓
                safety
```

This document covers only the portion from:

```text
EEG loading/preprocessing
```

through:

```text
decoder probability output
```

Probability calibration is required by the overall project but receives its own dedicated document next.

---

# 3. APPROVED EEG TASK

The current task is:

> **Binary classification of imagined Left-fist versus imagined Right-fist movement**

using PhysioNet EEGBCI runs:

```text
4
8
12
```

For these runs:

```text
T1 → Left-fist motor imagery
T2 → Right-fist motor imagery
T0 → Rest
```

The project must not silently change to:

- motor execution;
- hands-versus-feet;
- four-class motor imagery;
- rest/left/right three-class classification;
- or arbitrary rescue-goal classification.

---

# 4. PREPROCESSING PHILOSOPHY

The preprocessing pipeline should be:

```text
minimal
scientifically justified
reproducible
identical where appropriate across compared models
easy to audit
```

The objective is not to create the most elaborate EEG-cleaning pipeline.

Every preprocessing operation creates assumptions.

Therefore each operation must answer:

1. Why is it necessary?
2. Is it fit using training data?
3. Could it leak test information?
4. Does it alter the signal in a way that affects interpretation?
5. Is the same operation applied consistently across baselines?
6. Is the parameter recorded?

---

# 5. REQUIRED PREPROCESSING ORDER

The approved conceptual order is:

```text
Raw EEG
        ↓
channel-name standardization
        ↓
montage assignment
        ↓
raw metadata validation
        ↓
selected signal preprocessing
        ↓
event extraction
        ↓
task-specific event mapping
        ↓
epoch construction
        ↓
epoch validation
        ↓
dataset split
        ↓
training-only fitted transformations
        ↓
model input
```

The exact position of a specific operation may vary if technically required, but the scientific logic must remain equivalent.

---

# 6. SIGNAL PREPROCESSING STAGES

Potential stages include:

- band-pass filtering;
- referencing;
- resampling if approved;
- artifact handling;
- epoch construction;
- optional normalization;
- model-specific transformation.

Not every possible EEG-processing technique should be added.

The final implemented chain must contain only operations that are justified and documented.

---

# 7. BAND-PASS FILTERING

Motor-imagery decoding is strongly associated with sensorimotor mu/beta activity.

Therefore a motor-related band-pass is scientifically reasonable.

However:

> **The approved initial M1 filter is 7–30 Hz.**

An official MNE motor-imagery CSP example also uses a 7–30 Hz band, but the project setting is authoritative because the Project Owner explicitly approved it and it is recorded as D-031 in `DECISIONS.md`.

## Final selection rule

The chosen band must be justified using:

- neuroscience rationale;
- validation data;
- consistency with the selected task;
- and avoidance of final test-set tuning.

## Required recording

Save:

```text
l_freq
h_freq
filter method
filter phase/settings where relevant
sampling frequency
```

with the preprocessing configuration.

---

# 8. FILTERING AND DATA LEAKAGE

A fixed deterministic filter applied identically to each recording does not inherently learn class labels.

However, filter parameters become part of model development if they are tuned based on performance.

Therefore:

- do not repeatedly test many bands on the final test set;
- use training/validation evidence to choose among candidate settings;
- once the final protocol is frozen, evaluate the untouched test data.

---

# 9. EEG REFERENCE

EEG is a differential measurement.

The approved initial M1 reference strategy is **average EEG reference** (D-032).

A different reference requires a superseding approved decision.

## Requirement

The approved reference choice must be:

- explicit;
- applied consistently;
- recorded;
- compatible with channel handling;
- justified in the final methodology.

Do not rely on a library default without documenting it.

---

# 10. RESAMPLING

The source EEG sampling frequency is 160 Hz.

The approved M1-T03 policy is **no resampling**; preserve the native validated 160 Hz sampling rate (D-038).

If a later superseding decision introduces resampling, document:

```text
original sampling rate
new sampling rate
anti-aliasing/filtering behavior
reason for resampling
```

Resampling should only be added if it provides a real computational or methodological benefit.

---

# 11. ARTIFACT HANDLING

The project has not approved a complex artifact-removal pipeline.

Potential EEG artifacts include:

- blinks;
- eye movements;
- muscle activity;
- movement;
- poor electrode contact;
- electrical interference.

## Approved initial rule

```text
No ICA
No automatic bad-channel interpolation
Reject an epoch when EEG peak-to-peak amplitude exceeds 150 µV
Record every rejected epoch and rejection reason/threshold
```

This is D-035. More sophisticated artifact handling requires separate approval.

---

# 12. ARTIFACT-REJECTION GOVERNANCE

If trials are rejected:

- the rejection rule must be deterministic or explicitly logged;
- rejected trial IDs must be preserved;
- class-specific rejection counts must be examined;
- subject-specific rejection counts must be examined.

Do not remove poor-performing trials simply because they cause classification errors.

That would invalidate evaluation.

---

# 13. EVENT EXTRACTION

Events must be derived from the source annotations.

For runs 4/8/12:

```text
T1 = Left imagery
T2 = Right imagery
```

The event-extraction stage must verify:

- both classes exist;
- event counts are plausible;
- events occur within recording bounds;
- event IDs match semantic labels;
- trial provenance is preserved.

---

# 14. T0 / REST HANDLING

The locked classification target is binary Left vs Right.

T0 represents rest. For the initial M1 binary pipeline, its operational treatment is approved as D-036.

The implementation must not silently convert the model into:

```text
Rest vs Left vs Right
```

unless a future scope decision approves that change.

Approved policy:

- exclude T0 from the primary binary epoch/training dataset;
- retain T0 annotations in raw data and inspection/provenance information;
- do not create a third classifier class.

A later exploratory use of T0 requires separate approval.

---

# 15. EPOCH CONSTRUCTION

An epoch is a trial segment:

\[
X_i \in \mathbb{R}^{C \times T}
\]

where:

- \(C\) = channels;
- \(T\) = time samples.

The model dataset becomes:

\[
X \in \mathbb{R}^{N \times C \times T}
\]

with:

\[
y \in \{0,1\}^{N}
\]

for the current binary task.

The canonical processed object is **MNE Epochs**. When persisted, processed epochs use MNE FIF `*-epo.fif` (D-039). Model-specific arrays may be derived later without replacing this canonical representation or its metadata/provenance.

The approved canonical M1 task epoch is **-1.0 s to +4.0 s relative to cue onset** (D-033).

---

# 16. EPOCH TIMING

The approved cue-relative canonical epoch window is -1.0 s to +4.0 s. The initial CSP training crop is +1.0 s to +2.0 s relative to cue onset; that crop belongs to the CSP stage and does not replace the canonical stored epoch.

Important considerations:

- motor-imagery activity may not begin immediately at cue onset;
- overly early intervals may contain cue response rather than sustained imagery;
- overly long intervals may add unrelated activity;
- different windows can materially alter model performance.

The approved values must be documented as:

```text
tmin
tmax
```

and, if a crop is used:

```text
crop_tmin
crop_tmax
```

---

# 17. BASELINE CORRECTION

The approved initial M1 baseline policy is D-034:

```text
baseline = None
```

Do not leave baseline behavior ambiguous or silently enable a library default.

---

# 18. CHANNEL SELECTION

The source dataset contains 64 EEG channels.

The approved M1-T03 policy is to preserve all 64 validated EEG channels with no channel reduction (D-037).

A reduced sensorimotor subset may later be studied only as a separately approved experiment.

If channel reduction is introduced, it must be classified as one of:

- fixed neuroscience-driven channel subset;
- training-only feature/channel selection;
- ablation experiment.

It must never use test performance to choose channels.

---

# 19. CHANNEL ORDER

Channel order is part of the model input contract.

The preprocessing pipeline must preserve:

```text
channel_names
channel_order
```

with every model/checkpoint.

This is especially important for EEGNet.

A checkpoint trained with one channel order must not be evaluated with another.

---

# 20. DATA TYPES AND NUMERICAL VALIDATION

Before model training, validate:

- no NaN;
- no infinity;
- correct tensor/array dtype;
- expected dimensions;
- correct label count;
- correct subject metadata alignment.

Model input should be deterministic from:

```text
raw data
+ preprocessing config
+ code version
```

---

# 21. DATA SPLITTING MUST OCCUR BEFORE SUPERVISED FITTING

Any supervised transformation must be fitted only after the appropriate split.

This includes:

- CSP;
- LDA;
- learned normalization;
- feature selection;
- calibration;
- EEGNet training;
- hyperparameter tuning.

Correct pattern:

```text
raw/epochs
        ↓
split
        ↓
fit on train
        ↓
tune on validation
        ↓
evaluate once on test
```

---

# 22. SPLIT PROTOCOL STATUS

The final subject-split strategy remains unresolved.

Required research direction includes:

- subject-level performance;
- cross-subject analysis.

Potential modes include:

## Within-subject mode

Train/validate/test using trials from the same subject with leakage-safe trial grouping.

## Cross-subject mode

Train on one set of subjects and evaluate on unseen subjects.

## Subject-wise cross-validation

Rotate held-out subjects.

The final experimental design document must freeze the exact protocol.

---

# 23. GROUPING REQUIREMENTS

When splitting:

- trials must retain subject identity;
- repeated windows from the same trial must remain grouped;
- data derived from the same original event must not cross train/test boundaries.

If preprocessing generates multiple windows from one trial, the grouping unit is the **original trial**, not the window.

---

# 24. CLASS BALANCE

For every split, record:

```text
Left count
Right count
```

The project already approves:

- accuracy;
- balanced accuracy;
- precision;
- recall;
- F1;
- confusion matrix.

Balanced accuracy is especially useful if class counts differ.

No oversampling or class weighting is currently locked.

If required, it must be justified and recorded.

---

# 25. CLASSICAL BASELINE — CSP + LDA

The mandatory classical baseline is:

```text
EEG epochs
→ CSP
→ log-variance / CSP feature representation
→ LDA
→ class prediction + probability
```

This baseline is required even if the neural decoder eventually performs better.

---

# 26. CSP PURPOSE

Common Spatial Patterns finds spatial projections that maximize variance differences between the two classes.

For two-class motor imagery, CSP is appropriate because Left- and Right-hand imagery can exhibit different spatial covariance patterns.

Conceptually:

\[
Z = W^T X
\]

where:

- \(X\) is multichannel EEG;
- \(W\) contains learned spatial filters;
- \(Z\) contains spatially transformed signals.

Features are commonly based on transformed variance.

---

# 27. CSP FITTING RULE

CSP is supervised.

Therefore:

> **CSP must be fitted only on the training partition of each experiment/fold.**

Never:

```text
fit CSP on all data
→ split features
```

Correct:

```text
split EEG
→ fit CSP on training EEG
→ transform validation/test using fitted CSP
```

---

# 28. CSP COMPONENT COUNT

The exact number of CSP components is unresolved.

It should be treated as a model hyperparameter.

Selection must use:

- training/validation data;
- cross-validation;
- or another approved non-test procedure.

The final value must be stored in configuration.

---

# 29. CSP REGULARIZATION

Any covariance regularization setting is also a model decision.

No regularization parameter is currently locked.

If regularization is used, record:

- method;
- parameter;
- justification.

---

# 30. LDA

Linear Discriminant Analysis is the approved classical classifier.

LDA receives CSP features and outputs:

- predicted class;
- class score/probability where supported.

The project should use an implementation that provides probabilities suitable for later calibration.

---

# 31. CSP+LDA PIPELINE OBJECT

Where practical, the classical baseline should be represented as a single reproducible fit/predict pipeline.

Conceptually:

```python
pipeline.fit(X_train, y_train)
proba = pipeline.predict_proba(X_test)
```

The implementation must ensure CSP is fitted inside the training process.

---

# 32. CLASSICAL BASELINE OUTPUT

The unified decoder interface requires something conceptually equivalent to:

```text
DecoderPrediction
    model_id
    class_names
    probabilities
    predicted_class
    subject_id
    trial_id
```

For the current task:

```text
class_names = ["left", "right"]
```

The actual stored class ordering must be explicit.

---

# 33. EEGNET / COMPACT CNN

The intended neural model is:

> **EEGNet or an explicitly approved compact EEG CNN implementation**

EEGNet is preferred because it is designed specifically for EEG-based BCI and provides a compact model rather than unnecessary deep complexity.

The neural model should learn temporal and spatial EEG features directly from epoch data.

---

# 34. EEGNET ROLE

EEGNet exists to answer:

> **Does an EEG-specific compact neural network provide better or more useful decoding than the classical CSP+LDA baseline under the approved evaluation protocol?**

It is not assumed to outperform CSP+LDA.

---

# 35. EEGNET INPUT CONTRACT

Conceptually:

```text
batch × channels × time
```

or the exact tensor arrangement expected by the implementation.

If the implementation uses an additional singleton dimension:

```text
batch × 1 × channels × time
```

that must be documented.

Input shape must be validated before training.

---

# 36. EEGNET ARCHITECTURE GOVERNANCE

The exact architecture/hyperparameters are not yet frozen.

The implementation should remain recognizably compact and EEG-appropriate.

Parameters that may require configuration include:

- temporal kernel length;
- number of temporal filters;
- depth multiplier;
- separable convolution settings;
- dropout;
- activation;
- classifier head.

The project should not create a very deep arbitrary CNN merely to increase model complexity.

---

# 37. EEGNET REFERENCE IMPLEMENTATION RULE

If Codex implements EEGNet based on the Lawhern et al. architecture or a trusted implementation, it must:

- cite/reference the architecture source in documentation/code comments where appropriate;
- clearly record any deviations;
- not claim an exact EEGNet replication if the architecture differs substantially.

If the implementation is intentionally simplified:

> **compact EEG CNN**

may be more accurate wording than claiming exact EEGNet.

---

# 38. EEGNET TRAINING

The neural model requires:

- training split;
- validation split;
- loss function;
- optimizer;
- learning rate;
- batch size;
- number of epochs;
- checkpoint selection;
- seed;
- early stopping if used.

Exact values are currently unresolved.

These must be centralized in configuration once approved.

---

# 39. LOSS FUNCTION

For binary Left-vs-Right classification, appropriate loss formulations may include:

- binary cross-entropy;
- two-class cross-entropy.

The exact implementation depends on output shape.

No loss formulation is independently locked here.

The important requirement is consistency between:

- output activation;
- loss;
- probability extraction.

---

# 40. OUTPUT REPRESENTATION

Possible mathematically valid designs include:

## Two-logit output

```text
logits[2]
→ softmax
→ P(left), P(right)
```

## One-logit output

```text
logit
→ sigmoid
→ P(right)
→ derive P(left)
```

Either can support the project.

The final implementation must expose a normalized two-class probability vector to the unified decoder interface.

---

# 41. PROBABILITY OUTPUT REQUIREMENT

For every trial:

\[
0 \le p_i \le 1
\]

and:

\[
\sum_i p_i \approx 1
\]

The decoder must never pass:

- raw logits;
- unnormalized scores;
- arbitrary activation magnitudes

to the Bayesian layer while calling them probabilities.

---

# 42. MODEL TRAINING CHECKPOINTS

The neural training process should save:

- current model;
- selected best model according to approved validation criterion;
- training configuration;
- class order;
- channel order;
- epoch shape;
- seed;
- model ID;
- code/Git reference where practical.

Checkpoint naming should be stable.

---

# 43. MODEL-SELECTION METRIC

The exact metric used to select the best neural checkpoint is not yet locked.

Potential candidates include:

- validation loss;
- balanced accuracy;
- F1.

The selection criterion must be chosen before final test evaluation.

Do not choose whichever metric makes the final model look best after test inspection.

---

# 44. EARLY STOPPING

Early stopping may be used.

If used, define:

- monitored validation quantity;
- patience;
- minimum improvement;
- maximum epochs.

The final test set must never control early stopping.

---

# 45. RANDOM SEEDS

Training must record random seeds where practical.

Seeds may affect:

- weight initialization;
- batch ordering;
- split;
- dropout;
- training trajectory.

For final experiments, one lucky seed should not be selected solely because it performs best.

The Experimental Design document must later define whether:

- a fixed seed;
- multiple seeds;
- or both

are used for reportable results.

---

# 46. GPU / CPU CONSISTENCY

EEGNet may train on GPU or CPU.

The environment should record:

- device;
- PyTorch version;
- CUDA information if applicable.

Minor numerical differences between hardware can occur.

The project should prioritize reproducibility, not claim perfect bit-level equivalence across all devices.

---

# 47. MODEL EVALUATION METRICS

The approved EEG metrics include:

- accuracy;
- balanced accuracy;
- precision;
- recall;
- F1;
- confusion matrix;
- cross-validation performance;
- cross-subject performance where applicable.

ROC-AUC is optional if scientifically justified for the final binary protocol.

---

# 48. ACCURACY

\[
Accuracy = \frac{\text{correct predictions}}{\text{total predictions}}
\]

Accuracy is intuitive but can be misleading if class balance changes.

Therefore it must not be the only metric.

---

# 49. BALANCED ACCURACY

Balanced accuracy averages recall across classes.

It is useful when Left and Right class counts are unequal.

This metric is already part of the approved evaluation plan.

---

# 50. PRECISION, RECALL, AND F1

For each class, evaluate where appropriate:

\[
Precision = \frac{TP}{TP+FP}
\]

\[
Recall = \frac{TP}{TP+FN}
\]

\[
F1 = 2\frac{Precision\cdot Recall}{Precision+Recall}
\]

Averaging strategy must be explicitly recorded.

---

# 51. CONFUSION MATRIX

The confusion matrix must preserve explicit class order:

```text
left
right
```

It should make it possible to inspect whether one motor-imagery class is systematically confused with the other.

---

# 52. SUBJECT-WISE EVALUATION

Aggregate performance can hide large variation.

Where the protocol permits, report:

- metric per subject;
- mean;
- variability/distribution;
- difficult subjects;
- failure cases.

Do not remove a poor-performing subject solely to improve the average.

---

# 53. CROSS-SUBJECT EVALUATION

Cross-subject evaluation is an approved research direction.

The exact protocol remains unresolved.

When implemented, no subject in the held-out test group may appear in training.

Cross-subject model performance should be discussed as a measure of generalization rather than a requirement that performance remain equal to within-subject decoding.

---

# 54. FAIR CSP+LDA VS EEGNET COMPARISON

The comparison should use, as far as scientifically appropriate:

- the same subjects;
- the same runs;
- the same semantic labels;
- the same underlying train/validation/test partition;
- the same epoch timing;
- comparable channel data;
- the same evaluation metrics.

Model-specific transformations are allowed.

Do not give one model access to extra test information.

---

# 55. PREPROCESSING FAIRNESS

If a preprocessing choice is clearly model-specific, document it.

Otherwise, baseline and neural model should receive equivalent signal definitions.

Example:

```text
same EEG trials
same filter
same channels
same epoch window
```

with:

```text
CSP-specific spatial transformation
```

only inside the classical pipeline.

---

# 56. HYPERPARAMETER TUNING

Hyperparameters must be tuned only through approved development data.

Potential CSP/LDA hyperparameters:

- number of CSP components;
- CSP covariance settings;
- LDA settings.

Potential EEGNet hyperparameters:

- learning rate;
- dropout;
- model dimensions;
- batch size;
- epochs;
- optimizer.

Do not conduct unrestricted search merely to maximize a final number.

A small, justified tuning strategy is preferable.

---

# 57. MODEL COMPLEXITY REPORTING

For the neural model, record:

- parameter count;
- model configuration;
- input size;
- training time where useful.

The project does not need an enormous network.

Compactness supports:

- reproducibility;
- interpretability;
- faster experiments;
- future simulated real-time replay.

---

# 58. OVERFITTING

Signs of overfitting may include:

- training accuracy rising while validation performance falls;
- unstable subject-wise performance;
- highly variable seed performance;
- strong within-subject but weak unseen-subject results.

The project must report such behavior.

Do not hide training curves if they reveal a methodological limitation.

---

# 59. DATA AUGMENTATION

No EEG data-augmentation method is currently approved.

If augmentation is later introduced, it must:

- preserve label validity;
- operate on training data only;
- be described mathematically;
- be included as an explicit experimental condition.

Do not silently augment the data.

---

# 60. CLASS WEIGHTING / RESAMPLING

No class-weighting or oversampling method is currently locked.

If class imbalance materially affects training, possible methods may be evaluated.

Any such method must use training data only and be recorded.

---

# 61. MODEL PROBABILITY QUALITY

Classification accuracy alone is insufficient for the full project because the probability vector drives later uncertainty-aware decisions.

Therefore the decoder stage must save:

```text
true label
predicted label
raw probability vector
subject
trial
model ID
```

These outputs allow the later calibration document to evaluate:

- reliability diagrams;
- ECE;
- Brier Score.

---

# 62. RAW VS CALIBRATED PROBABILITY

This document's model output is:

> **raw decoder probability**

The next calibration module transforms:

```text
raw decoder probability
→ calibrated probability
```

The EEG model itself should not silently apply calibration unless the calibration object is explicitly part of the inference pipeline.

---

# 63. UNIFIED DECODER INTERFACE

Both CSP+LDA and EEGNet must implement or be wrapped behind an equivalent interface.

Conceptual API:

```python
decoder.fit(...)
decoder.predict(...)
decoder.predict_proba(...)
decoder.save(...)
decoder.load(...)
```

Not every implementation requires identical internal methods, but downstream modules must consume a stable probability contract.

---

# 64. DECODER PREDICTION CONTRACT

Conceptually:

```text
DecoderPrediction:
    model_id
    model_type
    class_names
    probabilities
    predicted_class
    subject_id
    run_id
    trial_id
    preprocessing_config_id
```

Optional useful fields:

```text
checkpoint_id
timestamp
fold_id
```

The Bayesian system must not need direct access to:

- PyTorch tensors;
- scikit-learn internals;
- CSP objects.

---

# 65. MODEL SERIALIZATION

CSP+LDA and EEGNet should be saveable and reloadable.

Saved model metadata must preserve:

- class order;
- preprocessing version;
- expected channels;
- expected epoch dimensions;
- training subjects/split reference;
- model config.

A model without its input contract is not reproducible.

---

# 66. MODEL REGISTRY / MANIFEST

A simple local manifest is sufficient.

Conceptual example:

```text
model_id
model_type
checkpoint_path
dataset_version
preprocessing_config
split_id
class_names
channel_order
input_shape
training_seed
validation_metric
git_commit
```

No cloud model registry is required.

---

# 67. EXPERIMENT OUTPUTS

Each EEG experiment should save:

```text
experiment ID
config
split manifest
model ID
subject IDs
true labels
predictions
raw probabilities
metrics
confusion matrix
training history where applicable
timestamp
Git commit
```

This supports later calibration and system integration.

---

# 68. FAILURE CASE ANALYSIS

The EEG evaluation should preserve representative failure cases such as:

- confident wrong Left prediction;
- confident wrong Right prediction;
- ambiguous probability;
- subject with poor generalization;
- inconsistent run performance;
- model disagreement between CSP+LDA and EEGNet.

These cases are useful inputs to the later uncertainty/shared-autonomy evaluation.

---

# 69. MODEL DISAGREEMENT ANALYSIS

A useful analysis may compare trials where:

```text
CSP+LDA predicts Left
EEGNet predicts Right
```

or vice versa.

This is not a mandatory standalone experiment, but it may reveal:

- subject-specific strengths;
- confidence differences;
- calibration issues.

The project should not automatically ensemble the models.

No ensemble is currently approved.

---

# 70. ENSEMBLE STATUS

Combining CSP+LDA and EEGNet into an ensemble is **not part of the locked core architecture**.

The architecture treats them as alternative decoders/baselines.

An ensemble may later be explored only if:

- scientifically justified;
- approved;
- and separately evaluated.

Do not silently combine probabilities to improve performance.

---

# 71. NEURAL FEATURE INTERPRETABILITY

Possible optional analyses include:

- learned spatial-filter inspection;
- temporal kernel analysis;
- saliency;
- feature visualization.

None are mandatory for the core system.

Do not add complex explainability methods merely for presentation.

---

# 72. CSP INTERPRETABILITY

CSP patterns may be visualized as scalp maps.

This can help check whether discriminative patterns are plausible for motor-imagery EEG.

However:

- CSP patterns are discriminative mathematical patterns;
- they are not exact source-localization results.

Final wording must remain cautious.

---

# 73. TRAINING LOGGING

EEGNet training should log:

- epoch number;
- training loss;
- validation loss;
- selected validation metric;
- learning rate if changing;
- checkpoint events.

Optional:

- training time;
- device.

The training log should be machine-readable where practical.

---

# 74. NO SCREENSHOT-ONLY RESULTS

A graph shown in a notebook or dashboard is not sufficient evidence.

Every plot should be reproducible from:

```text
saved raw results
```

For example:

```text
predictions.csv
training_history.csv
metrics.json
```

---

# 75. BASELINE RESULTS MUST BE PRESERVED

If EEGNet performs better, keep the CSP+LDA result.

If CSP+LDA performs better, keep the EEGNet result.

Do not overwrite results to present only the preferred model.

The comparison is part of the research.

---

# 76. MODEL SELECTION FOR DOWNSTREAM INTEGRATION

The model used in the final shared-autonomy pipeline should be selected using an approved criterion.

Possible selection factors include:

- balanced accuracy;
- calibration quality;
- probability stability;
- cross-subject behavior;
- computational practicality.

The model with the highest accuracy is not automatically the best downstream choice.

This decision should be made only after calibration evaluation.

---

# 77. DOWNSTREAM MODEL IDENTITY MUST BE EXPLICIT

Every full-system experiment must record whether EEG evidence came from:

```text
CSP+LDA
```

or:

```text
EEGNet / compact CNN
```

The final paper/report must not mix results from different decoders without saying so.

---

# 78. SIMULATED PROBABILITY STREAMS

The Bayesian/shared-autonomy modules are allowed to use synthetic probability streams during development.

Example:

```text
[0.55, 0.45]
[0.63, 0.37]
[0.78, 0.22]
```

This allows the cognition layer to be tested independently.

Synthetic probability tests must be clearly labeled.

They are not EEG results.

---

# 79. FULL INTEGRATION REQUIREMENT

Before the project is considered complete, the system must support:

```text
real PhysioNet EEG epoch
→ real trained decoder
→ real decoder probability
→ calibration
→ Bayesian update
→ uncertainty
→ shared autonomy
```

Synthetic evidence alone is insufficient for the final integrated system.

---

# 80. OFFLINE REPLAY

The trained decoder may be invoked on prerecorded EEG epochs in sequence.

The UI should describe this as:

> **Offline EEG Replay**

or:

> **Simulated Real-Time BCI**

Never:

> **Live EEG**

unless future hardware acquisition is actually implemented.

---

# 81. DECODER LATENCY

Inference latency may be recorded during replay.

However, because the current system is offline and runs on prerecorded data, decoder runtime must not be misrepresented as measured end-to-end live BCI latency.

It is only:

> **software inference/runtime latency under the tested hardware configuration.**

---

# 82. MODEL VALIDITY GATES

Before a decoder can be used downstream, it should pass the following gates.

## Gate 1 — Input validity

- expected channels;
- expected channel order;
- expected epoch shape;
- finite values.

## Gate 2 — Model validity

- checkpoint loads;
- prediction runs;
- output dimensions correct;
- probability normalization correct.

## Gate 3 — Scientific validity

- correct task;
- correct split;
- no leakage;
- metrics generated from unseen evaluation data.

## Gate 4 — Probability validity

- raw probabilities available;
- calibration evaluation possible.

Only then should it be connected to Bayesian goal inference.

---

# 83. MODEL FAILURE CONDITIONS

A model experiment should fail explicitly if:

- a split is empty;
- one class is absent from training;
- channel order changes unexpectedly;
- checkpoint does not match input shape;
- probabilities contain NaN;
- probabilities fail normalization;
- subject metadata is lost;
- test data was accidentally used in fitting.

A software run that produces numbers despite these failures is not a valid experiment.

---

# 84. REPRODUCIBILITY CONFIGURATION

An EEG experiment configuration should eventually include fields such as:

```yaml
dataset:
  name: physionet_eegbci
  version: "1.0.0"
  subjects: [...]
  runs: [4, 8, 12]

preprocessing:
  l_freq: TBD
  h_freq: TBD
  reference: TBD
  epoch_tmin: TBD
  epoch_tmax: TBD
  baseline: TBD
  artifact_policy: TBD
  resample_hz: null

split:
  strategy: TBD
  seed: TBD

csp_lda:
  n_components: TBD
  regularization: TBD

eegnet:
  architecture: TBD
  batch_size: TBD
  learning_rate: TBD
  optimizer: TBD
  epochs: TBD
  dropout: TBD
  seed: TBD
```

The `TBD` fields are deliberate.

---

# 85. SCIENTIFIC VERIFICATION AFTER PREPROCESSING

Before training:

1. inspect representative raw EEG;
2. inspect representative filtered EEG;
3. inspect PSD before/after filtering;
4. inspect event mapping;
5. inspect epoch count;
6. inspect epoch shape;
7. inspect class balance;
8. inspect channel order;
9. verify no NaN/Inf;
10. verify subject/trial metadata;
11. verify split.

---

# 86. SCIENTIFIC VERIFICATION AFTER CSP+LDA

Verify:

- CSP fitted only on training data;
- number of CSP components;
- transformed feature dimensions;
- LDA class order;
- probability output;
- validation/test metrics;
- confusion matrix;
- subject-wise behavior where applicable.

Optional but useful:

- inspect CSP spatial patterns.

---

# 87. SCIENTIFIC VERIFICATION AFTER EEGNET

Verify:

- architecture matches documented implementation;
- input tensor shape;
- loss/output compatibility;
- training curve;
- validation curve;
- checkpoint selection;
- final test metrics;
- class order;
- probability vector;
- subject-level failure cases.

---

# 88. REQUIRED MODEL COMPARISON TABLE

The final results phase should be capable of producing a table conceptually like:

| Metric | CSP + LDA | EEGNet |
|---|---:|---:|
| Accuracy | measured | measured |
| Balanced Accuracy | measured | measured |
| Precision | measured | measured |
| Recall | measured | measured |
| F1 | measured | measured |
| Calibration metric | measured later | measured later |
| Parameter/complexity note | recorded | recorded |

No values are to be prefilled before experiments.

---

# 89. MODEL COMPARISON INTERPRETATION

Possible valid outcomes:

## EEGNet improves accuracy

Interpret whether the improvement is:

- consistent across subjects;
- accompanied by better/worse calibration;
- robust in cross-subject conditions.

## CSP+LDA performs similarly

This suggests a compact classical model may be sufficient for this task.

## CSP+LDA performs better

This is scientifically meaningful and may indicate:

- limited data;
- subject variability;
- neural-model overfitting;
- preprocessing/model mismatch.

The project must not hide any of these outcomes.

---

# 90. CALIBRATION HANDOFF

The output of this document's methodology is:

```text
raw probability vector
```

The next module receives:

```text
true label
raw probabilities
split metadata
model ID
```

and evaluates calibration.

The calibration document must define:

- calibration concept;
- method selection;
- fitting partition;
- ECE;
- Brier Score;
- reliability diagram;
- use in downstream Bayesian inference.

---

# 91. BAYESIAN HANDOFF

After calibration:

```text
calibrated Left/Right evidence
```

is passed through the separate application goal-mapping policy before Bayesian goal inference.

The decoder does not know Search & Rescue semantics.

This separation remains mandatory.

---

# 92. BINARY EEG-TO-GOAL ISSUE — STILL UNRESOLVED

The EEG decoder produces:

```text
P(Left MI | EEG)
P(Right MI | EEG)
```

The Search & Rescue scenario may contain more than two goals.

No model code may hardwire:

```text
Left = Victim A
Right = Victim B
```

as a permanent assumption.

The approved options remain unresolved:

1. two active goals at a time;
2. hierarchical binary selection;
3. abstract binary priority/choice;
4. future multiclass EEG.

The ML layer ends at class evidence.

---

# 93. CODE ARCHITECTURE

Recommended files:

```text
src/eeg/
    loader.py
    preprocessing.py
    epochs.py
    visualization.py
    replay.py

src/models/
    csp_lda.py
    eegnet.py
    inference.py
```

Supporting:

```text
src/evaluation/
    eeg_metrics.py

tests/
    test_loader.py
    test_preprocessing.py
    test_epochs.py
    test_csp_lda.py
    test_eegnet.py
    test_decoder_interface.py
```

Exact filenames may be refined later, but module boundaries should remain.

---

# 94. PREPROCESSING MODULE RESPONSIBILITY

`preprocessing.py` should contain signal-processing operations.

It must not contain:

- dataset downloading;
- model training;
- Bayesian logic;
- Search & Rescue logic.

---

# 95. EPOCH MODULE RESPONSIBILITY

`epochs.py` should contain:

- annotation/event conversion;
- task mapping;
- epoch creation;
- metadata preservation;
- epoch validation.

It must not silently redefine the target task.

---

# 96. CSP+LDA MODULE RESPONSIBILITY

`csp_lda.py` should contain:

- model definition;
- fitting;
- prediction;
- probabilities;
- serialization;
- metadata.

---

# 97. EEGNET MODULE RESPONSIBILITY

`eegnet.py` should contain:

- architecture;
- training;
- inference;
- checkpoint handling;
- probability output.

It must not include downstream Bayesian logic.

---

# 98. INFERENCE WRAPPER RESPONSIBILITY

`inference.py` should provide a consistent model-neutral interface.

Conceptual usage:

```python
decoder = load_decoder(model_id)
prediction = decoder.predict_proba(epoch)
```

Downstream code should not need:

```python
if model_type == "eegnet":
    ...
elif model_type == "csp":
    ...
```

throughout the codebase.

---

# 99. UNIT TESTS — PREPROCESSING

Tests should verify where practical:

- output finite;
- output shape;
- channel order preserved;
- deterministic fixed preprocessing;
- invalid parameters rejected;
- no silent resampling.

---

# 100. UNIT TESTS — CSP+LDA

Tests should verify:

- fitting works on synthetic EEG-like data;
- prediction shape;
- probability shape;
- probabilities normalized;
- save/load round trip;
- class order preserved.

---

# 101. UNIT TESTS — EEGNET

Tests should verify:

- forward pass;
- expected tensor dimensions;
- output shape;
- finite logits;
- probability conversion;
- checkpoint save/load;
- tiny training smoke test.

A unit test should not require full dataset training.

---

# 102. INTEGRATION TEST

A minimal integration test should support:

```text
synthetic or small validated EEG epoch
→ decoder
→ probability vector
```

Then later:

```text
probability vector
→ calibrator
```

The full Search & Rescue environment should not be required to test the EEG model.

---

# 103. DEVELOPMENT ORDER

The approved order remains:

## Stage 1 — Loader

No preprocessing/model yet.

## Stage 2 — Inspection

Validate real EEG.

## Stage 3 — Preprocessing + epochs

Freeze approved preprocessing settings first.

## Stage 4 — CSP+LDA

Establish baseline.

## Stage 5 — EEGNet

Train neural decoder.

## Stage 6 — Compare

Generate valid metrics and failure cases.

## Stage 7 — Calibration handoff

Export raw probabilities and labels.

## Stage 8 — Offline replay integration

Connect selected decoder to downstream cognition.

---

# 104. FIRST MODEL BEFORE EEGNET

The project should complete CSP+LDA before relying on EEGNet.

Reasons:

- establishes data pipeline;
- exposes leakage;
- provides quick baseline;
- validates labels;
- provides probability outputs;
- allows downstream work to begin earlier.

This does not prohibit parallel preparation of the EEGNet module once interfaces are stable.

---

# 105. AI-ASSISTED IMPLEMENTATION RULE

Codex may generate much of the code.

However, the project owner must verify:

- what data enters each model;
- which split is used;
- what CSP fits on;
- class meaning;
- output probabilities;
- metric calculation;
- checkpoint identity.

The project must not treat “code runs” as equivalent to “methodology is correct.”

---

# 106. CODEX TASK-SCOPE RULE

Each implementation ticket should remain narrow.

Example:

> Implement CSP+LDA only using the already approved epochs and split manifest. Fit CSP only on training folds. Expose `predict_proba`. Add tests. Do not modify preprocessing or split logic.

This is preferred over:

> Build the whole EEG pipeline.

---

# 107. EXPERIMENT LOGGING

Every EEG model experiment should log:

```text
experiment_id
dataset version
subjects
runs
preprocessing config
split ID
model type
model hyperparameters
random seed
training metrics
validation metrics
test metrics
predictions
probabilities
class order
checkpoint ID
Git commit
```

---

# 108. NO FINAL METRICS UNTIL VERIFIED

Do not include a result in:

- README;
- resume;
- technical report;
- portfolio;
- application materials

unless:

1. it came from an actual experiment;
2. the split was validated;
3. the metric calculation was checked;
4. the configuration is traceable.

---

# 109. FAILURE ANALYSIS IS REQUIRED

For each final model, preserve:

- typical correct trial;
- ambiguous trial;
- confident incorrect trial;
- subject with weak performance;
- any systematic class bias;
- any major run variability.

This material will strengthen the later discussion and uncertainty rationale.

---

# 110. CLAIM BOUNDARIES

Allowed after implementation:

> “Implemented CSP+LDA and EEGNet-based decoders for Left- versus Right-hand motor imagery using PhysioNet EEG.”

Allowed:

> “Compared classical and neural decoding under a leakage-safe evaluation protocol.”

Allowed only if implemented:

> “Evaluated cross-subject generalization.”

Not allowed before evidence:

> “EEGNet outperformed CSP+LDA.”

Not allowed:

> “The model reads human intention directly.”

Not allowed:

> “The model understands rescue goals.”

Not allowed:

> “Real-time EEG decoding” when using only prerecorded replay.

Preferred:

> “Offline EEG replay with simulated real-time inference.”

---

# 111. OUT-OF-SCOPE ML FEATURES

Not required:

- Transformers for EEG;
- LLMs;
- RAG;
- graph neural networks;
- generative EEG models;
- GAN augmentation;
- complex ensemble;
- reinforcement-learning EEG decoder;
- source localization;
- self-supervised pretraining;
- federated learning;
- cloud training pipeline.

These may only be added if a later research question justifies them.

---

# 112. OPEN METHODOLOGY DECISIONS

The following remain explicitly unresolved:

## Preprocessing

- exact band-pass;
- reference;
- resampling;
- artifact policy;
- epoch interval;
- baseline correction;
- channel reduction.

## CSP+LDA

- number of CSP components;
- covariance regularization;
- exact LDA options.

## EEGNet

- exact architecture variant;
- kernel/filter dimensions;
- dropout;
- optimizer;
- learning rate;
- batch size;
- number of epochs;
- checkpoint selection metric;
- early stopping.

## Evaluation

- exact subject split;
- within-subject protocol;
- cross-subject fold structure;
- number of random seeds;
- hyperparameter-search procedure.

## Downstream

- calibration method;
- EEG-to-goal mapping.

No unresolved item should be frozen by Codex without approval.

---

# 113. DECISIONS THAT SHOULD BE FROZEN BEFORE FINAL TRAINING

Before final reportable experiments, the project should explicitly lock:

1. T0 handling;
2. band-pass filter;
3. reference;
4. epoch interval;
5. baseline correction;
6. artifact policy;
7. channel policy;
8. CSP configuration;
9. EEGNet architecture;
10. training procedure;
11. split protocol;
12. model-selection criterion;
13. number of seeds/repetitions;
14. calibration-fitting strategy.

Once frozen, those settings belong in:

- configuration;
- `DECISIONS.md`;
- experiment logs;
- final methodology.

---

# 114. ACCEPTANCE CRITERIA — EEG SIGNAL PROCESSING & ML

The EEG/ML subsystem is correctly implemented when:

1. runs 4/8/12 are used for the approved initial task;
2. T1/T2 semantics are correct;
3. T0 policy is explicit;
4. preprocessing is reproducible;
5. channel order is preserved;
6. epoch shape is validated;
7. labels and metadata remain aligned;
8. train/validation/test boundaries are explicit;
9. no trial/window leakage occurs;
10. CSP is fitted only on training data;
11. LDA outputs class probabilities;
12. EEGNet receives the correct input dimensions;
13. EEGNet checkpointing is reproducible;
14. raw probabilities are saved;
15. class ordering is explicit;
16. CSP+LDA and EEGNet are evaluated fairly;
17. subject-wise results can be generated;
18. cross-subject evaluation can be supported once its protocol is frozen;
19. calibration can consume the stored raw probabilities;
20. the decoder interface is model-neutral;
21. synthetic tests verify output contracts;
22. real EEG experiments produce traceable result artifacts;
23. failure cases are preserved;
24. no Search & Rescue goal semantics are embedded inside the EEG model;
25. no unsupported performance or live-BCI claims are made.

---

# 115. CURRENT METHODOLOGY SUMMARY

The EEG subsystem begins with real prerecorded PhysioNet EEGBCI data from runs 4, 8, and 12 and performs a leakage-safe Left-vs-Right motor-imagery decoding task. After validated channel handling, signal preprocessing, event extraction, and epoch construction, the same underlying trial definitions should support two mandatory model paths: a classical **CSP + LDA** baseline and an **EEGNet / approved compact CNN** neural decoder. The initial M1 preprocessing/epoching policy is fixed by D-031 through D-039: 7–30 Hz band-pass, average EEG reference, canonical -1.0-to-+4.0-second epochs, +1.0-to-+2.0-second initial CSP crop, `baseline=None`, the approved 150 µV peak-to-peak rejection policy without ICA/interpolation, T0 excluded from binary training while provenance is preserved, all 64 channels, no resampling, and MNE Epochs/FIF as the canonical processed representation/persistence format. CSP must be fitted only on training data, and EEGNet must be trained and selected through non-test partitions. Both models must expose explicit normalized class-probability vectors through a common decoder interface. CSP settings, EEGNet hyperparameters, the final split protocol, and calibration strategy remain unresolved until explicitly approved. The EEG subsystem ends at probabilistic Left/Right neural evidence and must not embed Search & Rescue goal semantics.

---

# 116. NEXT DOCUMENT

The next planned document is:

**`09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md` — Probability Calibration & Uncertainty Methodology**

That document should define:

- raw classifier confidence versus calibrated probability;
- why calibration matters for shared autonomy;
- calibration-data partitioning;
- candidate calibration methods;
- reliability diagrams;
- Expected Calibration Error;
- Brier Score;
- entropy;
- normalized entropy where appropriate;
- confidence/autonomy state interpretation;
- uncertainty propagation;
- failure cases;
- calibration ablation;
- and the interface into Bayesian goal inference.

The exact calibration technique and confidence thresholds must remain unresolved until they are explicitly selected through the approved methodology process.
