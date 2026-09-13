# CURRENT_TASK.md

## Current Codex Implementation Authority

**Current status:** NO ACTIVE IMPLEMENTATION TASK
**Current milestone:** M7 — Experiments / Ablations / Robustness
**Task ID:** None
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical branch:** main

---

# 1. CLOSED MILESTONE — M6

M6 — End-to-End EEG Integration: COMPLETE / PASS / CLOSED.

M6-T06 status: PASS / ACCEPTED / MERGED / CLOSED
Accepted candidate SHA: 575c44a50c16b108fdfa712386aeb8a6da4b2bd4
Software merge SHA: a02463619e7b109fc877e515b3c2de34391e966e
Governance-close SHA: da1fb56c7a51bf89117c1b7ae74abceb4b6dd411
Exact-ref GitHub Actions run: 34709434481
Verification: requested and resolved SHA matched; dependency installation PASS; full pytest 402 passed, 16 warnings; git diff --check PASS; working tree clean; overall SUCCESS.

M6 demonstrates a software-only end-to-end path using public prerecorded EEG / offline replay / simulated real-time BCI. It does not claim live EEG, physical EEG hardware, physical robot deployment, certified safety, or real-world efficacy.

---

# 2. M7 PLANNING STATUS

M7 planning decisions D-077 through D-079 are approved and resolve the former U-034, U-035, and U-036 blockers.

The approved planning direction is:

```text
M7-T01 — Consolidated Experiment & Evaluation Harness
M7-T02 — Frozen Final Experiment Execution & Scientific Audit
```

This two-phase structure is planning only. It minimizes governance overhead while preserving the scientific dependency that the experiment harness must be frozen before protected final-test execution.

---

# 3. CURRENT AUTHORITY

There is no active implementation task.

M7 implementation is NOT AUTHORIZED.

Do not create an M7 implementation branch, modify production/evaluation code, run reportable M7 experiments, or access protected final-test outcomes under M7 until the Project Owner separately authorizes an implementation ticket.

The next candidate implementation task is M7-T01, but it remains PLANNED / NOT AUTHORIZED.

---

# 4. IMPLEMENTATION GATE

Before any M7 implementation begins, a separately approved `CURRENT_TASK.md` must define the exact M7-T01 scope, allowed files, tests, acceptance criteria, final-test protection, and stop conditions.

D-077 through D-079 authorize scientific methodology only. They do not themselves authorize coding or experiment execution.
