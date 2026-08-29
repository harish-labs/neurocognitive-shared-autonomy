# 15_IMPLEMENTATION_BLUEPRINT.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Complete Module-by-Module Implementation Blueprint for ChatGPT + Project Owner + Codex

**Document ID:** H-01  
**Document class:** Implementation / Engineering Blueprint  
**Authority level:** Subordinate to all Master Authority, Scenario, Architecture, Data, Neuroscience, ML, Bayesian, Shared-Autonomy, Planning, and Safety specifications  
**Status:** Authoritative implementation blueprint; unresolved scientific decisions remain blocked until explicitly approved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND IMPLEMENTATION RULE

This document converts the approved project architecture into **small, testable implementation units**.

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
10. `09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md`
11. `10_BAYESIAN_GOAL_INFERENCE.md`
12. `11_COGNITIVE_AND_ADAPTIVE_MODEL.md`
13. `12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`
14. `13_AUTONOMOUS_PLANNING_AND_CONTROL.md`
15. `14_SAFETY_CRITICAL_CONTROL.md`

If this document conflicts with a higher-authority document, the higher-authority document wins.

The implementation philosophy is:

```text
DESIGN / APPROVE
→ IMPLEMENT
→ RUN
→ VERIFY
→ INTEGRATE
→ REVIEW
→ COMMIT
→ NEXT MODULE
```

No Codex task may silently redesign the project.

---

# 1. DEVELOPMENT ROLES

## ChatGPT — Project Brain / Research Director

Responsible for:

- scientific reasoning;
- architecture;
- mathematics;
- methodology;
- experiment design;
- reviewing code/results;
- identifying scientific mistakes;
- creating precise implementation tickets;
- preserving project scope.

ChatGPT recommends.

It does not silently approve unresolved project decisions.

---

## Project Owner — Final Authority

Responsible for:

- approving scientific/architectural decisions;
- accepting/rejecting proposed changes;
- manually verifying important outputs;
- relaying implementation tasks;
- deciding scope.

---

## Codex — Implementation Engineer

Responsible for:

- reading approved documentation;
- editing repository files;
- writing code;
- writing tests;
- running commands;
- debugging;
- generating experiment artifacts;
- reporting actual status.

Codex must not independently decide unresolved scientific parameters.

---

## Git / GitHub — Persistent Source of Truth

Responsible for preserving:

- code;
- configuration;
- documentation;
- tests;
- experiment scripts;
- state;
- decisions;
- results;
- history.

---

# 2. GLOBAL CODEX RULES

Every Codex task must follow these rules.

1. Read `MASTER_PROJECT_SPEC.md` first.
2. Read the active task document.
3. Read only the additional project documents required for that task.
4. Implement only the requested scope.
5. Do not modify unrelated scientific assumptions.
6. Do not invent missing parameters.
7. If a required parameter is unresolved, stop and report it.
8. Add tests where practical.
9. Run the relevant tests.
10. Report exactly what changed.
11. Report exact commands used.
12. Report failures honestly.
13. Do not fabricate metrics.
14. Do not call prerecorded EEG “live EEG.”
15. Do not add unnecessary technologies.
16. Do not proceed automatically to the next module.

---

# 3. STANDARD IMPLEMENTATION TICKET FORMAT

Every implementation request should contain:

```text
TASK ID
MODULE
OBJECTIVE

READ FIRST
INPUTS
OUTPUTS

ALLOWED FILES
FORBIDDEN FILES

REQUIREMENTS
SCIENTIFIC CONSTRAINTS

TESTS
MANUAL CHECKS
ACCEPTANCE CRITERIA

STOP CONDITIONS
DELIVERABLE REPORT
```

This structure is mandatory for major implementation tasks.

---

# 4. STANDARD CODEX COMPLETION REPORT

After a task, Codex should report:

```text
1. Task status: PASS / PARTIAL / BLOCKED / FAIL
2. Files created
3. Files modified
4. Exact implementation completed
5. Tests added
6. Tests executed
7. Test results
8. Commands to reproduce
9. Output files created
10. Manual checks required
11. Known limitations
12. Open blockers
13. Git commit / suggested commit
```

A statement such as:

> “Done.”

is not sufficient.

---

# 5. PROJECT MILESTONES

The approved milestone structure is:

```text
M0 — Infrastructure / Project Contracts
M1 — EEG Data + CSP/LDA
M2 — EEGNet
M3 — Calibration + Bayes + Uncertainty + Adaptation Framework
M4 — 2D Search & Rescue + A* + Safety
M5 — Shared Autonomy + Human Interaction
M6 — End-to-End EEG Integration
M7 — Experiments / Ablations / Robustness
M8 — Dashboard / Documentation / Portfolio
```

Calendar duration is intentionally not fixed.

Progress is measured by verified module completion.

---

# 6. PARALLEL DEVELOPMENT STRATEGY

Three technical tracks can proceed independently once interfaces are stable.

## Track A — EEG

```text
loader
→ preprocessing
→ epochs
→ CSP/LDA
→ EEGNet
→ calibration
```

## Track B — Cognitive

```text
synthetic probabilities
→ Bayesian core
→ entropy
→ shared-autonomy policy
→ adaptation
```

## Track C — Autonomy

```text
artificial goal
→ environment
→ A*
→ safety
```

Then:

```text
A + B + C
→ end-to-end integration
```

This allows rapid progress without coupling every task to EEG training.

---

# 7. IMPLEMENTATION DEPENDENCY MAP

```text
Module 0  Configuration
   ↓
Module 1  EEG Loader
   ↓
Module 2  EEG Inspection
   ↓
Module 3  Preprocessing / Epochs
   ↓
Module 4  CSP + LDA
   ├──────────────→ Module 6 Unified Decoder
Module 5  EEGNet ─┘
                         ↓
Module 7  Calibration
                         ↓
             Goal-Evidence Adapter [BLOCKED]
                         ↓
Module 8  Bayesian Intent
                         ↓
Module 9  Uncertainty
                         ↓
Module 14 Shared Autonomy
                         ↓
Module 12 A* Planner
                         ↓
Module 13 Safety
                         ↓
Module 11 Environment

Module 10 Adaptation
        ↘ cognitive/shared-autonomy parameters

Module 15 Human Interaction
        ↘ Module 14 / Module 13

Module 16 Offline Replay
        ↘ Module 6

Module 18 Logging
        ↘ all runtime modules

Module 19 EEG Evaluation
        ↘ Modules 4/5/7

Module 20 System Evaluation
        ↘ Modules 8–18

Module 17 Dashboard
        ↘ consumes already-working core interfaces
```

---

# 8. BLOCKED SCIENTIFIC DECISIONS

The following must not be silently solved during implementation:

1. Binary Left/Right EEG → multi-goal Search & Rescue mapping.
2. Exact mapping from `P(class | EEG)` to Bayesian likelihood `P(E | G)`.
3. Exact calibration method.
4. Calibration fitting partition.
5. Final cross-subject protocol.
6. Confidence thresholds.
7. Bayesian stopping/commitment rule.
8. Adaptation mechanism.
9. Hazard-risk scale.
10. Risk weight \(\lambda\).
11. Prohibited-hazard threshold.
12. Final A/B/C/D experimental semantics.

Initial M1 preprocessing decisions that were previously on this blocker list are now resolved by D-031 through D-039: filter band, EEG reference, epoch timing/CSP crop, baseline correction, artifact policy, T0 handling, channel policy, resampling policy, and processed-data representation.

When implementation reaches any still-unresolved boundary, Codex must stop unless an approved decision already exists in `DECISIONS.md`.

---

# 9. MODULE 0 — CONFIGURATION & PROJECT INFRASTRUCTURE

## Purpose

Create the stable configuration, reproducibility, state, and project scaffolding required by later modules.

## Primary files

```text
config.yaml
src/config.py
PROJECT_STATE.md
CURRENT_TASK.md
DECISIONS.md
RESEARCH_LOG.md
EXPERIMENT_LOG.md
TODO.md
tests/
requirements.txt
```

The final Codex instruction filename must be standardized separately.

## Inputs

- approved project documents;
- repository structure.

## Outputs

- validated config loading;
- project state files;
- deterministic seed utility;
- results/log directories;
- dependency definition.

## Required behavior

- load configuration;
- validate required keys;
- support deterministic seed configuration;
- expose typed/structured settings where practical;
- fail on invalid configuration;
- avoid scientific hard-coded constants.

## Tests

- valid config loads;
- missing config fails clearly;
- invalid type/value fails;
- seed utility reproducible.

## Acceptance criteria

- repository starts cleanly;
- config accessible from modules;
- unresolved scientific values can remain `TBD`/unset rather than being invented;
- logs/results directories are defined;
- tests can run independently.

## Forbidden changes

- do not choose preprocessing parameters;
- do not choose thresholds;
- do not implement models.

---

# 10. MODULE 1 — EEG DATA LOADER

## Purpose

Load real PhysioNet EEGBCI motor-imagery recordings correctly.

## Primary file

```text
src/eeg/loader.py
```

## Initial scope

Configurable:

```text
subject IDs
runs = 4, 8, 12
```

## Inputs

- subject IDs;
- run IDs;
- dataset/cache configuration.

## Outputs

- MNE Raw data;
- source paths;
- subject/run metadata.

## Required behavior

- download through MNE utilities;
- cache locally;
- load EDF;
- standardize EEGBCI channel names;
- attach appropriate validated montage;
- preserve annotations;
- validate subject/run inputs;
- report:
  - subject;
  - channel count;
  - sampling frequency;
  - duration;
  - annotations.

## Tests

- configuration validation;
- invalid subject/run rejection;
- metadata structure;
- helper-function tests without requiring repeated network downloads where possible.

## Manual checks

- expected 64-channel structure;
- sampling frequency around 160 Hz;
- correct annotations;
- plausible montage.

## Acceptance criteria

Loader works on at least one real configured subject/run set and does not preprocess data.

## Forbidden changes

- no filtering;
- no epoching;
- no model training.

---

# 11. MODULE 2 — EEG VISUALIZATION / INSPECTION

## Purpose

Allow scientific inspection before preprocessing/modeling.

## Primary file

```text
src/eeg/visualization.py
```

## Inputs

- validated Raw EEG.

## Outputs

- inspection plots;
- metadata summary.

## Required behavior

Support selected views such as:

- raw traces;
- PSD;
- montage/sensor layout;
- annotation overview.

## Tests

- functions accept valid Raw object;
- invalid inputs fail clearly;
- saved figures created where requested.

## Manual checks

Project owner verifies:

- signal exists;
- channels plausible;
- annotations plausible;
- montage plausible;
- no obvious dataset mismatch.

## Acceptance criteria

Representative real EEG can be inspected before any model is trained.

---

# 12. MODULE 3 — EEG PREPROCESSING & EPOCHS

## Purpose

Convert validated continuous EEG into model-ready Left/Right motor-imagery trials.

## Primary files

```text
src/eeg/preprocessing.py
src/eeg/epochs.py
```

## Scientific parameters approved for M1-T03

D-031 through D-039 approve:

- 7–30 Hz band-pass;
- average EEG reference;
- canonical epoch -1.0 s to +4.0 s relative to cue onset;
- initial CSP training crop +1.0 s to +2.0 s;
- T0 excluded from binary epoch/training data while raw annotations/provenance are preserved;
- `baseline=None`;
- no ICA or automatic bad-channel interpolation; reject epochs above 150 µV peak-to-peak and log rejections;
- preserve all 64 validated EEG channels;
- no resampling; preserve 160 Hz;
- canonical processed representation MNE Epochs, with persisted epochs saved as `*-epo.fif`.

These approvals remove the scientific-parameter blocker, but Module 3 may begin only when `CURRENT_TASK.md` explicitly authorizes M1-T03.

## Inputs

- validated Raw;
- approved preprocessing config.

## Outputs

Canonical output:

```text
MNE Epochs
```

with preserved/derivable metadata including:

```text
y
subject_ids
run_ids
trial_ids
channel_names
sampling_frequency
```

If persisted, epochs use MNE FIF `*-epo.fif`. Model-specific arrays may be derived later without replacing the canonical representation.

## Required behavior

- apply only approved preprocessing;
- extract annotations/events;
- map:
  - T1 → Left imagery;
  - T2 → Right imagery;
- handle T0 according to approved policy;
- preserve trial provenance;
- validate class counts;
- reject/record invalid trials according to policy.

## Tests

- event mapping;
- epoch shape;
- label alignment;
- finite data;
- metadata alignment;
- deterministic processing.

## Manual checks

- sample epochs;
- class counts;
- channel order;
- shape;
- PSD before/after filter;
- exclusion log.

## Acceptance criteria

Model-ready dataset is reproducible from source + config.

## Forbidden changes

- do not tune preprocessing on final test data;
- do not convert to 3-class task without approval.

---

# 13. MODULE 4 — CSP + LDA BASELINE

## Purpose

Establish the mandatory classical motor-imagery baseline.

## Primary file

```text
src/models/csp_lda.py
```

## Inputs

- approved epochs;
- leakage-safe split.

## Outputs

- fitted CSP+LDA model;
- predicted labels;
- raw class probabilities;
- model metadata.

## Required behavior

- fit CSP on training data only;
- fit LDA on training features;
- expose `predict`;
- expose `predict_proba`;
- preserve class order;
- support save/load;
- record configuration.

## Blockers

Exact:

- CSP component count;
- regularization;
- LDA options

must be approved or treated as controlled tuning parameters using non-test data.

## Tests

- synthetic fit/predict;
- probability normalization;
- class order;
- save/load;
- leakage-safe pipeline structure.

## Acceptance criteria

A reproducible classical baseline produces real predictions and probability vectors on held-out data.

---

# 14. MODULE 5 — EEGNET / COMPACT CNN

## Purpose

Implement the neural EEG decoder.

## Primary file

```text
src/models/eegnet.py
```

## Inputs

- same approved underlying EEG trial definition/split as baseline where scientifically appropriate.

## Outputs

- trained checkpoint;
- predictions;
- raw probability vectors;
- training history;
- model metadata.

## Blockers

Must freeze or explicitly configure:

- exact architecture variant;
- learning rate;
- optimizer;
- batch size;
- epochs;
- dropout;
- checkpoint-selection criterion;
- early stopping if used.

## Required behavior

- correct input shape;
- compact EEG-appropriate architecture;
- training/validation separation;
- save best checkpoint;
- expose probability vector;
- preserve class/channel order.

## Tests

- forward pass;
- output dimensions;
- probability normalization;
- tiny training smoke test;
- checkpoint round trip.

## Acceptance criteria

EEGNet/compact CNN can be trained, evaluated, saved, loaded, and compared fairly with CSP+LDA.

## Forbidden changes

- no arbitrary deep architecture inflation;
- no downstream Bayes inside the network.

---

# 15. MODULE 6 — UNIFIED DECODER INTERFACE

## Purpose

Allow downstream modules to consume either decoder without model-specific branching.

## Primary file

```text
src/models/inference.py
```

## Input

- model/checkpoint;
- EEG epoch.

## Output

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
```

## Required behavior

- stable `predict_proba` interface;
- validate class order;
- validate probability normalization;
- return model identity.

## Tests

- wrapper around CSP+LDA;
- wrapper around EEGNet;
- identical output contract;
- invalid model/input fails.

## Acceptance criteria

Downstream code does not need to know internal model details.

---

# 16. MODULE 7 — PROBABILITY CALIBRATION

## Purpose

Evaluate and improve the reliability of decoder probabilities.

## Primary file

```text
src/models/calibration.py
```

## Inputs

- saved raw probability vectors;
- labels from approved calibration partition;
- decoder identity.

## Outputs

- calibrator;
- calibrated probabilities;
- calibration metadata.

## Blockers

Must approve:

- calibration method;
- fitting partition.

## Work allowed before blocker resolution

Implement:

- ECE utility;
- Brier Score;
- reliability-bin data;
- calibration interface/skeleton.

## Required behavior after approval

- fit on non-test data;
- preserve class order;
- save/load calibrator;
- transform probabilities;
- support identity/no-calibration baseline.

## Tests

- ECE toy cases;
- Brier toy cases;
- probability validity;
- save/load;
- test labels not needed at inference.

## Acceptance criteria

Raw vs calibrated probability quality can be evaluated reproducibly.

---

# 17. GOAL-EVIDENCE ADAPTER — CRITICAL ARCHITECTURAL SEAM

## Purpose

Translate calibrated Left/Right EEG class evidence into a mathematically valid goal-hypothesis evidence/likelihood representation.

## Suggested file

```text
src/cognition/goal_mapping.py
```

Exact filename may be finalized later.

## Status

**BLOCKED.**

Do not implement the final adapter until the project owner approves:

1. the binary BCI goal-selection protocol;
2. the probability/likelihood semantics.

## Forbidden shortcut

Do not hard-code:

```text
Left → Victim A
Right → Victim B
```

inside the EEG model or Bayesian core as an assumed permanent solution.

---

# 18. MODULE 8 — BAYESIAN GOAL INFERENCE

## Purpose

Maintain sequential probabilistic belief over candidate intent hypotheses.

## Primary file

```text
src/cognition/bayesian_intent.py
```

## Inputs

- named hypotheses;
- prior;
- externally supplied likelihood vector.

## Output

```text
IntentBelief
```

containing:

- prior;
- likelihood;
- posterior;
- hypothesis names;
- update index;
- evidence reference.

## Core equation

\[
P(G\mid E_{1:t})
\propto
P(E_t\mid G)P(G\mid E_{1:t-1})
\]

## Work allowed immediately

Implement generic Bayesian math using synthetic likelihoods.

## Required behavior

- validate prior;
- validate likelihood;
- normalize posterior;
- sequential updates;
- preserve history;
- reset explicitly;
- support generic \(K\) hypotheses.

## Tests

- uniform evidence;
- repeated evidence;
- contradictory evidence;
- informative prior;
- three hypotheses;
- invalid input;
- reset.

## Acceptance criteria

Analytically verifiable synthetic tests pass.

## Blocked integration

Real EEG integration waits for Goal-Evidence Adapter approval.

---

# 19. MODULE 9 — UNCERTAINTY

## Purpose

Quantify uncertainty in the current Bayesian goal posterior.

## Primary file

```text
src/cognition/uncertainty.py
```

## Input

- posterior probability vector.

## Output

```text
UncertaintyEstimate:
    entropy
    normalized_entropy if used
    confidence_state
```

## Core measure

\[
H(P)=-\sum_i p_i\log p_i
\]

## Work allowed immediately

Implement entropy and optional normalized-entropy utility.

## Blocker

Final confidence-state thresholds are unresolved.

## Tests

- uniform posterior → maximal/high entropy;
- concentrated posterior → minimal entropy;
- invalid probability rejection;
- NaN/Inf handling.

## Acceptance criteria

Entropy is mathematically correct and available to downstream control.

---

# 20. MODULE 10 — ADAPTATION / PERSONALIZATION

## Purpose

Provide simple, interpretable user/system adaptation from correction history.

## Primary file

```text
src/cognition/adaptation.py
```

## Status

**Mechanism unresolved.**

## Candidate targets

- prior;
- decoder reliability;
- confidence thresholds;
- evidence weighting.

## Work allowed before approval

Implement only:

- module interface;
- enabled/disabled state;
- subject-isolated state;
- reset;
- update log hooks.

## Required after approval

- exact update rule;
- bounded parameters;
- subject isolation;
- traceable updates;
- ON/OFF ablation.

## Tests

- disabled means no update;
- bounds;
- reset;
- subject isolation;
- deterministic known update.

## Acceptance criteria

Adaptation is measurable, reversible, logged, and ablatable.

---

# 21. MODULE 11 — SEARCH & RESCUE ENVIRONMENT

## Purpose

Implement the simple 2D technical application environment.

## Primary file

```text
src/autonomy/environment.py
```

## Framework

Gymnasium.

## Inputs

- map configuration;
- start;
- goals;
- blocked cells;
- hazard map;
- seed.

## Output

- environment observation/state;
- step transition;
- termination status.

## Action space

```text
UP
DOWN
LEFT
RIGHT
WAIT
```

## Required behavior

- map validation;
- deterministic seeded reset;
- legal movement;
- blocked-cell handling;
- goal detection;
- terminal states;
- hazard representation.

## Tests

- bounds;
- movement;
- WAIT;
- blocked cells;
- goal reaching;
- invalid map;
- deterministic reset.

## Acceptance criteria

Environment works independently using artificial goals.

---

# 22. MODULE 12 — A* PLANNER

## Purpose

Plan a route to an approved goal.

## Primary file

```text
src/autonomy/planner.py
```

## Inputs

- start;
- approved goal;
- blocked cells;
- risk map;
- planner config.

## Outputs

```text
PlanningResult:
    path
    path_cost
    movement_cost
    risk_cost
    status
```

## Required behavior

- 4-connected A*;
- Manhattan heuristic;
- blocked cells excluded;
- no-path handling;
- deterministic path;
- risk cost configurable;
- replanning.

## Blockers

Final:

- hazard scale;
- \(\lambda\);
- forbidden-hazard policy

remain unresolved.

## Tests

- empty grid;
- obstacle;
- no path;
- risk-free equivalence;
- high-risk shortcut;
- deterministic output;
- replanning.

## Acceptance criteria

Planner works independently with artificial approved goals.

---

# 23. MODULE 13 — SAFETY CONTROLLER

## Purpose

Authorize or reject every proposed autonomous action.

## Primary file

```text
src/autonomy/safety.py
```

## Inputs

- current state;
- proposed action;
- human stop/pause state;
- blocked cells;
- safety policy;
- hazard policy when approved.

## Output

```text
SafetyDecision:
    safe
    proposed_action
    approved_action
    intervention_type
    reason
    requires_replan
```

## Core rules implementable immediately

- invalid action reject;
- out-of-bounds reject;
- blocked-cell reject;
- pause blocks movement;
- emergency stop blocks movement.

## Blocker

Final prohibited-hazard threshold/policy.

## Tests

- valid action;
- invalid action;
- bounds;
- blocked cell;
- pause;
- emergency stop;
- deterministic result;
- replan flag.

## Acceptance criteria

No full-system autonomous movement bypasses safety.

---

# 24. MODULE 14 — SHARED-AUTONOMY CONTROLLER

## Purpose

Convert belief + uncertainty + human state into an autonomy decision.

## Primary file

```text
src/autonomy/shared_controller.py
```

## Inputs

- IntentBelief;
- UncertaintyEstimate;
- human-control state;
- current mission state;
- policy config.

## Output

```text
AutonomyDecision:
    mode
    candidate_goal
    approved_goal
    requires_confirmation
    reason
```

## Modes

```text
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

## Work allowed before threshold approval

Implement:

- state machine;
- human action precedence;
- policy interface;
- no permanent numerical thresholds.

## Blockers

- exact proceed/confirm/defer thresholds;
- whether highest-confidence state can auto-approve;
- binary goal-selection protocol.

## Tests

- legal state transitions;
- pause;
- stop;
- override precedence;
- injected policy behavior.

## Acceptance criteria

Shared-autonomy control works with synthetic belief/uncertainty before EEG integration.

---

# 25. MODULE 15 — HUMAN INTERACTION LAYER

## Purpose

Represent human authority actions.

## Suggested file

```text
src/app/human_interface.py
```

## Required actions

```text
CONFIRM
OVERRIDE
PAUSE
RESUME if supported
STOP
```

## Required behavior

- explicit command objects;
- stale-request protection;
- duplicate handling;
- stop propagation;
- logging.

## Tests

- confirmation request association;
- stale confirmation rejection;
- duplicate command handling;
- pause;
- stop.

## Acceptance criteria

Human actions change core controller state, not just UI state.

---

# 26. MODULE 16 — OFFLINE EEG REPLAY

## Purpose

Feed prerecorded EEG evidence to the system in sequence.

## Suggested file

```text
src/eeg/replay.py
```

## Inputs

- real preprocessed epochs/trials;
- replay configuration.

## Outputs

- ordered EEG samples/evidence events;
- replay metadata.

## Required terminology

```text
Offline EEG Replay
Simulated Real-Time BCI
```

## Required behavior

- deterministic sequence;
- preserve trial IDs/order;
- configurable replay pacing;
- avoid duplicate evidence unless intentional;
- support pause/stop.

## Tests

- sequence order;
- reset;
- trial metadata;
- no duplicate replay;
- pause/stop behavior.

## Acceptance criteria

Real prerecorded EEG can drive decoder inference in a controlled stream.

---

# 27. MODULE 17 — TECHNICAL DASHBOARD

## Purpose

Provide technical inspection and demonstration.

## Primary file

```text
src/app/dashboard.py
```

## Framework

Streamlit.

## Display

- EEG replay state;
- model probabilities;
- calibrated probabilities;
- Bayesian posterior;
- entropy;
- autonomy state;
- candidate/approved goal;
- 2D map;
- path;
- safety events;
- human controls;
- episode outcome.

## Rule

Dashboard consumes working core modules.

It must not contain hidden scientific logic.

## Tests

Core logic should be testable headlessly; UI tests may remain lightweight.

## Acceptance criteria

Evaluator can understand the system state and interact without altering the scientific architecture.

---

# 28. MODULE 18 — EXPERIMENT LOGGER

## Purpose

Create traceable machine-readable records of every experiment.

## Primary file

```text
src/evaluation/logger.py
```

## Required metadata

Where applicable:

```text
experiment_id
episode_id
timestamp
seed
Git commit
config
subject
trial
model
calibrator
posterior
entropy
autonomy decision
planner path
safety event
human action
terminal state
metrics
```

## Outputs

Prefer:

```text
CSV
JSON
JSONL
```

## Tests

- required fields;
- serialization;
- append/read;
- deterministic IDs where appropriate;
- no silent field loss.

## Acceptance criteria

Every reported metric is traceable to underlying run artifacts.

---

# 29. MODULE 19 — EEG / MODEL EVALUATION

## Purpose

Evaluate EEG decoding and calibration.

## Primary file

```text
src/evaluation/eeg_metrics.py
```

## Metrics

- accuracy;
- balanced accuracy;
- precision;
- recall;
- F1;
- confusion matrix;
- ECE;
- Brier Score;
- reliability data;
- subject-wise performance;
- cross-subject performance when protocol is approved.

## Inputs

- true labels;
- predictions;
- probability vectors;
- subject/fold metadata.

## Tests

Use analytically checkable toy cases.

## Acceptance criteria

Metrics are reproducible and independent of UI.

---

# 30. MODULE 20 — SYSTEM / SHARED-AUTONOMY EVALUATION

## Purpose

Evaluate the full NeuroCognitive Shared Autonomy system.

## Primary files

```text
src/evaluation/autonomy_metrics.py
src/evaluation/experiments.py
```

## Metrics

- task success;
- wrong-goal commitment;
- decision latency;
- entropy;
- confirmations;
- overrides;
- deferrals;
- completion time;
- path length;
- path efficiency;
- replanning;
- unsafe attempts;
- executed safety violations;
- hazard entry;
- safety overrides.

## Experiment support

- A/B/C/D conditions;
- ablations;
- robustness/noise;
- cross-subject;
- safety stress tests.

## Blockers

Final experimental definitions must be frozen in later Experimental Design and Metrics documents.

## Acceptance criteria

Experiments run automatically and save machine-readable results.

---

# 31. MILESTONE M0 — INFRASTRUCTURE

## Goal

Create a clean repository foundation.

## Deliverables

- repository structure;
- configuration;
- requirements;
- state/decision files;
- test framework;
- logging skeleton;
- reproducibility utilities;
- module placeholders only where helpful.

## Exit criteria

- tests execute;
- configuration validates;
- repository is ready for M1;
- no scientific parameter has been invented.

---

# 32. MILESTONE M1 — REAL EEG + CLASSICAL BASELINE

## Sequence

```text
M1.1 Loader
M1.2 Inspection
M1.3 Record/verify approved preprocessing parameters
M1.4 Preprocessing
M1.5 Events / epochs
M1.6 Split
M1.7 CSP+LDA
M1.8 Evaluation
```

## Required manual verification

Before M1 exit:

- correct real dataset;
- correct run semantics;
- correct labels;
- correct epoch shapes;
- no leakage;
- valid probabilities;
- baseline metrics generated from actual held-out data.

---

# 33. MILESTONE M2 — EEGNET

## Sequence

```text
M2.1 Freeze architecture/training config
M2.2 Implement EEGNet
M2.3 Training
M2.4 Validation
M2.5 Checkpoint
M2.6 Test evaluation
M2.7 Compare with CSP+LDA
```

## Exit criteria

- reproducible neural checkpoint;
- valid held-out metrics;
- probability outputs;
- fair baseline comparison;
- failure cases saved.

---

# 34. MILESTONE M3 — COGNITIVE / PROBABILISTIC LAYER

This milestone can begin partly in parallel using synthetic data.

## Sequence

```text
M3.1 Calibration metrics
M3.2 Select calibration method
M3.3 Calibration model
M3.4 Generic Bayesian core
M3.5 Entropy
M3.6 Shared confidence-policy interface
M3.7 Adaptation interface
M3.8 Approve goal mapping + likelihood model
M3.9 Goal-Evidence Adapter
```

## Important blocker

`M3.8` is the critical scientific decision before real EEG → Bayesian goal inference is complete.

---

# 35. MILESTONE M4 — AUTONOMY ENVIRONMENT

## Sequence

```text
M4.1 2D environment
M4.2 Standard A*
M4.3 Risk-aware cost
M4.4 Safety core
M4.5 Hazard policy
M4.6 Replanning
```

## Exit criteria

Using artificial goals:

- environment works;
- planner works;
- safety rejects invalid actions;
- replanning works;
- tests pass.

---

# 36. MILESTONE M5 — SHARED AUTONOMY

## Sequence

```text
M5.1 Shared state machine
M5.2 Human actions
M5.3 Confidence policy
M5.4 Confirm/override
M5.5 Pause/stop
M5.6 Synthetic integration
M5.7 Adaptation after mechanism approval
```

## Exit criteria

Synthetic probability/belief sequences can drive:

```text
proceed / confirm / defer
→ planning
→ safety
→ environment
```

with human override.

---

# 37. MILESTONE M6 — FULL EEG INTEGRATION

## Required preconditions

- EEG model verified;
- calibration defined;
- goal-mapping protocol approved;
- likelihood construction approved;
- Bayes tests pass;
- uncertainty tests pass;
- shared-autonomy policy defined;
- environment/planner/safety verified.

## Integration pipeline

```text
real PhysioNet EEG
→ preprocessing
→ decoder
→ calibration
→ goal-evidence adapter
→ Bayesian inference
→ entropy
→ shared autonomy
→ approved goal
→ A*
→ safety
→ 2D environment
```

## Exit criteria

A real EEG-derived probability sequence can drive a reproducible simulated rescue episode.

---

# 38. MILESTONE M7 — EXPERIMENTS

## Required principal systems

```text
A — Direct EEG
B — Confidence-aware
C — Bayesian shared autonomy
D — Full system
```

## Required analysis

- EEG baseline comparison;
- calibration;
- Bayesian goal inference;
- uncertainty;
- task metrics;
- safety metrics;
- robustness/noise;
- cross-subject;
- ablation;
- failure cases.

## Exit criteria

All reportable claims are backed by stored result artifacts.

---

# 39. MILESTONE M8 — DASHBOARD & PORTFOLIO

## Sequence

Only after the core pipeline works:

```text
dashboard
→ final plots
→ technical report
→ README
→ demo
→ portfolio/resume wording
```

## Rule

No UI polish should block or replace scientific validation.

---

# 40. FIRST CODEX TASK — EXACT APPROVED START

The initial coding task remains:

> **Read `MASTER_PROJECT_SPEC.md` first. We are starting Milestone 1 only. Implement a clean MNE-Python data loader for the PhysioNet EEGBCI motor-imagery dataset. Initially support configurable subject IDs and runs 4, 8 and 12. Requirements: download through MNE utilities; cache locally; load EDF files; standardize channel names; attach the appropriate montage; print subject, channel count, sampling frequency, duration and annotations; add basic validation/error handling; write unit tests where practical; do not implement preprocessing or modelling yet. After coding, tell me: (1) files created/modified, (2) installation requirements, (3) exact command to run, (4) expected output, (5) what I should manually check. Do not continue beyond the loader.**

This remains the correct first scientific implementation ticket after M0 scaffolding.

---

# 41. MANUAL REVIEW GATES

The project owner must manually review at the following points.

## Gate A — Loader

Verify:

- real data;
- correct runs;
- channels;
- 160 Hz;
- annotations;
- montage.

## Gate B — Epochs

Verify:

- Left/Right label semantics;
- shapes;
- class balance;
- no obvious leakage.

## Gate C — CSP/LDA

Verify:

- CSP fits train only;
- probability output;
- held-out metrics.

## Gate D — EEGNet

Verify:

- architecture;
- training/validation split;
- checkpoint;
- probability output.

## Gate E — Calibration

Verify:

- fitting split;
- reliability diagram;
- ECE;
- Brier.

## Gate F — Bayesian

Verify:

- analytic synthetic examples;
- exact likelihood semantics before real EEG integration.

## Gate G — Planner/Safety

Verify:

- blocked path;
- hazard path;
- stop;
- replan.

## Gate H — End-to-End

Verify:

- real EEG-derived evidence;
- no hidden true-goal input;
- logs;
- correct control flow.

---

# 42. PROJECT STATE FILE RULES

## `PROJECT_STATE.md`

Contains:

- what is implemented;
- what is tested;
- current milestone;
- known failures;
- next candidate task.

It is navigation, not scientific proof.

---

## `CURRENT_TASK.md`

Contains:

- one active ticket;
- allowed files;
- acceptance criteria;
- stop condition.

---

## `DECISIONS.md`

Contains:

- approved scientific/architectural decisions;
- date;
- rationale;
- documents affected.

Unresolved items do not become decisions merely because code needs a value.

---

## `RESEARCH_LOG.md`

Contains:

- scientific references;
- findings;
- methodological reasoning;
- unresolved research questions.

---

## `EXPERIMENT_LOG.md`

Contains:

- experiments actually run;
- config;
- results;
- artifact paths;
- interpretation notes.

---

## `TODO.md`

Contains:

- backlog;
- optional extensions;
- known technical debt.

---

# 43. DEFINITION OF “DONE” FOR A MODULE

A module is complete only when:

```text
code exists
+
tests exist where practical
+
tests pass
+
manual check completed where required
+
interfaces match architecture
+
no hidden scope change
+
state updated
+
commit created
```

Code merely compiling is not enough.

---

# 44. SCIENTIFIC STOP CONDITIONS

Codex must stop and report instead of guessing when:

- event semantics are unclear;
- preprocessing parameters are unresolved;
- class order is ambiguous;
- train/test boundary is unclear;
- calibration split is missing;
- likelihood semantics are undefined;
- confidence thresholds are absent;
- adaptation rule is absent;
- hazard rule is absent;
- experiment baseline definition is unclear.

---

# 45. SOFTWARE STOP CONDITIONS

Codex should also stop when:

- required source file is missing;
- dependency conflict blocks execution;
- model checkpoint does not match input;
- dataset cannot be validated;
- tests reveal structural mismatch;
- a requested change would modify unrelated architecture.

---

# 46. DEBUGGING RULE

When a test fails:

```text
identify exact failure
→ make minimal fix
→ rerun affected test
→ rerun relevant regression tests
```

Do not respond to one error by rewriting large parts of the project.

---

# 47. NO “BUILD THE WHOLE PROJECT” PROMPT

Avoid tasks such as:

> “Build everything.”

Preferred:

> “Implement Module 1 loader only.”

Then:

> “Implement event extraction only.”

Then:

> “Implement CSP+LDA only.”

This reduces AI-generated scope drift.

---

# 48. CODE REVIEW RULE

After Codex completes a scientifically important module, ChatGPT should independently inspect:

- actual code;
- tests;
- relevant output;
- config;
- experiment artifacts.

Do not rely only on Codex's written summary.

---

# 49. REPRODUCIBILITY RULE

Every reportable experiment should be reconstructable from:

```text
code commit
config
dataset/split
model/checkpoint
calibrator
map/policy
seed
results
```

If not reproducible, it is not ready for final reporting.

---

# 50. RESULT DISCIPLINE

Never hard-code expected project performance.

Never engineer experiments to guarantee System D wins.

Valid outcomes include:

- CSP+LDA outperforming EEGNet;
- calibration adding little;
- Bayes improving reliability but increasing latency;
- safety increasing path length;
- adaptation helping only some subjects.

These are scientifically valid.

---

# 51. CLAIM DISCIPLINE DURING IMPLEMENTATION

Until results exist, say:

```text
designed to evaluate
intended to test
implements
supports
```

Do not say:

```text
improves by X%
reduces errors by X%
outperforms
achieves
```

without real verified evidence.

---

# 52. FORBIDDEN SCOPE EXPANSION

Codex must not introduce the following without explicit approval:

```text
LLMs
RAG
Gemini/OpenAI runtime API
AWS/cloud architecture
Kubernetes
blockchain
IoT
physical EEG hardware
physical robot
complex CV
3D simulation
mobile app
ROS 2
Gazebo
PPO
SNN
multiclass EEG
```

The last five remain possible future extensions only after the core.

---

# 53. FINAL IMPLEMENTATION COMPLETION CRITERIA

The core project is implementation-complete when:

1. real PhysioNet EEG loads correctly;
2. preprocessing/epochs are validated;
3. CSP+LDA works;
4. EEGNet/compact CNN works;
5. both expose real probability outputs;
6. calibration is implemented/evaluated;
7. Bayesian core performs valid sequential updates;
8. approved goal-evidence mapping is implemented;
9. entropy is operational;
10. uncertainty changes behavior;
11. adaptation is implemented as approved or explicitly scope-adjusted;
12. 2D environment works;
13. A* works;
14. safety rejects unsafe actions;
15. shared autonomy supports proceed/confirm/defer;
16. human confirm/override/pause/stop work;
17. offline EEG replay works;
18. end-to-end EEG-driven simulation works;
19. A/B/C/D experiments run;
20. robustness/ablation/cross-subject analysis runs;
21. logs/results are reproducible;
22. dashboard reflects actual system state;
23. no unsupported claims remain.

---

# 54. IMPLEMENTATION BLUEPRINT SUMMARY

The project should be built as a sequence of **small verified modules rather than one AI-generated monolith**. The EEG track begins with real PhysioNet loading, inspection, approved preprocessing, CSP+LDA, EEGNet, and calibration. In parallel, the cognitive track can implement a generic Bayesian filter and entropy using synthetic likelihoods, while the autonomy track can implement the 2D Gymnasium environment, A*, and explicit safety using artificial goals. Shared autonomy is then added as a separate state-machine layer with human confirmation, override, pause, and emergency stop. The major scientific integration boundary remains the unresolved conversion from binary Left/Right EEG class evidence into a valid Search & Rescue goal-likelihood representation; no agent may invent this mapping. Once that decision and the remaining thresholds/risk/adaptation parameters are explicitly approved, the three tracks are integrated into a full offline EEG replay pipeline, followed by automated A/B/C/D experiments, robustness, ablation, cross-subject evaluation, and only then the Streamlit presentation layer and final portfolio documentation.

---

# 55. NEXT DOCUMENT

The next planned document is:

**`16_REPOSITORY_AND_CODE_ARCHITECTURE.md` — Repository Structure, File Ownership, Interfaces, Naming, Configuration, Testing, Logging, and Git Workflow**

That document should define the final repository layout in detail, including:

- exact folder responsibilities;
- file naming;
- module imports;
- schemas/interfaces;
- configuration hierarchy;
- artifact locations;
- experiment IDs;
- model/result versioning;
- test organization;
- Git workflow;
- Codex-safe file boundaries;
- and persistent project-state documents.

It must not change the scientific implementation plan defined here.
