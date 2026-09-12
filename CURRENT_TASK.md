# CURRENT_TASK.md

## Current Codex Implementation Authority

**Current status:** ACTIVE / AUTHORIZED
**Current milestone:** M6 End-to-End EEG Integration
**Task ID:** M6-T06
**Task title:** End-to-End Integration Verification
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical branch:** `task/m6-t06-end-to-end-verification`

---

# 1. AUTHORIZATION

Project Owner explicitly approved completing the final M6 task on 2026-09-12.

M6-T01 through M6-T05 are PASS / ACCEPTED / MERGED / CLOSED. M6-T06 is the sole active task. M7 remains NOT STARTED / NOT AUTHORIZED.

The project remains **public prerecorded EEG / offline EEG replay / simulated real-time BCI only**. No live EEG, physical EEG hardware, physical robot, certified-safety, efficacy, or experimental-performance claim is authorized.

U-034, U-035, and U-036 remain unresolved experimental-analysis decisions and must not be resolved or implemented in M6-T06.

---

# 2. OBJECTIVE

Perform the final M6 integration verification against the accepted implementation now on `main`.

M6-T06 is verification-only. It must prove that the accepted end-to-end offline mission path behaves consistently across the already-approved boundaries:

```text
canonical prerecorded MNE Epochs
-> OfflineEpochReplay
-> decoder runtime inference
-> approved calibration
-> bounded Bayesian replay episode
-> uncertainty/shared-autonomy decision
-> human authorization / hold semantics
-> exact symbolic mission goal
-> zero-movement navigation start
-> caller-driven one-step safety-gated execution
-> explicit D-070 replanning when supplied
-> terminal / hold / no-safe-path / paused / stopped outcomes
```

No scientific, architectural, runtime, planner, safety, human-authority, decoder, calibration, or Bayesian behavior may be redesigned in this task.

---

# 3. READ FIRST

1. `MASTER_PROJECT_SPEC.md`
2. `CURRENT_TASK.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`, especially D-051 through D-057, D-064 through D-071, and D-074 through D-076
5. `AGENTS.md`
6. `docs/15_IMPLEMENTATION_BLUEPRINT.md`, especially M6 exit criteria and Gate H
7. accepted M6-T01 through M6-T05 code/tests
8. accepted M5 navigation/human-authority code/tests
9. `.github/workflows/verify.yml`

---

# 4. ALLOWED IMPLEMENTATION FILES

Exactly:

```text
tests/test_m6_end_to_end.py
```

All accepted production modules are read-only verification targets.

Do not modify production source, configuration, requirements, workflows, documentation, experiment files, or governance files from the task branch.

If verification exposes a production defect requiring a code change, STOP and report BLOCKED with the failing test and root cause. Do not repair it inside M6-T06 without separate Project Owner authorization.

---

# 5. REQUIRED VERIFICATION COVERAGE

The focused M6 end-to-end verification must cover at least:

1. A canonical accepted prerecorded EEG epoch sequence flows through replay -> decoder/calibrator -> Bayesian episode -> M6-T04 authorization -> zero-movement READY navigation for a valid PROCEED case.
2. Replay order/provenance is preserved and exactly one accepted epoch produces one evidence observation.
3. Decoder/calibrator class order remains exactly `("left", "right")` and calibrated evidence remains valid.
4. Bayesian commitment stops evidence consumption immediately and never exceeds five accepted observations.
5. Binary candidate A/B identity is preserved exactly; no direct K-goal EEG interpretation is introduced.
6. CONFIRM remains stationary until explicit valid human confirmation, then creates only a fresh zero-movement navigation start.
7. DEFER/WAITING remains stationary and does not force argmax selection.
8. OVERRIDE changes the exact symbolic goal and requires fresh navigation to that goal.
9. PAUSE blocks movement; RESUME requires fresh authorization and never replays queued movement.
10. STOP prevents further movement for the control session.
11. Each caller `advance_one_step()` causes at most one accepted safety-gated environment transition.
12. Safety rejects invalid/blocked/prohibited transitions without bypass.
13. NO_SAFE_PATH remains stationary with no safety relaxation or goal substitution.
14. Explicit D-070 replacement-snapshot replanning produces a fresh zero-movement plan to the same approved goal, with event/execution replay protection.
15. Duplicate/stale request, command, execution, and event identities fail closed.
16. Malformed replay provenance, invalid decoder/calibrator pairing, invalid candidate identity, stale environment/session state, and unsupported inputs fail closed.
17. No hidden true-goal label is used for runtime intent selection.
18. No whole-route hidden loop, async worker, hidden queue, retry worker, or automatic repeated replanning is introduced.
19. No live EEG/hardware semantics are introduced.
20. The final successful verification is reproducible at an exact Git commit.

---

# 6. REQUIRED RUNS

Run at minimum:

1. focused `tests/test_m6_end_to_end.py`;
2. all M6 tests:
   - `tests/test_eeg_replay.py`
   - `tests/test_runtime_adapter.py`
   - `tests/test_replay_episode.py`
   - `tests/test_intent_navigation_bridge.py`
   - `tests/test_offline_mission.py`
   - `tests/test_m6_end_to_end.py`;
3. relevant M5 interaction/navigation/replanning regressions;
4. full `pytest`;
5. `git diff --check`;
6. confirm task-branch diff from authorization baseline contains only `tests/test_m6_end_to_end.py`;
7. run the accepted exact-ref GitHub Actions `Verify repository ref` workflow against the final candidate SHA and report the resolved SHA, job result, pytest result, diff-check result, and clean-tree result.

The final M6-T06 acceptance requires both local verification (when available) and the exact-ref GitHub Actions verification run. If local execution is unavailable, do not weaken GitHub Actions verification.

---

# 7. ACCEPTANCE CRITERIA

M6-T06 is acceptable only if:

- focused end-to-end integration tests pass;
- accepted M5/M6 regressions pass;
- full pytest passes except already-known non-failing warnings;
- `git diff --check` passes;
- exact-ref GitHub Actions verification succeeds against the final candidate SHA;
- task-branch diff contains only `tests/test_m6_end_to_end.py`;
- no production code change, dependency change, scientific decision, architecture change, UI, experiment, metric, or claim is introduced;
- offline prerecorded EEG / simulated real-time BCI terminology remains accurate;
- U-034/U-035/U-036 remain unresolved;
- M7 remains NOT STARTED / NOT AUTHORIZED.

A passing M6-T06 candidate may then be reviewed by ChatGPT. Only after review, merge, and governance close may M6 be declared PASS / COMPLETE / CLOSED.

---

# 8. STOP CONDITIONS

STOP and report BLOCKED if:

- any production/source/config/dependency/workflow change appears necessary;
- verification reveals inconsistent accepted interfaces;
- an unresolved scientific/architectural decision becomes necessary;
- exact-ref CI cannot verify the candidate;
- any test failure cannot be explained without changing accepted behavior.

Do not start M7.
