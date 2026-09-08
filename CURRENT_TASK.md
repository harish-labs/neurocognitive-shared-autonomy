# CURRENT_TASK.md

## Current Codex Implementation Authority

**Current status:** ACTIVE IMPLEMENTATION TASK
**Current milestone:** M6 — End-to-End EEG Integration
**Task ID:** M6-T04
**Task title:** Intent Authorization -> Navigation Bridge
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical task branch:** `task/m6-t04-intent-navigation-bridge`
**Authorization base:** `afae16fac406d32a106af341171b6dc64520b04d`

---

# 1. ACTIVE TASK — M6-T04

```text
Task ID: M6-T04
Task title: Intent Authorization -> Navigation Bridge
Status: AUTHORIZED / IMPLEMENTATION NOT STARTED
```

M6-T04 is the sole active implementation task.

## Objective

Compose the accepted M6-T03 Bayesian replay-episode result with the already-accepted uncertainty, shared-autonomy, human-interaction authorization, and navigation-start interfaces.

The bridge may establish a fresh navigation plan only when the accepted authorization path permits it. `NavigationRuntime.start_navigation()` remains the terminal execution boundary for this task and must perform zero movement.

Approved composition boundary:

```text
BayesianReplayEpisodeResult
  -> exact BayesianEpisodeResult snapshot
  -> estimate_binary_uncertainty()
  -> decide_shared_autonomy()
  -> authorize_shared_autonomy_decision()
  -> NavigationRuntime.start_navigation() only when AUTHORIZED
```

The bridge must not recompute EEG evidence, alter Bayesian posterior mathematics, change thresholds, bypass human authority, or directly move the environment.

## Inputs

- accepted `BayesianReplayEpisodeResult` from M6-T03
- `HumanInteractionController`
- current symbolic goal registry / accepted `SearchRescueEnvironment`
- accepted `NavigationRuntime`
- caller-supplied confirmation request ID when required
- caller-supplied fresh execution ID when navigation start is permitted

## Authorized implementation files

```text
src/control/intent_navigation_bridge.py
tests/test_intent_navigation_bridge.py
```

Do not modify accepted M1/M4/M5/M6-T01/T02/T03 modules unless a separate reviewer-approved remediation is required.

## Required behavior

1. Accept only the exact M6-T03 result type and fail closed on malformed/inconsistent state.
2. Preserve candidate ordering, posterior, update count, terminal status, and committed candidate exactly; do not rerun Bayesian evidence accumulation.
3. Construct the accepted `BayesianEpisodeResult` snapshot only as a structural handoff to the existing uncertainty/shared-autonomy APIs.
4. Compute uncertainty only through the accepted `estimate_binary_uncertainty()` implementation.
5. Apply the existing `decide_shared_autonomy()` policy without changing thresholds or semantics.
6. Route the resulting decision through `authorize_shared_autonomy_decision()` using the current symbolic goal registry.
7. `PROCEED` may start navigation only after the interaction bridge returns `AUTHORIZED` and the controller state still permits fresh execution.
8. `CONFIRM` must open/retain the existing M5 confirmation path and must not start navigation before explicit human confirmation.
9. `WAITING`, `DEFER`, invalid authorization, invalid goal, PAUSE, STOP, or conflicting human-interaction state must cause zero movement and no navigation start.
10. A successful navigation start may create only a zero-movement `READY` plan through `NavigationRuntime.start_navigation()`.
11. Do not call `advance_one_step()` or any replanning API in M6-T04.
12. Exact symbolic goal identity must be preserved from candidate mapping through controller authorization to the environment goal registry.
13. Caller identifiers must remain explicit; do not generate hidden/random request IDs or execution IDs.
14. Preserve fail-closed behavior and immutable/auditable returned records.

## Explicitly out of scope

```text
EEG replay iteration
decoder or calibrator invocation
Bayesian evidence accumulation
new uncertainty metrics or thresholds
new shared-autonomy policy
new human-command semantics
automatic CONFIRM handling
OVERRIDE/RESUME orchestration
navigation step execution
replanning
full mission loop / orchestrator
logging infrastructure
experiments / metrics / result claims
adaptation changes
multiclass or direct K-goal EEG
live EEG / hardware
M6-T05
M6-T06
M7
```

## Required tests

At minimum verify:

```text
COMMITTED/PROCEED -> exact policy authorization -> READY navigation plan with moved=False
navigation start uses the exact symbolic committed goal
PENDING/WAITING -> HOLD with no navigation start
horizon intermediate-confidence result -> CONFIRM request path with no navigation start
horizon low-confidence result -> DEFER/HOLD with no navigation start
missing/invalid request ID for CONFIRM fails closed
invalid/malformed M6-T03 result fails closed
invalid/current-goal mismatch fails closed
PAUSE blocks autonomous navigation start
STOP blocks autonomous navigation start
active confirmation cannot be bypassed
duplicate/reused execution ID remains rejected by accepted navigation runtime
no call to advance_one_step or replanning
no environment movement occurs within M6-T04
```

Run focused tests plus relevant M6-T03, shared-autonomy, human-interaction/bridge, navigation-runtime regressions and the full pytest suite. Use the repository verification workflow if local Python execution remains unavailable.

## Acceptance criteria

- only authorized implementation/test files change;
- all required tests pass;
- exact M6-T03 posterior/candidate semantics preserved;
- accepted M5 authority and M4 safety/navigation boundaries are reused, not reimplemented;
- successful T04 output can establish a fresh zero-movement navigation plan but cannot move the agent;
- no scientific/architectural policy changes;
- no new dependencies;
- no reportable result claims.

## Stop conditions

Stop and report if implementation requires:

- a new scientific, architectural, or human-authority decision;
- changes to accepted thresholds or Bayesian semantics;
- changes to existing accepted M5 navigation/interaction contracts;
- dependency changes;
- M6-T05/M6-T06/M7 work;
- resolution of U-034/U-035/U-036.

Preserve:

```text
offline prerecorded EEG / simulated real-time BCI only
human determines WHAT; AI determines HOW
STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > shared-autonomy policy
fresh authorization before navigation
safety veto before every environment transition
U-034 unresolved
U-035 unresolved
U-036 unresolved
M6-T05 NOT STARTED / NOT AUTHORIZED
M6-T06 NOT STARTED / NOT AUTHORIZED
```
