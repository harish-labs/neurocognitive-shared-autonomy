# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex.  
**Current status:** ACTIVE / NOT STARTED  
**Current milestone:** M5 — Shared Autonomy + Human Interaction  
**Task ID:** M5-T01  
**Task title:** Human Command & Confirmation State Layer  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Approved decision baseline:** `0c2ed84207f55303610d8b7c61bd9e99eea8301a`  
**Branch rule:** Create the task branch from the current `main` after this authorization and its corresponding `PROJECT_STATE.md` update are present.  
**Last updated:** 2026-09-01

---

# 1. CLOSED TASK RECORD — M4-T05

```text
Task ID: M4-T05
Task title: Controlled Replanning After Environment Change
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Task branch: task/m4-t05-controlled-replanning
Accepted task-branch head / canonical software commit:
e8183ccebc9c2f67a1b33347b9ef12d25ddbcbfe
```

Accepted M4-T05 verification:

```text
pytest tests/test_replanning.py -> 13 passed
pytest tests/test_environment.py tests/test_planner.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py -> 84 passed
pytest -> 214 passed, 1 pre-existing non-failing PyTorch warning
```

The complete accepted M4 autonomy stack now includes environment/risk map, risk-aware A*, hard safety, safety-gated execution, and D-066 controlled replanning.

---

# 2. M5-T01 OBJECTIVE

Implement only the deterministic, headless human-command and confirmation-request state layer required by D-067.

The task owns command identity, confirmation-request identity/staleness, human goal approval/correction state, PAUSE/RESUME/STOP state, duplicate protection, and explicit command results.

It does **not** execute navigation, run the shared-autonomy Bayesian policy, invoke EEG/model code, or implement UI callbacks.

Conceptual boundary:

```text
upstream shared-autonomy / mission layer
        ↓
confirmation request or explicit human command
        ↓
M5-T01 human interaction state layer
        ↓
explicit deterministic command result / human-control state
        ↓
future integration task
```

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
8. docs/14_SAFETY_CRITICAL_CONTROL.md
9. docs/15_IMPLEMENTATION_BLUEPRINT.md
10. docs/16_REPOSITORY_AND_CODE_ARCHITECTURE.md
11. docs/19_TESTING_AND_VERIFICATION.md
12. src/control/shared_autonomy.py
13. src/autonomy/safety.py
14. src/autonomy/execution.py
15. src/autonomy/replanning.py
16. relevant accepted tests
```

GitHub `main` is canonical.

---

# 4. GOVERNING DECISIONS

Preserve all existing approved decisions, especially:

```text
D-003 — human determines WHAT; AI determines HOW safely
D-016 — required human controls
D-021 — planner -> safety -> environment execution
D-056 — explicit human confirmation and human PAUSE/STOP/OVERRIDE precedence
D-057 — unresolved uncertainty holds position / requests human input
D-058 through D-060 — explicit-feedback adaptation boundary
D-064/D-065 — hard safety and no-safe-path behavior
D-066 — controlled replanning contract
D-067 — Human Interaction Command Contract
```

D-067 is authoritative for M5-T01.

---

# 5. ALLOWED FILES

Primary authorized files:

```text
src/control/human_interaction.py
tests/test_human_interaction.py
```

Only if genuinely required for package exports/imports:

```text
src/control/__init__.py
```

Do not modify accepted modules unless a genuine interface defect makes the task impossible:

```text
src/control/shared_autonomy.py
src/autonomy/environment.py
src/autonomy/planner.py
src/autonomy/safety.py
src/autonomy/execution.py
src/autonomy/replanning.py
src/cognition/*
src/models/*
src/eeg/*
```

If such a defect exists, stop and report `BLOCKED` rather than changing accepted semantics.

---

# 6. COMMAND VOCABULARY

Support exactly these human command types for this task:

```text
CONFIRM
OVERRIDE
PAUSE
RESUME
STOP
```

Each command must carry a unique non-empty `command_id`.

A CONFIRM command also carries the target `request_id`.

An OVERRIDE command also carries the explicitly selected goal.

Do not add additional human command types, automatic commands, timers, or hidden transitions.

---

# 7. CONFIRMATION REQUEST CONTRACT

Represent an active confirmation request explicitly and immutably/read-only where practical.

It must contain at least:

```text
request_id
candidate_goal
```

Required behavior:

```text
each request_id is non-empty and unique within the controller/session state
there is at most one currently active confirmation request
CONFIRM must reference the exact active request_id
CONFIRM for a stale/non-active request_id is rejected
CONFIRM approves only the candidate_goal attached to that request
CONFIRM cannot supply/substitute another goal
accepted CONFIRM consumes/closes that request
repeated confirmation of an already consumed/stale request cannot approve or execute anything again
```

The layer may expose a small explicit API to register/open a confirmation request. Do not generate nondeterministic IDs internally; the caller may supply the explicit request ID.

Do not compute Bayesian confidence or decide when CONFIRM should be requested in this task. That remains upstream shared-autonomy policy behavior.

---

# 8. HUMAN CONTROL STATE

Maintain explicit deterministic human-control state sufficient to represent at least:

```text
current approved_goal or None
active confirmation request or None
paused: bool
stopped: bool
consumed command IDs
consumed/closed confirmation request IDs as needed for stale/duplicate protection
```

State must not depend on UI widget state.

STOP is terminal for this controller/session until an explicit reset/new-session API is invoked.

If an explicit reset/new-session helper is implemented, it may only clear M5-T01 interaction state; it must not reset EEG models, Bayesian/adaptation state, environments, or mission execution because those integrations are outside this task.

---

# 9. COMMAND RESULT CONTRACT

Return an immutable structured result for each handled command.

It must expose enough information to audit at least:

```text
status
command_id
command_type
accepted / applied
approved_goal after handling
paused after handling
stopped after handling
active_request_id after handling, if any
requires_fresh_execution or equivalent explicit downstream flag when applicable
reason
```

Recommended statuses include semantics equivalent to:

```text
APPLIED
REJECTED
STALE_REQUEST
ALREADY_CONSUMED
INVALID_GOAL
INVALID_STATE
```

Exact enum names may differ if the behavior remains explicit and deterministically tested.

M5-T01 returns state/intent-to-control information only; it does not itself call planner/safety/environment execution.

---

# 10. CONFIRM SEMANTICS

For a valid active confirmation request:

```text
exact request_id match required
accepted CONFIRM sets approved_goal to the request's candidate_goal
active confirmation becomes closed/inactive
command_id becomes consumed
no movement is executed
```

Invalid/stale request:

```text
no goal approval change
no request resurrection
no downstream execution request
explicit rejected/stale result
```

A duplicate command_id must be rejected as already consumed with no repeated effect.

---

# 11. OVERRIDE SEMANTICS

OVERRIDE must receive an explicit goal and a caller-supplied set/mapping of currently valid mission goals sufficient for validation.

Required behavior:

```text
unknown/non-current goal -> INVALID_GOAL / no state change except command consumption as appropriate
valid goal -> becomes the human-approved goal
valid OVERRIDE cancels/invalidates any active confirmation request
valid OVERRIDE supersedes the prior approved-goal commitment in the interaction state
no movement toward either old or new goal occurs inside M5-T01
result explicitly indicates that future execution must be fresh/re-authorised through the accepted planner -> safety -> environment path
```

OVERRIDE must never create a low-level movement action or bypass safety.

If the interaction state is PAUSED, an otherwise valid OVERRIDE may update the human-approved goal but must **not clear PAUSE** or imply movement; PAUSE remains effective until a valid RESUME. This preserves the approved authority ordering without converting OVERRIDE into resume.

If the interaction state is STOPPED, OVERRIDE is invalid and cannot restart the session.

---

# 12. PAUSE SEMANTICS

Required behavior:

```text
PAUSE sets/retains paused=True
preserve approved_goal
preserve current confirmation/control state unless invalidated by another separately valid human action
no movement or queued-action execution occurs
repeated PAUSE with a new command_id is idempotent at the state-effect level
```

A duplicate command_id remains `ALREADY_CONSUMED` rather than being reprocessed.

PAUSE does not call safety/execution in this task; future integration will propagate the state to those accepted layers.

---

# 13. STOP SEMANTICS

Required behavior:

```text
STOP sets stopped=True
STOP also ensures paused/no-autonomous-motion state for this interaction session
STOP cancels/invalidates any active confirmation request
STOP does not erase historical approved-goal information unless needed by a clearly documented state representation
no planner/executor call occurs
```

After STOP:

```text
CONFIRM -> invalid
OVERRIDE -> invalid
PAUSE -> no restart / no lower-authority effect
RESUME -> invalid
```

Continuing autonomous interaction requires an explicit reset/new session outside ordinary RESUME semantics.

STOP cannot be bypassed by model/shared-autonomy state.

---

# 14. RESUME SEMANTICS

RESUME is valid only when:

```text
paused=True
stopped=False
```

Valid RESUME:

```text
sets paused=False
preserves the same approved_goal
never replays an old/queued action
returns an explicit requires_fresh_execution=True (or semantically equivalent) signal if an approved goal exists
performs no planning/safety/environment execution itself
```

If there is no approved goal, RESUME may simply clear PAUSE without inventing a goal or movement request; report that state explicitly.

If an environment changed while paused, M5-T01 does not inspect or replan the map. A later integration task must use D-066 before movement.

RESUME when not paused or after STOP -> explicit invalid-state result.

---

# 15. DUPLICATE / CONSUMPTION RULE

For every non-empty valid command ID received by the controller:

```text
first processing attempt -> deterministic result and consume the command ID
second/subsequent use of the same command_id -> ALREADY_CONSUMED
no repeated state transition
no repeated goal approval
no repeated downstream execution signal
```

Malformed input that cannot be identified as a valid non-empty command ID may be rejected without inserting an unusable identifier into consumed state.

Do not implement expiration times, asynchronous queues, retry workers, timestamps as authority, or background processing.

---

# 16. AUTHORITY PRECEDENCE

Preserve D-067:

```text
STOP
> PAUSE
> OVERRIDE
> CONFIRM / RESUME
> shared-autonomy policy
> planner
> safety
> environment execution
```

For M5-T01 this means, at minimum:

```text
STOPPED cannot be escaped by lower-authority commands
PAUSE remains active unless explicitly RESUMED or STOPPED
OVERRIDE cannot silently unpause or bypass STOP
CONFIRM cannot bypass PAUSE/STOP into execution
RESUME cannot bypass STOP
```

Safety's movement veto remains downstream and is never weakened by this state layer.

---

# 17. REQUIRED TESTS

Add focused deterministic tests covering at least:

```text
open/register valid confirmation request
exact active request CONFIRM -> candidate becomes approved goal
CONFIRM cannot substitute another goal
stale/non-active request_id rejected
consumed confirmation cannot be applied again
unique command_id consumed once
duplicate command_id -> ALREADY_CONSUMED with identical state/no repeated effect
valid OVERRIDE -> supplied valid goal becomes approved
invalid/non-current override goal rejected
OVERRIDE cancels active confirmation
OVERRIDE while paused keeps paused=True
STOP blocks later CONFIRM
STOP blocks later OVERRIDE
STOP blocks RESUME
STOP cancels active confirmation
PAUSE preserves approved goal
repeated PAUSE with distinct command IDs is idempotent
RESUME only valid from paused and not stopped
RESUME preserves approved goal
RESUME never executes/replays a queued action
RESUME with approved goal emits fresh-execution-needed signal without calling planner/executor
RESUME with no approved goal invents no goal
no command handler imports/calls EEG/model/Bayesian inference
no command handler calls environment.step(), A*, executor, or replanning coordinator
identical command sequences on fresh controller instances produce identical state/results
```

Use small synthetic goal identifiers/coordinates; do not require Streamlit.

---

# 18. REGRESSION REQUIREMENT

Run at minimum:

```text
pytest tests/test_human_interaction.py
pytest tests/test_shared_autonomy.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py tests/test_human_interaction.py
pytest
```

If the accepted shared-autonomy test filename differs, use the actual canonical filename and report it exactly.

Report exact results. The existing non-failing PyTorch warning may remain if unchanged.

---

# 19. OUT OF SCOPE / FORBIDDEN

Do not implement:

```text
full shared-autonomy -> human-command integration loop
Bayesian/uncertainty policy changes
new thresholds
EEG replay/model inference/calibration
adaptation updates from commands
planner invocation
safety invocation
environment.step()
controlled replanning invocation
UI / Streamlit callbacks
logging infrastructure / experiment metrics
network/API command transport
background/asynchronous command queues
timeouts or stale-by-wall-clock policies
multi-user interaction
reportable experiments or efficacy claims
```

Do not call prerecorded EEG live EEG.

---

# 20. ACCEPTANCE CRITERIA

M5-T01 may be reported PASS only if:

```text
D-067 command and request identity semantics are enforced
stale/duplicate inputs fail without repeated effects
CONFIRM approves only its attached candidate
OVERRIDE validates and changes only the human-approved goal state
PAUSE is reversible only through valid RESUME
STOP is terminal until explicit reset/new session
RESUME never replays old movement and only signals fresh downstream execution
no planner/safety/environment/EEG integration is added
focused + integration-adjacent + full regression tests pass
no new scientific/architectural policy is invented
```

---

# 21. STOP CONDITIONS

Stop and report `BLOCKED` if:

```text
D-067 conflicts with accepted shared-autonomy behavior
implementation requires changing accepted shared_autonomy/safety/execution/replanning semantics
an additional human-command precedence decision is required
implementation requires UI/network/asynchronous behavior to function
unrelated accepted modules must be modified
```

After implementation, tests, commit, and push:

```text
STOP
```

Do not merge and do not begin M5 integration, EEG/full-system integration, UI, logging, or experiments until ChatGPT review and Project Owner acceptance.
