# 22_AI_DEVELOPMENT_WORKFLOW.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### AI-Assisted Development Governance, ChatGPT/Codex Roles, Review Loop, Change Control, and Scientific Accountability

**Document ID:** K-01  
**Document class:** AI-Assisted Development / Governance & Workflow  
**Authority level:** Subordinate to all Master Authority, Scientific, Architecture, Implementation, Experimental, Testing, and Validity documents  
**Status:** Authoritative workflow baseline for the current **ChatGPT + Project Owner + Codex + Git/GitHub** development model  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. PURPOSE AND AUTHORITY

This document defines how the project is developed using AI-assisted software engineering while preserving:

- scientific correctness;
- explicit human approval;
- narrow implementation scope;
- reproducibility;
- traceability;
- independent technical review;
- and disciplined change control.

The current workflow is:

```text
ChatGPT
→ Project Owner
→ Codex
→ Tests / Results
→ ChatGPT Review
→ Project Owner Approval
→ Git / State Update
```

If this document conflicts with a higher-authority project document, the higher-authority document wins.

---

# 1. CORE DEVELOPMENT PRINCIPLE

The project must not be built as:

```text
one giant prompt
→ one giant AI-generated codebase
→ assume it works
```

The approved process is:

```text
DESIGN
→ APPROVE
→ IMPLEMENT
→ RUN
→ VERIFY
→ INTEGRATE
→ REVIEW
→ COMMIT
→ NEXT
```

Every meaningful step should produce inspectable evidence.

---

# 2. DEVELOPMENT ROLES

The project has four operational roles.

---

# 3. CHATGPT — PROJECT BRAIN / RESEARCH DIRECTOR

ChatGPT is responsible for:

- scientific reasoning;
- neuroscience interpretation;
- probability and Bayesian methodology;
- system architecture;
- experiment design;
- evaluation design;
- identifying unresolved assumptions;
- reviewing implementation evidence;
- reviewing code, tests, logs, and outputs where needed;
- generating narrow Codex implementation tickets;
- maintaining cross-document consistency;
- identifying scientific invalidity even when software appears to work.

ChatGPT must not silently finalize unresolved scientific choices.

---

# 4. PROJECT OWNER — FINAL AUTHORITY

The Project Owner is responsible for:

- approving or rejecting proposed changes;
- choosing between unresolved alternatives;
- deciding final project scope;
- reviewing important outputs;
- approving scientific methodology;
- approving architecture changes;
- approving final claims;
- deciding whether a module is accepted.

The Project Owner has final authority.

No AI system independently owns the scientific direction of the project.

---

# 5. CODEX — IMPLEMENTATION ENGINEER

Codex is responsible for:

- reading approved project specifications;
- editing repository files;
- implementing approved functionality;
- writing tests;
- running tests;
- debugging;
- running approved experiments;
- creating reproducible artifacts;
- reporting exact files changed;
- reporting exact commands and outputs;
- reporting blockers honestly.

Codex is **not** authorized to independently redefine:

- project scope;
- methodology;
- scientific assumptions;
- model semantics;
- experimental comparisons;
- threshold policies;
- safety policy;
- goal-mapping logic;
- unresolved parameter choices.

---

# 6. GIT / GITHUB — PERSISTENT TECHNICAL SOURCE OF TRUTH

Git/GitHub preserves:

- implementation history;
- accepted code;
- configuration history;
- experiment state;
- fixes;
- regressions;
- documentation updates;
- state-file changes;
- scientific decision implementation history.

Conversation history is useful, but the repository is the persistent technical truth.

---

# 7. LIVE PROJECT MEMORY FILES

The following files form persistent operational memory:

```text
PROJECT_STATE.md
CURRENT_TASK.md
DECISIONS.md
RESEARCH_LOG.md
EXPERIMENT_LOG.md
TODO.md
```

Each has a distinct role.

---

# 8. `PROJECT_STATE.md`

Purpose:

> Record what is actually true about the project right now.

It should contain:

```text
current milestone
implemented modules
tested modules
manual verification status
known blockers
latest accepted commit
latest artifacts
current next candidate task
```

Do not mark a feature complete because code exists.

Completion requires the relevant verification.

---

# 9. `CURRENT_TASK.md`

Purpose:

> Hold exactly one active implementation ticket.

It should define:

```text
Task ID
Objective
Read First
Allowed Files
Forbidden Files
Inputs
Outputs
Requirements
Scientific Constraints
Tests
Manual Checks
Acceptance Criteria
Stop Conditions
Completion Report Format
```

Parallel tasks are allowed only when interfaces and file ownership are explicitly separated.

---

# 10. `DECISIONS.md`

Purpose:

> Record explicit approved scientific and architectural decisions.

Typical decisions include:

```text
EEG filter band
EEG reference
epoch interval
T0 handling
calibration method
calibration split
goal-selection protocol
Bayesian likelihood semantics
confidence thresholds
adaptation mechanism
risk representation
risk λ
hazard threshold
cross-subject protocol
```

An unresolved option must not be written as an approved decision.

---

# 11. `RESEARCH_LOG.md`

Purpose:

> Preserve research findings, alternatives, literature notes, and unresolved reasoning.

It may contain:

- papers reviewed;
- methodological alternatives;
- rejected options;
- questions;
- scientific rationale;
- evidence supporting future decisions.

`RESEARCH_LOG.md` does not by itself authorize implementation.

---

# 12. `EXPERIMENT_LOG.md`

Purpose:

> Record experiments that were actually executed.

Each experiment should preserve:

```text
experiment ID
date
objective
subjects/runs
split
config
model
checkpoint
seed
Git commit
metrics
artifacts
validity status
notes
```

Do not record hypothetical results as completed experiments.

---

# 13. `TODO.md`

Purpose:

> Track work that may need to be done later.

Suggested categories:

```text
Core
Blocked
Validation
Documentation
Optional
Future
```

A TODO entry is not automatically approved scope.

---

# 14. STANDARD DEVELOPMENT LOOP

The standard implementation loop is:

```text
1. ChatGPT analyzes the next problem.
2. ChatGPT creates a narrow implementation ticket.
3. Project Owner approves, edits, or rejects the ticket.
4. Codex implements only the approved scope.
5. Codex runs required tests and commands.
6. Codex reports exact implementation evidence.
7. ChatGPT independently reviews important code/tests/results.
8. Project Owner accepts or requests correction.
9. Git/state files are updated.
10. Only then move to the next task.
```

---

# 15. WHY CODEX OUTPUT REQUIRES REVIEW

Code can execute successfully while remaining scientifically invalid.

Examples:

```text
CSP fitted before data split
```

```text
calibration fitted using final test labels
```

```text
decoder P(class|EEG) treated directly as P(E|G)
```

```text
confidence threshold invented inside source code
```

```text
T1/T2 meaning accidentally reversed
```

Therefore a Codex completion message is not sufficient proof.

---

# 16. NARROW TASK PRINCIPLE

Tasks should be intentionally bounded.

Good:

```text
Implement the PhysioNet EEGBCI loader only.
```

Bad:

```text
Implement the complete BCI, Bayes, simulation, UI, and experiments.
```

Narrow tasks reduce:

- hidden assumptions;
- debugging cost;
- interface drift;
- scientific scope creep;
- regression risk.

---

# 17. MODULE COMPLETION RULE

The normal module cycle is:

```text
implement
→ run
→ test
→ manually verify where needed
→ review
→ accept
→ commit
→ next
```

Do not create several scientifically dependent modules before validating upstream outputs.

---

# 18. APPROVED PARALLEL DEVELOPMENT TRACKS

Parallel development is allowed when interfaces are stable.

## EEG Track

```text
loader
→ preprocessing
→ epochs
→ CSP/LDA
→ EEGNet
→ calibration
```

## Cognitive Track

```text
synthetic likelihood
→ Bayesian core
→ entropy
→ adaptation interface
```

## Autonomy Track

```text
artificial approved goal
→ 2D environment
→ A*
→ safety
```

Integration occurs later through defined contracts.

---

# 19. CODEX TASK FORMAT

A Codex implementation ticket should use:

```text
TASK ID:
MODULE:
OBJECTIVE:

READ FIRST:

ALLOWED FILES:
FORBIDDEN FILES:

INPUTS:
OUTPUTS:

REQUIREMENTS:
SCIENTIFIC CONSTRAINTS:

TESTS:
MANUAL CHECKS:

ACCEPTANCE CRITERIA:
STOP CONDITIONS:

AFTER COMPLETION REPORT:
```

---

# 20. READ-FIRST RULE

Every Codex task should begin with:

```text
Read MASTER_PROJECT_SPEC.md first.
```

Then list the minimum relevant project documents.

Example:

```text
Read:
MASTER_PROJECT_SPEC.md
06_DATASET_AND_DATA_PIPELINE.md
CURRENT_TASK.md
```

Do not require every document to be reread for every task unless needed.

---

# 21. FILE-BOUNDARY RULE

Every task should specify the files Codex may modify.

Example:

```text
Allowed:
src/eeg/loader.py
tests/test_loader.py

Forbidden:
src/models/*
src/cognition/*
src/autonomy/*
```

If another file must change:

```text
STOP
→ explain why
→ request approval
```

---

# 22. SCIENTIFIC STOP CONDITIONS

Codex must stop rather than guess when the active task requires an unresolved scientific decision.

Current important unresolved areas include:

- exact EEG band-pass filter;
- EEG reference;
- epoch interval;
- baseline correction;
- artifact handling;
- T0 handling;
- final processed-data format;
- final train/validation/test protocol;
- final cross-subject protocol;
- calibration method;
- calibration fitting partition;
- binary EEG-to-multi-goal interaction protocol;
- decoder-probability → Bayesian likelihood construction;
- Bayesian stopping/commitment rule;
- autonomy confidence thresholds;
- exact adaptation mechanism;
- environmental risk values;
- risk weight \(\lambda\);
- prohibited-hazard threshold;
- final A/B/C/D component semantics.

---

# 23. TECHNICAL STOP CONDITIONS

Codex should also stop when:

- source data are invalid;
- required dependency cannot be resolved safely;
- an interface contract is missing;
- an implementation requires unauthorized architectural redesign;
- a test exposes upstream scientific inconsistency;
- a checkpoint/data format is incompatible;
- required files are missing or contradictory.

---

# 24. BLOCKED IS A VALID STATUS

Use:

```text
PASS
PARTIAL
BLOCKED
FAIL
```

`BLOCKED` means progress cannot continue validly without an approval, dependency, or scientific decision.

Example:

```text
Goal-Evidence Adapter
Status: BLOCKED

Reason:
The EEG class-probability → goal-likelihood semantics have not been approved.
```

This is correct project behavior.

---

# 25. CODEX COMPLETION REPORT

After every task, Codex should report:

```text
1. Status
2. Files created
3. Files modified
4. Exact implementation completed
5. Tests added
6. Tests executed
7. Test results
8. Exact commands used
9. Output / artifact paths
10. Manual checks required
11. Known limitations
12. Open blockers
13. Suggested Git commit message
```

---

# 26. NO “DONE” WITHOUT EVIDENCE

A task is not complete because Codex states that it is done.

Completion requires:

```text
implementation
+
tests where practical
+
actual test execution
+
manual checks where required
+
acceptance criteria
```

---

# 27. CHATGPT REVIEW CHECKLIST

For scientifically important tasks, ChatGPT should review:

1. Does implementation match approved architecture?
2. Were unresolved choices preserved?
3. Are labels correct?
4. Is class order explicit?
5. Is there leakage?
6. Are equations implemented correctly?
7. Are interfaces stable?
8. Are tests scientifically meaningful?
9. Were tests actually executed?
10. Are outputs real?
11. Did scope expand?
12. Are claims accurate?

---

# 28. PROJECT OWNER REVIEW

The Project Owner should manually inspect critical outputs.

Examples:

- EEG metadata;
- annotations;
- montage;
- EEG plots;
- preprocessing outputs;
- model results;
- calibration curves;
- Bayesian trajectories;
- 2D route behavior;
- safety behavior;
- final system comparisons.

The owner does not need to manually author every code module.

---

# 29. CHANGE-CONTROL WORKFLOW

Scientific or architectural changes follow:

```text
1. Problem identified
2. ChatGPT analyzes alternatives
3. Project Owner approves one option
4. DECISIONS.md updated
5. Master/spec updated if required
6. Codex ticket created
7. Codex implements
8. Tests execute
9. ChatGPT reviews
10. Project Owner accepts
11. Git/state updated
```

No unilateral redesign.

---

# 30. MASTER SPECIFICATION RULE

`MASTER_PROJECT_SPEC.md` is change-controlled.

Codex must not edit it merely because current implementation would be easier under different assumptions.

---

# 31. DOCUMENT CONFLICT RULE

If implementation reveals a conflict:

```text
identify conflict
→ determine authority
→ report
→ correct only after approval
```

Do not silently modify documentation to match generated code.

---

# 32. UNRESOLVED DECISION MARKERS

Use explicit states:

```text
TBD
UNRESOLVED
BLOCKED
```

Do not disguise unresolved science using arbitrary defaults.

---

# 33. AI-GENERATED CODE POLICY

AI-generated implementation is permitted.

Scientific credibility depends on:

```text
approved methodology
+
verification
+
testing
+
reproducibility
+
review
```

Manual typing is not the scientific standard.

Correct implementation is.

---

# 34. PROJECT OWNER DEVELOPMENT PHILOSOPHY

The project follows an AI-assisted rapid-build approach:

```text
implement efficiently using Codex
→ verify scientific correctness during development
→ integrate the system
→ deepen conceptual mastery afterward
```

However, critical methodology cannot be deferred.

During implementation, enough understanding is required to verify:

- inputs;
- outputs;
- labels;
- probability meaning;
- leakage;
- metrics;
- equations;
- module interfaces.

---

# 35. MINIMUM CONCEPTUAL UNDERSTANDING DURING BUILD

Before approving important modules, the Project Owner should understand:

## EEG

```text
what the dataset contains
what T1/T2 mean
what one epoch represents
```

## CSP/LDA

```text
spatial filtering
feature extraction
linear classification
```

## EEGNet

```text
EEG tensor input
class probability output
```

## Calibration

```text
accuracy ≠ probability reliability
```

## Bayesian inference

```text
prior × likelihood → posterior
```

## Uncertainty

```text
entropy measures belief concentration
```

## Shared autonomy

```text
proceed / confirm / defer / pause / stop
```

## Planning

```text
approved goal → route
```

## Safety

```text
planner proposes
→ safety authorizes
```

---

# 36. DEBUGGING WORKFLOW

When implementation fails:

```text
capture exact error
→ reproduce
→ isolate smallest cause
→ inspect relevant code/log
→ apply minimal fix
→ rerun failing test
→ rerun relevant regressions
```

Do not rewrite large portions unnecessarily.

---

# 37. ERROR REPORT FORMAT

Useful reports include:

```text
Command:
Expected:
Actual:
Error:
Relevant files:
Recent change:
Minimal reproduction:
```

Avoid vague reports such as:

```text
it doesn't work
```

---

# 38. EXPERIMENT EXECUTION WORKFLOW

For reportable experiments:

```text
freeze config
→ record Git commit
→ run experiment
→ save raw outputs
→ compute metrics
→ validate experiment
→ update EXPERIMENT_LOG
→ review results
```

Do not manually alter result values.

---

# 39. RESULT REVIEW WORKFLOW

ChatGPT should review:

- experiment configuration;
- split definitions;
- result tables;
- logs;
- plots;
- failure cases;
- metric definitions.

Questions:

```text
Is this experiment valid?
Is there leakage?
Is the comparison fair?
Does the metric mean what we claim?
Are failures visible?
Can the result be reproduced?
```

---

# 40. NO FABRICATED RESULTS

Neither ChatGPT nor Codex may invent:

```text
accuracy
F1
ECE
Brier Score
task success
wrong-goal reduction
safety improvement
latency
path efficiency
```

Synthetic numbers are allowed only in tests/examples.

---

# 41. NEGATIVE RESULTS

Negative or mixed results must be preserved.

Possible valid outcomes:

```text
CSP+LDA > EEGNet
calibration adds little
Bayesian accumulation adds latency
adaptation harms some subjects
safety increases path length
full system does not dominate all metrics
```

Do not tune experiments until a desired conclusion appears.

---

# 42. EXPERIMENT INVALIDATION

An experiment should be marked invalid when:

- train/test leakage exists;
- wrong event labels were used;
- test data influenced tuning;
- class order was wrong;
- wrong config loaded;
- required provenance is missing;
- implementation was scientifically incorrect.

Invalid results must not support final claims.

---

# 43. CLAIM APPROVAL WORKFLOW

Before adding a claim to:

- README;
- portfolio;
- resume;
- technical report;

verify:

```text
claim
→ experiment ID
→ valid methodology
→ metric
→ artifact
→ reproducibility
```

If this chain is incomplete, the claim is not approved.

---

# 44. OPTIONAL TECHNOLOGY CONTROL

Optional technologies must not be added because they sound impressive.

Examples:

```text
ROS2
Gazebo
PPO
SNN
multiclass EEG
live EEG
physical robot
active inference
```

To add one:

1. define its purpose;
2. identify the gap it solves;
3. confirm it improves project value;
4. obtain Project Owner approval;
5. update specifications;
6. create a narrow Codex task.

---

# 45. PROHIBITED UNNECESSARY COMPLEXITY

Do not introduce:

```text
runtime LLM
RAG
OpenAI/Gemini API
AWS/cloud architecture
Kubernetes
blockchain
IoT hardware
unrelated computer vision
complex microservices
3D simulation
mobile app
```

unless the project scope is explicitly changed.

---

# 46. CURRENT CORE DATASET AND TASK

Current approved dataset:

```text
PhysioNet EEG Motor Movement/Imagery Database
EEGMMIDB / EEGBCI
```

Initial runs:

```text
4
8
12
```

Run semantics:

```text
T0 = rest
T1 = imagined left fist
T2 = imagined right fist
```

Initial decoding task:

```text
Left vs Right motor imagery
```

Core EEG is prerecorded.

Approved interface wording:

```text
Offline EEG Replay
Simulated Real-Time BCI
```

---

# 47. CURRENT CORE ARCHITECTURE

```text
EEG
→ preprocessing
→ CSP+LDA / EEGNet
→ probability
→ calibration
→ goal evidence
→ Bayesian posterior
→ entropy
→ shared autonomy
→ approved goal
→ A*
→ safety
→ 2D SAR environment
→ evaluation
```

---

# 48. HUMAN AUTHORITY RULE

The permanent system principle is:

> **Human determines WHAT intended objective is selected. AI determines HOW to achieve it safely.**

Human must retain:

```text
confirm
override
pause
stop
```

High model confidence cannot bypass explicit human stop or hard safety.

---

# 49. CURRENT FIRST IMPLEMENTATION TASK

The first coding task remains:

> **Read `MASTER_PROJECT_SPEC.md` first. We are starting Milestone 1 only. Implement a clean MNE-Python data loader for the PhysioNet EEGBCI motor-imagery dataset. Initially support configurable subject IDs and runs 4, 8 and 12. Requirements: download through MNE utilities; cache locally; load EDF files; standardize channel names; attach the appropriate montage; print subject, channel count, sampling frequency, duration and annotations; add basic validation/error handling; write unit tests where practical; do not implement preprocessing or modelling yet. After coding, tell me: (1) files created/modified, (2) installation requirements, (3) exact command to run, (4) expected output, (5) what I should manually check. Do not continue beyond the loader.**

---

# 50. GIT COMMIT DISCIPLINE

After an accepted task:

```text
commit
```

before beginning a major next task.

Good commit examples:

```text
Implement EEGBCI loader
Add EEG epoch extraction
Add CSP-LDA baseline
Add Bayesian belief filter
Add A-star planner
```

---

# 51. PROJECT STATE UPDATE RULE

After every accepted task, update:

```text
PROJECT_STATE.md
```

with:

- implementation status;
- verification status;
- blockers;
- artifact paths;
- latest commit;
- next candidate task.

---

# 52. CURRENT TASK UPDATE RULE

When a task completes:

```text
CURRENT_TASK.md
```

should no longer present that task as active.

Replace or archive it according to repository practice.

---

# 53. DECISION LOGGING RULE

When a scientific choice is explicitly approved:

```text
DECISIONS.md
```

should record it before or alongside implementation.

Do not allow implementation code to become the only record of a decision.

---

# 54. RESEARCH LOGGING RULE

If a decision depends on research:

```text
RESEARCH_LOG.md
```

should preserve the supporting evidence, alternatives, and reasoning.

---

# 55. EXPERIMENT LOGGING RULE

Every reportable experiment should be recorded in:

```text
EXPERIMENT_LOG.md
```

with identity, config, commit, artifacts, and validity status.

---

# 56. CODEX RESPONSE DISCIPLINE

Codex completion reports should distinguish:

```text
Implemented
Tested
Not Tested
Blocked
Assumed
```

For scientific parameters:

```text
Assumed
```

should normally be empty.

---

# 57. CHATGPT RESPONSE DISCIPLINE

ChatGPT should clearly distinguish:

```text
APPROVED
RECOMMENDED
UNRESOLVED
OPTIONAL
BLOCKED
```

Do not blur a suggestion into an approved project decision.

---

# 58. TEST-ONLY VALUES

Unit tests may use arbitrary synthetic constants.

Examples:

```text
prior = [0.5, 0.5]
likelihood = [0.8, 0.2]
risk_lambda = 5
```

These are verification fixtures.

They must not silently migrate into final scientific configuration.

---

# 59. AI REVIEW OF AI-GENERATED IMPLEMENTATION

The workflow deliberately separates generation from scientific review.

Codex can implement quickly.

ChatGPT can independently review.

The Project Owner provides final approval.

The strongest verification comes from:

```text
approved architecture
+
tests
+
actual execution
+
manual checks
+
independent review
```

No single AI system is treated as infallible.

---

# 60. SCIENTIFIC SOURCE RULE

For literature-dependent methodology:

- prefer primary or authoritative sources;
- record important references;
- distinguish published evidence from project-specific choice;
- do not use unsupported model memory as the sole basis for critical parameters.

---

# 61. MANUAL VERIFICATION CANNOT BE ELIMINATED

Automated tests do not replace all manual scientific checks.

Manual inspection is especially important for:

- EEG channel/montage correctness;
- event labels;
- signal plots;
- preprocessing behavior;
- calibration diagrams;
- posterior trajectories;
- route/safety behavior;
- dashboard state.

---

# 62. PERFORMANCE CLAIM RULE

Do not use metrics from:

```text
smoke tests
tiny development subsets
training data
temporary validation runs
synthetic tests
```

as final headline performance.

Only approved final evaluation experiments support project claims.

---

# 63. CROSS-SESSION CONTINUITY

The repository must contain enough information to resume work in a new ChatGPT/Codex session.

Priority continuity files:

```text
MASTER_PROJECT_SPEC.md
PROJECT_STATE.md
CURRENT_TASK.md
DECISIONS.md
AGENTS.md
```

These should minimize reliance on conversation memory.

---

# 64. CODEX REPOSITORY INSTRUCTION FILE

The permanent repository-level Codex instruction file should be:

```text
AGENTS.md
```

It should contain:

- authority hierarchy;
- Codex role;
- what to read first;
- current scope;
- stop conditions;
- no-fabrication rules;
- testing requirements;
- task-completion format;
- state-file update rules;
- change-control restrictions.

`AGENTS.md` is the implementation-agent instruction authority.

---

# 65. DEVELOPMENT COMPLETION STANDARD

The project is ready for final reporting only when:

1. architecture matches approved specifications;
2. all core modules are implemented;
3. tests pass;
4. manual scientific review gates pass;
5. real prerecorded EEG reaches the end-to-end pipeline;
6. experiments are reproducible;
7. A/B/C/D comparisons are completed;
8. ablations/failure cases are preserved;
9. remaining unresolved items are explicitly documented;
10. final claims are evidence-backed.

---

# 66. WORKFLOW ACCEPTANCE CRITERIA

The AI-assisted workflow is functioning correctly when:

1. ChatGPT owns scientific reasoning/review;
2. Project Owner retains final approval;
3. Codex implements narrow approved tasks;
4. Git/GitHub preserves technical truth;
5. unresolved scientific decisions block implementation;
6. allowed/forbidden file boundaries are respected;
7. tests are actually run;
8. completion reports contain evidence;
9. important implementation receives independent review;
10. state files remain current;
11. approved decisions are logged;
12. experiments preserve config/commit/artifacts;
13. scope changes require approval;
14. no fabricated results appear;
15. Codex does not silently redesign the project.

---

# 67. CURRENT WORKFLOW SUMMARY

The NeuroCognitive Shared Autonomy project uses a controlled **ChatGPT + Project Owner + Codex + Git/GitHub** workflow. ChatGPT acts as the Project Brain and Research Director, handling scientific reasoning, architecture, methodology, experiment design, and independent review. The Project Owner remains the final authority for all scientific, architectural, and scope decisions. Codex acts as the implementation engineer, executing narrow approved tasks, writing and running tests, debugging, and producing reproducible artifacts. Git/GitHub stores the persistent technical truth, while the live state files preserve current progress, decisions, research findings, experiment history, and future work. Scientific choices that remain unresolved must block implementation rather than being guessed. AI-assisted coding is therefore used for speed, while scientific accountability remains controlled through explicit approval, testing, reproducibility, and review.

---

# 68. NEXT GOVERNANCE ARTIFACT

The next governance artifact should be:

**`AGENTS.md` — Codex Repository Instructions**

It should convert this workflow into concise repository-level operational instructions that Codex reads while working in the codebase.
