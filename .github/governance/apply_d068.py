from __future__ import annotations

import sys
from pathlib import Path

DECISION_ENTRY = r'''## D-068 — Shared-Autonomy to Human-Interaction Authorization Contract

**Status:** APPROVED

**Date:** 2026-09-01  
**Supplements:** D-003, D-020, D-021, D-056, D-057, D-067

**Decision:**

```text
M5-T02 is an authorization-only integration boundary. It connects accepted SharedAutonomyDecision outputs to the accepted HumanInteractionController and produces explicit deterministic authorization/hold state. It does not execute movement, invoke the planner, call safety, step the environment, or perform replanning.

Goal identity remains symbolic at this boundary. A shared-autonomy candidate/approved goal must exactly match a currently valid configured mission-goal identifier, represented by a key in EnvironmentConfig.goals or an equivalent caller-supplied current goal registry. Do not use substring matching, fallback goals, nearest goals, planner-preferred goals, or a hard-coded Left/Right-to-victim mapping.

PROCEED:
- A structurally valid PROCEED decision with an exact currently valid symbolic goal may be adopted as the interaction state's policy-approved goal only when the interaction controller is not PAUSED and not STOPPED and no unresolved confirmation request would be bypassed.
- M5-T02 performs no movement and creates no direct planner/safety/environment call.
- Missing, invalid, stale, or non-current goal identity fails closed and holds.

CONFIRM:
- A structurally valid CONFIRM decision with an exact currently valid candidate may open one explicit ConfirmationRequest using a deterministic caller-supplied request_id.
- No autonomous goal approval occurs while confirmation is required.
- Existing active-confirmation identity and uniqueness rules from D-067/M5-T01 remain authoritative; M5-T02 may not replace or bypass an unresolved active request.
- Human CONFIRM remains the only action that approves the candidate attached to that active request.

WAITING / DEFER:
- Do not change the approved goal.
- Do not invent a confirmation candidate or force an argmax goal.
- Hold under D-057 and request human input where the accepted shared-autonomy decision requires it.

HUMAN AUTHORITY:
- STOPPED interaction state blocks policy goal adoption and confirmation opening.
- PAUSE blocks autonomous PROCEED goal adoption; no policy result may cause movement while paused.
- An already-active confirmation may remain preserved during PAUSE under D-067, and explicit human CONFIRM/OVERRIDE behavior remains owned by HumanInteractionController.
- OVERRIDE remains the human-selected approved goal and is never generated or reinterpreted by the policy bridge.
- RESUME remains an explicit human command; M5-T02 does not synthesize it or replay queued movement.

ONE HUMAN COMMAND / ONE PROCESSING PATH:
- Human commands are consumed exactly once by HumanInteractionController.
- M5-T02 must never synthesize a duplicate PAUSE, STOP, OVERRIDE, CONFIRM, or RESUME command from SharedAutonomyDecision.human_action.
- The same human action must not be processed once through shared_autonomy.py and again as a newly invented HumanCommand.
- Shared-autonomy PAUSE/STOP/OVERRIDE outputs may be observed for consistency, but the bridge must not convert them into a second human-command side effect.

POLICY-APPROVED GOAL API:
- HumanInteractionController may gain one narrow non-human-command API for adopting an accepted policy-approved symbolic goal.
- The API must validate exact current goal identity and fail closed when STOPPED, PAUSED, an unresolved confirmation would be bypassed, or the goal is not currently valid.
- This API is not a human command, consumes no command_id, creates no execution, and must not weaken D-067.

BINARY EEG / MULTI-GOAL BOUNDARY:
- M5-T02 consumes an already-produced symbolic SharedAutonomyDecision.
- It does not decide how binary EEG maps onto multiple mission goals, does not hard-code the older candidate-only interface conventions, and does not introduce multiclass EEG.

EXECUTION BOUNDARY:
- M5-T02 ends at deterministic goal authorization / confirmation / hold state.
- A later separately reviewed M5 task must connect an approved symbolic goal to the current environment's exact goal coordinate and implement interruptible planner -> safety -> environment execution while preserving PAUSE/STOP/OVERRIDE and D-066 replanning authority.
```

**Context:** M5-T01 implemented deterministic human command/confirmation state, while the accepted shared-autonomy policy still emits symbolic goal decisions and the accepted executor consumes an already-approved SAR coordinate. A narrow authorization bridge is required before any full execution integration so Codex does not invent goal-resolution, human-command duplication, or movement semantics.

**Alternatives considered:** directly combining policy, human commands, planning, safety, and movement in one large integration task; hard-coding binary EEG choices to fixed victim coordinates; converting shared-autonomy human_action fields into duplicate HumanCommand events; allowing PROCEED to bypass PAUSE or an active confirmation.

**Rationale:** Separating authorization from movement keeps human WHAT authority explicit, preserves D-067 command identity and precedence, avoids premature coupling to the synchronous route executor, and leaves interruptible execution for a separately reviewable task.

**Affected documents/modules:** `DECISIONS.md`, `CURRENT_TASK.md`, `PROJECT_STATE.md`, `src/control/shared_autonomy.py`, `src/control/human_interaction.py`, future `src/control/interaction_bridge.py`, and corresponding tests.

**Implementation consequence:** A separately authorized M5-T02 task may implement only the shared-autonomy-to-human-interaction authorization bridge under this contract. D-068 does not authorize planner/safety/environment execution, EEG/model integration, adaptation updates, UI, logging/metrics infrastructure, or experiments.

**Approved by:** Project Owner

---

'''

CURRENT_TASK = r'''# CURRENT_TASK.md

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
'''

PROJECT_STATE = r'''# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Last updated:** 2026-09-01

---

# 1. STATUS AT A GLANCE

```text
Project phase:
M1-T01 through M1-T10 accepted and merged.
M4-T01 through M4-T05 accepted and merged.
M5-T01 Human Command & Confirmation State Layer accepted and merged.
D-068 Shared-Autonomy to Human-Interaction Authorization Contract approved.
M5-T02 Shared-Autonomy / Human-Interaction Authorization Bridge authorized and not yet implemented.

Current module:
Shared-autonomy / human-interaction authorization integration

Current task:
M5-T02

Task status:
ACTIVE / NOT STARTED

Canonical branch:
main

Latest accepted task-branch software commit:
732cf91890e22a1a66bbe918a4b01500af5966f2

Latest accepted software task:
M5-T01 — Human Command & Confirmation State Layer

Latest approved scientific/architectural decision:
D-068 — Shared-Autonomy to Human-Interaction Authorization Contract

Latest valid reportable experiment:
None yet
```

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, certified safety, or human-subject result claim is authorized.

---

# 2. ACCEPTED IMPLEMENTATION SEQUENCE

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
M1-T07 — Probability Calibration
M1-T08 — Bayesian Goal Inference
M1-T09 — Uncertainty / Shared-Autonomy Policy
M1-T10 — Adaptation / Prior Personalization
M4-T01 — 2D Search & Rescue Environment + Risk Map
M4-T02 — Risk-Aware A* Planner
M4-T03 — Safety Controller / Hard Constraint Enforcement
M4-T04 — Planner → Safety → Environment Execution Integration
M4-T05 — Controlled Replanning After Environment Change
M5-T01 — Human Command & Confirmation State Layer
```

Total accepted implementation tasks: 16. M5-T02 is authorized but not accepted yet.

---

# 3. CURRENT M5 STATE

```text
Shared-autonomy decision policy: PASS
Human command / confirmation state layer: PASS
D-068 authorization transition contract: APPROVED
Shared-autonomy -> human-command authorization bridge: AUTHORIZED / NOT STARTED
Human-command -> planner/safety/execution integration: NOT STARTED
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
```

D-068 boundary:

```text
SharedAutonomyDecision
        ↓
exact symbolic goal validation / confirmation routing
        ↓
HumanInteractionController authorization state
        ↓
STOP — no movement in M5-T02
```

Later execution integration must resolve the approved symbolic goal against the current environment snapshot and separately support interruptible runtime human authority.

---

# 4. D-068 AUTHORITY SUMMARY

```text
M5-T02 authorization-only; no movement
exact current symbolic goal identifiers only
PROCEED cannot bypass PAUSE/STOP/active confirmation
CONFIRM creates one explicit request and cannot autonomously approve
WAITING/DEFER create no commitment
human commands processed only by HumanInteractionController; bridge never synthesizes/double-applies them
no hard-coded binary EEG -> victim mapping
coordinate resolution/runtime execution reserved for later task
```

Accepted authority remains `STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > autonomous policy`; safety retains low-level veto.

---

# 5. M5-T01 ACCEPTED VERIFICATION

```text
python -m pytest tests/test_human_interaction.py -> 19 passed
python -m pytest tests/test_shared_autonomy.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py tests/test_human_interaction.py -> 77 passed
python -m pytest -> 233 passed, 1 known PyTorch warning
```

---

# 6. KNOWN OPERATIONAL ISSUE

`requirements.txt` currently omits `pandas` and `scikit-learn` although accepted pre-M5 modules/tests require them. This remains separate maintenance and is not authorized in M5-T02.

---

# 7. CURRENT BLOCKERS

M5-T02: none under D-068.

Later M5 execution integration is not authorized and must be separately reviewed after M5-T02, especially because the current executor consumes a whole route synchronously while PAUSE/STOP/OVERRIDE require interruptible runtime authority.

Experimental unresolved items remain U-034 final A/B/C/D matrix, U-035 robustness perturbation levels, and U-036 inferential-statistics policy. They do not block M5-T02.

---

# 8. CLAIM STATUS

Implementation claims remain limited to accepted tasks through M5-T01. M5-T02, full human-interaction execution integration, end-to-end EEG-driven mission execution, efficacy/safety improvements, live EEG, physical robot, and certified real-world safety are not yet authorized claims.

---

# 9. NEXT ACTION

Codex implements M5-T02 exactly as `CURRENT_TASK.md` on a new branch from current canonical `main`, runs focused/adjacent/full regressions, commits/pushes, and STOPS for ChatGPT review. Do not merge or begin M5-T03 automatically. Do not bundle dependency maintenance, EEG/full-system integration, UI, logging, or experiments.
'''


def apply_decision(root: Path) -> None:
    path = root / "DECISIONS.md"
    text = path.read_text(encoding="utf-8")
    if "## D-068 — Shared-Autonomy to Human-Interaction Authorization Contract" in text:
        raise SystemExit("D-068 already present")
    marker = "# 3. UNRESOLVED DECISIONS"
    idx = text.find(marker)
    if idx < 0:
        raise SystemExit("unresolved-decisions marker missing")
    text = text[:idx] + DECISION_ENTRY + text[idx:]
    path.write_text(text, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: apply_d068.py <decision|task|state> <repo-root>")
    stage, root_text = sys.argv[1:]
    root = Path(root_text)
    if stage == "decision":
        apply_decision(root)
    elif stage == "task":
        (root / "CURRENT_TASK.md").write_text(CURRENT_TASK, encoding="utf-8")
    elif stage == "state":
        (root / "PROJECT_STATE.md").write_text(PROJECT_STATE, encoding="utf-8")
    else:
        raise SystemExit(f"unknown stage: {stage}")


if __name__ == "__main__":
    main()
