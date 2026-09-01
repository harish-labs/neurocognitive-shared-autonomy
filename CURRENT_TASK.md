# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no implementation task is currently authorized.  
**Current status:** NO ACTIVE IMPLEMENTATION TASK  
**Current milestone:** M5 — Shared Autonomy + Human Interaction  
**Task ID:** None  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-09-01

---

# 1. CLOSED TASK RECORD — M5-T01

```text
Task ID: M5-T01
Task title: Human Command & Confirmation State Layer
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Task branch: task/m5-t01-human-interaction
Accepted task-branch head / canonical software commit:
732cf91890e22a1a66bbe918a4b01500af5966f2
```

Accepted implementation scope:

```text
src/control/human_interaction.py
tests/test_human_interaction.py
```

Accepted M5-T01 behavior:

```text
D-067 human-command contract enforced
unique non-empty command_id with single-consumption / ALREADY_CONSUMED behavior
unique confirmation request_id with exact-active-request CONFIRM semantics
stale/non-active confirmation rejection
CONFIRM approves only the candidate attached to the active request
OVERRIDE validates exact currently valid goals and fails closed for unsupported containers
OVERRIDE cancels active confirmation, preserves PAUSE, and only signals fresh downstream execution
PAUSE preserves interaction state and blocks autonomous motion state
RESUME is valid only from PAUSED, preserves approved goal, and never replays queued movement
STOP is terminal until explicit reset/new session and blocks lower-authority commands
headless deterministic state layer only; no planner/safety/environment/EEG/Bayesian/UI execution integration added
```

Accepted verification was run through a temporary GitHub Actions verification branch rooted at the accepted task SHA. The verification-only workflow file was not merged into `main`.

```text
python -m pytest tests/test_human_interaction.py
-> 19 passed

python -m pytest tests/test_shared_autonomy.py tests/test_safety.py tests/test_execution.py tests/test_replanning.py tests/test_human_interaction.py
-> 77 passed

python -m pytest
-> 233 passed, 1 warning
```

The warning is the already-known non-failing PyTorch same-padding warning from the EEGNet/calibration path.

The clean CI environment also exposed an existing dependency-manifest gap: `requirements.txt` does not currently list `pandas` or `scikit-learn`, although accepted pre-M5 modules/tests require them. Those packages were added only to the temporary verification environment so the canonical regression suite could run. M5-T01 did not modify `requirements.txt`.

---

# 2. IMPLEMENTATION AUTHORITY NOW

```text
No Codex implementation task is currently authorized.
```

M5-T01 is complete and merged. Do not begin another M5 task automatically.

The next architectural boundary is a separately reviewed integration task connecting the already accepted shared-autonomy decision policy to the accepted human-command state layer and, only when authorized, to the accepted planner/safety/execution stack.

Before authorizing that integration, ChatGPT and the Project Owner must review the exact transition/data-flow contract. Codex must not invent integration semantics independently.

The discovered dependency-manifest gap (`pandas`, `scikit-learn` absent from `requirements.txt`) should also be handled through a separate narrow maintenance/governance decision or task rather than being silently bundled into M5 integration.

---

# 3. FORBIDDEN UNTIL SEPARATELY AUTHORIZED

Do not begin:

```text
shared-autonomy -> human-command integration
human-command -> planner/safety/execution integration
EEG -> full mission execution
adaptation updates triggered from the new interaction layer
UI / Streamlit callbacks
logging/experiment orchestration
A/B/C/D experiments
robustness experiments
reportable efficacy claims
```

Unresolved experimental decisions remain:

```text
U-034 — Final A/B/C/D component matrix
U-035 — Robustness perturbation levels
U-036 — Final inferential-statistics policy
```
