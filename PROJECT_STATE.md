# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub
**Last updated:** 2026-09-09

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
M6-T05: ACTIVE / AUTHORIZED.

Current module:
M6 End-to-End EEG Integration

Current task:
M6-T05 — End-to-End Offline Mission Orchestrator

Task status:
ACTIVE / AUTHORIZED

Task branch:
`task/m6-t05-offline-mission-orchestrator`

M6-T05 authority:
Project Owner explicitly approved starting M6-T05 on 2026-09-09. `CURRENT_TASK.md` is the exact implementation authority.

Approved T05 implementation boundary:
- compose accepted prerecorded EEG replay, decoder/calibrator runtime adapter, Bayesian replay episode, M6-T04 intent-navigation authorization, HumanInteractionController, and NavigationRuntime;
- already-instantiated/already-fitted decoder and calibrator only;
- caller-driven synchronous orchestration;
- zero-movement navigation start;
- at most one safety-gated environment step per caller movement operation;
- explicit human commands only, no synthesized commands;
- existing D-070 replanning only with explicit caller-supplied event/replacement snapshot;
- exact symbolic goal identity preserved;
- no hidden whole-route execution loop;
- no new scientific policy, dependencies, logging infrastructure, UI, or experiments.

Authorized implementation files:
`src/control/offline_mission.py`
`tests/test_offline_mission.py`

The project remains offline prerecorded EEG / simulated real-time BCI only. No live EEG, hardware, certified-safety, efficacy, or reportable end-to-end experimental claim is authorized by M6-T05.

M6-T06: NOT STARTED / NOT AUTHORIZED.
M7: NOT STARTED / NOT AUTHORIZED.

# 2. RECENT CLOSED TASK — M6-T04

M6-T04 status: PASS / ACCEPTED / MERGED / CLOSED
Accepted candidate SHA: db5ab59ebf2dfa03ec937f5dc8cdc2b85cc875e2
Software merge SHA: 8f02af114e6ffb143a834bdc66d8721dea69c64c
Verification: focused 8 passed; relevant regressions 94 passed; full pytest 381 passed, 1 known PyTorch warning; git diff --check PASS; no new dependencies; no scope deviations.

# 3. REMAINING UNRESOLVED DECISIONS

U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy

These remain unresolved and are not M6-T05 implementation blockers. They must not be resolved or implemented inside M6-T05.

# 4. AUTHORITY

`CURRENT_TASK.md` is the sole active Codex implementation authority. Do not start M6-T06 or M7 until M6-T05 is implemented, run, tested, reviewed, accepted, merged, and governance-closed.
