# 16_REPOSITORY_AND_CODE_ARCHITECTURE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Repository Structure, File Ownership, Interfaces, Configuration, Testing, Logging, Results, and Git Workflow

**Document ID:** H-02  
**Document class:** Implementation / Repository & Code Architecture  
**Authority level:** Subordinate to all Master Authority, Scenario, Architecture, Data, Neuroscience, ML, Bayesian, Shared-Autonomy, Planning, Safety, and Implementation Blueprint documents  
**Status:** Authoritative repository/code-organization baseline; unresolved scientific decisions remain external to code structure  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND REPOSITORY RULE

This document defines **where project logic belongs, which files own which responsibilities, how modules communicate, how experiments are recorded, and how Git/GitHub preserve implementation state**.

It must remain consistent with all previously approved project documents, especially:

- `MASTER_PROJECT_SPEC.md`
- `04_SYSTEM_ARCHITECTURE.md`
- `15_IMPLEMENTATION_BLUEPRINT.md`

If this document conflicts with a higher-authority project document, the higher-authority document wins.

The governing repository principle is:

> **Scientific decisions belong in approved documentation and configuration. Code implements them; code must not silently invent them.**

---

# 1. REPOSITORY ROOT

The planned repository root is:

```text
neurocognitive-shared-autonomy/
```

The repository must contain:

- scientific documentation;
- implementation code;
- configuration;
- tests;
- experiment scripts;
- model artifacts;
- results;
- logs;
- live project-state files.

The repository should remain understandable without opening the Streamlit dashboard.

---

# 2. AUTHORITATIVE ROOT STRUCTURE

```text
neurocognitive-shared-autonomy/
│
├── README.md
├── MASTER_PROJECT_SPEC.md
│
├── 01_PROJECT_CONCEPT_AND_PROBLEM.md
├── 02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md
├── 03_SEARCH_AND_RESCUE_SCENARIO.md
├── 04_SYSTEM_ARCHITECTURE.md
├── 05_TECHNOLOGY_STACK.md
├── 06_DATASET_AND_DATA_PIPELINE.md
├── 07_NEUROSCIENCE_AND_BCI_FOUNDATIONS.md
├── 08_EEG_SIGNAL_PROCESSING_AND_ML.md
├── 09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md
├── 10_BAYESIAN_GOAL_INFERENCE.md
├── 11_COGNITIVE_AND_ADAPTIVE_MODEL.md
├── 12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md
├── 13_AUTONOMOUS_PLANNING_AND_CONTROL.md
├── 14_SAFETY_CRITICAL_CONTROL.md
├── 15_IMPLEMENTATION_BLUEPRINT.md
├── 16_REPOSITORY_AND_CODE_ARCHITECTURE.md
│
├── PROJECT_STATE.md
├── CURRENT_TASK.md
├── DECISIONS.md
├── RESEARCH_LOG.md
├── EXPERIMENT_LOG.md
├── TODO.md
│
├── AGENTS.md
│
├── config.yaml
├── requirements.txt
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── config.py
│   │
│   ├── eeg/
│   │   ├── loader.py
│   │   ├── preprocessing.py
│   │   ├── epochs.py
│   │   ├── visualization.py
│   │   └── replay.py
│   │
│   ├── models/
│   │   ├── csp_lda.py
│   │   ├── eegnet.py
│   │   ├── calibration.py
│   │   └── inference.py
│   │
│   ├── cognition/
│   │   ├── bayesian_intent.py
│   │   ├── uncertainty.py
│   │   ├── adaptation.py
│   │   └── goal_mapping.py        # only after mapping approval
│   │
│   ├── autonomy/
│   │   ├── environment.py
│   │   ├── planner.py
│   │   ├── safety.py
│   │   └── shared_controller.py
│   │
│   ├── evaluation/
│   │   ├── eeg_metrics.py
│   │   ├── autonomy_metrics.py
│   │   ├── experiments.py
│   │   └── logger.py
│   │
│   ├── app/
│   │   ├── dashboard.py
│   │   └── human_interface.py
│   │
│   ├── schemas/
│   │   └── ...
│   │
│   └── utils/
│       ├── reproducibility.py
│       └── validation.py
│
├── models/
│
├── experiments/
│
├── results/
│   ├── figures/
│   ├── tables/
│   └── logs/
│
├── notebooks/
│   ├── 01_eeg_exploration.ipynb
│   └── 02_results_analysis.ipynb
│
├── tests/
│
├── docs/
│
└── demo/
```

This is the baseline structure.

Small implementation-driven refinements are allowed if they do not alter scientific architecture.

---

# 3. CODEX INSTRUCTION FILE

Earlier project material used:

```text
CLAUDE.md
```

when the workflow used Claude/Claude Code.

The workflow has since changed to:

```text
ChatGPT + Project Owner + Codex
```

The approved permanent Codex repository instruction filename is:

```text
AGENTS.md
```

This file is the repository-level instruction authority for Codex.

Do not silently substitute a different permanent authority filename such as:

- `CODEX.md`
- `CLAUDE.md`

---

# 4. ROOT DOCUMENT OWNERSHIP

## `MASTER_PROJECT_SPEC.md`

Highest-authority project definition.

Contains:

- locked project identity;
- core architecture;
- mandatory components;
- optional components;
- forbidden scope;
- claim rules;
- unresolved decisions;
- governance.

Code must not contradict it.

---

## Numbered design documents

Purpose:

> Translate the master specification into specialized scientific and implementation detail.

They remain subordinate to the master specification.

---

# 5. LIVE PROJECT-STATE DOCUMENTS

These files are operational memory.

## `PROJECT_STATE.md`

Contains only current implementation reality:

```text
current milestone
implemented modules
tested modules
known failures
current branch/commit
recent artifacts
next candidate task
```

It must not claim a module works unless it has actually been run/tested.

---

## `CURRENT_TASK.md`

Contains exactly one current implementation ticket.

Recommended structure:

```text
Task ID
Objective
Read first
Allowed files
Forbidden files
Requirements
Tests
Acceptance criteria
Stop conditions
```

---

## `DECISIONS.md`

Records explicit approved decisions.

Each meaningful entry should contain:

```text
Decision ID
Date
Topic
Decision
Reason
Affected documents/modules
Owner approval
```

Example topics:

```text
EEG filter
epoch window
calibration method
goal mapping
risk lambda
adaptation mechanism
```

Unresolved items must not appear as decided.

---

## `RESEARCH_LOG.md`

Records:

- papers/references checked;
- scientific findings;
- alternative methods considered;
- reasoning;
- remaining questions.

It is not a substitute for final methodology documents.

---

## `EXPERIMENT_LOG.md`

Records experiments actually run.

Minimum structure:

```text
experiment ID
date
purpose
config
code commit
data/split
model
results
artifact locations
notes
```

---

## `TODO.md`

Contains backlog only.

Categories may include:

```text
Core
Blocked
Validation
Documentation
Optional
Future Work
```

---

# 6. CONFIGURATION OWNERSHIP

Primary configuration file:

```text
config.yaml
```

Parser/validator:

```text
src/config.py
```

The configuration file should contain **experiment/runtime values**, not scientific explanation.

Example categories:

```yaml
dataset:
preprocessing:
split:
csp_lda:
eegnet:
calibration:
bayesian_intent:
uncertainty:
adaptation:
environment:
planner:
safety:
shared_autonomy:
logging:
reproducibility:
```

---

# 7. UNRESOLVED VALUES IN CONFIGURATION

Do not invent values simply because a config key exists.

Before approval, valid approaches include:

```text
null
TBD
missing required key with controlled validation
```

depending on implementation stage.

Example:

```yaml
planner:
  risk_lambda: null
```

is better than silently setting:

```yaml
risk_lambda: 0.5
```

without approval.

---

# 8. CONFIGURATION VALIDATION

`src/config.py` should validate:

- required keys;
- correct data types;
- valid ranges;
- mutually incompatible settings;
- unresolved values before a module needing them runs.

Example:

```text
preprocessing requested
+
epoch window unresolved
→ stop with clear configuration error
```

Do not fall back to hidden defaults for scientifically important parameters.

---

# 9. SOURCE-CODE PACKAGE RESPONSIBILITIES

The `src/` tree should follow one rule:

> **Each package represents one scientific/engineering responsibility.**

Packages:

```text
eeg/
models/
cognition/
autonomy/
evaluation/
app/
schemas/
utils/
```

Cross-package imports should reflect the approved architecture.

---

# 10. `src/eeg/`

Owns:

- PhysioNet access;
- EEG loading;
- signal preprocessing;
- event extraction;
- epochs;
- EEG visualization;
- prerecorded replay.

It must not own:

- Bayesian logic;
- Search & Rescue planning;
- safety;
- adaptation policy.

---

# 11. `src/eeg/loader.py`

Owns:

```text
dataset access
EDF loading
channel standardization
montage
raw metadata validation
```

Must not contain:

```text
filtering
epoching
CSP
EEGNet
```

---

# 12. `src/eeg/preprocessing.py`

Owns only approved signal operations such as:

```text
filtering
reference
artifact policy
resampling if approved
```

Must be driven by configuration.

---

# 13. `src/eeg/epochs.py`

Owns:

```text
annotation/event mapping
T1/T2 semantics
epoch extraction
trial metadata
label construction
```

For runs 4/8/12:

```text
T1 = Left imagery
T2 = Right imagery
```

---

# 14. `src/eeg/visualization.py`

Owns diagnostic EEG plots.

It is an inspection utility, not an experiment authority.

Plots must be generated from real current data.

---

# 15. `src/eeg/replay.py`

Owns:

```text
ordered prerecorded EEG replay
trial sequencing
pause/reset support
replay metadata
```

Preferred UI terminology:

```text
Offline EEG Replay
Simulated Real-Time BCI
```

---

# 16. `src/models/`

Owns machine-learning decoding and calibration.

Contains:

```text
csp_lda.py
eegnet.py
calibration.py
inference.py
```

It must not contain:

- Bayesian intention;
- Search & Rescue semantics;
- A*;
- safety.

---

# 17. `src/models/csp_lda.py`

Owns:

```text
CSP
LDA
fit
predict
predict_proba
serialization
```

CSP must fit only on allowed training data.

---

# 18. `src/models/eegnet.py`

Owns:

```text
EEGNet / approved compact CNN
training
validation
checkpointing
inference
```

It must expose normalized class probabilities through the common decoder interface.

---

# 19. `src/models/calibration.py`

Owns:

```text
calibrator fit
probability transformation
save/load
calibrator metadata
```

Calibration metrics may live in evaluation code.

The final calibration method remains externally approved.

---

# 20. `src/models/inference.py`

Provides model-neutral inference.

Downstream modules should interact with:

```text
DecoderPrediction
```

rather than directly with:

- PyTorch tensors;
- scikit-learn objects;
- CSP internals.

---

# 21. `src/cognition/`

Owns:

- Bayesian intent;
- uncertainty;
- adaptation;
- approved goal-evidence mapping.

It does not own environment movement.

---

# 22. `src/cognition/bayesian_intent.py`

Owns:

```text
prior
likelihood
posterior
sequential update
belief history
reset
```

It must remain generic over named hypotheses.

It must not contain a hard-coded Left→Victim mapping.

---

# 23. `src/cognition/uncertainty.py`

Owns:

```text
entropy
optional normalized entropy
confidence-state representation
```

Final thresholds remain configuration/policy decisions.

---

# 24. `src/cognition/adaptation.py`

Owns only the explicitly approved adaptation mechanism.

Before approval, only interface/state scaffolding is permitted.

It must support:

```text
enabled
disabled
reset
subject-isolated state
logging
```

---

# 25. `src/cognition/goal_mapping.py`

This file is conceptually reserved for the critical interface:

```text
calibrated Left/Right evidence
→ goal evidence / Bayesian likelihood
```

Its final logic is **BLOCKED** until:

1. the goal-selection protocol is approved;
2. the likelihood semantics are approved.

The file itself need not exist before then.

---

# 26. `src/autonomy/`

Owns:

```text
environment
planner
safety
shared-autonomy controller
```

The package should remain independent of EEG framework internals.

---

# 27. `src/autonomy/environment.py`

Owns:

- 2D map;
- agent state;
- legal environment transitions;
- goals;
- blocked cells;
- hazards;
- termination;
- Gymnasium interface.

---

# 28. `src/autonomy/planner.py`

Owns:

```text
A*
Manhattan heuristic
path reconstruction
risk-aware cost
replanning
```

The planner receives an approved goal.

It never infers intent.

---

# 29. `src/autonomy/safety.py`

Owns:

```text
hard constraints
action rejection
pause
emergency stop
replan request
safety records
```

The planner proposes.

Safety authorizes.

---

# 30. `src/autonomy/shared_controller.py`

Owns the shared-autonomy state machine and policy.

Inputs:

```text
belief
uncertainty
human action/state
mission state
```

Outputs:

```text
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

It must not contain EEG model code.

---

# 31. `src/evaluation/`

Owns:

- metrics;
- experiment orchestration;
- logging.

Scientific modules should not duplicate metric formulas.

---

# 32. `src/evaluation/eeg_metrics.py`

Owns:

```text
accuracy
balanced accuracy
precision
recall
F1
confusion matrix
ECE
Brier Score
reliability-bin data
```

Optional metrics may be added only if justified.

---

# 33. `src/evaluation/autonomy_metrics.py`

Owns:

```text
task success
wrong-goal commitment
decision latency
confirmation count
override count
deferral count
path metrics
replanning
unsafe attempts
executed violations
safety overrides
```

Final mathematical definitions belong to the Metrics document.

---

# 34. `src/evaluation/experiments.py`

Owns experiment execution.

It should support controlled conditions such as:

```text
A
B
C
D
ablation
noise
cross-subject
safety stress
```

It should not contain UI code.

---

# 35. `src/evaluation/logger.py`

Owns structured experiment logging.

It must support machine-readable outputs.

Preferred formats:

```text
JSON
JSONL
CSV
```

---

# 36. `src/app/`

Owns user-facing interaction only.

Contains:

```text
dashboard.py
human_interface.py
```

Scientific logic should remain in reusable core modules.

---

# 37. `src/app/dashboard.py`

Owns Streamlit layout/presentation.

May display:

- EEG replay;
- probabilities;
- posterior;
- entropy;
- autonomy mode;
- map/path;
- safety events;
- controls.

It must call core interfaces rather than reimplement them.

---

# 38. `src/app/human_interface.py`

Owns structured human actions:

```text
CONFIRM
OVERRIDE
PAUSE
RESUME
STOP
```

It must support stale/duplicate action protection where required.

---

# 39. `src/schemas/`

Purpose:

> Keep shared data contracts explicit.

Potential schemas include:

```text
EEGEpoch
DecoderPrediction
CalibratedEvidence
GoalEvidence
IntentBelief
UncertaintyEstimate
AutonomyDecision
PlanningRequest
PlanningResult
SafetyDecision
HumanAction
ExperimentRecord
```

Exact implementation may use:

- dataclasses;
- typed dictionaries;
- another lightweight typed structure.

No heavy schema framework is required.

---

# 40. SCHEMA RULE

A shared object should have one authoritative definition.

Do not recreate slightly different versions of:

```text
DecoderPrediction
```

inside several modules.

This prevents interface drift.

---

# 41. SCHEMA VALIDATION

Important contracts should validate:

- dimensions;
- class/hypothesis names;
- probability ranges;
- finite values;
- IDs;
- required metadata.

Validation should fail early.

---

# 42. `src/utils/`

Contains small cross-cutting utilities only.

Approved examples:

```text
reproducibility.py
validation.py
```

Do not turn `utils/` into a miscellaneous dumping ground.

---

# 43. `src/utils/reproducibility.py`

May own:

- seed initialization;
- environment metadata;
- Git commit capture;
- run IDs;
- deterministic helpers.

---

# 44. `src/utils/validation.py`

May own reusable generic validators such as:

```text
probability validation
finite-array checks
coordinate validation
ID validation
```

Scientific transformation logic belongs in its actual module.

---

# 45. `data/`

Conceptual structure:

```text
data/
├── raw/
└── processed/
```

Raw data must remain immutable.

MNE may maintain its own external cache.

The repository should record/reference cache location rather than blindly duplicate large files.

---

# 46. RAW DATA RULE

Do not commit large source EEG files to Git unless there is a deliberate repository decision.

The dataset is reproducibly retrievable through MNE/PhysioNet.

Prefer:

```text
code + config + dataset reference
```

over storing all EDF files in version control.

---

# 47. PROCESSED DATA RULE

Processed artifacts should be reproducible from:

```text
raw source
+ preprocessing config
+ code commit
```

Processed data format remains unresolved.

It should preserve:

- channels;
- labels;
- subject;
- run;
- trial IDs;
- preprocessing identity.

---

# 48. `models/`

Contains persisted trained model artifacts.

Recommended logical organization:

```text
models/
├── csp_lda/
├── eegnet/
└── calibration/
```

Exact subfolders may be introduced when needed.

---

# 49. MODEL ARTIFACT NAMING

Prefer stable IDs.

Conceptual examples:

```text
csp_lda_<model_id>
eegnet_<model_id>
calibrator_<calibrator_id>
```

Avoid:

```text
final_model.pkl
final_final_model.pt
best2.pt
```

which become ambiguous.

---

# 50. MODEL MANIFEST

Each saved model should be traceable to:

```text
model_id
model type
dataset version
preprocessing config
split ID
class order
channel order
input shape
training seed
code commit
```

---

# 51. `experiments/`

Contains experiment definitions/scripts/configurations.

Examples:

```text
baseline_decoding
calibration
bayesian_synthetic
shared_autonomy
noise_robustness
safety_ablation
cross_subject
```

Final folder naming can remain simple.

---

# 52. EXPERIMENT ID

Every reportable run should have an unambiguous ID.

Conceptual format:

```text
EXP-<category>-<date>-<sequence>
```

Example:

```text
EXP-EEG-20260827-001
```

Exact format may be standardized later.

The important property is uniqueness and traceability.

---

# 53. `results/`

Primary generated evidence folder:

```text
results/
├── figures/
├── tables/
└── logs/
```

Results must come from actual experiments.

Do not manually type measured values into plots.

---

# 54. RESULT ARTIFACT OWNERSHIP

## `results/figures/`

Generated plots.

## `results/tables/`

Generated CSV/table artifacts.

## `results/logs/`

Runtime/experiment logs.

Where useful, experiment-specific subfolders may be created.

---

# 55. RESULT IMMUTABILITY

Once an experiment result is used in a report, do not silently overwrite it.

If methodology/config changes:

```text
new experiment ID
→ new result artifacts
```

This preserves scientific history.

---

# 56. `notebooks/`

Approved notebooks:

```text
01_eeg_exploration.ipynb
02_results_analysis.ipynb
```

Use notebooks for:

- exploration;
- inspection;
- analysis.

Do not keep authoritative reusable logic only in notebook cells.

Reusable code belongs in `src/`.

---

# 57. `tests/`

Tests should mirror the source architecture.

Conceptual structure:

```text
tests/
├── test_config.py
├── test_loader.py
├── test_preprocessing.py
├── test_epochs.py
├── test_csp_lda.py
├── test_eegnet.py
├── test_calibration.py
├── test_bayesian_intent.py
├── test_uncertainty.py
├── test_adaptation.py
├── test_environment.py
├── test_planner.py
├── test_safety.py
├── test_shared_controller.py
├── test_human_interface.py
└── test_integration_*.py
```

Exact filenames may be refined.

---

# 58. TEST CATEGORIES

## Unit tests

Validate one module.

## Integration tests

Validate module boundaries.

## Scientific/mathematical tests

Validate equations and leakage-sensitive logic.

## Smoke tests

Verify commands run.

## Regression tests

Ensure later fixes do not break previously validated behavior.

---

# 59. NETWORK-DEPENDENT TESTS

Dataset download tests should not make every test run depend on network availability.

Prefer:

- local fixture/small mock for ordinary unit tests;
- separate real-data smoke test;
- cached dataset integration test.

---

# 60. TEST DATA MUST NOT BECOME SCIENTIFIC TEST SET

Synthetic/unit-test fixtures are for software testing.

They are not the scientific held-out evaluation partition.

Keep terminology separate:

```text
unit-test fixture
```

vs:

```text
model test split
```

---

# 61. IMPORT DIRECTION

Recommended dependency direction:

```text
schemas / utils / config
        ↓
eeg / models / cognition / autonomy
        ↓
evaluation
        ↓
app
```

Avoid circular dependencies.

---

# 62. PROHIBITED DEPENDENCY DIRECTION

Examples of poor architecture:

```text
eeg/loader.py
→ imports Streamlit dashboard
```

```text
planner.py
→ imports EEGNet
```

```text
Bayesian module
→ imports Gymnasium environment internals
```

These indicate layer mixing.

---

# 63. INTERFACE-FIRST DEVELOPMENT

When two tracks are developed in parallel, define the shared contract first.

Example:

```text
DecoderPrediction
```

can be defined before both CSP+LDA and EEGNet are complete.

This reduces integration rewrites.

---

# 64. MODULE PUBLIC INTERFACES

Prefer small public APIs.

Examples:

```text
load_eeg(...)
create_epochs(...)
fit(...)
predict_proba(...)
calibrate(...)
update(...)
compute_entropy(...)
plan(...)
check_action(...)
decide(...)
```

Internal helpers should remain module-local where possible.

---

# 65. NO HIDDEN GLOBAL STATE

Avoid scientific state stored only in module globals.

Important state should be passed explicitly or owned by clearly defined objects:

```text
config
Bayesian filter state
adaptation state
environment state
controller state
```

This improves reproducibility and testing.

---

# 66. IDENTIFIERS

Important runtime entities should have stable IDs:

```text
experiment_id
episode_id
selection_id
trial_id
model_id
calibrator_id
plan_id
policy_id
map_id
```

These allow logs to connect modules.

---

# 67. CLASS AND HYPOTHESIS ORDER

Never rely on implicit order.

Every probability vector should preserve:

```text
class_names
```

or:

```text
hypothesis_names
```

This is critical for:

- calibration;
- Bayes;
- goal mapping.

---

# 68. LOGGING ARCHITECTURE

The system needs two kinds of logs.

## Developer/runtime logs

Errors, warnings, debug output.

## Scientific experiment records

Structured data used for analysis.

Do not confuse them.

---

# 69. SCIENTIFIC EXPERIMENT RECORD

A full-system record may include:

```text
experiment_id
episode_id
subject_id
trial_id
decoder_model_id
raw_probabilities
calibrated_probabilities
goal_mapping_policy_id
Bayesian prior
likelihood
posterior
entropy
autonomy_decision
human_action
approved_goal
plan_id
path
safety_decision
environment_transition
terminal outcome
```

Only applicable fields need to exist per experiment.

---

# 70. REPRODUCIBILITY METADATA

Where practical preserve:

```text
random seed
config snapshot
dataset selection
preprocessing config
split ID
model/checkpoint
Git commit
Python/library environment
map config
policy versions
timestamp
```

---

# 71. CONFIG SNAPSHOT

Every reportable experiment should save the exact configuration used.

Do not rely on whatever `config.yaml` contains weeks later.

Prefer an experiment-specific snapshot.

---

# 72. GIT COMMIT CAPTURE

Every experiment should record the current Git commit when practical.

If the working tree is dirty, that should be visible or the experiment should be treated cautiously.

---

# 73. GIT WORKFLOW

Recommended development pattern:

```text
small branch
→ narrow implementation
→ tests
→ review
→ commit
→ merge
```

Examples:

```text
feature/eeg-loader
feature/csp-lda
feature/bayesian-intent
feature/safety-controller
```

Exact branch naming is not mandatory.

---

# 74. COMMIT SCOPE

Prefer commits such as:

```text
Implement EEGBCI loader
Add CSP+LDA baseline
Add Bayesian posterior tests
Add A* path planner
```

Avoid giant commits such as:

```text
Finish whole project
```

---

# 75. COMMIT MESSAGE DISCIPLINE

Commit messages should describe actual implementation.

Do not write:

```text
Fix everything
```

when only one module changed.

---

# 76. CODING TASK FILE BOUNDARIES

`CURRENT_TASK.md` should specify:

```text
Allowed files
Forbidden files
```

Example:

```text
Allowed:
src/eeg/loader.py
tests/test_loader.py

Forbidden:
src/eeg/preprocessing.py
src/models/*
```

This reduces Codex scope drift.

---

# 77. CROSS-MODULE CHANGE RULE

If Codex discovers that a task requires changing a forbidden or upstream file:

1. stop;
2. explain why;
3. propose the minimal required change;
4. wait for approval.

Do not silently expand scope.

---

# 78. DECISION-TO-CODE WORKFLOW

For unresolved scientific decisions:

```text
research/reason
→ project owner approves
→ DECISIONS.md updated
→ relevant design document updated if necessary
→ config updated
→ Codex ticket issued
→ implementation
→ tests
```

Code is downstream of decision.

---

# 79. NO SCIENTIFIC CONSTANTS SCATTERED THROUGH CODE

Important values must be centralized.

Examples:

```text
filter limits
epoch times
confidence thresholds
risk lambda
hazard threshold
adaptation bounds
```

Do not repeat them in multiple files.

---

# 80. MAGIC NUMBER RULE

A value such as:

```python
if confidence > 0.8:
```

is prohibited unless:

- `0.8` is approved;
- defined in configuration/policy;
- recorded in experiments.

---

# 81. ENVIRONMENT / MAP CONFIGURATION

Experimental maps should be stored in a transparent configuration format.

Each map should have:

```text
map_id
dimensions
start
goals
blocked cells
hazards
```

Map definitions should be versioned.

---

# 82. POLICY VERSIONING

Policies that materially affect experiments need stable identity:

```text
calibration policy
goal-mapping policy
Bayesian likelihood model
confidence policy
adaptation policy
planner risk policy
safety policy
```

---

# 83. HEADLESS-FIRST RULE

Core experiments must run without Streamlit.

Ideal pattern:

```text
python experiment script
→ result artifacts
```

Then:

```text
Streamlit
→ reads/calls core system
```

This keeps the UI from becoming the scientific implementation.

---

# 84. COMMAND REPRODUCIBILITY

Every major module/task should have an exact command to:

- run;
- test;
- reproduce basic behavior.

Those commands should be documented in task completion reports and eventually README documentation.

---

# 85. ERROR HANDLING

Errors should be explicit.

Examples:

```text
InvalidSubjectError
InvalidProbabilityError
NoPathError/status
ConfigurationError
ModelInputMismatch
```

Exact custom exception classes are optional.

The key requirement is clear failure rather than silent fallback.

---

# 86. VALIDATION AT MODULE BOUNDARIES

Each module should validate inputs important to its scientific correctness.

Examples:

## Decoder

- expected channels;
- probability normalization.

## Bayes

- matching hypotheses;
- non-negative likelihood.

## Planner

- valid start/goal.

## Safety

- valid action/state.

---

# 87. PERFORMANCE OPTIMIZATION

Optimize only after correctness.

Avoid premature:

- multiprocessing;
- distributed execution;
- GPU complexity beyond EEGNet;
- caching systems;
- microservices.

The dataset/project scale does not require infrastructure complexity.

---

# 88. NO CLOUD DEPENDENCY

The core repository must remain runnable locally.

No AWS/GCP backend is required.

Cloud compute may be used manually if available, but it is not architectural.

---

# 89. NO CONTAINER REQUIREMENT

Docker is not currently required.

If environment reproducibility later benefits from a container, it may be added as an optional engineering artifact after the local environment is stable.

Do not make containerization a prerequisite now.

---

# 90. DOCUMENTATION AND CODE CONSISTENCY

When implementation reveals that an approved document is inaccurate:

- do not silently edit the scientific definition;
- flag the discrepancy;
- follow change control.

Documentation must reflect actual approved behavior.

---

# 91. README ROLE

`README.md` is the public-facing summary.

It should eventually contain:

- project purpose;
- architecture diagram;
- setup;
- demo;
- results;
- limitations.

It is not the source of truth for unresolved methodology.

---

# 92. `docs/` ROLE

The `docs/` folder may contain supporting:

- architecture diagrams;
- generated technical figures;
- supplemental notes;
- demo documentation.

The numbered root documents remain the primary structured specifications unless the project owner later reorganizes them.

---

# 93. `demo/` ROLE

The `demo/` folder may contain:

- short demo assets;
- example configs;
- recordings;
- screenshots.

Demo artifacts must represent actual system behavior.

---

# 94. LARGE FILE RULE

Do not commit:

- large raw EEG datasets;
- unnecessary checkpoints;
- duplicate result archives;

without a deliberate decision.

Repository size should remain manageable.

---

# 95. GENERATED ARTIFACT RULE

Generated artifacts should be clearly separated from source code.

Example:

```text
src/
```

contains implementation.

```text
results/
```

contains generated evidence.

---

# 96. REPOSITORY HYGIENE

The repository should eventually exclude temporary files such as:

```text
__pycache__/
.ipynb_checkpoints/
local cache files
temporary model outputs
```

through an appropriate ignore configuration.

The exact `.gitignore` may be created during M0.

---

# 97. SECURITY / SECRET RULE

The core project should not require API keys.

If any development-only external service is later used, secrets must never be committed.

No secret-management infrastructure is otherwise needed.

---

# 98. FINAL REPOSITORY ACCEPTANCE CRITERIA

The repository architecture is successful when:

1. every scientific component has a clear file owner;
2. no module contains unrelated responsibilities;
3. unresolved scientific decisions remain external to implementation;
4. configuration centralizes important parameters;
5. probability/class/hypothesis contracts are explicit;
6. code dependencies follow the architecture;
7. circular imports are avoided;
8. tests mirror module structure;
9. experiments run headlessly;
10. results are machine-readable;
11. model/result IDs are traceable;
12. experiment configuration is preserved;
13. Git commit is captured where practical;
14. Codex tasks can restrict file scope;
15. live state documents reflect actual implementation;
16. Streamlit remains presentation-only;
17. raw data remain reproducible and unmodified;
18. large/generated artifacts are separated from source;
19. no unnecessary cloud/LLM/3D infrastructure is introduced;
20. Git/GitHub preserve a credible technical history.

---

# 99. CURRENT REPOSITORY ARCHITECTURE SUMMARY

The repository is organized around strict separation of scientific responsibilities. EEG loading and preprocessing live in `src/eeg`, decoding and calibration in `src/models`, Bayesian intent/uncertainty/adaptation in `src/cognition`, environment/planning/safety/shared autonomy in `src/autonomy`, metrics and experiments in `src/evaluation`, and Streamlit/human interaction in `src/app`. Shared typed data contracts belong in `src/schemas`, while only small cross-cutting helpers belong in `src/utils`. Configuration is centralized in `config.yaml`, reportable experiments preserve config snapshots and Git state, and generated models/results are stored outside source code. `PROJECT_STATE.md`, `CURRENT_TASK.md`, `DECISIONS.md`, `RESEARCH_LOG.md`, `EXPERIMENT_LOG.md`, and `TODO.md` provide persistent operational memory. The permanent Codex instruction filename remains deliberately unresolved and must not be silently standardized. Most importantly, repository structure must enforce the scientific architecture rather than allowing code convenience to redefine it.

---

# 100. NEXT DOCUMENT

The next planned document is:

**`17_EXPERIMENTAL_DESIGN.md` — Complete Experimental Design, A/B/C/D Comparisons, Cross-Subject Evaluation, Robustness, Noise Stress Tests, and Ablation Protocol**

That document should define:

- experimental questions;
- hypotheses;
- A/B/C/D system configurations;
- dataset split protocol;
- subject protocol;
- calibration partition;
- repeated runs/seeds;
- controlled EEG/noise degradation;
- Bayesian tests;
- shared-autonomy tests;
- safety stress tests;
- adaptation ON/OFF;
- component ablations;
- fair comparison rules;
- test-set protection;
- and reportable experiment matrices.

It must preserve any still-unapproved scientific parameters rather than silently fixing them.
