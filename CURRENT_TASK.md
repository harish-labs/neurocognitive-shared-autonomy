# CURRENT_TASK.md

## Current Codex Implementation Authority

**Current status:** ACTIVE / AUTHORIZED — PRE-FINAL EXECUTION
**Current milestone:** M7 — Experiments / Ablations / Robustness  
**Task ID:** M7-T02  
**Task title:** Frozen Final Experiment Execution & Scientific Audit  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Canonical branch:** `main`  
**Authorized task branch:** `task/m7-t02-final-experiments-scientific-audit`  
**Accepted M7-T01 candidate / M7-T02 software base:** `1e60d8a0e3344e3706f9a08892b8695b7536c309`

---

# 1. OWNER AUTHORIZATION

On 2026-09-13 the Project Owner explicitly approved all of the following as one consolidated transition:

1. accept and merge M7-T01;
2. reconcile `MASTER_PROJECT_SPEC.md` through approved decisions D-077, D-078, and D-079;
3. freeze the recommended M7-T02 final deterministic SAR scenario suite;
4. freeze the deterministic simulated-human policy described below;
5. proceed to M7-T02 as a large high-effort task rather than splitting it into unnecessary micro-tasks.

M7-T01 candidate `1e60d8a0e3344e3706f9a08892b8695b7536c309` was scientifically reviewed by ChatGPT and accepted for merge after the R2 population-level remediation. Exact-ref GitHub Actions run `34746224355` checked out that SHA and reported `440 passed, 16 warnings`, successful diff integrity, and a clean tree.

M7-T02 is therefore AUTHORIZED subject to the mandatory governance and leakage gates in this ticket.

On 2026-09-13 the Project Owner additionally approved D-081, resolving the fixed-intent real-EEG episode-construction blocker and approving the disclosed protected-data prefetch interpretation. M7-T02 remains ACTIVE / AUTHORIZED. E1–E9 have not yet been executed, and no protected final outcome has yet been accessed.

On 2026-09-13 the Project Owner additionally approved D-082. The accepted D-035 preprocessing/QC boundary now determines the actual eligible cohort from all 109 source subjects. The cross-subject split must be frozen from that cohort using one ascending-sort/seed-42 shuffle and the D-082 largest-remainder 70/15/15 allocation. The historical D-042 `76/16/17` counts and provisional subject membership must not be forced when post-QC `N` differs from 109.

On 2026-09-13 the Project Owner additionally approved D-083. Cross-subject eligibility is exactly retained T1 `>=1` and retained T2 `>=1` after fixed D-035 QC. It does not require D-040 within-subject feasibility or a D-081 episode. After the D-082 split is frozen, balanced sequential families include only subjects with at least one valid five-observation T1 episode and at least one valid five-observation T2 episode; nonparticipation never changes frozen membership and must be reported per experiment.

---

# 2. PURPOSE

Execute the frozen M7 experiment program and produce reproducible, auditable scientific results for E1–E9 without changing the already-approved scientific policy after protected outcomes are visible.

This is the reportable experiment phase. It may access the protected final-test cohort only after all pre-final gates below pass and the final execution manifest is frozen.

Negative, mixed, non-significant, or unexpected results are valid and must be preserved.

## 2.1 D-084 pre-final ablation semantics

D-084 resolves the prior E7 execution-semantics blocker. `Full - Bayes` uses the approved calibrated five-observation arithmetic running mean with the D-055/D-057 thresholds; `Full - uncertainty` performs all five D-053 Bayesian updates, records uncertainty descriptively, and commits the final posterior argmax without uncertainty gates. The complete D-084 text in `DECISIONS.md` is authoritative. The pre-final artifact, test, and final-manifest gates remain mandatory before protected outcomes are accessed.

Valid pre-final work completed before the stop:

- all 109 source subjects audited; D-083 cross-subject eligible `N=68`, excluded `41`;
- D-082 split frozen at `48 train / 10 validation / 10 final_test` with no replacement;
- D-081 manifest frozen with `261` episodes from `2,017` retained source trials (`1,305` sequential observations and `712` tails);
- D-083 final sequential participation frozen at `8` included subjects; subject 84 has no valid five-trial class episode and subject 57 has a T1 episode only;
- protected outcome access remains `false`; no decoder/calibrator artifact was fit and E1–E9 were not executed.

---

# 3. MANDATORY PHASE 0 — GOVERNANCE RECONCILIATION BEFORE FINAL-TEST ACCESS

Before reading, running, summarizing, or otherwise exposing any protected final-test outcome, Codex must reconcile the repository governance exactly as already approved by the Project Owner.

Required governance edits:

- reconcile `MASTER_PROJECT_SPEC.md` through D-079;
- remove stale statements that U-034/U-035/U-036 remain unresolved;
- state that D-077 resolves U-034, D-078 resolves U-035, and D-079 resolves U-036;
- preserve all unrelated Master authority unchanged;
- add the approved M7-T02 execution decision(s) to `DECISIONS.md` without inventing additional policy;
- update `PROJECT_STATE.md` to close M7-T01 as PASS / ACCEPTED / MERGED / CLOSED and mark M7-T02 ACTIVE / AUTHORIZED;
- reconcile stale M7 status text in governance/backlog files only where needed to avoid contradictions.

The governance reconciliation must be committed on the authorized M7-T02 branch before any protected final-test outcome is accessed.

This is reconciliation of already-approved owner decisions, not permission to make new scientific decisions.

---

# 4. FROZEN M7-T02 EXECUTION CONTRACT

## 4.1 Principal experimental policy

Preserve D-077 exactly:

- A — Direct EEG;
- B — Confidence-Aware;
- C — Bayesian Shared Autonomy;
- D — Full System;
- evaluate both approved decoder families where valid: CSP+LDA and EEGNet/approved compact EEG CNN;
- common planner/risk/hard-safety/human emergency authority remain fixed across A–D except in the explicit safety ablation;
- adaptation is enabled only in D and the explicit adaptation comparison;
- do not redefine component membership after results are visible.

Preserve D-078 exactly:

- R1 epsilon: `0.00, 0.25, 0.50, 0.75, 1.00`;
- R2 q: `0.00, 0.10, 0.20, 0.30, 0.40`;
- R2 selection occurs once over the complete ordered condition/evaluation-run evidence population, never independently per short episode;
- perturb after the condition's approved identity/model-specific calibration stage and before direct decision/confidence gating/Bayesian update;
- labels and evaluation-only intended-goal metadata are never perturbed.

Preserve D-079 exactly:

- subject is the primary inferential unit for real EEG / subject-generalization comparisons;
- two-sided alpha `0.05`;
- paired raw subject-level effect;
- 95% paired bootstrap CI with 10,000 resamples and a fixed recorded seed;
- paired sign-flip/permutation test;
- exact `2^n_final` sign enumeration for the actual complete paired final-subject vector when practical (`2^17 = 131072` remains the historical full-109 example);
- Holm correction within each experiment family;
- no pseudo-replication using trials, observations, actions, maps, or neural seeds as subjects.

## 4.2 Frozen operational/random seeds

Use `42` for M7-T02 operational randomness unless an already-approved upstream artifact has its own frozen training/selection seed that must be preserved. In particular:

- bootstrap seed: `42`;
- R2 population-selection seed: `42` for the primary robustness matrix;
- environment reset / deterministic orchestration seed where a seed field is required: `42`.

Do not create extra neural-network repeat runs merely to increase inferential sample size. Existing approved model-seed policy and already-frozen model artifacts take precedence. Neural seeds are descriptive/reproducibility metadata, never independent subjects.

## 4.3 Frozen controlled SAR scenario suite for E5 / safety validation

Use these deterministic fixtures, derived from already-accepted planner/safety/replanning contracts. Coordinate convention is `(row, column)`.

### S1 — Basic free-space route

- grid: `3 x 4`
- start: `(1,0)`
- approved goal: `(0,3)`
- blocked cells: none
- risk map: all FREE

### S2 — Static obstacle route

- grid: `3 x 4`
- start: `(1,0)`
- approved goal: `(0,3)`
- blocked cells: `{(1,1)}`
- risk map: all FREE

### S3 — Short risky vs longer safer route

- grid: `3 x 5`
- start: `(1,0)`
- approved goal: `(1,4)`
- blocked cells: none
- HIGH-risk cells: `(1,1)`, `(1,2)`, `(1,3)` at `0.75`
- all other cells FREE
- D-063 lambda remains `2.0`

### S4 — No-safe-path case

- grid: `3 x 3`
- start: `(1,0)`
- approved goal: `(1,2)`
- blocked cells: `{(0,1), (1,1), (2,1)}`
- risk map: all FREE
- expected contract: explicit NO_SAFE_PATH / stationary behavior, not goal substitution.

### S5 — Dynamic blockage / controlled replanning

Initial snapshot:

- grid: `3 x 5`
- start: `(1,0)`
- approved goal: `(1,4)`
- blocked cells: none
- risk map: all FREE

Replacement snapshot for the frozen environment-change event:

- same grid and same approved goal;
- replacement start equals the current valid agent position;
- add blocked cell `(1,1)`;
- event ID is stable and consumed once;
- replan under D-066/D-070 without changing the approved goal.

### S6 — Prohibited-hazard safety rejection

- grid: `3 x 4`
- current/start: `(1,1)`
- approved goal: `(0,3)`
- prohibited cell: `(1,2)` with risk `1.00`
- frozen proposed action for the safety probe: RIGHT
- expected contract: PROHIBITED_HAZARD / REPLAN_REQUIRED; the prohibited move must not execute.

### S7 — Emergency stop

- grid: `3 x 4`
- current/start: `(1,1)`
- approved goal: `(0,3)`
- otherwise free map
- issue STOP / emergency-stop authority before the next movement proposal is executed
- expected contract: halted and zero movement after stop.

These seven scenarios are deterministic validation scenarios. Do not fabricate stochastic significance testing over them. Report them descriptively/exhaustively under D-079.

## 4.4 Frozen full-system mission map

For E3/E4/E6/E7/E9 end-to-end mission orchestration, use the already-accepted M6 two-goal environment unless an experiment explicitly uses one of S1–S7 above:

- grid: `3 x 5`;
- start: `(1,0)`;
- `victim_a = (1,4)`;
- `victim_b = (0,2)`;
- no blocked cells and all FREE in the primary baseline mission map.

Candidate order is stable as `(victim_a, victim_b)` when this map is used. Do not reinterpret Left/Right class semantics or hidden true-goal metadata.

## 4.5 Deterministic simulated-human policy

M7-T02 remains a software-only offline-replay experiment. No real human-subject data are introduced.

The simulated operator is deterministic and exists only to exercise the already-approved human-authority interface reproducibly:

- `PROCEED`: no simulated-human command is injected.
- `CONFIRM`: if the controller's proposed candidate equals the episode's evaluation-only intended goal, submit the accepted explicit CONFIRM command for that request. If the proposed candidate is not the intended goal, submit an explicit OVERRIDE/correction to the intended goal rather than approving the wrong proposal.
- `DEFER`: submit an explicit OVERRIDE/correction selecting the evaluation-only intended goal, thereby representing a human response to the request for input. Do not force an autonomous argmax.
- `PAUSE` and `STOP`: inject only in their dedicated controlled experiments/scenarios, not randomly in the primary A/B/C/D comparison.
- adaptation may update only from the resulting legitimate explicit applied human-feedback event through the already-accepted D-058–D-060 interfaces;
- hidden true-goal metadata may be read by the simulator only to generate the explicit human command and to score evaluation outcomes; it must never be passed directly into decoder fitting, calibration fitting, Bayes, planner likelihood, or adaptation state.

This simulated-human contract must be logged distinctly as simulated/offline and must not be described as a real human study.

## 4.6 D-081 fixed-intent episode construction

For E3/E4/E6/E7/E9, construct sequential episodes within one `(subject_id, run_id, intended_class)` group. Order by `event_sample` with canonical trial index or stable canonical identity as tie-breaker, then form non-overlapping consecutive blocks of exactly five source trials. Never mix subjects, runs, or intended classes; never overlap, reuse, pad, duplicate, or create shorter tail episodes. Record excluded tails and retain those single trials for valid E1/E2 use.

A/B/C/D share the identical frozen episode basis. A and B use source observation 1; C and D receive observations 1–5 in the same order and may stop early only under the accepted decision policy. Evaluation labels are authorized only for episode construction, simulated-human command selection, and scoring, and remain forbidden from decoder/calibration/Bayesian inference, planning, safety, and direct adaptation state.

For E9, order completed episodes within each subject/candidate-pair stream by `run_id`, first source `event_sample`, and stable episode identity. R1/R2 reuse the frozen episode identities; R2 selection remains population-level and does not restart at episode boundaries.

The resulting episodes are deterministic offline repeated-trial constructions for a fixed intended choice, not natural continuous EEG sessions or live/online BCI evidence accumulation.

The disclosed retrieval/cache creation for final-subject public EDF files is protected-data prefetch rather than protected-outcome access under D-081. Preserve that audit entry. First protected-outcome access remains forbidden until every split, episode, artifact, test, and execution-manifest gate passes.

---

# 5. PRE-FINAL LEAKAGE / ARTIFACT FREEZE GATE

Before first protected final-test evaluation:

1. complete D-035 QC for all 109 source subjects and freeze the D-082 QC/eligibility manifest with counts, exclusions, reasons, policy IDs, code SHA, and run/data provenance;
2. derive actual post-QC eligible count `N`, sort eligible IDs ascending, perform one deterministic seed-42 shuffle, allocate every eligible subject under the D-082 largest-remainder 70/15/15 rule, and freeze the versioned D-040/D-041/D-042/D-082 split manifest;
3. verify split hashes/provenance, disjointness, exhaustive eligible-cohort coverage, exclusion of every ineligible subject, and absence of any post-freeze subject replacement;
4. inventory all model/calibrator/checkpoint artifacts required for CSP+LDA and EEGNet;
5. verify each artifact was fit/selected using only approved training/validation partitions;
6. if an artifact must be produced because no accepted persisted artifact exists, fit/select/freeze it using training/validation only, record its exact configuration/hash/provenance, and freeze it before final-test access;
7. freeze the complete M7-T02 execution manifest before inspecting final-test outcomes;
8. record software Git SHA, split-manifest identity, model/checkpoint identity, calibrator identity, decoder family, condition/ablation, scenario ID, seeds, and scientific-policy IDs.

Cross-subject eligibility at steps 1–2 is governed by D-083: retained T1 `>=1` and retained T2 `>=1`. Track D-040 within-subject feasibility separately. Only after the split is frozen, derive D-081 per-subject T1/T2 episode counts and experiment-specific balanced-sequential inclusion manifests; never remove or replace a frozen subject due to episode availability.

No final-test result may influence model selection, calibration, threshold choice, artifact choice, scenario choice, perturbation levels, metric definitions, or report inclusion.

---

# 6. REQUIRED REPORTABLE EXPERIMENT FAMILIES

Execute the approved experiment program as far as repository data/artifacts permit without violating the stop conditions.

## E1 — EEG decoding

Evaluate CSP+LDA and EEGNet separately.

Report within-subject and cross-subject tracks separately where implemented/valid, including:

- accuracy;
- balanced accuracy;
- per-class precision/recall/F1;
- macro F1;
- confusion matrix;
- subject-wise values for cross-subject evaluation.

Do not choose a winner post hoc to hide the other decoder.

## E2 — Probability calibration

For each decoder family compare its frozen raw/identity probability output against the approved calibrated output.

Report:

- 10 equal-width reliability bins;
- ECE;
- Brier Score;
- reliability diagrams/plot-ready data;
- subject-wise values where appropriate.

Calibration fitting must remain validation-only under D-048–D-050.

## E3 — Direct/single-evidence vs sequential Bayesian inference

Compare the approved direct evidence baseline against D-053/D-054 sequential Bayesian accumulation.

Report:

- goal/commitment correctness;
- primary wrong-goal rate = wrong commitments / all evaluated decision episodes;
- secondary conditional wrong-goal rate = wrong commitments / committed episodes;
- accepted evidence count;
- posterior confidence;
- entropy;
- decision mode and latency.

## E4 — Uncertainty-aware shared autonomy

Evaluate the effect of the approved confidence/uncertainty behavior without changing thresholds after outcomes are visible.

Report:

- wrong-goal commitment;
- PROCEED / CONFIRM / DEFER counts and rates;
- human interventions under the frozen simulated-human policy;
- accepted evidence count / decision latency;
- correctness after explicit simulated-human confirmation/correction.

## E5 — Planning / safety

Run frozen S1–S7.

Report descriptively/exhaustively:

- planning success/status;
- path length;
- D-062 cumulative risk;
- movement cost / weighted risk contribution / total path cost where available;
- replanning count;
- unsafe action attempts;
- executed hard-safety violations;
- NO_SAFE_PATH/unreachable;
- emergency-stop success;
- deterministic trace/provenance.

Include explicit Safety ON vs Safety OFF simulation ablation where authorized by D-077/E7, while retaining basic software validity protections. Safety OFF may expose simulated prohibited-action execution for comparison but must never corrupt software state or bypass emergency STOP authority.

## E6 — Principal A/B/C/D comparison

Run A/B/C/D for both decoder families where valid.

Primary outputs:

- task success;
- primary wrong-goal commitment rate;
- conditional wrong-goal rate;
- decision latency in accepted EEG observations;
- navigation/environment steps separately;
- confirmation/override/deferral counts;
- task/navigation outcome;
- cumulative risk;
- unsafe attempts;
- executed hard-safety violations;
- no-safe-path/replan events.

No composite overall score.

## E7 — Ablations and robustness

Ablations:

- Full;
- Full - calibration;
- Full - Bayes;
- Full - uncertainty;
- Full - safety;
- Full - adaptation.

Each ablation must change only its named component relative to Full.

Robustness:

- A/B/C/D × both decoder families where valid × all R1 severities;
- A/B/C/D × both decoder families where valid × all R2 severities;
- R2 uses the accepted population-level selection contract and primary seed 42.

Preserve original and perturbed evidence/provenance.

## E8 — Cross-subject held-out-subject evaluation

Preserve one value per protected final subject for primary inferential comparisons. Report individual-subject distributions and macro descriptive summaries.

Do not pool trials across subjects for inference.

## E9 — Adaptation

Evaluate adaptation OFF vs ON using ordered episodes and only explicit simulated-human feedback under the frozen policy.

Report:

- pre/post or episode-indexed task/commitment behavior;
- confirmation/deferral rates;
- decision latency;
- prior evolution;
- explicit-feedback provenance;
- adaptation bounds and warm-up behavior.

Never update adaptation using hidden evaluation truth directly.

---

# 7. STATISTICAL ANALYSIS

For real-EEG / subject-level paired system comparisons permitted by D-079:

- aggregate to exactly one metric value per subject per compared condition before inference;
- raw paired effect is condition B minus condition A, with direction clearly labeled for every comparison;
- 95% paired bootstrap CI;
- exactly 10,000 bootstrap resamples;
- bootstrap seed 42;
- two-sided paired sign-flip test;
- for a complete paired final-subject vector, use exact `2^n_final` sign assignments whenever practical and record the actual `n_final` and enumeration count;
- Holm-adjust raw p-values within the same experiment family;
- preserve raw and adjusted p-values;
- report n subjects;
- do not equate statistical significance with practical importance.

Do not apply artificial subject-level significance testing to deterministic S1–S7 planner/safety scenarios.

---

# 8. FAILURE ANALYSIS / VALIDITY AUDIT

Create a machine-readable failure taxonomy and preserve concrete failures rather than hiding them.

At minimum distinguish:

- decoder misclassification;
- poorly calibrated confidence;
- Bayesian evidence accumulation failure / misleading evidence;
- CONFIRM event;
- DEFER event;
- wrong autonomous commitment;
- simulated-human correction/override;
- no-safe-path;
- safety rejection;
- replanning event;
- prohibited-hazard attempt;
- emergency stop;
- adaptation-helped / adaptation-hurt descriptive cases where supported;
- robustness-induced degradation;
- missing/invalid artifact or provenance failure.

Audit limitations and claims. Never claim live EEG, real human-subject efficacy, physical robot performance, real rescue deployment, medical benefit, or certified safety.

---

# 9. RESULT / ARTIFACT REQUIREMENTS

Use compact repository-safe artifacts only. Do not commit public EEG raw data, large downloaded datasets, environment caches, or unnecessary large model binaries.

Preferred result layout, unless an already-established repository result convention conflicts:

```text
results/m7/
  manifest/
  e1_decoding/
  e2_calibration/
  e3_bayesian/
  e4_shared_autonomy/
  e5_planning_safety/
  e6_abcd/
  e7_ablation_robustness/
  e8_cross_subject/
  e9_adaptation/
  statistics/
  failures/
  figures/
  tables/
```

Machine-readable JSON/CSV should be primary. Figures must be reproducible from stored machine-readable results.

Record in `EXPERIMENT_LOG.md` only experiments actually executed. Do not pre-fill results.

If large model artifacts cannot be committed, record their exact local/path identity where available, cryptographic hash, generating configuration, split provenance, and software SHA without fabricating portability.

---

# 10. AUTHORIZED FILE / IMPLEMENTATION BOUNDARY

M7-T02 may modify/add only what is required for final experiment execution, result persistence, analysis, and the explicitly approved governance reconciliation, including:

- `MASTER_PROJECT_SPEC.md` — reconciliation through D-079 only;
- `DECISIONS.md` — record the already-approved M7-T02 execution contract;
- `PROJECT_STATE.md`;
- `CURRENT_TASK.md` only for accurate task status/close information;
- `RESEARCH_LOG.md` only if needed to reconcile resolved M7 decisions, not to invent findings;
- `TODO.md` only for stale-status reconciliation;
- `EXPERIMENT_LOG.md` — actual experiment records/results only;
- `docs/17_EXPERIMENTAL_DESIGN.md`;
- `docs/18_METRICS_AND_EVALUATION.md`;
- `src/evaluation/**`;
- `tests/test_evaluation_*.py`;
- `tests/test_m7_*.py`;
- a minimal headless M7 experiment runner/CLI under `scripts/**` or `src/evaluation/**`;
- compact `results/m7/**` machine-readable outputs, tables, and reproducible figures.

Accepted production modules remain READ-ONLY unless a genuine defect prevents executing the frozen experiment contract:

- `src/eeg/**`;
- `src/models/**`;
- `src/cognitive/**`;
- `src/control/**`;
- `src/autonomy/**`;
- `config.yaml` / `src/config.py` scientific policy;
- split manifests;
- model training semantics;
- thresholds;
- calibration-fitting semantics;
- planner/risk/safety semantics;
- human-authority semantics.

If a production/runtime defect requires changing those modules, STOP and return for review rather than silently changing the system after final-evaluation authorization.

No new dependency is authorized unless a genuinely unavoidable blocker is reported and separately approved.

---

# 11. FINAL-TEST ACCESS RULES

Protected final-test access is permitted in M7-T02 only after Phase 0 governance reconciliation and the pre-final artifact/manifest freeze gate pass.

Once any protected final-test outcome has been observed:

- do not refit/select/tune models;
- do not alter calibration;
- do not alter thresholds;
- do not alter A/B/C/D definitions;
- do not alter robustness severity levels or R2 selection policy;
- do not alter scenario maps to improve results;
- do not change metric definitions/denominators;
- do not add/drop subjects based on performance;
- do not choose a different model/checkpoint based on final outcomes;
- do not add new experiments merely because the first result is unfavorable unless separately labeled exploratory and separately authorized.

If an execution bug invalidates a final run, preserve the invalid run/provenance, fix only if the fix is within authorized evaluation code and does not alter scientific semantics, rerun with an explicit invalidation/rerun audit trail, and never delete the original record.

---

# 12. REQUIRED TESTING / VERIFICATION

Before reportable execution, run focused tests covering:

- final-manifest validation and final-test gate;
- exact scenario definitions S1–S7;
- simulated-human CONFIRM/correction/DEFER behavior;
- adaptation feedback isolation;
- A/B/C/D frozen semantics;
- ablation one-component-only differences;
- R1/R2 provenance and population-level R2 selection;
- result schema and deterministic serialization;
- subject aggregation / no pseudo-replication;
- bootstrap / exact sign-flip / Holm;
- no final-test-driven fitting hooks.

After implementation and reportable execution, run:

- focused M7 tests;
- relevant M5/M6 integration regressions;
- complete pytest suite;
- compiler/import check;
- `git diff --check`;
- clean working tree check;
- exact-ref GitHub Actions for the final candidate SHA.

The experiment runner must be headless and deterministic given the frozen manifest/artifacts.

---

# 13. STOP CONDITIONS

STOP and report BLOCKED before further protected evaluation if any of the following occurs:

1. complete 109-source-subject QC or the D-082 eligibility/split manifests cannot be produced and verified under accepted eligibility semantics;
2. the split manifest cannot be verified exactly;
3. a required model/calibrator artifact cannot be proven train/validation-only and leakage-safe;
4. a new scientific/evaluation decision is required;
5. a production M1–M6 code defect requires changing a READ-ONLY production module;
6. a new dependency is genuinely required;
7. final-test results would be needed to choose a model, threshold, scenario, metric, perturbation, ablation, or artifact;
8. the deterministic simulated-human policy cannot be represented through the accepted human-interaction API without changing its semantics;
9. final-result provenance cannot be made auditable;
10. the task would require claiming real human, live EEG, physical robot, or certified safety evidence.

Do not improvise around a stop condition.

---

# 14. COMPLETION / CANDIDATE REQUIREMENTS

Return one consolidated M7-T02 candidate only after the authorized work has been completed as far as validly possible.

Required completion report:

```text
status: PASS / BLOCKED / PARTIAL
branch
starting SHA
governance reconciliation commit SHA
final execution-manifest identity/hash
candidate SHA
changed files
M7-T01 governance-close confirmation
MASTER_PROJECT_SPEC reconciliation confirmation
recorded M7-T02 decision IDs
split-manifest identity and verified cohort counts
model/checkpoint/calibrator artifact identities and hashes
protected-final-test first-access point / audit statement
E1–E9 execution status individually
actual numerical results summary without selective omission
negative/mixed/non-significant results explicitly listed
R1/R2 execution summary
S1–S7 planning/safety summary
A/B/C/D results for both decoder families where valid
ablation results
adaptation results
subject-level n and statistical outputs
Holm families and adjusted p-values
failure taxonomy summary
result artifact paths
figure/table paths
focused test commands/results
M5/M6 regression commands/results
full pytest result
import/compiler result
git diff --check
working-tree status
GitHub Actions run ID
requested/resolved candidate SHA
Actions conclusion
warnings/limitations
confirmation that no final-test-driven tuning occurred
confirmation that no live EEG / real-human / physical-robot claim was made
```

Do not merge the M7-T02 candidate. ChatGPT must review the actual GitHub diff, result artifacts, provenance, statistics, and exact-ref CI before M7 can be accepted/closed.
