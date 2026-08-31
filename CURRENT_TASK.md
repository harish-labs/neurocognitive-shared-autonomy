# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### No Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no task is currently authorized  
**Current status:** NO ACTIVE TASK  
**Current milestone:** M1 — EEG Dataset / Loader / Epochs / CSP+LDA  
**Task ID:** NONE AUTHORIZED  
**Task title:** Awaiting next approved implementation ticket  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Last updated:** 2026-08-31

---

# 1. CURRENT AUTHORIZATION STATE

There is currently no active implementation task authorized for Codex.

Completed, scientifically reviewed, accepted, and merged on canonical `main`:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
```

M1-T05 acceptance and merge record:

```text
Accepted rebased task-branch commit:
e1f35e0dd8dd3296b6f85e32ac4ed5a6fd6e2d50

Pull request:
not created / not verifiable from this environment

Squash-merge commit:
d7597efb8db7c8d77aecbd87f9cf2366dd02b484
```

M1-T05 implements the approved CSP+LDA baseline under D-033 and D-040 through D-044 with train-only fitting, validation-only component selection by balanced accuracy across the full approved `{2,4,6,8}` set, deterministic tie-breaking, protected test/final-test isolation, and probability output.

Do not begin EEGNet or any later implementation module without a new explicitly approved `CURRENT_TASK.md` ticket.

U-014 and later unresolved decisions remain unresolved. This closeout does not resolve or reinterpret them.

---

# 2. CLOSED TASK RECORD — M1-T05

```text
Task ID:
M1-T05

Task title:
CSP+LDA Baseline

Final status:
PASS / ACCEPTED / MERGED

Task branch:
task/m1-t05-csp-lda-baseline

Accepted rebased branch commit:
e1f35e0dd8dd3296b6f85e32ac4ed5a6fd6e2d50

Merged through:
approved squash merge on canonical main

Canonical software merge commit:
d7597efb8db7c8d77aecbd87f9cf2366dd02b484
```

Accepted scope:

```text
- single CSP+LDA baseline module
- CSP crop +1.0 s to +2.0 s applied only inside the CSP path
- all 64 channels preserved
- CSP candidates evaluated over the full approved set {2,4,6,8}
- validation balanced accuracy used for candidate selection
- deterministic tie-break to 4 when tied, otherwise smallest tied candidate
- train-only fitting and protected test/final-test isolation
- stable predict / predict_proba behavior and class-order coverage
- targeted automated tests
```

No EEGNet, calibration, Bayesian, shared-autonomy, planning, safety, replay, or later experiment implementation was authorized or merged in M1-T05.

---

# 3. NEXT GOVERNANCE GATE

Before any further implementation:

```text
1. Resolve any scientific decision required by the proposed task.
2. Record the approved decision in DECISIONS.md when applicable.
3. Draft one narrow implementation ticket.
4. Obtain explicit Project Owner approval.
5. Record that ticket here before Codex begins implementation.
```

For EEGNet and later modules, unresolved decisions remain and must not be silently decided.

Until a new ticket is approved:

```text
STOP
STATUS = NO ACTIVE TASK
```

---

# 4. READ FIRST FOR THE NEXT TASK

Before activating or implementing any future ticket, read in this order:

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
