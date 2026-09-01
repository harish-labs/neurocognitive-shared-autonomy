# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex.  
**Current status:** ACTIVE / NOT STARTED  
**Current milestone:** M5 — Shared Autonomy + Human Interaction  
**Task ID:** M5-T02  
**Task title:** Shared-Autonomy / Human-Interaction Authorization Bridge  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Approved decision baseline:** D-068 plus all prior accepted decisions  
**Branch rule:** Create the task branch from current `main` only after this authorization and the corresponding `PROJECT_STATE.md` update are both present.  
**Last updated:** 2026-09-01

---

# 1. CLOSED TASK RECORD — M5-T01

```text
Task ID: M5-T01
Task title: Human Command & Confirmation State Layer
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Accepted software commit:
732cf91890e22a1a66bbe918a4b01500af5966f2
```

Accepted verification:

```text
python -m pytest tests/test_human_interaction.py -> 19 passed
python -m pytest tests/test_shared_autonomy.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py tests/test_human_interaction.py -> 77 passed
python -m pytest -> 233 passed, 1 known non-failing PyTorch warning
```

---

# 2. OBJECTIVE

Implement only the deterministic authorization bridge defined by D-068 between:

```text
accepted SharedAutonomyDecision
        ↓
M5-T02 authorization bridge
        ↓
accepted HumanInteractionController state
```

M5-T02 ends at explicit policy-goal adoption, confirmation-request registration, or HOLD/REJECT state.

It performs **no movement** and must not invoke planner, safety, environment execution, or replanning.

---

# 3. READ FIRST

Codex must read, in order:

```text
1. MASTER_PROJECT_SPEC.md
2. AGENTS.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. CURRENT_TASK.md
6. docs/04_SYSTEM_ARCHITECTURE.md
7. docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md
8. docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md
9. docs/14_SAFETY_CRITICAL_CONTROL.md
10. docs/15_IMPLEMENTATION_BLUEPRINT.md
11. docs/16_REPOSITORY_AND_CODE_ARCHITECTURE.md
12. docs/19_TESTING_AND_VERIFICATION.md
13. src/control/shared_autonomy.py
14. src/control/human_interaction.py
15. src/autonomy/environment.py
16. src/autonomy/execution.py
17. src/autonomy/replanning.py
18. relevant accepted tests
```

GitHub `main` is canonical.

---

# 4. GOVERNING DECISIONS

Preserve all approved decisions, especially D-003, D-020, D-021, D-056, D-057, D-064, D-065, D-066, D-067, and D-068. D-068 is authoritative for this task.

---

# 5. ALLOWED FILES

Primary authorized files:

```text
src/control/interaction_bridge.py
tests/test_interaction_bridge.py
```

Authorized only if required by D-068's policy-approved-goal state API:

```text
src/control/human_interaction.py
tests/test_human_interaction.py
```

Only if genuinely required for exports:

```text
src/control/__init__.py
```

Do not modify accepted semantics in `src/control/shared_autonomy.py`, any `src/autonomy/*` accepted module, `src/cognition/*`, `src/models/*`, or `src/eeg/*`. If required, STOP/BLOCKED.

---

# 6. INPUT / GOAL CONTRACT

The bridge consumes an accepted `SharedAutonomyDecision`, the current `HumanInteractionController`, a caller-supplied current symbolic mission-goal registry, and a caller-supplied `request_id` only for a new CONFIRM request.

For PROCEED/CONFIRM goals:

```text
non-empty symbolic identifier
exact match to current goal-registry key
no substring/fuzzy/value matching
no fallback/nearest/planner-preferred goal
no hard-coded Left/Right -> victim mapping
```

Keep the interaction state's approved goal symbolic. Coordinate resolution belongs to a later execution-integration task against the then-current environment snapshot.

---

# 7. OUTPUT CONTRACT

Return an immutable structured bridge result sufficient to audit at least:

```text
status
policy_mode
candidate_goal, if any
approved_goal after handling
active_request_id after handling, if any
holds_position
requests_human_input
policy_goal_adopted: bool
confirmation_opened: bool
reason
```

Recommended semantic statuses: `AUTHORIZED`, `WAITING_FOR_CONFIRMATION`, `HOLD`, `REJECTED`, `INVALID_GOAL`, `INVALID_STATE`. Exact names may differ if explicit/deterministic.

No executed action, path, planner result, safety result, or environment transition is allowed.

---

# 8. PROCEED

Required behavior:

```text
STOPPED -> INVALID_STATE / HOLD
PAUSED -> INVALID_STATE / HOLD
active unresolved confirmation -> do not bypass/replace; HOLD / REJECT
invalid/non-current symbolic goal -> INVALID_GOAL / HOLD
otherwise adopt exact symbolic policy-approved goal into interaction state
no HumanCommand synthesized
no command_id consumed
no planner/safety/environment/replanning call
```

A narrow `HumanInteractionController` non-human-command policy-goal adoption API may be added. It must validate exact goal identity and fail closed under STOPPED/PAUSED/active-confirmation/invalid-goal conditions.

Repeated adoption of the same goal may be state-idempotent but must never create movement or queued execution.

---

# 9. CONFIRM

For a structurally valid CONFIRM decision:

```text
candidate must be exact/current
policy approved_goal must not bypass human confirmation
caller supplies non-empty deterministic request_id
use HumanInteractionController.open_confirmation_request
never replace an active request silently
no goal autonomously approved
holds_position=True
requests_human_input=True
```

CONFIRM request opening is allowed while PAUSED (but not STOPPED) because it causes no movement; PAUSE remains active. Explicit human CONFIRM remains owned by the controller.

---

# 10. WAITING / DEFER

Do not change approved_goal, force argmax, invent a confirmation candidate, or execute movement. DEFER preserves D-057 stationary explicit-human-input behavior.

---

# 11. HUMAN-ACTION / DUPLICATE-PATH RULE

Never convert `SharedAutonomyDecision.human_action` into a new HumanCommand. Human commands remain owned exclusively by `HumanInteractionController.handle_command`.

No synthesized PAUSE/STOP/OVERRIDE/CONFIRM/RESUME. Policy decisions reflecting human actions may produce a HOLD/authority result only. If policy human-action observation conflicts with actual controller authority state, fail closed rather than inventing reconciliation behavior.

---

# 12. STRUCTURAL VALIDATION

Fail closed on materially inconsistent directly-constructed `SharedAutonomyDecision` values, including:

```text
PROCEED without approved goal
PROCEED candidate/approved identity conflict
CONFIRM without requires_human_confirmation=True
CONFIRM without valid candidate
CONFIRM carrying autonomous approved_goal
DEFER attempting a new approved goal
unsupported mode/type
```

Do not recalculate Bayesian/posterior thresholds inside the bridge.

---

# 13. REQUIRED TESTS

Cover at least:

```text
valid PROCEED exact symbolic goal adopted
invalid/substring PROCEED rejected
PROCEED blocked PAUSED/STOPPED/active confirmation
repeated same PROCEED no movement side effect
valid CONFIRM opens exact caller-ID request
invalid CONFIRM candidate/request rejected
CONFIRM while PAUSED opens request but preserves pause
CONFIRM while STOPPED rejected
CONFIRM never autonomously approves
active confirmation never replaced
WAITING/DEFER preserve state and hold
no forced fallback goal
human_action never becomes duplicate HumanCommand
conflicting human-action/controller state fails closed
forged inconsistent decision fails closed
no planner/safety/environment/executor/replanning calls/imports
no EEG/model/adaptation/UI dependency
fresh controllers + identical inputs -> identical result/state
```

Extend `tests/test_human_interaction.py` for any new policy-goal adoption API.

---

# 14. REGRESSION REQUIREMENT

Run at minimum:

```text
python -m pytest tests/test_interaction_bridge.py tests/test_human_interaction.py tests/test_shared_autonomy.py
python -m pytest tests/test_shared_autonomy.py tests/test_human_interaction.py tests/test_interaction_bridge.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py
python -m pytest
```

Report exact results/warnings. The pre-existing `requirements.txt` omission of `pandas` and `scikit-learn` is not authorized for modification here. In a clean verification environment, install them only as test-environment dependencies if necessary and report that explicitly.

---

# 15. OUT OF SCOPE

No planner, safety, environment.step, executor, replanning, symbolic->coordinate execution resolution, EEG/model/calibration changes, Bayesian/shared-autonomy policy changes, adaptation updates, UI, logging/metrics infrastructure, network/API transport, async/background processing, full-system orchestration, experiments/claims, or `requirements.txt` maintenance.

---

# 16. ACCEPTANCE / STOP

PASS only if D-068 is enforced, exact symbolic validation is fail-closed, PROCEED cannot bypass PAUSE/STOP/active confirmation, CONFIRM cannot autonomously approve, WAITING/DEFER create no commitment, human commands are not double-processed, no movement integration is added, and focused/adjacent/full regression tests pass without new policy.

STOP/BLOCKED if D-068 conflicts with accepted M5-T01, accepted `shared_autonomy.py` semantics must change, autonomy execution modules must change, symbolic identity cannot be preserved without a new decision, or another authority decision is required.

After implementation/tests/commit/push: STOP. Do not merge or begin M5-T03/full EEG integration/UI/maintenance/experiments.
