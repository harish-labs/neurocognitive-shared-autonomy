# 06_DATASET_AND_DATA_PIPELINE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### EEG Dataset Specification, Data Governance, Preprocessing Boundaries, Leakage Prevention, and Reproducible Data Pipeline

**Document ID:** D-01  
**Document class:** Data & Neuroscience / Dataset Specification  
**Authority level:** Subordinate to the Master Authority Documents, Search & Rescue Scenario Specification, System Architecture, and Technology Stack  
**Status:** Authoritative dataset baseline; unresolved preprocessing and evaluation choices are explicitly preserved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND NON-ASSUMPTION RULE

This document defines:

- the approved EEG dataset;
- the exact task subset currently selected;
- the meaning of the dataset runs and annotations;
- how data must be downloaded and validated;
- how raw data flows toward model-ready epochs;
- what information must be preserved;
- what must never leak across training/evaluation boundaries;
- how offline EEG replay relates to the dataset;
- and which preprocessing/evaluation choices remain unresolved.

It must remain consistent with:

1. `MASTER_PROJECT_SPEC.md`
2. `01_PROJECT_CONCEPT_AND_PROBLEM.md`
3. `02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md`
4. `03_SEARCH_AND_RESCUE_SCENARIO.md`
5. `04_SYSTEM_ARCHITECTURE.md`
6. `05_TECHNOLOGY_STACK.md`

If this document conflicts with any higher-authority project document, the higher-authority document wins.

No implementation agent may silently change:

- the dataset;
- the initial motor-imagery task;
- the selected run family;
- the meaning of T0/T1/T2;
- the train/validation/test logic;
- or the public-prerecorded nature of the EEG.

Any scientifically meaningful change must be approved and recorded.

---

# 1. PURPOSE OF THE DATASET WITHIN THE PROJECT

The EEG dataset provides **real prerecorded neural evidence** for the human-intent side of the project.

Its role is not to create a standalone EEG-classification leaderboard.

Its role is to supply imperfect neural evidence to the larger architecture:

```text
EEG
→ preprocessing
→ decoder
→ probability calibration
→ Bayesian intent inference
→ uncertainty
→ shared autonomy
→ safe autonomous Search & Rescue behaviour
```

The dataset therefore supports two levels of research:

## Level 1 — EEG decoding research

Evaluate:

- CSP + LDA;
- EEGNet / compact CNN;
- probability quality;
- calibration;
- subject variability;
- cross-subject generalization.

## Level 2 — downstream shared-autonomy research

Use the decoder's probabilistic outputs as evidence for:

- Bayesian belief updating;
- uncertainty estimation;
- confidence-dependent autonomy;
- human confirmation/deferral;
- Search & Rescue goal-level control.

The downstream system must never treat a single EEG prediction as guaranteed human intention.

---

# 2. APPROVED DATASET

The approved starting dataset is:

> **PhysioNet EEG Motor Movement/Imagery Dataset (EEGMMIDB / EEGBCI), version 1.0.0**

The project accesses it through:

> **MNE-Python `mne.datasets.eegbci` utilities**

The dataset was collected using the BCI2000 system and contains motor execution and motor imagery recordings.

The official dataset contains:

- **109 subjects/volunteers**;
- **64 EEG channels**;
- **14 runs per subject**;
- recordings stored in **EDF+** format;
- a sampling frequency of **160 Hz**;
- event annotations using the task codes **T0, T1, and T2**.

These dataset-level facts have been cross-checked against the official PhysioNet dataset description and MNE EEGBCI documentation.

---

# 3. DATASET SOURCE AND CITATION IDENTITY

The source dataset should be identified consistently in future documentation.

## Dataset

**Gerwin Schalk. EEG Motor Movement/Imagery Dataset, version 1.0.0. PhysioNet, 2009.**

Dataset DOI:

```text
10.13026/C28G6P
```

## BCI2000 foundational paper

The PhysioNet resource also points to the BCI2000 publication:

**Schalk, G., McFarland, D. J., Hinterberger, T., Birbaumer, N., & Wolpaw, J. R. (2004). BCI2000: A General-Purpose Brain-Computer Interface (BCI) System. IEEE Transactions on Biomedical Engineering, 51(6), 1034–1043.**

The final Literature document should contain the full approved references.

---

# 4. COMPLETE RUN STRUCTURE

The dataset contains 14 runs for each subject.

The task mapping is:

| Run(s) | Task |
|---|---|
| **1** | Baseline — eyes open |
| **2** | Baseline — eyes closed |
| **3, 7, 11** | Motor execution — left fist vs right fist |
| **4, 8, 12** | **Motor imagery — left fist vs right fist** |
| **5, 9, 13** | Motor execution — both fists vs both feet |
| **6, 10, 14** | Motor imagery — both fists vs both feet |

The project's **initial approved task uses runs 4, 8, and 12**.

This means the initial EEG classification problem is specifically:

> **imagined left-fist movement vs imagined right-fist movement**

not:

- actual physical movement;
- hands versus feet;
- four-class motor imagery;
- unrestricted intention decoding.

---

# 5. WHY RUNS 4, 8, AND 12 ARE USED

The selected runs align with the project's current initial task:

```text
Left-hand motor imagery
vs
Right-hand motor imagery
```

This choice provides a clean binary BCI starting point.

The binary task is deliberately simpler than immediately attempting:

- left hand;
- right hand;
- both hands;
- feet;
- rest;
- multiple arbitrary rescue goals.

This supports the project's development philosophy:

> **validate a scientifically defensible simple system first, then extend only if justified.**

The use of a binary motor-imagery task does, however, create the already documented unresolved application issue:

> **How should binary Left/Right neural evidence map to a Search & Rescue environment that may contain more than two possible mission goals?**

That question remains unresolved and is outside the authority of the dataset pipeline itself.

---

# 6. ANNOTATION SEMANTICS

The dataset uses:

```text
T0
T1
T2
```

annotations.

At the dataset level:

## T0

Represents **rest**.

## T1

Its meaning depends on the run family.

For runs:

```text
3, 4, 7, 8, 11, 12
```

T1 corresponds to the **left fist** condition.

For runs:

```text
5, 6, 9, 10, 13, 14
```

T1 corresponds to the **both fists** condition.

## T2

Its meaning also depends on the run family.

For runs:

```text
3, 4, 7, 8, 11, 12
```

T2 corresponds to the **right fist** condition.

For runs:

```text
5, 6, 9, 10, 13, 14
```

T2 corresponds to the **both feet** condition.

---

# 7. PROJECT-SPECIFIC LABEL MEANING

Because the approved initial project uses runs:

```text
4
8
12
```

the relevant task annotations are:

```text
T1 → imagined left fist
T2 → imagined right fist
T0 → rest
```

The implementation must not use a global rule such as:

```text
T1 = left
T2 = right
```

for every EEGBCI run.

That would be incorrect outside the unilateral left/right run families.

The event mapping must therefore be tied to the selected run type.

---

# 8. REST / T0 STATUS — NOT YET FULLY FROZEN

The current project's primary classification problem is binary:

```text
Left motor imagery
vs
Right motor imagery
```

Therefore T0 is **not one of the two intended target classes**.

However, the exact operational treatment of T0 has not yet been explicitly frozen in the authority documents.

Possible uses include:

- excluding T0 from the binary training labels;
- retaining rest intervals only as contextual data;
- using rest periods for EEG inspection;
- using T0 in a later expanded experiment.

## Important rule

Codex must not silently convert the project into a three-class:

```text
Rest / Left / Right
```

classification problem.

The exact T0 handling should be frozen when the preprocessing/epoching protocol is approved.

For the initial binary classifier, treating T1 and T2 as the target classes is consistent with the locked project objective, but the final preprocessing implementation should document precisely how T0 segments are handled.

---

# 9. CHANNELS AND ELECTRODE SYSTEM

The source dataset contains **64 EEG channels**.

The recordings follow an international scalp-electrode placement scheme documented by PhysioNet.

The core project should initially preserve the full available EEG channel set unless a later scientifically justified channel-selection experiment is approved.

The project has **not yet locked a reduced channel subset**.

Therefore:

- do not silently use only C3/C4;
- do not silently use only motor-cortex channels;
- do not perform feature/channel selection using test data;
- do not claim a reduced montage unless implemented and evaluated.

A reduced-channel experiment may later be scientifically useful, but it is not currently part of the locked baseline.

---

# 10. CHANNEL STANDARDIZATION

The MNE EEGBCI utilities provide a standardization function for channel names/positions.

The approved loader architecture requires:

```text
mne.datasets.eegbci.standardize(raw)
```

or the currently compatible MNE equivalent.

The loader should:

1. load the EDF;
2. standardize channel naming;
3. verify channel count/names;
4. attach the appropriate standard montage;
5. verify that montage application succeeds;
6. report unexpected/missing channels.

No channel should be silently renamed through an undocumented custom mapping when an official MNE standardization step is available.

---

# 11. MONTAGE

The project architecture requires an appropriate EEG montage to be attached.

Official MNE motor-imagery examples use a standard montage after EEGBCI channel standardization.

However, the exact final montage configuration must be verified against the MNE version used by the project and documented in code/configuration.

## Rule

Do not invent electrode locations manually.

Use the validated MNE-compatible standard montage strategy.

The actual montage name/version should be recorded once the environment is initialized and tested.

---

# 12. SAMPLING FREQUENCY

The PhysioNet EEGMMIDB recordings are sampled at:

> **160 Hz**

The loader must read the sampling frequency from the file metadata and validate it.

Do not hard-code 160 Hz as an unchecked assumption in later processing.

Expected:

```text
raw.info["sfreq"] ≈ 160 Hz
```

If a loaded file reports an unexpected sampling frequency, the loader should stop or explicitly flag the mismatch.

---

# 13. FILE FORMAT

The EEG data are distributed as **EDF+** recordings.

MNE should load the files through its EDF reader.

Conceptual pipeline:

```text
mne.datasets.eegbci.load_data(...)
        ↓
local EDF paths
        ↓
mne.io.read_raw_edf(...)
        ↓
MNE Raw
```

The project should not manually rewrite the original dataset into another raw format before validation.

---

# 14. DATA ACCESS AND CACHING

The approved data-access path is:

```text
MNE EEGBCI utility
→ PhysioNet data
→ local cache
```

The loader must:

- accept configurable subject IDs;
- accept configurable run IDs;
- download missing files through MNE utilities;
- reuse already downloaded data;
- avoid repeated unnecessary downloads;
- expose the resolved local file paths.

The raw source files should be treated as **immutable**.

The project must not edit the original EDF files.

---

# 15. RAW DATA GOVERNANCE

The repository conceptual structure contains:

```text
data/
├── raw/
└── processed/
```

However, MNE may maintain its own dataset cache location.

The exact physical storage strategy has not been fully locked.

Acceptable approaches may include:

- using MNE's managed dataset cache and recording paths;
- configuring a project-local dataset location;
- linking/reference-tracking rather than duplicating large raw files.

## Non-negotiable rule

Regardless of storage arrangement:

> **raw source EEG must remain unchanged.**

Any transformation belongs in memory or in `data/processed/`.

---

# 16. SUBJECT CONFIGURATION

The dataset contains 109 subjects.

The loader must accept subjects through configuration.

Example conceptual configuration:

```yaml
dataset:
  subjects:
    - 1
    - 2
    - 3
  runs:
    - 4
    - 8
    - 12
```

This is only an interface example.

The final development-subject list is not fixed here.

---

# 17. INITIAL DEVELOPMENT SUBSET

The Master Project Specification permits beginning with:

> **a small configurable subset of subjects**

before broader evaluation.

Earlier project planning discussed beginning with a small number of subjects for rapid pipeline validation.

No exact initial number is currently authoritative.

Therefore:

- Codex may use a small test subject subset when instructed;
- the subset must be recorded;
- early-development results must not be presented as final project performance;
- the final evaluation must use the later approved subject protocol.

---

# 18. COMPLETE DATA PIPELINE

The approved conceptual data pipeline is:

```text
Configuration
        ↓
Subject/run selection
        ↓
MNE EEGBCI download/cache
        ↓
EDF loading
        ↓
Channel-name standardization
        ↓
Montage assignment
        ↓
Raw metadata validation
        ↓
Annotation inspection
        ↓
Signal preprocessing
        ↓
Event extraction
        ↓
Task-specific event mapping
        ↓
Epoch generation
        ↓
Epoch quality validation
        ↓
Labels + subject/run/trial metadata
        ↓
Dataset split
        ↓
Training-only fitted transformations
        ↓
Model-ready tensors/arrays
        ↓
CSP+LDA / EEGNet
        ↓
Evaluation / replay
```

Each stage must be independently inspectable.

---

# 19. STAGE 1 — CONFIGURATION VALIDATION

Before loading data, validate:

- subject IDs are valid;
- run IDs are valid;
- selected run family matches the intended task;
- cache/data location exists or can be created;
- duplicate subject/run entries are handled;
- impossible configurations fail clearly.

For the current core task, runs should be:

```text
4, 8, 12
```

unless an explicitly approved experiment states otherwise.

---

# 20. STAGE 2 — DOWNLOAD / CACHE

Primary interface:

```python
mne.datasets.eegbci.load_data(...)
```

The loader should return the resolved files rather than assuming a path.

Record:

- subject ID;
- run ID;
- source file path;
- dataset version where available;
- download/cache status.

Network access is an installation/runtime concern, not part of the scientific result.

---

# 21. STAGE 3 — EDF LOADING

Use MNE's EDF reader.

For each file, validate at least:

- file opens successfully;
- EEG channels exist;
- sampling frequency;
- duration;
- annotation presence;
- channel count;
- subject/run association.

The previously approved first-loader task explicitly requires printing/reporting:

- subject;
- channel count;
- sampling frequency;
- duration;
- annotations.

This remains part of the loader acceptance behaviour.

---

# 22. STAGE 4 — CHANNEL STANDARDIZATION

After loading:

```text
raw EDF
→ EEGBCI channel standardization
```

Validate:

- expected channel-name transformation;
- no duplicated names;
- no unexpected loss of EEG channels;
- montage compatibility.

The project should preserve a record of the standardized channel order used for modelling.

Channel order must be consistent when creating tensors for EEGNet.

---

# 23. STAGE 5 — MONTAGE ASSIGNMENT

After channel standardization:

```text
standardized Raw
→ standard montage
```

Validate:

- montage assignment completes;
- electrode positions are available where expected;
- channel visualization is plausible;
- no silent mismatch occurs.

A montage plot should be inspected during early pipeline validation.

---

# 24. STAGE 6 — RAW DATA QUALITY INSPECTION

Before modelling, manually inspect representative subjects/runs.

Minimum inspection should include:

- raw trace;
- annotations;
- channel count;
- channel names;
- sampling rate;
- signal duration;
- montage;
- PSD or equivalent spectral inspection.

The purpose is not to manually clean every recording.

The purpose is to catch:

- wrong files;
- broken metadata;
- incorrect channel mapping;
- unexpected annotations;
- gross signal issues.

---

# 25. STAGE 7 — SIGNAL PREPROCESSING

The approved architecture requires EEG preprocessing.

However, the exact preprocessing parameters are **not yet locked**.

Potential operations include:

- band-pass filtering;
- channel selection if later justified;
- referencing;
- artifact handling;
- epoch-specific baseline policy;
- optional normalization.

## Critical rule

The preprocessing document must later freeze these choices based on neuroscience/BCI reasoning.

Codex must not silently choose arbitrary defaults and make them project assumptions.

---

# 26. BAND-PASS FILTER — UNRESOLVED PROJECT PARAMETER

Motor-imagery EEG commonly focuses on sensorimotor frequency ranges, and official MNE CSP examples use a band-pass configuration for their demonstration.

However:

> **The project's final band-pass limits are not yet locked.**

Therefore a value such as:

```text
7–30 Hz
```

must be treated only as a **reference/example from an official MNE motor-imagery demonstration**, not as the final project setting unless explicitly approved.

The final choice should be documented in:

- `07_NEUROSCIENCE_AND_BCI_FOUNDATIONS.md`;
- `08_EEG_SIGNAL_PROCESSING_AND_ML.md`;
- configuration;
- and experiment metadata.

---

# 27. EEG REFERENCING — UNRESOLVED PROJECT PARAMETER

The final EEG reference strategy has not been explicitly frozen.

Possible MNE workflows may use an average reference or another justified reference.

No referencing strategy should become permanent merely because it appears in an example notebook.

The final method must:

- be scientifically justified;
- be applied consistently;
- be recorded;
- and not leak evaluation information.

---

# 28. ARTIFACT HANDLING — UNRESOLVED

The project has not locked a complex artifact-removal pipeline.

Possible artifact issues include:

- eye movement;
- muscle activity;
- bad channels;
- transient noise.

However, adding ICA or aggressive artifact rejection without need could create:

- implementation complexity;
- data loss;
- leakage risk;
- additional hyperparameters.

Therefore:

> **No complex artifact-removal method is currently mandatory.**

The later preprocessing methodology must state exactly:

- what artifact handling is performed;
- why;
- whether bad channels/trials are excluded;
- and how exclusion is logged.

---

# 29. STAGE 8 — EVENT EXTRACTION

Events must be extracted from annotations using MNE-compatible functionality.

The event logic must preserve the original annotation identity.

For runs 4, 8, and 12:

```text
T1 = imagined left fist
T2 = imagined right fist
```

The event extraction must be validated by checking:

- number of T1 events;
- number of T2 events;
- event timing;
- label balance;
- unexpected annotations.

Do not assume the event distribution is identical for every subject without checking.

---

# 30. STAGE 9 — EPOCH CONSTRUCTION

Epochs convert continuous EEG into trial-level samples.

Conceptually:

```text
continuous Raw
+ event onset
+ epoch time window
→ trial tensor
```

The required eventual structure is:

```text
X: trials × channels × samples
y: binary task labels
```

plus metadata.

The exact epoch time window is **not yet locked**.

---

# 31. EPOCH WINDOW — UNRESOLVED PROJECT PARAMETER

Official MNE CSP examples use a specific broader epoch interval and then crop a training interval for their demonstration.

That example is useful as a methodological reference.

It is **not automatically the project's final epoch timing**.

The final project must explicitly define:

- epoch start relative to cue;
- epoch end;
- whether an initial post-cue delay is excluded;
- whether baseline correction is used;
- whether the same window is used for CSP and EEGNet.

The values must be scientifically justified and recorded.

---

# 32. BASELINE CORRECTION — UNRESOLVED

The final baseline-correction policy is not currently locked.

Do not silently enable or disable baseline correction based only on library defaults.

The chosen setting must be explicit.

---

# 33. STAGE 10 — LABEL ENCODING

Human-readable labels should remain available:

```text
left
right
```

Numeric encoding may be used internally, for example:

```text
left  → 0
right → 1
```

but the exact numeric ordering is an implementation detail.

## Critical rule

The class ordering must be stored with:

- model checkpoint;
- decoder interface;
- calibration model;
- Bayesian mapping adapter.

Do not rely on memory or alphabetical order to infer class semantics.

---

# 34. REQUIRED TRIAL METADATA

Every extracted trial should preserve enough metadata to audit its origin.

Recommended conceptual schema:

```text
trial_id
subject_id
run_id
source_file
event_code
semantic_label
event_sample / onset
sampling_frequency
channel_order
epoch_start
epoch_end
preprocessing_config_id
```

Additional fields may be added.

This metadata is essential for:

- leakage detection;
- cross-subject analysis;
- replay;
- reproducibility;
- failure tracing.

---

# 35. PROCESSED EEG DATA CONTRACT

The architecture expects a data contract resembling:

```text
EEGEpoch:
    data
    sampling_frequency
    channel_names
    label
    subject_id
    run_id
    trial_id
```

For batch modelling:

```text
X
shape:
    n_trials × n_channels × n_samples

y
shape:
    n_trials
```

Subject and trial metadata must remain aligned with array order.

---

# 36. STAGE 11 — DATASET SPLITTING

Dataset splitting is one of the most important scientific parts of the project.

The exact final cross-subject protocol remains unresolved.

Therefore this document defines **rules**, not the final split.

Possible research modes include:

- within-subject evaluation;
- subject-wise cross-validation;
- held-out-subject evaluation;
- another approved subject-level protocol.

The Experimental Design document will freeze the final protocol.

---

# 37. NON-NEGOTIABLE LEAKAGE RULES

## Rule 1 — No test fitting

The test set must not be used to fit:

- filters with learned parameters;
- scalers;
- CSP;
- feature selection;
- LDA;
- EEGNet;
- calibration;
- learned adaptation;
- hyperparameters.

---

## Rule 2 — CSP is fitted on training data only

CSP uses class information.

Therefore fitting CSP before the train/test split would leak label-dependent information.

Correct:

```text
training EEG
→ fit CSP

validation/test EEG
→ transform using already fitted CSP
```

---

## Rule 3 — Calibration cannot use final test labels

If a calibration model is fitted:

```text
training / calibration split
→ fit calibrator

test split
→ evaluate calibrator
```

The exact calibration split strategy will be defined later.

---

## Rule 4 — Hyperparameter tuning cannot use test results

Do not repeatedly inspect test performance and adjust:

- filter band;
- epoch window;
- CNN architecture;
- learning rate;
- CSP components;
- thresholds;
- calibration method.

Those decisions belong to training/validation methodology.

---

## Rule 5 — Subject leakage must be prevented in cross-subject experiments

If the goal is unseen-subject evaluation:

```text
same subject
```

must not appear in both training and test sets.

---

## Rule 6 — Trial/window leakage must be prevented

If a trial is divided into multiple overlapping windows, windows from the same original trial must not be split across train and test in a way that creates near-duplicate leakage.

The grouping unit must preserve trial provenance.

---

## Rule 7 — Test-set normalization leakage is prohibited

Any normalization that learns dataset statistics must be fitted using the appropriate training partition only.

---

# 38. WITHIN-SUBJECT VS CROSS-SUBJECT QUESTIONS

These are different scientific questions.

## Within-subject

Asks:

> Can a model decode a person's EEG when it has been trained on data from that same person?

Potentially stronger performance but requires subject-specific calibration/training.

## Cross-subject

Asks:

> Can a model generalize to EEG from a person not represented in training?

This is harder and directly exposes inter-subject variability.

The final project should include cross-subject analysis because it has already been established as an important research direction.

The exact procedure is not yet frozen.

---

# 39. SUBJECT-WISE RESULT REPORTING

Final EEG results should not be reported only as one aggregate number.

Where appropriate, preserve:

- subject-level accuracy;
- balanced accuracy;
- F1;
- calibration;
- sample count;
- failure cases.

This allows the final discussion to show inter-subject variability rather than hiding it behind an average.

---

# 40. CLASS BALANCE

Before training, compute and record:

```text
number of Left trials
number of Right trials
```

for:

- each subject;
- each run;
- each split;
- the complete selected dataset.

Balanced accuracy is already an approved metric partly because class distributions may not be perfectly identical.

No automatic resampling method is currently approved.

If class imbalance requires intervention, it must be documented.

---

# 41. BAD / MISSING DATA POLICY

The loader/preprocessing pipeline must explicitly handle cases such as:

- missing EDF;
- failed download;
- unreadable EDF;
- missing expected run;
- unexpected channel count;
- missing annotation;
- no T1 events;
- no T2 events;
- invalid montage;
- NaN/non-finite EEG samples;
- empty epoch set.

The system must not silently continue with corrupted or incomplete data and then report a metric as if nothing happened.

---

# 42. EXCLUSION LOGGING

If any:

- subject;
- run;
- channel;
- trial;
- epoch;

is excluded, the reason should be recorded.

Conceptual log:

```text
entity_type
entity_id
reason
stage
timestamp
config
```

This becomes important for the final technical report.

---

# 43. PREPROCESSING CONFIGURATION

All important preprocessing settings must be centralized.

Conceptual configuration:

```yaml
eeg:
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
```

`TBD` here is intentional.

The project must not pretend unresolved methodological parameters have already been decided.

---

# 44. MODEL-SPECIFIC DATA REPRESENTATION

## CSP + LDA

Input should originate from the same scientifically approved epochs.

CSP performs its own spatial transformation.

Avoid creating a special, incompatible dataset unless required.

## EEGNet

EEGNet will consume tensor-form EEG.

Typical conceptual arrangement:

```text
batch × channels × time
```

or the exact layout required by the approved implementation.

Any added singleton dimensions must be documented.

## Critical fairness principle

Where possible, CSP+LDA and EEGNet should be evaluated on equivalent underlying trials/splits so the comparison is meaningful.

---

# 45. TRAINING / VALIDATION / TEST DATA LINEAGE

Every model result should be able to answer:

```text
Which subjects?
Which runs?
Which trials?
Which preprocessing config?
Which split?
Which seed?
Which model?
Which calibration setup?
```

If these questions cannot be answered later, the result is not sufficiently reproducible.

---

# 46. DATA VERSIONING

The source dataset version is:

```text
EEG Motor Movement/Imagery Dataset v1.0.0
```

Processed dataset versions should be tied to preprocessing configuration.

Conceptual identifier:

```text
processed_eeg_v001
```

with metadata such as:

```text
source_dataset_version
subjects
runs
filter config
epoch config
channel order
label mapping
code commit
```

Do not overwrite processed data without trace when the preprocessing definition changes.

---

# 47. RAW / PROCESSED SEPARATION

Recommended conceptual rule:

```text
data/raw/
    immutable or externally cached source data

data/processed/
    generated epochs / arrays / metadata
```

The raw layer is evidence.

The processed layer is reproducible output.

Deleting/recreating processed data should be possible from raw data + code + configuration.

---

# 48. SAVING PROCESSED DATA

The exact processed-data serialization format is **not locked**.

Possible approaches may include:

- MNE Epochs files;
- NumPy arrays with metadata;
- another transparent documented format.

Selection criteria:

- preserves channel order;
- preserves sampling rate;
- preserves trial metadata;
- easy to reproduce;
- compatible with both CSP+LDA and EEGNet;
- does not create unnecessary duplication.

Do not choose a complex database.

---

# 49. DATA PIPELINE VALIDATION REPORT

After preprocessing a selected subject set, generate a validation summary.

Recommended fields:

```text
dataset name/version
subjects
runs
number of raw files
sampling frequency
channel count
channel names
montage
T0 count
T1 count
T2 count
Left trial count
Right trial count
epoch shape
rejected epochs
non-finite values
class balance
preprocessing config
```

This summary should be human-readable and machine-readable where practical.

---

# 50. MANUAL CHECKPOINTS

The project owner should manually inspect at least:

## After loading

- correct subject;
- correct runs;
- 64-channel expectation;
- 160 Hz expectation;
- annotations present.

## After montage

- sensor layout appears plausible.

## After event extraction

- T1/T2 mapping is correct for runs 4/8/12.

## After epoching

- number of trials is plausible;
- `X` dimensions are correct;
- `y` matches trial count;
- Left/Right classes exist;
- no unexpected empty trials.

## Before final training

- split is correct;
- subject/trial grouping is correct;
- test data has not been used for fitting.

These checks remain important even when Codex generates the implementation.

---

# 51. UNIT TEST REQUIREMENTS

The dataset pipeline should include tests where practical.

## Loader tests

- subject configuration validation;
- run configuration validation;
- expected metadata structure;
- cache/path handling;
- invalid input error.

Network-dependent tests should be minimized or separated from ordinary unit tests.

## Event tests

Using controlled/synthetic annotations where possible:

- T1 mapping;
- T2 mapping;
- unexpected event handling.

## Epoch tests

- expected dimensions;
- label alignment;
- trial metadata alignment;
- finite data.

## Split tests

- no overlapping IDs across forbidden partitions;
- no subject overlap in subject-held-out tests;
- deterministic split for fixed seed.

---

# 52. OFFLINE EEG REPLAY DATA SOURCE

The full project uses:

> **offline EEG replay / simulated real-time BCI**

Replay should consume:

- real prerecorded EEG epochs;
- or their decoder outputs in controlled experiment modes.

Conceptual full replay:

```text
stored/loaded EEG epoch
→ EEG decoder
→ calibrated probability
→ Bayesian update
→ shared autonomy
```

Synthetic probabilities may be used for module testing, but the main integrated demonstration must ultimately connect to real dataset-derived EEG evidence.

---

# 53. REPLAY ORDER

Replay must preserve the experiment's intended evidence order.

If sequential Bayesian inference uses repeated EEG evidence:

- trial/evidence ordering must be explicitly defined;
- evidence must not be randomly reordered without recording the procedure;
- the same evidence must not accidentally be counted multiple times unless repetition is part of the experimental design.

This is especially important because Bayesian accumulation assumes a sequence of evidence.

---

# 54. EEG TRIAL TO BAYESIAN EVIDENCE BOUNDARY

The dataset pipeline ends scientifically at:

```text
validated EEG epoch + metadata
```

The decoder converts that epoch to:

```text
P(Left | EEG)
P(Right | EEG)
```

The calibration module may then produce calibrated evidence.

The **goal mapping policy** converts that class-level evidence into the hypothesis representation used by Bayesian goal inference.

The dataset pipeline must not hard-code Search & Rescue goal semantics into EEG labels.

Correct:

```text
T1
→ left motor imagery
→ decoder class "left"
→ separate application mapping policy
```

Incorrect:

```text
T1
→ Victim A
```

inside the dataset loader.

---

# 55. BINARY-TO-MULTIPLE-GOAL AMBIGUITY

This data document must preserve the project's major open question.

The EEG dataset supplies a binary task:

```text
Left imagery
Right imagery
```

The Search & Rescue environment may contain more than two goals.

Possible mapping approaches remain:

1. two active goals at a time;
2. hierarchical binary selection;
3. abstract binary priority/choice;
4. later multiclass EEG.

No approach is chosen here.

The dataset pipeline should therefore remain **application-agnostic** beyond the semantic Left/Right labels.

---

# 56. PROBABILITY CALIBRATION DATA BOUNDARY

Calibration requires its own valid fitting/evaluation logic.

The exact calibration method is unresolved.

Regardless of method:

- calibration must use held-out or appropriately partitioned data;
- final test labels must not be used to tune the calibrator;
- calibration parameters must be stored;
- calibration results must be reported separately from classification accuracy.

A perfectly accurate-looking softmax score is not assumed to be calibrated confidence.

---

# 57. DATA FOR ROBUSTNESS EXPERIMENTS

The project plans controlled uncertainty/noise stress testing.

Potential stress tests may alter:

- decoder probabilities;
- EEG signal quality;
- another explicitly defined evidence layer.

Previously discussed noise levels such as:

```text
10%
20%
30%
```

are **provisional examples**, not locked experimental values.

Any injected noise must be:

- defined mathematically;
- seeded where stochastic;
- recorded;
- applied consistently across compared systems.

---

# 58. ORIGINAL EEG VS SIMULATED NOISE

The final report must clearly distinguish:

```text
noise present in original EEG
```

from:

```text
artificially injected experimental noise
```

Do not imply simulated degradation is part of the original PhysioNet recording.

---

# 59. DATA ETHICS AND PRIVACY

The core project uses a public research EEG dataset.

Therefore the initial implementation does not collect new participant EEG.

The project must not claim:

- clinical consent collection by the project;
- live patient monitoring;
- private medical-record processing;
- hospital EEG acquisition.

If a future human study or live headset is introduced, ethics/privacy requirements must be separately reviewed.

---

# 60. DATASET LIMITATIONS

The dataset provides important strengths:

- real EEG;
- many subjects;
- standardized motor/imagery protocol;
- repeated runs;
- established BCI use.

However, the project must acknowledge limitations.

## 60.1 Motor imagery is not unrestricted intention

The data represent a constrained experimental task.

The system does not decode arbitrary thoughts.

---

## 60.2 Binary Left/Right evidence is abstract

The EEG task does not naturally represent:

- victim identity;
- rescue strategy;
- safe-zone semantics;
- multi-goal planning.

The application mapping is an engineered BCI interface layer.

---

## 60.3 Offline dataset

Signals are prerecorded.

The project does not evaluate:

- headset latency;
- electrode setup time;
- online artifact drift;
- live BCI adaptation;
- hardware failure.

---

## 60.4 Inter-subject variability

EEG differs substantially across individuals.

Cross-subject performance may be materially lower than within-subject performance.

This is a research finding to measure, not hide.

---

## 60.5 Laboratory task versus real rescue cognition

Motor imagery performed in the source experiment is not the same as cognition during a real emergency.

The Search & Rescue environment is a research abstraction.

---

# 61. DATA CLAIM RULES

Allowed, once implemented:

> “The system was evaluated using prerecorded motor-imagery EEG from the PhysioNet EEG Motor Movement/Imagery Dataset.”

Allowed:

> “Runs 4, 8, and 12 were used for Left-vs-Right motor-imagery decoding.”

Allowed:

> “EEG evidence was replayed in a simulated real-time interface.”

Not allowed:

> “We recorded EEG from rescue operators.”

Not allowed:

> “The system reads the operator's thoughts.”

Not allowed:

> “The system performs live brain-controlled rescue.”

Not allowed unless actually evaluated:

> “The model generalizes across users.”

Not allowed before real metrics exist:

> “EEGNet achieved X% accuracy.”

---

# 62. DATA PIPELINE ANTI-PATTERNS — DO NOT DO

## Do not mix run semantics

Never use T1/T2 without knowing the run family.

---

## Do not fit CSP before splitting

That creates leakage.

---

## Do not normalize using the full dataset

Any learned normalization must respect partition boundaries.

---

## Do not inspect test results repeatedly while tuning

The test set is not a development dashboard.

---

## Do not discard difficult subjects without reporting them

Subject exclusion must have a documented technical/scientific reason.

---

## Do not create a new arbitrary label mapping in each script

Class semantics must be centralized.

---

## Do not save arrays without metadata

An `X.npy` without subject/trial/channel provenance is not sufficient.

---

## Do not silently change channel order

EEGNet and CSP inputs must be traceable.

---

## Do not silently change sampling rate

If resampling is later approved, the original and new sampling frequencies must be recorded.

No resampling is currently locked.

---

## Do not copy preprocessing settings blindly from an example

Reference examples are starting evidence, not project decisions.

---

# 63. OPEN DATA / PREPROCESSING DECISIONS

The following remain unresolved.

## 63.1 Final subject protocol

- initial development subjects;
- within-subject protocol;
- held-out-subject protocol;
- cross-subject fold structure.

---

## 63.2 T0/rest handling

Exact treatment in preprocessing.

---

## 63.3 Band-pass filter

Exact lower/upper cutoffs.

---

## 63.4 EEG reference

Exact referencing strategy.

---

## 63.5 Epoch interval

Exact cue-relative timing.

---

## 63.6 Baseline correction

Exact policy.

---

## 63.7 Artifact rejection

Exact method and thresholds.

---

## 63.8 Channel subset

Current default direction is to preserve available EEG channels, but no reduced-channel experiment is locked.

---

## 63.9 Resampling

Not currently required or locked.

---

## 63.10 Processed data file format

Not locked.

---

## 63.11 Calibration partition

Calibration is required but exact fitting split is not locked.

---

# 64. SOURCE-VERIFIED REFERENCE SETTINGS THAT ARE NOT PROJECT SETTINGS

To prevent future confusion, official MNE examples contain methodological settings such as:

- a standard montage;
- motor-imagery band-pass filtering;
- defined epoch windows;
- CSP-based decoding.

These are useful reference implementations.

They are **not automatically authoritative project parameters**.

For example, an official MNE CSP motor-imagery example uses a 7–30 Hz filter and a specific epoch/training interval for a hands-vs-feet demonstration.

Our current project uses a different initial task:

```text
Left-hand imagery
vs
Right-hand imagery
```

Therefore those example settings must be independently justified before adoption.

---

# 65. DATA PIPELINE OUTPUTS

The complete data layer should eventually produce:

## Raw-level outputs

- resolved EDF paths;
- subject/run metadata;
- MNE Raw objects;
- validation summary.

## Preprocessed-level outputs

- cleaned/filtered Raw or equivalent;
- event table;
- MNE Epochs or equivalent;
- trial metadata.

## Model-level outputs

```text
X
y
subject_ids
trial_ids
channel_names
sampling_frequency
```

## Experiment-level outputs

- split manifest;
- preprocessing config;
- subject list;
- label counts;
- model input dimensions;
- exclusion log.

---

# 66. SPLIT MANIFEST

Every final experiment should save an explicit split manifest.

Conceptual form:

```text
experiment_id
train_subjects
validation_subjects
test_subjects
train_trial_ids
validation_trial_ids
test_trial_ids
split_seed
split_strategy
```

This is stronger than relying only on the code that created the split.

---

# 67. DATASET MANIFEST

A project-level dataset manifest should record:

```text
dataset_name
dataset_version
source
subjects_requested
subjects_loaded
runs_requested
runs_loaded
file_count
sampling_frequency
channel_count
standardized_channel_order
annotation_mapping
date_prepared
code_commit
```

This manifest may be JSON/YAML/CSV depending on implementation.

---

# 68. REPRODUCIBILITY REQUIREMENTS

The data pipeline is reproducible only if another run can reconstruct the same model input from:

```text
source dataset
+ subject/run list
+ code commit
+ preprocessing config
+ split manifest
```

The system should not rely on undocumented manual edits.

---

# 69. DATA PIPELINE DEVELOPMENT ORDER

The approved implementation order is:

## Step 1 — Loader only

Implement:

- MNE download/cache;
- EDF loading;
- channel standardization;
- montage;
- metadata printing;
- validation.

Do not preprocess or model yet.

## Step 2 — EEG inspection

Validate:

- traces;
- montage;
- annotations;
- PSD;
- subject/run metadata.

## Step 3 — Preprocessing

Implement only after parameters are approved.

## Step 4 — Event and epoch pipeline

Produce:

```text
X
y
metadata
```

and manually verify class labels.

## Step 5 — Dataset split

Implement leakage-safe split logic.

## Step 6 — CSP+LDA

Fit only on training data.

## Step 7 — EEGNet

Use the same approved underlying split where scientifically appropriate.

## Step 8 — Calibration

Fit only using approved non-test data.

## Step 9 — Offline replay

Connect actual EEG-derived probability evidence to the downstream system.

---

# 70. FIRST CODING TASK — PRESERVED BOUNDARY

The previously approved first coding task remains:

> **Read the Master Project Specification first. Implement a clean MNE-Python data loader for the PhysioNet EEGBCI motor-imagery dataset. Initially support configurable subject IDs and runs 4, 8, and 12. Download through MNE utilities, cache locally, load EDF files, standardize channel names, attach the appropriate montage, print subject/channel count/sampling frequency/duration/annotations, add basic validation/error handling, and write unit tests where practical. Do not implement preprocessing or modelling yet.**

After implementation, Codex should report:

1. files created/modified;
2. installation requirements;
3. exact command to run;
4. expected output;
5. what the project owner should manually check.

This boundary remains authoritative.

---

# 71. ACCEPTANCE CRITERIA — DATASET LAYER

The dataset/data-pipeline implementation is valid when:

1. the correct PhysioNet EEGMMIDB/EEGBCI source is used;
2. subjects and runs are configurable;
3. runs 4/8/12 are correctly recognized as Left-vs-Right motor imagery;
4. EDF files load successfully;
5. raw files remain unmodified;
6. channel names are standardized;
7. montage assignment is validated;
8. 64-channel expectation is checked rather than blindly assumed;
9. sampling frequency is read and validated;
10. annotations are preserved;
11. T1/T2 semantics are correct for the selected runs;
12. T0 handling is explicit;
13. preprocessing settings are configurable;
14. unresolved preprocessing choices are not silently frozen;
15. epochs retain subject/run/trial metadata;
16. class labels remain traceable;
17. no test-set leakage occurs;
18. CSP and other fitted transforms are trained only on permitted partitions;
19. calibration does not fit on final test data;
20. cross-subject experiments prevent subject overlap;
21. overlapping trial windows cannot leak across partitions;
22. exclusions are logged;
23. splits are reproducible;
24. experiment inputs are traceable to dataset/config/code state;
25. offline replay uses genuine dataset-derived evidence in the integrated system.

---

# 72. CURRENT DATASET SUMMARY

The project uses the **PhysioNet EEG Motor Movement/Imagery Dataset / EEGBCI** as its approved prerecorded neural-data source. The dataset contains 64-channel EEG from 109 subjects across 14 runs per subject, recorded with BCI2000 and distributed in EDF+ format at 160 Hz. The project's initial task is limited to **runs 4, 8, and 12**, which correspond to **motor imagery of the left fist versus the right fist**. In these runs, T1 represents the left-fist imagery condition and T2 the right-fist imagery condition, while T0 represents rest. MNE-Python is used to download/cache the data, load EDF recordings, standardize channels, attach an appropriate montage, extract annotations/events, and later construct epochs. The data pipeline must preserve subject/run/trial provenance and enforce strict leakage boundaries for CSP, neural models, calibration, normalization, and cross-subject evaluation. The exact filter band, reference, epoch timing, T0 policy, artifact handling, final subject split, calibration partition, and processed-data serialization remain unresolved and must be explicitly approved before they become permanent methodology.

---

# 73. NEXT DOCUMENT

The next planned document is:

**`07_NEUROSCIENCE_AND_BCI_FOUNDATIONS.md` — Neuroscience / BCI Scientific Basis**

It should establish:

- what EEG measures;
- EEG channels/electrodes;
- motor cortex relevance;
- motor imagery;
- sensorimotor rhythms;
- mu/beta activity;
- ERD/ERS where relevant;
- events and epochs;
- signal variability;
- artifacts;
- BCI concepts;
- why motor imagery is appropriate;
- what EEG can and cannot infer;
- and the scientific basis for the later preprocessing choices.

That document should provide the neuroscience reasoning needed before final preprocessing parameters are frozen.

---

# 74. OFFICIAL VERIFICATION SOURCES USED FOR DATASET FACTS

The dataset-specific factual details in this document were cross-checked against:

1. **PhysioNet — EEG Motor Movement/Imagery Dataset v1.0.0**
   - dataset identity;
   - 109 volunteers;
   - 64-channel EEG;
   - 14-run protocol;
   - T0/T1/T2 annotation meanings;
   - BCI2000 origin;
   - dataset DOI.

2. **MNE-Python EEGBCI documentation**
   - `mne.datasets.eegbci.load_data`;
   - run-number mapping;
   - 64 channels / 109 subjects / 14 runs;
   - EDF+ format;
   - MNE channel standardization workflow.

3. **MNE-Python motor-imagery CSP example**
   - used only as a methodological reference for MNE preprocessing/CSP workflow;
   - example-specific filter/epoch values are deliberately **not** treated as locked project parameters.
