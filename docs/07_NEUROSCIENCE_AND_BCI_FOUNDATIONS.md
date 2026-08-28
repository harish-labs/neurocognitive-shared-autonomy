# 07_NEUROSCIENCE_AND_BCI_FOUNDATIONS.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Neuroscience, Electroencephalography, Motor Imagery, Sensorimotor Rhythms, and BCI Scientific Foundations

**Document ID:** D-02  
**Document class:** Data & Neuroscience / Scientific Foundation  
**Authority level:** Subordinate to the Master Authority Documents, Search & Rescue Scenario Specification, System Architecture, Technology Stack, and Dataset/Data Pipeline Specification  
**Status:** Authoritative scientific-foundation baseline; methodological parameters not yet approved remain explicitly unresolved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND SCIENTIFIC-CLAIM RULE

This document defines the **neuroscience and brain-computer-interface concepts that the project is allowed to rely on**.

It must remain consistent with:

1. `MASTER_PROJECT_SPEC.md`
2. `01_PROJECT_CONCEPT_AND_PROBLEM.md`
3. `02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md`
4. `03_SEARCH_AND_RESCUE_SCENARIO.md`
5. `04_SYSTEM_ARCHITECTURE.md`
6. `05_TECHNOLOGY_STACK.md`
7. `06_DATASET_AND_DATA_PIPELINE.md`

If this document conflicts with a higher-authority project document, the higher-authority document wins.

This document explains scientific foundations. It does **not** silently freeze unresolved preprocessing parameters.

In particular, this document does not independently finalize:

- the exact EEG band-pass limits;
- the exact reference scheme;
- the exact epoch interval;
- baseline correction;
- artifact-rejection thresholds;
- reduced-channel selection;
- calibration method;
- confidence thresholds;
- cross-subject split;
- or the binary EEG-to-Search-&-Rescue goal mapping.

Those decisions require their appropriate later methodology or experiment documents and, where necessary, explicit owner approval.

---

# 1. PURPOSE OF THIS DOCUMENT

This document answers:

> **What does EEG actually measure?**

> **Why can motor imagery produce decodable EEG patterns?**

> **Why are sensorimotor rhythms, CSP, and EEGNet scientifically relevant?**

> **Why are EEG predictions uncertain?**

> **What is a brain-computer interface in the context of this project?**

> **What can and cannot legitimately be inferred from the selected EEG dataset?**

The purpose is to ensure that future code, documentation, experiments, and portfolio claims use neuroscience terminology correctly and do not exaggerate what the system is doing.

---

# 2. THE NEUROSCIENCE ROLE IN THIS PROJECT

The project contains a genuine neuroscience/BCI component because it uses:

- real human EEG;
- motor-imagery trials;
- scalp-channel spatial information;
- sensorimotor neural activity;
- event/cue-related trial segmentation;
- classical EEG decoding through CSP + LDA;
- neural decoding through EEGNet / a compact CNN;
- subject variability;
- and uncertainty arising from neural-signal decoding.

However, the project is **not primarily a neuroscience experiment about discovering a new neural mechanism**.

The neuroscience role is:

```text
real neural measurement
        ↓
motor-imagery evidence
        ↓
probabilistic decoding
        ↓
uncertain human-intent signal
        ↓
shared-autonomy research
```

The main research contribution lies at the intersection of:

- EEG/BCI;
- probabilistic intent inference;
- uncertainty;
- human–AI interaction;
- autonomous planning;
- and safety.

---

# 3. WHAT EEG IS

Electroencephalography, or EEG, records **electrical potential differences measured at the scalp**.

Scalp EEG primarily reflects the summed, synchronized electrical activity of large populations of neurons, particularly postsynaptic currents in cortical neuronal populations whose geometry and synchronization make them detectable at the scalp.

EEG should not be described as directly reading individual neuron firing.

A more accurate conceptual chain is:

```text
neuronal population activity
        ↓
synchronized postsynaptic currents
        ↓
electrical fields propagate through brain / skull / scalp
        ↓
electrode voltage differences
        ↓
EEG channels
```

The signals measured at the scalp are therefore indirect, spatially mixed observations of underlying neural activity.

---

# 4. EEG IS A DIFFERENTIAL MEASUREMENT

An EEG channel does not represent an absolute brain voltage.

EEG measures potential differences relative to a reference.

This means the observed waveform depends partly on:

- electrode location;
- reference choice;
- volume conduction;
- source geometry;
- noise;
- and preprocessing.

Therefore the EEG reference strategy is scientifically meaningful.

The exact project reference scheme remains unresolved and must later be documented explicitly.

---

# 5. TEMPORAL AND SPATIAL CHARACTERISTICS OF EEG

EEG has very high temporal resolution.

Neural electrical changes can be observed on the millisecond timescale.

This makes EEG useful for studying:

- sensory processing;
- movement preparation;
- motor imagery;
- decision-related dynamics;
- and time-varying BCI signals.

However, scalp EEG has substantially weaker spatial localization than methods such as MRI-based structural imaging.

Reasons include:

- volume conduction;
- skull/scalp attenuation;
- spatial mixing;
- limited electrode sampling;
- multiple neural sources contributing to one channel.

Therefore this project must not make claims such as:

> “Channel C3 directly measures one specific group of motor neurons.”

A scalp channel reflects a spatially mixed measurement.

---

# 6. EEG CHANNELS AND ELECTRODES

The approved PhysioNet EEG Motor Movement/Imagery dataset contains **64 EEG channels**.

Multiple electrodes distributed over the scalp allow the project to observe spatial patterns associated with different motor-imagery conditions.

Motor-imagery BCI systems frequently focus on activity over central sensorimotor areas.

Electrode names commonly encountered in sensorimotor EEG include locations around:

```text
C3
Cz
C4
```

and surrounding channels.

However:

> **The project has not locked a reduced C3/Cz/C4-only channel subset.**

The initial data pipeline should preserve the available channel information unless a later channel-selection experiment is explicitly approved.

---

# 7. VOLUME CONDUCTION

Electrical activity spreads through biological tissue before reaching scalp electrodes.

This phenomenon is commonly called **volume conduction**.

Consequences include:

- one cortical source can influence several scalp channels;
- one scalp channel can contain contributions from several sources;
- neighboring EEG channels are not independent;
- raw channel amplitude should not be interpreted as a perfectly localized neural source.

This is one reason spatial-filtering approaches such as Common Spatial Patterns can be useful for motor-imagery classification.

---

# 8. EEG RHYTHMS

EEG contains activity across multiple frequency ranges.

Frequency-band names such as:

- delta;
- theta;
- alpha;
- mu;
- beta;
- gamma;

are useful descriptive conventions.

Their exact boundaries can vary across literature and individuals.

For this project, the most relevant rhythms are **sensorimotor mu and beta activity**.

---

# 9. SENSORIMOTOR MU RHYTHM

The **mu rhythm** is a sensorimotor rhythm typically observed over central sensorimotor regions.

A commonly cited approximate frequency range is:

\[
8\text{–}13\ \mathrm{Hz}
\]

Mu occupies a frequency range similar to posterior alpha activity but differs in its typical spatial distribution and functional context.

Movement, movement preparation, movement observation, and motor imagery can modulate sensorimotor mu activity.

The project should not treat the numerical 8–13 Hz range as a mandatory filter boundary.

It is a neuroscientific reference range.

Individual subjects can show different peak frequencies and broader/narrower useful bands.

---

# 10. SENSORIMOTOR BETA RHYTHM

Sensorimotor beta activity is commonly discussed in an approximate range around:

\[
13\text{–}30\ \mathrm{Hz}
\]

with exact definitions varying by study.

Motor-related beta activity often changes during movement preparation, execution, imagery, and post-movement recovery.

For this project, beta activity is relevant because motor imagery can modify oscillatory activity over sensorimotor cortex even when no physical movement is performed.

Again:

> **13–30 Hz is a broad neuroscientific reference, not the final project band-pass setting.**

---

# 11. MOTOR IMAGERY

Motor imagery is the mental simulation or rehearsal of a movement **without overtly executing that movement**.

Examples include imagining movement of:

- the left hand;
- the right hand;
- feet;
- or another body part.

Motor imagery is useful in BCI because imagined movement can modulate sensorimotor EEG activity in systematic ways.

The project's initial task is:

> **imagined left-fist movement versus imagined right-fist movement**

using PhysioNet runs:

```text
4
8
12
```

---

# 12. MOTOR EXECUTION VS MOTOR IMAGERY

The source dataset contains both:

- motor execution runs;
- motor imagery runs.

The project deliberately starts with **motor imagery**, not executed movement.

This distinction is important.

Motor execution involves actual physical movement.

Motor imagery involves internal movement representation without required overt movement.

Although motor execution and motor imagery can share related sensorimotor neural patterns, they are not identical conditions.

The project must not accidentally train on motor-execution runs while claiming motor imagery.

---

# 13. DATASET RUNS RELEVANT TO THIS PROJECT

For the approved initial task:

```text
Run 4  → Left vs Right motor imagery
Run 8  → Left vs Right motor imagery
Run 12 → Left vs Right motor imagery
```

For these runs:

```text
T1 → imagined left fist
T2 → imagined right fist
T0 → rest
```

The meaning of T1/T2 changes in other run families.

Therefore the neuroscience interpretation must always remain tied to the selected run family.

---

# 14. WHAT “LEFT” AND “RIGHT” MEAN

In this project, the classifier labels:

```text
Left
Right
```

refer to:

> **left-fist motor imagery**

and:

> **right-fist motor imagery**

They do **not** directly mean:

- move the rescue robot left;
- move the rescue robot right;
- rescue Victim A;
- rescue Victim B;
- choose safe zone;
- choose medical point.

Application semantics are introduced later through a separate goal-mapping interface.

This separation is mandatory.

---

# 15. CONTRALATERAL SENSORIMOTOR ORGANIZATION

Motor control is strongly lateralized.

Activity associated with one side of the body often has substantial representation in the opposite cerebral hemisphere.

Therefore left- and right-hand movement or motor imagery can produce distinguishable spatial patterns over sensorimotor scalp regions.

However, the project must avoid oversimplification.

Motor-imagery EEG can show:

- bilateral activity;
- subject-specific spatial patterns;
- different mu and beta topographies;
- variable lateralization strength.

The correct statement is:

> **Left- and right-hand motor imagery can produce distinguishable sensorimotor EEG patterns, often involving lateralized changes over central regions.**

Not:

> “Left imagery always activates exactly one electrode and right imagery always activates exactly the opposite electrode.”

---

# 16. EVENT-RELATED DESYNCHRONIZATION AND SYNCHRONIZATION

Two core concepts in motor-imagery EEG are:

> **Event-Related Desynchronization (ERD)**

and:

> **Event-Related Synchronization (ERS)**

These describe changes in rhythmic EEG activity relative to an event or reference period.

---

# 17. EVENT-RELATED DESYNCHRONIZATION — ERD

ERD refers to a reduction in the power/amplitude of an ongoing rhythm associated with an event.

In motor tasks and motor imagery, sensorimotor mu and beta rhythms often show ERD.

Conceptually:

```text
resting synchronized sensorimotor rhythm
        ↓
movement / motor imagery
        ↓
reduced rhythmic power
        ↓
ERD
```

ERD is frequency-specific and spatially dependent.

---

# 18. EVENT-RELATED SYNCHRONIZATION — ERS

ERS refers to an increase in rhythmic power relative to a reference period.

Motor-related beta activity can show synchronization/rebound phenomena, particularly after movement-related activity.

The project does not require a dedicated ERD/ERS quantification algorithm to be considered complete unless later approved.

However, understanding ERD/ERS is important because it explains why frequency-specific EEG features can discriminate motor-imagery conditions.

---

# 19. ERD/ERS IS NOT THE SAME AS AN ERP

An **event-related potential (ERP)** is typically studied as a signal component that is phase/time locked to an event and often revealed by averaging.

ERD/ERS concerns event-related changes in ongoing oscillatory power.

Pfurtscheller and Lopes da Silva emphasized this distinction in foundational ERD/ERS work.

For this project:

- motor-imagery decoding is primarily motivated by changes in ongoing sensorimotor rhythms;
- the project is not primarily an ERP-classification system.

---

# 20. WHY MOTOR IMAGERY CAN BE DECODED

Motor imagery creates a useful BCI signal because imagined movement changes patterns of sensorimotor neural activity.

A decoder can exploit differences in:

- spatial distribution;
- frequency content;
- temporal evolution;
- covariance structure;
- learned spatial-temporal representations.

The classifier does not “understand the thought.”

It detects statistical differences between EEG associated with the defined experimental classes.

---

# 21. EEG SIGNAL-TO-NOISE CHARACTERISTICS

Scalp EEG has low signal amplitude relative to many sources of interference.

EEG is affected by:

- ongoing unrelated neural activity;
- eye movements;
- blinking;
- facial/jaw muscle activity;
- neck/scalp muscle activity;
- body movement;
- electrode contact;
- environmental electrical interference;
- reference choice;
- session variability;
- attention;
- fatigue;
- mental strategy.

Therefore EEG classification is intrinsically uncertain.

This uncertainty is one of the reasons the project's Bayesian/shared-autonomy architecture is scientifically meaningful.

---

# 22. ARTIFACTS

An EEG artifact is recorded activity that does not represent the neural phenomenon being studied or that contaminates interpretation.

Important examples include:

## Ocular artifacts

- blinks;
- eye movements.

## Muscular artifacts

- facial tension;
- jaw activity;
- scalp/neck muscle activity.

## Movement artifacts

- cable/electrode movement;
- participant movement.

## Electrical artifacts

- line-frequency contamination;
- equipment interference.

The exact artifact-removal strategy remains unresolved.

Complex ICA-based cleaning is not mandatory unless later justified.

---

# 23. SIGNAL VARIABILITY

Motor-imagery EEG varies:

## Within one subject

Across:

- trials;
- runs;
- fatigue states;
- attention;
- motor-imagery strategy;
- time.

## Between subjects

Due to:

- anatomy;
- cortical folding;
- skull conductivity;
- imagery ability;
- neural dynamics;
- electrode contact;
- individual frequency peaks.

This variability explains why cross-subject BCI decoding is difficult.

---

# 24. BCI ILLITERACY / PERFORMANCE VARIABILITY TERMINOLOGY

BCI literature has historically used terms such as “BCI illiteracy” to describe users with poor control performance.

This project should avoid using such terminology casually.

Low decoding performance may reflect:

- task strategy;
- signal quality;
- model mismatch;
- session variability;
- individual neurophysiology;
- experimental protocol.

The project should describe observed performance directly rather than attributing failure to the participant.

---

# 25. WHY CROSS-SUBJECT EVALUATION MATTERS

A model can perform well when trained and tested on the same participant distribution yet perform worse on an unseen participant.

Therefore cross-subject evaluation tests a different and harder question:

> **Does the learned representation generalize across people?**

Cross-subject degradation is expected to be plausible and scientifically informative.

The final protocol remains unresolved, but the phenomenon is foundational to the project.

---

# 26. WHAT A BRAIN-COMPUTER INTERFACE IS

A brain-computer interface uses measured brain activity to provide information or control to an external system.

Classic BCI work defines BCIs around translating brain signals into commands or communication without relying solely on conventional peripheral motor output.

In this project, the conceptual BCI path is:

```text
motor-imagery EEG
        ↓
decoder
        ↓
probabilistic Left/Right evidence
        ↓
goal-selection interface
        ↓
shared autonomous system
```

However, this project uses **prerecorded EEG**.

Therefore it is an:

> **offline BCI research prototype**

with:

> **simulated real-time EEG replay**

rather than a live online BCI.

---

# 27. OFFLINE VS ONLINE BCI

## Offline BCI

Uses prerecorded data for:

- model development;
- evaluation;
- replay;
- controlled experiments.

This project is currently offline.

## Online BCI

Would involve:

- live EEG acquisition;
- real-time preprocessing;
- real-time inference;
- user feedback during acquisition;
- hardware latency;
- session adaptation.

Those conditions are not part of the current core system.

---

# 28. OPEN-LOOP VS CLOSED-LOOP CONSIDERATIONS

A live BCI often forms a closed loop:

```text
brain activity
→ system response
→ user perceives response
→ future brain activity changes
```

The current dataset was not recorded while participants controlled this Search & Rescue simulator.

Therefore the integrated project does **not** represent a genuine live neuroadaptive closed-loop experiment.

The project simulates the downstream control loop using prerecorded EEG evidence.

This limitation must be preserved in the final report.

---

# 29. WHY THIS IS STILL A VALID BCI RESEARCH PROTOTYPE

Using prerecorded EEG remains scientifically useful for the project's objective because it allows controlled investigation of:

- neural decoding;
- probability quality;
- Bayesian evidence accumulation;
- uncertainty-aware decision policies;
- shared-autonomy logic;
- safety;
- robustness;
- system-level trade-offs.

It allows the research question to be investigated without requiring:

- EEG hardware;
- participant recruitment;
- ethics approval for new EEG acquisition;
- or physical robotics.

But offline results cannot automatically be generalized to a live BCI deployment.

---

# 30. BCI PIPELINE

The project's neural interface follows the standard conceptual stages:

```text
Brain activity
        ↓
EEG measurement
        ↓
signal preprocessing
        ↓
feature/representation learning
        ↓
classification
        ↓
probability output
        ↓
application command interpretation
```

This project extends the usual pipeline by adding:

```text
calibration
→ Bayesian evidence accumulation
→ uncertainty
→ shared autonomy
→ safety
```

That extension is central to the project.

---

# 31. EVENTS AND ANNOTATIONS

The continuous EEG includes annotations indicating task events.

For the selected runs:

```text
T0 = rest
T1 = left-fist motor imagery
T2 = right-fist motor imagery
```

Events allow continuous EEG to be segmented into task-related trials.

The event onset is not itself the neural signal.

It is the experimental marker used to define the temporal relationship between cue/task and EEG activity.

---

# 32. EPOCHS

An EEG epoch is a segment of continuous EEG extracted around an event.

Conceptually:

\[
X_i \in \mathbb{R}^{C \times T}
\]

where:

- \(C\) = channels;
- \(T\) = time samples;
- \(i\) = trial/epoch.

Epoching converts continuous EEG into trial-level observations suitable for:

- CSP;
- LDA;
- EEGNet;
- visualization;
- evaluation.

The exact epoch interval remains unresolved.

---

# 33. WHY EPOCH TIMING MATTERS

Motor-imagery neural dynamics evolve over time after the cue.

An epoch chosen:

- too early;
- too late;
- too broadly;
- or inconsistently

may include less relevant activity or distort evaluation.

Official MNE examples demonstrate that cue-relative timing matters.

However, those example intervals are not automatically the project's final values.

The final timing must be scientifically justified in the EEG Signal Processing & ML document.

---

# 34. FREQUENCY FILTERING

Band-pass filtering can emphasize frequency ranges relevant to sensorimotor rhythms.

For motor imagery, literature frequently studies mu/beta ranges.

Official MNE CSP examples demonstrate one band-pass configuration around the sensorimotor range.

However:

> **The project's exact filter is not yet locked.**

A filter such as:

```text
7–30 Hz
```

is a reference example, not an authority decision.

The final band should be selected and documented before final experiments.

---

# 35. WHY OVERFILTERING IS A RISK

Filtering too aggressively can:

- remove informative activity;
- distort temporal structure;
- introduce edge artifacts;
- produce preprocessing-specific results that fail to generalize.

Therefore filter choices should be:

- scientifically motivated;
- consistent;
- recorded;
- validated.

The project should not tune filter bands repeatedly on the final test set.

---

# 36. COMMON SPATIAL PATTERNS — CSP

Common Spatial Patterns is a classical spatial-filtering method widely used in two-class motor-imagery EEG decoding.

CSP seeks spatial projections whose signal variance differs strongly between two classes.

Conceptually:

```text
multichannel EEG
        ↓
spatial filters
        ↓
class-discriminative variance features
```

For Left-vs-Right motor imagery, CSP can exploit spatial covariance differences across scalp channels.

---

# 37. CSP IS SUPERVISED

CSP uses class labels to derive spatial filters.

Therefore:

> **CSP must be fitted only on the training data.**

Fitting CSP on the full dataset before cross-validation or test splitting would introduce leakage.

This is a scientific requirement, not only a software-engineering preference.

---

# 38. INTERPRETING CSP PATTERNS

CSP spatial filters/patterns can provide useful information about discriminative channel structure.

However, CSP components should not automatically be interpreted as exact anatomical neural sources.

They are mathematical spatial projections optimized for discrimination.

The project may inspect CSP patterns, but should describe them cautiously.

---

# 39. LINEAR DISCRIMINANT ANALYSIS — LDA

LDA is the approved classical classifier paired with CSP.

Conceptually:

```text
EEG epochs
→ CSP features
→ LDA
→ class probability / prediction
```

This combination provides:

- an established baseline;
- relatively low complexity;
- interpretable experimental comparison;
- a benchmark against the neural EEGNet model.

The project is not strengthened by skipping the classical baseline.

---

# 40. EEGNET

EEGNet is a compact convolutional neural-network architecture designed for EEG-based BCI applications.

The foundational EEGNet work introduced a compact architecture using operations designed to learn temporal and spatial EEG representations efficiently.

For this project, EEGNet provides the neural-decoding comparison against:

```text
CSP + LDA
```

The project uses EEGNet because it is appropriately matched to EEG rather than because deep learning is assumed to outperform classical methods.

---

# 41. EEGNET IS NOT GUARANTEED TO WIN

The project must allow outcomes such as:

```text
CSP+LDA > EEGNet
CSP+LDA ≈ EEGNet
EEGNet > CSP+LDA
```

depending on:

- subject;
- split;
- preprocessing;
- training data;
- evaluation metric.

A classical model outperforming the neural decoder would still be a valid result.

---

# 42. CLASS PROBABILITIES

The EEG decoder outputs a probability-like vector such as:

\[
P(L \mid EEG), P(R \mid EEG)
\]

These values quantify the model's class belief.

They do **not** directly represent:

- probability that the human truly wants Victim A;
- probability that the rescue mission is safe;
- probability that the model is objectively correct.

That distinction motivates:

- calibration;
- Bayesian goal inference;
- uncertainty-aware control.

---

# 43. PREDICTIVE CONFIDENCE IS NOT CERTAINTY

A model output:

```text
0.95 Left
0.05 Right
```

does not mean:

> “There is a guaranteed 95% probability the human's real-world intention is the mapped rescue goal.”

It means the model assigned high probability to the Left motor-imagery class under its learned representation.

Calibration must evaluate whether probability magnitudes correspond meaningfully to empirical correctness.

---

# 44. WHY CALIBRATION MATTERS IN A BCI

In a normal classifier, a wrong high-confidence prediction is undesirable.

In an autonomy system, it can be more serious because confidence influences action.

Therefore the project asks not only:

> “Which class is predicted?”

but:

> “Can the system trust the magnitude of that probability enough to decide how much autonomy to assume?”

This is the scientific bridge from neural decoding to uncertainty-aware shared autonomy.

---

# 45. BAYESIAN GOAL INFERENCE IS A SYSTEM MODEL

The Bayesian layer does not claim to model the biological brain's internal Bayesian computation.

It is an **engineering/probabilistic model of the system's belief about human intention**.

Core form:

\[
P(G \mid E_{1:t})
\propto
P(E_t \mid G)P(G \mid E_{1:t-1})
\]

where:

- \(G\) = goal/intention hypothesis;
- \(E_t\) = incoming EEG-derived evidence.

This model accumulates uncertain evidence over time.

---

# 46. LATENT INTENTION

The human's intended goal is treated as a latent variable:

> It exists conceptually but is not directly observed by the autonomous system.

EEG provides imperfect evidence about it.

The system therefore maintains a probability distribution rather than assuming certainty.

This is more scientifically defensible than:

```text
one EEG trial
→ one unquestioned rescue command
```

---

# 47. UNCERTAINTY

The approved initial uncertainty measure is entropy:

\[
H(P)=-\sum_i p_i\log p_i
\]

A concentrated posterior has relatively low uncertainty.

A more uniform posterior has relatively high uncertainty.

The system uses uncertainty to decide whether autonomous assistance is justified.

Exact thresholds remain unresolved.

---

# 48. NEURAL UNCERTAINTY VS SYSTEM UNCERTAINTY

The phrase “EEG uncertainty” can refer to several different things.

The project should distinguish:

## Signal variability

Noise/variability in measured EEG.

## Model predictive uncertainty

Ambiguity in decoder output.

## Calibration quality

Whether probability magnitude reflects empirical reliability.

## Goal-belief uncertainty

Uncertainty in the Bayesian posterior over candidate intentions.

## Environmental uncertainty

Uncertainty associated with planning/hazard state.

These are not identical.

The final system should avoid collapsing them into one undefined “uncertainty score.”

---

# 49. SHARED AUTONOMY FROM A BCI PERSPECTIVE

Direct low-level BCI control can require frequent reliable neural commands.

That is difficult when EEG decoding is noisy.

The project instead uses **goal-level shared autonomy**:

```text
Human neural evidence
→ intended objective

Autonomous system
→ safe route execution
```

This reduces the requirement for EEG to specify every movement.

---

# 50. WHY EEG IS NOT USED AS A JOYSTICK

The selected motor-imagery task is binary and uncertain.

Using each Left/Right prediction to command:

```text
turn left
turn right
```

would make the system highly sensitive to individual classification errors.

Instead, the project uses neural evidence to infer a higher-level choice/goal.

Autonomy then handles navigation.

This design is central to the project's scientific rationale.

---

# 51. THE BINARY-MAPPING PROBLEM

The dataset gives:

```text
Left MI
Right MI
```

The Search & Rescue environment may contain:

- Victim A;
- Victim B;
- safe zone;
- medical resource;
- other goals.

These meanings are not present in the EEG dataset.

Therefore the system requires an explicit BCI interaction protocol.

Current unresolved possibilities remain:

1. two active choices at a time;
2. hierarchical/sequential binary selection;
3. abstract binary priority choice;
4. future multiclass EEG.

No option is approved here.

---

# 52. WHY THE MAPPING IS AN INTERFACE, NOT A NEUROSCIENCE CLAIM

Suppose a future interface maps:

```text
Left MI → option A
Right MI → option B
```

This does not mean the brain naturally encodes:

```text
Left MI = Victim A
```

The mapping is an **artificial BCI control convention**.

The scientifically correct chain is:

```text
participant performs Left MI
→ EEG decoder estimates Left class
→ interface interprets Left as current option A
```

This distinction must remain explicit in final documentation.

---

# 53. HUMAN AGENCY

The project's BCI design preserves human authority through:

- confirmation;
- override;
- pause;
- emergency stop.

This matters because EEG prediction is probabilistic and can be wrong.

Shared autonomy should not turn uncertain neural evidence into irreversible machine decisions.

---

# 54. SAFETY AND NEUROTECHNOLOGY

The project uses a safety-relevant scenario because errors from human-machine interfaces can have consequences in autonomous systems.

However, the project only demonstrates **simulated safety mechanisms**.

It does not demonstrate:

- certified BCI safety;
- clinical-grade neurotechnology;
- safety of a physical rescue robot;
- deployment readiness.

The scientific claim is limited to measurable safety behaviour in the simulation.

---

# 55. MOTOR IMAGERY PERFORMANCE IS USER-DEPENDENT

Motor-imagery decoding can vary substantially between people.

This can arise from both:

- neurophysiological differences;
- experimental/technical conditions.

Therefore subject-wise analysis is important.

The project should not treat one individual's high accuracy as representative of the entire dataset.

---

# 56. TRAINING EFFECTS AND USER ADAPTATION

In live BCI research, users may learn mental strategies over repeated sessions and systems may adapt to users.

The current project does not directly measure long-term human BCI learning because it uses prerecorded data.

Therefore the project's planned “adaptation” primarily refers to **system-side adaptation based on interaction/corrections** unless the scope later changes.

This distinction prevents overclaiming neuroplastic or human-learning effects.

---

# 57. WHAT “ADAPTIVE” MAY MEAN HERE

Potential project adaptation mechanisms include:

- modifying priors;
- estimating user-specific reliability;
- modifying evidence weights;
- adjusting confidence thresholds.

These are computational adaptation mechanisms.

They do not automatically mean:

- adaptive control theory;
- neural plasticity;
- co-adaptive live BCI learning.

The final wording must match what is actually implemented.

---

# 58. MOTOR CORTEX TERMINOLOGY

The project may refer broadly to:

- motor cortex;
- sensorimotor cortex;
- central sensorimotor scalp regions;
- motor-related neural activity.

It should avoid overly precise source-localization claims unless source reconstruction is actually performed.

No source-localization method is currently part of the project.

---

# 59. SOURCE LOCALIZATION — OUT OF SCOPE

The project does not currently require:

- MRI;
- forward head models;
- inverse solutions;
- cortical source reconstruction;
- dipole fitting.

Scalp EEG decoding is sufficient for the research question.

Therefore:

> **sensor-level EEG classification**

is the appropriate description.

---

# 60. NEUROANATOMICAL OVERCLAIMING — PROHIBITED

Do not write statements such as:

> “The model identified activation of the left primary motor cortex.”

unless the implemented analysis actually supports source-level localization.

Safer wording:

> “The EEG exhibited discriminative sensorimotor scalp patterns associated with Left- and Right-hand motor imagery.”

---

# 61. ERD/ERS ANALYSIS STATUS

Understanding ERD/ERS is part of the scientific foundation.

A dedicated ERD/ERS quantitative analysis is **not currently a mandatory project module**.

Potentially useful exploratory analysis could include:

- class-specific spectral power;
- scalp topography;
- time-frequency visualization.

But such analysis should not become required unless approved.

---

# 62. PSD ROLE

Power Spectral Density (PSD) can help inspect the distribution of EEG power across frequency.

PSD is useful for:

- quality inspection;
- understanding signal bands;
- detecting obvious electrical contamination;
- validating preprocessing effects.

PSD alone does not perform motor-imagery decoding.

---

# 63. TIME-FREQUENCY ANALYSIS STATUS

Time-frequency analysis may help visualize how motor-related spectral power evolves after cues.

However, a complex time-frequency pipeline is not currently required for the core system.

It may be used for neuroscience interpretation if implementation time permits and if it improves scientific understanding.

---

# 64. ARTIFACT REMOVAL SHOULD NOT BECOME SCOPE CREEP

EEG preprocessing can become extremely complex.

The project should not add:

- ICA;
- automated artifact classifiers;
- source separation;
- bad-channel interpolation pipelines;

merely to appear neuroscientifically sophisticated.

Any artifact-handling component should solve an observed problem and be validated.

---

# 65. PREPROCESSING SHOULD PRESERVE EXPERIMENTAL VALIDITY

Whatever preprocessing is eventually selected must satisfy:

- reproducibility;
- no test leakage;
- no hidden manual trial selection;
- traceable exclusions;
- consistent processing across compared models;
- correct cue/event semantics.

The best-looking waveform is not necessarily the scientifically correct pipeline.

---

# 66. WHY THE CLASSICAL BASELINE IS SCIENTIFICALLY IMPORTANT

A neural network can look impressive without demonstrating necessity.

CSP + LDA provides a strong reference because motor-imagery BCI has historically used spatial-filtering and linear classification successfully.

Therefore comparing EEGNet against CSP + LDA asks:

> **Does the additional neural-model complexity provide meaningful value on our selected data and evaluation protocol?**

This makes the ML portion scientifically stronger.

---

# 67. WHY PROBABILITY OUTPUTS MATTER MORE THAN ONLY ACCURACY

For the downstream architecture, the EEG model does not only answer:

```text
Left or Right?
```

It also supplies evidence magnitude.

Two trials could both predict Left:

```text
Trial A: 0.51 Left / 0.49 Right
Trial B: 0.95 Left / 0.05 Right
```

A shared-autonomy system should not necessarily treat them identically.

That is why:

- probability calibration;
- uncertainty;
- Bayesian accumulation

are essential.

---

# 68. WHY SEQUENTIAL EVIDENCE CAN HELP

A single EEG trial can be wrong.

Multiple independent or partially informative observations may provide stronger evidence.

Conceptually:

```text
weak Left evidence
+ weak Left evidence
+ stronger Left evidence
→ posterior increasingly favors Left
```

Sequential Bayesian inference formalizes this accumulation.

However, repeated evidence is not automatically independent.

The mathematical assumptions must be documented in the Bayesian Goal Inference document.

---

# 69. DECISION LATENCY TRADE-OFF

Accumulating more neural evidence can improve confidence but delay action.

This creates a meaningful trade-off:

\[
\text{fast decision}
\leftrightarrow
\text{reliable decision}
\]

The project should measure:

- decision latency;
- wrong commitment;
- deferral;
- task performance.

A slower but safer system may be preferable under some conditions.

The experiment should determine the trade-off rather than assume it.

---

# 70. CALIBRATION TRADE-OFF

Calibration can improve the meaning of probabilities without necessarily increasing classification accuracy.

Therefore:

```text
accuracy
```

and:

```text
calibration
```

must be evaluated separately.

A model with slightly lower accuracy but better-calibrated confidence may be more useful for uncertainty-aware autonomy.

This is a legitimate possible research finding.

---

# 71. BCI PERFORMANCE METRICS

The EEG component should support metrics such as:

- accuracy;
- balanced accuracy;
- F1;
- confusion matrix;
- subject-wise performance;
- cross-subject performance;
- calibration measures.

The final metrics document will formalize definitions.

EEG decoding metrics must remain distinct from Search & Rescue task metrics.

---

# 72. SYSTEM-LEVEL METRICS ARE NOT EEG METRICS

The following are system-level measures:

- wrong-goal rate;
- mission success;
- safety violation;
- human intervention;
- path efficiency;
- completion time.

A model can have good EEG accuracy but poor system-level safety if confidence handling is bad.

Conversely, shared autonomy may reduce dangerous outcomes even when raw EEG classification remains imperfect.

That separation is central to the project.

---

# 73. NO THOUGHT-READING CLAIM

The project does **not** decode arbitrary thought content.

It classifies a predefined motor-imagery task.

Allowed:

> “The model decodes Left- versus Right-hand motor imagery from EEG.”

Not allowed:

> “The AI knows what the user is thinking.”

Not allowed:

> “The system reads rescue intentions directly from the brain.”

The rescue intent is represented through a designed BCI interaction protocol.

---

# 74. NO MEDICAL DIAGNOSIS CLAIM

The project does not:

- diagnose neurological disorders;
- assess brain health;
- predict disease;
- provide clinical recommendations.

It uses EEG as a control/research signal.

---

# 75. NO NEUROPROSTHETIC DEPLOYMENT CLAIM

Although similar BCI principles can be used in neuroprosthetics or assistive technologies, this project is a simulation-based research prototype.

It must not claim:

- prosthetic control validation;
- rehabilitation efficacy;
- therapeutic benefit.

---

# 76. NO REAL SEARCH-AND-RESCUE VALIDATION CLAIM

The environment is simulated.

The project does not prove that:

- firefighters;
- emergency responders;
- disabled operators;
- astronauts;
- or rescue teams

could safely use the system in practice.

Those would require new experimental evidence.

---

# 77. SCIENTIFIC TERMINOLOGY — APPROVED

The project may accurately use:

- electroencephalography / EEG;
- scalp EEG;
- motor imagery;
- motor-imagery BCI;
- sensorimotor rhythm;
- mu rhythm;
- beta rhythm;
- ERD/ERS;
- EEG epoch;
- EEG channel;
- CSP;
- LDA;
- EEGNet;
- neural decoding;
- probability calibration;
- Bayesian goal inference;
- uncertainty;
- shared autonomy;
- offline EEG replay;
- simulated real-time BCI.

---

# 78. TERMINOLOGY REQUIRING CARE

## “Neural intent”

Acceptable when clearly referring to:

> EEG-derived evidence associated with a predefined motor-imagery control intention.

It must not imply arbitrary mental-state decoding.

## “Cognitive”

Acceptable because the system models latent intention, belief, uncertainty, evidence accumulation, and human decision authority.

It must not imply a comprehensive cognitive architecture.

## “NeuroCognitive”

Acceptable because the project combines:

- neural EEG evidence;
- computational intent/belief modelling.

## “Brain-controlled”

Use cautiously.

Prefer:

> EEG-based goal-level control

or:

> motor-imagery BCI input

because the system is shared autonomy, not complete direct brain control.

---

# 79. NEUROSCIENCE FOUNDATION FOR THE PROJECT TITLE

The term:

> **NeuroCognitive Shared Autonomy**

is justified only if the final implementation includes:

## Neuro

- real EEG;
- motor imagery;
- neural decoding.

## Cognitive

- latent intention;
- Bayesian belief update;
- uncertainty;
- evidence accumulation;
- adaptation where implemented.

## Shared Autonomy

- human goal authority;
- machine route/execution responsibility;
- confirmation/override;
- safety.

If any of these components is removed through a future approved scope change, terminology should be reassessed.

---

# 80. WHY THIS PROJECT IS MORE THAN AN EEG CLASSIFIER

A normal EEG classification project may end at:

```text
EEG
→ classifier
→ Left / Right accuracy
```

This project continues:

```text
EEG
→ classifier probabilities
→ calibration
→ Bayesian intent inference
→ uncertainty
→ autonomy decision
→ human confirmation / deferral
→ planning
→ safety
→ task outcome
```

Therefore it studies the consequences of uncertain neural decoding in an intelligent autonomous system.

---

# 81. NEUROSCIENCE ASSUMPTIONS USED BY THE PROJECT

The project currently assumes:

1. Left- and Right-hand motor imagery can produce statistically distinguishable EEG patterns.
2. Sensorimotor spatial/frequency patterns provide useful decoding information.
3. Individual EEG trials remain noisy and uncertain.
4. Decoder performance varies across subjects.
5. Classifier probabilities require empirical evaluation before being trusted as confidence.
6. Multiple pieces of evidence can be accumulated probabilistically.
7. Offline prerecorded EEG is sufficient for an initial system-level research prototype.
8. Motor-imagery labels do not inherently encode Search & Rescue semantics.

These assumptions are consistent with established BCI research, but their practical consequences must still be evaluated on the selected data and implementation.

---

# 82. NEUROSCIENCE QUESTIONS THIS PROJECT DOES NOT ANSWER

The project is not designed to determine:

- where human intention is generated in the brain;
- how consciousness produces decisions;
- whether the brain itself performs Bayesian inference;
- the exact neural source of each EEG component;
- mechanisms of neuroplasticity;
- clinical motor rehabilitation outcomes;
- detailed cortical connectivity;
- neural coding of rescue decisions.

Those would require different experimental designs and often additional measurement modalities.

---

# 83. UNRESOLVED NEUROSCIENCE / PREPROCESSING DECISIONS

The following remain open.

## 83.1 Exact band-pass range

Mu/beta science motivates a sensorimotor-focused range, but exact cutoffs are not locked.

## 83.2 EEG referencing

Not locked.

## 83.3 Epoch timing

Not locked.

## 83.4 Baseline correction

Not locked.

## 83.5 Artifact-removal method

Not locked.

## 83.6 Channel reduction

Not locked.

## 83.7 Resampling

Not locked.

## 83.8 Dedicated ERD/ERS analysis

Scientifically useful but not currently mandatory.

## 83.9 Exact cross-subject protocol

Required direction but not locked.

These must remain unresolved until the later methodology documents approve them.

---

# 84. SCIENTIFIC VALIDATION CHECKLIST

Before the EEG pipeline is considered scientifically credible, verify:

- correct dataset;
- correct run family;
- correct T1/T2 semantics;
- correct channel names;
- plausible montage;
- correct sampling rate;
- correct event timing;
- correct epoch labels;
- no train/test leakage;
- representative raw EEG inspected;
- representative spectral behavior inspected;
- CSP fitted only on training data;
- EEGNet evaluated on valid splits;
- class ordering preserved;
- probability output verified;
- subject variability reported;
- limitations documented.

---

# 85. MANUAL LEARNING CHECKLIST FOR PROJECT OWNERSHIP

After implementation, the project owner should be able to explain:

## EEG

- what scalp EEG measures;
- why it is indirect;
- why EEG has high temporal but limited spatial resolution.

## Motor imagery

- what motor imagery means;
- why it affects sensorimotor rhythms;
- why Left/Right imagery can be classified.

## Frequency activity

- what mu and beta rhythms are;
- what ERD and ERS mean.

## Data

- what runs 4/8/12 represent;
- what T0/T1/T2 mean.

## Models

- what CSP does;
- why LDA is a baseline;
- what EEGNet adds.

## Uncertainty

- why classifier confidence is not certainty;
- why calibration matters;
- why Bayesian accumulation is used.

## BCI

- why this is offline replay;
- why it is not thought reading;
- why Left/Right labels require an external rescue-goal mapping.

This understanding is required for credible technical interviews, reports, and master's applications.

---

# 86. RELATIONSHIP TO THE NEXT ML METHODOLOGY DOCUMENT

This neuroscience document explains **why** the signal-processing and ML pipeline exists.

The next EEG methodology document must translate these foundations into concrete implementation choices.

It will need to specify:

- preprocessing sequence;
- filter design;
- epoch window;
- reference;
- artifact policy;
- CSP configuration;
- LDA configuration;
- EEGNet architecture;
- training protocol;
- model probability extraction;
- evaluation;
- cross-subject handling;
- and baseline comparison.

It must not contradict the neuroscience limitations documented here.

---

# 87. FOUNDATIONAL SCIENTIFIC REFERENCES

The final literature review will formalize the complete bibliography.

The following works form part of the scientific foundation for this project.

## Pfurtscheller & Lopes da Silva — ERD/ERS

**Pfurtscheller, G., & Lopes da Silva, F. H. (1999). Event-related EEG/MEG synchronization and desynchronization: basic principles. Clinical Neurophysiology, 110(11), 1842–1857.**

Relevant to:

- ERD;
- ERS;
- frequency-specific event-related oscillatory changes.

---

## Wolpaw et al. — BCI foundations

**Wolpaw, J. R., Birbaumer, N., McFarland, D. J., Pfurtscheller, G., & Vaughan, T. M. (2002). Brain–computer interfaces for communication and control. Clinical Neurophysiology, 113(6), 767–791.**

Relevant to:

- BCI definition;
- brain-signal-based communication/control;
- sensorimotor BCI foundations.

---

## Schalk et al. — BCI2000

**Schalk, G., McFarland, D. J., Hinterberger, T., Birbaumer, N., & Wolpaw, J. R. (2004). BCI2000: A General-Purpose Brain-Computer Interface (BCI) System. IEEE Transactions on Biomedical Engineering, 51(6), 1034–1043.**

Relevant to:

- the BCI2000 system;
- source experimental infrastructure associated with EEGBCI.

---

## Lawhern et al. — EEGNet

**Lawhern, V. J., Solon, A. J., Waytowich, N. R., Gordon, S. M., Hung, C. P., & Lance, B. J. (2018). EEGNet: a compact convolutional neural network for EEG-based brain–computer interfaces. Journal of Neural Engineering, 15(5), 056013.**

Relevant to:

- compact convolutional EEG decoding;
- EEGNet architecture.

---

## Motor-imagery mu/beta evidence

Classical and later motor-imagery literature provides evidence that movement and imagined movement modulate sensorimotor mu/beta rhythms and that these signals can be used for BCI decoding.

The final literature document should select and cite the exact foundational motor-imagery/CSP papers used in the technical report rather than expanding this preliminary list without verification.

---

# 88. VERIFIED REFERENCE CONTEXT USED FOR THIS DOCUMENT

The scientific statements in this document were cross-checked against:

- the foundational Pfurtscheller & Lopes da Silva ERD/ERS review;
- the Wolpaw et al. BCI review;
- the EEGNet paper by Lawhern et al.;
- established motor-imagery mu/beta EEG literature;
- the official MNE motor-imagery CSP example;
- and the already approved PhysioNet EEGBCI dataset specification.

Important distinction:

> Settings shown in an MNE example are **methodological examples**, not automatically project methodology.

This document uses the scientific literature to establish concepts while deliberately preserving all project-specific unresolved parameters.

---

# 89. CURRENT NEUROSCIENCE FOUNDATION SUMMARY

The project's neural interface is based on **scalp EEG recorded during predefined motor imagery**. EEG provides temporally precise but spatially mixed measurements of synchronized cortical population activity and is sensitive to noise, artifacts, individual anatomy, task strategy, and session variability. Left- and Right-hand motor imagery can produce distinguishable sensorimotor EEG patterns, including changes in mu- and beta-range rhythmic activity commonly described through ERD/ERS. The project uses real prerecorded EEG from PhysioNet runs 4, 8, and 12, where T1 represents Left-fist imagery and T2 represents Right-fist imagery. CSP + LDA provides the classical spatial-pattern baseline, while EEGNet provides a compact neural decoder. Decoder probabilities are not treated as certainty; they are evaluated for calibration, accumulated through a separate Bayesian intent model, and converted into uncertainty-aware shared-autonomy decisions. The neural labels themselves do not contain Search & Rescue semantics, so any mapping from Left/Right motor imagery to rescue objectives must occur through an explicitly designed BCI interaction protocol. The project uses offline EEG replay and must not claim live brain control, unrestricted thought reading, clinical neuroscience, or real-world rescue validation.

---

# 90. NEXT DOCUMENT

The next planned document is:

**`08_EEG_SIGNAL_PROCESSING_AND_ML.md` — EEG Signal Processing & Machine Learning Methodology**

That document should define the implementation-level EEG methodology, including:

- final preprocessing order;
- filter configuration once approved;
- reference configuration once approved;
- event extraction;
- epoch interval once approved;
- T0 handling;
- artifact policy;
- CSP feature extraction;
- LDA baseline;
- EEGNet architecture;
- training procedure;
- validation;
- probability outputs;
- model comparison;
- subject-wise/cross-subject evaluation boundaries;
- leakage prevention;
- model persistence;
- and reproducibility.

Any currently unresolved preprocessing choice must remain marked unresolved until explicitly approved.
