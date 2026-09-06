# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.  
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub  
**Last updated:** 2026-09-06

---

# 1. STATUS AT A GLANCE

```text
Project phase:
M1-T01 through M1-T10 accepted and merged.
M4-T01 through M4-T05 accepted and merged.
M5-T01 through M5-T04 accepted and merged.
PRE-M6-R01 through PRE-M6-R06 accepted and merged.
Final Pre-M6 audit found widespread stale decision-state documentation contradictions.
PRE-M6-R07 was authorized for documentation reconciliation and stopped correctly when the change-controlled Master Specification was found to contain stale unresolved-state claims.
PRE-M6-R07A — Master Authority Reconciliation is now active.

Current module:
PRE-M6-R07A — Master Authority Reconciliation

Current task:
PRE-M6-R07A

Task status:
ACTIVE IMPLEMENTATION TASK

Canonical branch:
main

R07 parent authorization state before R07A amendment:
b3f506bdaf44072dcccccfc575822bbd5e654fab

Latest accepted task-branch software commit:
23196b8c11ccc800728a077a9ea4203b6be9ae7b

Final merged software commit through accepted R06:
f66dba3b78dc91abedaff1b24a3597c7748426df

Latest accepted software task:
PRE-M6-R06 — Accepted-Code Dependency Manifest Reconciliation

Latest approved scientific/architectural decision register entry:
D-073 — YAML Parser Dependency Contract

Latest valid reportable experiment:
None yet
```

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, certified safety, human-subject result, or end-to-end EEG-driven mission-execution claim is authorized.

---

# 2. ACCEPTED IMPLEMENTATION SEQUENCE

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
M1-T07 — Probability Calibration
M1-T08 — Bayesian Goal Inference
M1-T09 — Uncertainty / Shared-Autonomy Policy
M1-T10 — Adaptation / Prior Personalization
M4-T01 — 2D Search & Rescue Environment + Risk Map
M4-T02 — Risk-Aware A* Planner
M4-T03 — Safety Controller / Hard Constraint Enforcement
M4-T04 — Planner → Safety → Environment Execution Integration
M4-T05 — Controlled Replanning After Environment Change
M5-T01 — Human Command & Confirmation State Layer
M5-T02 — Shared-Autonomy / Human-Interaction Authorization Bridge
M5-T03 — Human-Authority-Aware Stepwise Navigation Runtime
M5-T04 — Stepwise Replacement-Snapshot Replanning Integration
PRE-M6-R01 — M4 Wrong-Terminal Route Protection: PASS / MERGED
PRE-M6-R02 — Human OVERRIDE Symbolic Goal Identity Correction: PASS / MERGED
PRE-M6-R03 — Environment Snapshot Immutability and Goal Registry Hardening: PASS / MERGED
PRE-M6-R04 — Adaptation Disabled-State Mutation Correction: PASS / MERGED
PRE-M6-R05 — Central Runtime Composition Configuration: PASS / MERGED
PRE-M6-R06 — Accepted-Code Dependency Manifest Reconciliation: PASS / MERGED
```

Total accepted implementation tasks: 25.

PRE-M6-R07/R07A are governance/documentation remediation and are not accepted implementation tasks yet.

---

# 3. CURRENT ACCEPTED RUNTIME STATE

```text
EEG loader/preprocessing/splits: PASS
CSP+LDA baseline: PASS
EEGNet / compact CNN: PASS
Probability calibration: PASS
Bayesian goal inference: PASS
Uncertainty/shared-autonomy policy: PASS
Adaptation / prior personalization: PASS
2D SAR environment + risk-aware A*: PASS
Safety controller: PASS
Planner -> safety -> environment integration: PASS
Controlled replanning: PASS
Human command/confirmation state: PASS
Shared-autonomy -> human authorization bridge: PASS
Fresh authorization -> stepwise navigation runtime: PASS
Replacement-snapshot stepwise replanning: PASS
Offline EEG -> full-system execution: NOT STARTED
UI: NOT STARTED
Reportable system experiments: NOT STARTED
```

Accepted authority remains `STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > shared-autonomy policy`; safety retains veto before every environment transition. D-069 stepwise execution and D-070 replacement-snapshot replanning remain authoritative.

---

# 4. ACCEPTED VERIFICATION STATE

M5-T04 independent verification:

```text
focused -> 105 passed in 0.52s
adjacent -> 143 passed in 0.36s
full -> 281 passed, 1 warning in 26.83s
```

PRE-M6-R06 verification:

```text
installation from requirements.txt: PASS
full pytest suite: 327 passed, 1 warning
warning: pre-existing PyTorch convolution padding warning
```

R07A is documentation-only; production test execution is not required unless an unexpected validation hook requires it.

---

# 5. PRE-M6-R07 AUDIT FINDING

The final Pre-M6 audit after R06 found material stale decision-state claims in implementation-facing documentation.

Original R07 scope covered:

```text
AGENTS.md
TODO.md
RESEARCH_LOG.md
docs/15_IMPLEMENTATION_BLUEPRINT.md
```

Codex correctly stopped because materially stale contradictions were also discovered outside that scope, including:

```text
MASTER_PROJECT_SPEC.md
README.md
docs/01_PROJECT_CONCEPT_AND_PROBLEM.md
docs/02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md
docs/03_SEARCH_AND_RESCUE_SCENARIO.md
docs/04_SYSTEM_ARCHITECTURE.md
docs/05_TECHNOLOGY_STACK.md
docs/06_DATASET_AND_DATA_PIPELINE.md
docs/07_NEUROSCIENCE_AND_BCI_FOUNDATIONS.md
docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md
docs/09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md
docs/10_BAYESIAN_GOAL_INFERENCE.md
docs/11_COGNITIVE_AND_ADAPTIVE_MODEL.md
docs/12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md
docs/13_AUTONOMOUS_PLANNING_AND_CONTROL.md
docs/14_SAFETY_CRITICAL_CONTROL.md
docs/17_EXPERIMENTAL_DESIGN.md
docs/19_TESTING_AND_VERIFICATION.md
docs/20_LIMITATIONS_ETHICS_AND_VALIDITY.md
docs/23_RESULTS_AND_ANALYSIS.md
docs/25_FUTURE_WORK.md
```

No R07 candidate was committed or pushed from that stopped attempt. Its four authorized files may contain local uncommitted edits in the Codex workspace, but those edits are not accepted repository state.

---

# 6. CURRENT PRE-M6-R07A REMEDIATION

The Project Owner explicitly approved:

```text
PRE-M6-R07A — Master Authority Reconciliation
using only already-approved decisions
with no new scientific or architectural changes
```

Authorized implementation file:

```text
MASTER_PROJECT_SPEC.md
```

Purpose:

Reconcile stale transfer-era/unresolved-state statements in the Master Specification with decisions already approved in `DECISIONS.md`, while preserving the Master as the project constitution rather than converting it into a live implementation-state file.

R07A may reflect already-approved decisions through D-073 where the Master currently contradicts them. It may not change decision semantics or create new ones.

The genuinely unresolved experimental decisions remain:

```text
U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
```

R07B — Secondary Documentation Reconciliation is NOT AUTHORIZED YET and may be defined only after R07A is reviewed and merged.

---

# 7. CLAIM / SCOPE BOUNDARIES

Preserve at least:

```text
public prerecorded EEG / offline replay / simulated real-time BCI only
no live EEG or hardware claim
human determines WHAT; AI determines HOW
accepted binary EEG evidence semantics; no fabricated direct K-goal decoder
accepted calibration/Bayesian/uncertainty/shared-autonomy/adaptation semantics
fresh navigation authorization remains required
D-069 stepwise navigation remains authoritative
D-070 event-bounded replacement-snapshot replanning remains authoritative
safety veto remains mandatory before every environment transition
no UI, reportable experiments, logging infrastructure, hardware integration, or M6 implementation without separate authorization
```

---

# 8. NEXT ACTION

Execute only PRE-M6-R07A on its separately authorized task branch after that branch is created from the amended governance state.

After R07A candidate implementation:

```text
review exact MASTER_PROJECT_SPEC.md diff
verify only already-approved decisions were reflected
verify U-034/U-035/U-036 remain unresolved
merge only after ChatGPT review/acceptance
then define R07B separately
```

Do not close Pre-M6 or begin M6 automatically.
