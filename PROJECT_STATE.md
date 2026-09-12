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

Current module:
M6 End-to-End EEG Integration

Current task:
None

Task status:
NO ACTIVE IMPLEMENTATION TASK

M6-T05 accepted candidate:
05abf5eb251ebdc4bc7adafff156b590bca9589d

M6-T05 software merge:
4fd3e26a3c63e74ef9d6ad27d79feacb13b164e4

M6-T05 PR:
#17

M6-T05 verification:
focused M6-T05 tests: 10 passed
relevant regression tests: 124 passed
full pytest: 391 passed, 1 warning
warning: known non-failing PyTorch padding='same' warning
git diff --check: PASS
new dependencies: none
scope deviations: none

The accepted M6-T05 implementation provides a synchronous, caller-driven offline mission orchestration path through prerecorded EEG replay, decoder/calibrator runtime evidence, bounded Bayesian inference, intent/navigation authorization, explicit human command handling, stepwise safety-gated navigation, and explicit D-070 replanning delegation.

The project remains public prerecorded EEG / offline EEG replay / simulated real-time BCI only. No live EEG, physical EEG hardware, physical robot, certified-safety, efficacy, or reportable end-to-end experimental claim is authorized by M6-T05.

M6-T06: NOT STARTED / NOT AUTHORIZED.
M7: NOT STARTED / NOT AUTHORIZED.

# 2. REMAINING UNRESOLVED DECISIONS

U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy

These remain unresolved experimental-analysis decisions and were not modified by M6-T05.

# 3. CURRENT AUTHORITY

There is no active implementation task.

Do not start M6-T06 or M7 without separate Project Owner approval and a new CURRENT_TASK.md authorization.
