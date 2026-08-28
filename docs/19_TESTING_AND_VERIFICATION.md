# 19_TESTING_AND_VERIFICATION.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Unit Testing, Integration Testing, Scientific Verification, Regression Testing, and End-to-End Validation

**Document ID:** I-03  
**Document class:** Experiments & Evaluation / Testing & Verification Specification  
**Authority level:** Subordinate to all Master Authority, Scenario, Architecture, Data, Neuroscience, ML, Bayesian, Shared-Autonomy, Planning, Safety, Implementation, Repository, Experimental Design, and Metrics documents  
**Status:** Authoritative testing and verification baseline; unresolved scientific parameters remain unresolved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND VERIFICATION RULE

This document defines **how the project proves that software works correctly and that scientific conclusions are valid**.

It must remain consistent with all previously approved project documents.

If this document conflicts with a higher-authority project document, the higher-authority document wins.

The core rule is:

> **Software correctness and scientific validity are different. The project requires both.**

A program can run successfully while still being scientifically wrong.

Examples:

```text
CSP fits on the whole dataset before splitting
→ software works
→ experiment is invalid
```

```text
T1/T2 labels are reversed
→ model trains
→ scientific interpretation is wrong
```

```text
Bayesian code produces normalized numbers
→ software works
→ likelihood semantics may still be invalid
```

Therefore verification must occur at multiple levels.

---

# 1. PURPOSE OF THIS DOCUMENT

This document defines:

- unit testing;
- integration testing;
- mathematical verification;
- dataset verification;
- leakage testing;
- model-interface testing;
- calibration testing;
- Bayesian analytical testing;
- uncertainty testing;
- adaptation testing;
- environment/planner testing;
- safety testing;
- shared-autonomy state-machine testing;
- offline replay testing;
- end-to-end testing;
- regression testing;
- manual scientific review gates;
- and final verification criteria.

---

# 2. TESTING LEVELS

The project uses five major verification levels:

```text
T1 — Unit correctness
T2 — Interface / integration correctness
T3 — Scientific / mathematical validity
T4 — End-to-end system validity
T5 — Regression / reproducibility validity
```

A module should not progress directly to end-to-end integration without passing the earlier levels relevant to it.

---

# 3. SOFTWARE CORRECTNESS VS SCIENTIFIC VALIDITY

## Software correctness asks:

- Does the function run?
- Are dimensions correct?
- Are outputs finite?
- Does save/load work?
- Does state transition correctly?

## Scientific validity asks:

- Are the correct EEG runs used?
- Are event labels correct?
- Is CSP fit only on training data?
- Is calibration fit only on allowed data?
- Does Bayesian inference use a valid likelihood?
- Does test data remain untouched?
- Does uncertainty actually influence behavior?
- Are safety claims limited to simulation?

Both are mandatory.

---

# 4. AUTOMATED TESTING PHILOSOPHY

Automated tests should be:

- small;
- deterministic;
- focused;
- fast where possible;
- independent of UI;
- reproducible.

Not every test should require:

- downloading the full EEG dataset;
- training EEGNet;
- running the entire simulation.

Large tests should be separated from ordinary unit tests.

---

# 5. TEST DIRECTORY

Recommended structure:

```text
tests/
├── test_config.py
├── test_loader.py
├── test_preprocessing.py
├── test_epochs.py
├── test_csp_lda.py
├── test_eegnet.py
├── test_decoder_interface.py
├── test_calibration.py
├── test_bayesian_intent.py
├── test_uncertainty.py
├── test_adaptation.py
├── test_environment.py
├── test_planner.py
├── test_safety.py
├── test_shared_controller.py
├── test_human_interface.py
├── test_replay.py
├── test_metrics.py
└── test_integration_*.py
```

Exact filenames may be refined.

---

# 6. TEST CATEGORIES

Recommended markers/categories:

```text
unit
integration
real_data
slow
model_training
end_to_end
regression
```

The exact test framework/marker implementation is not yet locked.

The important point is that expensive tests can be run separately.

---

# 7. TEST FIXTURES

Use synthetic or tiny controlled fixtures where possible.

Examples:

- synthetic probability vectors;
- synthetic EEG-shaped arrays;
- tiny grid maps;
- small Bayesian likelihood sequences;
- short human-action sequences.

Synthetic fixtures are for software verification only.

They are not scientific EEG results.

---

# 8. REAL-DATA VERIFICATION

Some stages require actual PhysioNet data.

Examples:

- loader;
- channel/montage inspection;
- annotation semantics;
- real epoch extraction;
- real CSP/LDA baseline;
- real EEGNet training.

These should use controlled subject/run subsets during development.

---

# 9. CONFIGURATION TESTS

## Required tests

- valid config loads;
- missing required field fails;
- invalid type fails;
- invalid range fails;
- unresolved required scientific parameter blocks module execution;
- deterministic seed config works.

## Scientific rule

Configuration must not silently substitute arbitrary defaults for unresolved scientific parameters.

---

# 10. EEG LOADER TESTS

## Automated tests

Verify:

- subject ID validation;
- run ID validation;
- expected metadata structure;
- file path handling;
- cache behavior where practical;
- invalid input handling.

## Real-data smoke test

Using at least one real subject/run:

- file downloads/loads;
- MNE Raw object exists;
- channels exist;
- annotations exist;
- sampling frequency is plausible;
- duration is non-zero.

---

# 11. LOADER MANUAL VERIFICATION

The project owner must inspect:

```text
subject ID
run ID
channel count
channel names
sampling frequency
duration
annotations
montage
```

The expected current dataset baseline is:

- 64 channels;
- 160 Hz;
- EEGBCI run semantics.

Unexpected values must be investigated, not ignored.

---

# 12. CHANNEL / MONTAGE VERIFICATION

Verify:

- standardized channel names are valid;
- no duplicate channels;
- montage attaches successfully;
- sensor positions look plausible;
- channel order is recorded.

A successful `set_montage()` call alone is not enough.

Manual inspection is required during early development.

---

# 13. EVENT-MAPPING TESTS

For runs:

```text
4
8
12
```

verify:

```text
T1 → Left-fist imagery
T2 → Right-fist imagery
```

Tests should reject accidental use of the hands-vs-feet run mapping.

---

# 14. T0 POLICY TEST

Once T0 handling is approved, tests should verify:

- T0 is handled exactly according to policy;
- binary task remains Left vs Right;
- T0 does not silently become a third class.

---

# 15. PREPROCESSING TESTS

After preprocessing parameters are approved, verify:

- expected sampling frequency;
- filter settings applied;
- reference applied;
- output dimensions;
- no NaN/Inf;
- channel order preserved;
- deterministic processing;
- artifact policy applied as documented.

---

# 16. PREPROCESSING SCIENTIFIC VERIFICATION

Manual checks should compare representative:

```text
raw signal
vs
processed signal
```

and inspect:

- PSD;
- expected frequency behavior;
- obvious distortion;
- epoch integrity.

The goal is not aesthetic signal appearance.

The goal is methodological correctness.

---

# 17. EPOCH TESTS

Verify:

- event count;
- epoch count;
- epoch shape;
- label count;
- metadata alignment;
- class presence;
- trial IDs unique;
- no empty epochs;
- no invalid values.

---

# 18. SPLIT TESTS

Split logic must be tested separately.

Required:

- train/validation/test sets non-overlapping;
- expected counts;
- deterministic for fixed seed;
- group constraints respected;
- subject boundaries respected for cross-subject mode.

---

# 19. SUBJECT-LEAKAGE TEST

For held-out-subject evaluation:

```text
train_subjects ∩ test_subjects = ∅
```

This should be an explicit automated assertion.

Similarly:

```text
validation_subjects ∩ test_subjects = ∅
```

where applicable.

---

# 20. TRIAL-LEAKAGE TEST

If multiple windows originate from one trial, all derived windows must remain within the same split group.

Automated tests should compare:

```text
original_trial_id
```

across partitions.

---

# 21. CSP LEAKAGE TEST

The pipeline must prove that CSP is fit only on training data.

Recommended implementation-level verification:

- CSP exists inside a training pipeline;
- fit receives train only;
- test transformation uses already-fit CSP.

A test should fail if CSP is fit before splitting.

---

# 22. NORMALIZATION LEAKAGE TEST

Any learned normalization/scaling must:

```text
fit on train
transform validation/test
```

A test or review should confirm no statistics are computed on the full dataset.

---

# 23. CSP+LDA UNIT TESTS

Use synthetic EEG-shaped data.

Verify:

- fit succeeds;
- transformed feature dimensions valid;
- predicted label shape;
- probability shape;
- probabilities sum to 1;
- class names preserved;
- save/load round trip.

---

# 24. CSP+LDA REAL-DATA SMOKE TEST

Using a small approved real-data split:

- train;
- predict;
- save probabilities;
- calculate metrics.

The numeric performance is not pre-specified.

The test verifies the pipeline functions scientifically.

---

# 25. EEGNET UNIT TESTS

Verify:

- forward pass;
- correct input dimensions;
- output dimensions;
- finite logits;
- probability conversion;
- loss/output compatibility;
- checkpoint save/load.

---

# 26. EEGNET TRAINING SMOKE TEST

Use a tiny dataset/subset.

Goal:

- one short training run;
- loss computed;
- backward pass works;
- validation runs;
- checkpoint can be restored.

This is not a reportable model-performance experiment.

---

# 27. EEGNET SCIENTIFIC VERIFICATION

Before reportable evaluation verify:

- train/validation/test separation;
- model-selection criterion defined;
- no final test early stopping;
- class order correct;
- channel order correct;
- checkpoint metadata preserved;
- test metrics calculated only after model selection.

---

# 28. DECODER INTERFACE TESTS

For both:

```text
CSP+LDA
EEGNet
```

verify the same output contract:

```text
model_id
class_names
probabilities
predicted_class
trial metadata
```

No downstream code should rely on model-specific probability ordering.

---

# 29. PROBABILITY VALIDATION TEST

Every decoder output must satisfy:

\[
0 \le p_i \le 1
\]

and:

\[
\sum_i p_i \approx 1
\]

Reject:

- NaN;
- Inf;
- negative probability;
- unnormalized output beyond tolerance.

---

# 30. CALIBRATION METRIC TESTS

## ECE

Use toy bins with independently calculable values.

## Brier Score

Use simple binary cases.

Example:

```text
y=1, p=1
→ Brier contribution = 0
```

```text
y=1, p=0
→ Brier contribution = 1
```

## Reliability data

Verify bin counts and means.

---

# 31. CALIBRATOR TESTS

After final calibration method approval:

- fit on allowed data;
- transform probabilities;
- preserve class order;
- output valid probabilities;
- save/load;
- test labels not required during inference.

---

# 32. CALIBRATION LEAKAGE TEST

Verify that:

```text
calibration_fit_ids
```

do not overlap with:

```text
final_test_ids
```

according to the approved split strategy.

This should be logged and, where practical, asserted automatically.

---

# 33. BAYESIAN ANALYTICAL TESTS

Bayesian math requires independently calculable tests.

Example:

Prior:

\[
[0.5,0.5]
\]

Likelihood:

\[
[0.8,0.2]
\]

Posterior must be:

\[
[0.8,0.2]
\]

---

# 34. BAYESIAN REPEATED-EVIDENCE TEST

Starting:

\[
[0.5,0.5]
\]

First likelihood:

\[
[0.8,0.2]
\]

gives:

\[
[0.8,0.2]
\]

Second same likelihood gives:

\[
\left[
\frac{0.64}{0.68},
\frac{0.04}{0.68}
\right]
\]

within tolerance.

---

# 35. BAYESIAN CONTRADICTORY-EVIDENCE TEST

Use opposing likelihoods.

Verify:

- posterior responds correctly;
- probability remains normalized;
- belief can move back toward ambiguity.

---

# 36. BAYESIAN K-HYPOTHESIS TEST

Use at least three named hypotheses.

Verify:

- generic \(K\)-class support;
- hypothesis order preserved;
- posterior normalized.

This proves the Bayesian core itself is not hard-coded to binary inference.

---

# 37. BAYESIAN INVALID-INPUT TESTS

Reject:

- negative prior;
- negative likelihood;
- all-zero likelihood;
- NaN/Inf;
- mismatched dimensions;
- mismatched hypothesis names.

---

# 38. BAYESIAN SCIENTIFIC VERIFICATION GATE

Real EEG may not feed the Bayesian core until:

1. goal-selection protocol approved;
2. likelihood semantics approved;
3. Goal-Evidence Adapter reviewed;
4. class/hypothesis mapping verified.

Normalized posterior numbers alone do not prove scientific validity.

---

# 39. GROUND-TRUTH LEAKAGE TEST

The hidden experimental:

```text
true_goal
```

must not be present in runtime Bayesian/shared-autonomy input.

Where practical, design schemas so:

```text
true_goal
```

exists only in evaluation records.

---

# 40. ENTROPY TESTS

For binary distribution:

```text
[0.5, 0.5]
```

entropy should be maximal.

For:

```text
[1.0, 0.0]
```

entropy should be minimal/zero within tolerance.

Reject invalid distributions.

---

# 41. NORMALIZED ENTROPY TEST

If normalized entropy is approved:

For uniform distribution over \(K\) hypotheses:

\[
H_{norm}=1
\]

For a fully concentrated distribution:

\[
H_{norm}=0
\]

within numerical tolerance.

---

# 42. UNCERTAINTY-BEHAVIOR TEST

To justify “uncertainty-aware,” test that changing uncertainty can change controller behavior.

Conceptually:

```text
same candidate goal
low uncertainty → one mode
high uncertainty → different mode
```

The exact modes depend on final thresholds/policy.

---

# 43. ADAPTATION TESTS

Only after mechanism approval.

Required:

- adaptation OFF leaves parameters unchanged;
- known feedback produces known update;
- bounds enforced;
- reset works;
- Subject A update does not affect Subject B;
- invalid feedback rejected;
- update logged.

---

# 44. ADAPTATION LEAKAGE TEST

Ensure adaptation at time \(t\) does not use:

- future episode labels;
- future corrections;
- final evaluation outcome not yet available.

---

# 45. ENVIRONMENT UNIT TESTS

Verify:

- map bounds;
- start validity;
- goal validity;
- UP/DOWN/LEFT/RIGHT;
- WAIT;
- blocked-cell rejection;
- deterministic reset;
- terminal goal state.

---

# 46. MAP CONFIGURATION TESTS

Reject:

- negative dimensions;
- start outside map;
- blocked start;
- invalid goal coordinate;
- malformed hazard map;
- mismatched map dimensions.

---

# 47. A* ANALYTICAL TESTS

## Empty grid

Expected path length equals Manhattan distance.

## Static obstacle

Route avoids obstacle.

## No path

Returns explicit failure.

## Risk-free

Risk-aware planner matches distance behavior when risk is zero.

---

# 48. A* RISK TEST

Using synthetic risk values only:

```text
short risky route
long safe route
```

Test that:

- \(\lambda=0\) favors the shortest route;
- sufficiently high synthetic \(\lambda\) can favor the safer route.

These tests validate code behavior.

They do not choose the final project \(\lambda\).

---

# 49. A* DETERMINISM TEST

Same map/config/request should produce the same path under fixed tie-breaking/configuration.

---

# 50. REPLANNING TEST

Procedure:

```text
plan
→ execute several steps
→ block a future route cell
→ replan
```

Verify:

- old plan invalidated;
- new route starts from current position;
- new route avoids block.

---

# 51. SAFETY UNIT TESTS

Required:

- valid action approved;
- invalid action rejected;
- out-of-bounds rejected;
- blocked cell rejected;
- paused movement rejected;
- emergency stop blocks movement;
- replan flag works;
- deterministic result.

---

# 52. PROHIBITED-HAZARD TEST

After hazard threshold/policy approval:

- traversable risk cell remains allowed;
- prohibited hazard rejected;
- cost cannot override hard safety.

---

# 53. EMERGENCY-STOP INTEGRATION TEST

During active navigation:

```text
STOP
```

then verify:

```text
zero further environment movement
```

This is a critical test.

---

# 54. PAUSE TEST

During navigation:

```text
PAUSE
```

then verify:

- position does not change;
- no queued move executes;
- state remains paused.

Resume behavior is tested only after final resume semantics are approved.

---

# 55. SAFETY-BYPASS TEST

Attempt to call environment execution through the full-system control path without a SafetyDecision.

The architecture should prevent or clearly flag this.

Goal:

> No normal autonomous action bypasses safety.

---

# 56. SHARED-AUTONOMY STATE-MACHINE TESTS

Once the policy is approved, verify legal states:

```text
WAITING_FOR_EEG
INFER_INTENT
UNCERTAIN
WAITING_FOR_CONFIRMATION
GOAL_APPROVED
NAVIGATING
PAUSED
STOPPED
COMPLETED
FAILED
```

---

# 57. ILLEGAL STATE-TRANSITION TESTS

Examples:

```text
STOPPED → NAVIGATING
```

without reset should fail.

```text
PAUSED → movement
```

without resume should fail.

---

# 58. HUMAN CONFIRMATION TEST

Verify:

- confirmation applies only to current request/selection;
- approved goal updates correctly;
- stale confirmation rejected.

---

# 59. HUMAN OVERRIDE TEST

Verify:

- current incorrect goal invalidated;
- current route stopped/invalidated;
- correction logged;
- control returns to approved transition path.

Exact Bayesian reset behavior remains dependent on final policy.

---

# 60. DUPLICATE HUMAN-ACTION TEST

Repeated same confirmation should not produce multiple commits.

Duplicate actions should be idempotent or explicitly rejected.

---

# 61. OFFLINE REPLAY TESTS

Verify:

- configured EEG sequence order;
- trial metadata preserved;
- no unintended duplicate evidence;
- reset works;
- pause works;
- stop works.

---

# 62. REPLAY CLAIM TEST

UI/text output must say:

```text
Offline EEG Replay
```

or:

```text
Simulated Real-Time BCI
```

It must not display:

```text
Live EEG
```

unless live acquisition is actually added later.

---

# 63. METRIC UNIT TESTS

Every metric function should have known-answer tests.

Examples:

- accuracy;
- balanced accuracy;
- F1;
- ECE;
- Brier;
- task success;
- wrong-goal rate;
- safety counts.

Metric calculations must not exist only in notebooks.

---

# 64. LOGGER TESTS

Verify:

- required metadata retained;
- serialization/deserialization;
- no field corruption;
- experiment IDs preserved;
- probability arrays remain aligned with class names;
- episode records append correctly.

---

# 65. EXPERIMENT-CONFIG SNAPSHOT TEST

A reportable experiment should save the exact config used.

Test:

```text
run experiment
→ snapshot exists
→ snapshot can be reloaded
```

---

# 66. GIT-METADATA TEST

Where Git is available, verify experiment metadata records:

```text
commit hash
```

and optionally dirty-working-tree status.

---

# 67. INTEGRATION TEST LEVELS

Integration should proceed progressively.

## I1

```text
Loader
→ preprocessing
→ epochs
```

## I2

```text
epochs
→ CSP/LDA
→ probability
```

## I3

```text
epochs
→ EEGNet
→ probability
```

## I4

```text
probability
→ calibration
```

## I5

```text
synthetic likelihood
→ Bayes
→ entropy
```

## I6

```text
synthetic belief
→ shared autonomy
```

## I7

```text
approved artificial goal
→ planner
→ safety
→ environment
```

## I8

```text
real EEG probability
→ approved adapter
→ Bayes
→ entropy
```

## I9

```text
complete offline EEG replay
→ full system
```

---

# 68. END-TO-END VALIDATION

The final core pipeline must execute:

```text
real PhysioNet EEG
→ preprocessing
→ decoder
→ calibrated probability
→ approved goal-evidence adapter
→ Bayesian update
→ entropy
→ shared-autonomy decision
→ approved goal
→ A*
→ safety
→ environment
→ result log
```

All module IDs/configs must remain traceable.

---

# 69. END-TO-END SUCCESS TEST

A controlled episode should demonstrate:

- valid EEG evidence;
- valid model output;
- valid posterior;
- valid uncertainty;
- goal approval;
- path planning;
- safe movement;
- task completion;
- complete log.

This proves integration.

It does not prove superiority over baselines.

---

# 70. END-TO-END WRONG-EVIDENCE TEST

Use a controlled evidence sequence leading toward the wrong candidate.

Verify the system behaves according to the approved uncertainty/human policy.

The experiment should not force correction unless that is part of the defined simulated-human policy.

---

# 71. END-TO-END UNCERTAIN-EVIDENCE TEST

Use ambiguous evidence.

Expected:

- higher uncertainty;
- defer/confirm behavior according to approved thresholds.

---

# 72. END-TO-END SAFETY TEST

Use an approved goal whose shortest route encounters a prohibited cell.

Verify:

- planner/safety interaction;
- unsafe action blocked;
- replan or no-safe-path outcome.

---

# 73. END-TO-END HUMAN STOP TEST

During a full replay/navigation episode:

```text
STOP
```

must immediately halt movement.

---

# 74. REGRESSION TESTING

Regression tests preserve already-verified behavior after later changes.

Examples:

- loader still reads correct annotations after preprocessing changes;
- Bayes tests still pass after adaptation is added;
- emergency stop still works after dashboard integration;
- class order remains correct after model serialization changes.

---

# 75. REGRESSION BASELINE

Once a module passes a critical test suite, preserve those tests permanently unless the approved requirement itself changes.

Do not delete failing tests merely to restore a green test suite.

---

# 76. BUG-FIX VERIFICATION

Every important bug fix should ideally add:

```text
a test that failed before the fix
and passes after the fix
```

This prevents recurrence.

---

# 77. SCIENTIFIC REGRESSION

Scientific regression occurs when code still runs but methodology degrades.

Examples:

- future refactor fits CSP before splitting;
- new calibrator accidentally uses test labels;
- dashboard introduces hidden goal truth into runtime.

Tests should protect against these where possible.

---

# 78. MANUAL SCIENTIFIC REVIEW GATES

Automated tests cannot verify everything.

The project owner/ChatGPT should manually review key points.

---

# 79. REVIEW GATE A — DATA

Verify:

- dataset;
- runs;
- channels;
- annotations;
- montage;
- labels.

Do not proceed if these are unclear.

---

# 80. REVIEW GATE B — PREPROCESSING

Verify:

- approved parameters;
- signal/PSD;
- epoch shapes;
- exclusions;
- split design.

---

# 81. REVIEW GATE C — DECODERS

Verify:

- CSP training boundary;
- EEGNet training boundary;
- class order;
- probability semantics;
- real metrics.

---

# 82. REVIEW GATE D — CALIBRATION

Verify:

- calibration partition;
- ECE;
- Brier;
- raw vs calibrated reliability.

---

# 83. REVIEW GATE E — BAYES

Verify:

- prior;
- likelihood semantics;
- posterior equation;
- synthetic analytical tests;
- no hidden ground truth.

---

# 84. REVIEW GATE F — SHARED AUTONOMY

Verify:

- threshold policy approved;
- human authority;
- proceed/confirm/defer logic;
- stop/pause behavior.

---

# 85. REVIEW GATE G — PLANNING / SAFETY

Verify:

- path correctness;
- hazard interpretation;
- \(\lambda\);
- safety precedence;
- no-safe-path behavior.

---

# 86. REVIEW GATE H — END TO END

Verify:

- real EEG reaches full system;
- logs complete;
- no scope/claim drift;
- experiment can be reproduced.

---

# 87. CODE REVIEW REQUIREMENT

For scientifically important modules, ChatGPT should independently review actual:

- source code;
- tests;
- config;
- logs;
- outputs.

Codex's summary is not proof.

---

# 88. TEST PASS LEVELS

Recommended task status:

```text
PASS
PARTIAL
BLOCKED
FAIL
```

## PASS

All required tests/checks passed.

## PARTIAL

Implementation works partly, but acceptance criteria incomplete.

## BLOCKED

Cannot proceed due to unresolved decision/dependency.

## FAIL

Implementation does not meet current requirements.

---

# 89. BLOCKED IS A VALID RESULT

If a task reaches an unresolved scientific choice:

```text
BLOCKED
```

is preferable to inventing a value.

Examples:

- goal mapping undefined;
- calibration method unapproved;
- threshold not frozen.

---

# 90. TEST ARTIFACTS

Important tests may save artifacts such as:

```text
validation summaries
test logs
example posterior trajectories
path JSON
safety logs
```

Large temporary test artifacts should not clutter the repository.

---

# 91. CONTINUOUS TEST EXECUTION

The project may run automated tests after each module/commit.

No external CI platform is required for the core project.

Local reproducible test commands are sufficient initially.

---

# 92. TEST COMMAND DOCUMENTATION

Every module completion report should include exact commands such as:

```text
python -m ...
```

or the selected test-runner command.

The exact testing framework syntax should be documented once standardized.

---

# 93. ENVIRONMENT REPRODUCIBILITY

Tests should record/confirm:

- Python version;
- important package versions;
- CPU/GPU where relevant.

EEGNet GPU tests may differ slightly numerically across hardware.

---

# 94. TOLERANCES

Floating-point tests should use explicit reasonable tolerance.

Examples:

```text
probability sums ≈ 1
posterior values ≈ analytical expectation
```

Do not require unrealistic exact equality for floating-point calculations.

---

# 95. RANDOMNESS IN TESTS

Tests should avoid uncontrolled randomness.

If randomness is required:

- fix seed;
- record it;
- use deterministic expected properties.

---

# 96. PERFORMANCE TESTING — SECONDARY

Potential runtime checks:

- EEGNet inference time;
- A* planning time;
- replay throughput.

These are secondary.

Do not optimize before correctness is established.

---

# 97. STRESS TESTING

Useful controlled stress cases include:

- invalid data;
- ambiguous EEG probability;
- contradictory Bayesian evidence;
- no path;
- repeated safety rejection;
- high-risk route;
- emergency stop;
- corrupted config.

---

# 98. CLAIM VERIFICATION

Before any final claim enters README/resume/report, verify:

```text
claim
→ experiment ID
→ result artifact
→ metric
→ valid methodology
```

If this chain does not exist, the claim is not ready.

---

# 99. NO FABRICATED TEST SUCCESS

Do not write:

```text
all tests passed
```

unless the tests were actually executed.

Test execution output should be available in the Codex completion report or logs.

---

# 100. NO FABRICATED RESULTS

Unit tests may contain synthetic numbers.

Those must never be transferred into:

- Results;
- README performance;
- resume metrics.

Synthetic expected values are verification fixtures only.

---

# 101. TESTING OF A/B/C/D EXPERIMENTS

Before comparing A/B/C/D:

- each system condition must pass standalone execution;
- component matrix must be frozen;
- same episode inputs must be reusable;
- metrics must be consistent.

---

# 102. ABLATION VERIFICATION

For each ablation, verify that exactly the intended component is disabled.

Example:

```text
Full - Bayes
```

must not also silently disable calibration and uncertainty unless that is part of the explicitly defined condition.

---

# 103. ROBUSTNESS TEST VERIFICATION

Noise/degradation experiments must verify:

- perturbation actually applied;
- original evidence preserved;
- severity recorded;
- seed recorded;
- labels unchanged unless experiment explicitly defines label noise.

---

# 104. CROSS-SUBJECT VERIFICATION

Before each cross-subject run, automatically print/save:

```text
train subjects
validation subjects
test subjects
overlap check
```

Any overlap invalidates that run.

---

# 105. ADAPTATION-ON/OFF VERIFICATION

When adaptation is disabled:

- adaptation state must remain unchanged;
- output logs should confirm `adaptation_enabled=false`.

When enabled:

- each change should be logged.

---

# 106. FINAL SYSTEM VERIFICATION CHECKLIST

Before declaring the core project complete, verify:

1. PhysioNet data loads.
2. Correct runs/labels are used.
3. Preprocessing is approved and reproducible.
4. Splits are leakage-safe.
5. CSP+LDA passes tests and real-data evaluation.
6. EEGNet passes tests and real-data evaluation.
7. Decoder interface is stable.
8. Calibration metrics are correct.
9. Final calibrator uses non-test data only.
10. Bayesian core passes analytical tests.
11. Goal-evidence mapping is explicitly approved.
12. Likelihood semantics are documented.
13. Entropy is correct.
14. Uncertainty changes behavior.
15. Adaptation matches the approved mechanism if implemented.
16. Environment works.
17. A* works.
18. Safety intercepts actions.
19. Human confirm/override/pause/stop work.
20. Offline replay preserves evidence ordering.
21. Full EEG-derived pipeline runs end to end.
22. A/B/C/D experiments are reproducible.
23. Ablations are verified.
24. Cross-subject overlap is zero in held-out experiments.
25. Results map to real experiment artifacts.
26. Unsupported claims are absent.

---

# 107. ACCEPTANCE CRITERIA — TESTING INFRASTRUCTURE

The testing framework is acceptable when:

1. each major module has appropriate tests;
2. expensive tests can be separated from fast tests;
3. synthetic fixtures remain distinct from scientific data;
4. deterministic seeds are used where needed;
5. failures are explicit;
6. unresolved scientific choices block instead of defaulting;
7. mathematical tests use known answers;
8. leakage checks exist;
9. integration tests follow architecture boundaries;
10. regression tests preserve critical behavior;
11. commands are reproducible;
12. actual execution results are reported honestly.

---

# 108. ACCEPTANCE CRITERIA — SCIENTIFIC VERIFICATION

Scientific verification is acceptable when:

1. dataset semantics are manually confirmed;
2. labels are correct;
3. train/test boundaries are audited;
4. CSP fitting boundary is verified;
5. calibration fitting boundary is verified;
6. Bayesian likelihood semantics are approved;
7. true-goal leakage is absent;
8. uncertainty affects behavior;
9. safety remains independent from confidence;
10. final metrics are computed from valid experiment logs;
11. negative/failure cases remain visible;
12. final claims are evidence-backed.

---

# 109. CURRENT TESTING & VERIFICATION SUMMARY

The project uses a layered verification strategy that separates software correctness from scientific validity. Unit tests verify individual functions, interfaces, numerical behavior, state transitions, and serialization. Integration tests verify controlled module boundaries such as EEG→decoder, probability→calibration, synthetic likelihood→Bayesian posterior, belief→shared autonomy, and approved goal→A*→safety→environment. Scientific verification separately audits dataset run semantics, T1/T2 labels, train/test leakage, CSP fitting boundaries, calibration partitioning, Bayesian likelihood semantics, hidden-ground-truth separation, and claim validity. Real EEG smoke tests complement synthetic fixtures, while analytical probability tests verify Bayesian updates, entropy, calibration metrics, and core evaluation formulas. End-to-end validation must eventually demonstrate a real PhysioNet EEG replay passing through decoding, calibration, approved goal-evidence mapping, Bayesian inference, uncertainty-aware shared autonomy, planning, safety, and environment execution with complete logs. Regression tests then protect previously verified behavior as the system evolves. A task reaching an unresolved scientific decision must be marked **BLOCKED**, not “solved” through an invented default.

---

# 110. NEXT DOCUMENT

The next planned document is:

**`20_LIMITATIONS_ETHICS_AND_VALIDITY.md` — Limitations, Ethical Boundaries, Internal/External Validity, Threats to Validity, and Responsible Claiming**

That document should define:

- offline EEG limitation;
- motor-imagery limitation;
- simulation limitation;
- binary-interface limitation;
- subject variability;
- cross-subject limits;
- model/calibration limitations;
- Bayesian assumptions;
- simplified cognition;
- adaptation limitations;
- safety limitations;
- no clinical claims;
- no thought-reading claims;
- no real rescue validation;
- public-dataset ethics;
- internal validity;
- construct validity;
- external validity;
- reproducibility threats;
- and responsible reporting.

It should make the final technical report scientifically defensible without unnecessarily weakening the project.
