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

Completed, scientifically reviewed, and merged on canonical `main`:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
```

Latest accepted software commit:

```text
1af72b5deb9981f469a4394859aac49add65e2a7
M1-T03: Implement EEG preprocessing and epochs (#9)
```

Latest approved scientific-decision commit:

```text
ea00a631b60967cfece65b42e00e7b36c4efac7d
Record approved EEG split and held-out subject protocol (#10)
```

Approved split decisions now recorded in `DECISIONS.md`:

```text
D-040 — EEG Train / Validation / Test Evaluation Tracks
D-041 — Primary Cross-Subject Evaluation Protocol
D-042 — Fixed Held-Out Subject Strategy
```

These resolve U-010, U-011, and U-012.

The next candidate task is a narrow M1 split-manifest implementation task, but it is **not authorized yet**. Before implementation begins, the affected numbered methodology/state documentation must be reconciled to D-040 through D-042 and a new explicit implementation ticket must be approved and recorded here.

Do not begin dataset splitting, CSP/LDA, EEGNet, calibration, or any later module until a new active ticket exists.

---

# 2. READ FIRST

Before any future implementation ticket is activated, Codex must read in this order:

```text
1. MASTER_PROJECT_SPEC.md
2. CURRENT_TASK.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. AGENTS.md
6. numbered methodology documents referenced by the new ticket
7. relevant accepted source code and tests
```

If any required file conflicts with `MASTER_PROJECT_SPEC.md` or an approved Project Owner decision:

```text
STOP
STATUS = BLOCKED
REPORT THE CONFLICT
```

---

# 3. NEXT GOVERNANCE GATE

Required before M1 split-manifest implementation:

```text
1. Reconcile relevant methodology documents to D-040 through D-042.
2. Verify canonical main and accepted M1-T03 code/tests.
3. Draft one narrow M1 split-manifest implementation ticket.
4. Obtain explicit Project Owner approval for that ticket.
5. Record the active ticket in this file.
```

Until then:

```text
STOP
```
