# 25_FUTURE_WORK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Future Work, Extension Priorities, Research Opportunities, and Scope-Controlled Evolution

**Document ID:** L-03  
**Document class:** Future Work / Extension Roadmap / Research Opportunities  
**Status:** Authoritative future-work framework — **future items are not automatically approved core scope**  
**Authority level:** Subordinate to `MASTER_PROJECT_SPEC.md`, approved scientific documents, implementation governance, results framework, discussion framework, and explicit Project Owner decisions  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. PURPOSE

This document defines possible future extensions after the core project is completed and validated.

It exists to answer:

> **What could the project become next without weakening the focus of the current research?**

Future work must remain clearly separated from the approved core.

A future-work item is:

```text
an extension opportunity
```

not:

```text
a hidden requirement for the current project
```

---

# 1. CORE RULE

Do not expand the current project merely because a future direction sounds impressive.

The current project should first complete and validate:

```text
public prerecorded motor-imagery EEG
→ CSP+LDA
→ EEGNet / compact CNN
→ calibration
→ Bayesian goal inference
→ uncertainty
→ shared autonomy
→ A*
→ safety
→ 2D SAR simulation
→ reproducible experiments
```

Only after the core pipeline is stable should future extensions be considered.

---

# 2. FUTURE-WORK CATEGORIES

Future directions are grouped into:

```text
F1 — Scientific completion of currently unresolved methodology
F2 — Stronger EEG / BCI methods
F3 — Stronger cognitive / probabilistic inference
F4 — Human–AI interaction and personalization
F5 — Robotics / autonomy expansion
F6 — Safety / verification expansion
F7 — Real-time / hardware expansion
F8 — Generalization / evaluation expansion
F9 — Software / systems engineering expansion
F10 — Research dissemination / portfolio expansion
```

---

# 3. PRIORITY LEVELS

Use these priority levels:

```text
P0 — Required before final core conclusions
P1 — Strong next-step extension
P2 — Valuable research extension
P3 — Long-term / optional exploration
```

Future work should not override current milestone priorities.

---

# 4. P0 — RESOLVE CURRENT SCIENTIFIC OPEN DECISIONS

Before treating the current project as scientifically complete, the following unresolved methodological decisions must be finalized.

## EEG preprocessing

```text
- exact filter band
- reference
- epoch interval
- baseline correction
- artifact policy
- T0 handling
```

## Evaluation

```text
- train/validation/test protocol
- cross-subject protocol
- subject split strategy
```

## Calibration

```text
- calibration method
- fitting partition
- reliability-bin strategy
```

## Bayesian inference

```text
- binary EEG → goal-selection protocol
- decoder output → goal likelihood semantics
- prior policy
- stopping / commitment rule
```

## Shared autonomy

```text
- confidence / entropy thresholds
- exact proceed / confirm / defer policy
```

## Adaptation

```text
- target parameter
- update rule
- bounds
- reset behavior
```

## Planning / safety

```text
- risk scale
- risk λ
- prohibited-hazard threshold
- no-safe-path semantics
```

These are not optional future features.

They are methodological items that must be resolved before final experiments if the relevant component is included.

---

# 5. P1 — LIVE EEG ACQUISITION

One major future extension is replacing prerecorded EEG replay with a real EEG acquisition system.

Potential future architecture:

```text
EEG headset
→ live acquisition
→ online preprocessing
→ decoder
→ calibration
→ Bayesian inference
→ shared autonomy
→ simulation / robot
```

This would allow evaluation of:

- real acquisition latency;
- electrode placement variability;
- live signal quality;
- user fatigue;
- online artifacts;
- feedback-driven behavior;
- true human-system interaction.

---

# 6. LIVE EEG CLAIM CHANGE

If live EEG is added and verified, terminology may evolve from:

```text
Offline EEG Replay
Simulated Real-Time BCI
```

toward:

```text
Online BCI
Live EEG Control
```

but only after the corresponding system is genuinely implemented and tested.

---

# 7. P1 — HUMAN-SUBJECT INTERACTION STUDY

A controlled human study would substantially strengthen the HCI and BCI contribution.

Possible measures:

```text
task completion
confirmation frequency
override behavior
decision latency
trust
usability
mental workload
fatigue
subjective confidence
preference
```

This would require:

- ethical approval where applicable;
- consent;
- participant protocol;
- recruitment criteria;
- data-management plan;
- human-subject analysis.

The current project must not claim these outcomes without such a study.

---

# 8. P1 — MULTI-GOAL BCI INTERACTION

The initial EEG decoder is binary.

A major future direction is to strengthen the interface between binary BCI evidence and richer goal spaces.

Possible approaches include:

```text
hierarchical binary selection
sequential binary menus
context-dependent option sets
multistage goal confirmation
multiclass motor imagery
hybrid BCI interaction
```

The best approach should be selected based on interaction simplicity and scientific defensibility.

---

# 9. HIERARCHICAL BINARY SELECTION

A strong near-term extension could use hierarchical binary choice.

Example:

```text
Level 1:
Rescue Target
vs
Safe Zone

Level 2:
Victim A
vs
Victim B
```

Advantages:

- preserves binary decoder;
- allows more than two mission goals;
- keeps EEG task scientifically aligned with dataset structure.

Potential downside:

- increases decision steps;
- increases latency;
- may increase cognitive burden.

---

# 10. MULTICLASS EEG

A later extension could move from:

```text
Left vs Right
```

toward:

```text
Left hand
Right hand
Both fists
Feet
```

or another scientifically justified multiclass setup.

This requires:

- suitable dataset runs;
- explicit class semantics;
- new evaluation protocol;
- new confusion analysis;
- potentially different model design.

Multiclass BCI must not be retrofitted silently into the current binary project.

---

# 11. P1 — BETTER CROSS-SUBJECT GENERALIZATION

Cross-subject EEG generalization is a major research challenge.

Future work may examine:

```text
subject-normalized representations
domain adaptation
transfer learning
subject-independent pretraining
few-shot subject calibration
meta-learning
```

The purpose would be to reduce dependence on subject-specific retraining.

---

# 12. P1 — FEW-SHOT PERSONALIZATION

A practical future system may use:

```text
general pretrained decoder
+
small amount of new-user calibration
```

This could balance:

```text
generalization
vs
personalization
```

Potential evaluation:

- zero-shot performance;
- few-shot performance;
- subject-specific performance;
- amount of calibration data required.

---

# 13. P1 — STRONGER PROBABILITY CALIBRATION

Future calibration research could compare:

```text
temperature scaling
Platt scaling
isotonic regression
vector scaling
Bayesian calibration
ensemble calibration
```

The goal should remain:

> improve probability reliability for downstream decision-making.

Do not add methods merely to increase methodological complexity.

---

# 14. P1 — DISTRIBUTION-SHIFT CALIBRATION

A valuable extension is to study whether calibration remains reliable under:

- unseen subjects;
- lower signal quality;
- altered recording conditions;
- temporal drift.

This is especially important because confidence is used operationally in shared autonomy.

---

# 15. P1 — ADVANCED UNCERTAINTY ESTIMATION

The current project uses posterior entropy as the primary uncertainty signal.

Future work may investigate:

```text
predictive entropy
Monte Carlo dropout
deep ensembles
Bayesian neural networks
evidential deep learning
conformal prediction
out-of-distribution detection
```

These methods could help distinguish different uncertainty sources.

---

# 16. UNCERTAINTY DECOMPOSITION

A more advanced system might separate:

```text
aleatoric uncertainty
epistemic uncertainty
distribution shift
goal ambiguity
```

This could improve autonomy decisions.

For example:

```text
high epistemic uncertainty
→ request more evidence

high environmental risk
→ change route

high goal ambiguity
→ ask user confirmation
```

These should remain separate signals.

---

# 17. P1 — RICHER BAYESIAN GOAL MODELS

The current core uses sequential Bayesian updating.

Future work may consider:

```text
Hidden Markov Models
Dynamic Bayesian Networks
Bayesian state-space models
Particle filtering
hierarchical Bayesian models
```

These may be useful if:

- goals can change over time;
- evidence has temporal dependence;
- goal transitions must be modeled explicitly.

---

# 18. TEMPORAL DEPENDENCE MODELING

Repeated EEG evidence may be correlated.

A future probabilistic model could explicitly account for temporal dependence rather than treating evidence updates as conditionally independent.

This may reduce false posterior overconfidence.

---

# 19. P2 — ACTIVE INFERENCE

Active inference is an optional research direction.

It could potentially unify:

```text
belief
uncertainty
action
goal-directed control
```

However, it should only be added if there is a clear scientific question.

It must not replace the simpler Bayesian system merely because it is more sophisticated.

---

# 20. P1 — BETTER ADAPTATION / PERSONALIZATION

The current project may implement only simple, bounded adaptation.

Future work could investigate:

```text
adaptive priors
subject-specific confidence thresholds
online calibration updates
decoder reliability tracking
evidence-weight adaptation
context-dependent arbitration
```

Any adaptation mechanism must remain:

- interpretable;
- bounded;
- logged;
- reversible;
- leakage-safe.

---

# 21. TRUE CO-ADAPTIVE BCI

With live EEG and participants, future research could study actual co-adaptation:

```text
human learns system
+
system learns human
```

This is qualitatively different from current offline system-side personalization.

It would require longitudinal interaction data.

---

# 22. P1 — HUMAN-AWARE SHARED AUTONOMY

Future shared-autonomy policies could consider:

```text
user correction history
recent uncertainty
confirmation burden
goal history
task urgency
environmental risk
```

This could produce more context-sensitive autonomy.

---

# 23. DYNAMIC AUTONOMY LEVELS

Instead of a simple fixed threshold structure, future work could dynamically alter autonomy based on:

```text
belief confidence
user reliability
risk
mission urgency
recent errors
```

Example:

```text
high confidence + low environmental risk
→ stronger autonomous assistance

low confidence + high mission risk
→ confirmation / deferral
```

---

# 24. P2 — HUMAN TRUST AND AUTOMATION BIAS

With a human study, future work could examine whether displaying model confidence affects:

- trust;
- over-reliance;
- under-reliance;
- intervention behavior;
- perceived control.

This would strengthen the HCI dimension.

---

# 25. P2 — EXPLAINABLE SHARED AUTONOMY

The interface could explain decisions such as:

```text
“Goal uncertain — confirmation requested.”

“Route changed because hazard risk increased.”

“Movement blocked by safety controller.”
```

The goal should be transparent reasoning, not verbose explanations.

---

# 26. P1 — DYNAMIC SEARCH & RESCUE ENVIRONMENT

The current environment is static-first.

Future work could add controlled dynamics:

```text
new obstacle appears
hazard level changes
victim priority changes
route becomes unavailable
safe zone changes
```

This would test replanning and autonomy under non-stationary conditions.

---

# 27. DYNAMIC HAZARD MODEL

Future environmental hazards may evolve over time.

Examples:

```text
fire spread
flood depth
smoke concentration
structural instability
```

This would require a scientifically defined hazard model.

Do not add unrealistic visual complexity without modeling value.

---

# 28. P2 — CONTINUOUS-SPACE NAVIGATION

The current grid is intentionally simple.

Future work could move toward:

```text
continuous 2D navigation
robot kinematics
velocity control
continuous obstacles
```

This would make planning closer to robotics while increasing implementation complexity.

---

# 29. P1 — ROS2 / GAZEBO INTEGRATION

After the algorithmic pipeline is complete, a robotics extension could integrate:

```text
ROS2
Gazebo
```

Potential mapping:

```text
Bayesian approved goal
→ ROS2 navigation goal
→ planner / controller
→ simulated robot
```

This would provide a stronger robotics portfolio layer.

It is not required for the current research contribution.

---

# 30. P2 — PHYSICAL ROBOT

A later hardware extension could connect the shared-autonomy system to:

- ground robot;
- assistive mobile platform;
- small research robot.

This would introduce:

```text
localization
sensor uncertainty
actuation
network delay
hardware safety
```

It would require a new validation layer.

---

# 31. P2 — DRONE / AERIAL ROBOTICS

Aerial robotics may be relevant to Search & Rescue.

However, it introduces:

- 3D motion;
- flight dynamics;
- collision avoidance;
- regulatory and safety constraints.

It should remain a separate future project rather than expanding the current core.

---

# 32. P2 — MULTI-AGENT SEARCH & RESCUE

The current project uses one agent.

Future work could explore:

```text
multiple rescue agents
task allocation
shared map
coordination
distributed planning
```

This would create a new multi-agent systems research problem.

---

# 33. P2 — REINFORCEMENT LEARNING COMPARISON

A later experiment could compare A* / explicit policy against an RL-based navigation or arbitration method.

Possible methods:

```text
PPO
DQN
actor-critic
```

The purpose must be a controlled comparison.

RL should not replace A* simply because it appears more advanced.

---

# 34. RL FOR SHARED AUTONOMY

A future controller could learn:

```text
when to proceed
when to confirm
when to defer
```

based on a reward involving:

```text
success
latency
human burden
risk
wrong-goal penalty
```

This creates a difficult reward-design problem and should be carefully validated.

---

# 35. P2 — FORMAL SAFETY METHODS

The current safety controller uses explicit simulated constraints.

Future work could investigate:

```text
runtime assurance
formal shielding
control barrier functions
reachability analysis
temporal logic constraints
formal verification
```

This would support stronger safety arguments.

---

# 36. SAFETY VERIFICATION EXPANSION

A stronger safety study could include:

```text
adversarial state transitions
unexpected planner output
stale actions
sensor inconsistency
unsafe goal requests
network delay
controller failure
```

The purpose would be to stress-test supervisory safety.

---

# 37. P2 — ADVERSARIAL / ROBUST EEG EVALUATION

Future work may examine robustness to:

```text
channel dropout
signal corruption
electrode noise
temporal distortion
artifact contamination
distribution shift
```

This is particularly relevant if moving toward real BCI deployment.

---

# 38. P2 — OUT-OF-DISTRIBUTION DETECTION

An operational BCI should recognize when the current signal does not resemble training data.

Future work may add:

```text
OOD score
signal-quality gate
unknown-state detection
```

Possible behavior:

```text
OOD detected
→ do not commit
→ request recalibration / user confirmation
```

---

# 39. P2 — NEUROMORPHIC / BRAIN-INSPIRED MODELS

A later research extension may compare:

```text
EEGNet
vs
spiking neural network
```

or another brain-inspired architecture.

This is particularly aligned with future study interests, but it is not needed for the current system.

The comparison should answer a real question such as:

- energy efficiency;
- temporal processing;
- robustness;
- compactness.

---

# 40. P2 — BIO-INSPIRED ADAPTIVE CONTROL

Future adaptive mechanisms could draw from biological principles such as:

- homeostatic adaptation;
- bounded confidence;
- evidence accumulation;
- reliability learning.

These should remain mathematically explicit rather than metaphorical.

---

# 41. P2 — COGNITIVE ACCUMULATOR MODELS

A future cognition extension could compare the Bayesian belief model with evidence-accumulation models such as:

```text
drift-diffusion style models
sequential probability ratio tests
race models
```

Potential research question:

> Which temporal evidence model produces the best reliability-latency trade-off for EEG-driven goal selection?

---

# 42. P2 — INTENT-CHANGE DETECTION

The current goal may be treated as stable over an evidence sequence.

Future work could detect:

```text
human changes intended goal
```

during operation.

This requires:

- dynamic latent state;
- change-point detection;
- posterior reset/transition policy.

---

# 43. P2 — MULTIMODAL HUMAN INPUT

A future assistive interface could combine EEG with:

```text
eye gaze
button / switch
voice
joystick
EMG
```

This could improve reliability.

However, the research question would shift from pure EEG-driven intent toward hybrid control.

---

# 44. P2 — ERROR-RELATED POTENTIALS

Future BCI research could use neural error signals to detect when the system acts against user expectation.

Potential architecture:

```text
system action
→ user perceives error
→ ErrP detection
→ correction / posterior update
```

This could create a richer closed-loop BCI.

It would require a dataset or live experimental protocol designed for ErrPs.

---

# 45. P2 — ATTENTION / COGNITIVE STATE MONITORING

Future work could investigate whether cognitive-state signals such as:

- workload;
- fatigue;
- attention;

should modify autonomy.

This would substantially expand the neuroscience scope and requires appropriate data.

---

# 46. P1 — STRONGER EXPERIMENTAL GENERALIZATION

The current project should first establish controlled results.

Future work could broaden evaluation across:

```text
more subjects
more seeds
more map configurations
different risk layouts
different evidence sequences
different calibration conditions
```

This strengthens statistical confidence.

---

# 47. MULTI-DATASET EVALUATION

A stronger future BCI study could evaluate the same pipeline on multiple public motor-imagery datasets.

This would test whether findings are dataset-specific.

Requirements:

- harmonized labels;
- channel handling;
- preprocessing governance;
- dataset-specific reporting.

---

# 48. P1 — LONGITUDINAL EVALUATION

With live subjects, future work could evaluate repeated sessions across days/weeks.

Questions:

```text
Does decoder performance drift?
Does calibration remain valid?
Does adaptation help?
Does human interaction improve with familiarity?
```

---

# 49. P2 — FAIRNESS / SUBJECT DISPARITY ANALYSIS

Future work could investigate whether system performance varies systematically across subject groups only if appropriate demographic metadata are legitimately available and ethically usable.

This must not involve unsupported demographic inference from EEG.

---

# 50. P2 — STATISTICAL MODELING OF SUBJECT VARIABILITY

Future analysis may use:

```text
mixed-effects models
hierarchical models
subject-level random effects
```

to better characterize repeated measurements and inter-subject variability.

---

# 51. P1 — BETTER FAILURE ANALYSIS

A future iteration can build a structured failure taxonomy:

```text
signal failure
decoder failure
calibration failure
belief failure
policy failure
planner failure
safety intervention
environment failure
human correction
```

This could support automated failure attribution.

---

# 52. P2 — CAUSAL FAILURE PROPAGATION

A more advanced analysis could model how upstream errors propagate.

Example:

```text
EEG misclassification
→ distorted likelihood
→ wrong posterior
→ autonomous proceed
→ wrong goal
→ mission failure
```

This could support causal system debugging.

---

# 53. P1 — BETTER REAL-TIME SOFTWARE ENGINEERING

If the project evolves toward online BCI, future engineering may include:

```text
stream processing
timing guarantees
buffer management
asynchronous acquisition
event synchronization
latency profiling
fault recovery
```

These are unnecessary for the current prerecorded core.

---

# 54. P2 — ROS2 SOFTWARE ARCHITECTURE

If ROS2 is approved later, modules could map to:

```text
EEG node
decoder node
intent-belief node
shared-autonomy node
planner interface
safety node
logging node
```

This should be introduced only after core algorithmic behavior is stable.

---

# 55. P2 — C++ PERFORMANCE PATH

C++ could later be added for:

- ROS2 integration;
- real-time components;
- latency-sensitive inference/control.

It should not be added merely to make the repository look more complex.

---

# 56. P3 — CLOUD / DISTRIBUTED EXPERIMENT INFRASTRUCTURE

If future experimentation becomes computationally large, cloud or distributed execution may help.

Possible uses:

```text
large cross-subject sweeps
hyperparameter search
multi-dataset benchmarks
```

This is not part of the core research architecture.

---

# 57. P1 — REPRODUCIBILITY PACKAGE

After final results, a strong future/release step is to prepare:

```text
clean GitHub repository
fixed requirements
configuration examples
reproduction commands
experiment manifests
result tables
model checkpoints where appropriate
demo
```

This substantially improves portfolio and scientific value.

---

# 58. P1 — PUBLIC TECHNICAL REPORT

The completed project can be packaged as a rigorous technical report containing:

```text
problem
literature
methodology
architecture
experiments
results
discussion
limitations
future work
```

This is separate from claiming peer-reviewed publication.

---

# 59. P2 — RESEARCH PAPER

If the final experiments produce sufficiently strong and novel findings, the project could later be converted into a research manuscript.

Requirements include:

- clear research contribution;
- finalized methodology;
- sufficient experimental evidence;
- reproducible results;
- comparison with relevant literature;
- strong limitations section.

Publication should remain optional.

---

# 60. NO PREDATORY PUBLICATION

Do not submit merely to obtain a publication label.

A publication attempt should be considered only if:

```text
research contribution is real
+
results are valid
+
venue is credible
```

The technical project remains valuable without publication.

---

# 61. P1 — GITHUB PORTFOLIO

A portfolio version should emphasize:

```text
system architecture
real public EEG
reproducibility
Bayesian reasoning
uncertainty-aware autonomy
safety
experiments
failure cases
```

Avoid excessive decorative UI.

The technical pipeline is the primary evidence.

---

# 62. P1 — DEMONSTRATION VIDEO

A concise demo may show:

```text
offline EEG replay
decoder probabilities
posterior belief
entropy
confirmation / override
route planning
safety intervention
mission completion
```

The video must clearly label the system as an offline/simulated research prototype.

---

# 63. P1 — INTERVIEW / LEARNING PREPARATION

After implementation, the project can be used to deepen understanding of:

```text
EEG
CSP
LDA
CNNs
calibration
Bayesian inference
entropy
shared autonomy
A*
safety
experimental validity
```

The Project Owner should be able to explain not only what was built but why each component exists.

---

# 64. FUTURE-WORK PRIORITY MATRIX

| Future Direction | Priority | Scientific Value | Engineering Cost | Core Scope Change |
|---|---|---|---|---|
| Resolve current open methodology | P0 | Critical | Medium | No |
| Live EEG | P1 | Very High | High | Yes |
| Human-subject study | P1 | Very High | High | Yes |
| Hierarchical multi-goal selection | P1 | High | Medium | Moderate |
| Cross-subject generalization | P1 | High | Medium | No |
| Few-shot personalization | P1 | High | Medium | Moderate |
| Stronger calibration | P1 | High | Medium | No |
| Advanced uncertainty | P1/P2 | High | Medium/High | Moderate |
| Dynamic SAR | P1 | High | Medium | Moderate |
| ROS2/Gazebo | P1/P2 | High for robotics | High | Yes |
| Formal safety | P2 | High | High | Yes |
| Physical robot | P2 | High | Very High | Major |
| Reinforcement learning | P2 | Medium/High | High | Moderate |
| Neuromorphic/SNN | P2 | Research-specific | High | Moderate |
| Multi-agent SAR | P2 | High | Very High | Major |
| Cloud/distributed system | P3 | Low for core science | Medium/High | Yes |

---

# 65. RECOMMENDED POST-CORE EXTENSION ORDER

After the current project is complete, a sensible extension sequence is:

```text
1. Strengthen cross-subject evaluation
2. Improve calibration / uncertainty
3. Finalize robust multi-goal BCI interaction
4. Add stronger personalization
5. Add dynamic SAR conditions
6. Add live EEG if hardware becomes available
7. Conduct human interaction study
8. Add ROS2 / Gazebo if robotics depth is desired
9. Add formal safety or physical robot only after simulation is mature
```

This order preserves scientific progression.

---

# 66. WHAT SHOULD NOT BE DONE FIRST

Do not prioritize:

```text
3D graphics
cloud deployment
LLM integration
mobile app
microservices
blockchain
large UI redesign
```

before the current system produces valid scientific results.

These add engineering surface without addressing the main research question.

---

# 67. FUTURE WORK VS CURRENT LIMITATION

Some future-work items directly address current limitations.

| Current Limitation | Future Extension |
|---|---|
| Prerecorded EEG | Live EEG acquisition |
| No human study | Human-subject evaluation |
| Binary BCI | Hierarchical / multiclass interface |
| Subject variability | Transfer learning / personalization |
| Entropy-only uncertainty | Advanced uncertainty methods |
| Simplified Bayes assumptions | Dynamic probabilistic models |
| Static 2D map | Dynamic SAR |
| Simulation-only safety | Formal verification / hardware testing |
| No physical robot | ROS2 / robot integration |
| One dataset | Multi-dataset evaluation |

---

# 68. FUTURE WORK MUST BE HYPOTHESIS-DRIVEN

Each major extension should have a clear question.

Good:

> **Does hierarchical binary goal selection reduce wrong-goal commitment without excessive decision latency?**

Bad:

> **Add hierarchical selection because it sounds advanced.**

Good:

> **Does subject-specific calibration improve cross-subject reliability?**

Bad:

> **Add personalization because AI systems should personalize.**

---

# 69. FUTURE TECH STACK GOVERNANCE

A technology is added only when it serves a defined research or engineering need.

Example:

```text
ROS2
```

is justified if:

```text
robotics integration is now a research goal
```

not because:

```text
ROS2 looks good on a resume
```

---

# 70. FUTURE CLAIM DISCIPLINE

Future work sections may say:

```text
could
may
would enable
future research can examine
```

Do not describe future capabilities as if already implemented.

---

# 71. FUTURE ETHICAL REQUIREMENTS

Live neural-data research introduces stronger ethical requirements.

Future human/live EEG work must address:

```text
informed consent
privacy
data retention
neural-data sensitivity
participant withdrawal
risk minimization
human agency
```

---

# 72. FUTURE SAFETY REQUIREMENTS

Moving from simulation to hardware requires a new safety framework.

Potential requirements include:

```text
hardware emergency stop
collision prevention
fault handling
communication loss behavior
actuator limits
physical risk assessment
```

The current simulated safety controller is not sufficient for real deployment.

---

# 73. FUTURE SECURITY REQUIREMENTS

A deployed neural-control system would need:

```text
authentication
authorization
secure data transport
protected neural data
tamper resistance
audit logs
secure software updates
```

Cybersecurity is outside current core scope but would become necessary for real deployment.

---

# 74. FUTURE CLINICAL BOUNDARY

If the project ever moves toward:

- assistive neurotechnology;
- rehabilitation;
- clinical BCI;

new validation requirements would be needed.

The current project should not be presented as clinically validated.

---

# 75. FUTURE RESEARCH QUESTION FAMILY

Potential future research questions include:

```text
F-RQ1:
Can few-shot subject adaptation improve held-out-user EEG decoding?

F-RQ2:
Does hierarchical binary goal selection scale the BCI to multiple SAR objectives?

F-RQ3:
Do advanced uncertainty methods outperform posterior entropy for autonomy gating?

F-RQ4:
Can a dynamic Bayesian model reduce overconfidence from correlated EEG evidence?

F-RQ5:
How does live human confirmation affect the reliability-latency trade-off?

F-RQ6:
Does shared autonomy remain effective in a dynamic SAR environment?

F-RQ7:
Can formal safety filters reduce simulated violations without excessive task cost?

F-RQ8:
How does the framework perform when transferred from simulation to ROS2/Gazebo or hardware?
```

These questions are future possibilities, not current approved objectives.

---

# 76. FUTURE ACADEMIC POSITIONING

The project can later branch toward several research directions:

```text
Computational Neuroscience + AI
Neurotechnology / BCI
Human–AI Interaction
Shared Autonomy
Robotics + AI
Safety-Critical Intelligent Systems
Adaptive Intelligent Systems
Brain-Inspired AI
```

The current architecture deliberately supports these paths without requiring all of them now.

---

# 77. FUTURE PORTFOLIO POSITIONING

Depending on the extension chosen, the same core project can later emphasize:

## BCI / neuroscience

```text
EEG decoding
cross-subject generalization
live BCI
```

## Cognitive AI

```text
latent-goal inference
uncertainty
adaptive belief
```

## Robotics

```text
shared autonomy
ROS2
planning
simulation
```

## AI safety

```text
uncertainty gating
human authority
safety constraints
failure analysis
```

The technical truth must remain consistent across all versions.

---

# 78. CHANGE-CONTROL RULE FOR FUTURE WORK

If a future item is promoted into active scope:

```text
1. define new research / engineering objective
2. analyze consequences
3. Project Owner approves
4. record in DECISIONS.md
5. update MASTER_PROJECT_SPEC.md if constitution changes
6. update affected numbered documents
7. create Codex ticket
8. implement
9. test
10. review
```

No future-work bullet automatically becomes implementation authority.

---

# 79. COMPLETION CRITERIA FOR FUTURE-WORK PLANNING

This document is successful if:

1. current core and future scope remain separated;
2. unresolved current methodology is not mislabeled as optional;
3. live EEG and hardware are clearly future work;
4. optional technologies remain controlled;
5. future extensions are hypothesis-driven;
6. scientific value is prioritized over complexity;
7. simulation-to-real progression is clear;
8. ethical/safety requirements expand appropriately with deployment;
9. portfolio/research directions are supported without scope drift;
10. future claims remain hypothetical until implemented.

---

# 80. CURRENT FUTURE-WORK SUMMARY

The strongest future evolution of the project is not to add as many technologies as possible, but to progressively remove the current system's most important limitations. The highest-value next directions are stronger cross-subject generalization, robust calibration and uncertainty estimation, a defensible multi-goal BCI interaction protocol, bounded personalization, and more dynamic Search & Rescue evaluation. A major second stage would introduce live EEG and real human interaction, enabling genuine online shared-autonomy research. Robotics depth could then be added through ROS2/Gazebo before any physical robot is considered. Formal safety, advanced probabilistic inference, reinforcement learning, neuromorphic models, multi-agent rescue, and hardware deployment remain valuable later research directions, but only when they answer clear scientific questions. The current project should first remain focused on producing a complete, reproducible, scientifically valid EEG-to-shared-autonomy system with honest results and failure analysis.
