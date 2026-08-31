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
```

M1-T04 acceptance and merge record:

```text
Accepted task-branch commit:
86b47c56bd655900cf478dbb7af6ec13eeb26e41

Pull request:
#13 — M1-T04: Implement EEG split manifest

Squash-merge commit:
3b33477166db6889747dabc8d4be21403b480735
```

M1-T04 operationalizes D-040 through D-042 with deterministic within-subject and cross-subject split manifests, explicit leakage validation, auditable persistence/provenance, and protected final-test membership.

Do not begin CSP/LDA or any later implementation module without a new explicitly approved `CURRENT_TASK.md` ticket.

U-013 — Final CSP configuration remains unresolved. This closeout does not resolve or reinterpret it.

---

# 2. CLOSED TASK RECORD — M1-T04

```text
Task ID:
M1-T04

Task title:
EEG Split Manifest

Final status:
PASS / ACCEPTED / MERGED

Task branch:
task/m1-t04-eeg-split-manifest

Accepted branch commit:
86b47c56bd655900cf478dbb7af6ec13eeb26e41

Merged through:
PR #13

Canonical software merge commit:
3b33477166db6889747dabc8d4be21403b480735
```

Accepted scope:

```text
- deterministic class-stratified within-subject 60/20/20 assignments
- original-trial grouping and derived-window leakage protection
- deterministic seed-42 cross-subject assignment
- exact 76/16/17 counts for the full eligible 109-subject cohort
- subject disjointness and completeness validation
- versioned manifest persistence, reload, provenance, and final-test protection
- explicit stop for unsupported cross-subject cohort sizes
- targeted automated tests
```

No CSP/LDA, EEGNet, calibration, Bayesian, shared-autonomy, planning, safety, replay, or experiment implementation was authorized or merged in M1-T04.

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

For CSP/LDA specifically, U-013 remains unresolved and must not be silently decided.

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
