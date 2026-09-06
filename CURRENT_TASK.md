# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no implementation task is currently authorized.  
**Current status:** ACTIVE IMPLEMENTATION TASK
**Current milestone:** Pre-M6 Audit Remediation
**Task ID:** PRE-M6-R07A
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-09-06

---

# 1. ACTIVE TASK — PRE-M6-R07A

```text
Task ID: PRE-M6-R07A
Task title: Master Authority Reconciliation
Phase: Pre-M6 Audit Remediation
Task branch: task/pre-m6-r07a-master-reconciliation
Status: ACTIVE IMPLEMENTATION TASK
Parent remediation: PRE-M6-R07
Starting canonical main:
b3f506bdaf44072dcccccfc575822bbd5e654fab
```

## Authorization basis

The Project Owner explicitly approved PRE-M6-R07A to reconcile `MASTER_PROJECT_SPEC.md` using only decisions already approved in `DECISIONS.md`, with no new scientific or architectural changes.

The original PRE-M6-R07 four-file reconciliation stopped correctly after discovering that stale unresolved-state contradictions also exist in the change-controlled Master Specification and other out-of-scope documentation. The uncommitted edits from the original R07 attempt are not part of R07A and must not be committed under this task.

## Objective

Reconcile stale transfer-era / unresolved-state statements in `MASTER_PROJECT_SPEC.md` with already-approved decisions and accepted project facts where the Master currently contradicts those later approvals.

This is authority reconciliation, not redesign. The task must preserve the project constitution while bringing its explicit unresolved-status statements into agreement with already-approved decisions.

## Read first

```text
1. MASTER_PROJECT_SPEC.md
2. DECISIONS.md
3. PROJECT_STATE.md
4. CURRENT_TASK.md
5. AGENTS.md for repository rules only
```

`DECISIONS.md` supplies the already-approved resolutions. Do not invent or improve decision semantics.

## Authorized implementation file

```text
MASTER_PROJECT_SPEC.md
```

No other file is authorized for implementation under PRE-M6-R07A.

## Required reconciliation

Reconcile only stale Master-Spec statements contradicted by already-approved decisions, including where applicable:

```text
CSP configuration -> approved by D-043/D-044
EEGNet architecture/training -> approved by D-045 through D-047
calibration method/fitting/binning -> approved by D-048 through D-050
binary EEG -> multi-goal interaction protocol -> approved by D-051
decoder evidence -> Bayesian likelihood construction -> approved by D-052
Bayesian prior/stopping -> approved by D-053/D-054
uncertainty/shared-autonomy thresholds/fallback -> approved by D-055 through D-057
adaptation mechanism/update/bounds -> approved by D-058 through D-060
risk values/normalization/lambda -> approved by D-061 through D-063
prohibited-hazard/no-safe-path behavior -> approved by D-064/D-065
accepted runtime authority/replanning contracts where the Master states those semantics are unresolved -> D-066 through D-070
central runtime configuration/YAML parser boundaries where relevant -> D-072/D-073
```

Do not merely delete unresolved sections. Replace obsolete unresolved claims with concise statements that point to or faithfully summarize the approved decision state while preserving the Master Specification's constitutional role.

## Must remain unresolved

```text
U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
```

Do not resolve these under R07A.

## Non-negotiable preservation

Preserve without weakening or reinterpretation:

```text
locked project identity and research question
offline prerecorded EEG / simulated real-time BCI only
no live EEG or hardware claim
human determines WHAT; AI determines HOW
binary decoder semantics; no fabricated direct K-goal decoder
calibrated-probability / Bayesian / uncertainty separation
human CONFIRM/OVERRIDE/PAUSE/STOP authority
safety veto and hard-safety vs soft-risk separation
D-069 stepwise execution
D-070 replacement-snapshot replanning
no fabricated results or efficacy claims
negative/mixed results remain valid
```

## Forbidden changes

```text
no DECISIONS.md changes
no PROJECT_STATE.md implementation-status rewriting beyond later governance close
no AGENTS/TODO/RESEARCH_LOG/README/numbered-doc edits
no production code, tests, config, dependencies, workflows, or artifacts
no M6 contract or implementation
no UI, experiments, logging/provenance implementation
no new scientific or architectural decisions
no rewriting approved decisions merely for stylistic preference
```

## Verification

Before committing, Codex must:

```text
review the complete MASTER_PROJECT_SPEC.md diff
search the Master for stale current unresolved claims corresponding to decisions already approved through D-073
confirm U-034/U-035/U-036 remain unresolved
confirm no file other than MASTER_PROJECT_SPEC.md changed for the R07A candidate
confirm no new scientific/architectural semantics were introduced
```

Production tests are not required because this task is documentation-only.

## Stop conditions

Stop and report instead of expanding scope if:

- a Master statement cannot be reconciled unambiguously from an approved D-xxx decision;
- reconciliation would require changing an approved decision rather than reflecting it;
- a new scientific/architectural decision is needed;
- an edit outside `MASTER_PROJECT_SPEC.md` is needed for R07A completion;
- the task would begin M6, experiments, UI, or implementation work.

## Completion report

Report:

```text
Status:
Starting main SHA:
Task branch:
Files modified:
Master sections reconciled:
Approved D-xxx entries used:
Unresolved items preserved:
Verification/search commands:
Verification result:
Open blockers:
Candidate commit SHA:
Suggested commit message:
```

After completing PRE-M6-R07A:

```text
STOP
```

Do not merge, resume R07B, close Pre-M6, or begin M6 automatically.

---

# 2. PARENT REMEDIATION — PRE-M6-R07

PRE-M6-R07 — Governance and Decision-State Documentation Reconciliation was authorized after the final Pre-M6 audit found stale decision-state claims in implementation-facing documentation.

Its first implementation attempt stopped correctly because material stale contradictions were also found outside its original four-file scope, including `MASTER_PROJECT_SPEC.md` and numerous secondary documents.

R07 is therefore split into controlled stages:

```text
PRE-M6-R07A — Master Authority Reconciliation (ACTIVE)
PRE-M6-R07B — Secondary Documentation Reconciliation (NOT AUTHORIZED YET)
```

R07B may be defined only after R07A is reviewed and merged.

---

# 3. CLOSED REMEDIATION THROUGH R06

PRE-M6-R01 through PRE-M6-R06 are PASS / ACCEPTED / MERGED. PRE-M6-R06 accepted candidate `23196b8c11ccc800728a077a9ea4203b6be9ae7b`, merged software commit `f66dba3b78dc91abedaff1b24a3597c7748426df`, with installation PASS and `327 passed, 1 warning`.

---

# 4. NEXT ARCHITECTURAL BOUNDARY

M6 remains NOT STARTED and NOT AUTHORIZED.

After all Pre-M6 remediation is accepted and the final audit explicitly passes, ChatGPT and the Project Owner must separately review and approve the exact offline EEG-to-full-system integration contract before any M6 implementation ticket is created.
