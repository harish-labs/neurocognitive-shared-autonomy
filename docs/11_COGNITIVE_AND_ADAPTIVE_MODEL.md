# 11_COGNITIVE_AND_ADAPTIVE_MODEL.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Cognitive Abstraction, Human Intent Representation, Adaptation, Personalization, and Correction-Driven System Adjustment

**Document ID:** F-02  
**Document class:** Mathematics & Cognition / Cognitive & Adaptive Model Specification  
**Authority level:** Subordinate to the Master Authority Documents and all previously approved scenario, architecture, data, neuroscience, EEG/ML, calibration/uncertainty, and Bayesian-inference specifications  
**Status:** Authoritative cognitive/adaptation baseline; the exact adaptation mechanism remains explicitly unresolved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND NON-OVERCLAIMING RULE

This document defines what the project means by:

- cognitive modelling;
- latent human intention;
- belief;
- evidence accumulation;
- correction;
- adaptation;
- personalization;
- and user-specific adjustment.

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

If this document conflicts with a higher-authority document, the higher-authority document wins.

This document must not silently convert the project into:

- a full cognitive architecture;
- a model of human consciousness;
- a psychological theory of decision-making;
- a neuroscience model of how the brain performs Bayesian inference;
- a co-adaptive live BCI;
- or an adaptive-control-theory project beyond what is actually implemented.

The current project uses a **limited computational cognitive abstraction**.

The exact adaptation mechanism remains unresolved and must not be selected without explicit approval.

---

# 1. PURPOSE OF THIS DOCUMENT

This document answers:

> **What does “cognitive” mean in this project?**

> **What exactly is being adapted?**

> **How can human corrections influence future behavior?**

> **What is the difference between Bayesian belief updating and adaptation?**

> **How can personalization be added without creating unsupported claims?**

> **How do we prevent adaptation from making the system unstable or scientifically uninterpretable?**

---

# 2. LIMITED MEANING OF “COGNITIVE”

The project uses the term **cognitive** in a deliberately narrow computational sense.

The system models:

- latent human intention;
- uncertainty about intention;
- prior belief;
- evidence accumulation;
- posterior belief;
- correction history;
- confidence-dependent action;
- and optional personalization from prior interactions.

Therefore the cognitive layer is:

> **a computational model of the system's belief about what the human intends and how that belief should be adjusted over time.**

It is not:

- a complete model of human cognition;
- a model of consciousness;
- a theory of perception;
- a theory of emotion;
- a general cognitive architecture.

---

# 3. WHY “NEUROCOGNITIVE” IS JUSTIFIED

The project title combines:

## Neuro

- real EEG;
- motor imagery;
- neural decoding;
- BCI input.

## Cognitive

- latent intention;
- prior belief;
- Bayesian evidence accumulation;
- uncertainty;
- correction;
- adaptation/personalization.

The term is justified only because both aspects are implemented.

If the Bayesian/cognitive layer were removed, the term would need reassessment.

---

# 4. COGNITIVE STATE

The cognitive state of the system is not the environment state.

A conceptual cognitive state may contain:

```text
current goal hypotheses
current posterior belief
current uncertainty
previous corrections
user/system reliability estimate
current adaptation parameters
current interaction context
```

This state must remain separate from:

```text
agent position
hazards
obstacles
path
task completion
```

---

# 5. LATENT HUMAN INTENTION

The project treats the human's intended objective as a latent variable.

The system cannot directly observe:

```text
true human goal
```

during ordinary inference.

Instead, it observes:

```text
EEG-derived evidence
```

and maintains probabilistic belief.

This is why the architecture uses:

```text
EEG decoder
→ calibrated evidence
→ Bayesian goal inference
```

rather than:

```text
EEG classifier
→ unquestioned command
```

---

# 6. BELIEF VS ADAPTATION

These are different processes.

## Bayesian belief update

Occurs during an inference sequence.

Conceptually:

```text
prior
+ current evidence
→ posterior
```

It answers:

> What does the system currently believe?

## Adaptation

Changes some parameter of future inference/control based on interaction history.

Conceptually:

```text
correction history
+ performance history
→ parameter update
```

It answers:

> What should the system change for future decisions?

Do not merge these concepts.

---

# 7. SHORT-TERM STATE VS LONGER-TERM ADAPTATION

A useful distinction is:

## Short-term

Within one goal-selection episode:

- posterior;
- entropy;
- current confidence;
- evidence count.

## Longer-term

Across repeated selections/episodes:

- user-specific prior;
- reliability estimate;
- threshold;
- evidence weighting;
- another approved adaptation variable.

The exact timescale is not locked yet.

---

# 8. WHY ADAPTATION EXISTS IN THIS PROJECT

Motor-imagery EEG can vary substantially between users.

The system may also observe patterns such as:

- repeated wrong interpretations;
- repeated high-confidence errors;
- frequent human overrides;
- excessive deferrals;
- consistent user-specific decoder reliability.

A static system may ignore this information.

The adaptation layer exists to investigate whether limited, interpretable personalization can improve future interaction.

---

# 9. ADAPTATION IS NOT REQUIRED TO BE COMPLEX

The project does not need advanced adaptive control theory.

A scientifically valid adaptation mechanism may be simple if it is:

- explicit;
- measurable;
- reproducible;
- interpretable;
- and tested.

Potential adaptation targets already approved conceptually include:

- priors;
- decoder reliability;
- confidence thresholds;
- evidence weights;
- user-specific correction statistics.

---

# 10. EXACT ADAPTATION MECHANISM — UNRESOLVED

The project has **not** approved one final adaptation mechanism.

The following remain candidates:

1. user-specific prior adaptation;
2. decoder reliability adaptation;
3. confidence-threshold adaptation;
4. evidence-weight adaptation;
5. another explicitly approved simple personalization rule.

No candidate may be silently treated as final.

---

# 11. ADAPTATION MUST BE SWITCHABLE

The architecture requires:

```text
adaptation ON
```

and:

```text
adaptation OFF
```

conditions.

This is necessary for:

- ablation;
- debugging;
- comparison;
- reproducibility.

The full system must not become dependent on adaptation being permanently enabled.

---

# 12. USER-SPECIFIC PRIOR ADAPTATION — CANDIDATE

One possible adaptation is to modify the initial prior over goal hypotheses.

Conceptually:

\[
P_0(G)
\]

could change based on prior interaction history.

Potential information might include:

- repeated choice tendencies;
- recent correction history;
- scenario context.

However:

> A prior must not be changed merely to match hidden test ground truth.

Any prior adaptation must use only information legitimately available before the current decision.

---

# 13. PRIOR ADAPTATION RISKS

Risks include:

- reinforcing previous mistakes;
- creating bias toward frequently selected goals;
- preventing recovery when user intention changes;
- leaking experimental target information.

Therefore any prior adaptation requires:

- bounded updates;
- logging;
- reset strategy;
- ablation.

---

# 14. DECODER RELIABILITY ADAPTATION — CANDIDATE

The system may maintain a user-specific estimate of how reliable the EEG decoder has been.

Conceptual variable:

\[
r_u
\]

for user \(u\).

This estimate might later influence:

- evidence strength;
- threshold;
- confidence interpretation.

Exact mathematics remain unresolved.

---

# 15. RELIABILITY ESTIMATE MUST BE BASED ON OBSERVABLE FEEDBACK

Possible sources of reliability evidence include:

- explicit human correction;
- confirmed successful selection;
- repeated disagreement between inferred and confirmed choice.

The hidden true goal from experimental metadata must not be used operationally unless the experiment explicitly models external supervision.

---

# 16. CONFIDENCE-THRESHOLD ADAPTATION — CANDIDATE

A system might adapt:

```text
high-confidence threshold
```

or:

```text
defer threshold
```

for a particular user.

For example, a user with less reliable EEG decoding might require stronger evidence before autonomous commitment.

However, threshold adaptation can create instability.

It remains unapproved until a precise rule is selected.

---

# 17. THRESHOLD-ADAPTATION RISKS

Potential risks:

- thresholds becoming too conservative;
- endless deferral;
- thresholds becoming too permissive;
- premature commitment;
- adaptation to noise rather than user behavior;
- inconsistent experimental comparisons.

Therefore thresholds must be:

- bounded;
- versioned;
- reversible;
- logged.

---

# 18. EVIDENCE-WEIGHT ADAPTATION — CANDIDATE

A possible mechanism is to scale how strongly new evidence influences Bayesian belief.

Conceptually:

```text
base likelihood
→ reliability-weighted likelihood
```

or another justified formulation.

This is scientifically sensitive because an arbitrary transformation can distort Bayesian semantics.

Therefore:

> **No evidence-weight adaptation may be implemented until the base likelihood model itself is approved.**

---

# 19. CORRECTION HISTORY

The adaptation module may maintain a correction history.

Conceptually:

```text
episode ID
selection ID
candidate goal
human confirmation / override
model confidence
posterior
uncertainty
final approved goal
adaptation action
```

This history supports:

- personalization;
- analysis;
- debugging.

---

# 20. HUMAN OVERRIDE AS A SIGNAL

An override indicates that the system's current interpretation should not be executed.

It may also provide evidence for future adaptation.

However:

> An override is first and foremost a human-authority action.

Adaptation is secondary.

The system must respect the override even if adaptation is disabled.

---

# 21. HUMAN CONFIRMATION AS A SIGNAL

Confirmation indicates that the human accepted the current inferred/selected objective.

It may later contribute to reliability statistics.

However, confirmation should not automatically be treated as perfect ground truth without considering the experiment design.

The adaptation protocol must define what feedback means.

---

# 22. FALSE CONFIRMATION / HUMAN ERROR

A real human may make mistakes.

The current core project uses simulated/offline interaction rather than a human-subject study.

Therefore the adaptation mechanism should not overclaim that human feedback is always correct in real use.

The project's simulated feedback assumptions must be documented.

---

# 23. ADAPTATION INPUT CONTRACT

Conceptually:

```text
AdaptationObservation:
    subject_id
    selection_id
    model_id
    candidate_goal
    approved_goal
    human_action
    posterior
    entropy
    model_confidence
    task_outcome
```

The exact fields depend on the approved adaptation mechanism.

---

# 24. ADAPTATION OUTPUT CONTRACT

Conceptually:

```text
AdaptationUpdate:
    parameter_name
    previous_value
    new_value
    reason
    source_observation_ids
    adaptation_policy_id
```

This makes every update traceable.

---

# 25. ADAPTATION MODULE FILE

Approved architecture:

```text
src/cognition/adaptation.py
```

Responsibilities:

- maintain approved adaptation state;
- consume allowed interaction feedback;
- update approved parameters;
- log changes;
- expose current personalization state;
- reset when required.

It must not:

- decode EEG;
- perform A*;
- override human control;
- modify safety constraints silently.

---

# 26. BASELINE MODE

The adaptation module must support:

```text
adaptation_enabled = false
```

In this condition:

- prior/threshold/reliability remain fixed;
- the rest of the system continues functioning.

This provides the mandatory ablation baseline.

---

# 27. PERSONALIZATION STATE

If adaptation is implemented, each user/subject may have a personalization state.

Conceptually:

```text
PersonalizationState:
    subject_id
    prior_parameters
    reliability_parameters
    threshold_parameters
    update_count
    last_updated
    policy_id
```

Only fields actually implemented should exist.

---

# 28. SUBJECT ID VS HUMAN ID

The PhysioNet dataset uses subject identifiers.

These are dataset subject IDs.

The project should not imply:

- known real-world identity;
- demographic identity;
- clinical identity.

Personalization should operate on the dataset's anonymous subject identifier.

---

# 29. COLD START

A new subject may have no adaptation history.

Therefore the system needs a default baseline state.

Possible default:

- uniform prior;
- global reliability estimate;
- global thresholds.

Exact initialization remains unresolved.

---

# 30. ADAPTATION WARM-UP

The system may need a minimum amount of feedback before adaptation becomes active.

The exact warm-up count remains unresolved.

This can prevent large changes from one early event.

---

# 31. BOUNDED ADAPTATION

Any adaptive parameter should have reasonable bounds.

Example concept:

```text
min_threshold ≤ threshold ≤ max_threshold
```

or:

```text
0 < reliability ≤ 1
```

Exact bounds remain unresolved.

The reason is to prevent unstable drift.

---

# 32. UPDATE RATE

Adaptation can be:

- fast;
- slow;
- per-event;
- per-episode.

The exact update rate is unresolved.

A slower update may be easier to interpret and more stable.

No learning-rate style parameter should be chosen arbitrarily.

---

# 33. FORGETTING / DECAY

A future adaptation mechanism may use decay so old interaction history has less influence.

Status:

> optional, not approved.

The core does not require forgetting.

---

# 34. RESET / CLEAR PERSONALIZATION

The system should support clearing adaptation state.

Possible reasons:

- new experiment;
- new user;
- ablation;
- corrupted state;
- controlled comparison.

Reset must be explicit and logged.

---

# 35. ADAPTATION MUST NOT MODIFY RAW EEG

Adaptation should operate on:

- priors;
- thresholds;
- reliability;
- evidence interpretation;

or another approved control parameter.

It should not edit the raw PhysioNet EEG.

---

# 36. ADAPTATION MUST NOT MODIFY TEST LABELS

Labels remain source truth for offline evaluation.

No personalization rule may alter:

```text
left/right ground-truth label
```

to improve model performance.

---

# 37. ADAPTATION AND MODEL RETRAINING

Retraining EEGNet or CSP/LDA per user is a different adaptation category.

The current adaptation concept does not require repeated model retraining.

Model retraining may be considered later but is not part of the locked core.

---

# 38. CO-ADAPTIVE BCI STATUS

A true co-adaptive BCI may involve:

```text
human adapts to machine
+
machine adapts to human
```

The current project does not directly study human learning because it uses prerecorded EEG.

Therefore:

> **The project must not claim full co-adaptive BCI behavior.**

It may claim:

> **system-side personalization/adaptation**

if actually implemented.

---

# 39. COGNITIVE MODEL COMPONENTS

The project's limited cognitive abstraction consists of:

1. latent intention;
2. prior belief;
3. incoming evidence;
4. Bayesian update;
5. posterior;
6. uncertainty;
7. human confirmation/override;
8. optional adaptation from history.

This is the approved conceptual boundary.

---

# 40. COGNITIVE MODEL FLOW

```text
EEG evidence
        ↓
Bayesian belief
        ↓
posterior
        ↓
uncertainty
        ↓
shared-autonomy action
        ↓
human correction / confirmation
        ↓
adaptation module if enabled
        ↓
future prior / reliability / threshold
```

---

# 41. ADAPTATION DOES NOT REPLACE BAYES

A system that changes thresholds over time but does not perform Bayesian updates is not the approved architecture.

Similarly, Bayesian belief update does not automatically count as adaptation.

Both are separate.

---

# 42. ADAPTATION DOES NOT REPLACE CALIBRATION

Calibration improves probability reliability.

Adaptation changes parameters based on interaction history.

They must remain separate.

A subject-specific calibrator could be considered a personalization mechanism later, but it is not currently the approved adaptation method.

---

# 43. ADAPTATION DOES NOT REPLACE SAFETY

Even if the system adapts successfully, safety constraints remain mandatory.

Adaptation must never learn to disable hard safety rules merely because doing so reduces task time.

---

# 44. HARD SAFETY PARAMETERS MUST NOT ADAPT AUTOMATICALLY

Hard constraints such as:

```text
blocked cell = forbidden
emergency stop = stop
```

must not be modified by ordinary personalization.

Adaptive logic may affect:

- confidence;
- priors;
- evidence;

not fundamental safety authority.

---

# 45. ADAPTATION AND AUTONOMY LEVEL

A future adaptation mechanism may influence how much evidence is required before autonomy proceeds.

This can indirectly change autonomy level.

However the human retains:

- override;
- pause;
- stop.

Adaptation cannot remove those rights.

---

# 46. HUMAN AUTHORITY PRECEDENCE

Control precedence should remain:

```text
Emergency stop
    highest authority

Human override / pause
    above autonomous commitment

Safety controller
    can reject unsafe actions

Shared-autonomy policy
    governs assistance

Adaptation
    modifies approved parameters only
```

Adaptation is never the highest authority.

---

# 47. ADAPTATION SCIENTIFIC QUESTION

The conditional research question is:

> **If the approved adaptation mechanism is implemented, does adaptation from user corrections or interaction history improve later shared-autonomy decisions?**

This question remains conditional because the exact mechanism is unresolved.

---

# 48. WORKING ADAPTATION HYPOTHESIS

A working hypothesis is:

> **A simple user-specific adaptation mechanism may reduce repeated incorrect commitments, unnecessary confirmations, or decision latency over repeated interactions.**

This is not guaranteed.

It must be testable.

---

# 49. POSSIBLE ADAPTATION METRICS

Potential evaluation measures include:

- wrong-goal rate before vs after adaptation;
- confirmation rate;
- override rate;
- decision latency;
- posterior confidence;
- task success;
- safety outcome;
- adaptation stability;
- number of updates.

The final Metrics document will define exact metrics.

---

# 50. ADAPTATION BASELINE COMPARISON

At minimum, if adaptation is implemented:

```text
Fixed system
vs
Adaptive system
```

must be comparable under equivalent experimental conditions.

Do not compare:

```text
adaptive system on easy episodes
vs
fixed system on harder episodes
```

without explicit reason.

---

# 51. ADAPTATION ABLATION

The required ablation is:

```text
Full system
vs
Full - adaptation
```

The project architecture must make this possible without retraining or rewriting unrelated modules.

---

# 52. ADAPTATION LEARNING CURVE

A useful output may show:

```text
x-axis:
interaction / episode number

y-axis:
selected adaptation metric
```

Possible examples:

- reliability estimate;
- threshold;
- wrong-goal rate;
- intervention rate.

This is only meaningful if the chosen adaptation mechanism evolves across interactions.

---

# 53. PRE-ADAPTATION VS POST-ADAPTATION

If the mechanism supports it, compare:

```text
initial state
vs
adapted state
```

on appropriately controlled data.

Do not evaluate on the same feedback examples used to update the adaptation and then call that generalization.

---

# 54. TRAINING / ADAPTATION / TEST SEPARATION

If adaptation learns from labeled feedback, experiments must define:

- adaptation data;
- post-adaptation evaluation data.

The system must not adapt using the same final test episode and then score that episode as if it was unseen.

The exact adaptation evaluation protocol remains unresolved.

---

# 55. ONLINE-STYLE SIMULATION

The project may simulate sequential adaptation:

```text
Episode 1
→ feedback
→ update

Episode 2
→ feedback
→ update

Episode 3
→ evaluate next behavior
```

This is valid as an offline simulation if the data order is explicitly defined.

It is still not live EEG acquisition.

---

# 56. ORDER EFFECTS

Adaptation results may depend on the order of interactions.

Therefore experiment logs should preserve:

```text
episode order
subject
feedback history
adaptation state
```

Randomized or fixed ordering must be reproducible.

---

# 57. NO INFORMATION FROM THE FUTURE

An adaptation update at time \(t\) must not use:

- future test trial labels;
- future human corrections;
- future episode outcomes.

This is another form of leakage.

---

# 58. USER RELIABILITY VS MODEL RELIABILITY

Use terminology carefully.

The project should prefer:

> **decoder reliability for a given subject**

rather than:

> **user reliability**

when referring to model performance.

The human is not “unreliable” simply because the model fails to decode their EEG.

---

# 59. HUMAN-ERROR MODELS — NOT CORE

The project does not currently require a probabilistic model of human confirmation mistakes.

If simulated human errors are later added, they must be clearly defined.

They are not part of the locked adaptation design.

---

# 60. ADAPTATION AND FAIRNESS

Personalization can improve one subject while harming another.

Therefore report:

- subject-wise effects;
- aggregate effects;
- negative cases.

Do not present only subjects who benefit.

---

# 61. ADAPTATION FAILURE CASES

The system should be able to analyze:

## Over-adaptation

One correction causes an excessive parameter shift.

## Wrong-direction adaptation

System becomes more likely to make the same mistake.

## Instability

Threshold/prior oscillates.

## No useful adaptation

Parameter changes but behavior does not improve.

## Excessive conservatism

Adaptation increases confirmation/defer rate too much.

## Excessive permissiveness

Adaptation commits too easily.

## Cross-subject inconsistency

Mechanism helps some subjects but harms others.

---

# 62. ADAPTATION SAFEGUARDS

Depending on the selected mechanism, safeguards may include:

- bounded parameters;
- minimum evidence before update;
- limited update magnitude;
- reset ability;
- versioned policy;
- explicit logging.

These safeguards are conceptually approved.

Exact formulas remain unresolved.

---

# 63. DETERMINISTIC VS STOCHASTIC ADAPTATION

A deterministic rule is preferable initially because it is easier to verify.

A stochastic adaptation algorithm is not required.

If stochasticity is introduced:

- seed it;
- log it;
- justify it.

---

# 64. SIMPLE IS PREFERRED

A good adaptation mechanism for this project should ideally be:

```text
small
interpretable
modular
testable
```

rather than:

```text
large
opaque
deep-learning based
difficult to ablate
```

This follows the project-wide principle of scientific clarity over unnecessary complexity.

---

# 65. NO RL-BASED ADAPTATION REQUIREMENT

Reinforcement learning is not required for adaptation.

A PPO agent is optional future work only.

Do not use RL simply because adaptation sounds like a learning problem.

---

# 66. NO LLM-BASED PERSONALIZATION

The system does not need:

- LLM memory;
- RAG;
- natural-language user modelling.

Adaptation is numerical/control-oriented.

---

# 67. NO CLOUD PROFILE STORE

User personalization can be stored locally in structured files.

No cloud database is required.

---

# 68. PERSONALIZATION STORAGE

A simple local representation is sufficient.

Conceptual format:

```text
subject_id
policy_id
parameter values
update count
history reference
```

Possible storage:

- JSON;
- CSV;
- another transparent format.

No database is required.

---

# 69. VERSIONING

Each adaptation policy should have an ID.

Example:

```text
adaptation_policy_v001
```

Every experiment should record:

- policy ID;
- initial parameters;
- final parameters;
- update events.

---

# 70. REPRODUCIBILITY

Every adaptation result must be reconstructable from:

```text
initial personalization state
interaction order
feedback
update rule
parameter bounds
random seed if any
code commit
```

Without this, the adaptation result is not reproducible.

---

# 71. CONFIGURATION

Conceptual configuration:

```yaml
adaptation:
  enabled: false
  policy: TBD
  target: TBD
  update_rate: TBD
  min_history: TBD
  bounds: TBD
  reset_each_subject: true
```

`TBD` is intentional.

---

# 72. STATE SEPARATION BY SUBJECT

Adaptation state must not leak between subjects unless the experiment explicitly defines a global/shared adaptation mechanism.

Default safe concept:

```text
Subject A state
≠
Subject B state
```

---

# 73. CROSS-SUBJECT PERSONALIZATION

A future experiment might initialize new-subject parameters from population estimates.

Status:

> optional and unresolved.

The core does not require population-level transfer learning.

---

# 74. ADAPTATION AND CROSS-SUBJECT GENERALIZATION

These answer different questions.

## Cross-subject generalization

Can the system work on unseen subjects before personalization?

## Adaptation

Can the system improve after receiving subject-specific interaction feedback?

Both may be studied, but they must not be conflated.

---

# 75. MODEL RETRAINING VS PARAMETER ADAPTATION

The project should distinguish:

```text
retrain EEG decoder
```

from:

```text
adapt shared-autonomy/cognitive parameter
```

The intended initial adaptation mechanism is more likely to affect the second category.

No retraining-based personalization is locked.

---

# 76. ADAPTATION WITH SYNTHETIC INPUTS

Before real EEG integration, adaptation can be tested using synthetic probability/posterior sequences.

This allows controlled verification of:

- update direction;
- bounds;
- reset;
- ablation.

Synthetic adaptation tests are not research results.

---

# 77. UNIT TESTS — ADAPTATION

Once a mechanism is approved, tests should verify:

- deterministic update for known input;
- parameter bounds;
- no update when disabled;
- reset behavior;
- subject separation;
- no update from invalid feedback;
- history recording;
- save/load behavior.

---

# 78. UNIT TEST — ADAPTATION OFF

With:

```text
adaptation.enabled = false
```

the same input sequence should leave adaptation parameters unchanged.

This is essential for ablation validity.

---

# 79. UNIT TEST — BOUNDS

If a parameter has:

```text
minimum
maximum
```

repeated updates must never exceed the approved bounds.

---

# 80. UNIT TEST — SUBJECT ISOLATION

Updating Subject A must not change Subject B state.

---

# 81. INTEGRATION TEST

Conceptual test:

```text
synthetic belief
→ shared-autonomy decision
→ human override
→ adaptation update
→ next selection
```

Verify that the adaptation target changes only as intended.

No real EEG required for this early integration test.

---

# 82. ADAPTATION DATA CONTRACT WITH BAYES

If prior adaptation is chosen, the interface should be explicit:

```text
adaptation state
→ new prior
→ Bayesian reset/init
```

Do not mutate the Bayesian posterior in place without recording the event.

---

# 83. ADAPTATION DATA CONTRACT WITH UNCERTAINTY

If threshold adaptation is chosen:

```text
adaptation state
→ confidence policy parameters
```

The uncertainty calculation itself remains unchanged.

For example:

```text
entropy formula
```

should not change merely because thresholds adapt.

---

# 84. ADAPTATION DATA CONTRACT WITH CALIBRATION

If decoder reliability is adapted, the relationship to calibrated probabilities must be explicitly defined.

Do not silently recalibrate probabilities through an unrelated reliability scalar.

---

# 85. ADAPTATION AND GOAL MAPPING

The critical binary EEG-to-goal mapping remains unresolved.

Adaptation must not be used to hide this design problem.

For example:

```text
learn a mapping from Left/Right to arbitrary goal
```

is not an approved substitute for defining the BCI interaction protocol.

---

# 86. ADAPTATION AND MULTI-GOAL INTERFACE

Once the goal-selection protocol is approved, adaptation may personalize behavior inside that protocol.

Examples conceptually:

- user-specific prior within current two choices;
- confidence threshold for each user.

It does not decide the protocol itself.

---

# 87. COGNITIVE MODEL AND HUMAN-AI INTERACTION

The cognitive layer should support the shared-autonomy principle:

```text
Human:
WHAT

AI:
HOW
```

The system may infer the human's current intended choice probabilistically.

It must not infer that the human should want another goal.

---

# 88. COGNITIVE MODEL AND SAFETY

A highly confident inferred goal can still produce an unsafe path.

Therefore:

```text
posterior confidence
```

does not override:

```text
safety controller
```

The safety layer remains independent.

---

# 89. COGNITIVE MODEL AND PLANNING

The cognitive system should not bias intention belief based merely on route convenience.

Example invalid logic:

```text
Victim A is closer
→ increase P(human wants Victim A)
```

unless a future explicit cognitive model justifies that context.

Current baseline must not do this.

---

# 90. ADAPTATION PERFORMANCE SHOULD BE SECONDARY TO CORRECTNESS

If adaptation introduces scientific ambiguity or invalid leakage, it should not be retained merely because it improves a metric.

The priority remains:

1. scientific correctness;
2. valid evaluation;
3. reproducibility;
4. performance.

---

# 91. NEGATIVE ADAPTATION RESULTS ARE VALID

Possible outcomes include:

- adaptation improves some users;
- adaptation harms some users;
- adaptation has no meaningful effect;
- adaptation reduces errors but increases delay;
- adaptation reduces confirmations but increases wrong commitment.

All are valid if measured honestly.

---

# 92. CLAIM BOUNDARIES — ADAPTIVE

Allowed if implemented:

> “The system adapts user-specific priors based on correction history.”

Allowed if implemented:

> “The system updates a subject-specific decoder reliability estimate.”

Allowed if implemented:

> “Confidence thresholds are personalized over repeated interactions.”

Not allowed without implementation:

> “The system learns each user's cognitive style.”

Not allowed:

> “The AI learns the user's mind.”

Not allowed:

> “The system models neuroplasticity.”

---

# 93. CLAIM BOUNDARIES — COGNITIVE

Allowed:

> “The system maintains a probabilistic latent-intent belief state.”

Allowed:

> “The system accumulates evidence and updates belief sequentially.”

Allowed:

> “Human correction can inform future personalization.”

Not allowed:

> “The system replicates human cognition.”

Not allowed:

> “The system understands human intent like a person.”

---

# 94. ADAPTIVE CONTROL TERMINOLOGY

The project title currently contains:

> **Uncertainty-Aware Adaptive Control**

This wording must remain aligned with actual implementation.

If the final implemented adaptation is only:

- prior adaptation;
- threshold adaptation;
- reliability adjustment;

then the report should say exactly that.

Do not imply:

- model predictive adaptive control;
- nonlinear adaptive control theory;
- formal stability proofs;

unless those are actually implemented.

---

# 95. POSSIBLE FUTURE STRONGER ADAPTATION

Future work may include:

- co-adaptive BCI;
- online decoder recalibration;
- personalized EEG fine-tuning;
- active learning;
- RL-based shared autonomy;
- hierarchical user models.

These are not core requirements.

---

# 96. ADAPTATION EXPERIMENT DESIGN REQUIREMENTS

If adaptation is included in final experiments, define:

1. adaptation target;
2. update rule;
3. initialization;
4. update frequency;
5. bounds;
6. feedback source;
7. subject separation;
8. adaptation sequence;
9. evaluation period;
10. reset condition.

Without these, adaptation results are not interpretable.

---

# 97. ADAPTATION LOG

Each update should record:

```text
subject
episode
selection
human action
candidate goal
approved goal
pre-update parameter
post-update parameter
posterior
entropy
update reason
policy ID
```

This creates auditability.

---

# 98. ADAPTATION RESULTS

Final results should report both:

```text
behavioral effect
```

and:

```text
parameter evolution
```

where relevant.

A changed parameter alone does not prove useful adaptation.

---

# 99. FAILURE ANALYSIS

A final adaptation analysis should include:

- representative beneficial case;
- representative harmful case;
- no-effect case;
- instability case if observed;
- subject-specific variation.

Do not show only successful adaptation trajectories.

---

# 100. IMPLEMENTATION ORDER

Recommended order:

## Stage 1

Implement Bayesian core without adaptation.

## Stage 2

Implement uncertainty and shared-autonomy policy.

## Stage 3

Collect synthetic correction-history examples.

## Stage 4

Select adaptation target/method through explicit approval.

## Stage 5

Implement adaptation as a separate module.

## Stage 6

Unit-test and bound updates.

## Stage 7

Run adaptation ON/OFF experiments.

## Stage 8

Integrate real EEG-derived evidence.

---

# 101. CODEX TASK BOUNDARY — ADAPTATION SKELETON

Before mechanism approval, Codex may only create a minimal interface/skeleton if needed.

Example:

> Implement the adaptation module interface and state container only. Support adaptation enabled/disabled, reset, subject-isolated state, and logging hooks. Do not implement any actual parameter-update rule until the adaptation mechanism is explicitly approved.

This avoids accidental scientific decisions.

---

# 102. CODEX TASK AFTER APPROVAL

Once the adaptation mechanism is approved, the implementation ticket must specify:

- exact formula;
- exact target parameter;
- inputs;
- bounds;
- update timing;
- reset rule;
- tests;
- ablation requirement.

Codex must not improvise beyond that ticket.

---

# 103. OPEN DECISIONS — MUST REMAIN OPEN

## 103.1 Adaptation target

Not locked.

## 103.2 Update formula

Not locked.

## 103.3 Update frequency

Not locked.

## 103.4 Parameter bounds

Not locked.

## 103.5 Minimum history/warm-up

Not locked.

## 103.6 Forgetting/decay

Not locked.

## 103.7 Feedback semantics

Not fully locked.

## 103.8 Prior adaptation

Candidate only.

## 103.9 Reliability adaptation

Candidate only.

## 103.10 Threshold adaptation

Candidate only.

## 103.11 Evidence-weight adaptation

Candidate only and dependent on approved likelihood model.

No implementation agent may silently select among them.

---

# 104. DECISIONS REQUIRED BEFORE FINAL ADAPTATION EXPERIMENTS

Explicitly approve:

1. adaptation target;
2. update rule;
3. feedback source;
4. initialization;
5. subject-specific/global scope;
6. update frequency;
7. bounds;
8. warm-up;
9. reset policy;
10. evaluation protocol;
11. ablation condition;
12. claim wording.

Record these in `DECISIONS.md`.

---

# 105. ACCEPTANCE CRITERIA — COGNITIVE MODEL

The cognitive model is correctly represented when:

1. human intention is treated as latent;
2. belief state is separate from environment state;
3. Bayesian inference is separate from adaptation;
4. posterior and uncertainty are explicit;
5. human confirmation/override are represented;
6. true goal remains evaluation-only;
7. cognitive terminology remains limited and accurate;
8. no brain-level cognitive mechanism is falsely claimed.

---

# 106. ACCEPTANCE CRITERIA — ADAPTATION MODULE

The adaptation module is complete only if:

1. a specific mechanism is explicitly approved;
2. the update rule is documented mathematically or procedurally;
3. the target parameter is explicit;
4. feedback source is explicit;
5. updates are bounded where necessary;
6. state is subject-isolated where required;
7. adaptation can be disabled;
8. reset is supported;
9. every update is logged;
10. no future/test information leaks into updates;
11. ON/OFF comparison is possible;
12. negative effects can be measured;
13. claims match the actual mechanism.

---

# 107. CURRENT COGNITIVE & ADAPTIVE MODEL SUMMARY

The project uses a deliberately limited computational cognitive model. Human intent is represented as a latent goal variable, EEG-derived evidence is accumulated through sequential Bayesian inference, the resulting posterior is converted into uncertainty, and shared autonomy uses that uncertainty to decide whether to proceed, confirm, or defer. Adaptation is a separate optional-but-intended layer that may personalize future behavior using correction or interaction history. Candidate adaptation targets include priors, decoder-reliability estimates, confidence thresholds, or evidence weighting, but **no final mechanism has yet been approved**. The adaptation layer must remain modular, switchable, bounded, subject-aware, traceable, and experimentally ablatable. It must never override human authority or hard safety constraints, and it must not be described as a complete cognitive architecture, co-adaptive live BCI, neuroplasticity model, or advanced adaptive-control system unless those capabilities are actually implemented.

---

# 108. NEXT DOCUMENT

The next planned document is:

**`12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md` — Shared Autonomy & Human–AI Interaction Specification**

That document should define:

- the human/AI responsibility split;
- autonomy states;
- proceed/confirm/defer/pause/stop;
- confirmation;
- override;
- pause;
- emergency stop;
- goal approval;
- human authority;
- uncertainty-dependent assistance;
- interaction state machine;
- human workload;
- intervention logging;
- failure cases;
- and HCI claim boundaries.

It must preserve all unresolved confidence thresholds and the unresolved binary EEG-to-multiple-goal interaction protocol.
