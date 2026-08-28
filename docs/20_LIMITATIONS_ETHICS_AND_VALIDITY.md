# 20_LIMITATIONS_ETHICS_AND_VALIDITY.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Limitations, Ethical Boundaries, Threats to Validity, and Responsible Scientific Claiming

**Document ID:** J-01  
**Document class:** Scientific Validity / Ethics / Limitations  
**Authority level:** Subordinate to all Master Authority, Scenario, Architecture, Data, Neuroscience, ML, Bayesian, Shared-Autonomy, Planning, Safety, Implementation, Experimental Design, Metrics, and Testing documents  
**Status:** Authoritative limitations/ethics/validity baseline; unresolved scientific decisions remain unresolved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND CLAIM-DISCIPLINE RULE

This document defines:

- what the project can reasonably claim;
- what it cannot claim;
- where its methodology is simplified;
- what threatens internal, construct, and external validity;
- and how ethical boundaries must be communicated.

It must remain consistent with all previously approved project documents.

If this document conflicts with a higher-authority document, the higher-authority document wins.

The governing rule is:

> **Limitations must be stated precisely enough to preserve scientific credibility, without exaggerating them so far that they misrepresent what the project actually demonstrates.**

The project is a **software-based research prototype using public prerecorded EEG and a simulated Search & Rescue environment**.

It is not a clinical system, medical device, certified BCI, or deployable rescue platform.

---

# 1. PURPOSE OF THIS DOCUMENT

This document addresses five areas:

```text
L1 — Technical limitations
L2 — Scientific/model limitations
L3 — Ethical boundaries
L4 — Threats to validity
L5 — Responsible reporting and claims
```

The purpose is not to weaken the project.

The purpose is to define exactly what evidence supports and what remains outside the demonstrated scope.

---

# 2. CORE PROJECT SCOPE LIMITATION

The project integrates:

- public prerecorded motor-imagery EEG;
- EEG decoding;
- probability calibration;
- Bayesian goal inference;
- uncertainty-aware shared autonomy;
- A* planning;
- simulated safety constraints;
- a simple 2D Search & Rescue environment.

The project does **not** demonstrate:

- live EEG acquisition;
- real-time human neural interaction;
- physical robot control;
- real disaster deployment;
- clinical decision support;
- medical diagnosis;
- direct thought reading;
- certified autonomous safety.

---

# 3. OFFLINE EEG LIMITATION

The dataset consists of prerecorded EEG.

Therefore the system is evaluated through:

```text
Offline EEG Replay
```

or:

```text
Simulated Real-Time BCI
```

The project cannot claim:

> “live EEG control”

unless actual live EEG hardware is later added and separately validated.

---

# 4. CONSEQUENCE OF OFFLINE EEG

Offline replay removes several challenges present in a live BCI:

- electrode placement variability;
- changing impedance;
- operator fatigue;
- feedback-driven behavior changes;
- real-time acquisition latency;
- hardware dropouts;
- online artifact handling;
- user adaptation during operation.

Therefore full real-time performance may differ from offline results.

---

# 5. MOTOR-IMAGERY LIMITATION

The EEG task is initially:

```text
Left-hand motor imagery
vs
Right-hand motor imagery
```

This is a constrained BCI control signal.

It does not decode:

- arbitrary thoughts;
- semantic plans;
- emotions;
- natural-language intentions;
- rescue strategy.

The project should use wording such as:

> **EEG-based motor-imagery intent/control decoding**

rather than:

> **mind reading**

---

# 6. BINARY-INTERFACE LIMITATION

The initial decoder is binary.

The Search & Rescue scenario may contain more than two possible objectives.

This creates a fundamental interaction-design constraint.

Preserved solution classes include:

1. two active options at a time;
2. hierarchical binary selection;
3. abstract binary priority selection;
4. future multiclass EEG.

No final option is currently approved.

This must remain visible as a design limitation until resolved.

---

# 7. EEG SIGNAL QUALITY LIMITATION

Scalp EEG is:

- low amplitude;
- noisy;
- spatially diffuse;
- sensitive to artifacts;
- highly variable across people and sessions.

This limits classification reliability.

A high model probability is not proof of true human intent.

---

# 8. SUBJECT VARIABILITY

Motor-imagery decoding performance can vary substantially between subjects.

Possible reasons include:

- physiological variation;
- different motor-imagery strategies;
- signal quality;
- recording noise;
- inter-subject differences.

Therefore aggregate performance must not hide poor-performing subjects.

Subject-wise reporting is required where appropriate.

---

# 9. DATASET LIMITATION

The project uses a public research dataset rather than data collected specifically for this Search & Rescue task.

Therefore the EEG represents:

```text
motor imagery
```

not actual rescue-goal cognition.

The Search & Rescue interpretation is an application-layer control mapping.

This distinction must be explicit.

---

# 10. TASK-SEMANTICS LIMITATION

The dataset's Left/Right labels represent motor-imagery tasks.

They do not naturally mean:

```text
Victim A
Victim B
Safe Zone
Medical Resource
```

Any mapping between motor imagery and application options is an interface convention.

It must not be presented as if the EEG directly encodes rescue semantics.

---

# 11. PREPROCESSING LIMITATION

EEG results can depend on:

- filter band;
- reference;
- epoch interval;
- baseline correction;
- artifact handling;
- channel selection;
- resampling.

Several of these are still unresolved.

Once frozen, they must be treated as methodological choices rather than universal truths.

---

# 12. MODEL LIMITATION

The project compares:

```text
CSP + LDA
EEGNet / compact CNN
```

These models represent two reasonable approaches.

They do not exhaust all EEG decoding methods.

The project must not claim:

> “best possible motor-imagery decoder”

unless a much broader benchmark supports it.

---

# 13. MODEL PERFORMANCE LIMITATION

Good classification performance on this dataset does not imply:

- equal performance on other EEG datasets;
- equal performance on live EEG;
- equal performance on clinical populations;
- equal performance on other tasks.

Results are specific to the evaluated protocol.

---

# 14. CALIBRATION LIMITATION

Probability calibration is distribution-dependent.

A calibrator that works well on one set of subjects or runs may become miscalibrated under:

- new subjects;
- altered signal quality;
- distribution shift;
- different preprocessing.

Calibration improves probability reliability under the tested conditions.

It does not make probabilities universally correct.

---

# 15. ECE LIMITATION

Expected Calibration Error depends on:

- bin count;
- binning method;
- sample size.

Therefore ECE is not a complete description of calibration.

It should be interpreted with:

- reliability diagrams;
- Brier Score;
- subject-wise behavior where useful.

---

# 16. BAYESIAN-MODEL LIMITATION

The Bayesian layer is a computational model of system belief.

It is not evidence that:

- the human brain performs the same Bayesian update;
- the posterior equals subjective human confidence;
- the model captures all cognitive processes involved in intention.

---

# 17. LIKELIHOOD-MODEL LIMITATION

A central unresolved issue remains:

```text
P(class | EEG)
```

is not automatically:

```text
P(evidence | goal)
```

The final Bayesian likelihood construction must be mathematically justified.

Until it is approved, real EEG-to-goal Bayesian inference is not scientifically complete.

---

# 18. CONDITIONAL-INDEPENDENCE LIMITATION

Simple sequential Bayesian updating may treat successive evidence observations as sufficiently informative given the goal.

EEG windows may be correlated.

If highly overlapping or repeated evidence is multiplied independently, posterior confidence may become artificially high.

The final evidence protocol must minimize or explicitly acknowledge this risk.

---

# 19. PRIOR LIMITATION

Bayesian results depend on priors, especially when evidence is weak.

A uniform prior is a clean baseline but may not represent real contextual knowledge.

A personalized or context-based prior may improve performance but can also introduce bias.

Therefore priors must be documented and sensitivity considered where relevant.

---

# 20. ENTROPY LIMITATION

Entropy measures distribution concentration.

It does not capture every form of uncertainty.

In particular, posterior entropy does not directly distinguish:

- epistemic uncertainty;
- aleatoric uncertainty;
- distribution shift;
- model misspecification.

Therefore the project should say:

> **posterior uncertainty measured using entropy**

rather than:

> **complete uncertainty estimation**

---

# 21. OVERCONFIDENCE LIMITATION

A posterior may become:

```text
low entropy
+
wrong
```

This is a critical failure case.

Low entropy must never be interpreted as proof of correctness.

---

# 22. SHARED-AUTONOMY LIMITATION

The shared-autonomy controller uses a simplified policy such as:

```text
proceed
confirm
defer
pause
stop
```

This is an engineered decision policy.

It is not a general theory of optimal human–AI collaboration.

---

# 23. THRESHOLD LIMITATION

Confidence/entropy thresholds may materially affect:

- wrong-goal rate;
- confirmation frequency;
- latency;
- task success.

Thresholds selected on development data may not generalize perfectly to new users or conditions.

Therefore threshold sensitivity should be analyzed where possible.

---

# 24. HUMAN-INTERACTION LIMITATION

The core project does not currently include a formal human-subject study.

Therefore it cannot claim measured:

- usability;
- trust;
- mental workload;
- fatigue;
- user satisfaction;
- cognitive burden;
- preference.

Automated experiments may only measure system behavior under a defined simulated-human policy.

---

# 25. SIMULATED-HUMAN LIMITATION

A simulated policy such as:

```text
if candidate matches true goal:
    confirm
else:
    override
```

is useful for controlled experiments.

It does not represent real human behavior.

Humans may:

- make errors;
- respond slowly;
- hesitate;
- change goals;
- misunderstand the interface.

These are outside the current core evaluation.

---

# 26. ADAPTATION LIMITATION

The adaptation mechanism remains unresolved.

Even after implementation, any adaptation is likely to be intentionally simple.

It should not be described as:

- learning a person's mind;
- cognitive-style modelling;
- full co-adaptive BCI;
- neuroplasticity modelling.

---

# 27. OFFLINE ADAPTATION LIMITATION

Because EEG is prerecorded, true human adaptation to the system cannot occur.

Only system-side parameter adaptation can be simulated.

Therefore the project should use:

> **system-side personalization**

rather than:

> **full co-adaptation**

unless a live interactive study is later performed.

---

# 28. SEARCH & RESCUE SIMULATION LIMITATION

The environment is a simplified 2D technical simulation.

It represents:

- targets;
- obstacles;
- hazards;
- paths;
- risk values.

It does not reproduce:

- real disaster physics;
- terrain complexity;
- smoke dynamics;
- communication failure;
- victim movement;
- robot dynamics;
- sensor uncertainty;
- multi-agent coordination.

---

# 29. 2D GRID LIMITATION

The grid environment simplifies:

- geometry;
- motion;
- navigation;
- collision behavior.

This is appropriate for isolating the research question.

It is not evidence that the same planner/controller would work unchanged on a physical robot.

---

# 30. A* LIMITATION

A* assumes:

- an explicit map;
- known traversability;
- defined cost;
- known goal.

Real rescue robots may require:

- SLAM;
- perception;
- dynamic planning;
- localization;
- continuous control.

Those are outside current scope.

---

# 31. RISK-MODEL LIMITATION

The environmental risk score is simulated.

It does not represent certified physical risk.

The conceptual cost:

\[
J=\text{distance}+\lambda\cdot\text{risk}
\]

is an engineering abstraction.

The exact risk scale and \(\lambda\) remain unresolved.

---

# 32. SAFETY LIMITATION

The safety controller enforces explicit software constraints in simulation.

It can demonstrate:

- blocked-cell rejection;
- prohibited-action rejection;
- emergency stop;
- safety interventions.

It cannot demonstrate:

- real human safety;
- hardware fail-safety;
- medical safety;
- industrial certification;
- formal safety guarantees.

---

# 33. SAFETY-Critical TERMINOLOGY LIMIT

The phrase:

> **safety-critical control**

is used in the limited project sense of:

- explicit constraint enforcement;
- action rejection;
- emergency stopping;
- measurable simulated violations.

It must not imply certified safety-critical deployment.

---

# 34. NO CLINICAL CLAIM

The project is not intended to:

- diagnose disease;
- detect medical emergencies;
- guide treatment;
- assess neurological disorder;
- replace clinical EEG interpretation.

Even though EEG is a biomedical signal, this is an AI/BCI/autonomy research project.

---

# 35. NO MEDICAL-DEVICE CLAIM

The project is not a validated medical device.

Do not use wording such as:

- medically validated;
- clinical-grade;
- diagnostic;
- FDA-ready;
- hospital-ready.

---

# 36. NO THOUGHT-READING CLAIM

The system does not read unrestricted thoughts.

It decodes a constrained motor-imagery classification signal under a known experimental task.

Preferred wording:

> **motor-imagery EEG decoding**

or:

> **EEG-based intent/control signal decoding**

---

# 37. NO REAL-TIME CLAIM

Preferred:

```text
Offline EEG Replay
Simulated Real-Time BCI
```

Avoid:

```text
Real-Time EEG BCI
```

unless actual live acquisition is implemented.

---

# 38. NO REAL RESCUE CLAIM

The Search & Rescue environment is an application scenario for testing autonomy.

Do not claim:

> “validated disaster-response system”

or:

> “ready for rescue deployment.”

---

# 39. PUBLIC-DATASET ETHICAL BOUNDARY

The project uses a publicly available research dataset.

The project should:

- cite the dataset appropriately;
- preserve subject anonymity;
- avoid attempting re-identification;
- use data within its intended research terms;
- avoid implying ownership of the dataset.

---

# 40. SUBJECT PRIVACY

Dataset subject IDs should remain anonymous identifiers.

The project should not attempt to infer or expose:

- real identity;
- private health status;
- sensitive personal information.

---

# 41. DATA MINIMIZATION

The project should process only information required for:

- EEG decoding;
- subject/fold grouping;
- experiment evaluation.

No unnecessary personal profiling is needed.

---

# 42. NO DEMOGRAPHIC INFERENCE

Unless the dataset explicitly provides relevant metadata and the project later approves an analysis, do not infer:

- age;
- sex;
- ethnicity;
- health condition;
- socioeconomic characteristics

from EEG.

This is outside scope.

---

# 43. RESPONSIBLE HUMAN-AI DESIGN

The system preserves:

- human confirmation;
- override;
- pause;
- stop.

This is important because the EEG signal is uncertain.

The project intentionally avoids a design where the autonomous system unquestioningly acts on every neural prediction.

---

# 44. HUMAN AGENCY

Human authority is a core ethical design principle.

The autonomous system may help execute the chosen objective.

It must not:

- replace human intent;
- silently choose another objective;
- remove stop/override authority.

---

# 45. AUTOMATION BIAS RISK

A highly confident system may encourage users to over-trust its output.

The interface should therefore display uncertainty carefully.

Avoid certainty language such as:

> “The system knows your intention.”

Prefer:

> “Current inferred goal.”

---

# 46. FALSE CONFIDENCE RISK

Even calibrated probabilities may be wrong.

Therefore visualizations should not present:

```text
0.95
```

as:

> “95% certain what the user wants.”

Better:

> “Model/posterior confidence: 0.95 under the current model.”

---

# 47. INTERNAL VALIDITY

Internal validity asks:

> Are observed differences actually caused by the component being tested?

Threats include:

- changing multiple modules between conditions;
- inconsistent splits;
- different EEG sequences;
- different maps;
- different seeds;
- hidden tuning differences.

The A/B/C/D design must control these.

---

# 48. INTERNAL-VALIDITY CONTROL

Where possible, comparisons should use:

```text
same EEG sequence
same subject
same map
same goal
same planner
same safety
same seed
```

and change only the intended experimental component.

---

# 49. TEST-SET TUNING THREAT

Using final test results to choose:

- preprocessing;
- architecture;
- calibration;
- thresholds;
- \(\lambda\);
- adaptation;

would inflate performance estimates.

The final test set must remain protected.

---

# 50. DATA-LEAKAGE THREAT

Important leakage risks include:

- CSP fit before split;
- normalization fit on all data;
- calibration fit on test labels;
- windows from same trial across train/test;
- subject overlap in cross-subject evaluation;
- future feedback used by adaptation;
- true goal injected into runtime inference.

These must be actively tested.

---

# 51. CONSTRUCT VALIDITY

Construct validity asks:

> Does the metric/system actually represent the concept being claimed?

Examples:

## “Intent”

The project operationalizes intent as a constrained BCI control objective.

It is not unrestricted human intent.

## “Uncertainty”

Operationalized initially as posterior entropy.

It is not all forms of uncertainty.

## “Safety”

Operationalized as explicit simulated constraints and violations.

It is not real-world physical safety.

---

# 52. COGNITIVE-CONSTRUCT LIMITATION

The project calls the system NeuroCognitive because it combines:

- neural input;
- latent-intent belief;
- uncertainty;
- adaptation.

This is a limited computational cognitive abstraction.

It is not a full cognitive model.

---

# 53. EXTERNAL VALIDITY

External validity asks:

> Do findings generalize beyond the evaluated conditions?

Major limits include:

- one public EEG dataset;
- motor-imagery task;
- prerecorded data;
- simulated 2D environment;
- no physical robot;
- no human-subject interaction study.

Therefore external claims must remain conservative.

---

# 54. CROSS-SUBJECT EXTERNAL VALIDITY

Cross-subject evaluation improves generalization evidence.

However, even strong held-out-subject performance does not guarantee:

- other datasets;
- other EEG devices;
- clinical users;
- real-time operation.

It is evidence only within the evaluated dataset/protocol.

---

# 55. ECOLOGICAL VALIDITY

The experiment uses motor imagery to control simulated rescue choices.

This is not a natural everyday interaction.

Therefore ecological validity is limited.

This is acceptable because the project is designed as a technical proof-of-concept.

---

# 56. STATISTICAL-CONCLUSION VALIDITY

Potential threats include:

- small subject count;
- few seeds;
- unstable metrics;
- multiple comparisons;
- selective reporting.

The final report should preserve:

- sample size;
- subject-wise results;
- variability;
- negative cases.

---

# 57. METRIC LIMITATION

No single metric captures system quality.

Examples:

```text
accuracy
```

does not capture calibration.

```text
low entropy
```

does not guarantee correctness.

```text
task success
```

does not guarantee safety.

```text
few confirmations
```

does not guarantee good shared autonomy.

Metrics must be interpreted together.

---

# 58. REPRODUCIBILITY THREATS

Potential threats include:

- package-version changes;
- stochastic training;
- GPU nondeterminism;
- unrecorded config changes;
- overwritten result files;
- manual notebook-only processing.

The repository architecture explicitly mitigates these through:

- config snapshots;
- Git commits;
- seeds;
- machine-readable logs;
- model manifests.

---

# 59. IMPLEMENTATION-BIAS THREAT

AI-assisted development can introduce:

- hidden defaults;
- inconsistent assumptions;
- copied formulas without context;
- interface drift;
- accidental scope expansion.

The ChatGPT → Project Owner → Codex workflow exists partly to reduce this risk.

---

# 60. AI-ASSISTED DEVELOPMENT ETHICS

Using AI coding tools is acceptable.

Scientific credibility depends on:

- human approval of methodology;
- verification of generated code;
- testing;
- transparent documentation;
- reproducible results.

The project should not claim hand-written implementation where most code is AI-assisted.

At the same time, code-generation assistance does not invalidate the project if the methodology and verification are sound.

---

# 61. VERIFICATION RESPONSIBILITY

AI-generated code must not be treated as correct because it compiles.

Important modules require:

- unit tests;
- integration tests;
- mathematical verification;
- manual review.

---

# 62. SELECTIVE-REPORTING RISK

The project must not show only:

- best subject;
- best seed;
- best map;
- best threshold;
- successful episodes.

Representative failures must be preserved.

---

# 63. NEGATIVE RESULTS

Negative results are valid.

Examples:

- CSP+LDA outperforms EEGNet;
- calibration adds little;
- Bayesian accumulation increases delay;
- adaptation harms some subjects;
- risk-aware planning increases completion time.

These outcomes should be reported honestly.

---

# 64. CONFIRMATION-BIAS RISK

Because the project is designed around uncertainty-aware shared autonomy, there is a risk of unconsciously designing experiments to prove that idea.

Mitigation:

- freeze experimental conditions;
- use clear baselines;
- preserve all outcomes;
- avoid tuning on final test.

---

# 65. BASELINE FAIRNESS

A baseline must not be intentionally weakened.

For example:

- System A should not use a worse decoder simply because it is “basic”;
- safety comparisons should isolate safety rather than unrelated changes;
- calibration comparisons should use the same underlying predictions.

---

# 66. A/B/C/D VALIDITY THREAT

If System D differs from System A in many components, improvement cannot automatically be attributed to one component.

Therefore component ablations are required.

---

# 67. ADAPTATION-VALIDITY THREAT

If adaptation is evaluated on the same feedback episode used to update it, improvement may be overstated.

Separate:

```text
adaptation data
```

from:

```text
post-adaptation evaluation
```

when testing generalization.

---

# 68. SIMULATION-TO-REALITY GAP

The full pipeline may work well in simulation while still failing in real use due to:

- EEG hardware variability;
- latency;
- robot dynamics;
- perception errors;
- sensor failures;
- unpredictable hazards;
- human behavior.

This gap must be stated clearly.

---

# 69. NO HARDWARE-IN-THE-LOOP VALIDATION

The current core does not include:

- EEG headset;
- physical robot;
- actuator;
- safety relay;
- physical environment.

Therefore hardware-level reliability is outside the evidence base.

---

# 70. NO HUMAN-SUBJECT VALIDATION

Without recruited participants interacting with the system, the project cannot claim evidence about:

- usability;
- user comfort;
- trust;
- fatigue;
- learnability;
- actual intervention behavior.

---

# 71. NO CLINICAL POPULATION VALIDATION

The dataset does not establish performance for:

- stroke patients;
- motor-impaired users;
- neurological disorders;
- elderly users;
- emergency responders.

Do not imply otherwise.

---

# 72. NO DEPLOYMENT-READINESS CLAIM

The project is a research prototype.

It is not:

- production hardened;
- certified;
- security audited;
- clinically validated;
- disaster-deployment ready.

---

# 73. CYBERSECURITY LIMITATION

Security engineering is not a core focus of this project.

A real deployed BCI/autonomous rescue system would require:

- authentication;
- secure data transport;
- access control;
- tamper resistance;
- adversarial resilience.

These are outside current scope.

---

# 74. PRIVACY LIMITATION IN REAL DEPLOYMENT

Although the public dataset is already anonymized, a real BCI system would process highly sensitive neural data.

Real deployment would require:

- consent;
- data minimization;
- secure storage;
- deletion policies;
- privacy governance.

The current prototype does not attempt to solve the full neural-data privacy problem.

---

# 75. DUAL-USE CONSIDERATION

BCI and autonomous control technologies can have beneficial and harmful applications.

This project is framed around:

- human authority;
- safety;
- assistive shared autonomy;
- transparent uncertainty.

It does not explore coercive, surveillance, or manipulative uses.

---

# 76. AUTONOMY BOUNDARY

The AI should remain a tool for execution assistance.

It must not silently convert:

```text
human intent uncertainty
```

into:

```text
AI chooses preferred objective
```

This is both a scientific and ethical boundary.

---

# 77. SAFETY VS HUMAN AUTHORITY EDGE CASE

Human authority is strong, but hard simulated safety constraints may reject an unsafe movement even if the user wants it.

Thus:

```text
human determines objective
```

does not mean:

```text
human can force violation of hard safety rules
```

This is consistent with the architecture.

---

# 78. RESPONSIBLE TERMINOLOGY TABLE

| Avoid | Prefer |
|---|---|
| Mind reading | Motor-imagery EEG decoding |
| Reads human thoughts | Infers constrained control intent |
| Live EEG | Offline EEG replay / simulated real-time BCI |
| Human cognition model | Computational latent-intent model |
| Fully autonomous rescue AI | Shared-autonomy simulation |
| Safe rescue robot | Simulated safety-constrained agent |
| Clinical EEG system | Research EEG decoding prototype |
| Real-time adaptive BCI | Offline system-side adaptation, unless live hardware exists |
| Proven safe | Reduced measured simulated violations, if supported |

---

# 79. RESPONSIBLE RESULTS LANGUAGE

Allowed if supported:

> “System D reduced wrong-goal commitment relative to System A under the tested simulation.”

Not allowed:

> “System D understands human intent better in real life.”

Allowed:

> “Calibration reduced ECE on the held-out evaluation split.”

Not allowed:

> “The calibrated probability is the true probability of human intention.”

---

# 80. RESPONSIBLE SAFETY LANGUAGE

Allowed:

> “The safety controller prevented blocked-cell entry in the tested simulation.”

Not allowed:

> “The system guarantees safe rescue operation.”

---

# 81. RESPONSIBLE COGNITIVE LANGUAGE

Allowed:

> “A Bayesian latent-intent belief state was maintained over candidate goals.”

Not allowed:

> “The system models the user's thought process.”

---

# 82. RESPONSIBLE ADAPTATION LANGUAGE

Allowed if implemented:

> “The system personalized confidence thresholds based on prior corrections.”

Not allowed:

> “The system learns the user's brain.”

---

# 83. ETHICS OF FAILURE REPORTING

Failures should not be hidden.

Particularly important:

- confident wrong predictions;
- wrong-goal commitments;
- safety interventions;
- subjects with poor decoding;
- adaptation failures.

This is essential because the application framing is safety-sensitive.

---

# 84. ETHICS OF DEMONSTRATION

A demo should not create a false impression of capabilities.

The UI must clearly indicate:

- prerecorded EEG;
- simulated environment;
- confidence/uncertainty;
- research-prototype status.

Do not stage a demo that visually implies a physical/live system if none exists.

---

# 85. LIMITATION DOCUMENTATION IN FINAL REPORT

The final technical report should include a concise but meaningful Limitations section covering at least:

1. prerecorded EEG;
2. binary motor imagery;
3. subject variability;
4. application-mapping abstraction;
5. simplified Bayesian assumptions;
6. simple adaptation;
7. 2D simulation;
8. simulated safety;
9. no live human study;
10. limited external validity.

---

# 86. THREATS-TO-VALIDITY STRUCTURE FOR FINAL REPORT

Recommended structure:

```text
Internal Validity
Construct Validity
External Validity
Statistical Conclusion Validity
Reproducibility
Ethical Boundaries
```

This gives the final report a strong scientific structure.

---

# 87. INTERNAL VALIDITY SUMMARY

Main threats:

- leakage;
- unfair baselines;
- multiple simultaneous changes;
- test-set tuning;
- hidden defaults.

Mitigations:

- grouped splits;
- component ablations;
- frozen configs;
- test-set protection;
- logging;
- independent review.

---

# 88. CONSTRUCT VALIDITY SUMMARY

Main threats:

- “intent” overclaim;
- “uncertainty” overclaim;
- “cognitive” overclaim;
- “safety” overclaim.

Mitigation:

> define each construct operationally and use limited terminology.

---

# 89. EXTERNAL VALIDITY SUMMARY

Main threats:

- one dataset;
- prerecorded data;
- motor-imagery task;
- no live users;
- simulated environment.

Mitigation:

> clearly limit claims to the tested protocol and identify real-time/hardware validation as future work.

---

# 90. STATISTICAL-CONCLUSION VALIDITY SUMMARY

Main threats:

- low sample size;
- high subject variability;
- seed variability;
- selective reporting;
- multiple comparisons.

Mitigation:

- subject-wise metrics;
- repeated seeds/folds where appropriate;
- variability reporting;
- predefined metrics;
- transparent negative results.

---

# 91. REPRODUCIBILITY SUMMARY

Main threats:

- AI-generated code changes;
- version drift;
- hidden config;
- overwritten results.

Mitigation:

- Git;
- config snapshots;
- experiment IDs;
- manifests;
- machine-readable logs;
- regression tests.

---

# 92. FUTURE WORK THAT DIRECTLY ADDRESSES LIMITATIONS

Appropriate future extensions include:

- live EEG acquisition;
- real participant interaction;
- broader motor-imagery/multiclass BCI;
- longitudinal personalization;
- more advanced uncertainty methods;
- dynamic environments;
- physical robot integration;
- ROS2/Gazebo;
- human-factors evaluation;
- stronger safety verification.

These are future work, not current claims.

---

# 93. LIMITATION PRIORITIZATION

Not all limitations are equally important.

## Critical limitations

- offline EEG;
- binary interface;
- EEG-to-goal mapping;
- likelihood semantics;
- no real human study;
- simulation-only safety.

## Important methodological limitations

- preprocessing dependence;
- subject variability;
- calibration shift;
- threshold dependence;
- simplified Bayes assumptions.

## Acceptable engineering simplifications

- 2D grid;
- A*;
- single agent;
- no 3D;
- no ROS2.

These simplifications are intentional and help isolate the research question.

---

# 94. WHAT DOES NOT NEED TO BE APOLOGIZED FOR

The project does not need to treat every deliberate scope choice as a flaw.

Examples:

- using A* instead of RL;
- using a 2D grid;
- using public data;
- avoiding hardware;
- using a compact CNN;
- not implementing 3D.

These are valid design choices for a focused research prototype.

---

# 95. LIMITATION VS INVALIDITY

A limitation means:

> the result is valid within a bounded scope.

An invalid experiment means:

> the result should not be trusted even within that scope.

Examples:

```text
offline EEG
→ limitation
```

```text
test leakage
→ invalidity
```

This distinction must remain clear.

---

# 96. ETHICAL ACCEPTANCE CRITERIA

The project is ethically well-bounded when:

1. public EEG data are used responsibly;
2. subject anonymity is preserved;
3. no re-identification is attempted;
4. no clinical claim is made;
5. no thought-reading claim is made;
6. prerecorded EEG is labeled accurately;
7. simulated safety is labeled accurately;
8. human authority is preserved;
9. failure cases are not hidden;
10. uncertainty is not presented as certainty;
11. no unsupported demographic inference is performed;
12. final claims remain evidence-based.

---

# 97. VALIDITY ACCEPTANCE CRITERIA

The project is scientifically defensible when:

1. train/test leakage is controlled;
2. subject leakage is controlled;
3. calibration fitting is test-protected;
4. true goal remains evaluation-only;
5. Bayesian likelihood semantics are explicit;
6. A/B/C/D comparisons are fair;
7. ablations isolate components;
8. metrics are defined before final interpretation;
9. subject/seed variability is preserved;
10. negative outcomes remain visible;
11. result artifacts are reproducible;
12. claims are bounded to the tested scope.

---

# 98. CURRENT LIMITATIONS, ETHICS & VALIDITY SUMMARY

The NeuroCognitive Shared Autonomy project is a software research prototype that combines prerecorded motor-imagery EEG, machine-learning decoding, probability calibration, Bayesian intent inference, uncertainty-aware shared autonomy, A* navigation, and explicit simulated safety constraints in a 2D Search & Rescue scenario. Its strongest limitations are that EEG is offline rather than live, the initial BCI is binary, the motor-imagery dataset does not directly encode rescue semantics, the exact EEG-to-goal likelihood mapping remains unresolved, and there is no human-subject or physical-robot validation. Calibration and Bayesian confidence remain distribution/model dependent, subject variability may be substantial, adaptation is intentionally limited, and the simulated safety layer cannot support real-world safety certification claims. Ethical boundaries require preserving dataset anonymity, avoiding clinical or thought-reading claims, preserving human override/stop authority, presenting uncertainty honestly, and reporting failures rather than only successful cases. Internal validity depends on leakage control and fair baselines; construct validity depends on precise use of terms such as intent, uncertainty, cognition, and safety; external validity is limited by the public prerecorded dataset and simulation; and reproducibility depends on Git, configuration snapshots, experiment logs, and verified AI-assisted code. These boundaries do not invalidate the project—they define the scope within which its conclusions can be scientifically credible.

---

# 99. NEXT DOCUMENT

The next planned document is:

**`21_LITERATURE_AND_SCIENTIFIC_FOUNDATION.md` — Literature Review, Scientific Foundations, Key References, and Evidence Map**

That document should organize the research foundation for:

- motor-imagery EEG;
- ERD/ERS;
- CSP;
- LDA;
- EEGNet;
- BCI uncertainty;
- probability calibration;
- Bayesian intent inference;
- shared autonomy;
- human–AI interaction;
- safety-aware autonomy;
- adaptive/personalized BCI;
- and Search & Rescue autonomy.

It should distinguish:

```text
foundational references
current project design decisions
future optional research directions
```

and should not fabricate citations or publication claims.
