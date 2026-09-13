# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub
**Last updated:** 2026-09-13

---

# 1. STATUS AT A GLANCE

Project phase:
M1-T01 through M1-T10 accepted and merged.
M4-T01 through M4-T05 accepted and merged.
M5-T01 through M5-T04 accepted and merged.
PRE-M6-R01 through PRE-M6-R06 accepted and merged.
PRE-M6-R07A: PASS / ACCEPTED / MERGED.
PRE-M6-R07B: PASS / ACCEPTED / MERGED.
Final Pre-M6 audit: PASS / CLOSED.
M6-T01: PASS / ACCEPTED / MERGED / CLOSED.
M6-T02: PASS / ACCEPTED / MERGED / CLOSED.
M6-R01: PASS / ACCEPTED / MERGED / CLOSED.
M6-T03: PASS / ACCEPTED / MERGED / CLOSED.
M6-T04: PASS / ACCEPTED / MERGED / CLOSED.
M6-T05: PASS / ACCEPTED / MERGED / CLOSED.
M6-T06: PASS / ACCEPTED / MERGED / CLOSED.

M6 — End-to-End EEG Integration: COMPLETE / PASS / CLOSED.

M7 planning decisions:
D-077 through D-079 APPROVED.
Former U-034, U-035, and U-036 resolved.

Current milestone:
M7 — Experiments / Ablations / Robustness

Current task:
M7-T01 — Consolidated Experiment & Evaluation Harness

Task status:
ACTIVE / AUTHORIZED

Authorized task branch:
`task/m7-t01-experiment-evaluation-harness`

Pre-authorization canonical main:
`19fadbdfa0cbe3bae57ac3be9be1f2fb8c808d21`

M7-T02 — Frozen Final Experiment Execution & Scientific Audit:
NOT STARTED / NOT AUTHORIZED

M6-T06 accepted candidate:
575c44a50c16b108fdfa712386aeb8a6da4b2bd4

M6-T06 software merge:
a02463619e7b109fc877e515b3c2de34391e966e

M6-T06 exact-ref GitHub Actions verification:
Run 34709434481
requested SHA = resolved SHA = 575c44a50c16b108fdfa712386aeb8a6da4b2bd4
dependency installation: PASS
full pytest: 402 passed, 16 warnings
git diff --check: PASS
working tree: clean
overall: SUCCESS

M6 demonstrates a software-only end-to-end path using public prerecorded EEG / offline replay / simulated real-time BCI. No live EEG, physical EEG hardware, physical robot deployment, certified safety, or real-world efficacy is claimed.

---

# 2. M7 EXPERIMENTAL DECISIONS

D-077 resolves U-034 and freezes the principal A/B/C/D experimental component matrix.

D-078 resolves U-035 and freezes the primary M7 robustness perturbation families and severity levels:
- probability/evidence flattening toward `[0.5, 0.5]` at epsilon 0.00, 0.25, 0.50, 0.75, 1.00;
- deterministic contradictory-evidence swaps at contamination fractions 0.00, 0.10, 0.20, 0.30, 0.40 under a frozen seed/index selection.

D-079 resolves U-036 and freezes the primary subject-level inferential-statistics policy: paired subject-level effects, 95% paired bootstrap confidence intervals, two-sided paired sign-flip/permutation tests, alpha 0.05, and Holm correction within experiment families.

No currently recorded M7-blocking scientific decisions remain unresolved.

---

# 3. M7 IMPLEMENTATION STRUCTURE

The consolidated M7 plan remains:

```text
M7-T01 — Consolidated Experiment & Evaluation Harness
M7-T02 — Frozen Final Experiment Execution & Scientific Audit
```

M7-T01 is now ACTIVE / AUTHORIZED.

M7-T01 scope includes the evaluation condition registry, approved metrics, D-078 robustness transforms, D-079 statistics, result/provenance schema, synthetic/development orchestration, required tests, and reconciliation of stale experiment/metrics documentation with already-approved decisions.

M7-T01 must not access or execute protected final-test outcomes. It must be implemented, tested, reviewed, accepted, and frozen before M7-T02 may be authorized.

M7-T02 remains NOT AUTHORIZED and is the only planned phase permitted to run the frozen protected final experiment matrix after explicit Project Owner approval.

---

# 4. FINAL-TEST PROTECTION

During M7-T01:

```text
protected final-test execution: FORBIDDEN
protected final-test outcome inspection: FORBIDDEN
final-test-driven tuning: FORBIDDEN
reportable final M7 results: NOT AUTHORIZED
```

M7-T01 verification must use synthetic fixtures, leakage-safe development/training/validation inputs or previously accepted non-final-test artifacts, and controlled deterministic planning/safety scenarios.

---

# 5. IMPLEMENTATION DISCIPLINE

M7-T01 is intentionally one large coherent task to reduce governance overhead and accelerate completion.

Do not split M7-T01 into micro-tasks unless implementation discovers a genuine safety, scientific, architectural, dependency, or protected-test boundary that requires separate Project Owner review.

If a new scientifically meaningful ambiguity appears, Codex must stop and report it rather than make the decision independently.

The accepted M1–M6 production runtime is read-only for M7-T01 unless a real defect blocks the harness and separate authorization is granted.

No new dependency is authorized.

---

# 6. NEXT GATE

Codex should implement M7-T01 on `task/m7-t01-experiment-evaluation-harness` exactly under `CURRENT_TASK.md`.

After implementation, testing, exact-ref GitHub Actions verification, and candidate push, ChatGPT must review the actual diff/code/tests/results before the task can be accepted or merged.

M7-T02 must not begin before that review and a separate explicit Project Owner authorization.
