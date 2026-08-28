# 05_TECHNOLOGY_STACK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Technology Stack & Dependency Strategy

**Document ID:** C-02  
**Document class:** System Design / Technology Specification  
**Authority level:** Subordinate to `MASTER_PROJECT_SPEC.md`, `01_PROJECT_CONCEPT_AND_PROBLEM.md`, `02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md`, `03_SEARCH_AND_RESCUE_SCENARIO.md`, and `04_SYSTEM_ARCHITECTURE.md`  
**Status:** Authoritative technology baseline; exact package versions remain to be frozen after environment validation  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY RULE

This document specifies **which technologies are part of the approved project, why they are used, what each is responsible for, and what technologies must not be introduced without a justified and approved reason**.

It does not modify the project's scientific architecture.

If this document conflicts with a higher-authority project document, the higher-authority document wins.

The guiding principle is:

> **Use the smallest technology stack that correctly supports the research architecture.**

The project must demonstrate:

- scientific depth;
- mathematical reasoning;
- reproducibility;
- modular software engineering;
- valid experimentation;
- and clear technical evidence.

It must **not** demonstrate technology count for its own sake.

---

# 1. APPROVED CORE TECHNOLOGY STACK

The current approved core stack is:

```text
Programming Language
    Python

EEG / Neuroscience
    MNE-Python

Machine Learning / Deep Learning
    scikit-learn
    PyTorch

Scientific Computing
    NumPy
    Pandas

Simulation
    Gymnasium

Autonomous Planning
    Custom A* implementation in Python

Visualization / Analysis
    Matplotlib

Technical Interface
    Streamlit

Configuration
    YAML configuration file(s)

Version Control / Source of Truth
    Git
    GitHub
```

The final system should be possible to implement entirely with this core stack.

---

# 2. TECHNOLOGY SELECTION PHILOSOPHY

Every technology must satisfy at least one of these conditions:

1. it is required for the approved scientific methodology;
2. it directly supports reproducible implementation;
3. it directly supports experimentation or validation;
4. it is required for technical inspection/demonstration;
5. it solves a real implementation problem that cannot be solved cleanly by the existing stack.

A technology must **not** be added because:

- it is currently popular;
- it looks impressive on a resume;
- it makes the architecture appear more complex;
- another project used it;
- an AI coding agent recommends it without scientific need;
- or it can replace a simple local component with a larger infrastructure system.

---

# 3. PRIMARY PROGRAMMING LANGUAGE — PYTHON

## Role

Python is the primary language for the entire core system.

It will be used for:

- EEG data loading;
- EEG preprocessing;
- model development;
- classical machine learning;
- deep learning;
- probability calibration;
- Bayesian inference;
- uncertainty estimation;
- adaptation;
- simulation;
- A* path planning;
- safety logic;
- shared-autonomy logic;
- evaluation;
- logging;
- plotting;
- technical dashboard;
- experiment automation;
- testing.

## Why Python is appropriate

The project's major scientific libraries are Python-native or have mature Python APIs:

- MNE-Python;
- PyTorch;
- scikit-learn;
- NumPy;
- Pandas;
- Gymnasium;
- Streamlit;
- Matplotlib.

Using one primary language reduces integration complexity and makes controlled experiments easier.

## Boundary

Python is sufficient for the **core project**.

C++ is not required unless later approved as an extension.

---

# 4. MNE-PYTHON

## Role

MNE-Python is the approved EEG/neuroscience framework.

It is responsible for:

- accessing the PhysioNet EEG Motor Movement/Imagery dataset through MNE utilities;
- loading EDF files;
- EEG channel handling;
- montage handling;
- annotations/events;
- filtering;
- epoch creation;
- EEG inspection;
- power spectral analysis where needed;
- compatibility with CSP-based workflows.

## Planned project modules

```text
src/eeg/loader.py
src/eeg/preprocessing.py
src/eeg/epochs.py
src/eeg/visualization.py
src/eeg/replay.py
```

## Dataset direction

Initial approved dataset direction:

> **PhysioNet EEG Motor Movement/Imagery / EEGBCI**

Initial motor-imagery runs:

```text
4
8
12
```

Initial classification task:

```text
Left-hand motor imagery
vs
Right-hand motor imagery
```

## Scientific requirement

MNE-Python is not only a convenience library.

Dataset annotations, event mapping, channels, sampling frequency, montage, and epoch construction must be inspected and validated.

---

# 5. SCIKIT-LEARN

## Role

scikit-learn supports the classical machine-learning and evaluation components.

Primary approved uses include:

- Linear Discriminant Analysis;
- classical pipeline utilities where appropriate;
- probability calibration where the chosen method is supported;
- train/validation utilities where scientifically appropriate;
- evaluation metrics;
- confusion matrices;
- statistical preprocessing utilities where justified.

## Core model role

The mandatory classical EEG baseline is:

```text
CSP
→ LDA
```

CSP may use MNE's implementation while LDA is provided by scikit-learn.

## Boundary

scikit-learn must not be used in a way that hides leakage.

For example:

- CSP fitting;
- scaling;
- calibration;
- model selection;

must respect training/validation/test boundaries.

---

# 6. PYTORCH

## Role

PyTorch is the approved deep-learning framework.

Primary use:

> **EEGNet / compact CNN EEG decoder**

PyTorch will support:

- model definition;
- training;
- validation;
- inference;
- checkpoint saving/loading;
- loss computation;
- batching;
- probability output generation.

## Architectural requirement

PyTorch belongs in the **EEG decoding layer**.

It must not absorb:

- Bayesian goal inference;
- safety;
- A* planning;
- shared-autonomy logic;
- or environment behaviour.

## Model complexity rule

The project should prefer an EEG-appropriate compact network.

Do not increase model depth/parameter count merely because compute is available.

---

# 7. NUMPY

## Role

NumPy is the primary numerical-array layer for non-neural components.

Expected uses include:

- numerical transformations;
- probability vectors;
- Bayesian calculations;
- entropy calculation;
- simulation arrays;
- risk maps;
- metrics preparation;
- controlled random generation where appropriate.

## Mathematical role

Typical operations include:

\[
P(G \mid E)
\]

normalization, entropy calculation:

\[
H(P)=-\sum_i p_i\log p_i
\]

and numerical checks.

## Requirement

Probability calculations must include validation for:

- non-finite values;
- invalid negative probabilities;
- invalid normalization;
- zero-division/normalization failure.

---

# 8. PANDAS

## Role

Pandas is primarily for structured data and experiment analysis.

Expected uses:

- experiment logs;
- result tables;
- subject-level summaries;
- configuration/result analysis;
- CSV input/output;
- metric aggregation.

## Boundary

Pandas should not become part of the real-time inference/control path unless there is a clear reason.

NumPy/tensors should handle numerical runtime data where simpler.

---

# 9. GYMNASIUM

## Role

Gymnasium is the approved framework for the simple 2D Search & Rescue environment.

The custom environment should support:

```text
reset()
step(action)
observation
terminated
truncated
info
```

as appropriate to Gymnasium conventions.

## Initial action space

```text
UP
DOWN
LEFT
RIGHT
WAIT
```

## Environment responsibilities

- agent state;
- map state;
- goal positions;
- blocked cells;
- hazard/risk representation;
- terminal states;
- seeded reset;
- deterministic testing where possible.

## Important boundary

The environment must not contain hidden:

- EEG decoding;
- Bayesian inference;
- shared-autonomy reasoning.

It represents the world, not the cognition system.

---

# 10. A* PATH PLANNING

## Technology choice

A* is the approved initial autonomous planner.

It should be implemented as a clear Python module:

```text
src/autonomy/planner.py
```

rather than requiring a separate robotics framework.

## Role

A* receives:

- current agent state;
- approved goal;
- obstacle map;
- risk information.

It returns:

- path;
- next action;
- cost;
- planning status.

## Risk-aware extension

Approved conceptual path cost:

\[
J = \text{distance} + \lambda \cdot \text{risk}
\]

Exact:

- hazard scale;
- risk formulation;
- \(\lambda\);

remain unresolved.

## Why A*

A* is sufficient for the core research question because the research contribution is not a novel path planner.

The planner exists so the project can study:

- goal-level BCI;
- shared autonomy;
- uncertainty;
- safety;
- and human–AI responsibility division.

---

# 11. MATPLOTLIB

## Role

Matplotlib is the approved scientific plotting library.

Expected plots include:

- EEG traces;
- PSD;
- epoch examples;
- training curves;
- confusion matrix;
- calibration/reliability plots;
- posterior evolution;
- uncertainty curves;
- model comparisons;
- robustness curves;
- ablation plots;
- task-performance plots.

## Visualization rule

Scientific plots should be generated from actual experiment outputs.

No chart may contain invented results.

---

# 12. STREAMLIT

## Role

Streamlit is the approved technical dashboard framework.

The dashboard may expose:

- EEG replay state;
- selected subject/trial;
- raw/calibrated probabilities;
- Bayesian posterior;
- entropy;
- current confidence/autonomy state;
- inferred/approved target;
- 2D map;
- path;
- hazard regions;
- safety events;
- confirmation;
- override;
- pause;
- emergency stop;
- current episode metrics.

## Boundary

Streamlit is a **presentation and interaction layer**.

It must not contain scientific logic that is unavailable to:

- tests;
- automated experiment scripts;
- or headless execution.

The UI is not the project.

---

# 13. YAML CONFIGURATION

The planned repository already contains:

```text
config.yaml
```

The configuration layer should hold values such as:

- subjects;
- runs;
- preprocessing settings;
- model settings;
- seeds;
- environment settings;
- planner parameters;
- uncertainty settings;
- safety settings;
- experiment mode.

## Important rule

An experimental parameter changed through configuration must be recorded with the corresponding experiment.

## Exact parser

The exact YAML parsing package is an implementation detail and is **not locked in this document**.

If an additional package is required for YAML parsing, it should be minimal and recorded in dependencies.

---

# 14. GIT

## Role

Git is the technical history and version-control layer.

It records:

- source code;
- project documents;
- configuration changes;
- experiment scripts;
- implementation milestones;
- fixes;
- approved architecture changes.

## Working principle

One module:

```text
implement
→ run
→ verify
→ commit
→ continue
```

is preferred over giant unreviewed changes.

## Recommended feature branch pattern

Previously approved examples include:

```text
feature/eeg-loader
feature/eeg-preprocessing
feature/csp-lda
feature/eegnet
feature/bayesian-intent
feature/simulation
feature/shared-autonomy
feature/dashboard
```

Exact branch names are conventions rather than scientific requirements.

---

# 15. GITHUB

## Role

GitHub is the persistent repository and public/private project evidence layer.

It should ultimately contain:

- code;
- documentation;
- tests;
- architecture;
- experiment configuration;
- reproducible results;
- README;
- limitations;
- demo artifacts where appropriate.

## Important boundary

GitHub does not replace local experiment validation.

A green repository or attractive README is not evidence that the science is correct.

---

# 16. TESTING FRAMEWORK

Testing is mandatory.

However, the exact Python testing framework has **not yet been explicitly locked** in the transferred project decisions.

The implementation should use an appropriate standard Python testing approach and record the choice when the repository is initialized.

This document does not silently select a framework.

Required testing categories remain:

- unit;
- integration;
- scientific/mathematical validation;
- smoke tests;
- reproducibility checks.

---

# 17. NOTEBOOKS

The approved repository structure includes:

```text
notebooks/
    01_eeg_exploration.ipynb
    02_results_analysis.ipynb
```

## Role

Notebooks are acceptable for:

- EEG exploration;
- visualization;
- preliminary investigation;
- result analysis.

## Boundary

Core scientific logic should not exist only in notebooks.

Reusable logic belongs in `src/`.

Experiments that generate reportable results should be reproducible through scripts/configuration rather than only through manually executed notebook cells.

---

# 18. STORAGE FORMATS

The project should prefer transparent local file formats.

## Data

Raw dataset files:

- format supplied by source dataset / MNE workflow.

Processed data:

- format selected by implementation based on need;
- must preserve metadata and be documented.

No processed-data format is currently locked.

## Experiment results

Prefer machine-readable:

```text
CSV
JSON
JSONL
```

as appropriate.

## Model checkpoints

Use the standard serialization appropriate to the model/framework.

## Documentation

Markdown is the primary repository documentation format.

---

# 19. COMPUTE STRATEGY

The project is software-first and should not depend on specialized infrastructure.

## CPU

Sufficient for:

- data loading;
- preprocessing;
- CSP+LDA;
- Bayesian inference;
- A*;
- Gymnasium;
- safety logic;
- most evaluation;
- dashboard.

## GPU

May accelerate EEGNet training.

GPU availability is an implementation convenience, not an architectural requirement.

The project must not be redesigned around expensive compute.

## Cloud

Not required.

---

# 20. DEPENDENCY MANAGEMENT STRATEGY

The repository should maintain a reproducible dependency definition.

The architecture currently expects:

```text
requirements.txt
```

A more structured environment file may be introduced later if justified, but it must not create unnecessary complexity.

## Version policy

Exact package versions are **not yet locked**.

Correct process:

1. establish the first working environment;
2. verify compatibility among MNE, PyTorch, scikit-learn, Gymnasium, Streamlit, NumPy, and Pandas;
3. record versions;
4. pin or constrain versions sufficiently for reproducibility;
5. update only deliberately.

Do not invent version numbers in documentation before the environment is tested.

---

# 21. ENVIRONMENT REPRODUCIBILITY

When the implementation environment is validated, record at minimum:

```text
Python version
MNE version
PyTorch version
scikit-learn version
NumPy version
Pandas version
Gymnasium version
Streamlit version
Matplotlib version
operating system
CPU/GPU information where relevant
```

If CUDA is used, record the relevant runtime information.

This metadata belongs with experimental results when it can affect reproducibility.

---

# 22. OPTIONAL TECHNOLOGIES — NOT CORE

The following have previously been identified as possible **future extensions only**.

They are not required for the core project.

---

## 22.1 C++

Potential use:

- later robotics-critical component;
- stronger systems/robotics evidence.

Current status:

> **Optional.**

The project should not introduce C++ into ordinary EEG/Bayesian code merely to claim C++ usage.

---

## 22.2 ROS 2

Potential use:

- later transfer of the final control system into a robotics-oriented simulator.

Current status:

> **Optional future extension.**

Not part of the core implementation.

---

## 22.3 Gazebo

Potential use:

- later robotic transfer-validation visualization/simulation.

Current status:

> **Optional future extension.**

The core project deliberately uses a lightweight 2D simulator.

---

## 22.4 Reinforcement Learning / PPO

Potential use:

- comparison with a learned autonomous policy;
- later research extension.

Current status:

> **Optional.**

A* remains the core planner.

Do not replace A* with PPO simply because reinforcement learning appears more advanced.

---

## 22.5 Spiking Neural Networks

Potential use:

- brain-inspired/neuromorphic extension.

Current status:

> **Optional future work.**

Do not add before the EEG/shared-autonomy core is complete.

---

## 22.6 Multiclass EEG

Potential use:

- expanded goal-selection mechanism.

Current status:

> **Optional / unresolved future extension.**

It must not be used to silently avoid resolving the current binary Left-vs-Right design.

---

## 22.7 Advanced uncertainty techniques

Potential use:

- later comparison beyond entropy/basic calibrated probabilities.

Current status:

> **Optional.**

The initial architecture requires scientifically valid uncertainty, not maximum methodological complexity.

---

# 23. TECHNOLOGIES EXPLICITLY NOT REQUIRED FOR THE CORE

The following should not be added merely for complexity:

```text
LLMs
RAG
Gemini / OpenAI API
blockchain
AWS / cloud architecture
Kubernetes
IoT systems
physical EEG headset
physical robot
complex microservices
unnecessary computer vision
mobile application
elaborate 3D visualization
```

This restriction is important.

The user's existing broader portfolio already includes technologies such as cloud, RAG, LLM orchestration, computer vision, and production software.

This project is intended to demonstrate **different technical depth**.

---

# 24. LLM / GENERATIVE AI POLICY INSIDE THE PROJECT

LLMs may be used as **development assistance** through ChatGPT/Codex.

They are not part of the runtime scientific architecture.

Therefore:

```text
ChatGPT/Codex
= development/research tooling
```

but:

```text
LLM API
≠ project inference module
```

The runtime rescue agent does not need an LLM to:

- decode EEG;
- infer Bayesian intention;
- calculate entropy;
- plan;
- avoid hazards;
- or enforce safety.

---

# 25. CHATGPT + CODEX DEVELOPMENT TOOLING

The official AI-assisted workflow is:

## ChatGPT

Role:

- research director;
- architecture reasoning;
- neuroscience review;
- mathematical review;
- methodology design;
- experiment design;
- documentation;
- independent review;
- next-task generation.

## Project owner

Role:

- final authority;
- approval;
- integration oversight;
- manual validation;
- decision control.

## Codex

Role:

- inspect repository;
- implement requested module;
- write/modify tests;
- run code;
- debug;
- execute experiments when instructed;
- update project state honestly;
- create commits.

## Git/GitHub

Role:

- persistent source of truth;
- historical record;
- actual implementation state.

No AI agent is allowed to fabricate an implementation state or result.

---

# 26. TECHNOLOGY BOUNDARIES BY MODULE

| Module | Primary technology |
|---|---|
| EEG dataset access | MNE-Python |
| EEG preprocessing | MNE-Python, NumPy |
| EEG visualization | MNE-Python, Matplotlib |
| CSP | MNE-Python |
| LDA | scikit-learn |
| EEGNet | PyTorch |
| Decoder interface | Python |
| Calibration | scikit-learn / approved Python implementation |
| Bayesian inference | Python, NumPy |
| Entropy/uncertainty | Python, NumPy |
| Adaptation | Python, exact method unresolved |
| Environment | Gymnasium, Python |
| A* | Python |
| Safety | Python |
| Shared autonomy | Python |
| Experiment logging | Python, Pandas / structured files |
| EEG metrics | scikit-learn + Python |
| System metrics | Python, Pandas |
| Plotting | Matplotlib |
| Dashboard | Streamlit |
| Version control | Git/GitHub |

This table defines responsibility, not package exclusivity.

---

# 27. TECHNOLOGIES MUST NOT CROSS SCIENTIFIC BOUNDARIES INCORRECTLY

Examples of incorrect design:

## PyTorch controls the whole system

Wrong:

```text
EEGNet neural network
→ outputs movement directly
→ bypasses Bayes/safety
```

Correct:

```text
EEGNet
→ probability evidence
→ Bayes
→ uncertainty
→ shared autonomy
→ planner
→ safety
```

---

## Streamlit becomes the controller

Wrong:

```text
button callback
contains all Bayesian and safety logic
```

Correct:

```text
dashboard
→ calls reusable core modules
```

---

## Gymnasium reward defines safety

Wrong:

```text
hazard = -10 reward
therefore "safe"
```

Correct:

```text
planner may use risk cost
+
safety controller enforces hard constraints
```

---

# 28. DEPENDENCY ADDITION RULE

If Codex requires a package that is not listed here:

1. explain what functionality requires it;
2. determine whether the existing stack already provides the capability;
3. classify it as:
   - implementation utility,
   - core scientific dependency,
   - optional extension;
4. record the decision if meaningful;
5. update dependency files;
6. do not silently introduce large frameworks.

A small utility dependency does not automatically require a project-scope decision.

A technology that changes architecture or methodology does.

---

# 29. PACKAGE VERSION CHANGE RULE

Do not update dependencies casually after experiments begin.

A major dependency update may change:

- preprocessing;
- numerical behaviour;
- model training;
- random behaviour;
- API semantics.

If versions change during the experimental stage:

- record the old version;
- record the new version;
- record why;
- rerun affected validation when necessary.

---

# 30. SECURITY AND DATA PRIVACY TECHNOLOGY REQUIREMENT

The initial project uses public prerecorded EEG.

Therefore the core stack does not require:

- authentication;
- user management;
- encrypted cloud database;
- healthcare backend;
- patient telemetry infrastructure.

If human participants or private EEG are later introduced, security/privacy requirements must be reassessed.

Do not import Healthsoft-style healthcare infrastructure into this project simply because that technology exists elsewhere in the user's portfolio.

---

# 31. PERFORMANCE AND COMPLEXITY RULE

Prefer:

```text
simple
validated
modular
reproducible
```

over:

```text
complex
novel-looking
difficult to verify
```

Examples:

- A* before RL.
- CSP+LDA before exotic EEG models.
- EEGNet before a large custom neural architecture.
- sequential Bayesian filtering before a complex probabilistic programming framework.
- 2D Gymnasium before Gazebo.
- local experiment logging before cloud pipelines.

---

# 32. SCIENTIFIC STACK PRIORITY

The stack should be thought of in this order:

```text
1. MNE-Python
   Real EEG + correct neuroscience handling

2. scikit-learn
   Classical baseline + evaluation + calibration

3. PyTorch
   Neural decoder

4. NumPy
   Bayesian mathematics + uncertainty

5. Gymnasium + Python A*
   Autonomous experimental environment

6. Python safety/shared-autonomy logic
   Research-control layer

7. Pandas + Matplotlib
   Experimental evidence

8. Streamlit
   Human-readable technical demonstration

9. Git/GitHub
   Reproducibility and proof
```

This ordering reflects scientific importance, not development difficulty.

---

# 33. INITIAL INSTALLATION GROUPS

Exact versions remain unresolved, but dependencies should be grouped conceptually.

## Scientific / EEG

```text
mne
numpy
scipy if required by the chosen MNE/scientific stack
```

**Note:** SciPy is a likely transitive/scientific dependency, but it is not separately locked as a project-level technology requirement here.

---

## Classical ML

```text
scikit-learn
```

---

## Deep Learning

```text
torch
```

---

## Data / Analysis

```text
pandas
matplotlib
```

---

## Simulation

```text
gymnasium
```

---

## UI

```text
streamlit
```

---

## Configuration / Testing / Development Utilities

Exact packages are to be selected during repository initialization and documented.

Do not assume a package merely because it is common.

---

# 34. HARDWARE REQUIREMENTS

The core system requires only a normal development computer capable of:

- running Python;
- processing the selected EEG data;
- training a compact EEG model;
- running the 2D simulator;
- running Streamlit.

A GPU is helpful but not mandatory.

The project must not claim that specialized EEG equipment or robotics hardware is required.

---

# 35. PLATFORM / OPERATING SYSTEM

No operating system has been scientifically locked.

The implementation should use the user's working development environment and document it for reproducibility.

Do not redesign the project around:

- Linux robotics tooling;
- WSL;
- containers;
- or cloud VMs;

unless an actual implementation requirement appears.

If ROS 2/Gazebo is later approved, platform considerations may change for that optional extension.

---

# 36. FILE AND DIRECTORY OWNERSHIP

Technology responsibility should map clearly to repository areas.

```text
data/
    dataset artifacts

src/eeg/
    MNE / EEG logic

src/models/
    scikit-learn / PyTorch decoder logic

src/cognition/
    NumPy/Python Bayesian + uncertainty + adaptation logic

src/autonomy/
    Gymnasium / A* / safety / shared autonomy

src/evaluation/
    metrics / experiments / logs

src/app/
    Streamlit / human interaction

results/
    machine-generated experimental evidence

tests/
    validation of all layers

docs/
    scientific / technical documentation
```

No directory should become an unstructured catch-all.

---

# 37. TECHNOLOGY CHOICE ACCEPTANCE CRITERIA

The technology stack is correctly implemented when:

1. Python remains the core implementation language.
2. MNE-Python handles EEG dataset/scientific EEG operations.
3. CSP+LDA exists as a classical baseline.
4. PyTorch implements the neural decoder.
5. NumPy/Python implements Bayesian and uncertainty mathematics transparently.
6. Gymnasium provides the simple 2D environment.
7. A* remains the initial planner.
8. safety and shared-autonomy logic remain explicit Python modules.
9. Matplotlib generates scientific figures from actual results.
10. Streamlit remains an inspection/demo layer rather than the scientific core.
11. Git/GitHub preserve project history and implementation evidence.
12. dependencies are recorded reproducibly.
13. exact versions are frozen only after validation.
14. unnecessary cloud/LLM/3D/hardware systems are not added.
15. optional extensions remain optional until explicitly approved.
16. development assistance from ChatGPT/Codex is not confused with runtime AI architecture.
17. no dependency silently changes the project's research methodology.

---

# 38. CURRENT TECHNOLOGY DECISIONS SUMMARY

## Locked core

```text
Python
MNE-Python
scikit-learn
PyTorch
NumPy
Pandas
Gymnasium
A*
Matplotlib
Streamlit
Git
GitHub
YAML-based configuration
```

## Required methodology but exact technique unresolved

```text
probability calibration method
adaptation method
confidence thresholds
risk formulation
cross-subject protocol
EEG-to-goal mapping
```

## Optional future technologies

```text
C++
ROS 2
Gazebo
PPO / reinforcement learning
Spiking Neural Networks
multiclass EEG
advanced uncertainty techniques
live EEG hardware
physical robotics
```

## Explicitly unnecessary for the current core

```text
LLM runtime
RAG
Gemini/OpenAI API runtime
blockchain
AWS/cloud architecture
Kubernetes
IoT
complex microservices
unnecessary computer vision
mobile application
elaborate 3D visualization
```

---

# 39. FINAL STACK STATEMENT

The project deliberately uses a compact scientific stack. **MNE-Python handles real motor-imagery EEG; CSP+LDA and PyTorch/EEGNet provide classical and neural decoding; calibration converts raw classifier probabilities into usable evidence; NumPy/Python implements sequential Bayesian goal inference and entropy-based uncertainty; Gymnasium provides a controlled 2D Search & Rescue environment; A* provides autonomous path planning; explicit Python safety and shared-autonomy modules regulate execution; Pandas and Matplotlib produce reproducible experimental evidence; Streamlit exposes a simple technical interface; and Git/GitHub preserve the actual implementation history.**

The project does not require 3D modelling, physical hardware, cloud infrastructure, LLMs, RAG, IoT, or complex distributed systems.

The objective is not to maximize the number of technologies.

The objective is to make every approved scientific component **correct, testable, interpretable, and reproducible**.

---

# 40. NEXT DOCUMENT

The next planned document is:

**`06_DATASET_AND_DATA_PIPELINE.md` — EEG Dataset Specification & Data Pipeline**

It should define in detail:

- PhysioNet EEGBCI;
- subject/run strategy;
- motor-imagery labels;
- data acquisition through MNE;
- caching;
- channel handling;
- montage;
- events;
- epoch construction;
- preprocessing boundaries;
- dataset metadata;
- split strategy boundaries;
- leakage prevention;
- data quality validation;
- processed-data representation;
- and dataset limitations.

It must preserve the currently unresolved final cross-subject evaluation protocol rather than silently choosing one.
