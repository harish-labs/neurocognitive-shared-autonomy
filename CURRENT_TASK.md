# CURRENT_TASK.md

## Current Codex Implementation Authority

**Current status:** ACTIVE / AUTHORIZED
**Current milestone:** M6 End-to-End EEG Integration
**Task ID:** M6-T05
**Task title:** End-to-End Offline Mission Orchestrator
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical branch:** `task/m6-t05-offline-mission-orchestrator`

---

# 1. AUTHORIZATION

Project Owner explicitly approved starting M6-T05 on 2026-09-09.

M6-T01 through M6-T04 are PASS / ACCEPTED / MERGED / CLOSED. M6-T05 is the sole active implementation task. M6-T06 and M7 remain NOT STARTED / NOT AUTHORIZED.

The project remains **public prerecorded EEG / offline EEG replay / simulated real-time BCI only**. No live EEG or hardware claim is authorized.

U-034, U-035, and U-036 remain unresolved and must not be resolved or implemented in M6-T05.

---

# 2. OBJECTIVE

Create one narrow, synchronous, caller-driven orchestration layer that composes the already accepted M6/M5 runtime boundaries into a reproducible simulated rescue episode without redesigning any scientific, human-authority, planning, or safety policy.

Approved composition:

```text
canonical accepted MNE Epochs
-> OfflineEpochReplay
-> decode_replay_observation() using already-instantiated/already-fitted decoder + calibrator
-> run_bayesian_replay_episode()
-> authorize_episode_navigation()
-> existing HumanInteractionController / explicit human commands when supplied
-> NavigationRuntime.start_navigation()
-> caller-driven NavigationRuntime.advance_one_step()
-> existing D-070 replanning path only when the caller explicitly supplies an approved event + replacement snapshot
-> terminal / hold / no-safe-path / confirmation / deferred / paused / stopped / replan-required outcome
```

This task composes accepted modules. It does not create new scientific behavior.

---

# 3. READ FIRST

1. `MASTER_PROJECT_SPEC.md`
2. `CURRENT_TASK.md`
3. `PROJECT_STATE.md`
4. `DECISIONS.md`, especially D-003, D-008, D-051 through D-057, D-064 through D-071, D-074 through D-076
5. `AGENTS.md`
6. `docs/15_IMPLEMENTATION_BLUEPRINT.md`, especially M6 and Gate H
7. accepted runtime modules used by this task

---

# 4. ALLOWED IMPLEMENTATION FILES

Exactly:

```text
src/control/offline_mission.py
tests/test_offline_mission.py
```

Existing accepted modules are read-only regression dependencies. If a required change to an accepted module appears necessary, STOP and report the blocker before editing it.

No dependency-manifest change is authorized.

---

# 5. REQUIRED BEHAVIOR

## 5.1 Replay / decoder / calibration

- Input must use canonical accepted `mne.Epochs` as the authoritative source.
- Instantiate/use `OfflineEpochReplay` for deterministic prerecorded replay.
- Decode replay observations lazily/in replay order through `decode_replay_observation()`.
- Receive already-instantiated, already-fitted decoder and calibrator objects; do not load, deserialize, train, fit, refit, tune, select, or persist them.
- Preserve exact replay identity, provenance, class order, and D-074 one-epoch -> one-evidence semantics.
- Do not consume extra replay observations after the Bayesian episode becomes terminal.

## 5.2 Bayesian / uncertainty / authorization

- Pass decoded evidence to the accepted `run_bayesian_replay_episode()` boundary with exactly two externally supplied current candidate goals A/B.
- Do not reimplement Bayesian update mathematics, thresholds, evidence mapping, or entropy.
- Route the accepted replay-episode result through the accepted M6-T04 `authorize_episode_navigation()` boundary.
- Preserve exact symbolic goal identity; never substitute nearest/planner-preferred/fallback goals.
- CONFIRM/DEFER/WAITING must remain non-moving outcomes until explicit accepted human authority permits otherwise.

## 5.3 Human authority

- Human commands remain explicit caller-supplied `HumanCommand` inputs handled exactly once by the accepted `HumanInteractionController`.
- Do not synthesize CONFIRM, OVERRIDE, PAUSE, RESUME, or STOP.
- Preserve D-067 precedence and duplicate/stale protections.
- A valid applied CONFIRM/OVERRIDE/RESUME may be used only as the existing fresh navigation authorization source accepted by `NavigationRuntime`.
- STOP is terminal for the current control session; PAUSE blocks movement; OVERRIDE changes WHAT and requires a fresh navigation start.

## 5.4 Navigation / safety / replanning

- The orchestrator must remain **stepwise and caller-driven**.
- It must not hide or execute an entire route in one uninterruptible loop.
- Each movement operation may delegate to at most one accepted `NavigationRuntime.advance_one_step()` call.
- Every actual movement therefore remains safety-gated by the accepted runtime before `environment.step()`.
- Initial navigation start remains zero movement.
- NO_SAFE_PATH remains stationary and must not relax safety or switch goals.
- Replanning is allowed only by delegating to the existing D-070 `NavigationRuntime.replan_after_environment_change()` contract with caller-supplied event identity, replacement snapshot, trigger, and fresh execution identity.
- Do not invent environment changes, retry loops, hidden map mutation, new event semantics, or automatic repeated replanning.

## 5.5 Mission state / outputs

- Expose immutable/auditable orchestration results or session state sufficient to trace the accepted stage outcomes for the current mission attempt.
- At minimum preserve the current replay/Bayesian/authorization/navigation outcome needed to understand why the mission is READY, MOVED/ACTIVE, GOAL_REACHED, HOLD/CONFIRM/DEFER, NO_SAFE_PATH, PAUSED, STOPPED, REPLAN_REQUIRED, SAFETY_REJECTED, or invalid.
- Do not implement experiment logging infrastructure or reportable metrics in this task.
- Do not fabricate success or efficacy results.

---

# 6. FORBIDDEN SCOPE

Do not:

- modify EEG preprocessing, epoch semantics, split policy, decoder architecture, decoder fitting, calibration methodology, Bayesian rules, uncertainty thresholds, adaptation policy, planner cost, safety policy, or human-authority semantics;
- introduce direct K-goal EEG decoding;
- use hidden true-goal labels for runtime intent selection;
- load/persist decoder or calibrator artifacts;
- add async workers, threads, callbacks that create hidden command/event queues, timers, retry workers, or background processing;
- auto-run a whole navigation route without caller interception between steps;
- implement dashboard/UI;
- implement experiment logging/metrics;
- run or claim M7 experiments;
- resolve U-034/U-035/U-036;
- start M6-T06 or M7.

---

# 7. TEST REQUIREMENTS

Focused tests must cover at least:

1. canonical prerecorded epoch(s) can flow through replay -> decoder/calibrator -> Bayesian -> T04 authorization to a zero-movement READY plan for a valid PROCEED case;
2. Bayesian replay stops consuming decoder observations immediately on commitment and never exceeds the approved five-observation horizon;
3. CONFIRM opens/uses the existing confirmation path and performs zero movement until explicit accepted CONFIRM;
4. DEFER/WAITING remain stationary;
5. explicit applied CONFIRM can create a fresh zero-movement navigation start;
6. explicit OVERRIDE changes the approved symbolic goal and requires a fresh plan to exactly that goal;
7. PAUSE prevents movement; valid RESUME requires fresh authorization and never replays a queued action;
8. STOP blocks all further movement in the current session;
9. one caller-driven advance causes at most one environment step and remains safety-gated;
10. NO_SAFE_PATH holds position without goal substitution or safety relaxation;
11. REPLAN_REQUIRED does not cause automatic retry; an explicit valid D-070 replacement-snapshot event may create a fresh zero-movement replacement plan;
12. duplicate/stale command/request/execution/event identities fail closed according to accepted modules;
13. malformed dependencies/provenance/goal identity fail closed;
14. no live EEG, artifact loading/fitting, hidden ground-truth intent input, whole-route execution loop, or new dependencies are introduced.

Run:

- focused `tests/test_offline_mission.py`;
- relevant M6-T01/T02/T03/T04 regressions;
- relevant M5 human interaction/navigation/replanning regressions;
- full pytest;
- `git diff --check`.

If local runtime verification is unavailable, use the accepted exact-ref GitHub Actions verification workflow rather than weakening the acceptance criteria.

---

# 8. ACCEPTANCE CRITERIA

M6-T05 is acceptable only if:

- the full prerecorded EEG-derived evidence path reaches the accepted mission-control/navigation boundary using only accepted modules;
- movement remains stepwise, interruptible, and safety-gated;
- human authority remains externally explicit and correctly prioritized;
- exact symbolic goal identity is preserved end to end;
- no extra EEG evidence is consumed after terminal Bayesian decision;
- zero-movement authorization/start semantics are preserved;
- no-safe-path and replan-required states fail closed;
- focused + regression + full tests pass;
- no new dependency or scientific/architectural policy is introduced;
- only the two authorized implementation files differ from the authorization baseline.

M6-T05 must be reviewed by ChatGPT before merge.

---

# 9. STOP CONDITIONS

STOP and report BLOCKED if:

- an accepted module must be modified;
- a new scientific/architectural decision is required;
- decoder/calibrator persistence/loading becomes necessary;
- a required human-command timing/queue semantics would need to be invented;
- a required environment-change/retry behavior is outside D-070;
- the task cannot preserve stepwise caller interception;
- tests expose an inconsistency between accepted interfaces.

Do not proceed to M6-T06.
