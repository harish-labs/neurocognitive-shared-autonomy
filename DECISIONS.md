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

# 3. UNRESOLVED DECISIONS

The following remain explicitly unresolved.

## Models

```text
None currently unresolved.
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
