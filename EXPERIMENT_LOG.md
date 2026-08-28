# EXPERIMENT_LOG.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Reproducible Experiment Register

**Purpose:** Record experiments that were actually executed  
**Current status:** No valid experiments executed yet  
**Rule:** Hypothetical, planned, or synthetic examples must not be logged as completed reportable experiments

---

# 1. CURRENT EXPERIMENT STATUS

```text
Validated experiments:
NONE

Invalidated experiments:
NONE

Current active experiment:
NONE
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

Freeze the exact component matrix before execution.

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
```

Examples:

```text
probability corruption
ambiguous evidence
contradictory evidence
signal degradation
blocked route
hazard changes
```

---

# 15. CROSS-SUBJECT RULE

For held-out-subject evaluation:

```text
train_subjects ∩ test_subjects = ∅
```

Record the actual subject lists.

Do not summarize only with a single overall average.

---

# 16. RESULT CLAIM RULE

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

# 17. CURRENT LOG

No reportable experiment has been executed yet.

The first entries should be added only after implementation and experiment execution begin.
