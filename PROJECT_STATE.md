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

M7 planning:
D-077 through D-079 APPROVED.
Former U-034, U-035, and U-036 resolved.
M7 implementation remains NOT STARTED / NOT AUTHORIZED.

Current task:
None

Task status:
NO ACTIVE IMPLEMENTATION TASK

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

Production-code changes in this M7 planning step: none
New dependencies in this M7 planning step: none
Experiment execution in this M7 planning step: none

---

# 2. M7 EXPERIMENTAL DECISIONS

D-077 resolves U-034 and freezes the principal A/B/C/D experimental component matrix.

D-078 resolves U-035 and freezes the primary M7 robustness perturbation families and severity levels:
- probability/evidence flattening toward `[0.5, 0.5]` at epsilon 0.00, 0.25, 0.50, 0.75, 1.00;
- deterministic contradictory-evidence swaps at contamination fractions 0.00, 0.10, 0.20, 0.30, 0.40 under a frozen seed/index selection.

D-079 resolves U-036 and freezes the primary subject-level inferential-statistics policy: paired subject-level effects, 95% paired bootstrap confidence intervals, two-sided paired sign-flip/permutation tests, alpha 0.05, and Holm correction within experiment families.

The principal M7 implementation plan is intentionally consolidated:

```text
M7-T01 — Consolidated Experiment & Evaluation Harness
M7-T02 — Frozen Final Experiment Execution & Scientific Audit
```

M7-T01 must be frozen and accepted before M7-T02 may execute protected final-test evaluation.

---

# 3. REMAINING UNRESOLVED DECISIONS

None currently recorded as M7-blocking unresolved scientific decisions.

Any new scientifically meaningful ambiguity discovered during M7 planning or implementation must be surfaced for Project Owner approval rather than invented in code.

---

# 4. CURRENT AUTHORITY

No M7 implementation task is active.

The next candidate task is M7-T01, but it is PLANNED / NOT AUTHORIZED.

Do not begin M7 code changes or reportable experiment execution until a separate Project Owner authorization updates `CURRENT_TASK.md` with the exact implementation ticket.
