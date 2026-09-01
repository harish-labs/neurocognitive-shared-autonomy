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

## D-030 — EEGBCI Loader Montage

**Status:** APPROVED

For the PhysioNet EEGBCI loader/data pipeline, use:

```text
MNE EEGBCI channel-name standardization:
mne.datasets.eegbci.standardize(raw)

Montage:
standard_1005
```

Basis:

- the MNE EEGBCI workflow standardizes EEGBCI channel names with `eegbci.standardize(raw)`;
- `standard_1005` was successfully attached to an actual EEGBCI recording during M1-T01 verification;
- all 64 EEG channels received plausible channel-position metadata;
- real subject 1 runs 4, 8, and 12 loaded successfully under this workflow.

Scope limitation:

This decision applies to the EEGBCI loader/data pipeline montage choice only.

It does not approve or freeze unrelated preprocessing choices such as:

- filtering;
- EEG reference;
- epoch interval;
- baseline correction;
- artifact handling;
- resampling;
- T0 policy.

---

## D-031 — M1 EEG Band-Pass Filter

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-001

**Decision:**

```text
Band-pass filter: 7–30 Hz
```

**Context:** M1-T03 requires an explicit motor-imagery filter range before preprocessing may be implemented.

**Alternatives considered:** a different motor-related band; leaving the range unresolved.

**Rationale:** 7–30 Hz is an established motor-imagery CSP starting range covering sensorimotor mu/beta activity and was explicitly approved by the Project Owner for the initial pipeline.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `docs/15_IMPLEMENTATION_BLUEPRINT.md`, `src/eeg/preprocessing.py` when separately authorized.

**Implementation consequence:** M1-T03 may use 7–30 Hz once an implementation ticket is separately authorized. This decision alone does not authorize coding.

**Approved by:** Project Owner

---

## D-032 — M1 EEG Reference

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-002

**Decision:**

```text
EEG reference: average EEG reference
```

**Context:** The preprocessing pipeline requires an explicit reference strategy rather than a library default.

**Alternatives considered:** retain the dataset reference; another justified reference strategy.

**Rationale:** A common average EEG reference is appropriate for the full 64-channel initial scalp EEG configuration and was explicitly approved for M1 preprocessing.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `src/eeg/preprocessing.py` when separately authorized.

**Implementation consequence:** M1-T03 may apply average EEG referencing consistently once separately authorized. Exact code must not introduce an unapproved alternative reference.

**Approved by:** Project Owner

---

## D-033 — M1 Epoch Interval and CSP Training Crop

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-003

**Decision:**

```text
Canonical task epoch: -1.0 s to +4.0 s relative to cue onset
Initial CSP training crop: +1.0 s to +2.0 s relative to cue onset
```

**Context:** Event-to-epoch timing must be explicit before epoch construction and the initial CSP baseline.

**Alternatives considered:** a shorter task epoch; a different post-cue CSP analysis window.

**Rationale:** The approved scheme preserves a broader cue-relative epoch while defining a later post-cue CSP analysis window that avoids using the immediate cue-onset response as the initial CSP training segment.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `src/eeg/epochs.py` for canonical epochs, and `src/models/csp_lda.py` for the later CSP crop when each task is authorized.

**Implementation consequence:** M1-T03 may construct -1.0-to-4.0-second epochs. The +1.0-to-2.0-second crop is reserved for the CSP baseline stage and must not silently replace the canonical stored epoch.

**Approved by:** Project Owner

---

## D-034 — M1 Baseline Correction

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-004

**Decision:**

```text
baseline = None
```

**Context:** Baseline behavior must be explicit because it changes epoch values and downstream covariance structure.

**Alternatives considered:** pre-cue baseline correction; another explicit baseline interval.

**Rationale:** The initial CSP-oriented motor-imagery pipeline will not apply baseline subtraction; the choice is explicit rather than inherited from an MNE default.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `src/eeg/epochs.py` when separately authorized.

**Implementation consequence:** M1-T03 epoch construction must explicitly use no baseline correction.

**Approved by:** Project Owner

---

## D-035 — M1 Artifact-Handling Policy

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-005

**Decision:**

```text
No ICA.
No automatic bad-channel interpolation.
Reject epochs with EEG peak-to-peak amplitude greater than 150 µV.
Record rejected epochs and the rejection reason/threshold.
```

**Context:** M1-T03 needs a simple, auditable artifact policy without silently introducing a complex cleaning pipeline.

**Alternatives considered:** ICA-based cleaning; automatic interpolation; no amplitude-based rejection; a different fixed threshold.

**Rationale:** A fixed epoch-level amplitude rule is transparent and reproducible while avoiding unapproved, higher-complexity artifact-removal methods.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `src/eeg/epochs.py` and/or `src/eeg/preprocessing.py` when separately authorized.

**Implementation consequence:** The initial pipeline may reject epochs only under the approved 150 µV peak-to-peak rule; rejection accounting must be retained. ICA and automatic interpolation remain out of scope unless later approved.

**Approved by:** Project Owner

---

## D-036 — M1 T0 / Rest Handling

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-006

**Decision:**

```text
Exclude T0 from the primary binary epoch/training dataset.
Use T1 = imagined left fist and T2 = imagined right fist as the two target classes.
Preserve original T0 annotations in raw data and inspection/provenance information.
Do not create a third classifier class.
```

**Context:** The initial project task is binary Left-vs-Right motor imagery, but T0 rest annotations are present in EEGBCI recordings.

**Alternatives considered:** three-class Rest/Left/Right; creating separate T0 training epochs; using T0 only in a later exploratory experiment.

**Rationale:** Excluding T0 from the primary classifier preserves the approved binary task while retaining the source annotation semantics for provenance and later analysis.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `src/eeg/epochs.py` when separately authorized.

**Implementation consequence:** M1-T03 must map only T1/T2 into binary model epochs and must not delete or reinterpret T0 annotations in the underlying raw recording.

**Approved by:** Project Owner

---

## D-037 — M1 Channel Policy

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-007

**Decision:**

```text
Preserve all 64 validated EEG channels.
No channel reduction in M1-T03.
```

**Context:** A reduced motor-cortex subset had not been approved, and silent channel selection would add a scientific assumption.

**Alternatives considered:** a fixed C3/Cz/C4-style subset; another fixed subset; training-only channel selection.

**Rationale:** Keeping all validated channels makes the initial preprocessing stage neutral and preserves information for later controlled channel-ablation/selection studies.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `src/eeg/preprocessing.py`, `src/eeg/epochs.py` when separately authorized.

**Implementation consequence:** M1-T03 must preserve the loader's validated 64-channel order and must not silently reduce channels.

**Approved by:** Project Owner

---

## D-038 — M1 Sampling-Rate Policy

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-008

**Decision:**

```text
No resampling in M1-T03.
Preserve the native validated EEGBCI sampling rate of 160 Hz.
```

**Context:** Resampling was optional and no computational or methodological need had been established for the initial preprocessing stage.

**Alternatives considered:** downsampling to another rate; another explicitly justified resampling strategy.

**Rationale:** Native 160 Hz sampling adequately represents the approved 7–30 Hz band and avoids an unnecessary transformation in the initial pipeline.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `src/eeg/preprocessing.py` when separately authorized.

**Implementation consequence:** M1-T03 must retain validated 160 Hz sampling and must not call a resampling operation unless this decision is superseded.

**Approved by:** Project Owner

---

## D-039 — M1 Processed EEG Representation and Persistence

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-009

**Decision:**

```text
Canonical in-memory processed representation: MNE Epochs.
When processed epochs are persisted, save them as MNE FIF epoch files using the *-epo.fif naming convention.
```

**Context:** The processed-data representation must preserve channel order/names, sampling rate, events, timing, and provenance rather than relying on bare arrays with implicit metadata.

**Alternatives considered:** NumPy arrays plus separate metadata; another transparent structured format; no persistence contract.

**Rationale:** MNE Epochs/FIF is native to the approved EEG stack and preserves the metadata needed to audit preprocessing and downstream model inputs.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `src/eeg/epochs.py` when separately authorized.

**Implementation consequence:** M1-T03 APIs should expose MNE Epochs as the canonical processed object. Any persisted processed epoch artifact must use FIF; model-specific NumPy/PyTorch arrays may be derived later without replacing the canonical representation.

**Approved by:** Project Owner

---

## D-040 — EEG Train / Validation / Test Evaluation Tracks

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-010

**Decision:**

```text
Use two explicitly separated EEG evaluation tracks.

Within-subject evaluation:
- deterministic, class-stratified 60% train / 20% validation / 20% test split;
- grouping unit is the original trial;
- no trial or derived window may cross partitions.

Cross-subject evaluation:
- subject-level 70% train / 15% validation / 15% test split;
- governed further by D-041 and D-042.

Within-subject and cross-subject results must be reported separately and must not be mixed into one unlabeled average.
```

**Context:** Decoder development needs a frozen train/validation/test boundary while preserving the scientific distinction between personalized within-subject decoding and unseen-subject generalization.

**Alternatives considered:** one undifferentiated split for all questions; cross-validation only; no fixed final test partition.

**Rationale:** Separate evaluation tracks answer different scientific questions while retaining a protected test set and explicit leakage boundaries.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, `docs/18_METRICS_AND_EVALUATION.md`, split-manifest utilities, CSP/LDA and EEGNet evaluation when separately authorized.

**Implementation consequence:** A later split-manifest ticket may implement these partition contracts. If a subject does not contain enough retained class trials to satisfy the approved class-stratified within-subject split, implementation must report the condition rather than silently substitute another scientific split rule.

**Approved by:** Project Owner

---

## D-041 — Primary Cross-Subject Evaluation Protocol

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-011

**Decision:**

```text
Primary cross-subject protocol:
fixed subject-held-out 70% train / 15% validation / 15% test split.

A subject must belong to exactly one partition.
No trial from a validation/test subject may appear in training.

Leave-one-subject-out or grouped subject K-fold may be added later only as explicitly authorized secondary analyses; they are not the primary protocol.
```

**Context:** Cross-subject evaluation must measure generalization to people not represented in model fitting while remaining computationally practical for the full EEGBCI cohort and both decoder families.

**Alternatives considered:** leave-one-subject-out as the primary protocol; grouped subject K-fold as the primary protocol; trial-level random splitting across subjects.

**Rationale:** A fixed held-out subject split gives a genuinely unseen final test cohort, preserves a validation cohort for model development, and avoids repeated full-cohort retraining as the primary experiment.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, `docs/18_METRICS_AND_EVALUATION.md`, split-manifest utilities, model evaluation code when separately authorized.

**Implementation consequence:** Cross-subject split code must enforce disjoint subject IDs across train, validation, and test and preserve subject-wise reporting.

**Approved by:** Project Owner

---

## D-042 — Fixed Held-Out Subject Strategy

**Status:** APPROVED

**Date:** 2026-08-30  
**Resolves:** U-012

**Decision:**

```text
After the approved preprocessing/QC boundary, form the eligible subject list.
Use one deterministic shuffle with fixed seed 42.
Freeze the resulting subject IDs in a versioned split manifest before model fitting.

For the full 109-subject eligible EEGBCI cohort, freeze:
- 76 train subjects
- 16 validation subjects
- 17 final test subjects

Every trial from a subject remains in that subject's partition.
Final test subjects must not be used for CSP fitting, EEGNet training, hyperparameter selection, calibration fitting, threshold tuning, or learned adaptation.
```

**Context:** The held-out-subject strategy must be reproducible and frozen before model development to prevent subject-selection leakage and test-set tuning.

**Alternatives considered:** hand-picking subjects; reshuffling per run/seed; exposing test subjects during model selection.

**Rationale:** A single seeded subject assignment gives a reproducible protected final test cohort while preserving the approved 70/15/15 cross-subject structure.

**Affected documents/modules:** `docs/06_DATASET_AND_DATA_PIPELINE.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, split-manifest utilities, experiment configuration and evaluation code when separately authorized.

**Implementation consequence:** The manifest must record the seed, eligible subject IDs, partition subject IDs, counts, and provenance. If preprocessing/QC produces an eligible cohort size other than 109, do not silently invent a different count-allocation rule; report the eligible count for reviewer decision before freezing a final subject manifest.

**Approved by:** Project Owner

---

## D-043 — Final CSP Configuration

**Status:** APPROVED

**Date:** 2026-08-31  
**Resolves:** U-013

**Decision:**

```text
Evaluate CSP n_components ∈ {2,4,6,8} using training/validation only, with 4 as the default candidate.
Use log-variance CSP features.
Use primary baseline covariance regularization reg=None.
Use standard LDA with probability output.
Select n_components using validation performance only.
The protected test partition must not influence selection.
The CSP crop remains the already-approved +1.0 s to +2.0 s from D-033.
Retain all 64 channels.
No test-set fitting or tuning.
```

**Context:** The classical CSP + LDA baseline requires a fixed, leakage-safe configuration and a bounded component-count selection rule before a later implementation ticket can be considered.

**Alternatives considered:** fixing one component count without validation; searching an unrestricted component range; covariance regularization as the primary baseline; using the protected test partition for model selection.

**Rationale:** The approved candidate set permits limited validation-only model selection while preserving a clear default, the already-approved CSP crop and channel policy, a standard interpretable log-variance CSP + LDA baseline, and strict final-test protection.

**Affected documents/modules:** `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, `docs/18_METRICS_AND_EVALUATION.md`, configuration/state documentation, and `src/models/csp_lda.py` only when separately authorized.

**Implementation consequence:** This decision resolves U-013 but does not authorize CSP/LDA implementation. A separate explicit `CURRENT_TASK.md` ticket is required before code, fitting, tuning, or evaluation begins. U-014 and all later unresolved decisions remain unchanged.

**Approved by:** Project Owner

---

## D-044 — CSP Component Selection Rule Supplement

**Status:** APPROVED

**Date:** 2026-08-31  
**Supplements:** D-043

**Decision:**

```text
Use validation balanced accuracy to select CSP n_components.
The canonical M1-T05 search must evaluate the full approved candidate set {2,4,6,8}.
If multiple candidates tie for best validation balanced accuracy, choose 4 if 4 is among the tied candidates.
Otherwise choose the smallest tied n_components.
```

**Context:** D-043 fixed the approved CSP candidate set and validation-only selection boundary, but the exact validation metric and deterministic tie-break rule were not yet recorded explicitly.

**Alternatives considered:** plain validation accuracy; evaluating only a subset of the approved candidates; arbitrary first-seen tie resolution.

**Rationale:** Validation balanced accuracy is more appropriate for guarded class-sensitive model selection, while the explicit full-set search and deterministic tie-break rule prevent silent candidate pruning and unstable branch-dependent selection behavior.

**Affected documents/modules:** `DECISIONS.md`, `src/models/csp_lda.py`, `tests/test_csp_lda.py`, and any M1-T05 reporting that states how CSP `n_components` is selected.

**Implementation consequence:** M1-T05 may update the authorized CSP+LDA baseline to score all approved candidates `{2,4,6,8}` by validation balanced accuracy, choose `4` when it is part of the best tied set, otherwise choose the smallest tied candidate, and keep the protected test partition excluded from fitting and selection. This supplement does not authorize EEGNet, calibration, Bayesian, or later modules.

**Approved by:** Project Owner

---

## D-045 — Final EEGNet Architecture

**Status:** APPROVED

**Date:** 2026-08-31  
**Resolves:** U-014

**Decision:**

```text
EEGNet compact EEG-specific architecture
input shape batch × 1 × 64 × time
all 64 EEG channels
native 160 Hz
full canonical EEGNet input epoch -1.0 s to +4.0 s
do not reuse the CSP-only +1.0 s to +2.0 s crop
F1 = 8
first temporal convolution kernel length 64 samples
same padding
no bias when followed by batch normalization
depthwise spatial convolution across all 64 channels
depth multiplier D = 2
max-norm depthwise constraint where supported
BatchNorm + ELU + average pooling
separable convolution with F2 = 16
separable temporal kernel length 16
BatchNorm + ELU + average pooling
dropout 0.5
flatten + dense 2 logits
explicit class order ("left", "right")
softmax probability output
same fixed architecture for within-subject and cross-subject tracks
no architecture search, attention, residual blocks, transformers, extra CNN depth, or test-set influence
```

**Context:** EEGNet implementation requires a fixed approved architecture before any later model-building ticket can be authorized or evaluated consistently across within-subject and cross-subject tracks.

**Alternatives considered:** a looser EEGNet-inspired design; architecture search; CSP-like temporal cropping; deeper or attention-based variants.

**Rationale:** This locks a compact, EEG-specific architecture with fixed input semantics, preserves the approved canonical epoch and channel policy, and prevents silent architectural drift or test-influenced model design.

**Affected documents/modules:** `DECISIONS.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, `docs/18_METRICS_AND_EVALUATION.md`, and a future `src/models/eegnet.py` only when separately authorized.

**Implementation consequence:** This decision resolves U-014 but does not authorize EEGNet implementation. Any later EEGNet ticket must use this fixed architecture, must keep the full canonical `-1.0 s to +4.0 s` epoch rather than the CSP-only crop, and must preserve the approved class order and test-set isolation.

**Approved by:** Project Owner

---

## D-046 — Final EEGNet Training Hyperparameters

**Status:** APPROVED

**Date:** 2026-08-31  
**Resolves:** U-015

**Decision:**

```text
two-class cross-entropy loss on two logits
Adam optimizer
learning rate 1e-3
weight decay 0
batch size 32
maximum 200 epochs
early stopping enabled, patience 20
checkpoint/model-selection metric = validation balanced accuracy
if validation balanced accuracy ties, retain the earliest checkpoint reaching the best value
random seed 42
shuffle training partition only
validation receives no gradient updates and is used only for checkpoint selection/early stopping
test/final-test must never influence training, architecture, hyperparameter selection, early stopping, or checkpoint selection
no class weighting for the primary baseline
no learning-rate scheduler for the primary baseline
use the already-approved M1-T03 epochs; no extra learned normalization, augmentation, channel selection, resampling, or additional filtering
use the same fixed training hyperparameters for within-subject and cross-subject tracks; fit separate models on their approved training partitions
after validation-only checkpoint selection, evaluate the frozen checkpoint once on the corresponding protected test partition
```

**Context:** EEGNet training requires a fixed approved optimization and checkpoint-selection policy before any later implementation ticket can proceed without silent hyperparameter drift or test leakage.

**Alternatives considered:** different optimizers; weighted losses; learning-rate schedules; augmentation or extra learned normalization; test-informed checkpointing.

**Rationale:** These settings create a bounded, reproducible primary EEGNet baseline with explicit validation-only model selection, fixed seed control, and protected test/final-test isolation across both evaluation tracks.

**Affected documents/modules:** `DECISIONS.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, `docs/18_METRICS_AND_EVALUATION.md`, and future EEGNet training code only when separately authorized.

**Implementation consequence:** This decision resolves U-015 but does not authorize EEGNet implementation. Any later EEGNet ticket must use these fixed training hyperparameters, keep validation limited to checkpoint selection and early stopping, and evaluate the frozen selected checkpoint once on the corresponding protected test partition.

**Approved by:** Project Owner

---

## D-047 — EEGNet Pooling and Depthwise Max-Norm Supplement

**Status:** APPROVED

**Date:** 2026-08-31  
**Supplements:** D-045

**Decision:**

```text
supplements D-045
first average pooling kernel (1,4), stride (1,4)
second average pooling kernel (1,8), stride (1,8)
depthwise spatial-convolution max-norm cap 1.0
no other D-045 architecture values change
D-046 remains unchanged
no architecture search or additional EEGNet variants are authorized
this decision only resolves the narrow M1-T06 implementation ambiguity
```

**Context:** M1-T06 EEGNet implementation exposed a narrow architectural ambiguity left open by D-045: the exact average-pooling kernel/stride values and the numeric depthwise max-norm cap required for a faithful, non-invented implementation.

**Alternatives considered:** leaving pooling and max-norm unspecified for implementer choice; authorizing multiple EEGNet variants; folding this clarification into a broader architecture revision.

**Rationale:** This supplements D-045 only where implementation-critical constants were missing, preserves every other approved EEGNet architecture value, leaves D-046 unchanged, and prevents silent architectural drift during M1-T06.

**Affected documents/modules:** `DECISIONS.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, and future EEGNet implementation code only when separately authorized.

**Implementation consequence:** This decision resolves only the narrow M1-T06 ambiguity for EEGNet pooling and depthwise max-norm. It does not authorize architecture search, additional EEGNet variants, or any change to other D-045 values or to D-046.

**Approved by:** Project Owner

---

## D-048 — Final Calibration Method

**Status:** APPROVED

**Date:** 2026-08-31  
**Resolves:** U-016

**Decision:**

```text
EEGNet uses temperature scaling
CSP+LDA uses sigmoid / Platt-style calibration
identity / no-calibration remains the experimental baseline
calibration remains model-specific
protected test/final-test data must not influence calibrator fitting or calibration-method choice
```

**Context:** Calibration is part of the locked project architecture, but implementation could not proceed validly without an explicit approved method choice for each decoder family and an explicit preserved no-calibration baseline.

**Alternatives considered:** one shared calibration method for all decoders; leaving the method unresolved; allowing protected test/final-test performance to drive method choice.

**Rationale:** These approvals freeze a model-specific primary calibration methodology while preserving identity / no-calibration as the experimental baseline and protecting the test/final-test partitions from method-selection leakage.

**Affected documents/modules:** `DECISIONS.md`, `docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, `docs/18_METRICS_AND_EVALUATION.md`, and future calibration code only when separately authorized.

**Implementation consequence:** This decision freezes calibration methodology only and does not itself authorize calibration implementation. A separate explicit `CURRENT_TASK.md` ticket is still required before coding. Protected test/final-test data remain excluded from calibrator fitting and calibration-method choice.

**Approved by:** Project Owner

---

## D-049 — Calibration Fitting Partition

**Status:** APPROVED

**Date:** 2026-08-31  
**Resolves:** U-017

**Decision:**

```text
existing validation partition is the calibration-fitting partition
training partition remains for decoder/model fitting
do not introduce a new split in the primary pipeline
test/final_test remain untouched and cannot influence fitting, calibration, or selection
```

**Context:** The project needed an explicit calibrator-fitting boundary that preserves the existing approved split semantics without silently introducing a fourth partition or blending model fitting with calibration fitting.

**Alternatives considered:** a new dedicated calibration split; fitting calibrators on training data; any scheme that exposes test/final-test labels during fitting or selection.

**Rationale:** Reusing the approved validation partition keeps the primary pipeline minimal and auditable while maintaining clear separation between decoder fitting, calibrator fitting, and protected final evaluation.

**Affected documents/modules:** `DECISIONS.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, `docs/18_METRICS_AND_EVALUATION.md`, and future calibration/evaluation code only when separately authorized.

**Implementation consequence:** This decision freezes calibration methodology only and does not itself authorize calibration implementation. A separate explicit `CURRENT_TASK.md` ticket is still required before coding. The training partition remains for decoder fitting, and the protected test/final-test partitions remain untouched by fitting, calibration, and selection.

**Approved by:** Project Owner

---

## D-050 — Reliability-Diagram Binning

**Status:** APPROVED

**Date:** 2026-08-31  
**Resolves:** U-018

**Decision:**

```text
primary reliability diagram and ECE use 10 equal-width confidence bins over [0,1]
report Brier Score alongside ECE
do not tune bin count or binning strategy using protected test performance
```

**Context:** Reportable calibration evaluation required a fixed primary binning rule for reliability diagrams and ECE, plus an explicit companion scalar metric, before later calibration work could be implemented and compared consistently.

**Alternatives considered:** leaving binning unresolved; adaptive or equal-frequency binning as the primary rule; tuning the bin count against protected test performance.

**Rationale:** A fixed 10-bin equal-width primary rule is simple, auditable, and reproducible, while paired Brier reporting helps prevent over-interpreting ECE alone.

**Affected documents/modules:** `DECISIONS.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, `docs/18_METRICS_AND_EVALUATION.md`, and future calibration/evaluation code only when separately authorized.

**Implementation consequence:** This decision freezes calibration methodology only and does not itself authorize calibration implementation. A separate explicit `CURRENT_TASK.md` ticket is still required before coding, and protected test performance must not be used to tune binning choices.

**Approved by:** Project Owner

---

## D-051 — Binary EEG → Multi-Goal Interaction Protocol

**Status:** APPROVED

**Date:** 2026-08-31  
**Resolves:** U-019

**Decision:**

```text
use a binary-choice interaction protocol
at each decision point expose exactly two currently valid SAR candidate goals/options: candidate A and candidate B
calibrated "left" EEG evidence supports candidate A
calibrated "right" EEG evidence supports candidate B
multi-goal SAR interaction is represented as a sequence of binary choices
do not treat the binary EEG decoder as a direct K-goal classifier
```

**Context:** The project required an explicit, non-invented interaction rule connecting the approved binary EEG decoder to the potentially multi-goal Search & Rescue setting before Bayesian goal-inference methodology could be frozen coherently.

**Alternatives considered:** permanently mapping left/right directly to fixed global SAR goals; treating the binary decoder as an arbitrary K-goal classifier; deferring the interaction protocol while implementing later Bayesian logic.

**Rationale:** A binary-choice interaction protocol preserves the approved binary EEG decoder semantics, keeps the human intent interface interpretable, and supports multi-goal SAR behavior as a controlled sequence of binary decisions without silently upgrading the decoder into a multiclass intent model.

**Affected documents/modules:** `DECISIONS.md`, `docs/10_BAYESIAN_GOAL_INFERENCE.md`, `docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, and future goal-mapping/Bayesian implementation code only when separately authorized.

**Implementation consequence:** This decision freezes the Bayesian/goal-mapping methodology only. It does not authorize Bayesian implementation. A separate explicit `CURRENT_TASK.md` ticket is still required before coding.

**Approved by:** Project Owner

---

## D-052 — Decoder Posterior → Goal Likelihood Construction

**Status:** APPROVED

**Date:** 2026-08-31  
**Resolves:** U-020

**Decision:**

```text
for the currently active binary choice, use the calibrated binary class probabilities directly as the two candidate evidence likelihood weights
combine these weights with the current prior/posterior through the sequential Bayesian update and normalize the resulting posterior
do not reinterpret binary decoder probabilities as arbitrary K-goal probabilities
route cost, path length, environmental risk/safety, planner preference, or goal desirability must not modify the intent likelihood
preserve the separation between human-intent inference and autonomous planning/safety
```

**Context:** The project needed an explicit rule for how calibrated binary decoder probabilities enter the Bayesian update without collapsing the separation between neural intent evidence and downstream planning/safety logic.

**Alternatives considered:** treating decoder probabilities as arbitrary K-goal probabilities; injecting planner or safety preferences into the intent likelihood; postponing the likelihood-construction rule until implementation time.

**Rationale:** This rule preserves the meaning of the binary calibrated evidence at the active decision boundary, supports a clean sequential Bayesian update, and prevents autonomous-planning considerations from contaminating human-intent inference.

**Affected documents/modules:** `DECISIONS.md`, `docs/10_BAYESIAN_GOAL_INFERENCE.md`, `docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md`, `docs/14_SAFETY_CRITICAL_CONTROL.md`, and future goal-mapping/Bayesian implementation code only when separately authorized.

**Implementation consequence:** This decision freezes the Bayesian/goal-mapping methodology only. It does not authorize Bayesian implementation. A separate explicit `CURRENT_TASK.md` ticket is still required before coding.

**Approved by:** Project Owner

---

## D-053 — Bayesian Prior Policy

**Status:** APPROVED

**Date:** 2026-08-31  
**Resolves:** U-021

**Decision:**

```text
primary baseline prior at the beginning of every binary decision episode is [0.5, 0.5]
no learned prior
no scenario-informed prior
no adaptive/personalized prior in the primary baseline
```

**Context:** The Bayesian module required an explicit approved prior policy so that later implementation would not silently introduce learned, scenario-biased, or personalized priors into the primary baseline.

**Alternatives considered:** learned priors; scenario-informed priors; adaptive or personalized priors in the primary baseline; leaving the prior unspecified until implementation.

**Rationale:** A uniform `[0.5, 0.5]` baseline prior is simple, transparent, and consistent with the approved binary-choice protocol while avoiding unapproved adaptive or scenario-derived bias in the primary baseline.

**Affected documents/modules:** `DECISIONS.md`, `docs/10_BAYESIAN_GOAL_INFERENCE.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, and future Bayesian implementation code only when separately authorized.

**Implementation consequence:** This decision freezes the Bayesian/goal-mapping methodology only. It does not authorize Bayesian implementation. A separate explicit `CURRENT_TASK.md` ticket is still required before coding.

**Approved by:** Project Owner

---

## D-054 — Bayesian Stopping / Commitment Rule

**Status:** APPROVED

**Date:** 2026-08-31  
**Resolves:** U-022

**Decision:**

```text
sequentially update the posterior using accepted evidence
commit candidate A or B when its posterior probability reaches or exceeds 0.90
maximum 5 accepted evidence updates per binary decision episode
if neither candidate reaches 0.90 after the fifth accepted evidence update, return UNCOMMITTED / DEFER
do not force-select the highest posterior candidate
reset the posterior to [0.5, 0.5] at the start of each new binary decision episode
```

**Context:** The Bayesian intent layer required an explicit stopping/commitment rule so that later implementation would not silently invent thresholds, maximum evidence horizons, or forced-decision behavior.

**Alternatives considered:** always choosing the highest posterior candidate; unlimited evidence accumulation; lower or higher unapproved commitment thresholds; carrying posterior state across independent binary decision episodes.

**Rationale:** This rule creates a bounded, auditable binary decision episode with a clear commitment threshold, a defined deferral outcome, and an explicit reset policy between episodes.

**Affected documents/modules:** `DECISIONS.md`, `docs/10_BAYESIAN_GOAL_INFERENCE.md`, `docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, and future Bayesian/shared-autonomy implementation code only when separately authorized.

**Implementation consequence:** D-051 through D-054 freeze the Bayesian/goal-mapping methodology only and do not authorize Bayesian implementation. A separate explicit `CURRENT_TASK.md` ticket is still required before coding.

**Approved by:** Project Owner

---

## D-055 — Confidence / Entropy Thresholds

**Status:** APPROVED

**Date:** 2026-08-31
**Resolves:** U-023

**Decision:**

```text
continue using Shannon entropy of the binary Bayesian posterior as the explicit uncertainty measure
PROCEED boundary: leading-candidate posterior >= 0.90, matching D-054
for a binary posterior, this corresponds to entropy <= approximately 0.469 bits
CONFIRM region: after the Bayesian 5-update horizon, leading posterior >= 0.75 and < 0.90
corresponding binary entropy is approximately 0.469-0.811 bits
DEFER region: after the 5-update horizon, leading posterior < 0.75
corresponding entropy is > approximately 0.811 bits
posterior thresholds are authoritative
entropy is the explicit uncertainty measure but must not create an independent contradictory decision rule
```

**Context:** The shared-autonomy layer needed fixed, interpretable uncertainty thresholds after the approved bounded binary Bayesian episode so that confidence and entropy cannot silently yield conflicting actions.

**Rationale:** The authoritative posterior boundaries preserve the approved D-054 commitment rule, while binary posterior entropy provides an explicit, equivalent uncertainty description for logging and explanation.

**Affected documents/modules:** `DECISIONS.md`, `docs/10_BAYESIAN_GOAL_INFERENCE.md`, `docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`, and future uncertainty/shared-autonomy implementation code only when separately authorized.

**Implementation consequence:** This decision freezes shared-autonomy/uncertainty policy methodology only. It does not authorize implementation. A separate explicit `CURRENT_TASK.md` ticket is still required before coding.

**Approved by:** Project Owner

---

## D-056 — Exact PROCEED / CONFIRM / DEFER Policy

**Status:** APPROVED

**Date:** 2026-08-31
**Resolves:** U-024

**Decision:**

```text
if Bayesian inference reaches D-054's >= 0.90 commitment threshold before or at update 5, output PROCEED
otherwise continue until all 5 accepted Bayesian evidence updates are exhausted
at update 5, if the strongest posterior is >= 0.75 and < 0.90, output CONFIRM for the current leading candidate
at update 5, if the strongest posterior is < 0.75, output DEFER
CONFIRM must never silently approve a goal; explicit human approval is required
human PAUSE, STOP, or OVERRIDE always takes precedence regardless of model confidence, posterior, or autonomy policy
```

**Context:** The project required an exact policy for interpreting the bounded Bayesian episode without allowing an intermediate-confidence candidate to become an autonomous goal approval.

**Rationale:** This policy retains immediate action only for the D-054 commitment boundary, requires human authority for intermediate confidence, and preserves deferral for unresolved uncertainty.

**Affected documents/modules:** `DECISIONS.md`, `docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`, and future shared-autonomy implementation code only when separately authorized.

**Implementation consequence:** This decision freezes shared-autonomy/uncertainty policy methodology only. It does not authorize implementation. A separate explicit `CURRENT_TASK.md` ticket is still required before coding.

**Approved by:** Project Owner

---

## D-057 — Prolonged-Uncertainty Fallback

**Status:** APPROVED

**Date:** 2026-08-31
**Resolves:** U-025

**Decision:**

```text
on DEFER, do not force-select the posterior argmax
do not begin autonomous movement
hold the agent stationary
request explicit human input / goal selection rather than accumulating unlimited EEG evidence
if the human provides a valid explicit choice or override, respect that human authority
if no human input is provided, remain deferred
any future binary EEG decision episode starts fresh with D-054's [0.5, 0.5] prior
do not carry the uncertain posterior into a new episode
```

**Context:** The bounded Bayesian protocol needed an explicit safe outcome for unresolved uncertainty after five accepted evidence updates.

**Rationale:** Holding position and requesting human input prevents forced intent selection or unlimited evidence accumulation while preserving the human as the final authority over the intended goal.

**Affected documents/modules:** `DECISIONS.md`, `docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`, and future shared-autonomy, safety, and human-interface implementation code only when separately authorized.

**Implementation consequence:** D-055 through D-057 freeze the shared-autonomy/uncertainty policy methodology only and do not authorize implementation. A separate explicit `CURRENT_TASK.md` implementation ticket is required before coding.

**Approved by:** Project Owner

---

## D-058 — Adaptation Mechanism / Prior Personalization

**Status:** APPROVED

**Date:** 2026-08-31
**Resolves:** U-026

**Decision:**

```text
use subject-specific, candidate-pair-specific Bayesian prior personalization
maintain counts only from explicit human-approved final choices
CONFIRM followed by explicit human acceptance may contribute the approved goal
OVERRIDE may contribute only the explicitly corrected/approved goal
PAUSE, STOP, unresolved DEFER, or autonomous PROCEED without explicit feedback do not update adaptation
never use EEG ground-truth labels, hidden test truth, task success, planner cost, or safety state as adaptation feedback
adaptation changes only the initial prior of future episodes for that same anonymous dataset subject and candidate pair
decoder, calibration, D-052 likelihood construction, Bayesian update equation, and D-055 through D-057 policy remain unchanged
adaptation OFF continues to use [0.5,0.5]
```

**Context:** The project required a narrowly bounded personalization mechanism that learns only from explicit human authority, rather than from hidden evaluation information, autonomous outcomes, or downstream planning and safety signals.

**Rationale:** Subject- and candidate-pair-specific initial-prior personalization can capture approved choice feedback while preserving the separation between decoder evidence, Bayesian likelihoods, shared-autonomy policy, and autonomous execution.

**Affected documents/modules:** `DECISIONS.md`, `docs/10_BAYESIAN_GOAL_INFERENCE.md`, `docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`, and future adaptation implementation code only when separately authorized.

**Implementation consequence:** This decision freezes adaptation methodology only. It does not authorize implementation. A separate explicit `CURRENT_TASK.md` ticket is required before coding.

**Approved by:** Project Owner

---

## D-059 — Adaptation Update Formula

**Status:** APPROVED

**Date:** 2026-08-31
**Resolves:** U-027

**Decision:**

```text
initialize each candidate pair with alpha_A = 1, alpha_B = 1
valid approved A feedback -> alpha_A += 1
valid approved B feedback -> alpha_B += 1
raw adaptive prior:
P0(A) = alpha_A / (alpha_A + alpha_B)
P0(B) = alpha_B / (alpha_A + alpha_B)
adaptation state updates only between decision episodes, never during an active Bayesian evidence sequence
adaptation ON uses the approved personalized prior
adaptation OFF continues to use D-053 [0.5,0.5]
```

**Context:** The approved adaptation mechanism needed a deterministic and auditable update rule for converting valid explicit human feedback into a future initial prior.

**Rationale:** Symmetric pseudo-count initialization yields a transparent normalized prior, and restricting updates to episode boundaries prevents adaptation from altering an active Bayesian evidence sequence.

**Affected documents/modules:** `DECISIONS.md`, `docs/10_BAYESIAN_GOAL_INFERENCE.md`, and future adaptation implementation code only when separately authorized.

**Implementation consequence:** This decision freezes adaptation methodology only. It does not authorize implementation. A separate explicit `CURRENT_TASK.md` ticket is required before coding.

**Approved by:** Project Owner

---

## D-060 — Adaptation Bounds / Warm-Up / Reset

**Status:** APPROVED

**Date:** 2026-08-31
**Resolves:** U-028

**Decision:**

```text
require 3 valid explicit feedback events for that subject/candidate pair before applying a non-uniform adaptive prior
during warm-up use [0.5,0.5]
after warm-up bound each candidate prior to [0.25,0.75] while preserving normalization
no decay/forgetting in the primary implementation
explicit reset sets alpha_A=1, alpha_B=1, update_count=0, yielding [0.5,0.5]
adaptation_enabled=False always bypasses personalization and returns [0.5,0.5]
state is keyed by anonymous dataset subject_id and candidate pair, not by global A/B slot position
every adaptation update must be traceable to the explicit feedback observation that caused it
no model retraining, threshold adaptation, evidence weighting, or raw-EEG modification
```

**Context:** Prior personalization needed explicit safeguards against premature personalization, extreme priors, cross-subject leakage, untraceable updates, and scope expansion into decoder or policy adaptation.

**Rationale:** A three-event warm-up, bounded normalized priors, symmetric reset, and anonymous subject/candidate-pair isolation make the primary implementation auditable and prevent feedback from silently changing scientific components outside the approved prior.

**Affected documents/modules:** `DECISIONS.md`, `docs/10_BAYESIAN_GOAL_INFERENCE.md`, `docs/17_EXPERIMENTAL_DESIGN.md`, `docs/18_METRICS_AND_EVALUATION.md`, and future adaptation implementation code only when separately authorized.

**Implementation consequence:** D-058 through D-060 freeze adaptation methodology only and do not authorize implementation. A separate explicit `CURRENT_TASK.md` implementation ticket is required before coding.

**Approved by:** Project Owner

---

## D-061 — Environmental Risk Values

**Status:** APPROVED

**Date:** 2026-09-01  
**Resolves:** U-029

**Decision:**

```text
Use a fixed normalized environmental-risk scale:
FREE = 0.00
LOW = 0.25
MODERATE = 0.50
HIGH = 0.75
PROHIBITED = 1.00

Blocked/obstacle cells remain a separate hard non-traversable category and must not be represented only as a high risk value.
```

**Context:** The SAR environment requires explicit, interpretable risk values before risk-aware A* planning and prohibited-hazard safety checks can be implemented reproducibly.

**Rationale:** A five-level fixed scale over [0,1] is simple, auditable, and sufficient for controlled simulated experiments while preserving the architectural distinction between soft environmental risk and hard obstacles.

**Affected documents/modules:** `DECISIONS.md`, `docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md`, `docs/14_SAFETY_CRITICAL_CONTROL.md`, future SAR environment/planner/safety code and experiment configuration.

**Implementation consequence:** Future SAR code may represent traversable environmental risk using exactly these canonical values. This decision does not by itself authorize implementation.

**Approved by:** Project Owner

---

## D-062 — Risk Normalization and Exposure Aggregation

**Status:** APPROVED

**Date:** 2026-09-01  
**Resolves:** U-030

**Decision:**

```text
The D-061 values are already canonical normalized values on [0,1].
Do not perform per-map min-max normalization, adaptive normalization, or data-dependent rescaling.
For planning, the risk contribution of a move is the risk value of the destination cell entered by that move.
Total path risk is the sum of entered-cell risk values; the start cell is not charged again as a movement risk contribution.
```

**Context:** Risk-aware planning needs an unambiguous normalization and aggregation rule so identical map semantics produce identical costs across runs and maps.

**Rationale:** Fixed normalization avoids map-dependent reinterpretation of hazard severity, while destination-cell additive exposure gives a transparent risk term that composes naturally with discrete A* movement cost.

**Affected documents/modules:** `DECISIONS.md`, `docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md`, future map/risk schemas, planner, tests, and evaluation code.

**Implementation consequence:** Future planner code may consume D-061 values directly and sum destination-cell exposure without additional normalization. This decision does not by itself authorize implementation.

**Approved by:** Project Owner

---

## D-063 — Risk Weight Lambda

**Status:** APPROVED

**Date:** 2026-09-01  
**Resolves:** U-031

**Decision:**

```text
Primary risk-aware A* weight: lambda = 2.0
Per-move planning cost for a traversable destination cell:
step_cost = 1.0 + 2.0 * risk(destination_cell)
Total path objective remains equivalent to distance + lambda * cumulative risk.
Use Manhattan distance as the heuristic over the four-connected grid.
Do not tune lambda using protected final system-test outcomes.
```

**Context:** The approved conceptual objective J = distance + lambda * risk requires a fixed primary lambda before risk-aware route behavior can be implemented and compared reproducibly.

**Rationale:** lambda = 2.0 gives simulated environmental risk meaningful influence without converting every non-zero-risk cell into a hard obstacle; one unit of maximum normalized traversable-risk exposure is weighted equivalently to two extra movement-cost units before hard safety filtering.

**Affected documents/modules:** `DECISIONS.md`, `docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md`, future planner configuration, planner tests, and planning/safety experiments.

**Implementation consequence:** Future primary A* planning must use lambda = 2.0 unless this decision is explicitly superseded. This decision does not by itself authorize implementation.

**Approved by:** Project Owner

---

## D-064 — Prohibited-Hazard Threshold

**Status:** APPROVED

**Date:** 2026-09-01  
**Resolves:** U-032

**Decision:**

```text
A hazard cell is prohibited when its canonical risk value is >= 1.00.
Under D-061, PROHIBITED = 1.00 is therefore a hard non-traversable safety condition.
HIGH = 0.75 remains traversable and is handled as soft risk through the planner cost.
Blocked/obstacle cells remain independently prohibited regardless of risk value.
The planner must not use a prohibited cell in a valid path, and the safety controller must reject any proposed transition into one.
```

**Context:** The project requires a precise boundary between traversable soft risk and hard hazard prohibition so the planner and safety controller cannot interpret the same map inconsistently.

**Rationale:** Reserving 1.00 for prohibition preserves lower risk levels as genuine soft trade-offs and keeps hard safety enforcement explicit rather than hiding it inside an arbitrarily large path cost.

**Affected documents/modules:** `DECISIONS.md`, `docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md`, `docs/14_SAFETY_CRITICAL_CONTROL.md`, future environment/planner/safety code and tests.

**Implementation consequence:** Future planning and safety modules must treat risk >= 1.00 as prohibited and must not silently relax this threshold to obtain a route. This decision does not by itself authorize implementation.

**Approved by:** Project Owner

---

## D-065 — Final No-Safe-Path Policy

**Status:** APPROVED

**Date:** 2026-09-01  
**Resolves:** U-033

**Decision:**

```text
If no route to the current human-approved goal exists after enforcing map bounds, blocked cells, and prohibited hazards, return an explicit NO_SAFE_PATH / UNREACHABLE result.
Do not execute movement.
Hold the agent stationary.
Do not relax hard safety constraints or the prohibited-hazard threshold.
Do not silently choose a different mission goal.
Log the no-safe-path event and the reason.
A new planning attempt may occur only after a relevant environment change or an explicit human-approved goal/control change.
```

**Context:** Safety and planning require a deterministic fail-safe outcome when an approved goal cannot be reached without violating hard constraints.

**Rationale:** Holding position preserves the human's authority over WHAT goal is intended while preventing the autonomy layer from trading away hard safety merely to produce a path. Explicit failure is scientifically preferable to hidden fallback behavior.

**Affected documents/modules:** `DECISIONS.md`, `docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md`, `docs/14_SAFETY_CRITICAL_CONTROL.md`, future planner/safety/shared-control integration and tests.

**Implementation consequence:** Future planner/safety integration must expose and test the explicit no-safe-path outcome. It may not switch goals or weaken hard constraints automatically. This decision does not by itself authorize implementation.

**Approved by:** Project Owner

---

## D-066 — Controlled Replanning / Runtime Environment-Change Contract

**Status:** APPROVED

**Date:** 2026-09-01

**Decision:**

```text
Represent each relevant runtime environment change by supplying a new immutable, validated replacement environment/map snapshot.
Preserve the agent's current (row, column) position and the same human-approved goal across the replacement snapshot.
Replanning may occur only after either:
1. an explicit ENVIRONMENT_CHANGED event; or
2. a safety decision with requires_replan=True together with a new validated environment snapshot.
Never repeatedly replan against an unchanged map after a rejection.
Permit at most one replan for each supplied environment-change event; any further replan requires another explicit environment-change event and another validated replacement snapshot.
If the replacement snapshot still yields NO_SAFE_PATH, hold position and stop.
PAUSE and STOP retain higher priority and do not themselves trigger autonomous replanning.
Do not substitute goals, relax blocked/prohibited safety constraints, invent stochastic/dynamic hazard behavior, or mutate the active map implicitly/hiddenly.
```

**Context:** M4-T04 completed one-plan planner → safety → environment execution, while the implementation blueprint still requires controlled replanning. A runtime contract was required so replanning could be implemented without silently inventing map-mutation semantics, retry loops, or goal/safety changes.

**Alternatives considered:** mutating the active environment object in place; automatically retrying indefinitely after any safety rejection; replanning against an unchanged map; allowing the replanner to alter the approved goal or relax hard constraints.

**Rationale:** Explicit immutable replacement snapshots make environment changes auditable and deterministic, preserve current position and human goal authority, and bound replanning so a rejected route cannot cause an uncontrolled retry loop.

**Affected documents/modules:** `DECISIONS.md`, `CURRENT_TASK.md`, `PROJECT_STATE.md`, `docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md`, `docs/14_SAFETY_CRITICAL_CONTROL.md`, `src/autonomy/execution.py` and/or a narrow replanning coordinator when separately authorized, and corresponding tests.

**Implementation consequence:** A separately authorized M4-T05 task may implement controlled replanning only under this contract. This decision does not authorize stochastic hazards, hidden map mutation, unlimited retries, goal substitution, or safety relaxation.

**Approved by:** Project Owner

---

## D-067 — Human Interaction Command Contract

**Status:** APPROVED

**Date:** 2026-09-01  
**Supplements:** D-016, D-056, D-057, D-066

**Decision:**

```text
CONFIRM
- Every confirmation request has a unique request_id.
- CONFIRM must reference the exact currently active request_id.
- A stale/non-active request_id is rejected.
- Repeating an already-consumed confirmation is an explicit duplicate / no-op and must never cause repeated approval or execution.
- CONFIRM approves only the candidate goal attached to that active request; it cannot substitute another goal.

OVERRIDE
- OVERRIDE immediately invalidates/cancels any active confirmation request and any prior autonomous goal commitment for the current control state.
- OVERRIDE must explicitly name a currently valid configured mission goal.
- An unknown/non-configured goal is rejected.
- A valid override becomes the new human-approved goal.
- Autonomous movement toward the prior goal must stop before any execution toward the override goal.
- Any future movement toward the override goal must re-enter the normal planner -> safety -> environment execution path.
- The planner may not reinterpret or replace the overridden human-approved goal.

PAUSE
- PAUSE takes immediate precedence over autonomous motion.
- Preserve current agent position, current human-approved goal, and relevant mission/control state.
- No queued autonomous action may execute while paused.
- Repeated PAUSE is idempotent and causes no repeated side effect.

STOP
- STOP is the strongest human command and terminates autonomous execution for the current episode/control session.
- STOP cannot be bypassed by CONFIRM, OVERRIDE, RESUME, model confidence, planner output, or lower-level autonomous state.
- Continuing after STOP requires an explicit reset/new episode; ordinary RESUME is not valid after STOP.

RESUME
- RESUME is supported and is valid only from PAUSED.
- RESUME never replays a previously queued autonomous action.
- Preserve the same current human-approved goal.
- Navigation after RESUME must begin from the current state through a fresh planner/safety execution request.
- If the environment changed while paused, use the already-approved D-066 controlled-replanning contract before movement.
- RESUME after STOP is invalid.

COMMAND ID / DUPLICATE PROTECTION
- Every human command has a unique non-empty command_id.
- A command_id may be consumed at most once.
- Reuse of an already-consumed command_id returns an explicit duplicate / ALREADY_CONSUMED-style outcome and must not repeat the command effect.
- M5 command handling is synchronous and deterministic; no background queue, retry worker, or asynchronous command processor is authorized.

AUTHORITY PRECEDENCE
STOP
> PAUSE
> OVERRIDE
> CONFIRM / RESUME
> shared-autonomy policy
> planner
> safety
> environment execution

Safety retains veto authority over low-level movement. Human OVERRIDE may change WHAT goal is approved, but it cannot force an unsafe low-level action or relax hard safety constraints.
```

**Context:** The shared-autonomy and human-authority specifications require explicit confirmation, override, pause, and stop behavior, while the human-interaction implementation also needs deterministic stale-request, duplicate-command, and resume semantics. These boundaries must be frozen before Codex implements an interaction state layer.

**Alternatives considered:** confirmation without request identity; accepting stale confirmations; replaying queued movement on resume; treating STOP as equivalent to PAUSE; allowing override to bypass planner/safety; asynchronous/background command queues.

**Rationale:** Request/command identity and deterministic state transitions prevent stale or duplicate human commands from causing repeated execution, while the precedence rules preserve the Project Owner-approved principle that the human controls WHAT objective and safety retains veto authority over HOW movement is executed.

**Affected documents/modules:** `DECISIONS.md`, `CURRENT_TASK.md`, `PROJECT_STATE.md`, `docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`, `src/control/shared_autonomy.py`, future `src/control/human_interaction.py`, and corresponding tests/integration tasks when separately authorized.

**Implementation consequence:** A separately authorized M5-T01 task may implement only the deterministic human-command/confirmation state layer under this contract. D-067 does not itself authorize full EEG-to-mission integration, UI callbacks, logging infrastructure, experiments, or any bypass of the accepted planner/safety/environment stack.

**Approved by:** Project Owner

---

## D-068 — Shared-Autonomy to Human-Interaction Authorization Contract

**Status:** APPROVED

**Date:** 2026-09-01  
**Supplements:** D-003, D-020, D-021, D-056, D-057, D-067

**Decision:**

```text
M5-T02 is an authorization-only integration boundary. It connects accepted SharedAutonomyDecision outputs to the accepted HumanInteractionController and produces explicit deterministic authorization/hold state. It does not execute movement, invoke the planner, call safety, step the environment, or perform replanning.

Goal identity remains symbolic at this boundary. A shared-autonomy candidate/approved goal must exactly match a currently valid configured mission-goal identifier, represented by a key in EnvironmentConfig.goals or an equivalent caller-supplied current goal registry. Do not use substring matching, fallback goals, nearest goals, planner-preferred goals, or a hard-coded Left/Right-to-victim mapping.

PROCEED:
- A structurally valid PROCEED decision with an exact currently valid symbolic goal may be adopted as the interaction state's policy-approved goal only when the interaction controller is not PAUSED and not STOPPED and no unresolved confirmation request would be bypassed.
- M5-T02 performs no movement and creates no direct planner/safety/environment call.
- Missing, invalid, stale, or non-current goal identity fails closed and holds.

CONFIRM:
- A structurally valid CONFIRM decision with an exact currently valid candidate may open one explicit ConfirmationRequest using a deterministic caller-supplied request_id.
- No autonomous goal approval occurs while confirmation is required.
- Existing active-confirmation identity and uniqueness rules from D-067/M5-T01 remain authoritative; M5-T02 may not replace or bypass an unresolved active request.
- Human CONFIRM remains the only action that approves the candidate attached to that active request.

WAITING / DEFER:
- Do not change the approved goal.
- Do not invent a confirmation candidate or force an argmax goal.
- Hold under D-057 and request human input where the accepted shared-autonomy decision requires it.

HUMAN AUTHORITY:
- STOPPED interaction state blocks policy goal adoption and confirmation opening.
- PAUSE blocks autonomous PROCEED goal adoption; no policy result may cause movement while paused.
- An already-active confirmation may remain preserved during PAUSE under D-067, and explicit human CONFIRM/OVERRIDE behavior remains owned by HumanInteractionController.
- OVERRIDE remains the human-selected approved goal and is never generated or reinterpreted by the policy bridge.
- RESUME remains an explicit human command; M5-T02 does not synthesize it or replay queued movement.

ONE HUMAN COMMAND / ONE PROCESSING PATH:
- Human commands are consumed exactly once by HumanInteractionController.
- M5-T02 must never synthesize a duplicate PAUSE, STOP, OVERRIDE, CONFIRM, or RESUME command from SharedAutonomyDecision.human_action.
- The same human action must not be processed once through shared_autonomy.py and again as a newly invented HumanCommand.
- Shared-autonomy PAUSE/STOP/OVERRIDE outputs may be observed for consistency, but the bridge must not convert them into a second human-command side effect.

POLICY-APPROVED GOAL API:
- HumanInteractionController may gain one narrow non-human-command API for adopting an accepted policy-approved symbolic goal.
- The API must validate exact current goal identity and fail closed when STOPPED, PAUSED, an unresolved confirmation would be bypassed, or the goal is not currently valid.
- This API is not a human command, consumes no command_id, creates no execution, and must not weaken D-067.

BINARY EEG / MULTI-GOAL BOUNDARY:
- M5-T02 consumes an already-produced symbolic SharedAutonomyDecision.
- It does not decide how binary EEG maps onto multiple mission goals, does not hard-code the older candidate-only interface conventions, and does not introduce multiclass EEG.

EXECUTION BOUNDARY:
- M5-T02 ends at deterministic goal authorization / confirmation / hold state.
- A later separately reviewed M5 task must connect an approved symbolic goal to the current environment's exact goal coordinate and implement interruptible planner -> safety -> environment execution while preserving PAUSE/STOP/OVERRIDE and D-066 replanning authority.
```

**Context:** M5-T01 implemented deterministic human command/confirmation state, while the accepted shared-autonomy policy still emits symbolic goal decisions and the accepted executor consumes an already-approved SAR coordinate. A narrow authorization bridge is required before any full execution integration so Codex does not invent goal-resolution, human-command duplication, or movement semantics.

**Alternatives considered:** directly combining policy, human commands, planning, safety, and movement in one large integration task; hard-coding binary EEG choices to fixed victim coordinates; converting shared-autonomy human_action fields into duplicate HumanCommand events; allowing PROCEED to bypass PAUSE or an active confirmation.

**Rationale:** Separating authorization from movement keeps human WHAT authority explicit, preserves D-067 command identity and precedence, avoids premature coupling to the synchronous route executor, and leaves interruptible execution for a separately reviewable task.

**Affected documents/modules:** `DECISIONS.md`, `CURRENT_TASK.md`, `PROJECT_STATE.md`, `src/control/shared_autonomy.py`, `src/control/human_interaction.py`, future `src/control/interaction_bridge.py`, and corresponding tests.

**Implementation consequence:** A separately authorized M5-T02 task may implement only the shared-autonomy-to-human-interaction authorization bridge under this contract. D-068 does not authorize planner/safety/environment execution, EEG/model integration, adaptation updates, UI, logging/metrics infrastructure, or experiments.

**Approved by:** Project Owner

---

# 3. UNRESOLVED DECISIONS

The following remain explicitly unresolved.

## Models

```text
None currently unresolved.
```

## Calibration

```text
None currently unresolved.
```

## Bayesian / Goal Mapping

```text
None currently unresolved.
```

## Shared Autonomy

```text
None currently unresolved.
```

## Adaptation

```text
None currently unresolved.
```

## Planning / Safety

```text
None currently unresolved.
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
