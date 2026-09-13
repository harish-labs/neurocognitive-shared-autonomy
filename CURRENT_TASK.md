# CURRENT_TASK.md

## Current Codex Implementation Authority

**Current status:** ACTIVE / AUTHORIZED
**Current milestone:** M7 — Experiments / Ablations / Robustness
**Task ID:** M7-T01
**Task title:** Consolidated Experiment & Evaluation Harness
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical branch:** main
**Authorized task branch:** `task/m7-t01-experiment-evaluation-harness`
**Pre-authorization canonical main:** `19fadbdfa0cbe3bae57ac3be9be1f2fb8c808d21`

---

# 1. AUTHORIZATION

The Project Owner explicitly authorizes M7-T01 as one consolidated implementation phase.

This authorization is intentionally broad enough to finish the complete experiment/evaluation harness without splitting it into micro-tasks, while preserving the protected-final-test boundary. D-077, D-078, and D-079 are the governing experimental decisions.

M7-T02 — Frozen Final Experiment Execution & Scientific Audit remains NOT AUTHORIZED.

---

# 2. PURPOSE

Implement and verify the deterministic, reproducible evaluation infrastructure required to run the approved M7 experiment families without yet executing protected final-test experiments.

M7-T01 must provide the machinery needed for:

```text
E1 — EEG decoding evaluation
E2 — probability calibration evaluation
E3 — Bayesian goal-inference evaluation
E4 — uncertainty/shared-autonomy evaluation
E5 — planning/safety evaluation
E6 — principal A/B/C/D comparison
E7 — component ablations and robustness
E8 — cross-subject aggregation
E9 — adaptation evaluation
```

The harness must be capable of representing these experiment families, but protected final-test execution and reportable final results remain reserved for M7-T02.

---

# 3. REQUIRED IMPLEMENTATION SCOPE

M7-T01 shall implement, as one coherent evaluation subsystem:

## 3.1 Condition registry / experiment definitions

Represent the frozen D-077 principal conditions exactly:

```text
A — Direct EEG
B — Confidence-Aware
C — Bayesian Shared Autonomy
D — Full System
```

The implementation must encode the approved component membership and must not silently redefine the matrix.

Support the required component ablations where applicable:

```text
Full
Full - calibration
Full - Bayes
Full - uncertainty
Full - safety
Full - adaptation
```

Ablation construction must change only the intended component and preserve unrelated components.

## 3.2 Metrics

Provide deterministic metric computation with explicit evaluation units and denominators for the approved evaluation layers, including at minimum:

```text
EEG:
accuracy
balanced accuracy
per-class precision / recall / F1
macro F1
confusion matrix

Calibration:
10 equal-width-bin reliability data under D-050
ECE under D-050
Brier Score

Bayesian / shared autonomy:
goal inference / commitment correctness
wrong-goal commitment
posterior confidence
entropy
accepted evidence count / decision latency
PROCEED / CONFIRM / DEFER counts and rates
human intervention counts where applicable

Planning / safety:
path length
approved D-062 cumulative risk exposure
path/planning cost where available
replanning count
unsafe action attempts
executed hard-safety violations
NO_SAFE_PATH / unreachable outcomes

Full system:
task success
wrong-goal commitment
decision latency separated from navigation/environment steps
confirmation / override / deferral counts
navigation/safety outcomes
```

Wrong-goal rate and task-success denominators must be explicit and machine-readable. Do not collapse unrelated dimensions into a composite overall score.

## 3.3 Robustness

Implement D-078 exactly:

```text
R1 evidence flattening:
p_epsilon = (1-epsilon) * p + epsilon * [0.5, 0.5]
epsilon = {0.00, 0.25, 0.50, 0.75, 1.00}

R2 contradictory-evidence contamination:
[pA, pB] -> [pB, pA]
q = {0.00, 0.10, 0.20, 0.30, 0.40}
```

Contamination selection must be deterministic under a recorded fixed seed/index rule. Original and perturbed evidence, perturbation family, severity, seed, and selected indices must be auditable.

Do not add signal-level EEG noise as a core M7-T01 requirement.

## 3.4 Inferential statistics

Implement D-079 subject-level inference:

```text
paired raw subject-level effect
95% paired bootstrap CI
10,000 bootstrap resamples
fixed recorded seed
two-sided paired sign-flip/permutation test
exact 2^17 sign enumeration when the complete 17-subject paired final-test vector is later supplied and feasible
Holm correction within an experiment family
```

The implementation must prevent trial/evidence/action/map/seed observations from being silently treated as independent human subjects.

Planner/safety deterministic scenario validation should remain descriptive/exhaustive unless a separately approved stochastic design exists.

## 3.5 Reproducibility / result schema

Provide deterministic machine-readable result/provenance structures sufficient to record, where applicable:

```text
experiment family / experiment ID
condition / ablation
decoder family
split / evaluation track
subject identity or anonymous subject key
seed(s)
perturbation family / severity / selected indices
effective operational configuration
relevant scientific-policy identifiers
input evidence/trial provenance
metric definitions / denominators
subject-level metrics
aggregate metrics
statistical outputs
software/git SHA supplied by the caller/runtime
```

Do not fabricate unavailable provenance. Fail closed or mark a field explicitly unavailable only where the schema permits it.

## 3.6 Experiment orchestration

Provide deterministic orchestration sufficient to evaluate synthetic/development inputs and already-produced module outputs through the approved condition/metric/robustness/statistics interfaces.

Reuse accepted production modules rather than duplicating Bayesian, shared-autonomy, planner, safety, navigation, decoder, or calibration logic.

M7-T01 is evaluation infrastructure, not a rewrite of accepted M1–M6 scientific/runtime modules.

## 3.7 Documentation reconciliation

Update `docs/17_EXPERIMENTAL_DESIGN.md` and `docs/18_METRICS_AND_EVALUATION.md` only as needed to reconcile stale TBD/unresolved language with already-approved decisions D-048 through D-057 and D-077 through D-079 and with the actual M7-T01 implementation.

Do not introduce new scientific policy through documentation edits.

---

# 4. PROTECTED FINAL-TEST BOUNDARY

M7-T01 MUST NOT execute, inspect, summarize, tune against, or produce reportable outcomes from the protected final-test cohort.

The harness may implement generic support needed for later final evaluation, but M7-T01 verification must use only:

```text
synthetic fixtures;
approved development/training/validation data or previously accepted non-final-test artifacts where leakage-safe;
deterministic mock/module outputs;
controlled planner/safety scenarios.
```

No threshold, calibration method, perturbation level, ablation definition, metric rule, statistical rule, or scientific parameter may be tuned using final-test outcomes.

Any attempt by the task to require final-test outcome access is a STOP condition and must return to the Project Owner.

---

# 5. AUTHORIZED FILE BOUNDARY

M7-T01 may add or modify only files needed for the evaluation harness within these boundaries:

```text
src/evaluation/**                    new evaluation package preferred
tests/test_evaluation_*.py           focused evaluation tests
tests/test_m7_*.py                   M7 integration/evaluation tests where needed
docs/17_EXPERIMENTAL_DESIGN.md       reconciliation only
docs/18_METRICS_AND_EVALUATION.md    reconciliation only
EXPERIMENT_LOG.md                    schema/template clarification only; no fabricated results
```

If a minimal package initializer is required under `src/evaluation/`, it is included.

Existing production scientific/runtime modules under `src/eeg/`, `src/models/`, `src/cognitive/`, `src/control/`, and `src/autonomy/` are READ-ONLY for this task unless an actual defect blocks the approved harness. A required production-module change is a STOP condition and requires review/authorization rather than silent scope expansion.

`config.yaml`, `src/config.py`, `requirements.txt`, `.github/**`, UI/demo code, model artifacts, split manifests, and protected result artifacts are READ-ONLY unless separately authorized.

No new dependency is authorized. Use the existing declared stack.

---

# 6. SCIENTIFIC / ARCHITECTURAL CONSTRAINTS

M7-T01 must preserve all approved authority, including:

- public prerecorded EEG / offline replay / simulated real-time BCI only;
- D-040 through D-042 split/final-test protection;
- D-048 through D-050 calibration policy;
- D-051 through D-057 binary evidence, Bayesian, and shared-autonomy policy;
- D-058 through D-060 adaptation policy;
- D-061 through D-065 planning/risk/safety policy;
- D-067 through D-070 human authority and navigation/replanning contracts;
- D-074 through D-076 M6 replay/decoder runtime boundaries;
- D-077 A/B/C/D matrix;
- D-078 robustness contract;
- D-079 inferential-statistics policy.

No live EEG, physical hardware, physical robot, certified-safety, or real-world efficacy claim is authorized.

A new scientifically meaningful ambiguity must not be decided by Codex. Stop and surface it for Project Owner approval.

---

# 7. REQUIRED TESTING

At minimum, focused tests must verify:

1. exact A/B/C/D and ablation component membership;
2. metric correctness on analytically checkable fixtures, including edge denominators;
3. D-050 reliability/ECE binning and Brier behavior;
4. D-078 R1 endpoints/intermediate values and R2 deterministic index selection/swap behavior;
5. reproducibility under identical seeds and sensitivity where seeds should differ;
6. subject-level aggregation with no pseudo-replication;
7. paired bootstrap CI determinism and correct paired resampling;
8. paired sign-flip/permutation behavior, including exact enumeration on small fixtures;
9. Holm adjustment correctness;
10. result/provenance schema validation and fail-closed malformed inputs;
11. synthetic/development orchestration for both approved decoder-family labels where applicable;
12. safety/planning metric accounting on controlled scenarios;
13. protection against accidental protected-final-test execution/access in M7-T01;
14. regression compatibility with accepted M1–M6 behavior.

Run:

```text
focused M7-T01 tests
relevant evaluation + M5/M6 integration regressions
full pytest suite
python/compiler/static import check as appropriate
git diff --check
```

No reportable final-test result is required or permitted for acceptance.

---

# 8. ACCEPTANCE CRITERIA

M7-T01 may be submitted for review only if:

- all required harness components above are implemented;
- D-077/D-078/D-079 semantics are represented exactly;
- metric denominators/evaluation units are explicit;
- robustness and statistics are deterministic/reproducible;
- no protected final-test result was accessed or produced;
- no scientific policy was invented;
- no production runtime module was modified outside authorization;
- no new dependency was added;
- focused and relevant regression tests pass;
- the full pytest suite passes;
- `git diff --check` passes;
- the working tree is clean at candidate commit;
- the candidate is pushed to `task/m7-t01-experiment-evaluation-harness`;
- GitHub Actions verifies the exact candidate SHA successfully before acceptance.

---

# 9. STOP CONDITIONS

STOP and report BLOCKED if any of the following occurs:

- a new scientific/experimental decision is required;
- final-test access is required to implement or verify the harness;
- a production scientific/runtime defect requires changing read-only M1–M6 modules;
- an approved D-077/D-078/D-079 rule is ambiguous in a way that changes scientific meaning;
- a new dependency appears necessary;
- implementation would require changing split semantics, model fitting, calibration fitting, thresholds, adaptation policy, planning/safety policy, or human-authority semantics;
- tests reveal a pre-existing production defect that cannot be handled strictly within evaluation code.

Do not silently broaden scope.

---

# 10. COMPLETION REPORT REQUIRED FROM CODEX

Return:

```text
status: PASS / BLOCKED
branch
starting SHA
candidate SHA
changed files
implementation summary by subsystem
scientific-policy conformance statement
protected-final-test access statement
new dependencies: yes/no
focused test commands + exact results
relevant regression commands + exact results
full pytest exact result
git diff --check result
working-tree status
GitHub Actions run ID + exact requested/resolved SHA + conclusion
any warnings / known limitations
```

Do not merge. ChatGPT must review the candidate before acceptance/merge.
