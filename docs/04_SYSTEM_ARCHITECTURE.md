# 04_SYSTEM_ARCHITECTURE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Complete Technical Architecture, Module Boundaries, Data Flow, Interfaces, Runtime Modes, and Integration Rules

**Document ID:** C-01  
**Document class:** System Design / Technical Architecture  
**Authority level:** Subordinate to the Master Authority Documents and the approved Search & Rescue Scenario Specification  
**Status:** Authoritative architecture baseline with unresolved choices explicitly preserved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND NON-INTERPRETATION RULE

This document defines the **technical architecture of the complete project**.

It must remain consistent with:

1. `MASTER_PROJECT_SPEC.md`
2. `01_PROJECT_CONCEPT_AND_PROBLEM.md`
3. `02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md`
4. `03_SEARCH_AND_RESCUE_SCENARIO.md`

If this architecture conflicts with any higher-authority document, the higher-authority document wins.

This document must **not** be interpreted as permission to:

- silently resolve the binary EEG-to-multiple-goal ambiguity;
- remove EEGNet because CSP+LDA works;
- remove Bayesian inference because the decoder already outputs probabilities;
- replace uncertainty with raw confidence alone;
- merge safety into the planner without preserving a distinct safety responsibility;
- turn the project into low-level EEG joystick control;
- add LLMs, RAG, cloud systems, 3D simulation, physical hardware, or microservices without explicit approval;
- claim live EEG acquisition;
- or invent performance values.

The architecture is **change-controlled**.

ChatGPT is the project brain/research director and architecture reviewer.  
The project owner is the final authority.  
Codex is the implementation engineer.  
Git/GitHub records the actual implementation and history.

---

# 1. PURPOSE OF THIS DOCUMENT

This document answers:

> **What are the system's technical components?**

> **How does information move from EEG data to autonomous rescue behaviour?**

> **What is each module allowed to know and do?**

> **What interfaces must remain stable so modules can be developed and tested independently?**

> **How do offline EEG replay, Bayesian inference, shared autonomy, planning, safety, adaptation, visualization, logging, and experiments integrate?**

The architecture is designed to support:

- modular development;
- independent testing;
- parallel implementation;
- controlled experiments;
- ablation studies;
- reproducibility;
- failure analysis;
- and future extensions without rewriting the scientific core.

---

# 2. ARCHITECTURAL PRINCIPLE

The complete system is divided into six scientific/engineering layers:

```text
LAYER 1 — EEG DATA & SIGNAL PROCESSING
LAYER 2 — EEG DECODING & PROBABILITY CALIBRATION
LAYER 3 — COGNITIVE / BAYESIAN INTENT & UNCERTAINTY
LAYER 4 — SHARED AUTONOMY & HUMAN AUTHORITY
LAYER 5 — AUTONOMOUS PLANNING & SAFETY
LAYER 6 — SIMULATION, LOGGING, EVALUATION & UI
```

These layers must remain logically separable.

The project is not one monolithic script.

---

# 3. LOCKED END-TO-END ARCHITECTURE

The intended final architecture is:

```text
Public prerecorded motor-imagery EEG
        ↓
EEG loader
        ↓
EEG inspection / validation
        ↓
EEG preprocessing
        ↓
event extraction + epoch creation
        ↓
        ├──────────────────────────────┐
        │                              │
        ▼                              ▼
CSP + LDA baseline              EEGNet / compact CNN
        │                              │
        └──────────────┬───────────────┘
                       ↓
             Unified decoder interface
                       ↓
              class probability vector
                       ↓
              probability calibration
                       ↓
            calibrated EEG evidence
                       ↓
         sequential Bayesian goal inference
                       ↓
              posterior belief over
           current goal/intention hypothesis
                       ↓
               uncertainty / entropy
                       ↓
              shared-autonomy policy
                       ↓
        ┌──────────────┼────────────────┐
        │              │                │
        ▼              ▼                ▼
     PROCEED        CONFIRM/DEFER     PAUSE/STOP
        │              │                │
        │          human response       │
        └──────────────┴────────────────┘
                       ↓
               approved mission goal
                       ↓
              autonomous A* planner
                       ↓
              proposed route/actions
                       ↓
                 safety controller
                       ↓
             safe/rejected/modified
                  action decision
                       ↓
               2D rescue environment
                       ↓
                 state transition
                       ↓
              human override / feedback
                       ↓
              adaptation if enabled
                       ↓
              next inference/control cycle
                       ↓
        logging + evaluation + dashboard
```

---

# 4. NON-NEGOTIABLE INFORMATION FLOW

The following information-flow rules are mandatory.

## Rule 1 — Raw EEG does not directly command the simulated agent

Raw EEG must pass through:

```text
preprocessing
→ decoder
→ probability layer
→ Bayesian/uncertainty layer
→ shared-autonomy logic
```

before it can affect autonomous mission behaviour.

---

## Rule 2 — Hard decoder labels are not sufficient downstream

Downstream reasoning must use **probabilistic evidence**.

The unified decoder interface must expose probabilities or calibrated scores suitable for probabilistic reasoning.

---

## Rule 3 — Bayesian inference must be a real separate module

The system may not rename a classifier's probability output as a "Bayesian posterior."

The Bayesian module must explicitly update belief over time using prior belief and incoming evidence.

---

## Rule 4 — Uncertainty must alter behaviour

The uncertainty module cannot exist only for visualization.

Its output must influence whether the system:

- proceeds;
- asks for confirmation;
- defers;
- pauses;
- or otherwise changes autonomy level.

---

## Rule 5 — Planning must not decide human intent

The planner receives an approved target.

It does not infer the human's intended target.

---

## Rule 6 — Safety must be able to override planning

A planner-generated action/path is not automatically executable.

The safety layer must be able to reject or constrain it.

---

## Rule 7 — Human emergency authority supersedes autonomy

Human:

- pause;
- override;
- emergency stop

must take precedence over autonomous execution.

---

## Rule 8 — Evaluation ground truth must not leak into inference

Experiment metadata may contain the true intended choice/goal for scoring.

The Bayesian/inference path must not receive that ground-truth field.

---

# 5. ARCHITECTURE LAYERS

# 5.1 Layer 1 — EEG Data & Signal Processing

Responsibilities:

- dataset access;
- caching;
- loading EDF data;
- channel normalization;
- montage assignment;
- event extraction;
- preprocessing;
- epoch construction;
- labels;
- subject metadata;
- inspection;
- validation.

This layer produces validated EEG trials suitable for modelling.

It does **not** perform:

- Bayesian reasoning;
- path planning;
- autonomy control;
- or safety.

---

# 5.2 Layer 2 — EEG Decoding & Calibration

Responsibilities:

- classical CSP+LDA modelling;
- EEGNet/compact CNN modelling;
- train/validation/test inference;
- probability outputs;
- probability calibration;
- unified model interface.

This layer converts EEG trials into evidence such as:

```text
P(Left | EEG)
P(Right | EEG)
```

It does not itself decide the final rescue action.

---

# 5.3 Layer 3 — Cognitive / Bayesian Intent & Uncertainty

Responsibilities:

- maintain prior belief;
- consume calibrated EEG evidence;
- perform sequential Bayesian updates;
- compute posterior;
- estimate uncertainty;
- expose confidence state;
- support adaptation of approved parameters.

This layer answers:

> **What does the system currently believe the human intends, and how uncertain is that belief?**

It does not plan movement.

---

# 5.4 Layer 4 — Shared Autonomy & Human Authority

Responsibilities:

- interpret posterior and uncertainty according to policy;
- determine whether to proceed or defer;
- request confirmation;
- handle override;
- handle pause;
- handle emergency stop;
- approve goal commitment.

This layer answers:

> **Should the system act autonomously yet?**

It is the bridge between uncertain human intent and autonomous execution.

---

# 5.5 Layer 5 — Autonomous Planning & Safety

Responsibilities:

- receive approved goal;
- compute A* path;
- incorporate risk-aware cost where approved;
- produce next action/path;
- validate proposed action through safety rules;
- replan when necessary.

This layer answers:

> **How should the approved objective be reached safely?**

---

# 5.6 Layer 6 — Simulation, Logging, Evaluation & UI

Responsibilities:

- execute discrete environment transitions;
- expose simulation state;
- replay EEG;
- record events;
- compute metrics;
- run experiments;
- show technical dashboard.

The UI observes and controls the system but must not contain hidden scientific logic that exists nowhere else.

---

# 6. REQUIRED MODULE INVENTORY

The architecture contains the following required modules.

---

## Module 0 — Configuration

**Suggested files:**

```text
config.yaml
src/config.py
```

### Purpose

Centralize experiment and runtime settings.

### May include

- dataset subjects;
- EEG runs;
- preprocessing parameters;
- epoch time window;
- channel selection;
- model settings;
- random seed;
- calibration settings;
- Bayesian settings;
- uncertainty thresholds;
- environment size;
- map ID;
- hazard settings;
- planner settings;
- safety settings;
- adaptation settings;
- logging paths.

### Mandatory rule

Scientific parameters must not be scattered as undocumented hard-coded constants.

---

## Module 1 — EEG Data Loader

**Suggested file:**

```text
src/eeg/loader.py
```

### Purpose

Load and validate PhysioNet EEG Motor Movement/Imagery data through MNE.

### Initial direction

Support configurable:

- subject IDs;
- runs 4, 8, 12.

### Responsibilities

- download through MNE utilities;
- cache locally;
- load EDF;
- standardize channel names where needed;
- attach appropriate montage;
- preserve annotations;
- expose metadata;
- perform basic validation.

### Minimum output

A validated MNE Raw object or equivalent typed structure plus subject/run metadata.

### Must not

- preprocess;
- train model;
- infer intent;
- modify labels silently.

---

## Module 2 — EEG Visualization / Inspection

**Suggested file:**

```text
src/eeg/visualization.py
```

### Purpose

Scientific inspection of EEG data.

### May show

- raw EEG traces;
- montage/channel positions;
- power spectral density;
- epoch examples;
- class distribution;
- selected-channel data.

### Role

Validation and debugging.

Not a core inference dependency.

---

## Module 3 — EEG Preprocessing and Epoch Extraction

**Suggested files:**

```text
src/eeg/preprocessing.py
src/eeg/epochs.py
```

### Purpose

Convert Raw EEG into model-ready trials.

### Conceptual flow

```text
Raw EEG
→ channel checks
→ band-pass filtering
→ event extraction
→ event mapping
→ epoching
→ quality checks
→ X, y, subject metadata
```

### Required outputs

Conceptually:

```text
X: trials × channels × samples
y: class labels
subject_ids
run_ids / metadata
sampling information
```

### Scientific requirements

- correct event mapping;
- no label leakage;
- no train/test leakage;
- preprocessing parameters configurable;
- preprocessing fitted only on training data where fitting is required.

---

## Module 4 — CSP + LDA Baseline

**Suggested file:**

```text
src/models/csp_lda.py
```

### Purpose

Provide the mandatory classical motor-imagery baseline.

### Responsibilities

- fit CSP on training data only;
- transform EEG features;
- train LDA;
- expose predicted labels;
- expose probabilities or compatible confidence output;
- save/load fitted pipeline where appropriate.

### Must support

- reproducible evaluation;
- downstream calibration;
- comparison against EEGNet.

---

## Module 5 — EEGNet / Compact CNN Decoder

**Suggested file:**

```text
src/models/eegnet.py
```

### Purpose

Provide the mandatory neural EEG decoder in the intended final system.

### Responsibilities

- define model;
- train;
- validate;
- save checkpoint;
- load checkpoint;
- predict;
- output probability vector.

### Scientific requirement

The architecture must remain compact and appropriate to EEG rather than adding depth merely for complexity.

### Must not

- fabricate performance;
- perform downstream Bayesian reasoning internally.

---

## Module 6 — Unified Decoder / Inference Interface

**Suggested file:**

```text
src/models/inference.py
```

### Purpose

Decouple downstream cognitive modules from the model type.

### Required conceptual interface

```python
prediction = decoder.predict_proba(eeg_epoch)
```

### Conceptual output

```text
DecoderPrediction:
    model_id
    class_names
    probabilities
    predicted_class
    timestamp / trial index
    subject metadata reference
```

### Benefit

The Bayesian layer should not care whether evidence came from:

- CSP+LDA;
- EEGNet;
- or a later approved decoder.

---

## Module 7 — Probability Calibration

**Suggested file:**

```text
src/models/calibration.py
```

### Purpose

Transform raw model probabilities into better calibrated evidence where required.

### Possible methods

The exact method is unresolved.

Candidates may later include:

- temperature scaling;
- Platt-style calibration;
- isotonic calibration;
- another justified method.

No method is approved by this document.

### Conceptual interface

```text
raw probability vector
→ calibrator
→ calibrated probability vector
```

### Required metadata

Record:

- calibration method;
- calibration fitting split;
- model version;
- calibration parameters/version.

### Leakage rule

Calibration must not be fitted on the final test set.

---

## Module 8 — Bayesian Goal / Intent Inference

**Suggested file:**

```text
src/cognition/bayesian_intent.py
```

### Purpose

Maintain sequential probabilistic belief about the current intended choice/goal.

### Core form

\[
P(G \mid E_{1:t})
\propto
P(E_t \mid G)P(G \mid E_{1:t-1})
\]

### State

Conceptually:

```text
goal hypotheses
prior
current posterior
evidence history
update count
```

### Responsibilities

- initialize prior;
- update posterior;
- normalize probabilities;
- expose posterior;
- reset between episodes/decisions as required;
- log evidence.

### Critical unresolved dependency

The exact mapping between:

```text
Left / Right EEG class probabilities
```

and:

```text
Search & Rescue goal hypotheses
```

is **not yet approved**.

Therefore the Bayesian module must be designed so the mapping policy is external/configurable rather than hard-wired into the mathematical core.

---

## Module 9 — Uncertainty Estimation

**Suggested file:**

```text
src/cognition/uncertainty.py
```

### Purpose

Measure uncertainty in current belief.

### Initial approved measure

Entropy:

\[
H(P)=-\sum_i p_i\log p_i
\]

Normalized entropy may be used if justified for comparison across different hypothesis counts.

### Responsibilities

- consume posterior;
- compute uncertainty;
- classify confidence state according to configured policy;
- expose value to shared-autonomy controller;
- log uncertainty.

### Must not

hard-code final confidence thresholds until approved.

---

## Module 10 — Adaptation / User-Specific Adjustment

**Suggested file:**

```text
src/cognition/adaptation.py
```

### Purpose

Support the intended adaptive component using correction/history where scientifically justified.

### Potential targets

- prior distribution;
- user reliability estimate;
- confidence thresholds;
- evidence weighting;
- another owner-approved parameter.

### Status

**Mechanism unresolved.**

### Architectural requirement

Adaptation must be modular and switchable so experiments can compare:

```text
adaptation ON
vs
adaptation OFF
```

### Claim restriction

If the implementation only updates priors or thresholds, documentation must say exactly that.

---

## Module 11 — Search & Rescue Environment

**Suggested file:**

```text
src/autonomy/environment.py
```

### Planned framework

Gymnasium.

### Purpose

Represent the simple 2D technical scenario.

### Core state

- map dimensions;
- agent position;
- candidate goals;
- blocked cells;
- hazard/risk map;
- current mission state;
- terminal state.

### Initial discrete actions

```text
UP
DOWN
LEFT
RIGHT
WAIT
```

### Responsibilities

- validate actions;
- update state;
- determine terminal conditions;
- expose observations;
- support seeded reset;
- provide map metadata.

### Must not

contain hidden Bayesian inference or model logic.

---

## Module 12 — Autonomous Planner

**Suggested file:**

```text
src/autonomy/planner.py
```

### Initial algorithm

A*.

### Input

- current environment state;
- approved goal;
- obstacle map;
- risk data.

### Output

- path;
- next planned action;
- planning status;
- path cost.

### Risk-aware planning

Conceptual cost:

\[
J = \text{distance} + \lambda \cdot \text{risk}
\]

Exact risk representation and \(\lambda\) remain unresolved.

### Must support

- no-path condition;
- replanning;
- deterministic testing.

---

## Module 13 — Safety Controller

**Suggested file:**

```text
src/autonomy/safety.py
```

### Purpose

Provide explicit safety enforcement independent of task optimization.

### Inputs

- proposed action/path;
- current environment state;
- hazard/constraint configuration;
- emergency-stop state.

### Outputs

Conceptually:

```text
SafetyDecision:
    proposed_action
    approved_action
    safe: bool
    intervention_type
    reason
```

### Responsibilities

- reject out-of-bounds action;
- reject blocked-cell action;
- enforce prohibited hazard constraints;
- respect stop state;
- trigger replan where needed;
- log intervention.

### Mandatory rule

Safety may not be only a penalty term.

At least some safety constraints must have explicit enforcement semantics.

---

## Module 14 — Shared-Autonomy Controller

**Suggested file:**

```text
src/autonomy/shared_controller.py
```

### Purpose

Convert posterior + uncertainty + human state into an autonomy decision.

### Inputs

- posterior;
- inferred candidate goal;
- uncertainty;
- configured policy;
- human state;
- current mission state.

### Outputs

Conceptually:

```text
AutonomyDecision:
    mode
    candidate_goal
    approved_goal
    requires_confirmation
    reason
```

### Conceptual modes

```text
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

Exact threshold logic is not yet frozen.

### Mandatory rule

This module must not silently use true experiment goal.

---

## Module 15 — Human Interaction Layer

**Suggested file:**

```text
src/app/human_interface.py
```

or another implementation-consistent location.

### Purpose

Represent human authority actions.

### Required interactions

- confirm;
- override;
- pause;
- resume if supported;
- emergency stop.

### Responsibilities

- forward human actions to shared-autonomy state;
- log actions;
- prevent UI-only state from diverging from control state.

### Critical rule

Emergency stop must propagate to execution/safety immediately.

---

## Module 16 — Offline EEG Replay

**Suggested file:**

```text
src/eeg/replay.py
```

or:

```text
src/app/eeg_replay.py
```

### Purpose

Feed prerecorded EEG trials/windows to the system in an ordered stream.

### Correct terminology

- offline EEG replay;
- simulated real-time BCI.

### Must not be described as

- live EEG;
- online acquisition;
- real-time neural sensing from a headset.

### Responsibilities

- select subject/trial;
- replay in defined sequence;
- preserve timestamps/order where needed;
- pass epochs/windows to decoder;
- support reproducible replay.

---

## Module 17 — Technical Dashboard

**Suggested file:**

```text
src/app/dashboard.py
```

### Planned tool

Streamlit.

### Purpose

Technical inspection and demonstration.

### May display

- current subject/trial;
- EEG replay status;
- decoder probabilities;
- calibrated probabilities;
- Bayesian posterior;
- entropy;
- autonomy mode;
- candidate/approved goal;
- 2D map;
- planned route;
- safety intervention;
- human controls;
- episode metrics.

### Mandatory rule

The dashboard must not be the only place where scientific logic exists.

---

## Module 18 — Experiment Logger

**Suggested file:**

```text
src/evaluation/logger.py
```

### Purpose

Record a complete trace of each experiment.

### Required metadata where applicable

- experiment ID;
- episode ID;
- timestamp;
- random seed;
- Git commit;
- config hash/path;
- subject;
- runs/trials;
- model ID;
- model checkpoint/version;
- calibration method/version;
- posterior history;
- uncertainty history;
- autonomy decisions;
- planner outputs;
- safety interventions;
- human interventions;
- environment state;
- terminal state;
- metrics.

### Output formats

Prefer machine-readable:

```text
CSV
JSON
JSONL
```

as appropriate.

---

## Module 19 — EEG / Model Evaluation

**Suggested file:**

```text
src/evaluation/eeg_metrics.py
```

### Responsibilities

Compute and export:

- accuracy;
- balanced accuracy;
- precision;
- recall;
- F1;
- confusion matrix;
- calibration metrics;
- subject-wise results;
- cross-subject results.

ROC-AUC may be used if appropriate to the final binary protocol.

---

## Module 20 — Shared-Autonomy / System Evaluation

**Suggested files:**

```text
src/evaluation/autonomy_metrics.py
src/evaluation/experiments.py
```

### Responsibilities

Compute and export:

- task success;
- wrong-goal rate;
- safety violations;
- unsafe action attempts;
- interventions;
- confirmation/deferral rate;
- decision latency;
- completion time;
- path length;
- path efficiency;
- replanning;
- robustness measures;
- ablation comparisons.

---

# 7. RECOMMENDED SUPPORTING MODULES

These are support structures, not new scientific components.

---

## 7.1 Data structures / schemas

Recommended location:

```text
src/types.py
```

or:

```text
src/schemas/
```

Purpose:

Define stable typed objects for module communication.

Possible structures:

```text
EEGEpoch
DecoderPrediction
CalibratedEvidence
IntentBelief
UncertaintyEstimate
AutonomyDecision
PlanningResult
SafetyDecision
HumanAction
EnvironmentState
EpisodeRecord
```

These structures should avoid passing arbitrary dictionaries everywhere.

---

## 7.2 Reproducibility utilities

Recommended location:

```text
src/utils/reproducibility.py
```

Responsibilities:

- set random seeds;
- record package versions;
- get Git commit hash;
- create experiment run ID.

---

## 7.3 Validation utilities

Recommended location:

```text
src/utils/validation.py
```

Responsibilities:

- probability normalization checks;
- shape checks;
- finite-value checks;
- map validation;
- configuration validation.

---

# 8. CORE DATA CONTRACTS

The exact Python classes may change during implementation, but the conceptual contracts must remain.

---

## 8.1 EEG trial contract

```text
EEGEpoch
    data
    sampling_frequency
    channel_names
    label
    subject_id
    run_id
    trial_id
```

No downstream module should need to rediscover subject identity from filenames.

---

## 8.2 Decoder output contract

```text
DecoderPrediction
    model_id
    class_names
    probabilities
    predicted_class
    subject_id
    trial_id
```

Requirements:

\[
0 \le p_i \le 1
\]

and:

\[
\sum_i p_i \approx 1
\]

---

## 8.3 Calibrated evidence contract

```text
CalibratedEvidence
    class_names
    raw_probabilities
    calibrated_probabilities
    calibration_method
    model_id
    trial_id
```

---

## 8.4 Intent belief contract

```text
IntentBelief
    hypothesis_names
    prior
    likelihood
    posterior
    update_index
    evidence_reference
```

The final goal names depend on the unresolved mapping policy.

---

## 8.5 Uncertainty contract

```text
UncertaintyEstimate
    entropy
    normalized_entropy
    confidence_state
    threshold_policy_id
```

`normalized_entropy` may be omitted if not used.

---

## 8.6 Autonomy decision contract

```text
AutonomyDecision
    mode
    candidate_goal
    approved_goal
    requires_confirmation
    confidence
    reason
```

---

## 8.7 Planning contract

```text
PlanningResult
    start
    goal
    path
    path_cost
    risk_cost
    status
```

Possible status values:

```text
SUCCESS
NO_PATH
INVALID_GOAL
REPLAN_REQUIRED
```

---

## 8.8 Safety decision contract

```text
SafetyDecision
    proposed_action
    approved_action
    safe
    intervention
    reason
```

---

## 8.9 Environment transition contract

Conceptually:

```text
observation, reward, terminated, truncated, info
```

if implemented through Gymnasium.

Reward may exist because Gymnasium uses it, but reward is **not the definition of safety**.

---

# 9. BINARY EEG-TO-GOAL MAPPING ARCHITECTURAL SEAM

This is the most important unresolved architecture boundary.

The system must include a conceptual adapter:

```text
EEG class evidence
        ↓
Goal Mapping Policy
        ↓
Bayesian goal hypotheses
```

The adapter must remain replaceable.

Possible future implementations include:

```text
TwoGoalMapping
HierarchicalBinaryMapping
AbstractPriorityMapping
MulticlassMapping
```

These names are illustrative interface concepts only.

No mapping is approved here.

## Critical rule

Do not place arbitrary code such as:

```python
if left:
    goal = victim_a
else:
    goal = medical_station
```

inside the EEG decoder.

The EEG decoder's scientific task is Left-vs-Right motor imagery.

The application mapping belongs in a separate policy layer.

---

# 10. COMPLETE RUNTIME DATA FLOW

## 10.1 Initialization

```text
Load config
→ set seed
→ identify experiment mode
→ load model/calibrator
→ initialize Bayesian belief
→ initialize environment
→ initialize safety controller
→ initialize logger
```

---

## 10.2 EEG evidence cycle

```text
EEG replay
→ epoch/window
→ decoder.predict_proba()
→ raw probabilities
→ calibrator
→ calibrated probabilities
→ goal-mapping adapter
→ Bayesian update
→ posterior
→ uncertainty
```

---

## 10.3 Shared-autonomy cycle

```text
posterior + uncertainty
→ shared-autonomy controller
→ PROCEED / CONFIRM / DEFER / PAUSE / STOP
```

If confirmation is required:

```text
request human confirmation
→ receive CONFIRM / OVERRIDE / PAUSE / STOP
→ update control state
```

---

## 10.4 Autonomous execution cycle

If the goal is approved:

```text
environment state + approved goal
→ A* planner
→ planned path / next action
→ safety controller
→ approved safe action or rejection
→ environment.step()
→ new environment state
```

---

## 10.5 Feedback cycle

```text
new state
+ human intervention
+ safety intervention
+ task outcome
→ logger
→ adaptation module if enabled/appropriate
→ next control cycle
```

---

# 11. STATE MACHINES

# 11.1 Shared-autonomy state machine

Recommended conceptual states:

```text
WAITING_FOR_EEG
INFER_INTENT
UNCERTAIN
WAITING_FOR_CONFIRMATION
GOAL_APPROVED
NAVIGATING
PAUSED
STOPPED
COMPLETED
FAILED
```

Conceptual transitions:

```text
WAITING_FOR_EEG
    → INFER_INTENT

INFER_INTENT
    → UNCERTAIN
    → WAITING_FOR_CONFIRMATION
    → GOAL_APPROVED

UNCERTAIN
    → INFER_INTENT
    → WAITING_FOR_CONFIRMATION

WAITING_FOR_CONFIRMATION
    → GOAL_APPROVED
    → INFER_INTENT        [override/reselect]
    → PAUSED
    → STOPPED

GOAL_APPROVED
    → NAVIGATING

NAVIGATING
    → NAVIGATING         [normal step/replan]
    → PAUSED
    → STOPPED
    → COMPLETED
    → FAILED

PAUSED
    → NAVIGATING / INFER_INTENT
    → STOPPED
```

Exact transition policy is implementation detail but must preserve human authority and uncertainty deferral.

---

# 11.2 Safety state

Conceptually:

```text
SAFE
INTERVENTION_REQUIRED
REPLAN_REQUIRED
EMERGENCY_STOP
```

Safety state must be distinct from task success state.

---

# 12. PLANNER–SAFETY RELATIONSHIP

The planner proposes.

The safety controller authorizes.

This ordering is intentional:

```text
planner
→ proposed action/path
→ safety controller
→ executable action
```

Do not reverse the scientific responsibility by allowing the planner to be the sole safety authority.

Some hazard information can be used in the planner's cost function.

However:

```text
risk-aware planning
```

and:

```text
hard safety enforcement
```

are not the same thing.

A risk cost may prefer safer routes.

A hard safety rule prevents forbidden behaviour.

---

# 13. HUMAN AUTHORITY PATH

Human actions must bypass ordinary inference where necessary.

```text
Emergency Stop
        ↓
Shared Autonomy State
        ↓
Safety Controller
        ↓
Execution halted
```

Similarly:

```text
Pause
→ prevent new movement

Override
→ invalidate/revise current intent commitment

Confirm
→ approve current candidate according to policy
```

The UI must not merely display these controls; their state must reach the underlying control architecture.

---

# 14. ADAPTATION FEEDBACK PATH

Because the adaptation mechanism remains unresolved, the architecture provides a generic feedback path:

```text
human correction / override
        +
model confidence
        +
posterior history
        +
task outcome
        ↓
adaptation module
        ↓
approved adaptable parameter(s)
        ↓
future inference/control
```

Potential targets may include:

- prior;
- reliability estimate;
- threshold;
- evidence weight.

No target is finalized.

## Mandatory experimental property

Adaptation must be switchable off without breaking the rest of the architecture.

---

# 15. OFFLINE EEG REPLAY ARCHITECTURE

The core project does not acquire live brain signals.

Replay architecture:

```text
PhysioNet dataset
        ↓
preprocessed stored or generated epoch
        ↓
replay scheduler
        ↓
decoder
        ↓
rest of system
```

The replay scheduler may introduce controlled timing so the interface resembles online operation.

This does not change the fact that the data are prerecorded.

Every UI/report must use:

> **Offline EEG Replay**

or:

> **Simulated Real-Time BCI**

where relevant.

---

# 16. EXPERIMENT MODES

The architecture must support multiple modes without duplicating the project.

---

## Mode A — EEG model evaluation only

```text
EEG
→ preprocessing
→ CSP+LDA / EEGNet
→ calibration
→ EEG metrics
```

No simulation required.

---

## Mode B — Cognitive layer test with synthetic probabilities

```text
synthetic probability sequences
→ Bayesian inference
→ uncertainty
→ shared-autonomy decision
```

Purpose:

Develop/test Bayesian and uncertainty logic before EEG decoder is complete.

---

## Mode C — Autonomy test with artificial goals

```text
explicit artificial goal
→ planner
→ safety
→ environment
```

Purpose:

Develop/test autonomy before EEG integration.

---

## Mode D — Shared-autonomy integration with synthetic intent

```text
synthetic posterior/evidence
→ shared autonomy
→ planner
→ safety
→ environment
```

---

## Mode E — Full offline EEG replay

```text
real EEG
→ complete architecture
→ Search & Rescue simulation
```

This is the main integrated demonstration mode.

---

## Mode F — Automated experiment mode

Headless or minimally interactive execution for:

- baselines;
- ablations;
- noise experiments;
- subject experiments;
- repeated episodes.

The research must not depend on manually clicking Streamlit for every experimental run.

---

# 17. PRINCIPAL EXPERIMENT CONFIGURATIONS

The architecture must make the following configurations possible.

## System A — Direct EEG control

Purpose:

Establish the simplest neural-control reference.

Conceptually:

```text
decoder output
→ direct decision/commitment
```

Safety treatment must be defined carefully in the Experimental Design document so comparisons are fair.

---

## System B — Confidence-aware EEG control

```text
decoder
→ confidence/uncertainty
→ act or defer
```

No sequential Bayesian goal inference.

---

## System C — Bayesian shared autonomy

```text
EEG evidence
→ Bayesian goal inference
→ autonomous navigation
```

Exact inclusion/exclusion of calibration and safety in controlled comparisons must be formally defined later.

---

## System D — Full NeuroCognitive system

```text
EEG
+ calibration
+ Bayesian inference
+ uncertainty
+ shared autonomy
+ safety
+ adaptation
```

This is the intended full architecture.

---

# 18. ABLATION SUPPORT

The implementation must allow at least:

```text
Full system
Full - Bayesian inference
Full - uncertainty gating
Full - safety
Full - adaptation
```

The architecture should avoid dependencies that make these impossible.

For example:

- safety should not be hard-coded inside the planner;
- adaptation should not overwrite baseline parameters irreversibly;
- Bayesian inference should not be embedded inside EEGNet;
- uncertainty should not be inseparable from the dashboard.

---

# 19. ROBUSTNESS INJECTION POINTS

Controlled perturbations may be injected at defined boundaries.

## EEG evidence noise

```text
decoder/calibrated probability
→ controlled perturbation
→ Bayesian layer
```

Purpose:

Study degraded neural evidence.

---

## Environment changes

```text
map state
→ block path / alter hazard
→ planner replan
```

Purpose:

Study autonomy/safety robustness.

---

## Cross-subject variation

Handled at EEG dataset/model evaluation level through the approved subject split.

---

## Important restriction

Noise/perturbation mechanisms must be logged and reproducible.

No arbitrary hidden randomness.

---

# 20. DATA LEAKAGE BOUNDARIES

The architecture must enforce these boundaries.

## Training-only fitted components

Anything that learns from data must be fitted without final test-set information.

Examples:

- CSP;
- LDA;
- EEGNet parameters;
- normalization requiring fitted statistics;
- calibration model;
- learned adaptation model if applicable.

---

## Test metadata boundary

The following may exist for evaluation:

```text
true EEG label
true intended experimental choice/goal
subject ID
condition
```

but must not enter the inference path except where a specific supervised training protocol permits it.

---

# 21. ERROR HANDLING ARCHITECTURE

The system should fail explicitly rather than silently.

Examples:

## EEG errors

- dataset missing;
- invalid subject;
- missing run;
- inconsistent channels;
- missing annotations;
- invalid epoch shape.

## Model errors

- missing checkpoint;
- class order mismatch;
- NaN probabilities;
- probabilities not normalized.

## Bayesian errors

- zero/invalid normalization;
- hypothesis mismatch;
- invalid prior;
- non-finite posterior.

## Environment errors

- invalid map;
- start inside obstacle;
- goal inside blocked cell;
- no valid action.

## Planner errors

- no path;
- invalid goal.

## Safety errors

- undefined constraint;
- impossible approved action.

## Runtime response

Errors should:

- produce descriptive messages;
- be logged;
- avoid silently substituting fabricated defaults;
- stop the relevant experiment when scientific validity is compromised.

---

# 22. CONFIGURATION HIERARCHY

Recommended precedence:

```text
default config
        ↓
experiment config
        ↓
command-line/runtime override
```

Every final resolved configuration should be saved with the experiment output.

Do not allow the dashboard to change scientific settings without recording them.

---

# 23. DETERMINISM AND REPRODUCIBILITY

Where technically possible:

- set Python random seed;
- set NumPy seed;
- set PyTorch seed;
- use deterministic evaluation settings where appropriate;
- record subject splits;
- record package versions;
- record model checkpoint;
- record config;
- record Git commit.

Perfect GPU determinism is not guaranteed in every operation, but nondeterminism must not be ignored.

---

# 24. RECOMMENDED REPOSITORY ARCHITECTURE

The approved conceptual repository remains:

```text
neurocognitive-shared-autonomy/
│
├── README.md
├── MASTER_PROJECT_SPEC.md
├── 01_PROJECT_CONCEPT_AND_PROBLEM.md
├── 02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md
├── 03_SEARCH_AND_RESCUE_SCENARIO.md
├── 04_SYSTEM_ARCHITECTURE.md
│
├── AGENTS.md / Codex instruction file        # exact final filename to be standardized
├── PROJECT_STATE.md
├── CURRENT_TASK.md
├── DECISIONS.md
├── RESEARCH_LOG.md
├── EXPERIMENT_LOG.md
├── TODO.md
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
│   │   └── adaptation.py
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
├── results/
│   ├── figures/
│   ├── tables/
│   └── logs/
│
├── experiments/
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

The detailed Repository & Code Architecture document may refine this layout later.

---

# 25. MODULE DEPENDENCY DIRECTION

Dependencies should flow primarily downward:

```text
eeg
↓
models
↓
cognition
↓
autonomy
↓
environment
↓
evaluation/app
```

But utility/config/schema modules may be shared.

Avoid circular imports such as:

```text
environment imports dashboard
dashboard imports environment
```

or:

```text
bayesian_intent imports shared_controller
shared_controller imports bayesian_intent
```

Use data contracts/interfaces to prevent circular coupling.

---

# 26. MODULES THAT MUST NOT BE COUPLED

The following should remain separate.

## EEGNet and Bayesian inference

Reason:

Need ablation and model substitution.

---

## Bayesian inference and A*

Reason:

Intent reasoning should remain independent of route planning.

---

## A* and safety enforcement

Reason:

Need separate risk-aware planning versus hard safety ablation.

---

## Streamlit and control algorithms

Reason:

Need automated/headless experiments.

---

## Adaptation and baseline parameters

Reason:

Need adaptation ON/OFF comparison.

---

## Evaluation ground truth and inference

Reason:

Avoid leakage.

---

# 27. TESTING BOUNDARIES BY MODULE

Each module needs direct tests where practical.

## Loader

Test:

- valid subject/run;
- invalid subject/run;
- channel metadata;
- annotations.

## Preprocessing

Test:

- expected output dimensions;
- label mapping;
- finite values;
- no accidental trial loss beyond documented rules.

## CSP+LDA

Test:

- fit/predict;
- probabilities;
- reproducibility.

## EEGNet

Test:

- forward-pass shape;
- training smoke test;
- checkpoint load/save;
- probability shape.

## Calibration

Test:

- output range;
- normalization;
- fit/test separation.

## Bayesian inference

Test with synthetic probabilities:

- uniform evidence preserves uncertainty;
- repeated evidence shifts posterior;
- normalization;
- reset.

## Uncertainty

Test:

- certainty has low entropy;
- uniform distribution has maximal/high entropy.

## Planner

Test:

- shortest valid path;
- blocked path;
- no-path condition;
- risk path.

## Safety

Test:

- blocked action rejected;
- prohibited hazard rejected;
- stop state respected.

## Shared controller

Test:

- high confidence;
- intermediate confidence;
- low confidence;
- override;
- pause;
- stop.

## Environment

Test:

- legal actions;
- illegal actions;
- terminal state;
- deterministic reset.

## Integration

Test:

```text
synthetic EEG probabilities
→ Bayes
→ uncertainty
→ shared controller
→ planner
→ safety
→ environment
```

before requiring the trained EEG model.

---

# 28. PARALLEL DEVELOPMENT ARCHITECTURE

The project is deliberately designed for parallel implementation.

Three tracks can proceed independently.

## Track A — EEG pipeline

```text
loader
→ preprocessing
→ CSP/LDA
→ EEGNet
→ calibration
```

---

## Track B — Cognitive / probabilistic layer

```text
synthetic class probabilities
→ Bayesian inference
→ entropy
→ confidence policy
→ adaptation tests
```

---

## Track C — Autonomy layer

```text
artificial goal
→ 2D environment
→ A*
→ safety
→ shared-controller integration
```

Then:

```text
Track A
 + Track B
 + Track C
        ↓
full integration
```

This is a key architecture decision because it prevents one subsystem from blocking all development.

---

# 29. IMPLEMENTATION MILESTONES MAPPED TO ARCHITECTURE

## M0 — Infrastructure

- repository;
- configs;
- authority docs;
- schemas;
- logging skeleton;
- tests;
- project-state files.

## M1 — EEG data pipeline

- loader;
- inspection;
- preprocessing;
- epochs;
- CSP+LDA.

## M2 — Neural decoder

- EEGNet;
- checkpointing;
- evaluation;
- baseline comparison.

## M3 — Cognitive/math layer

- calibration;
- Bayesian inference;
- uncertainty;
- adaptation framework.

Can use synthetic probability streams.

## M4 — Autonomy environment

- Gymnasium 2D environment;
- A*;
- hazards;
- safety.

Can use artificial goals.

## M5 — Shared autonomy

- confidence policy;
- confirm;
- override;
- pause;
- stop.

## M6 — EEG integration

```text
real EEG
→ decoder
→ calibration
→ Bayes
→ uncertainty
→ shared autonomy
→ planning
→ safety
→ environment
```

## M7 — Experiments

- A/B/C/D;
- noise;
- cross-subject;
- ablations;
- results artifacts.

## M8 — UI and portfolio layer

- Streamlit;
- final plots;
- README;
- documentation;
- demo.

---

# 30. CURRENT FIRST IMPLEMENTATION UNIT

The previously approved first technical implementation unit after infrastructure is:

> **Implement a clean MNE-Python data loader for the PhysioNet EEGBCI dataset, initially supporting configurable subject IDs and runs 4, 8, and 12.**

The loader milestone must not include preprocessing or modelling.

This architecture preserves that boundary.

---

# 31. CHATGPT + CODEX OPERATING MODEL

The development workflow is:

```text
ChatGPT
  ↓
scientific/architecture reasoning
  ↓
narrow implementation ticket
  ↓
project owner approval / relay
  ↓
Codex
  ↓
code + tests + execution
  ↓
Git commit + artifacts
  ↓
ChatGPT independent review
  ↓
PASS / FAIL / corrective ticket
```

ChatGPT should review:

- actual code;
- tests;
- outputs;
- experiment logs;
- relevant configs.

`PROJECT_STATE.md` is useful navigation but is **not proof of correctness**.

Codex must not declare a scientific component correct merely because code runs.

---

# 32. IMPLEMENTATION TICKET CONTRACT

A good task passed to Codex should contain:

```text
Task ID
Objective
Inputs
Outputs
Allowed files
Forbidden files
Requirements
Scientific constraints
Acceptance criteria
Validation commands
Stop conditions
```

Example architecture principle:

```text
TASK: EEG loader
Do:
- download/load/cache data
- validate channels/metadata
- add tests

Do not:
- preprocess
- train
- alter project architecture
```

This prevents scope drift.

---

# 33. LOGGING ARCHITECTURE

Two different kinds of logging are required.

## 33.1 Engineering/runtime logs

Examples:

- dataset load;
- model load;
- planner failure;
- invalid action;
- exception.

---

## 33.2 Scientific experiment logs

Examples:

- probabilities;
- posterior;
- entropy;
- autonomy mode;
- goal decision;
- safety action;
- task outcome;
- metrics.

These should not be confused.

---

# 34. MODEL AND RESULT VERSIONING

Every evaluated model should have a stable identifier.

Example conceptual form:

```text
eegnet_subjectwise_v001
csp_lda_binary_v001
calibrator_eegnet_v001
```

Do not overwrite models/results without trace.

Result folders should include an experiment identifier.

---

# 35. USER INTERFACE ARCHITECTURE

The dashboard should consume the same system interfaces used by headless experiments.

Recommended pattern:

```text
Core Controller / Experiment Runner
        ↑
        │
Streamlit Dashboard
```

Not:

```text
Streamlit button callback
→ hidden Bayes logic
→ hidden planner logic
```

This keeps experiments reproducible.

---

# 36. PERFORMANCE CONSIDERATIONS

This project prioritizes scientific correctness over real-time optimization.

However:

- EEG inference should be practical for replay;
- A* should be fast in a small grid;
- logging should not alter decisions;
- experiment runner should support batches;
- neural training should avoid unnecessary model size.

No distributed compute architecture is required.

No AWS is required.

---

# 37. SECURITY / PRIVACY BOUNDARY

The initial dataset is public prerecorded research data.

The architecture does not require:

- user accounts;
- authentication;
- cloud storage;
- personal medical records.

If a future human study is added, participant data handling becomes a separate requirement.

Do not build authentication or cloud privacy infrastructure into the core project merely for appearance.

---

# 38. FUTURE EXTENSION SEAMS

The architecture intentionally permits later replacement or extension.

Possible seams:

```text
EEG decoder
→ alternative decoder / SNN

Goal mapping policy
→ hierarchical mapping / multiclass

Planner
→ PPO comparison / different planner

Environment
→ ROS 2 / Gazebo transfer

Adaptation
→ richer personalization

EEG source
→ live headset
```

These are future seams, not current scope.

The core implementation must remain valid without them.

---

# 39. ARCHITECTURAL ANTI-PATTERNS — DO NOT DO

Do not create:

## One giant `main.py`

All scientific logic inside one script destroys ablation and testing.

---

## Dashboard-driven science

No model fitting or experimental truth should depend solely on UI callbacks.

---

## Hidden goal leakage

Do not send the true experiment target into the Bayes module.

---

## Hard-coded fabricated metrics

Never place expected accuracy or success values into code as results.

---

## Fake Bayesian layer

Do not rename softmax confidence as Bayesian inference.

---

## Fake safety

Do not merely color hazards red while allowing the agent to enter them unchanged.

---

## Fake adaptation

Do not call a static threshold "adaptive."

---

## Fake real-time BCI

Do not hide that EEG is prerecorded.

---

## Scope inflation

Do not add:

- LLM;
- RAG;
- blockchain;
- AWS;
- IoT;
- computer vision;
- 3D engine;
- physical robot;

without an approved scientific reason.

---

# 40. OPEN ARCHITECTURAL DECISIONS

The following remain unresolved and must not be silently implemented as permanent decisions.

## 40.1 EEG-to-goal mapping

Critical and unresolved.

Options previously preserved:

- two active goals;
- hierarchical binary choice;
- abstract binary choice;
- future multiclass EEG.

---

## 40.2 Calibration method

Required but method unresolved.

---

## 40.3 Confidence thresholds

Required policy but numerical thresholds unresolved.

---

## 40.4 Adaptation mechanism

Required intended module but exact parameter/algorithm unresolved.

---

## 40.5 Risk model

Risk-aware planning approved; exact values and \(\lambda\) unresolved.

---

## 40.6 Cross-subject protocol

Required research direction; exact split unresolved.

---

## 40.7 Codex instruction filename

The workflow has changed from Claude/Claude Code to ChatGPT/Codex.

A stable repository instruction file should eventually be selected.

Possible naming must not be assumed in this architecture.

If the implementation environment standardizes on `AGENTS.md`, that may later be adopted through explicit documentation update.

---

# 41. ARCHITECTURE ACCEPTANCE CRITERIA

The architecture is correctly realized when:

1. EEG data loading is independent of modelling.
2. Preprocessing is independent of downstream autonomy.
3. CSP+LDA and EEGNet can be substituted through one decoder interface.
4. Calibration can be enabled/disabled.
5. Bayesian inference receives evidence through an explicit adapter.
6. EEG-to-goal mapping is modular.
7. Bayesian posterior is separate from classifier probabilities.
8. Uncertainty is computed and consumed by the control policy.
9. Shared autonomy can proceed, confirm, defer, pause, or stop.
10. Human stop/override is respected.
11. The planner receives an approved goal rather than inferring intent.
12. Safety can reject planner output.
13. Environment logic is independent of UI.
14. Experiment runner can execute without Streamlit.
15. Logging captures scientific state transitions.
16. Adaptation can be disabled for ablation.
17. Safety can be disabled only in controlled experimental variants.
18. Bayesian inference can be disabled for ablation.
19. Synthetic probabilities can test cognition before EEG integration.
20. Artificial goals can test autonomy before EEG integration.
21. Full EEG replay can later connect all layers.
22. Ground-truth experiment goals do not leak into inference.
23. Results are traceable to config/model/Git state.
24. All unresolved decisions remain explicit until approved.

---

# 42. ARCHITECTURE SUMMARY

The project uses a layered, modular architecture in which **prerecorded motor-imagery EEG is first validated and preprocessed, then decoded using both CSP+LDA and EEGNet/compact CNN models through a unified probability interface. Probabilities are calibrated where appropriate and converted through a separate goal-mapping policy into evidence for sequential Bayesian intent inference. The Bayesian layer maintains posterior belief, while an uncertainty module quantifies confidence. A shared-autonomy controller uses this belief and uncertainty to determine whether the system should proceed, request confirmation, defer, pause, or stop. Once a mission goal is approved, an A*-based autonomous planner generates a route through a simple 2D Gymnasium Search & Rescue environment. A separate safety controller authorizes or rejects proposed actions according to obstacles, hazard rules, and emergency state. Human confirmation, override, pause, and emergency stop remain authoritative. Corrections may feed a modular adaptation mechanism once that mechanism is explicitly approved. Offline EEG replay, experiment logging, model/system evaluation, and a Streamlit technical dashboard sit around the scientific core without redefining it.**

The architecture is deliberately designed so the EEG, cognition, and autonomy tracks can be built in parallel and then integrated.

---

# 43. NEXT DEPENDENCY

The next documentation file is:

**`05_TECHNOLOGY_STACK.md` — Technology Stack & Dependency Strategy**

That document should specify:

- approved language/tool choices;
- role of each library;
- dependency boundaries;
- environment/setup policy;
- what technologies are intentionally excluded;
- and which technologies remain optional future extensions.

It must not change the architecture defined here.
