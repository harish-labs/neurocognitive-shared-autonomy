# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no implementation task is currently authorized.  
**Current status:** ACTIVE IMPLEMENTATION TASK
**Current milestone:** Pre-M6 Audit Remediation
**Task ID:** PRE-M6-R06
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-09-03

---

# 1. ACTIVE TASK — PRE-M6-R06

```text
Task ID: PRE-M6-R06
Task title: Accepted-Code Dependency Manifest Reconciliation
Phase: Pre-M6 Audit Remediation
Task branch: task/pre-m6-r06-dependency-manifest
Status: ACTIVE IMPLEMENTATION TASK
Starting canonical main:
eb5b8cd58c7a7e0a52d293e62d91870532559177
```

## Objective

Audit dependencies actually imported by already accepted and merged production/test code through PRE-M6-R05 and reconcile `requirements.txt` so a clean project installation can run the accepted implementation/test suite without ad hoc manual dependency installs.

This is dependency-manifest maintenance only. It must not change scientific behavior, runtime architecture, accepted configuration semantics, or production/test logic.

## Read first

```text
1. MASTER_PROJECT_SPEC.md
2. AGENTS.md
3. PROJECT_STATE.md
4. DECISIONS.md
5. requirements.txt
6. accepted production/test code imports as needed for the audit
```

If any dependency choice would require a new scientific, architectural, environment, packaging, or reproducibility policy decision, stop and report it instead of inventing one.

## Authorized implementation files

```text
requirements.txt
```

No other production, test, governance, documentation, lockfile, environment, or workflow file is authorized for implementation under PRE-M6-R06.

## Requirements

1. Audit imports used by already accepted/merged code and tests through PRE-M6-R05.
2. Add only missing direct third-party runtime/test dependencies required by that accepted code.
3. At minimum, reconcile the already verified omissions:
   ```text
   pandas
   scikit-learn
   matplotlib
   ```
   if the audit confirms they remain direct requirements.
4. Preserve existing declared dependencies unless the audit proves one is erroneous; removal is not authorized merely for cleanup.
5. Do not add dependencies only because they are listed in the future approved technology stack.
6. Do not add `streamlit` unless accepted code/tests already import and require it; UI is currently NOT STARTED.
7. Do not add unrelated optional/development tooling.
8. Do not freeze exact package versions or introduce a new pinning policy under this task.
9. Do not create `requirements-dev.txt`, `pyproject.toml`, lockfiles, environment files, or packaging metadata.
10. Do not modify code/tests to work around missing dependencies.
11. Do not implement M6 or any end-to-end EEG replay/integration behavior.
12. Do not add logging/provenance/artifact-persistence infrastructure or unified decoder/runtime interfaces.

## Verification

Codex must use a clean environment if available and report the exact commands actually executed.

Minimum verification target:

```text
install dependencies from requirements.txt
run full pytest suite
```

If full verification cannot be executed because of host/environment/network limitations, report `BLOCKED` or `PARTIAL` accurately and provide the exact failure. Do not fabricate pass counts.

The audit report must also identify:

```text
all third-party imports reviewed
which packages were already declared
which packages were missing
which package names differ from import names (for example sklearn -> scikit-learn)
why each added dependency is required by accepted code/tests
```

## Acceptance criteria

PRE-M6-R06 may be accepted only if:

```text
requirements.txt reflects direct third-party dependencies of accepted code/tests through PRE-M6-R05
+
no future/unimplemented-module dependency is added merely in anticipation
+
no new version-freezing/environment policy is invented
+
no production/test behavior is changed
+
verification is honestly reported
+
M6 remains not started
```

## Stop conditions

Stop and report instead of expanding scope if:

- determining the correct dependency requires a new packaging/version/reproducibility policy;
- dependency installation exposes a code defect requiring source/test modification;
- an accepted module depends on an undeclared optional backend whose inclusion is scientifically/architecturally ambiguous;
- clean verification requires modifying files outside `requirements.txt`;
- implementation would begin M6 or any other remediation item.

## Completion report

Report:

```text
Status:
Starting main SHA:
Task branch:
Files modified:
Dependencies audited:
Dependencies added:
Dependencies intentionally not added:
Exact install command:
Tests executed:
Test results:
Known warnings:
Known limitations:
Open blockers:
Candidate commit SHA:
Suggested commit message:
```

After completing PRE-M6-R06:

```text
STOP
```

Do not begin another remediation item or M6 automatically.

---

# 2. CLOSED TASK RECORD — PRE-M6-R05

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

PRE-M6-R05 is complete. PRE-M6-R06 is separately authorized above. M6 is not started.

---

# 3. CLOSED TASK SUMMARY

Accepted tasks before PRE-M6-R06 include M1-T01 through M1-T10, M4-T01 through M4-T05, M5-T01 through M5-T04, and PRE-M6-R01 through PRE-M6-R05.

The authoritative details of earlier closed tasks remain in Git history and `PROJECT_STATE.md`.

---

# 4. NEXT ARCHITECTURAL BOUNDARY

The next project boundary after all Pre-M6 remediation is accepted is offline EEG-to-full-system integration, but no M6 implementation is authorized by PRE-M6-R06.

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

# 5. UNRESOLVED EXPERIMENTAL DECISIONS

The following remain unresolved and are not authorized by this task:

```text
U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
```
