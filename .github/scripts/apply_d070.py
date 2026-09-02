from pathlib import Path

path = Path('DECISIONS.md')
text = path.read_text(encoding='utf-8')
marker = '\n# 3. UNRESOLVED DECISIONS\n'
if '## D-070 — Stepwise Replacement-Snapshot Replanning Contract' in text:
    raise SystemExit('D-070 already present')
if marker not in text:
    raise SystemExit('Unresolved-decisions marker not found')
entry = r'''

## D-070 — Stepwise Replacement-Snapshot Replanning Contract

**Status:** APPROVED

**Date:** 2026-09-02  
**Supplements:** D-065, D-066, D-067, D-069

**Decision:**

```text
M5-T04 extends the accepted NavigationRuntime with a narrow stepwise replacement-snapshot replanning transition. It must not replace, modify, or invoke the accepted M4 ControlledReplanningCoordinator or PlannerSafetyEnvironmentExecutor for runtime movement.

REPLAN OPERATION
- Add one synchronous deterministic operation equivalent to replan_after_environment_change(...).
- Replanning validates authority, event identity, the replacement snapshot, and the source execution state; invokes A* at most once; and creates a new stepwise NavigationSession when successful.
- The replan operation performs ZERO environment.step() calls and ZERO SafetyController.check() calls.
- Movement after a successful replan resumes only through later advance_one_step() calls under D-069.

AUTHORIZED REPLAN TRIGGERS
Exactly two trigger classes are accepted:
1. explicit ENVIRONMENT_CHANGED together with a new validated replacement environment snapshot; or
2. a prior M5 NavigationResult for the source execution with status REPLAN_REQUIRED, a SafetyDecision with requires_replan=True, and a new validated replacement environment snapshot.
A safety replan request without a genuinely changed validated snapshot does not authorize replanning.
Generic SAFETY_REJECTED, STALE_STATE, NO_SAFE_PATH, or other outcomes must not be silently promoted into a replan trigger.

EVENT IDENTITY
- Every supplied environment-change/replan opportunity has a caller-supplied unique non-empty event_id.
- One event_id may cause at most one actual planner invocation.
- Reuse after planner invocation returns explicit ALREADY_CONSUMED/no-op and never replans again.
- Invalid event identity, invalid trigger, invalid replacement snapshot, STOP, PAUSE, active confirmation, or authority mismatch occurs before planner invocation and does not consume the event.
- Once validation reaches the actual planner invocation, the event becomes consumed regardless of whether planning yields READY, NO_SAFE_PATH, or INVALID_GOAL_OR_PLAN.

EXECUTION IDENTITY ACROSS REPLAN
- A replacement plan is a new execution attempt with a caller-supplied unique non-empty new_execution_id.
- The prior source execution_id is closed/consumed permanently and must never be resurrected.
- Keep source_execution_id, event_id, and new_execution_id as distinct auditable identities.
- A closed/consumed execution ID cannot replay movement.

GOAL / INTENT AUTHORITY
- Ordinary environment-change replanning does not require a new EEG, Bayesian, shared-autonomy, or human confirmation decision when the human-approved symbolic goal and authority state are unchanged.
- The event authorizes only fresh HOW/route computation to the same already-approved symbolic goal; it never authorizes a new WHAT/mission goal.
- No goal substitution, planner-preferred alternative, nearest goal, fallback, or hard-coded EEG-to-goal mapping is allowed.

REPLACEMENT SNAPSHOT VALIDATION
The replacement environment must be a distinct SearchRescueEnvironment instance and must preserve:
- the same grid rows/columns;
- the same exact symbolic goal mapping;
- the same current approved symbolic goal and its coordinate;
- replacement config start equal to the current actual agent position;
- replacement state.position equal to the current actual agent position;
- non-terminated state;
- current position not blocked and not prohibited.
Only blocked_cells and/or risk_map may change under this transition, and at least one must genuinely differ from the source environment.
A structurally identical unchanged map supplied as a new object is INVALID_CHANGE.
Goal-registry changes are not environment-change replanning and must fail closed.

HUMAN AUTHORITY BEFORE REPLAN
Check in this order before planner invocation:
STOP > PAUSE > active confirmation > approved-goal consistency > replacement/event validation > planner.
- STOP: no replan; no movement; source navigation remains terminated.
- PAUSE: no planner invocation while paused; preserve current position and approved goal; do not prepare executable movement.
- Active confirmation/HOLD: no replan; zero movement.
- OVERRIDE or any approved-goal change invalidates old-goal replan continuation; movement to the new human-approved goal must use the accepted fresh OVERRIDE navigation-start path.

ENVIRONMENT CHANGE WHILE PAUSED / RESUME
- If an explicit environment change occurs while PAUSED, the old executable navigation remains closed.
- After a valid applied RESUME, the caller may supply that event_id, its validated replacement snapshot, and a new execution_id to perform the D-066 replan to the same approved goal.
- This resume-replan performs zero movement and never replays a pre-PAUSE action or route.
- A plain navigation restart must not be used to bypass a pending changed-while-paused D-066 replacement-snapshot transition when that event/snapshot is the basis for the resumed environment.

SAFETY-REQUESTED REPLAN
- A genuine source NavigationResult.REPLAN_REQUIRED plus a validated changed snapshot may replan directly to the same human-approved symbolic goal without human reconfirmation when authority remains unchanged.
- Safety REPLAN_REQUIRED by itself is not enough; the new validated changed snapshot is mandatory.

FRESH PLAN VALIDATION
The replacement A* result must satisfy the same D-069 plan-integrity rules:
- exact start at current position;
- exact approved-goal coordinate;
- structurally valid path/actions that reconstruct the request;
- no malformed SUCCESS;
- no path that reaches a different configured terminal goal first.
NO_SAFE_PATH means zero movement, hold/closed new attempt, consumed event, and no second replan using the same event.

SUCCESSFUL REPLAN RESULT
- A successful replan returns a READY-style zero-movement result.
- The new NavigationSession captures the replacement-environment signature, new execution_id, same exact symbolic goal, fresh path/actions, expected current position, and next_action_index=0.
- Subsequent movement uses ordinary D-069 advance_one_step() with the exact replacement environment and preserves human-authority and safety checks before each transition.

MULTIPLE ENVIRONMENT CHANGES
- A later genuine environment change requires another unique event_id, another validated replacement snapshot, and another new execution_id.
- Never retry a consumed event, never loop automatically, and never replan repeatedly against an unchanged snapshot.

NO HIDDEN ENVIRONMENT MUTATION
- NavigationRuntime does not mutate an old environment object into the replacement environment and does not invent snapshots.
- The caller supplies the replacement object explicitly.
- After successful replan, subsequent advancement must use that replacement environment; stale/old/different environment state fails closed under the existing signature checks.

SYNCHRONOUS ONLY
- No async worker, event bus, listener, background loop, retry worker, thread, timer, or hidden callback queue is authorized.
- An environment-change event is explicit structured input to one deterministic runtime call.
```

**Context:** D-066 defines immutable event-bounded replacement-snapshot replanning, while D-069 established an interruptible one-step M5 execution runtime. The accepted M4 ControlledReplanningCoordinator delegates to the accepted whole-route executor, so invoking it from M5 would bypass D-069's human-authority interception points and reintroduce complete-route synchronous execution.

**Alternatives considered:** invoking the accepted M4 ControlledReplanningCoordinator from the M5 runtime; reusing the old execution_id after replanning; replanning without a new snapshot after any safety rejection; requiring new EEG/human goal selection for every environmental route change; allowing PAUSE/RESUME to replay a queued pre-change route.

**Rationale:** A separate stepwise replacement transition preserves D-066's explicit environment-change provenance and one-replan-per-event guarantee while preserving D-069's zero-movement planning boundary, one-step execution, execution replay protection, and human-authority interception before every subsequent movement. Distinct command/request/execution/event identities make the resulting control history deterministic and auditable.

**Affected documents/modules:** `DECISIONS.md`, `CURRENT_TASK.md`, `PROJECT_STATE.md`, `src/control/navigation_runtime.py`, `tests/test_navigation_runtime.py`, an optional focused `tests/test_navigation_replanning.py`, and accepted M4/M5 dependencies only as read-only regression targets.

**Implementation consequence:** A separately authorized M5-T04 task may implement only stepwise D-066 replacement-snapshot replanning inside the accepted M5 NavigationRuntime under this contract. It must not modify or invoke the accepted whole-route M4 replanner/executor for movement, must not begin M6 EEG integration, and must not add UI, logging infrastructure, experiments, async processing, dependency maintenance, goal-mapping changes, or scientific threshold changes.

**Approved by:** Project Owner

---
'''
text = text.replace(marker, entry + marker, 1)
path.write_text(text, encoding='utf-8')
