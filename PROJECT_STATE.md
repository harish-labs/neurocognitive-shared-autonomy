# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Last updated:** 2026-09-13

---

# 1. STATUS AT A GLANCE

Completed / accepted core work:

- M1-T01 through M1-T10: accepted and merged.
- M4-T01 through M4-T05: accepted and merged.
- M5-T01 through M5-T04: accepted and merged.
- PRE-M6-R01 through PRE-M6-R07B: accepted and merged.
- Final Pre-M6 audit: PASS / CLOSED.
- M6-T01 through M6-T06, including M6-R01: PASS / ACCEPTED / MERGED / CLOSED.
- M6 — End-to-End EEG Integration: COMPLETE / PASS / CLOSED.
- M7 planning decisions D-077 through D-079: APPROVED.
- M7-T01 — Consolidated Experiment & Evaluation Harness: PASS / ACCEPTED / MERGED / CLOSED.

M7-T01 accepted candidate:

`1e60d8a0e3344e3706f9a08892b8695b7536c309`

M7-T01 exact-ref verification:

- GitHub Actions run: `34746224355`
- requested SHA: `1e60d8a0e3344e3706f9a08892b8695b7536c309`
- resolved SHA: `1e60d8a0e3344e3706f9a08892b8695b7536c309`
- result: `440 passed, 16 warnings`
- diff integrity: PASS
- clean tree: PASS
- conclusion: SUCCESS

Current milestone:

**M7 — Experiments / Ablations / Robustness**

Current task:

**M7-T02 — Frozen Final Experiment Execution & Scientific Audit**

Task status:

**ACTIVE / AUTHORIZED**

Authorized task branch:

`task/m7-t02-final-experiments-scientific-audit`

---

# 2. M7-T01 REVIEW CLOSE

ChatGPT reviewed the first M7-T01 candidate `fd37a3c14ecb78c42bc6afba9a7d65c53f1c4ec9` and identified a scientifically meaningful R2 orchestration defect: contradictory-evidence contamination was initially rounded independently inside short episodes, which could make nonzero q levels ineffective for A/B and collapse severities for C/D.

Codex remediated the defect in amended candidate `1e60d8a0e3344e3706f9a08892b8695b7536c309` by selecting R2 contamination once across the complete ordered condition/evaluation-run evidence population, preserving stable global observation identities and auditable provenance.

The amended candidate passed focused tests, regressions, full pytest, import/compiler checks, diff checks, and exact-ref GitHub Actions. No protected final-test outcomes were accessed and M7-T02 was not started during M7-T01.

M7-T01 is therefore accepted and closed.

---

# 3. M7-T02 OWNER APPROVAL

On 2026-09-13 the Project Owner explicitly approved:

- M7-T01 acceptance and merge;
- `MASTER_PROJECT_SPEC.md` reconciliation through D-079;
- the recommended deterministic M7-T02 S1–S7 final SAR scenario suite;
- the deterministic simulated-human policy;
- continuing with a large consolidated M7 task instead of unnecessary micro-tasks.

`CURRENT_TASK.md` contains the exact M7-T02 execution contract and is the current implementation authority.

D-081 now resolves the previously reported M7-T02 episode-construction blocker. It freezes same-subject/same-run/same-intended-class, event-sample-ordered, non-overlapping five-trial blocks; explicit tail exclusions; identical A/B/C/D episode pairing; deterministic E9 ordering; and the protected-data-prefetch interpretation. M7-T02 remains ACTIVE / AUTHORIZED. E1–E9 remain unexecuted and protected final outcomes remain unaccessed at this decision point.

---

# 4. GOVERNANCE RECONCILIATION GATE

The M7-T02 Phase 0 governance reconciliation is complete on the authorized task branch: `MASTER_PROJECT_SPEC.md` is reconciled through D-079, D-080 records the already-approved frozen M7-T02 execution contract, and directly stale M7 planning/status wording is corrected.

This reconciliation must be committed before any protected final-test outcome is accessed. Its exact commit SHA is preserved in Git history and the M7-T02 completion report. Protected final-test access remains forbidden until that commit exists.

---

# 5. FROZEN M7-T02 EXECUTION STATE

The following are frozen for the reportable M7 phase:

- D-077 A/B/C/D component matrix;
- D-078 R1/R2 robustness contract including population-level R2 selection;
- D-079 subject-level inference/statistics policy;
- deterministic S1–S7 controlled SAR scenario suite specified in `CURRENT_TASK.md`;
- accepted M6 two-goal mission map for primary full-system orchestration;
- deterministic simulated-human CONFIRM/correction/DEFER policy specified in `CURRENT_TASK.md`;
- primary operational/bootstrap/R2 seed 42 unless an accepted upstream artifact carries its own frozen seed;
- no extra neural-network seeds may be treated as independent human subjects;
- no composite overall score.
- D-081 fixed-intent episode construction and A/B/C/D source-episode pairing;
- D-081 deterministic E9 ordering and explicit incomplete-tail provenance;
- the disclosed final-subject EDF retrieval is recorded as protected-data prefetch, not outcome access.

---

# 6. PROTECTED FINAL-TEST GATE

M7-T02 may access reportable protected final-test outcomes only after all pre-final gates pass.

Required before first final-test outcome:

- exact D-040–D-042 split manifest verified;
- full approved 109-subject eligible cohort verified;
- 76 train / 16 validation / 17 protected final-test subject split verified;
- if eligible cohort != 109 or final cohort != 17, STOP for Project Owner review;
- decoder/checkpoint/calibrator artifacts proven train/validation-only and leakage-safe;
- final execution manifest frozen with artifact hashes/provenance;
- M7-T02 governance reconciliation committed.

Once protected outcomes are visible, no model/checkpoint/calibrator/threshold/scenario/metric/perturbation/ablation selection may be changed in response to them.

---

# 7. M7-T02 REQUIRED EXPERIMENT PROGRAM

The authorized large task covers the complete frozen M7 program as far as scientifically valid and technically available:

- E1 — EEG decoding;
- E2 — calibration;
- E3 — direct vs sequential Bayesian inference;
- E4 — uncertainty/shared autonomy;
- E5 — planning/safety using frozen S1–S7;
- E6 — principal A/B/C/D comparison for both decoder families where valid;
- E7 — component ablations plus R1/R2 robustness;
- E8 — cross-subject held-out-subject evaluation;
- E9 — adaptation OFF/ON with explicit simulated-human feedback only;
- D-079 paired subject-level statistics / Holm correction;
- failure taxonomy;
- reproducible tables/figures and machine-readable results;
- scientific validity / claim audit.

Negative, mixed, non-significant, and unexpected outcomes must be preserved.

---

# 8. READ-ONLY PRODUCTION BOUNDARY

Accepted M1–M6 production scientific/runtime modules remain read-only during M7-T02 unless a genuine defect blocks the frozen experiment contract and separate authorization is obtained.

In particular, protected results must not trigger changes to:

- EEG preprocessing/splits;
- model fitting/selection rules;
- calibration fitting;
- Bayesian mathematics;
- thresholds;
- adaptation policy;
- planner/risk/safety policy;
- human-authority semantics.

A required production change is a STOP condition.

---

# 9. CLAIM BOUNDARY

The system remains a software-only research prototype using public prerecorded EEG and offline replay / simulated real-time BCI.

M7-T02 does not authorize claims of:

- live EEG acquisition;
- real human-subject efficacy;
- physical robot performance;
- real Search & Rescue deployment;
- medical/clinical efficacy;
- certified safety.

---

# 10. NEXT GATE

Codex should execute M7-T02 on:

`task/m7-t02-final-experiments-scientific-audit`

under the exact `CURRENT_TASK.md` authority.

Codex must not merge the final candidate. After implementation, experiment execution, result persistence, testing, and exact-ref GitHub Actions, ChatGPT must review the actual code, provenance, results, statistics, figures/tables, and CI before M7 is accepted/closed.
