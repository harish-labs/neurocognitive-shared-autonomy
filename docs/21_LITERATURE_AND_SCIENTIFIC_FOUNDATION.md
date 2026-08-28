# 21_LITERATURE_AND_SCIENTIFIC_FOUNDATION.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Literature Review, Scientific Foundations, Key References, and Evidence Map

**Document ID:** J-02  
**Document class:** Scientific Foundation / Literature & Evidence  
**Authority level:** Subordinate to all Master Authority, Scenario, Architecture, Data, Neuroscience, ML, Bayesian, Shared-Autonomy, Planning, Safety, Implementation, Experimental Design, Metrics, Testing, and Limitations documents  
**Status:** Authoritative literature baseline for the current project; not a systematic review and not a substitute for final citation checking before publication  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. PURPOSE AND SCOPE

This document establishes the scientific foundation for the project's main components:

1. scalp EEG and brain-computer interfaces;
2. motor imagery and sensorimotor rhythms;
3. the PhysioNet EEG Motor Movement/Imagery dataset;
4. Common Spatial Patterns;
5. Linear Discriminant Analysis and classical EEG classification;
6. EEGNet / compact convolutional EEG decoding;
7. probability calibration;
8. Bayesian latent-goal inference;
9. uncertainty-aware shared autonomy;
10. BCI/shared-control interaction;
11. system-side adaptation and personalization;
12. A* planning;
13. safety-constrained simulated autonomy.

The purpose is to answer:

> **Which parts of the project are grounded in established literature, which parts are project-specific engineering choices, and which parts remain open research decisions?**

This is a focused evidence map, not an exhaustive literature survey.

---

# 1. LITERATURE GOVERNANCE

References in this document are grouped into three categories.

## A. Foundational references

Older work that established a concept used directly in the project.

Examples:

- event-related desynchronization/synchronization;
- BCI system architecture;
- Common Spatial Patterns;
- A*;
- Brier Score.

## B. Project-supporting references

Work that directly supports the type of system architecture selected here.

Examples:

- EEGNet;
- shared autonomy under uncertain user goals;
- BCI shared control;
- co-adaptive BCI research;
- probability calibration.

## C. Context / review references

Used to establish broader field consensus, limitations, or alternatives.

These are not automatically implementation requirements.

---

# 2. EVIDENCE MAP

| Project Component | Scientific Foundation | Representative Sources |
|---|---|---|
| EEG-based BCI | Neural activity used as a communication/control signal | Wolpaw et al. (2002); Schalk et al. (2004) |
| Motor imagery | Sensorimotor rhythm modulation and ERD/ERS | Pfurtscheller & Lopes da Silva (1999) |
| EEGMMIDB / EEGBCI | Public BCI2000 motor execution/imagery recordings | Schalk et al. (2004); Goldberger et al. (2000); MNE EEGBCI documentation |
| CSP | Supervised spatial filtering for two-condition EEG discrimination | Müller-Gerking et al. (1999); Blankertz et al. (2008) |
| LDA / classical BCI classification | Standard linear classification in EEG-BCI pipelines | Lotte et al. (2007, 2018) |
| EEGNet | Compact CNN designed for EEG-based BCIs | Lawhern et al. (2018) |
| Calibration | Confidence should reflect empirical correctness; temperature scaling is a practical neural calibration method | Brier (1950); Guo et al. (2017) |
| Bayesian goal belief | Sequential probabilistic belief over uncertain latent goals | Bayes rule; shared-autonomy goal inference literature |
| Shared autonomy | Human intent + autonomous assistance under uncertain goals | Dragan & Srinivasa (2013); Javdani et al. (2015) |
| BCI shared control | Low-bandwidth/noisy BCI commands benefit from context-aware autonomy | Millán et al. (2010) |
| Personalization/adaptation | BCI performance can benefit from system/user-specific adaptation | Vidaurre et al. (2011); Acqualagna et al. (2016) |
| A* planning | Heuristic minimum-cost graph search | Hart, Nilsson & Raphael (1968) |
| Simulated safety layer | Explicit action constraints and supervisory rejection | Project engineering choice grounded in safety-aware autonomy principles |

---

# 3. BRAIN-COMPUTER INTERFACE FOUNDATION

A brain-computer interface uses measurable neural activity as an input channel for communication or control.

Wolpaw and colleagues' influential BCI overview described BCIs as systems that provide a new communication/control pathway using brain activity rather than conventional peripheral nerves and muscles [R1].

BCI2000 later provided a general-purpose architecture for acquiring, processing, translating, and using brain signals in BCI experiments [R2].

These works support the project's high-level structure:

```text
brain signal
→ signal processing
→ feature / model inference
→ control output
```

The current project extends this idea with:

```text
uncertainty
→ Bayesian goal belief
→ shared autonomy
→ autonomous execution
```

---

# 4. MOTOR IMAGERY AND SENSORIMOTOR RHYTHMS

Motor imagery refers to mentally simulating a movement without physically performing it.

A major neuroscientific basis for motor-imagery BCI is the modulation of sensorimotor rhythms, commonly discussed using:

```text
event-related desynchronization (ERD)
event-related synchronization (ERS)
```

Pfurtscheller and Lopes da Silva's foundational review describes ERD/ERS as changes in rhythmic EEG activity associated with cortical activation and deactivation processes [R3].

This provides the scientific basis for using imagined left- and right-hand movement as discriminable EEG conditions.

---

# 5. MU AND BETA RHYTHMS

Motor-imagery BCI research frequently focuses on sensorimotor activity in approximately:

```text
mu / alpha-range activity
beta-range activity
```

The project's neuroscience document uses approximate reference ranges such as:

```text
mu ≈ 8–13 Hz
beta ≈ 13–30 Hz
```

These are neuroscientific reference ranges.

They do **not** automatically define the project's final preprocessing filter.

The actual filter must still be selected and documented separately.

---

# 6. CONTRALATERAL MOTOR ORGANIZATION

Left- and right-hand motor imagery can produce spatially different sensorimotor activity because cortical motor organization is substantially contralateral.

This motivates:

- spatial filtering;
- sensorimotor channel information;
- CSP-based discrimination.

However, scalp EEG reflects volume-conducted mixtures rather than isolated cortical sources.

Therefore the project does not claim precise source localization.

---

# 7. PHYSIONET EEG MOTOR MOVEMENT / IMAGERY DATASET

The project uses the public EEG Motor Movement/Imagery database distributed through PhysioNet and accessible through MNE-Python's `eegbci` utilities.

The MNE EEGBCI documentation associates the dataset with BCI2000 and PhysioNet and documents subjects 1–109 and the experimental run structure [R4].

The run mapping relevant to this project is:

```text
4, 8, 12
→ Motor imagery: left vs right hand
```

The dataset contains:

- 109 subjects;
- 64 EEG channels;
- 14 runs per subject;
- 160 Hz sampling;
- EDF/EDF+ recordings.

The project uses only the approved motor-imagery subset initially.

---

# 8. DATASET SOURCE REFERENCES

Two foundational sources support the dataset provenance.

## BCI2000

Schalk et al. described BCI2000 as a general-purpose BCI research system [R2].

## PhysioNet

Goldberger et al. introduced PhysioNet / PhysioBank as an open resource for complex physiological signals [R5].

The project should cite both the dataset platform/source and the specific EEGBCI documentation where appropriate.

---

# 9. COMMON SPATIAL PATTERNS

Common Spatial Patterns is a supervised spatial-filtering technique widely used for two-class motor-imagery EEG.

The key idea is to identify spatial projections whose variance differs strongly between two conditions.

Early work by Müller-Gerking and colleagues developed optimized spatial filters for discriminating EEG movement conditions [R6].

Blankertz et al. later provided a widely cited treatment of spatial-filter optimization and CSP-style methods for robust EEG single-trial analysis [R7].

---

# 10. WHY CSP IS A GOOD PROJECT BASELINE

CSP is appropriate here because the initial task is:

```text
binary Left vs Right motor imagery
```

and because it provides:

- a classical reference method;
- interpretable spatial filtering;
- relatively low computational complexity;
- a strong historical baseline for motor-imagery BCI.

This makes CSP+LDA scientifically more useful than using only a deep model.

---

# 11. CSP LIMITATIONS

CSP can be sensitive to:

- noise;
- covariance estimation;
- preprocessing;
- subject variability;
- overfitting with limited data.

Therefore:

- CSP must fit only on training data;
- component count/regularization must be controlled;
- performance should be assessed subject-wise.

---

# 12. LINEAR DISCRIMINANT ANALYSIS

LDA has historically been used extensively in EEG-BCI classification.

The BCI classifier reviews by Lotte et al. discuss LDA and other linear classifiers as important established approaches in EEG-based BCI systems [R8, R9].

The project's classical baseline:

```text
CSP
→ feature extraction
→ LDA
```

is therefore scientifically conventional and defensible.

---

# 13. WHY KEEP A CLASSICAL MODEL

The project must not assume deep learning is always superior.

CSP+LDA provides:

- lower complexity;
- easier debugging;
- easier leakage inspection;
- direct comparison with the BCI literature;
- potentially strong performance on limited EEG data.

If CSP+LDA outperforms EEGNet, that is a valid result.

---

# 14. EEGNET FOUNDATION

EEGNet was introduced by Lawhern et al. as a compact convolutional architecture for EEG-based BCI applications [R10].

Its design uses EEG-relevant convolutional structure while remaining substantially smaller than general-purpose deep CNNs.

This supports the project's choice to use:

```text
EEGNet / compact EEG CNN
```

instead of a much larger generic architecture.

---

# 15. EEGNET AND PROJECT TERMINOLOGY

If the final implementation closely follows the published architecture, the system may refer to it as:

> **EEGNet**

If the architecture is materially modified, safer wording is:

> **compact EEG CNN inspired by EEGNet**

The implementation must determine which wording is accurate.

---

# 16. DEEP LEARNING IS NOT THE PROJECT NOVELTY

The purpose of EEGNet here is to provide a neural decoder.

The project's stronger systems contribution is the integration of:

```text
EEG decoding
+
calibration
+
Bayesian latent-goal inference
+
uncertainty-aware shared autonomy
+
safety
```

Therefore the project should not spend unnecessary effort making EEGNet unusually complex.

---

# 17. EEG CLASSIFICATION REVIEWS

Lotte et al.'s 2007 review and 2018 ten-year update provide useful field context for EEG-BCI classification algorithms and methodological concerns [R8, R9].

These reviews support several project principles:

- no single classifier is universally optimal;
- preprocessing and feature representation matter;
- evaluation procedure matters;
- subject variability is important.

---

# 18. MOTOR-IMAGERY BCI LIMITATIONS IN THE LITERATURE

Modern reviews of motor-imagery BCI continue to identify challenges including:

- subject variability;
- calibration burden;
- online/offline differences;
- signal noise;
- limited generalization.

A comprehensive 2021 review of MI-BCI highlights such limitations and the continuing difficulty of moving systems beyond controlled laboratory conditions [R11].

This supports the project's conservative external-validity claims.

---

# 19. PROBABILITY CALIBRATION FOUNDATION

A classifier can be accurate while producing unreliable confidence values.

The project therefore separates:

```text
prediction correctness
```

from:

```text
probability reliability
```

This is especially important because downstream autonomy uses confidence/uncertainty.

---

# 20. BRIER SCORE FOUNDATION

Brier's 1950 work introduced a squared-error score for evaluating probabilistic predictions [R12].

For the project's binary classification setting:

\[
BS
=
\frac{1}{N}
\sum_i(p_i-y_i)^2
\]

is used as a probability-quality metric.

Lower values are better.

---

# 21. MODERN NEURAL-NETWORK CALIBRATION

Guo et al. showed that modern neural networks can be poorly calibrated and evaluated several post-hoc calibration methods, including temperature scaling [R13].

This supports:

- evaluating raw EEGNet confidence;
- considering temperature scaling as a candidate;
- not assuming softmax probabilities are trustworthy.

It does **not** force temperature scaling as the project's final calibration method.

---

# 22. CALIBRATION METHOD STATUS

Supported candidate methods include:

- temperature scaling;
- Platt/sigmoid calibration;
- isotonic regression.

The literature establishes these as legitimate methods.

The project still needs to choose one using an approved validation protocol.

---

# 23. BAYESIAN REASONING FOUNDATION

The Bayesian component uses the standard update:

\[
P(G\mid E)
\propto
P(E\mid G)P(G)
\]

Sequentially:

\[
P(G\mid E_{1:t})
\propto
P(E_t\mid G)
P(G\mid E_{1:t-1})
\]

This is standard probability theory.

The project contribution is not Bayes' theorem itself.

The important design question is how to construct a scientifically valid goal-evidence likelihood from EEG-derived evidence.

---

# 24. LATENT GOAL INFERENCE IN SHARED AUTONOMY

Shared-autonomy research often treats the human's intended goal as uncertain and uses the history of user inputs to estimate intent.

Dragan and Srinivasa explicitly framed shared control around:

- predicting user intent;
- combining human and autonomous policies;
- adapting arbitration based on confidence/context [R14].

Javdani et al. modeled shared autonomy with uncertainty over the user's goal and maintained a distribution over possible goals from input history [R15].

These works strongly support the project's architectural idea:

```text
uncertain human goal
→ probabilistic belief
→ autonomous assistance
```

---

# 25. WHAT THE PROJECT DOES DIFFERENTLY

The cited shared-autonomy literature does not automatically define this project's exact Bayesian model.

The project specifically uses:

```text
EEG-derived evidence
→ calibrated probabilities
→ goal-evidence adapter
→ explicit sequential Bayesian posterior
→ entropy
→ autonomy gating
```

This is a project-specific integration.

The likelihood semantics must therefore be justified independently.

---

# 26. SHARED AUTONOMY FOUNDATION

Shared autonomy allows a human to provide high-level control while autonomy assists with lower-level execution.

This directly supports the project's rule:

> **Human determines WHAT. AI determines HOW.**

Dragan & Srinivasa and Javdani et al. provide strong robotic shared-autonomy foundations for uncertain-intent assistance [R14, R15].

---

# 27. BCI SHARED CONTROL

Millán et al.'s review of BCIs and assistive technologies discusses the challenge of noisy, limited-bandwidth BCI outputs and highlights shared autonomy/shared control as an important method for controlling complex devices such as robots and wheelchairs [R16].

The review describes combining user mental commands with contextual/autonomous information so that assistive systems can perform meaningful actions more robustly.

This is highly aligned with the current project.

---

# 28. WHY GOAL-LEVEL CONTROL IS LITERATURE-CONSISTENT

BCI shared-control systems commonly avoid requiring users to provide every low-level movement.

Instead, the user provides higher-level commands while autonomy handles detailed navigation/control.

This supports the project's decision not to make:

```text
Left MI → move left one grid cell
```

the primary architecture.

---

# 29. HUMAN AUTHORITY AND SHARED CONTROL

Shared-autonomy research also highlights trade-offs between assistance and human control/agency.

Javdani et al. reported that increased assistance can improve task performance while users may still differ in how they value control authority [R15].

This supports preserving:

- confirmation;
- override;
- pause;
- stop.

It also supports reporting performance and human-control burden separately.

---

# 30. SYSTEM-SIDE ADAPTATION FOUNDATION

BCI performance varies between subjects and over time.

Adaptive BCI research has therefore explored systems that update classifiers or other parameters during interaction.

Vidaurre, Sannelli and colleagues investigated machine-learning-based co-adaptive calibration for motor-imagery BCIs [R17, R18].

Acqualagna et al. later evaluated a fully automatic co-adaptive motor-imagery BCI at larger scale [R19].

---

# 31. WHAT ADAPTATION LITERATURE SUPPORTS HERE

The literature supports the broad idea that:

> BCI systems may benefit from user-specific adaptation rather than remaining completely static.

It does **not** require the current project to implement full co-adaptive online classifier learning.

Because this project uses prerecorded EEG, its adaptation claims must remain limited to:

> **system-side personalization/adaptation**

---

# 32. PROJECT ADAPTATION STATUS

Current candidate adaptation targets remain:

- priors;
- decoder reliability;
- confidence thresholds;
- evidence weighting.

No final method is approved.

The adaptation literature provides motivation, not an automatic implementation decision.

---

# 33. A* PLANNING FOUNDATION

Hart, Nilsson and Raphael introduced A* as a heuristic graph-search method for minimum-cost path finding [R20].

For the project's simple 4-connected grid:

\[
f(n)=g(n)+h(n)
\]

with Manhattan distance as a natural heuristic.

This gives the project a transparent, established planning method.

---

# 34. WHY A* IS SCIENTIFICALLY SUFFICIENT

The research question is not:

> “Can we invent a new path-planning algorithm?”

Therefore an established planner is preferable.

A*:

- is understandable;
- is reproducible;
- supports obstacles;
- supports non-negative path costs;
- can incorporate simulated risk into \(g(n)\).

This prevents planning complexity from overshadowing the BCI/shared-autonomy research.

---

# 35. RISK-AWARE COST IS A PROJECT ENGINEERING EXTENSION

The conceptual cost:

\[
J=
distance+\lambda\times risk
\]

is a project-level engineering model.

The literature supports cost-aware graph planning broadly, but this exact project's:

- risk scale;
- hazard semantics;
- \(\lambda\);

are not externally established facts.

They must be defined experimentally.

---

# 36. SAFETY-CONSTRAINT FOUNDATION

The project's safety layer uses explicit action rejection.

Conceptually:

```text
planner proposes
→ safety checks hard constraints
→ execute or reject
```

This is consistent with a supervisory/safety-filter architecture.

However, the project does **not** implement formal runtime assurance, reachability analysis, or certified shielding.

Therefore the relevant claim is:

> **explicit simulated constraint enforcement**

not:

> **formally guaranteed robotic safety**

---

# 37. SAFETY LITERATURE STATUS

The project deliberately does not require advanced formal-safety literature to justify simple constraints such as:

- do not leave map bounds;
- do not enter blocked cells;
- stop on emergency stop.

If later work adds:

- formal shielding;
- control barrier functions;
- reachability;
- runtime assurance;

then additional dedicated literature is required.

---

# 38. UNCERTAINTY-AWARE BEHAVIOUR

The project uses uncertainty not merely as a displayed metric but as a control input.

This is consistent with shared-autonomy research emphasizing context/confidence-dependent arbitration [R14-R16].

For this project:

```text
posterior uncertainty
→ proceed / confirm / defer
```

is the central behavioral mechanism.

---

# 39. ENTROPY AS UNCERTAINTY

The project uses Shannon entropy over the goal posterior:

\[
H(P)=-\sum_g P(g)\log P(g)
\]

as its initial uncertainty measure.

This is mathematically standard.

The literature does not justify calling entropy a complete decomposition of model uncertainty.

Therefore the project correctly limits the claim to:

> **posterior uncertainty measured using entropy**

---

# 40. PROJECT NOVELTY POSITION

No individual component is claimed as entirely new.

The project's potential contribution is the **integrated experimental architecture**:

```text
real prerecorded motor-imagery EEG
→ classical + neural decoding
→ probability calibration
→ sequential Bayesian goal belief
→ entropy-based uncertainty
→ confidence-dependent shared autonomy
→ autonomous A* navigation
→ explicit simulated safety constraints
→ adaptation if implemented
```

The novelty claim, if made, should concern this combination and evaluation rather than claiming invention of CSP, EEGNet, Bayes, A*, or shared autonomy.

---

# 41. SCIENTIFIC GAP ADDRESSED BY THE PROJECT

The project investigates a practical systems question:

> **What happens when uncertain EEG intent is not converted directly into autonomous actions, but instead passed through calibrated probability estimation, sequential belief inference, uncertainty-aware control, and safety constraints?**

This links BCI decoding quality to downstream autonomous behavior.

That system-level connection is the central research value.

---

# 42. REFERENCE-TO-MODULE MAP

| Reference | Main Project Use |
|---|---|
| R1 Wolpaw et al. | BCI concept |
| R2 Schalk et al. | BCI2000 / dataset provenance |
| R3 Pfurtscheller & Lopes da Silva | ERD/ERS, motor imagery |
| R4 MNE EEGBCI documentation | Exact run semantics / software access |
| R5 Goldberger et al. | PhysioNet provenance |
| R6 Müller-Gerking et al. | Early optimized EEG spatial filters / CSP foundation |
| R7 Blankertz et al. | CSP/spatial filtering |
| R8 Lotte et al. 2007 | EEG classifier review |
| R9 Lotte et al. 2018 | Updated EEG classifier review |
| R10 Lawhern et al. | EEGNet |
| R11 MI-BCI review | Field limitations/context |
| R12 Brier | Brier Score |
| R13 Guo et al. | Neural calibration / temperature scaling |
| R14 Dragan & Srinivasa | Shared control, intent prediction, arbitration |
| R15 Javdani et al. | Uncertain latent goals in shared autonomy |
| R16 Millán et al. | BCI shared autonomy / assistive control |
| R17-R19 adaptive BCI work | Adaptation/personalization motivation |
| R20 Hart et al. | A* |

---

# 43. FOUNDATIONAL REFERENCES

## [R1] Wolpaw et al. — Brain–computer interfaces

Wolpaw, J. R., Birbaumer, N., McFarland, D. J., Pfurtscheller, G., & Vaughan, T. M. (2002).  
**Brain-computer interfaces for communication and control.**  
*Clinical Neurophysiology, 113(6), 767–791.*  
DOI: `10.1016/S1388-2457(02)00057-3`

Project relevance:

- BCI definition;
- neural control signal;
- BCI communication/control framing.

---

## [R2] Schalk et al. — BCI2000

Schalk, G., McFarland, D. J., Hinterberger, T., Birbaumer, N., & Wolpaw, J. R. (2004).  
**BCI2000: A general-purpose brain-computer interface (BCI) system.**  
*IEEE Transactions on Biomedical Engineering, 51(6), 1034–1043.*  
DOI: `10.1109/TBME.2004.827072`

Project relevance:

- BCI system architecture;
- EEGBCI dataset provenance.

---

## [R3] Pfurtscheller & Lopes da Silva — ERD/ERS

Pfurtscheller, G., & Lopes da Silva, F. H. (1999).  
**Event-related EEG/MEG synchronization and desynchronization: basic principles.**  
*Clinical Neurophysiology, 110(11), 1842–1857.*  
DOI: `10.1016/S1388-2457(99)00141-8`

Project relevance:

- motor-imagery neuroscience;
- sensorimotor rhythm modulation;
- ERD/ERS terminology.

---

## [R4] MNE-Python EEGBCI documentation

MNE-Python.  
**`mne.datasets.eegbci.load_data` / EEGBCI dataset documentation.**

Verified run mapping:

```text
4, 8, 12 → Motor imagery: left vs right hand
```

Project relevance:

- exact software-access method;
- subject/run definitions;
- dataset implementation reference.

Primary project access should use the current installed MNE version rather than assuming historical API details.

---

## [R5] Goldberger et al. — PhysioNet

Goldberger, A. L., et al. (2000).  
**PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals.**  
*Circulation, 101(23), e215–e220.*  
DOI: `10.1161/01.CIR.101.23.e215`

Project relevance:

- PhysioNet data infrastructure and provenance.

---

## [R6] Müller-Gerking et al. — Optimized EEG spatial filtering

Müller-Gerking, J., Pfurtscheller, G., & Flyvbjerg, H. (1999).  
**Designing optimal spatial filters for single-trial EEG classification in a movement task.**  
*Clinical Neurophysiology, 110(5), 787–798.*  
DOI: `10.1016/S1388-2457(98)00038-8`

Project relevance:

- spatial filtering for motor EEG discrimination;
- CSP foundation.

---

## [R7] Blankertz et al. — CSP / spatial filters

Blankertz, B., Tomioka, R., Lemm, S., Kawanabe, M., & Müller, K.-R. (2008).  
**Optimizing spatial filters for robust EEG single-trial analysis.**  
*IEEE Signal Processing Magazine, 25(1), 41–56.*  
DOI: `10.1109/MSP.2008.4408441`

Project relevance:

- CSP methodology;
- robust single-trial EEG spatial filtering.

---

## [R8] Lotte et al. — BCI classifier review

Lotte, F., Congedo, M., Lécuyer, A., Lamarche, F., & Arnaldi, B. (2007).  
**A review of classification algorithms for EEG-based brain-computer interfaces.**  
*Journal of Neural Engineering, 4(2), R1–R13.*  
DOI: `10.1088/1741-2560/4/2/R01`

Project relevance:

- classical EEG classifiers;
- comparative BCI methodology.

---

## [R9] Lotte et al. — 10-year classifier update

Lotte, F., et al. (2018).  
**A review of classification algorithms for EEG-based brain-computer interfaces: a 10 year update.**  
*Journal of Neural Engineering.*  
DOI: `10.1088/1741-2552/aab2f2`

Project relevance:

- updated BCI machine-learning context;
- classifier-selection and methodological context.

---

## [R10] Lawhern et al. — EEGNet

Lawhern, V. J., Solon, A. J., Waytowich, N. R., Gordon, S. M., Hung, C. P., & Lance, B. J. (2018).  
**EEGNet: a compact convolutional neural network for EEG-based brain-computer interfaces.**  
*Journal of Neural Engineering, 15(5), 056013.*  
DOI: `10.1088/1741-2552/aace8c`

Project relevance:

- compact neural EEG decoder;
- justification for EEGNet/compact CNN.

---

## [R11] Motor-imagery BCI review

Abiri, R., Borhani, S., Sellers, E. W., Jiang, Y., & Zhao, X. (review context; broader MI-BCI literature should be checked in the final bibliography) and related recent MI-BCI reviews.

For the current literature baseline, a verified 2021 review:

**A Comprehensive Review on Critical Issues and Possible Solutions of Motor Imagery Based Electroencephalography Brain-Computer Interface.**

Project relevance:

- MI-BCI practical limitations;
- adaptive/online BCI context;
- subject variability.

**Final-report rule:** verify complete author metadata and DOI from the primary publisher/PubMed record before formal manuscript citation.

---

## [R12] Brier — Probabilistic forecast score

Brier, G. W. (1950).  
**Verification of forecasts expressed in terms of probability.**  
*Monthly Weather Review, 78(1), 1–3.*  
DOI: `10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2`

Project relevance:

- Brier Score;
- probability-quality evaluation.

---

## [R13] Guo et al. — Neural probability calibration

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017).  
**On Calibration of Modern Neural Networks.**  
*Proceedings of the 34th International Conference on Machine Learning (ICML), 1321–1330.*

Project relevance:

- neural-network miscalibration;
- temperature scaling as a candidate method.

---

## [R14] Dragan & Srinivasa — Shared control and intent prediction

Dragan, A. D., & Srinivasa, S. S. (2013).  
**A policy-blending formalism for shared control.**  
*The International Journal of Robotics Research, 32(7), 790–805.*  
DOI: `10.1177/0278364913490324`

Project relevance:

- intent prediction;
- arbitration;
- confidence/context-dependent assistance;
- human–robot shared control.

---

## [R15] Javdani et al. — Shared autonomy under uncertain goals

Javdani, S., Srinivasa, S. S., & Bagnell, J. A. (2015).  
**Shared Autonomy via Hindsight Optimization.**  
*Robotics: Science and Systems.*  
DOI: `10.15607/RSS.2015.XI.032`

Project relevance:

- uncertainty over human goal;
- maintaining a goal distribution;
- autonomous assistance under uncertain intent;
- human-control/performance trade-offs.

---

## [R16] Millán et al. — BCI + assistive technology / shared autonomy

Millán, J. d. R., Rupp, R., Müller-Putz, G. R., Murray-Smith, R., Giugliemma, C., Tangermann, M., Vidaurre, C., Cincotti, F., Kübler, A., Leeb, R., Neuper, C., Müller, K.-R., & Mattia, D. (2010).  
**Combining Brain–Computer Interfaces and Assistive Technologies: State-of-the-Art and Challenges.**  
*Frontiers in Neuroscience, 4, 161.*  
DOI: `10.3389/fnins.2010.00161`

Project relevance:

- noisy/low-bandwidth BCI control;
- shared autonomy for robots/wheelchairs;
- context-aware assistance.

---

## [R17] Vidaurre, Sannelli & Blankertz — Co-adaptive calibration

Vidaurre, C., Sannelli, C., & Blankertz, B. (2011).  
**Machine-learning based co-adaptive calibration: towards a cure for BCI illiteracy.**  
*Neural Computation, 23, 791–816.*  
DOI: `10.1162/NECO_a_00089`

Project relevance:

- BCI adaptation;
- personalization motivation.

---

## [R18] Vidaurre et al. — Co-adaptive BCI efficiency

Vidaurre, C., Sannelli, C., Müller, K.-R., & Blankertz, B. (2011).  
**Co-adaptive calibration to improve BCI efficiency.**  
*Journal of Neural Engineering, 8, 025009.*  
DOI: `10.1088/1741-2560/8/2/025009`

Project relevance:

- adaptive calibration;
- system/user adaptation context.

---

## [R19] Acqualagna et al. — Large-scale co-adaptive MI-BCI

Acqualagna, L., Botrel, L., Vidaurre, C., Kübler, A., & Blankertz, B. (2016).  
**Large-Scale Assessment of a Fully Automatic Co-Adaptive Motor Imagery-Based Brain Computer Interface.**  
*PLOS ONE, 11(2), e0148886.*  
DOI: `10.1371/journal.pone.0148886`

Project relevance:

- empirical motivation for personalization;
- MI-BCI user variability.

---

## [R20] Hart, Nilsson & Raphael — A*

Hart, P. E., Nilsson, N. J., & Raphael, B. (1968).  
**A Formal Basis for the Heuristic Determination of Minimum Cost Paths.**  
*IEEE Transactions on Systems Science and Cybernetics, 4(2), 100–107.*  
DOI: `10.1109/TSSC.1968.300136`

Project relevance:

- A* graph search;
- minimum-cost path planning;
- heuristic-search foundation.

---

# 44. REFERENCES THAT SUPPORT THE PROJECT BUT DO NOT DEFINE IT

The project may cite additional literature on:

- modern motor-imagery CNNs;
- cross-subject EEG learning;
- transfer learning;
- uncertainty estimation;
- BCI shared control;
- HCI;
- robotic safety;
- adaptive autonomy.

However, additional references should only be added when they support:

```text
a real implemented component
or
a specific discussion/future-work statement
```

Do not inflate the bibliography with unrelated state-of-the-art methods.

---

# 45. OPTIONAL FUTURE LITERATURE DOMAINS

If optional components are later approved, targeted literature reviews may be added.

## ROS2 / physical robotics

Only if hardware/ROS integration is approved.

## Reinforcement learning

Only if PPO/RL comparison is approved.

## Neuromorphic / spiking models

Only if SNN comparison is approved.

## Active inference

Only if explicitly added to cognitive modelling.

## Formal safety

Only if formal verification/barrier/reachability methods are added.

## Live BCI co-adaptation

Only if actual interactive EEG acquisition is added.

---

# 46. LITERATURE-TO-CLAIM RULE

Every scientific claim should have one of three statuses.

## Directly supported by literature

Example:

> Motor imagery is associated with sensorimotor ERD/ERS.

## Supported by project experiment

Example:

> Calibration reduced ECE by X under the tested split.

## Project design choice

Example:

> We use A* with a configurable risk cost in a 2D SAR environment.

Do not present project design choices as established scientific facts.

---

# 47. LITERATURE-TO-IMPLEMENTATION RULE

A paper describing a technique does not automatically mean the project should implement it.

Example:

```text
MC dropout exists
```

does not mean:

```text
add MC dropout
```

The project uses literature to justify approved scope, not to continuously expand scope.

---

# 48. CITATION ACCURACY RULE

Before the final technical report or any research-paper submission:

1. verify title;
2. verify author list;
3. verify year;
4. verify journal/conference;
5. verify volume/pages where relevant;
6. verify DOI;
7. verify that the cited paper actually supports the statement.

Do not rely on memory alone.

---

# 49. NO FABRICATED PUBLICATION STATUS

The project's own prior tabular-classification research work is not a peer-reviewed publication unless formal publication later occurs.

Similarly, this NeuroCognitive Shared Autonomy project should not be called:

- published;
- peer-reviewed;
- accepted;

unless that actually happens.

A technical report is not equivalent to peer-reviewed publication.

---

# 50. CURRENT SCIENTIFIC FOUNDATION SUMMARY

The project's scientific foundation is well supported at the component level. Motor-imagery EEG and sensorimotor ERD/ERS are established BCI phenomena; the PhysioNet EEGBCI dataset and BCI2000 provide a reproducible public data foundation; CSP+LDA is a historically established classical motor-imagery pipeline; EEGNet provides a compact neural comparison; probability-calibration literature supports evaluating whether model confidence is trustworthy; shared-autonomy literature supports maintaining uncertainty over human goals and combining high-level human intention with autonomous execution; BCI shared-control literature directly motivates adding autonomy because EEG control is noisy and bandwidth-limited; adaptive BCI literature motivates limited personalization; and A* provides a transparent planning foundation. The project's research value therefore does not depend on claiming that any one component is new. Its contribution is the disciplined integration and evaluation of these elements around a specific question: whether calibrated, Bayesian, uncertainty-aware shared autonomy can make EEG-based intent control more reliable and safer than direct control in a controlled Search & Rescue simulation.

---

# 51. NEXT DOCUMENT

The next planned document is:

**`22_AI_DEVELOPMENT_WORKFLOW.md` — AI-Assisted Development Governance, ChatGPT/Codex Roles, Task Protocol, Review Loop, Change Control, and Scientific Accountability**

That document should formalize:

- ChatGPT as Project Brain / Research Director;
- project owner as final authority;
- Codex as implementation engineer;
- design → implement → test → review loop;
- narrow task tickets;
- independent code/result review;
- blocked/unresolved decision handling;
- Git/state-document updates;
- AI-generated-code verification;
- prohibited autonomous scope changes;
- and exact handoff procedures between ChatGPT and Codex.

It must reflect the **current ChatGPT + Codex workflow**, not the older Claude-specific workflow.
