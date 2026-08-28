# 02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Objectives, Scope, Research Questions, Hypotheses, Success Criteria, and Project Boundaries

**Document ID:** A-03  
**Document class:** Master Authority Supporting Document  
**Authority level:** Subordinate only to `MASTER_PROJECT_SPEC.md`  
**Status:** Authoritative baseline with explicitly unresolved items preserved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND NON-INTERPRETATION RULE

This document defines **what the project is trying to achieve, what questions it will investigate, what is inside and outside scope, and what counts as successful completion**.

It must be read together with:

1. `MASTER_PROJECT_SPEC.md` — highest authority;
2. `01_PROJECT_CONCEPT_AND_PROBLEM.md` — authoritative concept, motivation, and problem definition.

If this document conflicts with `MASTER_PROJECT_SPEC.md`, the Master Project Specification wins unless the project owner explicitly approves a change and the change is recorded through the project change-control process.

The following rules are binding:

- Do not silently change the project objective.
- Do not convert an unresolved item into an assumed design choice.
- Do not add technologies or features only to make the project appear larger.
- Do not remove an approved scientific component because implementation is difficult.
- Do not fabricate hypotheses, results, metrics, or claims after seeing outcomes.
- Negative or mixed experimental findings are valid.
- Search & Rescue is the application scenario, not the sole technical contribution.
- The project is about **safe shared autonomy under uncertain EEG-based human intent**, not only EEG classification and not only path planning.
- The project owner remains the final authority for scope or scientific changes.
- ChatGPT serves as the project brain/research director and reviewer.
- Codex serves as the implementation engineer.
- Git/GitHub records what was actually implemented.
- Codex may not independently redefine the research questions, architecture, scientific assumptions, or scope.

---

# 1. PURPOSE OF THIS DOCUMENT

This document answers four questions:

> **What exactly are we trying to achieve?**

> **What research questions are we testing?**

> **What is and is not part of the project?**

> **What conditions must be satisfied before the project can be considered complete and scientifically defensible?**

It does **not** define the detailed Search & Rescue map, exact software interfaces, final hyperparameters, or exact experimental split. Those belong in later dedicated documents.

---

# 2. PRIMARY PROJECT OBJECTIVE

The primary objective is:

> **To design, implement, and experimentally evaluate a software-first shared-autonomy framework that converts uncertain motor-imagery EEG evidence into safer and more reliable goal-level autonomous assistance by combining EEG decoding, probability calibration, sequential Bayesian goal inference, explicit uncertainty estimation, human-in-the-loop shared autonomy, safety constraints, adaptive behaviour where justified, and autonomous navigation in a simple 2D Search & Rescue simulation.**

The project must evaluate whether this architecture provides meaningful advantages over simpler direct EEG-control approaches.

The project is not considered successful merely because an EEG model classifies Left/Right correctly or because an autonomous agent reaches a target. The scientific value comes from the **complete interaction between uncertain neural intent, probabilistic reasoning, autonomy, safety, human control, and measurable evaluation**.

---

# 3. CENTRAL RESEARCH QUESTION

The current locked primary research question is:

> **RQ-0 — Can uncertainty-aware shared autonomy improve the reliability and safety of EEG-based intent control compared with direct brain-computer control?**

This is the umbrella research question for the entire project.

The experiment design must allow this question to be answered quantitatively rather than only through a demonstration video or qualitative explanation.

---

# 4. PRIMARY RESEARCH HYPOTHESIS

The primary hypothesis is:

> **H-0 — A system that combines calibrated EEG evidence, sequential Bayesian intent inference, explicit uncertainty handling, shared autonomy, and safety constraints will reduce inappropriate or unsafe autonomous commitments relative to direct EEG-based control, while retaining useful task performance.**

This is a **testable hypothesis**, not a guaranteed claim.

A valid outcome could be:

- improved safety but slower completion;
- improved goal reliability but more human confirmations;
- improved robustness under some conditions but not across subjects;
- little or no benefit from one component;
- or another mixed result supported by the experiments.

The system must not be engineered or evaluated in a way that guarantees the full method appears superior.

---

# 5. SECONDARY OBJECTIVES

The project has the following secondary objectives.

## Objective 1 — Establish a scientifically valid EEG processing pipeline

Use real public motor-imagery EEG data and construct a reproducible pipeline that:

- downloads/loads the dataset,
- validates data integrity,
- standardizes channels/montage as required,
- filters/preprocesses EEG,
- extracts events and epochs,
- creates labels,
- preserves subject identity,
- and prevents data leakage.

The initial approved direction is the PhysioNet EEG Motor Movement/Imagery dataset accessed through MNE-Python, initially using Left-vs-Right motor-imagery runs 4, 8, and 12.

---

## Objective 2 — Establish a classical EEG baseline

Implement and evaluate a **CSP + LDA** baseline.

This baseline is mandatory because the project must demonstrate whether the neural decoder provides value beyond a well-established classical motor-imagery approach.

---

## Objective 3 — Implement a neural EEG decoder

Implement and evaluate **EEGNet or the approved compact CNN decoder**.

The decoder must expose usable probability outputs to downstream modules rather than only hard class predictions.

---

## Objective 4 — Evaluate probability calibration

Determine whether raw classifier probabilities are suitable for downstream decision-making.

Calibration must be evaluated with appropriate metrics/diagnostics such as:

- reliability diagrams,
- Expected Calibration Error,
- Brier Score,
- or another justified method.

The exact calibration technique is currently unresolved and must be selected later rather than assumed here.

---

## Objective 5 — Implement sequential Bayesian goal/intention inference

Treat human intention as a latent state rather than assuming a single EEG prediction reveals the intended goal with certainty.

The system must perform an actual probabilistic update of the form:

\[
P(G \mid E_{1:t})
\propto
P(E_t \mid G)P(G \mid E_{1:t-1})
\]

where:

- \(G\) represents the current goal/intention hypothesis;
- \(E_t\) represents the current EEG-derived evidence;
- and the posterior is updated sequentially over observations.

The exact mapping from binary EEG output to Search & Rescue goals remains unresolved and is explicitly preserved as an open decision.

---

## Objective 6 — Make uncertainty operational

Uncertainty must not exist only as a displayed number.

The project must compute a usable uncertainty measure, with entropy as the approved initial direction:

\[
H(P)=-\sum_i p_i\log p_i
\]

and use uncertainty to alter system behaviour.

Conceptually:

- lower uncertainty / higher confidence → greater autonomous assistance;
- intermediate uncertainty → confirmation or reduced autonomous commitment;
- high uncertainty → defer, pause, or request human input.

Exact thresholds are not yet locked.

---

## Objective 7 — Implement genuine shared autonomy

The system must preserve the central responsibility split:

> **Human determines WHAT objective is intended. AI determines HOW to achieve that objective safely.**

Shared autonomy must include meaningful human control through mechanisms such as:

- confirmation,
- override,
- pause,
- and emergency stop.

The autonomous system must not simply execute every decoder output.

---

## Objective 8 — Implement autonomous planning in the Search & Rescue environment

Develop a simple 2D technical environment and autonomous planner capable of:

- representing the agent,
- representing goals,
- representing obstacles/blocked paths,
- representing hazard/risk regions,
- planning a path,
- and replanning when required.

A* is the approved initial path-planning method.

A risk-aware cost formulation may use a concept such as:

\[
J = \text{distance} + \lambda \cdot \text{risk}
\]

but the exact hazard model and \(\lambda\) remain unresolved.

---

## Objective 9 — Implement explicit safety behaviour

Safety must be represented separately from the intent decoder and task objective.

The system must be able to:

- reject blocked actions,
- reject or constrain unsafe actions,
- avoid or account for hazardous regions,
- trigger replanning,
- defer under uncertainty when appropriate,
- and support emergency stop behaviour.

Safety must be measurable in experiments.

---

## Objective 10 — Implement adaptation where scientifically justified

The intended final architecture includes user/system adaptation based on interaction or correction history.

Possible forms already discussed include:

- updating priors,
- updating reliability estimates,
- updating thresholds,
- or another approved user-specific mechanism.

The exact adaptation mechanism is not yet fixed.

The final documentation must describe only the mechanism actually implemented and must not imply advanced adaptive-control theory if the system merely adapts priors, reliability estimates, or thresholds.

---

## Objective 11 — Evaluate robustness and generalization

The project must investigate behaviour under uncertainty or distribution variation through:

- simulated prediction/signal degradation,
- cross-subject evaluation,
- controlled noise,
- failure-case analysis,
- and relevant stress testing.

Previously discussed noise levels such as 10%, 20%, and 30% are provisional ideas rather than locked constants.

---

## Objective 12 — Perform component-level ablation

The architecture must remain modular enough to remove or disable important components and measure their effect.

At minimum, the project should support ablation of:

- Bayesian inference,
- uncertainty handling,
- safety,
- and adaptation.

The purpose is to determine **which components actually contribute** rather than treating the final architecture as an inseparable black box.

---

## Objective 13 — Produce reproducible technical evidence

The project must generate traceable evidence including:

- configuration,
- random seed where applicable,
- dataset/subject split,
- model version/checkpoint,
- Git commit,
- experiment condition,
- metrics,
- logs,
- plots/tables,
- and timestamps/metadata where appropriate.

No result should exist only as an undocumented screenshot.

---

# 6. SECONDARY RESEARCH QUESTIONS AND HYPOTHESES

The questions below formalize the research themes already approved in the transferred project context. They do not resolve any currently open architecture decision.

---

## RQ-1 — Classical versus neural EEG decoding

> **Does the EEGNet/compact neural decoder provide better or more useful motor-imagery decoding than the CSP + LDA classical baseline under the approved evaluation protocol?**

### H-1

> The neural decoder is expected to provide competitive or improved decoding performance relative to CSP + LDA on at least some evaluation dimensions, but this must be established experimentally and is not assumed in advance.

### Relevant measurements

- accuracy,
- balanced accuracy,
- precision,
- recall,
- F1,
- confusion matrix,
- cross-validation performance,
- and cross-subject generalization where applicable.

A finding that CSP + LDA performs as well as or better than EEGNet is scientifically acceptable and must be reported honestly.

---

## RQ-2 — Calibration and decision reliability

> **Does probability calibration improve the reliability of decoder confidence for downstream autonomy decisions compared with using raw classifier probabilities?**

### H-2

> Calibration should reduce probability miscalibration, reflected in measures such as ECE and/or Brier Score, and should make downstream confidence-based decisions more defensible.

### Relevant measurements

- Expected Calibration Error,
- Brier Score,
- reliability diagrams,
- calibration behaviour across subjects/conditions where appropriate,
- and downstream decision behaviour.

Calibration is not expected to magically increase classification accuracy; its purpose is to improve the meaning of predicted confidence.

---

## RQ-3 — Sequential Bayesian intent inference

> **Does sequential Bayesian accumulation of EEG evidence improve goal/intention reliability relative to acting directly on individual EEG predictions?**

### H-3

> Sequential Bayesian inference should reduce premature or unstable goal commitment when evidence is noisy, at the possible cost of additional decision latency.

### Relevant measurements

- goal/intention inference accuracy,
- posterior confidence,
- entropy,
- wrong-goal commitment,
- time/observations to reliable commitment,
- and decision latency.

This question depends on the final approved mapping between EEG classes and Search & Rescue goals. Until that mapping is approved, the question remains conceptually locked but the exact experiment is not frozen.

---

## RQ-4 — Uncertainty-aware shared autonomy

> **Does allowing uncertainty to control autonomous commitment reduce inappropriate autonomous actions compared with direct or confidence-blind EEG control?**

### H-4

> Uncertainty-aware deferral/confirmation should reduce wrong or unsafe autonomous commitments, while potentially increasing confirmation frequency or completion time.

### Relevant measurements

- wrong-goal rate,
- inappropriate action rate,
- deferral frequency,
- confirmation frequency,
- human interventions,
- task success,
- completion time,
- and path efficiency.

A safety-versus-speed trade-off is a legitimate finding.

---

## RQ-5 — Explicit safety controller

> **Does an explicit safety layer reduce safety violations compared with an otherwise equivalent system without that safety layer?**

### H-5

> Explicit safety constraints should reduce attempted or executed unsafe actions and hazardous-zone violations, potentially at the cost of longer routes, replanning, or task delay.

### Relevant measurements

- attempted unsafe actions,
- executed safety violations,
- hazardous-zone entries,
- safety overrides,
- replanning count,
- path length,
- completion time,
- and task success.

Safety must not be judged only from reward.

---

## RQ-6 — Full-system value

> **Does the complete NeuroCognitive shared-autonomy system provide a better overall reliability/safety trade-off than simpler system variants?**

This is the system-level operationalization of the primary research question.

### H-6

> The complete system is expected to provide a stronger balance of goal reliability, uncertainty handling, safety, and task success than direct EEG control, but it may not dominate every baseline on every individual metric.

### Required principal comparison

**System A — Direct EEG control**

```text
EEG decoder → direct decision/action
```

**System B — Confidence-aware EEG control**

```text
EEG decoder → confidence/uncertainty → action or reject/defer
```

**System C — Bayesian shared autonomy**

```text
EEG evidence → Bayesian goal inference → autonomous navigation
```

**System D — Full NeuroCognitive shared autonomy**

```text
EEG
+ calibration
+ Bayesian inference
+ uncertainty
+ shared autonomy
+ safety
+ adaptation
```

The Experimental Design document may add justified baselines but must not remove these principal configurations without approval.

---

## RQ-7 — Robustness to degraded or uncertain EEG evidence

> **How does the system behave when EEG predictions become less reliable or noisier?**

### H-7

> The uncertainty-aware/Bayesian architecture should degrade more gracefully than direct EEG control as prediction quality deteriorates, because uncertain evidence can trigger deferral rather than immediate action.

### Relevant measurements

- task success under noise,
- wrong-goal rate,
- uncertainty/entropy,
- safety violations,
- deferrals,
- intervention frequency,
- completion time,
- and relative degradation from clean/baseline conditions.

Exact noise levels remain to be defined in the Experimental Design document.

---

## RQ-8 — Cross-subject generalization

> **How well do the EEG-decoding and downstream shared-autonomy components generalize when evaluated across subjects or on unseen subjects?**

### H-8

> Performance is expected to decrease under cross-subject generalization relative to within-subject conditions because EEG varies substantially across individuals; the research value lies in measuring and analysing that degradation rather than hiding it.

### Relevant measurements

- balanced accuracy/F1 across subjects,
- calibration differences,
- posterior/goal inference behaviour,
- downstream task success,
- and failure cases.

The exact cross-subject split/protocol is intentionally not fixed in this document.

---

## RQ-9 — Adaptation / personalization

> **If the approved adaptation mechanism is implemented, does adaptation from user corrections or interaction history improve later shared-autonomy decisions?**

### Status

**Conditional research question.**

The exact adaptation mechanism is still unresolved.

### Working hypothesis

> A justified user-specific adaptation mechanism may reduce repeated incorrect commitments, unnecessary confirmations, or decision latency over repeated interactions.

This hypothesis must not be finalized operationally until the adaptation mechanism itself is approved.

If adaptation is removed through an explicit scope change, this question must be revised through the same change-control process rather than silently deleted.

---

# 7. PROJECT SCOPE — IN SCOPE

The following are part of the approved project scope.

## 7.1 EEG / BCI

- public prerecorded EEG;
- motor-imagery data;
- PhysioNet EEG Motor Movement/Imagery dataset through MNE-Python as the approved starting direction;
- initially Left-hand versus Right-hand motor imagery;
- preprocessing;
- event handling;
- epoch extraction;
- CSP;
- LDA;
- EEGNet/compact CNN;
- decoder probabilities;
- model evaluation;
- calibration;
- cross-subject investigation.

---

## 7.2 Probabilistic cognition / intent inference

- latent goal/intention representation;
- prior;
- likelihood;
- posterior;
- sequential Bayesian evidence accumulation;
- entropy/uncertainty;
- confidence-dependent decision behaviour.

---

## 7.3 Human–AI interaction / shared autonomy

- human remains source of intended objective;
- autonomous system handles execution/planning;
- confirmation;
- override;
- pause;
- emergency stop;
- deferral;
- confidence-dependent assistance.

---

## 7.4 Autonomous planning

- simple 2D Search & Rescue simulation;
- agent state;
- goals;
- obstacles;
- blocked paths;
- hazard/risk zones;
- A* planning;
- risk-aware planning;
- replanning.

---

## 7.5 Safety

- explicit safety rules/constraints;
- unsafe-action rejection;
- hazard avoidance;
- uncertainty-triggered deferral where appropriate;
- emergency stopping;
- safety evaluation.

---

## 7.6 Adaptation

- user/system adaptation where scientifically justified;
- correction history;
- priors/reliability/threshold adaptation or another later approved mechanism.

The specific algorithm remains open.

---

## 7.7 Experimentation

- A/B/C/D system comparison;
- classical-versus-neural EEG comparison;
- calibration evaluation;
- Bayesian inference evaluation;
- component ablations;
- noise/robustness testing;
- cross-subject analysis;
- safety metrics;
- task metrics;
- failure analysis;
- reproducibility.

---

## 7.8 Interface / visualization

- simple technical 2D visualization;
- Streamlit dashboard;
- plots/tables necessary to understand and inspect results;
- offline EEG replay interface.

The interface is for technical interpretation and demonstration, not as the main contribution.

---

# 8. PROJECT SCOPE — OUT OF SCOPE

The following are explicitly outside the core project unless a future owner-approved decision changes the scope.

- physical EEG acquisition;
- live EEG headset integration;
- claiming live BCI;
- physical robot;
- drone hardware;
- IoT hardware;
- elaborate 3D simulation;
- photorealistic Search & Rescue environment;
- Blender modelling;
- unnecessary computer vision;
- LLM integration;
- RAG;
- Gemini/OpenAI API;
- blockchain;
- AWS/cloud architecture added only for complexity;
- Kubernetes;
- complex microservices;
- unrelated backend systems;
- mobile application;
- full clinical or medical-device validation;
- certified real-world rescue safety;
- full neurobiological brain modelling;
- mind-reading/thought-decoding claims.

The project must remain focused on the approved research problem.

---

# 9. MINIMUM VIABLE SYSTEM

If time or implementation constraints become severe, the minimum viable research system is:

```text
PhysioNet EEG
→ preprocessing
→ CSP + LDA
→ probabilities
→ Bayesian Left/Right goal inference
→ entropy/uncertainty
→ simple 2D Gymnasium/Search & Rescue environment
→ A* planning
→ confidence-based human confirmation
→ simple Streamlit demonstration
→ controlled system comparison
```

This MVP is an emergency fallback and **does not silently redefine the intended final project**.

A reduced implementation must be documented as such.

---

# 10. INTENDED FINAL CORE SYSTEM

The intended final core system is:

```text
PhysioNet motor-imagery EEG
        ↓
preprocessing / epoching
        ↓
CSP + LDA baseline
        +
EEGNet / compact CNN
        ↓
probability outputs
        ↓
probability calibration
        ↓
sequential Bayesian goal inference
        ↓
posterior belief
        ↓
entropy / uncertainty
        ↓
confidence-dependent shared autonomy
        ↓
confirmation / override / pause / stop
        ↓
safety controller
        ↓
A* / approved autonomous planning
        ↓
simple 2D Search & Rescue environment
        ↓
adaptation where justified
        ↓
logging / experiments / ablations / robustness
        ↓
technical dashboard and documentation
```

The intended final system remains software-first and does not require 3D modelling or physical hardware.

---

# 11. OPTIONAL EXTENSIONS — NOT CORE REQUIREMENTS

Only after the core system is correct, stable, and experimentally evaluated may optional extensions be considered.

Possible extensions already identified include:

- C++ component;
- ROS 2 transfer validation;
- Gazebo/robotics simulation;
- PPO or another RL comparison;
- Spiking Neural Network comparison;
- neuromorphic/brain-inspired extension;
- multiclass EEG intent selection;
- more advanced Bayesian filtering;
- active-inference-style exploratory model;
- human-subject study;
- live EEG hardware;
- physical robot integration;
- research-paper submission.

None of these may be treated as mandatory unless the project owner explicitly changes scope.

---

# 12. EXPECTED TECHNICAL OUTPUTS

The project is expected to produce, at minimum where applicable:

## 12.1 Code and system artifacts

- reproducible Git/GitHub repository;
- modular source code;
- configuration files;
- tests;
- EEG loading/preprocessing pipeline;
- CSP + LDA implementation;
- EEGNet/compact CNN implementation;
- calibration module;
- Bayesian goal-inference module;
- uncertainty module;
- adaptation module where implemented;
- Search & Rescue environment;
- A* planner;
- safety controller;
- shared-autonomy controller;
- human-interaction controls;
- offline EEG replay;
- Streamlit technical dashboard;
- experiment/evaluation scripts.

---

## 12.2 Model artifacts

- trained classical/neural model outputs where relevant;
- saved neural-model checkpoints where appropriate;
- calibration parameters/model where applicable;
- configuration metadata;
- subject/split information.

---

## 12.3 Experimental artifacts

- machine-readable logs;
- CSV/JSON result files;
- evaluation tables;
- plots;
- confusion matrices;
- calibration plots;
- robustness results;
- cross-subject results;
- ablation results;
- safety/task results;
- failure cases.

Every reported result must be traceable to an actual experiment.

---

## 12.4 Documentation artifacts

The broader documentation plan includes:

- master authority documents;
- scenario specification;
- architecture documentation;
- technology-stack document;
- dataset/data-pipeline document;
- neuroscience/BCI foundations;
- signal-processing and ML methodology;
- calibration/uncertainty document;
- Bayesian-inference document;
- cognitive/adaptation document;
- shared-autonomy/HCI document;
- planning document;
- safety document;
- implementation blueprint;
- repository/code architecture;
- experimental design;
- metrics/evaluation;
- testing/verification;
- limitations/ethics/validity;
- literature foundation;
- AI-assisted development workflow;
- live state/decision/experiment logs;
- final results/discussion;
- future work;
- final technical report;
- GitHub README;
- eventual resume/portfolio positioning.

No final report should contain performance claims before corresponding experiments exist.

---

# 13. SUCCESS CRITERIA — TECHNICAL COMPLETION

The project may be called technically complete only when an integrated, reproducible pipeline satisfies the following core conditions:

1. Real public EEG data can be loaded and validated.
2. EEG preprocessing and epoching operate correctly.
3. CSP + LDA is trained and evaluated.
4. EEGNet/compact CNN is trained and evaluated unless an explicit owner-approved scope change removes it.
5. Decoder probability outputs are available to downstream modules.
6. Probability calibration/uncertainty is evaluated and operationalized.
7. Bayesian goal/intention inference performs sequential belief updates.
8. Uncertainty influences system behaviour.
9. Shared-autonomy logic can act, defer, or request human intervention according to the approved policy.
10. Human confirmation/override/pause/stop is represented.
11. The safety module can reject unsafe actions.
12. The planner can navigate the approved 2D Search & Rescue environment.
13. Offline EEG replay can drive the end-to-end system.
14. Experiment logs and result artifacts are saved.
15. The principal A/B/C/D comparison can be executed.
16. Robustness testing can be executed.
17. Component ablation can be executed.
18. Cross-subject analysis can be performed under the final approved protocol.
19. Failure cases can be inspected and documented.
20. Results are reproducible and traceable to code/configuration.
21. Documentation accurately states what was and was not implemented.

A working Streamlit screen alone does not satisfy these conditions.

---

# 14. SUCCESS CRITERIA — RESEARCH QUALITY

Research success is different from software completion.

The project should be considered a strong research-quality technical artifact if it demonstrates:

- a clearly defined research question;
- falsifiable hypotheses;
- real public EEG data;
- appropriate baselines;
- controlled comparison;
- explicit uncertainty;
- measurable safety;
- modular ablation;
- reproducible experiments;
- honest failure analysis;
- honest limitations;
- no fabricated metrics;
- no leakage;
- no misleading real-time/clinical claims;
- and a defensible interpretation of trade-offs.

**The full system does not need to win every metric for the research to succeed.**

A scientifically valuable conclusion may be:

- one component adds little value;
- safety improves while speed decreases;
- neural decoding does not outperform the classical baseline;
- calibration helps some conditions but not others;
- cross-subject generalization remains weak;
- Bayesian accumulation reduces premature commitment but increases latency;
- or adaptation helps only specific subjects/conditions.

These are valid findings if supported by the experiments.

---

# 15. WHAT DOES NOT COUNT AS SUCCESS

The following are insufficient on their own:

- a visually attractive dashboard;
- high EEG accuracy on a leakage-prone split;
- a single successful demo episode;
- a video of the agent reaching a target;
- a 3D simulation with weak experiments;
- many technologies with no scientific purpose;
- only reporting the best seed/run;
- claiming safety because no collision happened in one demo;
- claiming uncertainty awareness because entropy is plotted but ignored by the controller;
- claiming Bayesian reasoning without a real probabilistic update;
- claiming adaptation without a measurable adaptation mechanism;
- claiming real-time EEG when the system uses prerecorded replay;
- writing resume metrics before experiments are completed.

---

# 16. SCIENTIFIC VALIDITY REQUIREMENTS

## 16.1 Data leakage

Training, validation, and testing must be separated correctly.

Subject identity must be preserved when the experiment requires subject-wise separation.

No preprocessing, feature fitting, calibration fitting, or model selection may leak test information.

---

## 16.2 Fair baselines

Comparisons must use equivalent datasets/conditions wherever scientifically appropriate.

The full system must not receive privileged information that simpler baselines do not receive unless the difference is part of the experimental question and is explicitly documented.

---

## 16.3 Traceability

Every reported number must be traceable to:

- code,
- experiment configuration,
- dataset/split,
- model,
- and result artifact.

---

## 16.4 Falsifiability

The experiment must permit hypotheses to fail.

The project must not define success metrics after seeing results merely to make the proposed system appear superior.

---

## 16.5 Failure analysis

Failure cases are mandatory evidence, not optional embarrassment.

Examples may include:

- incorrect EEG classification;
- overconfident prediction;
- wrong Bayesian commitment;
- delayed commitment;
- unnecessary deferral;
- incorrect goal;
- safety override;
- poor cross-subject performance;
- path inefficiency;
- adaptation failure.

---

# 17. CLAIM BOUNDARIES

The following terminology must match implementation.

## “NeuroCognitive”

May be used only because the project combines:

- EEG-derived neural evidence, and
- computational modelling of intention/belief/uncertainty.

It must not imply that the project recreates the human brain or models cognition comprehensively.

---

## “EEG-based intent decoding”

Must refer to the defined motor-imagery classification/goal-selection mechanism.

It must not imply unrestricted thought reading.

---

## “Bayesian”

Requires actual prior/likelihood/posterior probabilistic updating.

---

## “Uncertainty-aware”

Requires uncertainty to alter behaviour.

A displayed confidence score alone is insufficient.

---

## “Shared autonomy”

Requires a real division of control between human intention/authority and autonomous execution.

---

## “Safety” / “safety-critical”

Must refer to explicit implemented and measurable simulated safety constraints.

It must not imply certified real-world safety.

---

## “Adaptive control”

Must match the actual adaptation mechanism.

If only priors, reliability estimates, or thresholds adapt, documentation must say exactly that.

---

## “Real-time”

The planned system uses prerecorded EEG replay.

The correct phrasing is **offline EEG replay** or **simulated real-time BCI** unless physical live acquisition is later implemented.

---

# 18. KNOWN ASSUMPTIONS

The project currently assumes:

- public prerecorded motor-imagery EEG is sufficient for the core research prototype;
- a simple 2D environment is sufficient to study the algorithmic research problem;
- Search & Rescue provides a meaningful safety-relevant scenario without requiring physical robotics;
- goal-level BCI control is preferable to low-level continuous joystick-style EEG control for the approved concept;
- uncertainty must be incorporated into behavioural decisions;
- explicit safety should remain separate from mere task reward;
- A* is sufficient as the initial planner;
- deep theoretical mastery can continue after implementation, but scientific verification cannot be postponed;
- AI-assisted code generation is acceptable provided the owner verifies the system and the results;
- the project is not intended to replace formal university prerequisite coursework.

---

# 19. UNRESOLVED DECISIONS — MUST REMAIN OPEN

The following issues are explicitly **not yet finalized**.

## 19.1 Binary EEG output versus multiple rescue goals — critical

Initial EEG task:

> **Left-hand motor imagery vs Right-hand motor imagery**

Potential Search & Rescue scenario:

- Victim A;
- Victim B;
- medical/resource point;
- safe zone;
- other mission goals.

A binary decoder cannot automatically map one-to-one to an arbitrary number of goals.

Previously identified possibilities are:

1. only two active selectable goals at a time;
2. hierarchical/sequential binary selection;
3. later multiclass EEG;
4. EEG controls a binary abstract priority/choice while autonomous logic handles the broader mission.

**No final option is approved.**

This must be resolved before the goal-selection interface and related experiments are frozen.

---

## 19.2 Calibration method

Calibration is required.

The exact method is not yet approved.

---

## 19.3 Confidence/autonomy thresholds

The high/medium/low confidence boundaries are not fixed.

Previously discussed example values must not be treated as final constants.

---

## 19.4 Adaptation mechanism

Adaptation is part of the intended final architecture.

The exact implementation is not fixed.

---

## 19.5 Hazard/risk model

Risk-aware planning is approved conceptually.

The exact hazard representation, risk values, and \(\lambda\) are not fixed.

---

## 19.6 Cross-subject evaluation protocol

Cross-subject evaluation is required as a research direction.

The final subject split/training protocol remains to be defined in the Experimental Design document.

---

## 19.7 Research paper/publication status

A detailed technical report/documentation set is planned.

A peer-reviewed publication or research-paper submission is **not currently a mandatory deliverable**.

Future research or paper submission may be considered later.

---

# 20. PROJECT PHASE BOUNDARIES

The approved accelerated development philosophy is:

```text
DESIGN
→ GENERATE
→ RUN
→ VERIFY
→ INTEGRATE
→ COMPLETE CORE PROJECT
→ DEEPER THEORY / INTERVIEW MASTERY
```

This does **not** mean “build first and validate science later.”

During implementation, every module must still satisfy enough scientific verification to ensure:

- the dataset is correct;
- labels/events are correct;
- shapes/interfaces are correct;
- train/test leakage is avoided;
- probabilities are real outputs;
- Bayesian updates are mathematically valid;
- safety behaviour is actually enforced;
- metrics come from actual experiments;
- integration is logically valid.

Deep conceptual mastery can continue after the core project is complete.

---

# 21. OBJECTIVE PRIORITY ORDER

When implementation trade-offs occur, priority is:

1. **Scientific correctness**
2. **Validity of data and experiments**
3. **Correct end-to-end integration**
4. **Reproducibility**
5. **Core required modules**
6. **Failure/limitation analysis**
7. **Technical demonstration**
8. **UI polish**
9. **Optional extensions**

A visually impressive system with invalid experiments is a failed project.

A simple-looking system with rigorous experiments can be a successful project.

---

# 22. RELATIONSHIP TO LATER DOCUMENTS

This document establishes objectives and scope.

Later documents must expand, not contradict, it.

The next documents should define:

- `03_SEARCH_AND_RESCUE_SCENARIO.md` — exact application environment and role mapping;
- `04_SYSTEM_ARCHITECTURE.md` — detailed module/data flow;
- `05_TECHNOLOGY_STACK.md` — exact approved tools/dependencies;
- `06_DATASET_AND_DATA_PIPELINE.md` — EEG data handling;
- `07_NEUROSCIENCE_AND_BCI_FOUNDATIONS.md`;
- `08_EEG_SIGNAL_PROCESSING_AND_ML.md`;
- `09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md`;
- `10_BAYESIAN_GOAL_INFERENCE.md`;
- `11_COGNITIVE_AND_ADAPTIVE_MODEL.md`;
- `12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`;
- `13_AUTONOMOUS_PLANNING_AND_CONTROL.md`;
- `14_SAFETY_CRITICAL_CONTROL.md`;
- and the later implementation, experiment, testing, result, and reporting documents.

The detailed Search & Rescue scenario document must **not silently solve the binary-EEG-to-multiple-goal ambiguity**. If scenario design requires that decision, it must be flagged for owner approval first.

---

# 23. DOCUMENT COMPLETION STATEMENT

This document is considered complete as the authoritative **Objectives, Scope & Research Questions** baseline because it defines:

- the primary objective;
- secondary objectives;
- the central research question;
- formal secondary research questions;
- falsifiable hypotheses;
- in-scope components;
- out-of-scope components;
- the MVP;
- the intended final system;
- optional extensions;
- expected outputs;
- technical completion criteria;
- research-quality success criteria;
- scientific validity requirements;
- claim boundaries;
- assumptions;
- and unresolved decisions.

It deliberately does **not** resolve the known open design choices.

Those choices must remain open until the project owner explicitly approves them.

---

# 24. CURRENT ONE-PARAGRAPH SCOPE STATEMENT

**NeuroCognitive Shared Autonomy for Search & Rescue** is a software-first research project that uses prerecorded public motor-imagery EEG to infer a human operator's intended goal or choice, compares classical CSP+LDA and EEGNet-based decoding, calibrates model probabilities, accumulates uncertain neural evidence through sequential Bayesian inference, estimates uncertainty, and uses that uncertainty to regulate shared autonomy. The human retains confirmation, override, pause, and emergency-stop authority, while the autonomous system performs safe goal-directed navigation in a simple 2D Search & Rescue environment using A*-based planning and an explicit safety controller. The system is evaluated through direct, confidence-aware, Bayesian, and full shared-autonomy configurations, together with calibration, ablation, robustness, cross-subject, safety, task-performance, and failure analyses. The project intentionally excludes unnecessary hardware, 3D modelling, LLM/RAG/cloud complexity, and unsupported real-time or clinical claims. The exact binary-EEG-to-multiple-goal mapping, calibration method, confidence thresholds, adaptation mechanism, hazard-risk formulation, and cross-subject protocol remain unresolved and require explicit owner approval before they are frozen.
