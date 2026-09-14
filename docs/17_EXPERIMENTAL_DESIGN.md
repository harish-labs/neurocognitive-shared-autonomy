# 17_EXPERIMENTAL_DESIGN.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Experimental Design, A/B/C/D Comparisons, Cross-Subject Evaluation, Robustness, Noise Stress Tests, and Ablation Protocol

**Document ID:** I-01  
**Document class:** Experiments & Evaluation / Experimental Design Specification  
**Authority level:** Subordinate to all Master Authority, Scenario, Architecture, Data, Neuroscience, ML, Bayesian, Shared-Autonomy, Planning, Safety, Implementation, and Repository Architecture documents  
**Status:** Authoritative experiment-design baseline reconciled through D-084; M7-T02 R03 v5 is an unaccepted scientific-review candidate
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND EXPERIMENTAL-INTEGRITY RULE

This document defines **how the project will be experimentally tested**.

It must remain consistent with all previously approved project documents.

If this document conflicts with a higher-authority project document, the higher-authority document wins.

The central experimental rule is:

> **Experiments must be designed so the project can fail.**

No experiment may be constructed to guarantee that:

- EEGNet beats CSP+LDA;
- calibration improves every metric;
- Bayesian inference always helps;
- uncertainty always improves safety;
- adaptation always improves performance;
- or the full System D always wins.

Negative and mixed results are valid.

---

# 1. PURPOSE OF THIS DOCUMENT

This document defines:

- experimental questions;
- hypotheses;
- model-comparison protocol;
- calibration experiments;
- Bayesian experiments;
- uncertainty/shared-autonomy experiments;
- A/B/C/D comparisons;
- robustness and noise stress tests;
- safety stress tests;
- adaptation ablation;
- subject-level and cross-subject evaluation;
- repeated-run/seed policy boundaries;
- test-set protection;
- experiment logging;
- fair comparison rules;
- and reportable experiment matrices.

This document does **not** silently choose currently unresolved parameters.

---

# 2. PRIMARY RESEARCH QUESTION

The central research question remains:

> **Can uncertainty-aware shared autonomy improve the reliability and safety of EEG-based intent control compared with direct brain-computer control?**

The experimental design must directly test this question.

---

# 3. SECONDARY EXPERIMENTAL QUESTIONS

The project should also test:

1. How well does CSP+LDA decode Left-vs-Right motor imagery?
2. How well does EEGNet / the approved compact CNN decode the same task?
3. Which decoder is more suitable for downstream shared autonomy?
4. Are the raw classifier probabilities well calibrated?
5. Does calibration improve probability reliability?
6. Does sequential Bayesian evidence accumulation improve goal-level intent inference compared with direct single-observation decisions?
7. Does uncertainty-aware deferral reduce wrong-goal commitments?
8. What is the cost of uncertainty-aware control in decision latency and human intervention?
9. Does explicit safety control reduce executed simulated safety violations?
10. How does the system behave under degraded/noisy EEG evidence?
11. How well do decoding and confidence generalize across subjects?
12. If adaptation is implemented, does it improve later decisions relative to a fixed system?

---

# 4. EXPERIMENTAL PRINCIPLES

All experiments must follow these principles:

```text
same input where comparison requires fairness
same split where comparison requires fairness
same scenario where comparison requires fairness
change one intended component at a time
save all outputs
preserve failure cases
do not tune on final test data
```

---

# 5. EXPERIMENT FAMILIES

The project should organize experiments into clear families.

```text
E1 — EEG decoding
E2 — Probability calibration
E3 — Bayesian goal inference
E4 — Uncertainty / shared autonomy
E5 — Planning / safety
E6 — Full A/B/C/D system comparison
E7 — Robustness / noise / ablations
E8 — Cross-subject evaluation
E9 — Adaptation, if implemented
```

The exact experiment IDs may differ, but the conceptual separation should remain.

---

# 6. E1 — EEG DECODING EXPERIMENT

## Objective

Compare the mandatory classical and neural EEG decoders.

Models:

```text
CSP + LDA
EEGNet / approved compact CNN
```

Task:

```text
Left-hand motor imagery
vs
Right-hand motor imagery
```

Dataset:

```text
PhysioNet EEGBCI
runs 4, 8, 12
```

---

# 7. E1 INPUT CONSISTENCY

For a fair decoder comparison, both models should use the same:

- subjects;
- runs;
- semantic labels;
- underlying trial set;
- approved preprocessing;
- train/validation/test partition where scientifically appropriate.

Model-specific internal transformations are allowed.

Example:

```text
CSP spatial filtering
```

belongs only to CSP+LDA.

---

# 8. E1 METRICS

Core EEG metrics:

- accuracy;
- balanced accuracy;
- precision;
- recall;
- F1;
- confusion matrix.

Additional reporting:

- subject-wise performance;
- fold-wise performance;
- probability outputs;
- failure cases.

Calibration metrics are analyzed separately in E2.

---

# 9. E1 HYPOTHESIS

A neutral hypothesis is preferred:

> **H1: CSP+LDA and EEGNet will show measurable but potentially different decoding performance across subjects and evaluation conditions.**

The experiment does not assume one must win.

---

# 10. E1 DECODER REPORTING RULE

D-077 requires both approved decoder families to be evaluated under A/B/C/D where valid. M7 evaluation must not select whichever decoder gives a convenient post-hoc system result. Decoder-family results remain separately identified and include balanced accuracy and calibration quality in addition to accuracy.

---

# 11. E2 — PROBABILITY CALIBRATION EXPERIMENT

## Objective

Determine whether raw decoder probabilities are statistically reliable and whether calibration improves them.

Compare:

```text
raw probabilities
vs
calibrated probabilities
```

for each decoder where appropriate.

---

# 12. E2 METRICS

Required:

- reliability diagram;
- Expected Calibration Error;
- Brier Score.

Optional if later approved:

- negative log-likelihood.

---

# 13. E2 HYPOTHESIS

> **H2: An approved calibration method may reduce miscalibration of EEG decoder probabilities on held-out evaluation data.**

This must be tested independently for each decoder family where needed.

---

# 14. E2 CALIBRATION-DATA BOUNDARY

The calibrator must not fit on final test labels.

D-049 fixes the existing validation partition as the calibration-fitting partition. Training remains the decoder-fitting partition, and test/final-test data remain excluded from fitting, calibration, and selection. D-048 fixes temperature scaling for EEGNet, sigmoid/Platt-style calibration for CSP+LDA, and an identity/no-calibration baseline. D-050 fixes 10 equal-width reliability/ECE bins and companion Brier reporting.

---

# 15. E2 ABLATION

Calibration must be switchable.

Compare:

```text
calibration OFF
vs
calibration ON
```

while holding the rest of the relevant pipeline constant.

---

# 16. E3 — BAYESIAN GOAL-INFERENCE EXPERIMENT

## Objective

Determine whether sequential evidence accumulation improves goal-intent inference compared with direct/single-observation decision-making.

Synthetic likelihood sequences remain appropriate for analytical development validation. Real EEG integration follows the approved D-051 binary-choice protocol and D-052 calibrated-evidence likelihood construction.

---

# 17. E3 BASELINES

Possible controlled comparison:

```text
Single-evidence decision
vs
Sequential Bayesian accumulation
```

Optional simple comparison if useful:

```text
majority vote / average probability
```

but such baselines must not be called Bayesian.

---

# 18. E3 METRICS

Potential core metrics:

- goal inference accuracy;
- posterior confidence;
- entropy;
- wrong-goal commitment;
- number of evidence updates before commitment;
- decision latency;
- posterior assigned to true goal over time.

The final metric definitions belong in the next Metrics document.

---

# 19. E3 HYPOTHESIS

> **H3: Sequential Bayesian accumulation may reduce sensitivity to individual noisy EEG observations and improve the reliability of goal-level inference.**

This is falsifiable.

---

# 20. E3 SYNTHETIC VALIDATION FIRST

Before real EEG:

```text
known prior
+
known likelihood sequence
→ known posterior trajectory
```

The Bayesian system must pass analytical tests.

This ensures mathematical correctness is separated from EEG quality.

---

# 21. E3 REAL-EEG BOUNDARY

D-051 and D-052 resolve the interaction and likelihood semantics: each decision exposes exactly two valid candidates, calibrated Left evidence supports candidate A, calibrated Right evidence supports candidate B, and planning/risk must not alter the intent likelihood. Protected final-test execution remains reserved for M7-T02.

D-081 freezes the real-EEG sequential evaluation unit. Within each `(subject_id, run_id, intended_class)` group, order trials by acquisition `event_sample` with canonical trial identity as deterministic tie-breaker and form non-overlapping consecutive blocks of exactly five. Do not mix classes, runs, or subjects; do not overlap, reuse, pad, or create a short tail episode. Record excluded tails, which remain eligible for valid E1/E2 single-trial analysis.

A/B/C/D share each frozen episode identity. A and B use its first source observation; C and D receive the same ordered five-observation opportunity and may stop early only under accepted policy. Evaluation labels may construct and score the episode and drive the simulated-human command, but must not enter decoder/calibration/Bayesian inference, planning, safety, or adaptation directly. These are deterministic offline repeated-trial constructions for one fixed intended choice, not natural continuous sessions or live/online EEG accumulation.

---

# 22. E4 — UNCERTAINTY / SHARED-AUTONOMY EXPERIMENT

## Objective

Determine whether uncertainty-aware behavior reduces unjustified commitment compared with direct control.

Compare systems where the key difference is:

```text
uncertainty ignored
vs
uncertainty affects behavior
```

---

# 23. E4 CORE BEHAVIORS

The uncertainty-aware system may:

```text
PROCEED
CONFIRM
DEFER
```

depending on the approved policy.

Human-control actions remain:

```text
CONFIRM
OVERRIDE
PAUSE
STOP
```

---

# 24. E4 METRICS

Potential measures:

- wrong-goal commitment;
- deferral count/rate;
- confirmation count;
- human interventions;
- decision latency;
- task success;
- completion time.

---

# 25. E4 HYPOTHESIS

> **H4: Uncertainty-aware shared autonomy may reduce wrong-goal commitment at the cost of additional confirmation or decision latency.**

This hypothesis explicitly allows a trade-off rather than assuming unconditional improvement.

---

# 26. E4 FROZEN POLICY

D-054 through D-057 fix the maximum five accepted-evidence horizon and the posterior-authoritative policy: `>=0.90` PROCEED, after update five `>=0.75 and <0.90` CONFIRM, and `<0.75` DEFER. CONFIRM requires explicit human approval and DEFER holds position.

---

# 27. E5 — PLANNING / SAFETY EXPERIMENT

## Objective

Validate:

- A* path planning;
- risk-aware route selection;
- safety action rejection;
- replanning.

These experiments use artificial approved goals and do not require EEG.

---

# 28. E5 SCENARIO CLASSES

Recommended scenario categories:

```text
S1 — Basic free-space route
S2 — Static obstacle route
S3 — Short risky vs long safer route
S4 — No-path case
S5 — Dynamic blockage / replanning
S6 — Prohibited hazard
S7 — Emergency stop
```

For M7-T02, D-080 and `CURRENT_TASK.md` freeze the exact deterministic S1–S7 maps, states, risks, events, probes, and expected safety behavior. M7-T01 remains limited to controlled deterministic development scenarios.

---

# 29. E5 METRICS

Potential measures:

- path length;
- total path cost;
- risk exposure;
- planning success;
- replanning count;
- unsafe action attempts;
- executed safety violations;
- safety overrides;
- mission success.

---

# 30. E5 HYPOTHESES

> **H5a: A* should produce valid routes under the approved map/cost model when a route exists.**

> **H5b: The explicit safety controller should reduce executed hard-constraint violations relative to a safety-disabled simulation condition.**

> **H5c: Risk-aware planning may trade path length for lower simulated risk exposure depending on the approved \(\lambda\).**

---

# 31. SAFETY ABLATION

Compare:

```text
Safety ON
vs
Safety OFF
```

only in simulation.

Basic software validity protections must remain active in both.

The safety-off condition may allow simulated prohibited actions for experimental comparison but should never cause invalid software behavior.

---

# 32. E6 — PRINCIPAL A/B/C/D SYSTEM COMPARISON

The project has already approved four principal system conditions.

These must not be removed without explicit scope change.

---

# 33. SYSTEM A — DIRECT EEG CONTROL

Conceptually:

```text
EEG decoder
→ direct decision / commitment
```

Purpose:

> Establish the simplest direct BCI baseline.

Under D-077, System A uses the first accepted identity/no-calibration evidence observation, commits its evidence argmax directly, uses no Bayes or uncertainty refusal, and otherwise retains the common planner, risk, safety, and human emergency-authority stack.

---

# 34. SYSTEM B — CONFIDENCE-AWARE CONTROL

Conceptually:

```text
EEG decoder
→ confidence / uncertainty
→ act or defer
```

Purpose:

> Isolate the effect of confidence-aware rejection/deferral.

Under D-077, System B uses one model-specifically calibrated observation and no sequential Bayes. It applies `>=0.90` PROCEED, `>=0.75 and <0.90` CONFIRM, and `<0.75` DEFER.

---

# 35. SYSTEM C — BAYESIAN SHARED AUTONOMY

Conceptually:

```text
EEG evidence
→ Bayesian goal inference
→ autonomous navigation
```

Purpose:

> Evaluate sequential intent inference and shared autonomous execution.

Under D-077, System C uses calibration, up to five observations, D-053/D-054 sequential Bayesian accumulation, and D-055 through D-057 uncertainty/shared-autonomy behavior. Adaptation is disabled. The common planner/risk/safety/human-authority stack remains enabled.

---

# 36. SYSTEM D — FULL SYSTEM

Conceptually:

```text
EEG
+ calibration
+ Bayesian inference
+ uncertainty
+ shared autonomy
+ safety
+ adaptation where implemented
```

System D is System C with D-058 through D-060 adaptation enabled. Adaptation uses only legitimate explicit human-approved feedback and never hidden evaluation truth.

---

# 37. A/B/C/D COMPONENT MATRIX — FROZEN BY D-077

| Component | A — Direct EEG | B — Confidence-Aware | C — Bayesian Shared Autonomy | D — Full System |
|---|---:|---:|---:|---:|
| Same frozen decoder evidence | Yes | Yes | Yes | Yes |
| Calibration | Identity / OFF | ON | ON | ON |
| Evidence horizon | 1 | 1 | Up to 5 | Up to 5 |
| Sequential Bayesian accumulation | No | No | Yes | Yes |
| Uncertainty gating | No | Yes | Yes | Yes |
| Human CONFIRM / DEFER behavior | No | Yes | Yes | Yes |
| A* navigation / same risk model | Yes | Yes | Yes | Yes |
| Hard safety controller | Yes | Yes | Yes | Yes |
| Human STOP / PAUSE / OVERRIDE authority | Yes | Yes | Yes | Yes |
| Adaptation | No | No | No | Yes |

Both `CSP+LDA` and `EEGNet` are evaluated under all four principal conditions where valid.

---

# 38. A/B/C/D FAIRNESS RULE

Where the research question compares one component, hold unrelated components constant.

Example:

To evaluate uncertainty:

```text
same decoder
same EEG sequence
same map
same goal
same safety
same planner
```

and change only:

```text
uncertainty policy
```

Avoid comparing entire different stacks when a narrower comparison is needed.

---

# 39. E6 CORE METRICS

The full-system comparison should eventually report:

- task success;
- wrong-goal commitment;
- decision latency;
- confirmation count;
- override count;
- deferral count;
- path length;
- completion time;
- replanning;
- safety violations;
- safety overrides.

---

# 40. E6 PRIMARY HYPOTHESIS

> **H6: The full uncertainty-aware shared-autonomy system may reduce wrong-goal and unsafe simulated behavior relative to direct EEG control, while potentially increasing decision latency or human intervention.**

This is the principal system-level hypothesis.

---

# 41. E7 — COMPONENT ABLATION EXPERIMENTS

The project must support removing individual components.

Required ablations should include where applicable:

```text
Full
Full - calibration
Full - Bayes
Full - uncertainty
Full - safety
Full - adaptation
```

D-084 defines the otherwise non-equivalent execution semantics for the two sequential ablations: `Full - Bayes` uses the calibrated cumulative arithmetic mean after each of the same five D-081 observations and retains the approved `>=0.90` PROCEED, final `[0.75,0.90)` CONFIRM, and final `<0.75` DEFER policy. `Full - uncertainty` retains Bayesian updates but always consumes exactly five observations, records posterior entropy descriptively, then commits the final posterior argmax without PROCEED/CONFIRM/DEFER gating; exact ties select candidate A and are logged.

The architecture has already been designed to support this.

---

# 42. ABLATION FAIRNESS RULE

An ablation removes one component while keeping:

- same EEG evidence;
- same map;
- same goals;
- same seed;
- same evaluation conditions

where possible.

Do not change multiple unrelated factors simultaneously unless the experiment explicitly studies a compound condition.

---

# 43. E7 — ROBUSTNESS / NOISE STRESS TESTS

## Objective

Determine how the system degrades as neural evidence becomes less reliable.

Primary M7 robustness is applied at the normalized two-candidate probability/evidence interface after the condition's identity/model-specific calibration stage and before its decision, confidence, or Bayesian policy. Signal-level physiological noise is not a core M7-T01 requirement.

---

# 44. D-078 FROZEN ROBUSTNESS LEVELS

```text
R1 evidence flattening epsilon = 0.00, 0.25, 0.50, 0.75, 1.00
R2 contradictory-evidence contamination q = 0.00, 0.10, 0.20, 0.30, 0.40
```

---

# 45. NOISE MODEL REQUIREMENT

Every perturbation must state:

```text
what is changed
how it is changed
mathematical definition
severity
random seed
```

R1 uses `p_epsilon = (1-epsilon)*p + epsilon*[0.5,0.5]`. R2 swaps `[pA,pB]` to `[pB,pA]` at deterministic recorded indices selected once across the complete ordered evidence population for the condition/evaluation run; episode boundaries do not restart selection or round `q` independently. Provenance records requested `q`, seed, population size, stable global observation identities/indices, selection rule, realized count/fraction, and original/perturbed evidence. Labels and evaluation-only true goals do not change.

---

# 46. ROBUSTNESS HYPOTHESIS

> **H7: As EEG evidence quality degrades, uncertainty-aware systems may defer more often and degrade more gracefully than direct-control systems.**

This is central to the project.

Possible disconfirming result:

- uncertainty does not increase appropriately;
- wrong commitment remains high;
- deferral becomes excessive.

---

# 47. ROBUSTNESS METRICS

Potential measures across noise severity:

- EEG accuracy;
- ECE;
- Brier Score;
- posterior entropy;
- wrong-goal commitment;
- deferral;
- decision latency;
- task success;
- safety violations.

---

# 48. ROBUSTNESS PLOT

A useful plot may use:

```text
x-axis:
noise / degradation level

y-axis:
metric
```

with separate curves for:

```text
A
B
C
D
```

or selected components.

Only actual results may be plotted.

---

# 49. E8 — CROSS-SUBJECT EVALUATION

Cross-subject evaluation is an approved research direction and its primary protocol is frozen by D-041 and D-042.

Purpose:

> Test whether EEG decoding/confidence behavior generalizes to subjects not used in model fitting.

---

# 50. CROSS-SUBJECT RULE

The primary protocol is a fixed subject-held-out split:

```text
70% train subjects
15% validation subjects
15% final test subjects
```

If subject \(u\) is in validation or final test:

```text
no trials from subject u
```

may appear in training. Subject IDs must be disjoint across all three partitions.

---

# 51. PRIMARY CROSS-SUBJECT PROTOCOL

After the approved preprocessing/QC boundary:

```text
1. form the eligible subject list
2. apply one deterministic shuffle with seed 42
3. freeze the subject IDs in a versioned split manifest before model fitting
```

Under D-082, first apply the fixed D-035 QC policy to all 109 source subjects and freeze the actual post-QC eligible count `N`. Sort eligible IDs ascending, shuffle once with seed 42, and allocate contiguous partitions using floor quotas plus largest fractional remainders. Exact remainder ties use `final_test`, then `validation`, then `train`.

D-083 defines cross-subject eligibility exactly as at least one retained T1 trial and at least one retained T2 trial after QC. Do not require D-040 within-subject feasibility, five trials per class, or a D-081 episode for cohort membership. Track within-subject feasibility separately.

For the historical full-eligible-cohort case `N=109`, this method gives:

```text
76 train
16 validation
17 final test
```

Leave-one-subject-out or grouped subject K-fold may be added later only as explicitly authorized secondary analyses; they are not the primary cross-subject protocol.

If preprocessing/QC yields `N != 109`, use the D-082 allocation mechanically; do not force 76/16/17 or preserve provisional membership. Freeze all exclusions and reasons, exact allocation calculations, subject IDs, hashes, and provenance before fitting. No post-freeze replacement is permitted.

After split freeze, derive D-081 episode counts independently. Balanced sequential families include only subjects with at least one valid T1 episode and at least one valid T2 episode. Subjects with zero or one-class-only episodes remain in their frozen partition and in valid single-trial analyses; report their experiment-specific exclusion without replacement or reshuffling.

---

# 52. CROSS-SUBJECT CALIBRATION

Calibration must respect frozen subject boundaries where the scientific question concerns unseen subjects.

Do not:

```text
test subject labels
→ fit calibrator
→ call result cross-subject generalization
```

unless the experiment explicitly studies post-calibration personalization rather than zero-shot generalization.

Calibration method and fitting partition are governed by D-048 and D-049; protected subject labels never fit the calibrator.

# 53. WITHIN-SUBJECT VS CROSS-SUBJECT

These answer different questions.

## Within-subject

How well can a personalized decoder perform when subject-specific data are available?

## Cross-subject

How well does the system generalize before subject-specific adaptation?

Both may be reported.

They must not be mixed into one unlabeled average.

---

# 54. SUBJECT-WISE REPORTING

For cross-subject results, preserve:

- metric per held-out subject;
- mean;
- standard deviation or another approved variability measure;
- difficult subjects;
- failure cases.

Do not report only the average.

---

# 55. E9 — ADAPTATION EXPERIMENT

This experiment runs only if a specific adaptation mechanism is implemented and approved.

Compare:

```text
Adaptation OFF
vs
Adaptation ON
```

---

# 56. ADAPTATION DATA SEPARATION

If adaptation learns from feedback:

```text
adaptation episodes
```

must be separated from:

```text
post-adaptation evaluation episodes
```

when the objective is to measure improvement on later unseen interactions.

Do not adapt and evaluate on the exact same event while calling it generalization.

---

# 57. ADAPTATION HYPOTHESIS

> **H8: A simple approved personalization mechanism may improve later interaction performance for some subjects relative to a fixed system.**

Possible measured outcomes:

- fewer wrong commitments;
- fewer confirmations;
- lower latency;
- no meaningful change;
- harmful over-adaptation.

All are valid.

---

# 58. REPEATED RUNS / RANDOM SEEDS

Randomness may affect:

- neural-network initialization;
- train/validation split;
- data ordering;
- noise injection.

The M7-T02 seed policy is frozen by D-080 and `CURRENT_TASK.md`.

Possible options:

- one fixed seed for deterministic development;
- multiple seeds for reportable neural/stochastic experiments.

Primary operational randomness, R2 population selection, environment/reset randomness where needed, and the paired bootstrap use seed 42. Accepted upstream training/checkpoint artifacts retain their already-approved frozen seeds; no extra neural seeds are created as inferential samples.

---

# 59. SEED DISCIPLINE

Do not:

```text
run 20 seeds
→ report only the best one
```

If multiple seeds are used, report them consistently.

The experiment log must record each seed.

---

# 60. TRAIN / VALIDATION / TEST PROTECTION

The final test set should be treated as an evaluation resource, not a tuning dashboard.

Do not use final test performance to choose:

- filter band;
- epoch window;
- CSP component count;
- EEGNet hyperparameters;
- calibration method;
- confidence thresholds;
- risk \(\lambda\);
- adaptation parameters.

---

# 61. DEVELOPMENT SET VS FINAL TEST

The project may iterate freely on:

```text
training
validation
development maps
synthetic tests
```

within the approved protocol.

Final test data should be evaluated only after the relevant design is frozen.

---

# 62. LEAKAGE CHECKLIST BEFORE EVERY REPORTABLE EXPERIMENT

Verify:

- no test subjects in training for cross-subject experiment;
- no CSP fit on test data;
- no normalization fit on test data;
- no calibration fit on test labels;
- no threshold tuning on test outcomes;
- no adaptation using future test feedback;
- no hidden true goal passed into inference;
- no duplicated trial windows across train/test.

---

# 63. EXPERIMENT CONFIG SNAPSHOT

Every experiment must preserve the exact configuration.

Examples:

```text
dataset subjects/runs
preprocessing
split
model
calibration
Bayes
uncertainty policy
adaptation
map
planner
safety
seed
```

Do not rely on the current global config after the fact.

---

# 64. EXPERIMENT ARTIFACTS

Each reportable experiment should generate a folder conceptually like:

```text
results/
└── EXP-.../
    ├── config.yaml
    ├── metadata.json
    ├── predictions.csv
    ├── episode_log.csv
    ├── metrics.json
    ├── figures/
    └── tables/
```

Exact structure may vary.

---

# 65. EXPERIMENT METADATA

Minimum where applicable:

```text
experiment_id
date/time
Git commit
seed
dataset version
subjects
runs
split ID
model ID
calibrator ID
goal-mapping policy
Bayesian policy
uncertainty policy
adaptation policy
map ID
planner policy
safety policy
```

---

# 66. EXPERIMENT STATUS

Every experiment should have a status such as:

```text
VALID
INVALID
FAILED
PARTIAL
DEVELOPMENT_ONLY
```

An invalid experiment must not be quietly used in the final report.

---

# 67. INVALIDATION RULE

An experiment becomes invalid if, for example:

- leakage is discovered;
- wrong event labels were used;
- class order was reversed;
- test data influenced calibration;
- wrong map/policy was loaded;
- a critical logging failure prevents reconstruction.

Invalid experiments should be preserved for debugging but excluded from final results.

---

# 68. BASELINE FIRST RULE

Before testing complex System D, establish:

1. dataset validity;
2. CSP+LDA baseline;
3. EEGNet baseline;
4. calibration baseline;
5. synthetic Bayesian correctness;
6. autonomous planner baseline;
7. safety baseline.

This avoids end-to-end complexity hiding component failures.

---

# 69. COMPONENT VALIDITY GATE

A module should not enter a full-system experiment unless its standalone tests pass.

Examples:

```text
Bayes synthetic tests pass
A* unit tests pass
safety stop test passes
decoder probabilities valid
```

---

# 70. SYSTEM VALIDITY GATE

Before final A/B/C/D evaluation, verify:

- goal mapping approved;
- likelihood model approved;
- confidence policy frozen;
- safety policy frozen;
- experiment matrix frozen;
- split frozen;
- seeds frozen;
- metrics frozen.

---

# 71. HEADLESS EXECUTION

Final experiments should run through scripts, not manual UI clicking.

The dashboard may replay or inspect results.

Headless execution is required for reproducibility.

---

# 72. HUMAN-INTERACTION EXPERIMENTS

Because the core project is not currently a human-subject study, automated experiments may use a **simulated human policy**.

Example conceptual rule:

```text
if candidate == controlled intended goal:
    confirm
else:
    override
```

For M7-T02, D-080 and `CURRENT_TASK.md` freeze the deterministic simulated-human policy: no command for PROCEED; exact CONFIRM for a correct proposal; explicit OVERRIDE/correction for an incorrect CONFIRM proposal or DEFER; and PAUSE/STOP only in dedicated controlled scenarios. Hidden intended-goal truth is restricted to choosing that explicit command and evaluation scoring and must not enter inference or adaptation directly.

---

# 73. SIMULATED HUMAN CLAIM BOUNDARY

Results from such experiments measure:

> **system behavior under the defined simulated-human policy**

They do not measure:

- real human trust;
- actual workload;
- cognitive fatigue;
- usability.

---

# 74. FAILURE CASE PRESERVATION

For each major experiment family, preserve representative failure cases.

Examples:

## EEG

- confident wrong prediction;
- ambiguous trial.

## Bayes

- conflicting evidence;
- premature commitment.

## Shared autonomy

- excessive deferral;
- wrong confirmation request.

## Planning

- no path;
- costly replan.

## Safety

- unsafe proposal;
- safety intervention.

---

# 75. NEGATIVE RESULT RULE

The final report must include meaningful negative/mixed results.

Do not remove them because they weaken a simple “full system wins” narrative.

They strengthen scientific credibility.

---

# 76. D-079 SUBJECT-LEVEL STATISTICAL REPORTING

For real-EEG and subject-generalization comparisons, the subject is the primary inferential unit. Report the paired raw subject-level effect, individual subject values where practical, subject count, 95% paired bootstrap CI using 10,000 resamples and a recorded seed, and a two-sided paired sign-flip/permutation raw p-value.

---

# 77. PAIRED SIGN-FLIP POLICY

Use exact sign enumeration when feasible; for the complete paired final-test vector, enumerate all `2^n_final` assignments and record actual `n_final`. The former `2^17 = 131072` is the historical full-109 example. If exact enumeration is infeasible, use a deterministic recorded permutation sample. Trials, evidence observations, actions, maps, and neural-network seeds are not independent human subjects.

---

# 78. MULTIPLE COMPARISONS

Apply Holm correction across formal tests within the same experiment family. Preserve raw p-values and Holm-adjusted values. Deterministic planning/safety scenario validation remains descriptive/exhaustive absent a separately approved stochastic design.

---

# 79. REPORTABLE RESULT TABLES

The final results should support clear tables such as:

## EEG model comparison

| Model | Accuracy | Balanced Accuracy | F1 | ECE | Brier |
|---|---:|---:|---:|---:|---:|
| CSP+LDA | measured | measured | measured | measured | measured |
| EEGNet | measured | measured | measured | measured | measured |

## System comparison

| System | Wrong Goal | Deferrals | Decision Latency | Task Success | Safety Violations |
|---|---:|---:|---:|---:|---:|
| A | measured | measured | measured | measured | measured |
| B | measured | measured | measured | measured | measured |
| C | measured | measured | measured | measured | measured |
| D | measured | measured | measured | measured | measured |

No values are filled before real experiments.

---

# 80. REPORTABLE FIGURES

Potential final figures include:

- CSP/EEGNet performance comparison;
- reliability diagrams;
- posterior trajectory;
- entropy vs evidence update;
- wrong-goal vs latency trade-off;
- noise robustness curves;
- subject-wise cross-subject performance;
- path/risk trade-off;
- safety ON/OFF comparison;
- adaptation trajectory if implemented.

Every figure must be reproducible from stored result data.

---

# 81. CLAIM-TO-EXPERIMENT MAPPING

Every final claim should point to a specific experiment.

Example:

> “Calibration improved probability reliability.”

Requires:

```text
E2
```

> “Bayesian accumulation reduced wrong-goal commitment.”

Requires:

```text
E3 / E6
```

> “Safety reduced simulated violations.”

Requires:

```text
E5 / E7
```

No claim should exist without supporting experimental evidence.

---

# 82. REMAINING EXECUTION-SPECIFIC ITEMS

D-040 through D-083 resolve the scientific-policy items previously listed here. D-080 and `CURRENT_TASK.md` authorize and freeze M7-T02's exact final scenarios/maps, simulated-human rule, and operational seed policy; D-081 freezes fixed-intent episode construction; D-082 freezes actual post-QC cohort derivation and deterministic allocation; D-083 freezes one-per-class cross-subject eligibility and post-split experiment-specific sequential participation. Decoder/checkpoint/calibrator identities and the QC/split/episode/execution manifests must still be frozen before protected outcomes are inspected.

---

# 83. DECISIONS REQUIRED BEFORE FINAL REPORTABLE EXPERIMENTS

The scientific policies in items 1–11 and the subject-level statistical plan are approved in D-031 through D-079. M7-T02 is separately authorized by `CURRENT_TASK.md`, with its execution contract recorded by D-080, fixed-intent episode semantics recorded by D-081, post-QC cohort/allocation policy recorded by D-082, and eligibility/participation policy recorded by D-083. Its final execution manifest must freeze exact artifacts, inputs, QC/split/episode/inclusion manifest hashes, actual cohort values, and approved execution definitions before protected results are accessed.

---

# 84. EXPERIMENTAL ACCEPTANCE CRITERIA

The experimental design is correctly implemented when:

1. every experiment has a clear question;
2. every comparison changes only intended variables where possible;
3. test data remain protected;
4. subject leakage is prevented;
5. calibration leakage is prevented;
6. true goal remains evaluation-only;
7. A/B/C/D conditions are explicit;
8. ablations are modular;
9. robustness perturbations are mathematically defined;
10. seeds/configs are saved;
11. experiments run headlessly;
12. artifacts are machine-readable;
13. invalid experiments are marked;
14. subject-wise/failure cases are preserved;
15. negative results remain reportable;
16. final claims map to evidence.

---

# 85. CURRENT EXPERIMENTAL DESIGN SUMMARY

The project uses a layered experimental strategy. EEG experiments compare CSP+LDA and EEGNet on the same Left-vs-Right PhysioNet motor-imagery task. Calibration uses D-048 through D-050. Bayesian/shared-autonomy experiments use D-051 through D-057, while planning/safety experiments independently validate the accepted A*, D-061 through D-065 risk/safety behavior, action rejection, replanning, and emergency-stop behavior. D-077 freezes A/B/C/D, D-078 freezes robustness, D-079 freezes paired subject-level inference, D-081 freezes fixed-intent real-EEG episode construction, and D-082 freezes the actual post-QC cohort and deterministic 70/15/15 allocation. M7-T01 built and verified the development-only harness; D-080 and `CURRENT_TASK.md` authorize M7-T02 under committed governance and hard QC/split/episode/artifact/execution-manifest gates. All results must preserve provenance, explicit denominators, individual-subject structure, sample attrition, and negative or mixed outcomes.

---

# 86. NEXT DOCUMENT

The next planned document is:

**`18_METRICS_AND_EVALUATION.md` — Complete Metrics, Mathematical Definitions, Aggregation Rules, Statistical Reporting, and Evaluation Framework**

That document should define, precisely:

- accuracy;
- balanced accuracy;
- precision;
- recall;
- F1;
- confusion matrix;
- ECE;
- Brier Score;
- posterior confidence;
- entropy;
- decision latency;
- wrong-goal commitment;
- task success;
- path length;
- path efficiency;
- completion time;
- replanning;
- human interventions;
- safety violations;
- unsafe attempts;
- hazard exposure;
- safety overrides;
- subject-wise aggregation;
- seed/fold aggregation;
- and final reporting rules.

It must preserve any metric formulas that are still not approved rather than inventing them.
