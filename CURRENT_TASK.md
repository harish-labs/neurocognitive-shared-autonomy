# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no implementation task is currently authorized.  
**Current status:** ACTIVE IMPLEMENTATION TASK
**Current milestone:** Pre-M6 Audit Remediation
**Task ID:** PRE-M6-R07
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-09-06

---

# 1. ACTIVE TASK — PRE-M6-R07

```text
Task ID: PRE-M6-R07
Task title: Governance and Decision-State Documentation Reconciliation
Phase: Pre-M6 Audit Remediation
Task branch: task/pre-m6-r07-doc-reconciliation
Status: ACTIVE IMPLEMENTATION TASK
Starting canonical main:
7fdb8d914458551c287a3e19c03135228c5c123b
```

## Objective

Reconcile stale governance/reference documentation with already-approved decisions and already-accepted implementation state so Codex does not encounter obsolete unresolved/blocking statements when entering the M6 design boundary.

This is documentation/governance-state reconciliation only. It must not create new scientific decisions, change approved semantics, modify production/test behavior, or implement M6.

## Read first

```text
1. MASTER_PROJECT_SPEC.md
2. CURRENT_TASK.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. AGENTS.md
6. TODO.md
7. RESEARCH_LOG.md
8. docs/15_IMPLEMENTATION_BLUEPRINT.md
```

`DECISIONS.md` is authoritative for approved decisions. `PROJECT_STATE.md` is authoritative for verified current state. Do not reinterpret or improve approved decisions while reconciling stale documentation.

## Authorized implementation files

```text
AGENTS.md
TODO.md
RESEARCH_LOG.md
docs/15_IMPLEMENTATION_BLUEPRINT.md
```

No production code, tests, configuration, dependency files, experiment files, Master Specification, or `DECISIONS.md` changes are authorized under PRE-M6-R07.

If another document is found to contain the same material stale decision-state contradiction, stop and report it for separate scope approval rather than editing it automatically.

## Requirements

1. Remove or update stale statements that mark already-approved decisions as unresolved or blocked.
2. Preserve the exact substance of approved decisions in `DECISIONS.md`; do not create substitute summaries that change semantics.
3. Reconcile at minimum the stale status of decisions already resolved by D-043 through D-073 where those stale statements appear in the authorized files.
4. In particular, ensure already-resolved areas are not still presented as open blockers, including:
   ```text
   CSP configuration
   EEGNet architecture/training
   calibration method/fitting/binning
   binary EEG -> candidate interaction protocol
   decoder evidence -> Bayesian likelihood construction
   Bayesian prior/stopping rules
   uncertainty/shared-autonomy thresholds and fallback
   adaptation mechanism/update/bounds
   environmental risk values/normalization/lambda
   prohibited-hazard threshold
   no-safe-path policy
   accepted replanning/human-authority contracts where referenced
   ```
5. Preserve the genuinely unresolved experimental decisions exactly as unresolved:
   ```text
   U-034 — final A/B/C/D component matrix
   U-035 — robustness perturbation levels
   U-036 — inferential-statistics policy
   ```
6. Preserve offline prerecorded EEG / simulated real-time BCI claim discipline.
7. Preserve human WHAT authority, accepted binary decoder semantics, safety veto, D-069 stepwise navigation, and D-070 replanning semantics.
8. Do not author the M6 end-to-end integration contract under this task.
9. Do not start M6, UI, reportable experiments, logging/provenance infrastructure, or artifact-persistence work.
10. Do not modify implementation history merely to make documents look cleaner; historical statements may remain when clearly identified as historical rather than current blockers.

## Verification

Minimum verification:

```text
review git diff for all authorized files
search authorized files for stale unresolved/blocker references to already-resolved U-013 through U-033 / corresponding D-xxx decisions
confirm U-034/U-035/U-036 remain unresolved
confirm no files outside the authorized set changed
```

Because this task is documentation-only, production test execution is not required unless an unexpected repository rule or validation hook requires it. Do not fabricate test execution.

## Acceptance criteria

PRE-M6-R07 may be accepted only if:

```text
all material stale current-state contradictions in the four authorized files are reconciled
+
no approved decision is changed or reinterpreted
+
U-034/U-035/U-036 remain unresolved
+
no production/test/configuration behavior changes
+
no M6 architecture or implementation is introduced
+
changed files remain within the exact authorized set
```

## Stop conditions

Stop and report instead of expanding scope if:

- reconciliation would require changing `MASTER_PROJECT_SPEC.md` or `DECISIONS.md`;
- a stale statement cannot be reconciled unambiguously from canonical approved decisions/state;
- another file outside the authorized set contains a material contradiction that must be changed for a clean Pre-M6 close;
- a new scientific/architectural decision is required;
- implementation would begin M6, UI, experiments, logging/provenance, or production-code work.

## Completion report

Report:

```text
Status:
Starting main SHA:
Task branch:
Files modified:
Stale decision-state claims reconciled:
Approved decisions referenced:
Unresolved items preserved:
Verification/search commands:
Verification result:
Out-of-scope stale files discovered:
Open blockers:
Candidate commit SHA:
Suggested commit message:
```

After completing PRE-M6-R07:

```text
STOP
```

Do not merge, close Pre-M6, or begin M6 automatically.

---

# 2. CLOSED TASK — PRE-M6-R06

```text
Task ID: PRE-M6-R06
Task title: Accepted-Code Dependency Manifest Reconciliation
Phase: Pre-M6 Audit Remediation
Task branch: task/pre-m6-r06-dependency-manifest
Status: PASS / ACCEPTED / MERGED
Starting canonical main:
eb5b8cd58c7a7e0a52d293e62d91870532559177
```

Final candidate commit:
23196b8c11ccc800728a077a9ea4203b6be9ae7b

Final merged software commit:
f66dba3b78dc91abedaff1b24a3597c7748426df

Merge commit:
f66dba3b78dc91abedaff1b24a3597c7748426df

Verification:

- `requirements.txt` adds exactly `pandas`, `scikit-learn`, and `matplotlib`.
- Installation from `requirements.txt` succeeded.
- Full suite: `327 passed, 1 warning`.
- Warning: pre-existing PyTorch convolution padding warning.

PRE-M6-R06 is complete and accepted.

---

# 3. CLOSED TASK RECORD — PRE-M6-R05

```text
Task ID: PRE-M6-R05
Task title: Central Runtime Composition Configuration
Phase: Pre-M6 Audit Remediation
Task branch: task/pre-m6-r05-runtime-config
Final status: PASS / SCIENTIFICALLY ACCEPTED / MERGED
Canonical software SHA: 2ccb665cf20666d1af7abb931a481a27d402d7e6
```

Objective:

```text
Implement a validated typed central runtime/composition configuration boundary under D-072 while preserving existing scientific-policy owners and existing domain configuration/state contracts.
```

Accepted implementation files:

```text
config.yaml
src/config.py
tests/test_config.py
requirements.txt
```

Accepted dependency change: `requirements.txt` adds only the PyYAML dependency approved by D-073.

---

# 4. CLOSED TASK SUMMARY

Accepted tasks before PRE-M6-R07 include M1-T01 through M1-T10, M4-T01 through M4-T05, M5-T01 through M5-T04, and PRE-M6-R01 through PRE-M6-R06.

The authoritative details of earlier closed tasks remain in Git history and `PROJECT_STATE.md`.

---

# 5. NEXT ARCHITECTURAL BOUNDARY

The next project boundary after all Pre-M6 remediation is accepted is offline EEG-to-full-system integration, but no M6 implementation is authorized by PRE-M6-R07.

Before any M6 implementation ticket is created, ChatGPT and the Project Owner must review the exact end-to-end integration contract connecting the accepted offline EEG decoding / calibration / Bayesian inference / uncertainty-aware shared autonomy / human authorization layers to the accepted M5 stepwise navigation runtime.

Preserve at least:

```text
offline prerecorded EEG / simulated real-time BCI only
no live EEG or hardware claim
accepted binary left/right decoder semantics and approved goal-inference rules
no fabricated direct multi-goal decoder
calibrated probabilities and Bayesian thresholds remain unchanged
human WHAT authority and confirmation/override/pause/stop precedence remain unchanged
fresh execution authorization remains required before navigation
D-069 stepwise movement and D-070 replacement-snapshot replanning remain authoritative
safety veto before every movement
no automatic scope expansion into UI, reportable experiments, logging infrastructure, or unrelated dependency maintenance
```

---

# 6. UNRESOLVED EXPERIMENTAL DECISIONS

The following remain unresolved and are not authorized by this task:

```text
U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
```
