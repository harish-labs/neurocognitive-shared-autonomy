# GITHUB_README.md

# NeuroCognitive Shared Autonomy for Search & Rescue

### EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control

A software-only research prototype that investigates whether uncertain EEG-based control can be made more reliable and safer through calibrated probability estimation, Bayesian goal inference, uncertainty-aware shared autonomy, autonomous planning, and explicit simulated safety control.

---

## Project Status

```text
Current phase:
Pre-implementation / documentation finalized

Verified implementation:
Not started yet

Validated empirical results:
None yet

Primary implementation agent:
Codex

Repository instruction file:
AGENTS.md
```

This README is intentionally written before final experiments exist.

No accuracy, safety, or performance claims are made without reproducible experiment evidence.

---

## Research Question

> **Can uncertainty-aware shared autonomy improve the reliability and safety of EEG-based intent control compared with direct brain-computer control?**

The project evaluates this through progressively richer system conditions:

```text
A — Direct EEG
B — Confidence-aware
C — Bayesian shared autonomy
D — Full system
```

The full system is not assumed to be superior in advance.

---

## Core Idea

A conventional direct-control BCI can behave like:

```text
EEG
→ classifier
→ action
```

This project instead evaluates:

```text
EEG
→ decoder probability
→ probability calibration
→ goal evidence
→ Bayesian belief
→ uncertainty
→ shared autonomy
→ approved human goal
→ A* planner
→ safety controller
→ 2D Search & Rescue environment
```

The system is built around one responsibility rule:

> **Human determines WHAT intended objective is selected. AI determines HOW to achieve it safely.**

---

## Why This Project Exists

Motor-imagery EEG is noisy, variable across users, and uncertain.

If every neural prediction is treated as an immediate command, a single incorrect prediction can propagate directly into an incorrect autonomous decision.

This project studies whether reliability can be improved by:

- preserving probability rather than only hard class labels;
- calibrating confidence;
- accumulating evidence over time;
- maintaining a Bayesian belief over goals;
- measuring uncertainty explicitly;
- asking for confirmation when needed;
- allowing human override, pause, and stop;
- separating planning from intent inference;
- enforcing explicit safety constraints before movement.

---

## Dataset

The project uses the public:

**PhysioNet EEG Motor Movement/Imagery Database (EEGMMIDB / EEGBCI)**

Current documented dataset properties:

```text
Subjects: 109
EEG channels: 64
Sampling frequency: 160 Hz
Runs per subject: 14
Format: EDF+
```

Initial motor-imagery runs:

```text
4
8
12
```

For these runs:

```text
T0 = rest
T1 = imagined left fist
T2 = imagined right fist
```

Initial classification task:

```text
Left-hand motor imagery
vs
Right-hand motor imagery
```

The project currently uses prerecorded EEG only.

Approved terminology:

```text
Offline EEG Replay
Simulated Real-Time BCI
```

---

## System Architecture

```text
┌──────────────────────────────────────────────┐
│ Public Prerecorded Motor-Imagery EEG        │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ MNE EEG Loader / Preprocessing / Epochs     │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ CSP + LDA  /  EEGNet or Compact EEG CNN    │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ Unified Decoder Probability Interface       │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ Probability Calibration                     │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ Goal-Evidence Adapter                       │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ Sequential Bayesian Goal Inference          │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ Posterior Entropy / Uncertainty             │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ Shared-Autonomy Controller                  │
│ PROCEED / CONFIRM / DEFER / PAUSE / STOP   │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ Human-Approved Goal                         │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ A* Planner                                  │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ Safety Controller                           │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│ 2D Search & Rescue Environment              │
└──────────────────────────────────────────────┘
```

---

## EEG Decoders

Two decoder families are required.

### CSP + LDA

Classical motor-imagery baseline:

```text
EEG epochs
→ Common Spatial Patterns
→ LDA
→ class probabilities
```

This provides:

- a strong classical reference;
- lower complexity;
- easier leakage inspection;
- direct comparison with established BCI methods.

### EEGNet / Compact EEG CNN

Neural decoder:

```text
EEG epochs
→ compact convolutional model
→ class probabilities
```

If the final architecture materially departs from the published EEGNet design, the repository should describe it as:

```text
compact EEG CNN inspired by EEGNet
```

rather than inaccurately calling it EEGNet.

---

## Probability Calibration

Classification accuracy and confidence reliability are evaluated separately.

Planned calibration metrics include:

```text
Expected Calibration Error
Brier Score
Reliability Diagram
```

Candidate calibration methods include:

```text
Temperature Scaling
Platt / Sigmoid Scaling
Isotonic Regression
```

The final calibration method is intentionally not hard-coded before validation.

---

## Bayesian Goal Inference

The goal-belief layer uses sequential Bayesian updating:

\[
P(G \mid E_{1:t})
\propto
P(E_t \mid G)
P(G \mid E_{1:t-1})
\]

The Bayesian core maintains:

- named goal hypotheses;
- explicit prior;
- likelihood;
- normalized posterior;
- belief history;
- reset behavior.

### Important Probability Boundary

The decoder may output:

\[
P(C \mid EEG)
\]

but the goal model requires:

\[
P(E \mid G)
\]

These are **not automatically equivalent**.

The repository therefore keeps an explicit Goal-Evidence Adapter between decoder probabilities and Bayesian goal inference.

---

## Binary EEG vs Multi-Goal Search & Rescue

The initial EEG decoder is binary:

```text
Left
Right
```

The Search & Rescue environment may contain more than two objectives.

Current candidate interaction strategies include:

```text
Two active options at a time
Hierarchical binary selection
Abstract binary priority selection
Future multiclass EEG
```

This decision must not be silently hard-coded.

---

## Uncertainty

Initial uncertainty measure:

\[
H(P)=-\sum_g P(g)\log P(g)
\]

where \(P(g)\) is the Bayesian posterior over candidate goals.

Interpretation:

```text
High entropy
→ ambiguous belief

Low entropy
→ concentrated belief
```

Low entropy does **not** guarantee correctness.

A confidently wrong posterior is explicitly treated as a failure case.

---

## Shared Autonomy

Conceptual controller modes:

```text
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

The controller uses:

- posterior belief;
- uncertainty;
- current candidate goal;
- human input;
- mission state;
- safety state.

The exact confidence thresholds remain configurable until scientifically approved.

---

## Human Authority

The user must retain:

```text
CONFIRM
OVERRIDE
PAUSE
STOP
```

Operational priority:

```text
Emergency Stop
→ Human Override / Pause
→ Safety Controller
→ Shared-Autonomy Policy
→ Planner / Execution
```

No model-confidence score can override a human stop or hard safety rule.

---

## Search & Rescue Environment

The core environment is intentionally simple.

```text
2D
Single agent
Grid-based
Static-first
```

Core entities may include:

- rescue agent;
- victim / target locations;
- safe zone;
- optional medical/resource location;
- obstacles;
- traversable risk areas;
- prohibited hazards.

Initial actions:

```text
UP
DOWN
LEFT
RIGHT
WAIT
```

No 3D environment is required for the core research question.

---

## Planning

Core planner:

```text
A*
```

For the four-connected grid:

```text
Manhattan distance
```

is the natural heuristic.

The planner receives an already approved goal.

It does not infer human intent.

---

## Risk-Aware Planning

Conceptual cost:

\[
J = distance + \lambda \cdot risk
\]

The final:

- risk scale;
- hazard semantics;
- \(\lambda\);

remain methodological decisions.

Hard safety constraints are kept separate from soft path cost.

---

## Safety Controller

Execution rule:

```text
Planner proposes
→ Safety checks
→ Environment executes only if approved
```

Core safety behaviors include:

- reject out-of-bounds movement;
- reject blocked cells;
- reject invalid actions;
- block movement while paused;
- block movement after emergency stop;
- reject prohibited hazards once the policy is approved;
- request replanning where appropriate.

These are simulated software safety constraints, not real-world certification.

---

## Adaptation

Adaptation may be included through a bounded and explicit mechanism.

Candidate adaptation targets:

```text
User-specific prior
Decoder reliability
Confidence threshold
Evidence weighting
```

Requirements:

- switchable on/off;
- subject-isolated;
- bounded;
- logged;
- resettable;
- leakage-safe.

The repository must not claim sophisticated adaptive control unless the implementation supports it.

---

## Experimental Conditions

Principal comparison:

```text
A — Direct EEG
B — Confidence-aware
C — Bayesian shared autonomy
D — Full system
```

The project also supports ablations such as:

```text
Full
Full - calibration
Full - Bayes
Full - uncertainty
Full - safety
Full - adaptation
```

---

## Evaluation

### EEG / ML

```text
Accuracy
Balanced Accuracy
Precision
Recall
F1
Confusion Matrix
```

### Calibration

```text
ECE
Brier Score
Reliability Diagram
```

### Bayesian Inference

```text
Goal inference accuracy
Posterior confidence
Entropy
Wrong-goal commitment
Decision latency
Evidence steps to commitment
```

### Shared Autonomy

```text
Proceed rate
Confirmation rate
Deferral rate
Override rate
Human interventions
Wrong autonomous commitments
```

### Planning

```text
Path length
Path cost
Risk exposure
Replanning
Planning success
```

### Safety

```text
Unsafe attempts
Executed violations
Safety overrides
Hazard entries
Emergency-stop success
```

### End-to-End

```text
Task success
Correct-goal completion
Wrong-goal commitment
Completion time
Human interventions
Risk exposure
Safety events
```

---

## Robustness and Failure Analysis

The project is designed to preserve failure cases.

Potential stress conditions include:

```text
Ambiguous EEG evidence
Incorrect decoder output
Miscalibrated confidence
Contradictory Bayesian evidence
Blocked route
Hazard exposure
No-path case
Human override
Emergency stop
```

The system should be evaluated on how errors propagate:

```text
EEG
→ decoder
→ calibration
→ Bayes
→ uncertainty
→ autonomy
→ planner
→ safety
→ mission outcome
```

---

## Scientific Integrity

The project explicitly permits negative results.

Valid outcomes include:

```text
CSP+LDA outperforms EEGNet
Calibration adds little
Bayesian inference increases latency
Adaptation helps only some subjects
Safety increases path length
Full system does not dominate every metric
```

The experiments must not be tuned to guarantee a desired conclusion.

---

## Project Limitations

Current boundaries include:

- prerecorded EEG only;
- binary motor imagery;
- no live BCI;
- no human-subject interaction study;
- no physical robot;
- simple 2D simulation;
- simulated safety only;
- no clinical claims;
- no unrestricted thought decoding.

---

## Responsible Terminology

Prefer:

```text
Motor-imagery EEG decoding
EEG-based control intent
Bayesian latent-goal belief
Posterior uncertainty
Shared autonomy
Simulated safety constraints
Offline EEG replay
```

Avoid unsupported wording such as:

```text
Mind reading
Reads thoughts
Proven safe
Clinical-grade
Real rescue robot
Live EEG BCI
```

---

## Tech Stack

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

Optional technologies such as ROS2, Gazebo, C++, PPO, SNNs, live EEG hardware, and physical robotics are not part of the core unless explicitly approved later.

---

## Planned Repository Structure

```text
neurocognitive-shared-autonomy/
│
├── README.md
├── MASTER_PROJECT_SPEC.md
├── AGENTS.md
├── PROJECT_STATE.md
├── CURRENT_TASK.md
├── DECISIONS.md
├── RESEARCH_LOG.md
├── EXPERIMENT_LOG.md
├── TODO.md
├── config.yaml
├── requirements.txt
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── config.py
│   ├── eeg/
│   │   ├── loader.py
│   │   ├── preprocessing.py
│   │   ├── epochs.py
│   │   ├── visualization.py
│   │   └── replay.py
│   ├── models/
│   │   ├── csp_lda.py
│   │   ├── eegnet.py
│   │   ├── calibration.py
│   │   └── inference.py
│   ├── cognition/
│   │   ├── bayesian_intent.py
│   │   ├── uncertainty.py
│   │   ├── adaptation.py
│   │   └── goal_mapping.py
│   ├── autonomy/
│   │   ├── environment.py
│   │   ├── planner.py
│   │   ├── safety.py
│   │   └── shared_controller.py
│   ├── evaluation/
│   │   ├── eeg_metrics.py
│   │   ├── autonomy_metrics.py
│   │   ├── experiments.py
│   │   └── logger.py
│   ├── app/
│   │   ├── dashboard.py
│   │   └── human_interface.py
│   ├── schemas/
│   └── utils/
│
├── experiments/
├── models/
├── results/
│   ├── figures/
│   ├── tables/
│   └── logs/
├── notebooks/
├── tests/
├── docs/
└── demo/
```

---

## AI-Assisted Development Workflow

The project uses:

```text
ChatGPT
→ Project Brain / Research Director

Project Owner
→ Final authority

Codex
→ Implementation engineer

Git / GitHub
→ Persistent technical source of truth
```

Codex repository instructions:

```text
AGENTS.md
```

Development loop:

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

## First Implementation Task

The first coding task is intentionally narrow:

> **Read `MASTER_PROJECT_SPEC.md` first. We are starting Milestone 1 only. Implement a clean MNE-Python data loader for the PhysioNet EEGBCI motor-imagery dataset. Initially support configurable subject IDs and runs 4, 8 and 12. Requirements: download through MNE utilities; cache locally; load EDF files; standardize channel names; attach the appropriate montage; print subject, channel count, sampling frequency, duration and annotations; add basic validation/error handling; write unit tests where practical; do not implement preprocessing or modelling yet. After coding, tell me: (1) files created/modified, (2) installation requirements, (3) exact command to run, (4) expected output, (5) what I should manually check. Do not continue beyond the loader.**

---

## Setup

The final installation commands will be frozen after the implementation environment and package versions are validated.

Expected core dependencies include:

```text
mne
numpy
pandas
scikit-learn
torch
gymnasium
matplotlib
streamlit
pyyaml
```

Exact versions should be recorded in `requirements.txt`.

---

## Running the Project

The authoritative run commands will be added only after the corresponding modules exist.

Planned categories:

```text
Dataset validation
EEG baseline training
EEGNet training
Calibration evaluation
Bayesian simulation
SAR simulation
End-to-end replay
Experiment runner
Streamlit dashboard
```

Do not document commands that have not actually been tested.

---

## Results

At the time this README is generated:

```text
Validated EEG results:
None yet

Validated calibration results:
None yet

Validated Bayesian results:
None yet

Validated shared-autonomy results:
None yet

Validated end-to-end results:
None yet
```

Future headline metrics must link to reproducible experiments.

---

## Reproducibility

Every reportable experiment should preserve:

```text
Experiment ID
Git commit
Configuration snapshot
Subjects / runs
Split manifest
Random seed
Model / checkpoint
Calibration state
Map / policy
Raw outputs
Metrics
Validity status
```

No screenshots-only evidence.

---

## Documentation

The repository is supported by a detailed specification set covering:

- project concept;
- research questions;
- SAR scenario;
- architecture;
- technology stack;
- EEG dataset/pipeline;
- neuroscience;
- EEG signal processing;
- calibration/uncertainty;
- Bayesian inference;
- cognition/adaptation;
- shared autonomy;
- planning;
- safety;
- implementation;
- repository architecture;
- experimental design;
- metrics;
- testing;
- ethics/validity;
- literature;
- AI-assisted development;
- results analysis;
- discussion;
- future work;
- final technical reporting.

`MASTER_PROJECT_SPEC.md` remains the highest project authority.

---

## Future Work

Potential extensions include:

```text
Stronger cross-subject generalization
Few-shot personalization
Advanced calibration
Advanced uncertainty
Hierarchical multi-goal BCI
Dynamic Bayesian models
Live EEG
Human-subject evaluation
Dynamic SAR
ROS2 / Gazebo
Formal safety
Physical robotics
Neuromorphic / SNN comparison
```

These are future possibilities, not current requirements.

---

## Current Research Contribution

The intended contribution is not a new individual algorithm.

It is the integrated, reproducible evaluation of:

```text
Motor-imagery EEG
+
Calibration
+
Bayesian latent-goal inference
+
Uncertainty-aware shared autonomy
+
Autonomous planning
+
Explicit simulated safety
```

within one coherent Search & Rescue research framework.

---

## Disclaimer

This project is a research prototype.

It is not:

- a medical device;
- a clinical EEG system;
- a thought-reading system;
- a certified safety system;
- a real-world rescue platform;
- a live BCI at the current stage.

All final claims must remain bounded to the actual experiments performed.
