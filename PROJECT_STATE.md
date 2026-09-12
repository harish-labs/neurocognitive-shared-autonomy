# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub
**Last updated:** 2026-09-12

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
M6-T06: ACTIVE / AUTHORIZED.

Current module:
M6 End-to-End EEG Integration

Current task:
M6-T06 — End-to-End Integration Verification

Task status:
ACTIVE / AUTHORIZED

Task branch:
`task/m6-t06-end-to-end-verification`

Starting canonical main:
`9ec64e08ccaa64517d25eefe3bd95fbc15bdec4e`

M6-T06 authority:
Project Owner explicitly approved completing the final M6 task on 2026-09-12. `CURRENT_TASK.md` is the exact verification authority.

Approved T06 boundary:
- verification-only final M6 integration gate;
- production code/config/dependency/workflow files are read-only;
- only `tests/test_m6_end_to_end.py` may be added/modified on the task branch;
- verify the accepted offline prerecorded EEG replay -> decoder/calibration -> Bayesian -> shared autonomy/human authorization -> exact symbolic goal -> zero-movement navigation -> caller-driven safety-gated execution/replanning path;
- focused tests + M5/M6 regressions + full pytest + git diff check + exact-ref GitHub Actions verification are required;
- any production defect requiring source changes is a blocker and requires separate authorization.

The project remains public prerecorded EEG / offline EEG replay / simulated real-time BCI only. No live EEG, physical EEG hardware, physical robot, certified-safety, efficacy, or reportable experimental-performance claim is authorized.

M7: NOT STARTED / NOT AUTHORIZED.

# 2. M6-T05 CLOSED RECORD

M6-T05 status: PASS / ACCEPTED / MERGED / CLOSED
Accepted candidate SHA: `05abf5eb251ebdc4bc7adafff156b590bca9589d`
Software merge SHA: `4fd3e26a3c63e74ef9d6ad27d79feacb13b164e4`
PR: #17
Verification: focused 10 passed; relevant regressions 124 passed; full pytest 391 passed, 1 known PyTorch warning; git diff --check PASS; no new dependencies; no scope deviations.

# 3. REMAINING UNRESOLVED DECISIONS

U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy

These remain unresolved experimental-analysis decisions and are not M6-T06 verification blockers. They must not be resolved or implemented inside M6-T06.

# 4. AUTHORITY

`CURRENT_TASK.md` is the sole active Codex authority.

Do not start M7 until M6-T06 is implemented as verification-only, run, reviewed, accepted, merged, and governance-closed, and M6 is formally declared complete.
