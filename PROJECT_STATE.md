# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project  
**Update rule:** Update after every accepted implementation task, verified experiment, major blocker, approved scientific decision, or accepted architectural change  
**Do not use for:** speculative ideas, unapproved methodology, literature notes, hypothetical results, or future features  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. SOURCE-OF-TRUTH USE

```text
MASTER_PROJECT_SPEC.md -> what the project IS
DECISIONS.md            -> what has been explicitly DECIDED
CURRENT_TASK.md         -> what is being DONE NOW
PROJECT_STATE.md        -> what is ACTUALLY TRUE NOW
EXPERIMENT_LOG.md       -> what has actually been RUN as a reportable experiment
RESEARCH_LOG.md         -> unresolved scientific/research reasoning
TODO.md                 -> backlog; not authorization
AGENTS.md               -> Codex implementation rules
```

GitHub is the canonical implementation/state source of truth.

---

# 1. STATUS AT A GLANCE

```text
Project Phase:
EEG decoding implementation through M1-T06 is accepted and merged.

Current Module:
No active coding task authorized

Current Task ID:
NONE AUTHORIZED

Task Status:
NO ACTIVE TASK

Canonical Branch:
main

Latest Accepted Software Commit:
6b526d76acb53cd4f632ba87c975b4ede9e89a9c

Latest Accepted Software Task:
M1-T06 — EEGNet / Compact CNN

Latest Approved Scientific-Decision Commit:
792843762b82c030dbdce568f7b4c93ceeebac7d

Latest Valid Experiment:
None yet

Last Updated:
2026-08-31

Updated By:
ChatGPT + Project Owner + Codex
```

---

# 2. CURRENT PROJECT PHASE

The project currently has six accepted and merged EEG-stage implementation tasks on canonical `main`:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
```

The repository now contains:

```text
- verified EEGBCI loading and inspection
- accepted preprocessing and epoch extraction
- deterministic leakage-safe within-subject and cross-subject split utilities
- accepted CSP+LDA baseline
- accepted EEGNet / compact CNN baseline
- stable binary left/right probability outputs from both decoder families
```

No implementation task is currently authorized.

The project remains an **offline prerecorded EEG** system. No live EEG, physical robot, or real human-subject claim is authorized.

---

# 3. APPROVED EEG / MODEL DECISIONS NOW OPERATIONALIZED

Initial preprocessing/epoch decisions are resolved by D-031 through D-039:

```text
band-pass: 7–30 Hz
EEG reference: average EEG reference
canonical epoch: -1.0 s to +4.0 s
CSP-only crop: +1.0 s to +2.0 s
baseline: None
artifact handling: no ICA/interpolation; reject >150 µV peak-to-peak and log
T0: exclude from binary model data; preserve provenance
channels: all 64
resampling: none; native 160 Hz
processed representation: MNE Epochs; persisted *-epo.fif
```

Split/evaluation decisions are resolved by D-040 through D-042:

```text
within-subject: deterministic class-stratified 60/20/20 at original-trial level
cross-subject: fixed subject-held-out 70/15/15
seed: 42
for a full eligible 109-subject cohort: 76 train / 16 validation / 17 final-test subjects
no subject/trial/derived-window leakage
protected final-test excluded from fitting/tuning/calibration/adaptation
```

CSP+LDA decisions are resolved by D-043 and D-044.

EEGNet architecture/training decisions are resolved by D-045, D-046, and D-047.

---

# 4. IMPLEMENTATION STATUS MATRIX

| Module | Component | Status | Automated Tests | Manual Verification | Latest Accepted Commit | Notes |
|---|---|---|---|---|---|---|
| 1 | EEG Data Loader | PASS | Yes | Yes | `9b241681dfc986f53f5f8c0fcf40a3e3cea496e7` | EEGBCI subject/run loading verified |
| 2 | EEG Visualization / Inspection | PASS | Yes | Yes | `9b241681dfc986f53f5f8c0fcf40a3e3cea496e7` | traces/PSD/sensors/annotations verified |
| 3 | EEG Preprocessing / Epochs | PASS | Yes | Yes | `1af72b5deb9981f469a4394859aac49add65e2a7` | M1-T03 accepted |
| 3.1 | EEG Split Manifest / Leakage Assertions | PASS | Yes | Yes | `3b33477166db6889747dabc8d4be21403b480735` | M1-T04 accepted |
| 4 | CSP + LDA | PASS | Yes | Yes | `d7597efb8db7c8d77aecbd87f9cf2366dd02b484` | M1-T05 accepted |
| 5 | EEGNet / Compact CNN | PASS | Yes | Yes | `6b526d76acb53cd4f632ba87c975b4ede9e89a9c` | M1-T06 accepted |
| 6 | Unified Decoder Interface | NOT STARTED | No | No | — | separate authorization required |
| 7 | Probability Calibration | PARTIAL-BLOCKED | No | No | — | method/fitting/binning decisions unresolved |
| 8 | Bayesian Goal Inference | NOT STARTED | No | No | — | scientific semantics unresolved |
| 9 | Uncertainty / Entropy | NOT STARTED | No | No | — | policy thresholds unresolved |
| 10 | Adaptation / Personalization | BLOCKED | No | No | — | mechanism unresolved |
| 11 | 2D SAR Environment | NOT STARTED | No | No | — | later module |
| 12 | A* Planner | NOT STARTED | No | No | — | later module |
| 13 | Safety Controller | NOT STARTED | No | No | — | later module |
| 14 | Shared-Autonomy Controller | PARTIAL-BLOCKED | No | No | — | policy thresholds unresolved |
| 15 | Human Interaction Layer | NOT STARTED | No | No | — | later module |
| 16 | Offline EEG Replay | NOT STARTED | No | No | — | later module |
| 17 | Streamlit Dashboard | NOT STARTED | No | No | — | presentation only |
| 18 | Experiment Logger | NOT STARTED | No | No | — | later module |
| 19 | EEG / Model Evaluation | NOT STARTED | No | No | — | reportable experiments not yet run |
| 20 | Full System Evaluation | BLOCKED | No | No | — | final protocol pending |

---

# 5. CURRENTLY VERIFIED SOFTWARE COMPONENTS

## EEG Data Loader

```text
src/eeg/loader.py implemented
tests/test_loader.py implemented
real EEGBCI subject 1 runs 4 / 8 / 12 loaded
64 channels
160 Hz
T0/T1/T2 annotations
standard_1005 montage
```

## EEG Visualization / Inspection

```text
src/eeg/visualization.py implemented
tests/test_visualization.py implemented
real subject 1 runs 4 / 8 / 12 inspected
raw traces / PSD / sensors / annotation overview verified
```

## EEG Preprocessing / Epochs

```text
src/eeg/preprocessing.py implemented
src/eeg/epochs.py implemented
tests/test_preprocessing.py implemented
tests/test_epochs.py implemented
7–30 Hz filter
average reference
64 channels
160 Hz
-1.0 s to +4.0 s canonical epochs
baseline=None
T0 excluded from binary model data
150 µV peak-to-peak rejection with provenance
*-epo.fif persistence contract
```

High real-data epoch rejection remains a valid observation and was not used to change D-035.

## Split Manifest / Leakage Assertions

```text
src/eeg/splits.py implemented
tests/test_splits.py implemented
within-subject deterministic class-stratified 60/20/20
cross-subject deterministic seed-42 76/16/17 contract for full eligible 109-subject cohort
subject/trial/window disjointness checks
manifest persistence/provenance
protected final-test membership
```

## CSP+LDA Baseline

```text
src/models/csp_lda.py implemented
tests/test_csp_lda.py implemented
CSP crop +1.0 s to +2.0 s applied only inside CSP path
all 64 channels
candidate set {2,4,6,8}
validation balanced accuracy selection
4 preferred on exact best-score tie; otherwise smallest tied n_components
train-only fitting
protected test/final-test isolation
predict / predict_proba verified
canonical merge commit d7597efb8db7c8d77aecbd87f9cf2366dd02b484
```

## EEGNet / Compact CNN

```text
src/models/eegnet.py implemented
tests/test_eegnet.py implemented
requirements.txt includes torch
accepted task-branch head 1d6532ab1538fa361ed61c265c1a00577ae0afab
canonical software merge commit 6b526d76acb53cd4f632ba87c975b4ede9e89a9c
```

Accepted architecture/training behavior:

```text
input batch × 1 × 64 × time
full -1.0 s to +4.0 s canonical epoch
all 64 channels
160 Hz
F1=8
first temporal kernel=64, same padding
D=2 spatial depthwise convolution across 64 channels
depthwise max-norm cap=1.0
first average pool (1,4), stride (1,4)
separable F2=16, temporal kernel=16
second average pool (1,8), stride (1,8)
dropout=0.5
two logits
class order ("left", "right")
softmax probability output
cross-entropy
Adam lr=1e-3, weight_decay=0
batch size=32
max epochs=200
early-stopping patience=20
validation balanced accuracy checkpoint selection
earliest checkpoint retained on exact ties
seed=42
training partition shuffled only
protected test/final-test isolated from fitting, tuning, selection, and early stopping
```

Reviewer fix verification:

```text
feature-count dummy inference runs in temporary eval mode
BatchNorm running_mean/running_var/num_batches_tracked are not mutated by model construction
prior module training states are restored
```

Final targeted regression bundle reported and reviewed:

```text
48 passed, 1 warning
```

The single warning concerns PyTorch `padding='same'` with an even kernel possibly requiring a zero-padded copy. It is non-failing and was not an acceptance blocker.

---

# 6. M1-T06 REAL-DATA SMOKE CHECK

Real subject 1, runs 4/8/12:

```text
retained epochs: 13
partition counts: train=7, validation=3, test=3
run 4 rejected: 14
run 8 rejected: 9
run 12 rejected: 9
selected checkpoint epoch: 1
best validation balanced accuracy: 0.5
validation accuracy: 0.6666666666666666
validation balanced accuracy: 0.5
validation loss: 0.6873876452445984
test accuracy: 0.6666666666666666
test balanced accuracy: 0.5
test loss: 0.6873877048492432
class order: ("left", "right")
```

Interpretation rule:

> This is an integration/smoke result only. It is **not** a reportable model-efficacy experiment. Balanced accuracy of 0.5 does not support a performance claim, and no tuning against protected test data is authorized.

Negative or mixed later experimental results remain scientifically valid.

---

# 7. CURRENT SCIENTIFIC BLOCKERS

## Evaluation

```text
final statistical-analysis policy remains unresolved
if preprocessing/QC yields an eligible cross-subject cohort other than 109, D-042 requires reviewer decision before freezing the final manifest
```

## Calibration

```text
calibration method
calibration fitting partition
reliability-diagram binning strategy
```

## Bayesian / cognition

```text
binary EEG -> multi-goal SAR interaction protocol
exact decoder posterior -> goal-likelihood semantics
prior policy
Bayesian stopping / commitment rule
evidence sequence/reset semantics where not already fixed
```

## Shared autonomy

```text
confidence / entropy thresholds
PROCEED / CONFIRM / DEFER policy
mandatory-confirmation conditions
prolonged-uncertainty fallback
```

## Adaptation

```text
exact adaptation target
update formula
bounds
warm-up
decay
feedback semantics
```

## Planning / safety

```text
environmental risk values
risk normalization
risk lambda
prohibited-hazard threshold
final no-safe-path policy
```

## Experiments

```text
final A/B/C/D component matrix
robustness perturbation severities
inferential-statistics plan
```

These unresolved items must not be silently decided by Codex.

---

# 8. CURRENT TECHNICAL BLOCKERS

```text
M1-T06 has no open implementation blocker after acceptance and merge.
No implementation task is active.
```

The high artifact-rejection rate observed in the subject-1 smoke path remains a scientific/data-quality limitation, not permission to change the approved 150 µV threshold.

---

# 9. CURRENT EEG PIPELINE STATE

```text
Loader: PASS
Dataset caching: PASS
Channel standardization: PASS
Montage: PASS
Visualization: PASS
Preprocessing: PASS
Event extraction: PASS
Epoching: PASS
Within-subject split: PASS
Cross-subject split infrastructure: PASS
CSP+LDA: PASS
EEGNet: PASS
Unified decoder interface: NOT STARTED
Calibration metrics: NOT STARTED
Final calibrator: METHOD UNRESOLVED
```

---

# 10. CURRENT INTEGRATION STATE

```text
EEG loader -> preprocessing/epochs: PASS
preprocessing/epochs -> split assignment: PASS
split assignment -> CSP+LDA: PASS
split assignment -> EEGNet: PASS
probability outputs -> calibration: NOT STARTED
calibration -> goal evidence: BLOCKED
goal evidence -> Bayes: NOT STARTED
Bayes -> entropy: NOT STARTED
entropy -> shared autonomy: NOT STARTED
shared autonomy -> planner: NOT STARTED
planner -> safety: NOT STARTED
safety -> environment: NOT STARTED
offline EEG replay -> full system: NOT STARTED
```

---

# 11. CURRENT EXPERIMENT / RESULT STATE

```text
Reportable EEG decoding experiment: NOT STARTED
Calibration experiment: NOT STARTED
Bayesian experiment: NOT STARTED
Shared-autonomy experiment: NOT STARTED
Planning/safety experiment: NOT STARTED
A/B/C/D comparison: BLOCKED
Robustness/ablations: BLOCKED
Cross-subject model evaluation: NOT STARTED
Adaptation experiment: BLOCKED
```

No empirical model-performance conclusion is currently authorized.

`23_RESULTS_AND_ANALYSIS.md` remains an analysis framework until reportable experiments are executed.

`24_DISCUSSION_AND_FINDINGS.md` remains a discussion framework until reportable experiments are executed.

---

# 12. CURRENT TESTING STATE

```text
Unit tests: PASS for accepted EEG-stage modules
Leakage/split tests: PASS
Real-data smoke tests: PASS as integration checks
M1-T06 final targeted regression bundle: 48 passed, 1 warning
Calibration tests: NOT STARTED
Bayesian analytical tests: NOT STARTED
Entropy tests: NOT STARTED
Environment/planner/safety/shared-autonomy tests: NOT STARTED
End-to-end replay tests: NOT STARTED
```

The reported 48-test bundle covered EEGNet plus CSP-LDA, splits, epochs, preprocessing, and loader regressions. It is not represented as a full future end-to-end regression suite.

---

# 13. CURRENT VALID SOFTWARE ARTIFACTS

| Artifact ID | Type | Path | Task | Validity | Commit | Notes |
|---|---|---|---|---|---|---|
| M1-T01-LOADER | Source + tests | `src/eeg/loader.py`; `tests/test_loader.py` | M1-T01 | VALID | `9b241681dfc986f53f5f8c0fcf40a3e3cea496e7` | loader verified |
| M1-T02-VISUALIZATION | Source + tests + figures | `src/eeg/visualization.py`; `tests/test_visualization.py` | M1-T02 | VALID | `9b241681dfc986f53f5f8c0fcf40a3e3cea496e7` | inspection verified |
| M1-T03-PREPROCESSING-EPOCHS | Source + tests | `src/eeg/preprocessing.py`; `src/eeg/epochs.py`; tests | M1-T03 | VALID | `1af72b5deb9981f469a4394859aac49add65e2a7` | accepted pipeline |
| M1-T04-SPLIT-MANIFEST | Source + tests | `src/eeg/splits.py`; `tests/test_splits.py` | M1-T04 | VALID | `3b33477166db6889747dabc8d4be21403b480735` | leakage-safe split utilities |
| M1-T05-CSP-LDA | Source + tests | `src/models/csp_lda.py`; `tests/test_csp_lda.py` | M1-T05 | VALID | `d7597efb8db7c8d77aecbd87f9cf2366dd02b484` | accepted classical baseline |
| M1-T06-EEGNET | Source + tests | `src/models/eegnet.py`; `tests/test_eegnet.py` | M1-T06 | VALID | `6b526d76acb53cd4f632ba87c975b4ede9e89a9c` | accepted neural baseline |

No persistent trained-model checkpoint is currently recorded as a reportable model artifact.

---

# 14. CURRENT RISKS / LIMITATIONS

```text
High: scientific parameter guessed by implementation agent -> prevent through DECISIONS.md + stop conditions
High: binary EEG -> multi-goal semantics unresolved
High: probability-to-Bayesian likelihood semantics unresolved
High: leakage/test-set tuning -> enforce frozen partitions
Medium: scope drift -> one narrow CURRENT_TASK.md at a time
Medium: documentation/code drift -> reconcile state after each accepted task
```

Project limitations that remain explicit:

```text
public prerecorded EEG
offline replay / simulated real-time BCI only
binary motor imagery
no live EEG
no physical robot
no real human-subject study
simple 2D SAR simulation planned
no clinical claims
no unrestricted thought decoding
```

---

# 15. CURRENT CLAIM STATUS

Authorized implementation claims:

```text
- EEGBCI loader/inspection/preprocessing/split pipeline has been implemented and verified
- CSP+LDA baseline has been implemented and verified under approved leakage controls
- EEGNet baseline has been implemented and verified under approved leakage controls
- both model families expose stable left/right probability outputs
- subject-1 real-data smoke execution completes end-to-end through each accepted decoder path
```

Not authorized:

```text
- EEGNet outperforms CSP+LDA
- either decoder is above chance in a reportable experiment
- calibration improves reliability
- Bayesian inference improves goal selection
- shared autonomy improves task success
- safety improves outcomes
- cross-subject generalization claim
- adaptation improvement claim
```

---

# 16. NEXT GOVERNANCE GATE

No next implementation task is authorized.

Before the next task:

```text
1. identify one narrow next module
2. check MASTER_PROJECT_SPEC.md
3. check CURRENT_TASK.md
4. check PROJECT_STATE.md
5. check DECISIONS.md
6. check relevant technical documentation and accepted code/tests
7. resolve any blocking scientific/architectural decision
8. obtain explicit Project Owner approval
9. activate exactly one CURRENT_TASK.md ticket
```

Do not begin calibration, Bayesian inference, shared autonomy, planning, safety, replay, or another decoder-stage module without its own authorization.

---

# 17. CURRENT PROJECT STATE SUMMARY

The project has six accepted EEG-stage software tasks on canonical `main`. M1-T06 was accepted at task-branch head `1d6532ab1538fa361ed61c265c1a00577ae0afab` and squash-merged as `6b526d76acb53cd4f632ba87c975b4ede9e89a9c`. The accepted implementation follows D-045/D-046/D-047, uses the full canonical -1.0 s to +4.0 s EEG epoch, preserves all 64 channels at 160 Hz, selects checkpoints only from validation balanced accuracy, and keeps protected test/final-test data out of fitting and selection.

Final reviewed regression evidence for M1-T06 is `48 passed, 1 warning`. The subject-1 smoke path retained 13 epochs and produced validation/test balanced accuracy of 0.5; this is integration evidence only and supports no efficacy claim.

No implementation task is active. Calibration and later methodology remain governed by unresolved decisions in `DECISIONS.md`. The project remains an offline prerecorded EEG shared-autonomy research system, not a live-EEG system.
