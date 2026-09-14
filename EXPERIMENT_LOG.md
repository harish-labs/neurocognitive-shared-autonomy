# EXPERIMENT_LOG.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Reproducible Experiment Register

**Purpose:** Record experiments that were actually executed  
**Current status:** R02 candidate results executed; scientific review pending.
**Rule:** Hypothetical, planned, or synthetic examples must not be logged as completed reportable experiments

---

# 1. CURRENT EXPERIMENT STATUS

```text
Validated experiments:
NONE — no final scientific claim is approved pending review.

Invalidated experiments:
M7-T02 v1 and v2 (preserved; invalid implementation contracts)

Current active experiment:
M7-T02-R02 candidate v3
```

---

# 2. EXPERIMENT ID FORMAT

Recommended:

```text
E<family>-<module>-<sequence>
```

Examples:

```text
E1-CSP-001
E1-EEGNET-001
E2-CAL-001
E3-BAYES-001
E6-SYSTEM-001
E7-ABLATION-001
```

---

# 3. EXPERIMENT FAMILIES

```text
E1 — EEG Decoding
E2 — Probability Calibration
E3 — Bayesian Goal Inference
E4 — Uncertainty / Shared Autonomy
E5 — Planning / Safety
E6 — A/B/C/D System Comparison
E7 — Ablations / Robustness
E8 — Cross-Subject Evaluation
E9 — Adaptation
```

---

# 4. VALIDITY STATES

Use:

```text
PLANNED
RUNNING
VALID
INVALID
PARTIAL
BLOCKED
```

Only `VALID` experiments may support final claims.

---

# 5. REQUIRED EXPERIMENT RECORD

Use the following template.

```text
## <Experiment ID> — <Title>

Date:
YYYY-MM-DD

Status:
PLANNED / RUNNING / VALID / INVALID / PARTIAL / BLOCKED

Objective:
<exact question being tested>

Hypothesis:
<if applicable>

System condition:
A / B / C / D / Ablation / Other

Git commit:
<commit hash>

Code version:
<branch / tag if relevant>

Configuration:
<config path / snapshot>

Random seed(s):
<seed values>

Dataset:
<dataset>

Subjects:
<subject IDs>

Runs:
<run IDs>

Trials:
<count / selection>

Train split:
<manifest / IDs>

Validation split:
<manifest / IDs>

Test split:
<manifest / IDs>

Preprocessing:
<exact approved configuration>

Model:
<model ID>

Checkpoint:
<path / model ID>

Calibration:
<method / calibrator ID / none>

Bayesian configuration:
<prior / likelihood adapter / commitment rule>

Shared-autonomy configuration:
<thresholds / policy>

Adaptation:
<enabled / disabled / mechanism>

SAR map:
<map config>

Risk / Safety:
<config>

Perturbation:
<if robustness experiment>

Command:
<exact command>

Machine-readable outputs:
<paths>

Figures:
<paths>

Metrics:
<actual measured values>

Statistical analysis:
<method / result>

Manual verification:
<PASS / FAIL + notes>

Leakage checks:
<PASS / FAIL + details>

Validity assessment:
<why the experiment is or is not valid>

Failure cases:
<observed failures>

Interpretation:
<brief evidence-bound interpretation>

Eligible for final report:
YES / NO

Linked result section:
<optional>
```

---

# 6. REQUIRED TRACEABILITY

Every reportable experiment should be reconstructable from:

```text
experiment ID
Git commit
configuration
subject/run IDs
split manifest
seed
model checkpoint
calibrator
policy
map
raw outputs
metrics
```

If this is impossible, the experiment should not be treated as final-report quality.

---

# 7. INVALIDATION RULES

Mark an experiment `INVALID` if any of the following occurred:

```text
subject leakage
trial leakage
CSP fitted before split
normalization fitted on test data
calibrator fitted on test labels
test set used for tuning
wrong T1/T2 semantics
class order mismatch
wrong configuration
true goal leaked into inference
implementation scientifically incorrect
provenance missing
result cannot be reproduced
```

Do not delete invalid experiments.

Preserve them for audit and learning.

---

# 8. SYNTHETIC TESTS

Synthetic tests may verify:

```text
Bayes equations
entropy
planner behavior
safety rules
shared-autonomy transitions
```

They are not empirical EEG results.

If logged, clearly mark:

```text
TEST / SYNTHETIC
NOT ELIGIBLE FOR PERFORMANCE CLAIM
```

---

# 9. EEG EXPERIMENT TEMPLATE

Typical E1 comparison:

```text
CSP + LDA
vs
EEGNet / Compact CNN
```

Potential metrics:

```text
accuracy
balanced accuracy
precision
recall
F1
confusion matrix
```

Cross-subject / subject-wise results should be preserved where applicable.

---

# 10. CALIBRATION EXPERIMENT TEMPLATE

Compare:

```text
raw probabilities
vs
calibrated probabilities
```

Metrics:

```text
ECE
Brier Score
Reliability Diagram
```

Do not claim calibration improved performance unless supported by the actual calibration metrics.

---

# 11. BAYESIAN EXPERIMENT TEMPLATE

Potential measures:

```text
goal inference accuracy
posterior trajectory
entropy
wrong-goal commitment
leader switches
evidence steps to commitment
decision latency
recovery after misleading evidence
```

---

# 12. A/B/C/D EXPERIMENT TEMPLATE

D-077 freezes the exact component matrix. M7-T01 development checks are not reportable experiments; protected final execution remains reserved for separately authorized M7-T02.

Then compare:

```text
A — Direct EEG
B — Confidence-aware
C — Bayesian shared autonomy
D — Full system
```

Potential outcomes:

```text
task success
wrong-goal commitment
decision latency
human intervention
risk exposure
safety events
path cost
```

No condition is pre-labeled as the winner.

---

# 13. ABLATION EXPERIMENT TEMPLATE

Potential ablations:

```text
Full
Full - calibration
Full - Bayes
Full - uncertainty
Full - safety
Full - adaptation
```

A valid ablation should modify only the targeted component.

---

# 14. ROBUSTNESS EXPERIMENT TEMPLATE

For each perturbation record:

```text
definition
severity
seed
original evidence
perturbed evidence
labels unchanged?
selection rule and selected global observation identities/indices
evidence-population size and realized contamination count/fraction where applicable
```

Frozen D-078 families:

```text
R1 evidence flattening: epsilon = 0.00, 0.25, 0.50, 0.75, 1.00
R2 contradictory-evidence swap: q = 0.00, 0.10, 0.20, 0.30, 0.40,
selected once across the complete ordered condition/evaluation-run evidence population
```

---

# 15. M7 MACHINE-READABLE RESULT REQUIREMENTS

M7 result artifacts must preserve, where applicable:

```text
experiment family and ID
condition and ablation
decoder family
split and evaluation track
anonymous subject key
all operational/statistical/perturbation seeds
perturbation family, requested severity, seed, population size, selection rule,
selected global observation identities/indices, realized count/fraction, and original/perturbed evidence
effective operational configuration
scientific-policy identifiers
input trial/evidence provenance
metric evaluation units, numerators, and denominators
subject-level values before aggregation
aggregate values
paired statistics, raw p-values, and Holm-adjusted p-values
caller-supplied software/Git SHA
```

M7-T01 records must be marked `DEVELOPMENT_ONLY` and must fail closed on protected final-test splits. They are not eligible for final performance claims.

---

# 16. CROSS-SUBJECT RULE

For held-out-subject evaluation:

```text
train_subjects ∩ test_subjects = ∅
```

Record the actual subject lists.

Do not summarize only with a single overall average.

---

# 17. RESULT CLAIM RULE

A result may be used in:

```text
README
resume
portfolio
technical report
presentation
```

only if:

```text
experiment is VALID
+
metric definition is clear
+
artifact exists
+
reproducibility is sufficient
```

---

# 18. CURRENT LOG

No reportable experiment has been executed yet.

The first entries should be added only after implementation and experiment execution begin.

---

# 19. M7-T02 PRE-FINAL AUDIT CHECKPOINT — BLOCKED

**Date:** 2026-09-13
**Generating software SHA:** `f7260b0c3fe25c5364943857d0fc8c22a608e6a2`
**Policy:** D-035, D-040–D-042, D-079, D-081–D-083
**Protected outcomes accessed:** No

Completed pre-final work:

- audited all 109 EEGBCI source subjects under fixed D-035 QC;
- froze 68 D-083-eligible subjects and 41 exclusions with reasons;
- froze the D-082 split at 48 train / 10 validation / 10 final-test subjects;
- froze 261 D-081 episodes from 2,017 retained source trials, with 1,305 sequential observations and 712 tail observations;
- froze D-083 final sequential participation: 8 included, one no-episode exclusion, and one one-class-only exclusion, with no replacement.

Manifest file hashes:

- QC/eligibility: `a37dfeed5253533d47c1354b63616ae4ed19d01aec659acdf665bc8aa4f8f8cd`
- split: `befd67eaa0a14d96c8386447e424e606f829542c73ece86843fd6de252429ae8`
- episodes: `2c38cd6066422d54a35b5ff5d17da65dad687e163c3763aa690edef8ecafed03`
- participation: `8de4367ab2d274c28dff38c331c1af22e0a52815be6914f208d3c0225da11286`

Execution stopped before artifact fitting, final-execution-manifest freeze, or E1–E9 because the approved authorities do not define executable replacement decision semantics for `Full - Bayes` and `Full - uncertainty`. No result, probability, logit, prediction, calibration outcome, or downstream intent outcome from the protected final cohort was computed. This is a pre-final audit checkpoint, not a reportable efficacy experiment.
# M7-T02 protected execution (first outcome access)

- first protected outcome access occurred during the initial frozen-run attempt bound to manifest `57ccfa3e14db82954e3a14cceac429c10d701267ccbd55e207872bcf182239db` / software SHA `8d9ca7d`; execution failed closed at the Bayesian probability normalization boundary before producing reportable results.

- execution manifest: `results/m7/manifest/m7-final-execution-v5-d084-runner2.json`
- manifest SHA-256: `a5a552fc09055f812ab6bee10ba8622c419d19bf291c5707991fa368ef1429fa`
- runner/software SHA: `f1724f3`
- result artifact: `results/m7/final/m7-final-results-v1.json`
- result SHA-256: `c931f58b92b676bfbb8a184446ddb39da5011f279d84d419245503d8db139c5c`
- protected final subjects: `89,16,34,29,84,57,31,93,21,76`
- validity: E1-E9 executed from frozen D-084 contract; no subsequent scientific tuning

## M7-T02-R01 contract-correction rerun

- prior result `results/m7/final/m7-final-results-v1.json` (`c931f58b92b676bfbb8a184446ddb39da5011f279d84d419245503d8db139c5c`) is `INVALID_IMPLEMENTATION_CONTRACT` and remains preserved.
- invalidation reasons: D-083 sequential participation leakage; non-faithful Full adaptation and safety ablations; incorrect E7/E8 family assignment.
- R01 is a contract-correction rerun only; no model/calibrator refit, scientific threshold change, split change, or tuning occurred.
- execution manifest: `results/m7/manifest/m7-final-execution-v5-d084-r01.json` (`5980ff27c2459f22210c035b776d05a16ad00855a7b498916f90f43a8888252c`)
- corrected result: `results/m7/final/m7-final-results-v2.json` (`917f48b96ae47e8d38a867c1a9adc41b08607a3fc07cd2c0c2c5528aa5ba26e2`)
- sequential subjects: `89,16,34,29,31,93,21,76`; subjects `57,84` excluded from sequential analyses.

## M7-T02-R02 mission-orchestration correction

- v2 `results/m7/final/m7-final-results-v2.json` (`917f48b96ae47e8d38a867c1a9adc41b08607a3fc07cd2c0c2c5528aa5ba26e2`) is preserved as `INVALID_IMPLEMENTATION_CONTRACT` because E6 used S1-S7 instead of the per-episode frozen M6 mission map, and E7 safety was not mission-local.
- R02 is an implementation-contract correction only: no refitting, split change, threshold change, metric change, or result-driven tuning occurred.
- execution manifest: `results/m7/manifest/m7-final-execution-v5-d084-r02.json` (`cf99aac9a82c15b1cd2afb26490e976c324c90581007361e8e6bdd8fffa6ef6e`)
- corrected v3 result: `results/m7/final/m7-final-results-v3.json` (`be16490455e8c19e37378083db0332f91cbeb4d8aa111755fed341a43798e962`)
- E5 remains the frozen S1-S7 controlled planning/safety suite. E6 and the Full/Full-minus-safety E7 comparisons execute each episode's actual approved goal on the frozen two-goal M6 mission map.

## M7-T02-R03 completion remediation

- failed protected attempt 1: descriptive-uncertainty input normalization; no v4 artifact created.
- failed protected attempt 2: D-078 condition-evidence normalization; no v4 artifact created.
- both failures were fail-closed mechanical boundary defects. No tuning or refitting occurred.
- R03 v4 result: `results/m7/final/m7-final-results-v4.json` (`0eb854db327debab5edd1da156555fc83320e94696ff84886b97a6594bed769d`), using manifest `results/m7/manifest/m7-final-execution-v5-d084-r03.json` (`0c446cf83a2b4c5a79317d9848bbec3b3725f8038cff1e8d9e78b7ffbb8c15fc`).
- v1, v2, and v3 remain preserved as `INVALID_IMPLEMENTATION_CONTRACT` artifacts.
