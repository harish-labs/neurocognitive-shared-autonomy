# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### No Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no task is currently authorized  
**Current status:** NO ACTIVE TASK / PENDING APPROVAL  
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / CSP+LDA  
**Task ID:** NONE AUTHORIZED  
**Task title:** Awaiting next approved implementation ticket  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`

---

# 1. CURRENT AUTHORIZATION STATE

There is currently no active implementation task authorized for Codex.

Completed and merged on canonical `main`:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
```

Latest canonical governance commit:

```text
d71292387d4476b8ab40841d4ed1544cba3d81b6
Reconcile numbered methodology for M1-T03 (#6)
```

Latest verified software commit:

```text
9b241681dfc986f53f5f8c0fcf40a3e3cea496e7
M1-T02: Add EEG visualization and inspection (#2)
```

Scientific preprocessing decisions U-001 through U-009 are approved and recorded as D-031 through D-039 in `DECISIONS.md`. The affected numbered methodology documents (`docs/06`, `docs/08`, and `docs/15`) are reconciled to those decisions on canonical `main`.

The scientific and documentation prerequisites for drafting an M1-T03 preprocessing/epoching ticket are satisfied, but this does **not** itself authorize implementation.

Do not begin M1-T03 preprocessing/epoching until a new implementation ticket is explicitly approved in this file.

Do not implement preprocessing, epoching, or any later module until that authorization exists.

---

# 2. READ FIRST

Codex must read, in this order:

```text
1. MASTER_PROJECT_SPEC.md
2. AGENTS.md
3. PROJECT_STATE.md
4. DECISIONS.md
```

If any required file conflicts with `MASTER_PROJECT_SPEC.md`, stop and report the conflict.

---

# 3. DO NOT CONTINUE

Until a new task is explicitly approved:

```text
STOP
```
