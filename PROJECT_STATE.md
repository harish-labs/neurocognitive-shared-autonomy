# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Last updated:** 2026-09-14 (M8-T01 authorization)

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

**M8 — Final Dashboard, Scientific Reporting, Demo & Portfolio Release: ACTIVE / AUTHORIZED**

Current task:

**M8-T01 — Final Dashboard, Scientific Reporting, Demo & Portfolio Release.**

M8-T01 is the only active task. It is presentation/reporting/demo/portfolio work: it may consume but may not alter accepted M1–M7 science. `results/m7/**` is immutable/read-only, and protected E1–E9 experiments must not be rerun.

M7-T02 acceptance / merge record:

- accepted candidate and fast-forward merge SHA: `61af5226e7214f5b858e6e1faec4b042d340bdd8`;
- final executable/reporting software SHA: `a1a696204a8b06263efa8bb57abc610af3f7361e`;
- final execution manifest SHA-256: `f837258312adf17ec1a04079c71c5461838a4aff5096541acd993bb94da24306`;
- accepted v5 result SHA-256: `b5c7cc2efdbbbab53c65d54aa77542a2e69a71c42d5bdc670e2fd8c34af2dd9b`;
- exact-ref GitHub Actions run: `34840393388`, requested/resolved SHA `61af5226e7214f5b858e6e1faec4b042d340bdd8`, `511 passed, 16 warnings`, diff integrity PASS, clean tree PASS, conclusion SUCCESS.

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

D-081 resolves the previously reported M7-T02 episode-construction blocker. It freezes same-subject/same-run/same-intended-class, event-sample-ordered, non-overlapping five-trial blocks; explicit tail exclusions; identical A/B/C/D episode pairing; deterministic E9 ordering; and the protected-data-prefetch interpretation. This is retained as the historical pre-access contract; protected execution has since occurred under the preserved audit trail.

D-082 now resolves the post-QC cohort-size blocker without changing D-035. M7-T02 must complete the fixed 150 µV QC audit for all 109 source subjects, freeze the actual post-QC eligible cohort, then assign every eligible subject using one ascending-sort/seed-42 shuffle and deterministic largest-remainder 70/15/15 allocation. The historical 76/16/17 counts and provisional final-subject list are not forced execution inputs.

D-083 resolves the remaining eligibility ambiguity: cross-subject eligibility requires at least one retained T1 and one retained T2 trial after QC. D-040 within-subject feasibility and D-081 balanced-sequential participation remain separate. Episode availability is assessed only after split freeze and cannot remove, replace, reshuffle, or move a frozen subject.

D-084 resolves the former E7 ablation-semantics blocker. `Full - Bayes` uses a cumulative arithmetic mean over the calibrated D-081 evidence and the approved threshold policy; `Full - uncertainty` consumes all five D-053 Bayesian updates and commits only the final posterior argmax without uncertainty gates. R03 preserves v1-v3 as invalid implementation-contract artifacts and v4 as `INVALID_PROVENANCE_BINDING`. The provenance-correct v5 artifact is the current scientific-review candidate.

Pre-final audit state at the block:

- 109/109 source subjects audited;
- 68 D-083 cross-subject eligible; 41 excluded under fixed QC/source contracts;
- D-082 allocation: 48 train, 10 validation, 10 final test;
- final-test IDs: `89, 16, 34, 29, 84, 57, 31, 93, 21, 76`;
- 261 D-081 episodes; 2,017 retained source trials; 1,305 sequential observations; 712 tail observations;
- D-083 final balanced-sequential IDs: `89, 16, 34, 29, 31, 93, 21, 76` (`n=8`);
- no-replacement exclusions: subject 84 has no valid class episode; subject 57 has a T1 episode only;
- protected outcomes were accessed under the frozen manifests; v1-v3 are preserved as `INVALID_IMPLEMENTATION_CONTRACT`, v4 is preserved as `INVALID_PROVENANCE_BINDING`, and v5 is the current R03 final candidate. No refitting, scientific tuning, or outcome-driven selection occurred.

R03 final provenance state:

- final executable/reporting software SHA: `a1a696204a8b06263efa8bb57abc610af3f7361e`;
- final execution manifest: `results/m7/manifest/m7-final-execution-v6-d084-r03-final.json`, SHA-256 `f837258312adf17ec1a04079c71c5461838a4aff5096541acd993bb94da24306`;
- v5 result: `results/m7/final/m7-final-results-v5.json`, SHA-256 `b5c7cc2efdbbbab53c65d54aa77542a2e69a71c42d5bdc670e2fd8c34af2dd9b`;
- v5 scientific fields are exactly equal to v4 after excluding only `first_protected_outcome_access` provenance;
- E1-E9, the six E7 ablations, 40 R1 cells, 40 R2 cells, D-079 statistics, tables, figures, and failure-taxonomy registry are present;
- M7-T02-R03 v5 was accepted after ChatGPT scientific review, fast-forward merged to `main` at `61af5226e7214f5b858e6e1faec4b042d340bdd8`, and is CLOSED. The documented limitation remains: failure-taxonomy category counts were not aggregated in the v5 result schema.

Frozen manifest file hashes:

- QC/eligibility: `a37dfeed5253533d47c1354b63616ae4ed19d01aec659acdf665bc8aa4f8f8cd`;
- split: `befd67eaa0a14d96c8386447e424e606f829542c73ece86843fd6de252429ae8`;
- episodes: `2c38cd6066422d54a35b5ff5d17da65dad687e163c3763aa690edef8ecafed03`;
- participation: `8de4367ab2d274c28dff38c331c1af22e0a52815be6914f208d3c0225da11286`.

---

# 4. GOVERNANCE RECONCILIATION GATE

The M7-T02 Phase 0 governance reconciliation is complete on the authorized task branch: `MASTER_PROJECT_SPEC.md` is reconciled through D-079, D-080 records the already-approved frozen M7-T02 execution contract, and directly stale M7 planning/status wording is corrected.

This reconciliation was committed before protected final-test outcome access. Its exact commit SHA and the first-access audit are preserved in Git history and `EXPERIMENT_LOG.md`.

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
- D-082 complete-source QC, actual eligible-cohort freeze, and deterministic allocation policy.
- D-083 one-per-class cross-subject eligibility and post-split experiment-specific sequential participation.

---

# 6. PROTECTED FINAL-TEST GATE

M7-T02 may access reportable protected final-test outcomes only after all pre-final gates pass.

Required before first final-test outcome:

- D-035 QC completed and audited for all 109 source subjects;
- D-082 QC/eligibility manifest frozen with actual eligible `N` and all exclusion reasons;
- D-040/D-041/D-042/D-082 split manifest frozen from one sorted-list seed-42 shuffle and largest-remainder 70/15/15 allocation;
- partition disjointness/exhaustiveness, excluded-subject absence, hashes, and provenance verified;
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

# 10. M8-T01 GATE

M7 remains CLOSED. M8-T01 was explicitly authorized by the Project Owner on 2026-09-14 from canonical `main` at `0b279403ed8f5af8cb33b4e7916e512680ecc32e` on branch `task/m8-t01-final-presentation-release`.

M8 must produce the final read-only result presentation layer, Streamlit dashboard, M8 figures, final results/discussion/reporting documents, release README, demo package, and portfolio/resume wording without changing accepted scientific/runtime modules or any byte under `results/m7/**`. M8 remains active until its candidate is reviewed and accepted; Codex must not merge or close it.
