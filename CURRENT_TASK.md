# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no implementation task is currently authorized.  
**Current status:** ACTIVE DOCUMENTATION-ONLY TASK
**Current milestone:** Pre-M6 Audit Remediation
**Task ID:** PRE-M6-R07B
**Task title:** Secondary Documentation Reconciliation
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-09-06

---

# 1. CURRENT AUTHORITY

```text
PRE-M6-R07B - Secondary Documentation Reconciliation
Documentation-only task; no code, tests, configuration, dependencies, or M6 work.
```

Codex is authorized to reconcile only the approved secondary documentation scope for PRE-M6-R07B. No other task or M6 work is authorized.

---

# 2. CLOSED REMEDIATION — PRE-M6-R07A

```text
Task ID: PRE-M6-R07A
Task title: Master Authority Reconciliation
Status: PASS / ACCEPTED / MERGED
Accepted task-branch commit:
94611b858984e10b89849930be698416db871007
Merge commit:
8b919c04553b1f3ccd55647fa02a9543e2efe9d7
```

PRE-M6-R07A reconciled `MASTER_PROJECT_SPEC.md` with already-approved decisions through D-073. It preserved the genuinely unresolved experimental-analysis items:

```text
U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
```

---

# 3. PRE-M6-R07 STATUS

PRE-M6-R07 remains staged. PRE-M6-R07B — Secondary Documentation Reconciliation is **NOT AUTHORIZED**.

The final Pre-M6 audit remains open pending separately reviewed and explicitly authorized R07B work. Do not begin R07B automatically.

---

# 4. M6 BOUNDARY

M6 remains **NOT STARTED** and **NOT AUTHORIZED**.

After all Pre-M6 remediation is accepted and the final audit explicitly passes, ChatGPT and the Project Owner must separately review and approve the exact offline EEG-to-full-system integration contract before any M6 implementation ticket is created.
