# 10_BAYESIAN_GOAL_INFERENCE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Sequential Bayesian Goal / Intent Inference, Evidence Accumulation, Belief State, and Decision-Interface Methodology

**Document ID:** F-01  
**Document class:** Mathematics & Cognition / Bayesian Inference Specification  
**Authority level:** Subordinate to the Master Authority Documents and all previously approved scenario, architecture, data, neuroscience, EEG/ML, and calibration/uncertainty specifications  
**Status:** Authoritative Bayesian-inference baseline with the EEG-to-goal evidence mapping and several decision-policy details explicitly unresolved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND NON-INVENTION RULE

This document defines the project's approved **Bayesian goal / intent inference layer**.

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

If this document conflicts with a higher-authority project document, the higher-authority document wins.

The most important scientific restriction is:

> **The exact mapping from calibrated EEG decoder output `P(class | EEG)` to the Bayesian goal-evidence / likelihood representation must not be invented ad hoc.**

The project has explicitly preserved this as an unresolved scientific issue.

Therefore this document defines:

- the Bayesian state;
- prior;
- likelihood interface;
- posterior;
- sequential update;
- numerical rules;
- testing;
- logging;
- evaluation;
- reset/commitment interfaces;
- and the required separation between EEG class evidence and application goal semantics;

while preserving the following as unresolved until explicitly approved:

- the exact Left/Right EEG-to-goal mapping;
- the exact mathematical likelihood-construction rule;
- the final prior policy;
- any goal-transition model;
- the final evidence-window/sequence policy;
- posterior commitment thresholds;
- reset timing;
- adaptation of priors/reliability;
- and the final multi-goal interaction protocol.

---

# 1. PURPOSE OF BAYESIAN GOAL INFERENCE

The Bayesian layer exists because the project does not assume that:

```text
one EEG prediction
=
true human goal
```

Instead, the operator's intended objective is treated as a **latent variable**.

EEG decoding provides imperfect evidence.

The Bayesian module accumulates that evidence sequentially and maintains a probability distribution over candidate intention hypotheses.

The central question is:

> **Given the evidence received so far, how strongly should the system currently believe each candidate human intention?**

---

# 2. LOCATION IN THE COMPLETE ARCHITECTURE

The relevant pipeline is:

```text
motor-imagery EEG
        ↓
CSP+LDA / EEGNet
        ↓
raw class probabilities
        ↓
probability calibration
        ↓
calibrated Left/Right EEG evidence
        ↓
EEG-to-goal evidence adapter
        ↓
Bayesian goal inference
        ↓
posterior belief
        ↓
entropy / uncertainty
        ↓
shared-autonomy controller
        ↓
PROCEED / CONFIRM / DEFER / PAUSE / STOP
```

The Bayesian module receives a valid **goal-hypothesis likelihood/evidence representation**.

It does not itself:

- decode raw EEG;
- calibrate model probabilities;
- assign arbitrary rescue semantics to Left/Right classes;
- plan routes;
- enforce environmental safety;
- or control Streamlit.

---

# 3. CORE PROJECT PRINCIPLE

The Bayesian layer supports the project's central responsibility split:

> **Human determines WHAT objective is intended.**

> **AI determines HOW to achieve an approved objective safely.**

The Bayesian module only reasons about the system's uncertain belief concerning the human's intended objective.

It must not decide that another rescue goal is preferable because it is:

- closer;
- safer;
- easier;
- or cheaper.

Those are planning/safety considerations, not intent inference.

---

# 4. LATENT GOAL / INTENTION VARIABLE

Let:

\[
G
\]

represent the latent human goal/intention hypothesis.

For a candidate set:

\[
\mathcal{G} = \{g_1,g_2,\ldots,g_K\}
\]

the Bayesian module maintains:

\[
P(G=g_i)
\]

for each hypothesis.

The exact semantic meaning of the hypotheses depends on the final approved BCI interaction protocol.

Possible conceptual hypotheses might eventually represent:

- two currently active rescue choices;
- two branches in a hierarchical decision;
- two abstract priority choices;
- or a future multiclass goal set.

No specific mapping is approved in this document.

---

# 5. BELIEF STATE

At update step \(t\), the Bayesian belief state is:

\[
\mathbf{b}_t
=
[
P(G=g_1\mid E_{1:t}),
\dots,
P(G=g_K\mid E_{1:t})
]
\]

where:

\[
E_{1:t}
\]

denotes all accepted evidence up to step \(t\).

The belief must satisfy:

\[
0 \le b_t(i) \le 1
\]

and:

\[
\sum_i b_t(i)=1
\]

within numerical tolerance.

---

# 6. PRIOR

Before current evidence is incorporated, the system has a prior belief:

\[
P(G)
\]

or, sequentially:

\[
P(G\mid E_{1:t-1})
\]

The prior represents the system's belief **before processing the next evidence item**.

The exact initial prior policy is not yet locked.

Possible policies may include:

- uniform prior;
- scenario-informed prior;
- user-specific learned prior;
- adaptation-derived prior.

These possibilities must not be silently substituted for one another.

---

# 7. UNIFORM PRIOR — VALID BASELINE, NOT AUTOMATIC FINAL POLICY

A uniform prior is:

\[
P(G=g_i)=\frac{1}{K}
\]

for every hypothesis.

This is a scientifically clean baseline when the system has no justified reason to prefer one goal.

However:

> **The project has not formally locked uniform priors as the final policy for every experiment.**

It is suitable for:

- unit tests;
- synthetic tests;
- baseline experiments;
- early implementation.

Any non-uniform prior must have a documented source and justification.

---

# 8. PRIOR MUST NOT CONTAIN GROUND-TRUTH LEAKAGE

The prior must never be constructed using the hidden true goal from the same test episode.

Invalid:

```text
true goal = Victim B
→ set prior Victim B = 0.9
```

unless that prior is explicitly part of a controlled experiment using legitimately available information.

The true goal may exist in experiment metadata for evaluation only.

---

# 9. EVIDENCE

Let:

\[
E_t
\]

represent the evidence presented to the Bayesian model at update step \(t\).

The source evidence ultimately originates from:

```text
prerecorded EEG
→ decoder
→ calibrated class probabilities
```

However, the Bayesian core must not assume that raw/calibrated classifier probabilities are automatically valid Bayesian likelihoods.

An explicit adapter/interface must define the evidence semantics.

---

# 10. LIKELIHOOD

The Bayesian update requires:

\[
P(E_t \mid G=g_i)
\]

for each candidate hypothesis.

This is the **likelihood** of the current evidence under each possible goal.

The core update is:

\[
P(G=g_i\mid E_{1:t})
=
\frac{
P(E_t\mid G=g_i)
P(G=g_i\mid E_{1:t-1})
}{
\sum_j
P(E_t\mid G=g_j)
P(G=g_j\mid E_{1:t-1})
}
\]

This equation is the mathematical heart of the Bayesian module.

---

# 11. THE CRITICAL PROBABILITY-SEMANTICS DISTINCTION

The EEG decoder estimates quantities such as:

\[
P(C=\text{Left}\mid EEG)
\]

and:

\[
P(C=\text{Right}\mid EEG)
\]

The Bayesian update requires:

\[
P(E\mid G)
\]

These are not automatically the same mathematical quantity.

Therefore the project must not silently do:

```text
P(Left | EEG)
→ call it P(EEG evidence | Goal A)
```

without an explicitly defined model.

This is the main scientific boundary between:

- EEG classification;
- application mapping;
- Bayesian goal inference.

---

# 12. GOAL-EVIDENCE ADAPTER

The system architecture must include a separate conceptual component:

```text
calibrated EEG class evidence
        ↓
GoalEvidenceAdapter
        ↓
Bayesian likelihood vector
```

The adapter is not the Bayesian filter itself.

Its responsibilities will eventually include:

- interpreting the currently active BCI choice structure;
- mapping class semantics to application-level hypotheses;
- constructing or retrieving a valid likelihood vector;
- preserving hypothesis order;
- recording the mapping policy.

The exact adapter mathematics are unresolved.

---

# 13. REQUIRED EVIDENCE CONTRACT

The Bayesian core should consume an object conceptually like:

```text
GoalEvidence:
    hypothesis_names
    likelihoods
    evidence_id
    source_decoder_id
    source_calibrator_id
    mapping_policy_id
    subject_id
    trial_id
```

Requirements:

\[
likelihood_i \ge 0
\]

At least one likelihood must be strictly positive.

Likelihoods do not need to sum to 1 mathematically, although a normalized likelihood vector may be convenient if the approved mapping produces one.

---

# 14. WHY LIKELIHOODS DO NOT NEED TO SUM TO ONE

For fixed evidence \(E_t\), the likelihood terms:

\[
P(E_t\mid G=g_i)
\]

are evaluated across competing hypotheses.

Bayesian normalization occurs after multiplying by the prior.

Therefore the implementation should not confuse:

```text
likelihood normalization
```

with:

```text
posterior normalization
```

If the adapter emits normalized values, that must be because of the chosen evidence model, not because Bayes requires the likelihood vector itself to sum to one.

---

# 15. SEQUENTIAL BAYESIAN UPDATE

The approved project requires **sequential evidence accumulation**.

At step \(t\):

\[
prior_t
=
posterior_{t-1}
\]

then:

\[
posterior_t
\propto
likelihood_t \odot prior_t
\]

where:

\[
\odot
\]

denotes element-wise multiplication.

Finally normalize:

\[
posterior_t(i)
=
\frac{
likelihood_t(i)\cdot prior_t(i)
}{
\sum_j likelihood_t(j)\cdot prior_t(j)
}
\]

---

# 16. CONCEPTUAL SEQUENCE

Example with abstract hypotheses:

```text
Initial belief
Goal A = 0.50
Goal B = 0.50

Evidence 1 mildly supports Goal A
        ↓
Posterior shifts toward Goal A

Evidence 2 again supports Goal A
        ↓
Posterior becomes stronger

Evidence 3 supports Goal B
        ↓
Posterior may move back toward ambiguity

More evidence
        ↓
system either gains confidence or remains uncertain
```

This is conceptual only.

No numerical values in this example are project results.

---

# 17. STATIC-GOAL ASSUMPTION — NOT YET FULLY LOCKED

The simplest sequential model assumes that the human's intended goal remains stable during one goal-selection episode.

Under that model:

```text
posterior at t-1
→ prior at t
```

without an explicit transition matrix.

This is appropriate for the minimal Bayesian filter.

However:

> **The project has not formally approved a dynamic goal-transition model or a fixed static-goal assumption for every future interaction.**

Therefore:

- the minimal core may be implemented and tested using a stable-goal episode;
- no HMM/transition matrix should be added without need;
- if goal switching becomes part of the scenario, it must be modeled explicitly.

---

# 18. NO HMM / PARTICLE FILTER REQUIREMENT

The current project does not require:

- Hidden Markov Models;
- particle filters;
- Kalman filters;
- dynamic Bayesian networks;
- probabilistic programming frameworks.

A transparent discrete Bayesian belief update is sufficient for the approved core research question.

Advanced filters are optional future work only if justified.

---

# 19. CONDITIONAL-INDEPENDENCE ASSUMPTION

A simple sequential update effectively treats each new evidence item according to a likelihood model conditioned on the goal and previous information summarized through the posterior.

If repeated EEG observations are strongly correlated, naive repeated multiplication may create excessive confidence.

Therefore the final evidence-generation protocol must consider:

- whether evidence windows are independent;
- whether they overlap;
- whether multiple predictions originate from one EEG trial;
- whether repeated use of the same evidence occurs.

This issue must be documented in the Experimental Design / Bayesian implementation.

---

# 20. DO NOT DOUBLE-COUNT EVIDENCE

Invalid example:

```text
one EEG trial
→ same probability vector duplicated five times
→ posterior becomes extremely confident
```

unless the repetition is deliberately part of a defined experimental manipulation.

Every update should reference a unique or explicitly justified evidence item.

The evidence history must allow duplicate detection.

---

# 21. EVIDENCE WINDOW / SEQUENCE POLICY — UNRESOLVED

The project has not yet locked exactly what constitutes one Bayesian update.

Possible units could include:

- one EEG epoch;
- one decoder prediction from a defined replay window;
- a sequence constructed from multiple trials;
- another approved evidence unit.

No choice is silently approved here.

The final experimental protocol must specify:

```text
what one update means
how many updates are available
when evidence accumulation stops
```

---

# 22. POSTERIOR

The posterior is:

\[
P(G\mid E_{1:t})
\]

It represents the system's current probabilistic belief about the intended goal.

The posterior is **not**:

- the EEG classifier output;
- the environment's true goal;
- a safety score;
- a planner score;
- a reward.

These quantities must remain separate.

---

# 23. POSTERIOR CONFIDENCE

A simple posterior-confidence value may be:

\[
C_t = \max_i P(G=g_i\mid E_{1:t})
\]

This indicates how strongly the current posterior favors its leading hypothesis.

However the approved uncertainty mechanism also uses entropy:

\[
H(P_t)
=
-\sum_iP_t(g_i)\log P_t(g_i)
\]

The shared-autonomy layer may consume both posterior and uncertainty according to the final policy.

---

# 24. COMMITMENT IS NOT PART OF THE BAYESIAN EQUATION ITSELF

Bayes produces a posterior.

The decision to:

```text
PROCEED
CONFIRM
DEFER
```

belongs to the shared-autonomy policy.

Therefore the Bayesian module should not hard-code final autonomy thresholds.

It should expose:

- posterior;
- leading hypothesis;
- posterior confidence;
- evidence count/history.

The uncertainty/shared-autonomy layers decide how to act.

---

# 25. COMMITMENT THRESHOLDS — UNRESOLVED

Earlier project discussion included example confidence values.

Those values remain non-authoritative.

This document does not define:

```text
if posterior > 0.8:
    commit
```

as final behavior.

Thresholds must later be selected through a defensible validation/safety trade-off.

---

# 26. RESET POLICY

The Bayesian filter needs a reset mechanism.

Possible reset events may include:

- new episode;
- new explicit goal-selection cycle;
- human override/reselection;
- completed goal;
- another approved state transition.

The exact reset policy remains partially unresolved because it depends on the final BCI interaction protocol.

The implementation must nevertheless support explicit:

```text
reset(prior=...)
```

rather than relying on hidden state clearing.

---

# 27. RESET MUST BE LOGGED

A Bayesian reset changes the belief state.

Therefore logs should record:

```text
reset event
reset reason
prior after reset
episode/selection ID
timestamp/update index
```

This is important for reproducing posterior trajectories.

---

# 28. HUMAN OVERRIDE AND BAYESIAN STATE

When the human overrides an inferred goal, the system must not continue blindly with stale belief.

The exact response remains tied to the adaptation/shared-autonomy policy.

Possible future responses include:

- reset posterior;
- start new selection cycle;
- update adaptation statistics;
- apply a corrected prior.

No specific response is locked here.

The human override must always be respected operationally.

---

# 29. HUMAN CONFIRMATION

Confirmation is not Bayesian evidence by default.

It is an explicit human-authority action.

The shared-autonomy controller may treat confirmation as:

- approval of current candidate goal;
- termination of the current inference phase.

The project should not silently insert confirmation as another probabilistic likelihood update unless a formal model explicitly defines that behavior.

---

# 30. BAYESIAN STATE MUST BE SEPARATE FROM ENVIRONMENT STATE

Environment state contains:

- agent position;
- hazards;
- obstacles;
- possible goals;
- map.

Bayesian state contains:

- goal hypotheses;
- prior;
- likelihood/evidence history;
- posterior.

The true intended experimental goal may be stored separately for evaluation.

This separation prevents leakage and conceptual confusion.

---

# 31. TRUE GOAL IS EVALUATION METADATA

For controlled experiments, the system may know externally:

```text
true_goal
```

so that researchers can calculate:

- inference accuracy;
- wrong-goal commitment;
- decision latency.

However:

> **`true_goal` must not be passed into the Bayesian update during normal inference.**

The Bayesian system should see only permitted evidence and priors.

---

# 32. BINARY EEG-TO-MULTIPLE-GOAL ISSUE — CRITICAL OPEN DECISION

The current EEG task produces evidence about:

```text
Left motor imagery
Right motor imagery
```

The Search & Rescue environment may contain:

```text
Victim A
Victim B
safe zone
medical/resource point
other mission objectives
```

A binary decoder does not directly specify an arbitrary multi-goal posterior.

The preserved options remain:

1. only two active selectable goals at a time;
2. hierarchical/sequential binary selection;
3. future multiclass EEG;
4. binary abstract priority/choice while autonomy manages broader mission structure.

**No final option is approved.**

---

# 33. CONSEQUENCE FOR THE BAYESIAN MODULE

The mathematical filter must be generic with respect to hypothesis names.

It should not assume:

```text
K = 2
```

unless a specific experiment defines two hypotheses.

Conceptual class:

```text
BayesianIntentFilter(hypotheses=[...])
```

should be able to support:

```text
2
```

or more hypotheses if the later mapping policy requires them.

However, supporting generic \(K\) hypotheses in code does **not** solve the EEG mapping problem.

---

# 34. HYPOTHESIS ORDER

Hypothesis ordering is critical.

If:

```text
likelihood = [0.8, 0.2]
```

the system must know which entry corresponds to which hypothesis.

Every evidence object and belief state must preserve:

```text
hypothesis_names
```

Do not depend on dictionary ordering, UI order, or memory.

---

# 35. NUMERICAL NORMALIZATION

Given:

\[
u_i = likelihood_i \cdot prior_i
\]

compute:

\[
Z = \sum_i u_i
\]

then:

\[
posterior_i=\frac{u_i}{Z}
\]

Requirements:

- \(Z > 0\);
- all values finite;
- posterior normalized.

If:

```text
Z = 0
```

or is non-finite, the update must fail explicitly rather than invent a posterior.

---

# 36. LOG-SPACE IMPLEMENTATION — OPTIONAL

Repeated multiplication of very small likelihoods can cause numerical underflow.

A log-space implementation may be used:

\[
\log posterior
\propto
\log prior + \log likelihood
\]

followed by stable normalization.

Status:

> **implementation option, not mandatory for the first simple system.**

If ordinary probability-space operations are numerically stable for the short sequence, they may be sufficient.

The implementation should prioritize correctness and clarity.

---

# 37. ZERO PRIOR PROBLEM

Under ordinary Bayes:

```text
prior_i = 0
```

means that hypothesis cannot recover through finite likelihood multiplication.

Therefore priors containing exact zero should only be used if the project intentionally declares a hypothesis impossible.

For ordinary uncertain candidate goals, a non-zero prior is safer.

The final prior policy must document this.

---

# 38. ZERO LIKELIHOOD PROBLEM

Likewise:

```text
likelihood_i = 0
```

can eliminate a hypothesis.

The goal-evidence adapter should not emit exact zero merely because a decoder assigned a very low probability unless the evidence model explicitly justifies impossible evidence.

The exact clipping/smoothing policy remains to be defined with the likelihood mapping.

---

# 39. EVIDENCE STRENGTH

A likelihood vector encodes how compatible the evidence is with each hypothesis.

Examples for synthetic tests may include:

```text
[0.5, 0.5]
```

uninformative between two hypotheses.

```text
[0.7, 0.3]
```

moderately favors the first.

```text
[0.95, 0.05]
```

strongly favors the first.

These are **synthetic likelihood examples**, not decoder outputs or project results.

---

# 40. SYNTHETIC TESTING IS REQUIRED BEFORE EEG INTEGRATION

The Bayesian core can and should be tested independently using synthetic likelihood sequences.

This is important because the EEG-to-goal adapter remains unresolved.

The core Bayesian math does not need to wait for that mapping decision.

---

# 41. SYNTHETIC TEST CASE A — UNINFORMATIVE EVIDENCE

Initial prior:

```text
[0.5, 0.5]
```

Likelihood:

```text
[0.5, 0.5]
```

Expected behavior:

```text
posterior remains [0.5, 0.5]
```

within numerical tolerance.

This verifies that symmetric evidence does not create false preference.

---

# 42. SYNTHETIC TEST CASE B — REPEATED SUPPORT

Initial prior:

```text
[0.5, 0.5]
```

Repeated likelihoods favor hypothesis A:

```text
[0.7, 0.3]
[0.7, 0.3]
[0.7, 0.3]
```

Expected behavior:

- posterior probability for A increases monotonically;
- posterior remains normalized;
- entropy decreases.

No exact end posterior needs to be hard-coded unless verified analytically in the unit test.

---

# 43. SYNTHETIC TEST CASE C — CONTRADICTORY EVIDENCE

Initial prior:

```text
[0.5, 0.5]
```

Sequence:

```text
[0.8, 0.2]
[0.2, 0.8]
```

Expected behavior:

- evidence pulls the posterior in opposite directions;
- final belief becomes less decisive than after the first update;
- exact result follows the defined update.

This tests recovery from conflicting evidence.

---

# 44. SYNTHETIC TEST CASE D — INFORMATIVE PRIOR

Prior:

```text
[0.8, 0.2]
```

Likelihood mildly favors B:

```text
[0.4, 0.6]
```

Expected:

- posterior incorporates both prior and evidence;
- it must not simply equal the likelihood.

This confirms real Bayesian combination.

---

# 45. SYNTHETIC TEST CASE E — THREE HYPOTHESES

Hypotheses:

```text
A
B
C
```

Prior:

```text
[1/3, 1/3, 1/3]
```

Likelihood:

```text
[0.2, 0.6, 0.2]
```

Expected:

- posterior favors B;
- all probabilities remain normalized.

This validates that the core math can support \(K>2\) even though the real EEG mapping remains unresolved.

---

# 46. SYNTHETIC TEST CASE F — INVALID INPUT

Inputs such as:

```text
negative likelihood
NaN likelihood
mismatched hypothesis count
all-zero likelihood
invalid prior normalization
```

must raise clear errors.

The module must not silently repair scientifically invalid input.

---

# 47. BELIEF HISTORY

The module should preserve a history of:

```text
prior_t
likelihood_t
posterior_t
evidence_id
update_index
```

This supports:

- debugging;
- plots;
- posterior-trajectory analysis;
- failure analysis;
- reproducibility.

---

# 48. INTENT BELIEF DATA CONTRACT

The architecture previously established a conceptual object:

```text
IntentBelief:
    hypothesis_names
    prior
    likelihood
    posterior
    update_index
    evidence_reference
```

This remains authoritative.

Useful optional fields may include:

```text
leading_hypothesis
posterior_confidence
sequence_id
```

The exact Python representation may be refined.

---

# 49. BAYESIAN FILTER STATE CONTRACT

A persistent filter object may hold:

```text
hypothesis_names
current_posterior
initial_prior
update_count
belief_history
sequence_id
```

It should expose operations such as:

```text
initialize
update
reset
get_posterior
get_history
```

---

# 50. SUGGESTED IMPLEMENTATION FILE

Approved architecture:

```text
src/cognition/bayesian_intent.py
```

This module should contain:

- probability validation;
- prior initialization;
- Bayesian update;
- posterior normalization;
- history;
- reset.

It must not contain:

- EEG preprocessing;
- calibration fitting;
- hard-coded Left→Victim mapping;
- A*;
- environment safety;
- Streamlit UI.

---

# 51. OPTIONAL GOAL-MAPPING FILE

Because the goal mapping is a separate concern, a later implementation may use a file such as:

```text
src/cognition/goal_mapping.py
```

or another architecture-consistent location.

The exact filename is not locked.

Its responsibility would be:

```text
calibrated EEG class evidence
→ goal evidence / likelihood input
```

The Bayesian core remains independent.

---

# 52. BAYESIAN MODULE UNIT TESTS

Unit tests should verify:

1. prior validation;
2. likelihood validation;
3. posterior normalization;
4. uninformative evidence behavior;
5. repeated-support behavior;
6. conflicting evidence;
7. informative-prior behavior;
8. three-hypothesis update;
9. reset behavior;
10. history tracking;
11. hypothesis-order mismatch rejection;
12. non-finite value rejection.

---

# 53. MATHEMATICAL TESTING SHOULD USE ANALYTICALLY CHECKABLE VALUES

Bayesian unit tests should not rely only on:

```text
output looks reasonable
```

Use small values where the expected posterior can be calculated independently.

Example:

Prior:

\[
[0.5,0.5]
\]

Likelihood:

\[
[0.8,0.2]
\]

Unnormalized:

\[
[0.4,0.1]
\]

Normalization constant:

\[
0.5
\]

Posterior:

\[
[0.8,0.2]
\]

This is a test of the Bayesian math only.

It is not an approved EEG likelihood mapping.

---

# 54. MULTIPLE UPDATE ANALYTIC TEST

Starting from:

\[
[0.5,0.5]
\]

Update 1 likelihood:

\[
[0.8,0.2]
\]

gives:

\[
[0.8,0.2]
\]

Then likelihood:

\[
[0.8,0.2]
\]

gives unnormalized:

\[
[0.64,0.04]
\]

and posterior:

\[
\left[
\frac{0.64}{0.68},
\frac{0.04}{0.68}
\right]
\]

This demonstrates cumulative evidence.

Again, these are synthetic test likelihoods.

---

# 55. ENTROPY HANDOFF

After each posterior update:

```text
posterior
→ uncertainty module
→ entropy
```

The Bayesian module may expose posterior confidence but should not duplicate all uncertainty-policy logic.

The uncertainty module remains responsible for:

- entropy;
- optional normalized entropy;
- confidence-state representation.

---

# 56. SHARED-AUTONOMY HANDOFF

Conceptually:

```text
IntentBelief
+
UncertaintyEstimate
+
human state
→ shared-autonomy controller
```

The shared-autonomy controller determines:

```text
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

Bayesian inference does not itself execute the rescue agent.

---

# 57. DECISION LATENCY

Sequential accumulation introduces a new measurable quantity:

> **time / number of evidence updates required before the system reaches a sufficiently reliable decision state**

Possible measurement forms include:

- number of evidence updates;
- replay time;
- decision timestamp.

The exact commitment criterion remains unresolved.

---

# 58. GOAL INFERENCE ACCURACY

If a controlled experiment defines a true intended goal, the Bayesian inference result can be evaluated as:

```text
leading posterior hypothesis
vs
true experimental goal
```

Metrics may include:

- goal inference accuracy;
- wrong-goal rate.

These are different from EEG Left/Right classification accuracy.

---

# 59. WRONG-GOAL COMMITMENT

A particularly important system metric is:

> **the system committing to a goal that does not match the controlled true intention**

This should be recorded separately from:

```text
temporary posterior leader
```

because the posterior may fluctuate before commitment.

The commitment event is defined by shared-autonomy policy.

---

# 60. PREMATURE COMMITMENT

A system may be correct eventually but act too early.

Therefore experiments should preserve:

- posterior trajectory;
- commitment update index;
- true goal;
- whether later evidence would have corrected the belief.

This allows analysis of whether uncertainty-aware deferral prevents premature decisions.

---

# 61. POSTERIOR OSCILLATION

A posterior can alternate between hypotheses under conflicting evidence.

This is a useful failure/behavior case.

The project should measure/inspect:

- number of leading-hypothesis switches;
- entropy changes;
- effect on confirmation/deferral.

No special smoothing method is currently approved to suppress oscillation.

---

# 62. STOPPING RULE — UNRESOLVED

Sequential inference needs a policy for when evidence accumulation stops.

Possible rules may eventually include:

- posterior confidence threshold;
- entropy threshold;
- fixed maximum number of observations;
- confirmation;
- timeout;
- another validated rule.

No stopping rule is currently locked.

The Bayesian module should expose state so the shared-autonomy layer can implement the chosen rule later.

---

# 63. MAXIMUM-EVIDENCE LIMIT

For experiments, it may be necessary to define:

```text
maximum number of evidence updates
```

to prevent indefinite accumulation.

The exact value is not locked.

If introduced, it must be recorded and justified.

---

# 64. BAYESIAN EVIDENCE ACCUMULATION VS SIMPLE AVERAGING

Simple probability averaging:

\[
\bar{p}
=
\frac{1}{T}\sum_t p_t
\]

is not the same as an explicit Bayesian prior/likelihood/posterior update.

The project may use averaging as a comparison baseline if later justified.

It must not call probability averaging "Bayesian inference."

---

# 65. BAYESIAN EVIDENCE ACCUMULATION VS MAJORITY VOTE

Likewise:

```text
Left
Left
Right
→ majority Left
```

is a heuristic voting rule.

It does not use the full probability evidence or prior.

It may be a simple baseline but must not replace the approved Bayesian module.

---

# 66. PRIOR SENSITIVITY

Bayesian results may depend on the prior, especially when evidence is weak.

Therefore a future analysis may compare:

- uniform prior;
- approved personalized prior;
- another justified prior.

Such an analysis is useful if adaptation updates priors.

No prior-sensitivity experiment is mandatory yet, but the architecture should permit it.

---

# 67. LIKELIHOOD SENSITIVITY

The posterior also depends strongly on likelihood construction.

Because the EEG likelihood mapping is unresolved, the final project should perform validation/sensitivity checks once the mapping is approved.

The project must not hide this dependency.

---

# 68. ADAPTATION INTERFACE

The adaptation module may later update:

- priors;
- decoder reliability estimates;
- evidence weights;
- thresholds.

If priors are adapted, the Bayesian module should receive the adapted prior through an explicit interface.

Adaptation must not mutate Bayesian state silently.

---

# 69. ADAPTATION ABLATION

The project requires adaptation to be switchable.

Therefore Bayesian experiments must be able to run with:

```text
fixed prior
```

and, if implemented:

```text
adapted prior
```

or the corresponding approved adaptation parameter.

This supports the final ablation framework.

---

# 70. CROSS-SUBJECT EFFECTS

If decoder reliability differs strongly by subject, a global evidence model may behave differently across users.

This is one reason the project may later consider:

- user-specific reliability;
- user-specific priors;
- personalization.

However no subject-specific Bayesian model is currently locked.

---

# 71. CALIBRATION DEPENDENCY

The intended full system uses calibrated EEG evidence before Bayesian reasoning.

However the experimental framework should permit:

```text
Bayes with raw probability evidence
vs
Bayes with calibrated evidence
```

if scientifically defined.

This can help determine whether calibration materially affects posterior behavior.

The exact comparison belongs in Experimental Design.

---

# 72. CALIBRATION DOES NOT MAKE THE LIKELIHOOD MAPPING AUTOMATIC

Even after calibration, the model has:

\[
P(C\mid EEG)
\]

not automatically:

\[
P(E\mid G)
\]

Calibration improves probability reliability for the decoder task.

The application likelihood mapping still requires an explicit model.

This distinction must remain in code and documentation.

---

# 73. POSSIBLE FUTURE LIKELIHOOD-MODEL CATEGORIES — NOT APPROVED

Without selecting one, the project recognizes that the final mapping could conceptually be based on:

- an explicitly defined confusion/reliability model;
- a generative observation model;
- a mathematically justified transformation of calibrated class evidence;
- another validated interface model.

This list does **not** approve any method.

The final decision must be documented in `DECISIONS.md` before integration.

---

# 74. DO NOT USE AN AD HOC “POWER” OR “BOOST” RULE

Examples of scientifically weak implementation:

```text
likelihood = probability ** 2
```

or:

```text
posterior = previous_posterior + confidence
```

without a formal rationale.

Such heuristics must not be called Bayesian inference.

---

# 75. DO NOT USE TRUE GOAL TO BUILD THE LIKELIHOOD

The evidence model must be computable from information available to the system during inference.

The hidden experimental target exists only for scoring.

This is non-negotiable.

---

# 76. NO FABRICATED COGNITIVE INTERPRETATION

The Bayesian model represents:

> **the artificial system's belief about the human's intended control objective**

It does not prove that:

- the human brain internally performs this Bayesian update;
- the posterior matches subjective human confidence;
- the system models full cognition.

---

# 77. “COGNITIVE” CLAIM BOUNDARY

The Bayesian module contributes to the project's cognitive component because it models:

- latent intention;
- prior belief;
- evidence accumulation;
- belief update;
- uncertainty;
- decision commitment.

This is a computational cognitive abstraction.

It must not be described as a full cognitive architecture.

---

# 78. “BAYESIAN” CLAIM ACCEPTANCE RULE

The project may call this module Bayesian only if the implementation performs an actual update of the form:

\[
posterior
\propto
likelihood \times prior
\]

with normalization.

Not sufficient:

- softmax probability;
- moving average;
- confidence smoothing;
- majority vote;
- rule-based score accumulation.

---

# 79. FAILURE CASES

The Bayesian layer should support analysis of:

## Wrong posterior

Posterior strongly favors the wrong controlled goal.

## Slow convergence

Posterior remains uncertain for many updates.

## Premature confidence

Posterior becomes overconfident too quickly.

## Conflicting evidence

Posterior moves repeatedly between hypotheses.

## Prior domination

Strong prior overwhelms valid contrary evidence.

## Evidence domination

One extreme likelihood overwhelms all previous evidence.

## Numerical failure

Normalization becomes zero/non-finite.

## Mapping failure

The EEG-to-goal adapter produces semantically invalid evidence.

---

# 80. BAYESIAN METRICS

Approved broader project metrics include:

- goal inference accuracy;
- posterior confidence;
- entropy;
- decision latency/time to reliable commitment;
- wrong-goal commitment.

Additional useful diagnostics may include:

- number of updates before commitment;
- number of posterior-leader switches;
- posterior assigned to true goal over time.

Exact metrics will be frozen in `18_METRICS_AND_EVALUATION.md`.

---

# 81. POSTERIOR TRAJECTORY PLOT

A useful visualization is:

```text
x-axis:
evidence update

y-axis:
posterior probability
```

with one curve per hypothesis.

This allows evaluators to see:

- evidence accumulation;
- ambiguity;
- commitment;
- recovery from conflicting evidence.

The plot must use actual saved posterior history.

---

# 82. SYNTHETIC-ONLY BAYESIAN DEVELOPMENT MODE

The architecture explicitly permits:

```text
synthetic likelihood sequence
→ Bayesian filter
→ entropy
→ shared-autonomy policy
```

before real EEG integration.

This allows mathematical correctness to be established independently of EEG model quality.

Synthetic tests must be labeled clearly.

---

# 83. REAL-EEG INTEGRATION GATE

The Bayesian module should not consume real EEG-derived evidence until:

1. EEG decoder output is validated;
2. class order is explicit;
3. calibration strategy for the relevant experiment is defined;
4. goal-mapping policy is approved;
5. likelihood construction is mathematically defined;
6. synthetic Bayesian tests pass.

This prevents accidental end-to-end integration with invalid probability semantics.

---

# 84. CODEX TASK 1 — BAYESIAN CORE

A suitable first Codex task for this module is:

> Read `MASTER_PROJECT_SPEC.md`, `09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md`, and `10_BAYESIAN_GOAL_INFERENCE.md`. Implement only a generic discrete Bayesian intent filter in `src/cognition/bayesian_intent.py`. The filter must accept named hypotheses, a valid prior, and an externally supplied likelihood vector; perform normalized sequential posterior updates; preserve update history; support explicit reset; validate dimensions and finite/non-negative values; and include analytically checkable unit tests. Do not implement EEG-to-goal mapping, calibration, thresholds, adaptation, or shared-autonomy decisions.

This task can be completed before the unresolved mapping decision.

---

# 85. CODEX TASK 2 — GOAL-EVIDENCE ADAPTER

This task must **not** be issued until the project owner approves:

- the BCI goal-selection protocol;
- the probability/likelihood semantics.

Only then should Codex implement the adapter.

---

# 86. BAYESIAN CORE ACCEPTANCE TEST

The core module is correct when:

```text
known prior
+
known synthetic likelihood
→ analytically correct posterior
```

for one and multiple sequential updates.

No Search & Rescue UI is required for this test.

---

# 87. REPRODUCIBILITY

Every Bayesian experiment should record:

```text
sequence_id
hypothesis_names
initial prior
mapping_policy_id
likelihood_model_id
evidence IDs
likelihood sequence
posterior sequence
entropy sequence
reset events
commitment event
true experimental goal
experiment config
Git commit
```

The true experimental goal must remain evaluation-only.

---

# 88. CONFIGURATION

Conceptual configuration may include:

```yaml
bayesian_intent:
  hypotheses: TBD
  prior_policy: TBD
  likelihood_model: TBD
  max_updates: TBD
  reset_policy: TBD
```

Thresholds belong to the confidence/shared-autonomy policy rather than being buried here.

---

# 89. BAYESIAN MODULE VERSIONING

Once the evidence model is approved, record a stable configuration identity such as:

```text
bayesian_intent_v001
likelihood_model_v001
goal_mapping_policy_v001
```

This prevents silent mathematical changes across experiments.

---

# 90. CHANGE-CONTROL TRIGGERS

The following require explicit project-owner approval and a recorded decision:

- changing the goal hypothesis structure;
- changing binary-to-multi-goal mapping;
- changing likelihood construction;
- adding dynamic goal transitions;
- adding sophisticated Bayesian filtering;
- using adapted/user-specific priors as the default;
- changing reset/commitment semantics in a way that affects experiments.

---

# 91. BAYESIAN ABLATION

The overall project requires comparison with and without Bayesian inference.

Therefore the architecture must support:

```text
EEG evidence
→ direct / confidence-aware decision
```

and:

```text
EEG evidence
→ Bayesian accumulation
→ decision
```

without rewriting unrelated modules.

This is why the Bayesian filter must remain modular.

---

# 92. DIRECT-CONTROL BASELINE

System A conceptually uses:

```text
decoder output
→ direct decision
```

It does not maintain sequential Bayesian goal belief.

The Experimental Design document must define a fair comparison.

---

# 93. CONFIDENCE-AWARE BASELINE

System B conceptually uses:

```text
decoder
→ confidence/uncertainty
→ action or defer
```

without full Bayesian accumulation.

This isolates the value of uncertainty gating from sequential Bayesian reasoning.

---

# 94. BAYESIAN SHARED-AUTONOMY CONDITION

System C conceptually uses:

```text
EEG evidence
→ Bayesian goal inference
→ autonomous navigation
```

The exact inclusion of calibration/uncertainty/safety in this controlled baseline must be frozen later.

---

# 95. FULL SYSTEM CONDITION

System D contains:

```text
EEG
+ calibration
+ Bayesian inference
+ uncertainty
+ shared autonomy
+ safety
+ adaptation
```

The Bayesian module must therefore work both:

- independently in tests;
- as one replaceable component of the full system.

---

# 96. BAYESIAN INFERENCE AND SAFETY ARE DIFFERENT

Bayesian inference answers:

> **What goal does the system believe the human intends?**

Safety answers:

> **Is the proposed autonomous behavior permitted?**

A very confident posterior cannot authorize a blocked or unsafe path.

Safety remains downstream and independent.

---

# 97. BAYESIAN INFERENCE AND PLANNING ARE DIFFERENT

Bayesian inference chooses/represents goal belief.

A* planning computes a route to an approved goal.

Do not allow path length or hazard cost to alter the Bayesian posterior unless a future explicit prior/model says that information is legitimately available to intent inference.

---

# 98. SCENARIO-INFORMED PRIORS — USE CAREFULLY

A future system might use contextual priors.

For example, if only two options are currently active, the prior may be defined over those two choices.

However contextual priors must not covertly turn:

```text
what is easy for the robot?
```

into:

```text
what the human probably wants
```

without evidence.

The human's goal remains authoritative.

---

# 99. HUMAN CORRECTION AS ADAPTATION SIGNAL

A human override may later be used as evidence that:

- decoder reliability was poor;
- a prior should change;
- a threshold should adapt.

That belongs to the adaptation model.

It is not automatically part of the same Bayesian goal update.

---

# 100. LIMITATIONS OF THE BAYESIAN MODEL

The final report should acknowledge:

- the latent-goal hypothesis space is engineered;
- evidence semantics depend on the BCI mapping;
- independence assumptions may be simplified;
- priors may be simplistic;
- offline EEG does not provide a live co-adaptive loop;
- posterior probability does not equal subjective human certainty;
- binary motor imagery limits goal-interface richness;
- simulation does not validate real-world rescue cognition.

---

# 101. OUT-OF-SCOPE BAYESIAN FEATURES

Not required for the current core:

- probabilistic programming framework;
- Bayesian neural network;
- particle filter;
- active inference;
- hierarchical Bayesian population model;
- continuous-state Kalman-style intent estimation;
- nonparametric Bayes;
- causal Bayesian network;
- Bayesian reinforcement learning.

These may be future research extensions only if justified.

---

# 102. OPEN DECISIONS — MUST REMAIN OPEN

## 102.1 Binary EEG-to-goal interaction protocol

Critical and unresolved.

## 102.2 Exact likelihood construction

Critical and unresolved.

## 102.3 Initial prior policy

Not fully locked.

## 102.4 Goal stability / transition model

No dynamic model locked.

## 102.5 Evidence unit

Exact update unit not locked.

## 102.6 Evidence-sequence construction

Not locked.

## 102.7 Maximum number of updates

Not locked.

## 102.8 Reset policy

Partially unresolved.

## 102.9 Commitment/stopping rule

Not locked.

## 102.10 Adapted prior/reliability mechanism

Not locked.

No implementation agent may silently select these as permanent project methodology.

---

# 103. DECISIONS REQUIRED BEFORE END-TO-END GOAL INFERENCE IS FROZEN

Before full EEG-to-Search-&-Rescue integration, explicitly approve:

1. which goals/options are active during one BCI selection;
2. how Left/Right motor imagery corresponds to those choices;
3. what one evidence update represents;
4. how calibrated decoder probabilities are converted into a valid goal-likelihood representation;
5. initial prior;
6. whether the goal is assumed stable during one selection;
7. stopping/commitment rule;
8. maximum updates/timeout;
9. reset behavior after confirmation/override/completion;
10. interaction with adaptation.

These decisions must be recorded in `DECISIONS.md`.

---

# 104. ACCEPTANCE CRITERIA — BAYESIAN CORE

The core Bayesian module is correctly implemented when:

1. it accepts named hypotheses;
2. it accepts an explicit valid prior;
3. it accepts externally supplied likelihoods;
4. it performs actual prior × likelihood Bayesian updating;
5. posterior is normalized;
6. sequential posterior becomes the next prior;
7. evidence history is preserved;
8. reset is explicit;
9. invalid probabilities are rejected;
10. zero/non-finite normalization fails safely;
11. hypothesis order is validated;
12. synthetic analytic tests pass;
13. \(K>2\) works mathematically;
14. no EEG-to-goal mapping is embedded in the core;
15. no ground-truth goal enters inference;
16. no autonomy thresholds are embedded in the core;
17. the posterior can be passed to the uncertainty module.

---

# 105. ACCEPTANCE CRITERIA — FULL BAYESIAN GOAL INFERENCE

The end-to-end Bayesian goal-inference layer is not complete until:

1. the BCI goal-selection protocol is approved;
2. the EEG-to-goal adapter is implemented;
3. likelihood semantics are mathematically documented;
4. calibrated EEG evidence reaches the adapter correctly;
5. real EEG-derived evidence can update the posterior;
6. posterior trajectories are logged;
7. uncertainty is computed from posterior;
8. commitment/defer behavior is defined outside the Bayesian core;
9. true-goal metadata remains evaluation-only;
10. inference metrics can be calculated;
11. wrong-goal and latency failure cases can be reproduced;
12. the Bayesian component can be disabled for ablation.

---

# 106. CLAIM BOUNDARIES

Allowed once implemented:

> “Implemented sequential Bayesian goal inference using explicit prior, likelihood, and posterior updates.”

Allowed:

> “The system accumulated EEG-derived evidence over multiple observations.”

Allowed if measured:

> “Bayesian accumulation reduced wrong-goal commitment under the tested protocol.”

Not allowed:

> “The brain uses our Bayesian model.”

Not allowed:

> “The posterior is the user's true subjective confidence.”

Not allowed:

> “Bayesian inference guarantees correct intent recognition.”

Not allowed:

> “The system reads arbitrary intentions.”

---

# 107. CURRENT BAYESIAN GOAL-INFERENCE SUMMARY

The project treats the human operator's intended control objective as a **latent discrete goal variable** rather than equating one EEG classifier output with true intent. A generic Bayesian filter maintains a prior belief over currently valid goal/intention hypotheses and updates that belief sequentially using externally supplied likelihoods according to \(P(G\mid E_{1:t}) \propto P(E_t\mid G)P(G\mid E_{1:t-1})\). The resulting normalized posterior is passed to the uncertainty module, which computes entropy, and then to the shared-autonomy controller, which decides whether to proceed, confirm, defer, pause, or stop. The Bayesian mathematical core is deliberately independent of EEG decoding, Search & Rescue planning, safety, and UI logic. Most importantly, calibrated EEG decoder output \(P(class\mid EEG)\) is **not automatically treated as** the required likelihood \(P(E\mid G)\). The exact Left/Right motor-imagery-to-goal interaction protocol and the corresponding likelihood-construction rule remain unresolved and must be explicitly approved before real EEG end-to-end goal inference is frozen. The generic Bayesian core can nevertheless be implemented immediately and verified with analytically checkable synthetic likelihood sequences.

---

# 108. NEXT DOCUMENT

The next planned document is:

**`11_COGNITIVE_AND_ADAPTIVE_MODEL.md` — Cognitive Model & Adaptation / Personalization Specification**

That document should define:

- the limited computational meaning of “cognitive” in this project;
- latent intention and belief;
- correction history;
- user/system adaptation;
- candidate adaptation targets;
- priors;
- reliability estimates;
- confidence thresholds;
- personalization;
- learning from override/correction;
- adaptation ON/OFF ablation;
- safeguards against drift;
- logging;
- and claim boundaries.

The exact adaptation mechanism remains unresolved and must not be silently selected.
