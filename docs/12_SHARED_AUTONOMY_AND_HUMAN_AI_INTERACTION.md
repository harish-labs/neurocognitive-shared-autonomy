# 12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Shared Autonomy, Human Authority, Interaction States, Confirmation, Override, Deferral, and Human–AI Control Specification

**Document ID:** G-01  
**Document class:** Autonomy & Human–AI Interaction / Shared-Autonomy Specification  
**Authority level:** Subordinate to the Master Authority Documents and all previously approved scenario, architecture, data, neuroscience, EEG/ML, calibration/uncertainty, Bayesian, and cognitive/adaptive specifications  
**Status:** Authoritative shared-autonomy baseline; confidence thresholds and the binary EEG-to-multiple-goal interaction protocol remain explicitly unresolved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND HUMAN-AUTHORITY RULE

This document defines how control is divided between the human operator and the autonomous system.

It must remain consistent with:

1. `MASTER_PROJECT_SPEC.md`
2. `01_PROJECT_CONCEPT_AND_PROBLEM.md`
3. `02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md`
4. `03_SEARCH_AND_RESCUE_SCENARIO.md`
5. `04_SYSTEM_ARCHITECTURE.md`
6. `05_TECHNOLOGY_STACK.md`
7. `06_DATASET_AND_DATA_PIPELINE.md`
8. `07_NEUROSCIENCE_AND_BCI_FOUNDATIONS.md`
9. `08_EEG_SIGNAL_PROCESSING_AND_ML.md`
10. `09_PROBABILITY_CALIBRATION_AND_UNCERTAINTY.md`
11. `10_BAYESIAN_GOAL_INFERENCE.md`
12. `11_COGNITIVE_AND_ADAPTIVE_MODEL.md`

If this document conflicts with a higher-authority document, the higher-authority document wins.

The core non-negotiable principle is:

> **Human determines WHAT objective is intended. AI determines HOW to achieve that objective safely.**

Human authority must not be weakened by:

- model confidence;
- Bayesian posterior;
- planner efficiency;
- adaptation;
- or UI convenience.

---

# 1. PURPOSE OF THIS DOCUMENT

This document answers:

> **What exactly does “shared autonomy” mean in this project?**

> **Which decisions belong to the human and which belong to the autonomous system?**

> **How does uncertainty change the amount of autonomous assistance?**

> **When should the system proceed, confirm, defer, pause, or stop?**

> **How are human corrections represented?**

> **What interactions must be logged and evaluated?**

---

# 2. DEFINITION OF SHARED AUTONOMY IN THIS PROJECT

Shared autonomy means that the human and the autonomous system contribute different parts of the control process.

The human provides or confirms the intended mission objective.

The autonomous system performs the technical execution required to reach that approved objective.

Conceptually:

```text
Human
    ↓
goal / intention
    ↓
Autonomous System
    ↓
safe route execution
```

This is not equal control over every action.

It is a division of responsibility.

---

# 3. HUMAN RESPONSIBILITIES

The human operator is responsible for:

- expressing intended goal-level choice through the approved EEG interaction protocol;
- confirming an inferred objective when confirmation is requested;
- rejecting an incorrect interpretation;
- overriding a wrong or undesired autonomous commitment;
- pausing the system;
- resuming when appropriate;
- emergency stopping the system;
- retaining final authority over mission intent.

The human is **not required** to:

- specify every grid movement;
- perform obstacle avoidance;
- calculate the shortest route;
- compute hazard cost;
- manage A*;
- validate every safe movement.

---

# 4. AUTONOMOUS-SYSTEM RESPONSIBILITIES

The autonomous system is responsible for:

- receiving probabilistic goal evidence;
- maintaining Bayesian belief;
- estimating uncertainty;
- deciding whether autonomy is justified;
- requesting confirmation when necessary;
- planning a route after goal approval;
- avoiding blocked paths;
- accounting for hazards;
- enforcing safety;
- replanning if needed;
- logging decisions;
- presenting interpretable system state.

The autonomous system must not:

- replace the user's goal because another goal is easier;
- ignore an override;
- ignore pause;
- ignore emergency stop;
- suppress uncertainty to keep moving.

---

# 5. WHY SHARED AUTONOMY IS NECESSARY

The selected EEG control signal is noisy and probabilistic.

Direct control would create a fragile mapping:

```text
one EEG prediction
→ one autonomous action
```

A single incorrect neural prediction could immediately produce an unintended action.

Shared autonomy instead creates:

```text
multiple EEG-derived evidence items
→ probabilistic goal belief
→ uncertainty check
→ human confirmation if needed
→ autonomous execution
```

This allows the system to absorb some uncertainty before acting.

---

# 6. GOAL-LEVEL CONTROL

The project uses **goal-level control**, not low-level joystick-style control.

The EEG interface may eventually determine:

- which currently available option is intended;
- which branch in a hierarchical choice is intended;
- or another approved abstract binary choice.

The autonomous system then handles:

- path planning;
- movement;
- obstacle avoidance;
- hazard avoidance;
- replanning.

This division is central to the project.

---

# 7. LOW-LEVEL EEG JOYSTICK CONTROL — NOT CORE

The project must not silently implement:

```text
Left imagery → move left one cell
Right imagery → move right one cell
```

as the main system.

That would contradict the current project philosophy and research question.

Such a design could be used only as a deliberately defined comparison baseline if later approved.

---

# 8. HUMAN AUTHORITY PRECEDENCE

The control hierarchy must satisfy:

```text
Emergency Stop
    ↓ highest authority

Human Override / Pause
    ↓

Safety Controller
    ↓

Shared-Autonomy Policy
    ↓

Planner / Autonomous Execution
```

No lower layer may override a higher-authority human safety action.

---

# 9. SHARED-AUTONOMY INPUTS

The shared-autonomy controller conceptually receives:

```text
IntentBelief
UncertaintyEstimate
current human state
current mission state
current approved goal, if any
adaptation state, if enabled
```

The controller must not receive hidden test truth.

---

# 10. SHARED-AUTONOMY OUTPUT

Conceptually:

```text
AutonomyDecision:
    mode
    candidate_goal
    approved_goal
    requires_confirmation
    reason
    confidence
    uncertainty
```

Possible modes:

```text
PROCEED
CONFIRM
DEFER
PAUSE
STOP
```

Exact threshold rules remain unresolved.

---

# 11. PROCEED

`PROCEED` means the system has sufficient permission and confidence under the approved policy to continue autonomous assistance.

This may require:

- sufficiently low uncertainty;
- sufficiently strong posterior support;
- no human objection;
- no safety block.

`PROCEED` does not mean:

- certainty;
- guaranteed correctness;
- unrestricted autonomy.

---

# 12. CONFIRM

`CONFIRM` means:

> The system has a plausible candidate goal but requires explicit human approval before commitment.

This state is useful under intermediate uncertainty.

A confirmation request should present enough information for the user to understand:

- what goal is being proposed;
- why confirmation is requested;
- whether confidence is ambiguous.

The UI should not overwhelm the user with unnecessary mathematical detail.

---

# 13. DEFER

`DEFER` means:

> The system should not commit to a goal yet.

Possible reasons:

- high uncertainty;
- insufficient evidence;
- conflicting evidence;
- missing valid goal mapping;
- invalid decoder output.

Possible actions:

- wait;
- request more EEG evidence;
- ask for human input;
- remain stationary.

---

# 14. PAUSE

`PAUSE` temporarily stops autonomous movement.

The system should:

- preserve relevant state;
- prevent new motion;
- record pause event;
- await explicit resume or another approved action.

Pause is reversible.

---

# 15. STOP

`STOP` terminates autonomous execution for the current episode or until explicitly reset.

Emergency stop must:

- halt motion immediately;
- override planner;
- override confidence;
- override adaptation;
- be logged.

---

# 16. RESUME

If resume is supported, it must be explicit.

The system should define whether resume:

- continues current path;
- replans;
- restarts intent inference;
- or requests confirmation.

The exact resume behavior is not yet locked.

---

# 17. HUMAN CONFIRMATION

Human confirmation means:

> The operator accepts the system's current candidate/approved objective.

It is an authority action.

It is not automatically:

- another EEG observation;
- another Bayesian likelihood update;
- a model-training label;
- an adaptation update.

Those uses require explicit design.

---

# 18. HUMAN OVERRIDE

Override means:

> The human rejects or replaces the current inferred/approved objective.

The system must:

- stop current commitment;
- respect the correction;
- update control state;
- log the event.

The exact Bayesian reset/adaptation consequence remains unresolved.

---

# 19. HUMAN PAUSE

Pause must be possible during autonomous execution.

The system should not advance the environment while paused.

Any queued autonomous action should not be executed until the state is explicitly resumed.

---

# 20. EMERGENCY STOP

Emergency stop is the strongest control action.

It must be available regardless of:

- EEG confidence;
- posterior;
- planner state;
- adaptation state.

Emergency stop should propagate immediately to:

```text
shared-autonomy controller
→ safety controller
→ execution layer
```

---

# 21. CONFIDENCE-DEPENDENT ASSISTANCE

The approved architecture uses uncertainty to regulate assistance.

Conceptually:

## Low uncertainty / high confidence

More autonomous assistance may be permitted.

## Intermediate uncertainty

Human confirmation may be required.

## High uncertainty

System should defer.

Exact boundaries are unresolved.

---

# 22. THRESHOLDS — NOT LOCKED

No numerical threshold is currently authoritative.

Earlier examples such as:

```text
> 0.8
0.6–0.8
< 0.6
```

were illustrative only.

Codex must not implement those as final constants without explicit approval.

---

# 23. CONFIDENCE POLICY MUST BE CONFIGURABLE

Conceptual configuration:

```yaml
shared_autonomy:
  policy_id: TBD
  proceed_rule: TBD
  confirm_rule: TBD
  defer_rule: TBD
```

The implementation should not scatter thresholds across UI callbacks or controller code.

---

# 24. CONFIDENCE POLICY VERSIONING

Once approved, every policy should have a stable identifier.

Example:

```text
shared_autonomy_policy_v001
```

Every experiment must record the policy version.

---

# 25. UNCERTAINTY IS NOT THE ONLY DECISION VARIABLE

Autonomy state may depend on:

- posterior confidence;
- entropy;
- human input;
- mission state;
- current safety state.

However, the final policy should remain simple and interpretable.

Do not add a large black-box policy network.

---

# 26. HUMAN CONTROL STATE

A conceptual human state may include:

```text
NONE
CONFIRMED
OVERRIDDEN
PAUSED
STOPPED
```

The exact enum implementation may differ.

Human state should be explicit rather than inferred indirectly from UI elements.

---

# 27. SHARED-AUTONOMY STATE MACHINE

Recommended conceptual states:

```text
WAITING_FOR_EEG
INFER_INTENT
UNCERTAIN
WAITING_FOR_CONFIRMATION
GOAL_APPROVED
NAVIGATING
PAUSED
STOPPED
COMPLETED
FAILED
```

This is consistent with the architecture specification.

---

# 28. STATE TRANSITIONS

Conceptual transitions:

```text
WAITING_FOR_EEG
→ INFER_INTENT

INFER_INTENT
→ UNCERTAIN
→ WAITING_FOR_CONFIRMATION
→ GOAL_APPROVED

UNCERTAIN
→ INFER_INTENT
→ WAITING_FOR_CONFIRMATION

WAITING_FOR_CONFIRMATION
→ GOAL_APPROVED
→ INFER_INTENT
→ PAUSED
→ STOPPED

GOAL_APPROVED
→ NAVIGATING

NAVIGATING
→ NAVIGATING
→ PAUSED
→ STOPPED
→ COMPLETED
→ FAILED
```

Exact transitions may be refined, but must preserve human authority.

---

# 29. INVALID TRANSITIONS

The system should reject invalid transitions.

Examples:

```text
STOPPED → NAVIGATING
```

without explicit reset.

```text
PAUSED → move
```

without resume.

```text
WAITING_FOR_CONFIRMATION → GOAL_APPROVED
```

without confirmation under a policy that requires it.

---

# 30. GOAL APPROVAL

A goal becomes approved when the shared-autonomy policy and human-control state permit it.

Approval may occur through:

- sufficiently strong evidence under the final policy;
- explicit confirmation;
- another approved path.

The exact approval rule remains unresolved.

---

# 31. GOAL APPROVAL MUST BE LOGGED

Every commitment should record:

```text
candidate goal
approved goal
posterior
entropy
policy state
human action
timestamp/update index
reason
```

This is essential for wrong-goal analysis.

---

# 32. BINARY EEG-TO-MULTIPLE-GOAL ISSUE — STILL UNRESOLVED

The interface currently receives binary Left/Right motor-imagery evidence.

The environment may contain more than two possible mission objectives.

Preserved options remain:

1. only two active choices at a time;
2. hierarchical binary selection;
3. abstract binary priority/choice;
4. future multiclass EEG.

No option is selected in this document.

The shared-autonomy UI must not hard-code a permanent mapping.

---

# 33. TWO-ACTIVE-CHOICE INTERFACE — CANDIDATE ONLY

One possible future interaction:

```text
Option A
Option B
```

are presented.

Then:

```text
Left MI → Option A
Right MI → Option B
```

This would be an explicit interface convention.

Status:

> candidate only.

---

# 34. HIERARCHICAL BINARY INTERFACE — CANDIDATE ONLY

A richer future protocol may use sequential binary decisions.

Example conceptually:

```text
Victim-related?
    Yes / No

If Yes:
    Victim A / Victim B
```

This can represent more goals using a binary EEG decoder.

Status:

> candidate only.

---

# 35. ABSTRACT BINARY CHOICE — CANDIDATE ONLY

The EEG signal may control an abstract decision such as:

```text
priority A
priority B
```

while autonomy handles the rest of the mission structure.

Status:

> candidate only.

---

# 36. MULTICLASS EEG — FUTURE OPTION

A multiclass BCI could directly support more goal options.

It is not part of the current locked core.

It must not be introduced merely to bypass the current binary interface decision.

---

# 37. HUMAN–AI INTERACTION PRINCIPLE

The interface should make the system's current state understandable.

The human should be able to answer:

- what goal does the system currently think I intend?
- how confident/uncertain is it?
- is it asking me to confirm?
- what route is it following?
- did safety intervene?
- can I stop it?

This supports interpretable shared autonomy.

---

# 38. EXPLAINABILITY LEVEL

The project does not require full explainable-AI methods.

Basic operational transparency is sufficient.

Examples:

```text
Current inferred goal: Victim A
Posterior: 0.72
State: Confirmation Required
Reason: Uncertainty above proceed threshold
```

Values shown must be actual outputs.

---

# 39. UI MUST NOT MISREPRESENT CERTAINTY

Avoid phrases like:

> “The system knows you want Victim A.”

Prefer:

> “Current inferred goal: Victim A.”

or:

> “Highest-probability goal hypothesis: Victim A.”

---

# 40. HUMAN WORKLOAD

Shared autonomy should reduce the need for continuous low-level control.

However, too many confirmation requests can create excessive human burden.

Therefore the project should measure:

- confirmation frequency;
- override frequency;
- pause frequency;
- intervention count.

---

# 41. HUMAN WORKLOAD TRADE-OFF

A very conservative system may:

- reduce wrong commitments;
- increase confirmations;
- increase latency.

A very permissive system may:

- reduce confirmations;
- increase wrong commitments.

The project must evaluate this trade-off rather than assume one extreme is best.

---

# 42. DECISION LATENCY

Decision latency may include:

- number of EEG evidence updates;
- simulated replay time;
- time until confirmation;
- time until goal approval.

The final metric definition belongs in the Metrics document.

---

# 43. HUMAN INTERVENTION METRICS

Potential measures include:

```text
number of confirmations
number of overrides
number of pauses
number of emergency stops
interventions per episode
```

The exact final metric set will be frozen later.

---

# 44. WRONG-GOAL COMMITMENT

A wrong-goal commitment occurs when the system approves a goal that differs from the controlled intended goal.

This is more important than a temporary incorrect posterior leader.

The commitment event must be explicit.

---

# 45. PREMATURE COMMITMENT

The system may commit before sufficient evidence has accumulated.

This can be evaluated by comparing:

- commitment time;
- posterior trajectory;
- later evidence;
- true goal.

Uncertainty-aware control is intended to reduce this risk.

---

# 46. EXCESSIVE DEFERRAL

The opposite failure is:

```text
system remains uncertain
→ never acts
```

This may produce high safety but poor usefulness.

Therefore task success and latency must be evaluated alongside safety.

---

# 47. CONFIRMATION FATIGUE

If the system asks for confirmation too often, it may undermine the value of shared autonomy.

This is a conceptual HCI limitation.

The current offline simulation does not measure real psychological fatigue unless a human-subject study is later added.

Therefore final wording should be careful:

> “confirmation burden”

rather than claiming measured cognitive fatigue.

---

# 48. HUMAN-ERROR MODELLING — NOT CORE

The project does not currently simulate imperfect human confirmations as a core requirement.

If later introduced, the error model must be explicit.

Do not assume humans are always perfect in real deployment.

---

# 49. HUMAN RESPONSE TIME — NOT CORE

A real HCI study could measure response time.

The current project can measure simulated/system interaction timing.

It must not claim real human reaction-time findings unless actual participants are studied.

---

# 50. STREAMLIT ROLE

The Streamlit interface may provide:

- current EEG replay;
- decoder probabilities;
- posterior;
- entropy;
- current autonomy state;
- candidate goal;
- planned path;
- safety events;
- confirm button;
- override button;
- pause button;
- stop button.

The UI is a technical demonstration layer.

---

# 51. CORE LOGIC MUST BE HEADLESS

The same shared-autonomy controller must work without Streamlit.

Automated experiments should call the controller directly.

This prevents hidden UI-dependent science.

---

# 52. HUMAN-INTERACTION FILE

Suggested architecture:

```text
src/app/human_interface.py
```

Responsibilities:

- represent human commands;
- pass them into core controller;
- log action;
- prevent duplicate/invalid commands.

---

# 53. SHARED-CONTROLLER FILE

Approved architecture:

```text
src/autonomy/shared_controller.py
```

Responsibilities:

- consume belief;
- consume uncertainty;
- consume human state;
- apply approved policy;
- output autonomy decision.

It must not:

- decode EEG;
- train models;
- implement A*;
- bypass safety.

---

# 54. SHARED-AUTONOMY DATA CONTRACT

Conceptually:

```text
AutonomyDecision:
    mode
    candidate_goal
    approved_goal
    posterior_confidence
    uncertainty
    requires_confirmation
    reason
    policy_id
```

---

# 55. HUMAN ACTION DATA CONTRACT

Conceptually:

```text
HumanAction:
    action_type
    selected_goal
    timestamp
    selection_id
    source
```

Possible `action_type`:

```text
CONFIRM
OVERRIDE
PAUSE
RESUME
STOP
```

---

# 56. GOAL CANDIDATE VS APPROVED GOAL

These must remain separate.

## Candidate goal

The system's current leading interpretation.

## Approved goal

The goal permitted for autonomous execution.

A candidate is not automatically approved.

---

# 57. CONFIRMATION REQUEST CONTRACT

Conceptually:

```text
ConfirmationRequest:
    candidate_goal
    posterior_confidence
    uncertainty
    reason
    request_id
```

The UI may simplify displayed values, but the underlying record should remain.

---

# 58. OVERRIDE CONTRACT

An override should specify, where applicable:

```text
rejected_goal
corrected_goal
selection_id
reason/source
```

The corrected-goal field may depend on the final interaction protocol.

---

# 59. PAUSE CONTRACT

Pause should record:

```text
episode
current goal
current position
current path
time/update
```

so the system can resume consistently if supported.

---

# 60. EMERGENCY STOP CONTRACT

Stop should record:

```text
episode
reason
current state
current position
goal
time
```

Execution must halt.

---

# 61. SAFETY INTERACTION

Shared autonomy determines whether the system is allowed to assist.

Safety determines whether a proposed action is allowed.

Sequence:

```text
goal approved
→ planner
→ proposed action
→ safety
→ execute/reject
```

A high-confidence goal does not bypass safety.

---

# 62. PLANNING INTERACTION

Once a goal is approved, the planner receives:

```text
current state
approved goal
risk/obstacle map
```

The planner does not use raw EEG evidence.

---

# 63. REPLANNING AND HUMAN AUTHORITY

If a route changes because of hazards, the autonomous system may replan without asking the human to reselect the same goal, unless the replanning meaningfully changes mission semantics.

The human still may override or stop.

---

# 64. GOAL CHANGE

If the human changes intended mission objective, the current approved goal should be invalidated.

The exact Bayesian reset and re-selection flow remains unresolved.

This should be handled explicitly rather than treating the old goal as active.

---

# 65. ADAPTATION INTERACTION

Adaptation may later modify:

- prior;
- reliability;
- thresholds.

The shared-autonomy controller consumes the resulting parameters.

Adaptation must not directly execute a human action.

---

# 66. ADAPTATION CANNOT REMOVE CONFIRMATION RIGHTS

Even if the system learns that a subject is highly reliable, the human must retain:

- override;
- pause;
- stop.

---

# 67. ADAPTATION AND THRESHOLDS

If threshold adaptation is selected later:

```text
adaptation
→ policy parameters
→ shared controller
```

The controller should record which threshold version was active.

---

# 68. SYSTEM A — DIRECT CONTROL

In the A/B/C/D framework:

System A is the simplest baseline.

Conceptually:

```text
decoder output
→ direct decision
```

This condition lacks the full shared-autonomy reasoning.

The exact safety treatment must be defined in the Experimental Design document.

---

# 69. SYSTEM B — CONFIDENCE-AWARE CONTROL

Conceptually:

```text
decoder
→ confidence/uncertainty
→ act or defer
```

No sequential Bayesian accumulation.

This isolates the value of confidence-aware behavior.

---

# 70. SYSTEM C — BAYESIAN SHARED AUTONOMY

Conceptually:

```text
EEG evidence
→ Bayesian goal inference
→ autonomous navigation
```

The precise inclusion of confirmation/uncertainty/safety will be frozen in Experimental Design.

---

# 71. SYSTEM D — FULL SYSTEM

Conceptually:

```text
EEG
+ calibration
+ Bayesian inference
+ uncertainty
+ shared autonomy
+ safety
+ adaptation
```

This is the intended full architecture.

---

# 72. SHARED-AUTONOMY ABLATION

The project should support controlled removal of:

- uncertainty gating;
- confirmation;
- adaptation;
- Bayesian inference.

This allows the contribution of each element to be measured.

---

# 73. FAILURE CASES — HUMAN–AI INTERACTION

The project should support analysis of:

## Wrong confirmation request

System proposes wrong goal.

## Excessive confirmation

System asks for confirmation too often.

## Missed uncertainty

System proceeds despite ambiguous posterior.

## Ignored override

System fails to respect correction.

## Ignored pause

System continues movement while paused.

## Ignored stop

Critical failure.

## Goal-state mismatch

UI shows one goal while controller uses another.

## Stale confirmation

Old confirmation applied to a new selection cycle.

---

# 74. STALE ACTION PROTECTION

Human actions should be associated with:

```text
request_id
selection_id
episode_id
```

where appropriate.

This prevents a delayed confirmation from approving the wrong later goal.

---

# 75. DOUBLE-CLICK / DUPLICATE ACTION PROTECTION

The UI should avoid applying the same confirmation/override multiple times.

Duplicate commands should be idempotent where possible or rejected clearly.

---

# 76. HUMAN ACTION LOGGING

Every human action should record:

```text
episode
selection
action type
candidate goal
approved/corrected goal
posterior
entropy
timestamp/update
controller state
```

This is important for HCI metrics.

---

# 77. SYSTEM DECISION LOGGING

Every shared-autonomy decision should record:

```text
mode
candidate goal
approved goal
posterior confidence
entropy
threshold/policy
reason
human state
```

---

# 78. REPRODUCIBILITY

A shared-autonomy run must be reconstructable from:

```text
belief trajectory
uncertainty trajectory
policy version
human-action sequence
adaptation state
environment state
Git commit
experiment config
```

---

# 79. HUMAN-INTERACTION SIMULATION

Because the project is not currently a human-subject study, automated experiments may simulate human actions.

Examples:

```text
if system candidate matches controlled intended goal
→ simulated confirm

if candidate is wrong
→ simulated override
```

Any such simulator must be explicit.

It must not be called actual human behavior.

---

# 80. HUMAN-IN-THE-LOOP DEMO VS AUTOMATED EXPERIMENT

The project may have:

## Demo mode

Real user clicks:

- confirm;
- override;
- pause;
- stop.

## Automated experiment mode

Human behavior is simulated according to an explicit rule.

Results from the automated mode should be labeled appropriately.

---

# 81. NO HUMAN-SUBJECT CLAIM

Without recruited participants, the project must not claim:

- measured usability;
- cognitive workload;
- trust;
- user satisfaction;
- real human reaction times.

It may claim:

- human-authority controls implemented;
- intervention frequency in simulation;
- simulated confirmation burden.

---

# 82. FUTURE HCI STUDY — OPTIONAL

A future extension could evaluate:

- usability;
- trust;
- workload;
- confirmation burden;
- user preference.

This would require a separate study design and, depending on context, ethics approval.

Not part of current core.

---

# 83. INTERFACE SIMPLICITY

The UI should prioritize:

```text
clarity
control
state visibility
```

over visual sophistication.

The project does not require:

- 3D models;
- cinematic animation;
- game UI;
- complex dashboards.

---

# 84. WHAT THE HUMAN SHOULD SEE

Minimum useful technical information:

```text
current candidate goal
current approved goal
current system state
current uncertainty/confidence
current agent position/path
safety warning/intervention
available human controls
```

---

# 85. WHAT THE HUMAN DOES NOT NEED TO SEE

The user does not need raw internal structures such as:

- model tensors;
- source-code objects;
- raw likelihood vectors;
- full debug logs.

Those remain available to the technical evaluator.

---

# 86. HCI EXPLANATION STYLE

Prefer concise explanations:

> “Confidence is uncertain. Confirmation required.”

rather than:

> “Posterior entropy exceeded 0.684 nats because...”

The technical dashboard may optionally expose detailed values separately.

---

# 87. INTERPRETABILITY VS AUTOMATION

The system should make its reason for defer/confirm visible enough for inspection.

This supports trustworthy evaluation.

However, the project does not claim measured user trust.

---

# 88. ERROR STATES

The UI/controller should clearly handle:

```text
No valid EEG evidence
Invalid posterior
No goal mapping
No path
Safety block
Paused
Stopped
```

The system should not silently continue with stale state.

---

# 89. NO-PATH CONDITION

If the planner reports no path:

- do not reinterpret intent;
- do not choose a different goal silently;
- report failure;
- allow human intervention.

The goal remains the human's objective.

---

# 90. SAFETY BLOCK CONDITION

If safety rejects a planned action:

- log rejection;
- request replanning;
- keep human informed if useful.

Do not silently remove safety constraints.

---

# 91. UNCERTAINTY BLOCK CONDITION

If uncertainty is too high under the final policy:

- no autonomous goal commitment;
- defer or confirm.

Exact policy unresolved.

---

# 92. HUMAN OVERRIDE AFTER NAVIGATION STARTS

The human may override even after movement begins.

The system should:

- halt or safely transition;
- invalidate current goal if needed;
- re-enter selection/control state;
- log the event.

Exact restart semantics remain unresolved.

---

# 93. EMERGENCY STOP DURING NAVIGATION

Emergency stop should immediately prevent further environment steps.

This must be tested.

---

# 94. UNIT TESTS — SHARED CONTROLLER

Once policy is approved, tests should cover:

- high-confidence proceed;
- intermediate confirmation;
- low-confidence defer;
- human confirm;
- override;
- pause;
- resume if implemented;
- stop;
- invalid state transition;
- safety precedence.

---

# 95. UNIT TESTS — HUMAN INTERFACE

Tests should verify:

- command parsing;
- duplicate handling;
- stale request rejection;
- stop propagation;
- pause propagation;
- confirmation request matching.

---

# 96. INTEGRATION TEST — SYNTHETIC BELIEF

Before EEG integration:

```text
synthetic posterior
→ entropy
→ shared controller
→ confirm/defer/proceed
```

This validates policy independently.

---

# 97. INTEGRATION TEST — HUMAN OVERRIDE

Conceptual:

```text
candidate goal A
→ confirmation requested
→ human override to B
→ A invalidated
→ B becomes approved only through approved control path
```

Exact behavior depends on final goal-selection protocol.

---

# 98. INTEGRATION TEST — EMERGENCY STOP

Conceptual:

```text
NAVIGATING
→ STOP
→ no further movement
```

This must pass regardless of posterior confidence.

---

# 99. CODEX TASK BOUNDARY — SHARED CONTROLLER SKELETON

Before threshold approval, Codex may implement:

> A state-machine-based shared-autonomy controller with explicit modes, human-action handling, and policy interfaces, but no permanent numerical confidence thresholds. Use injected/configurable policy functions or placeholders. Add tests for legal/illegal state transitions, pause, stop, and override precedence. Do not choose the EEG-to-goal mapping.

---

# 100. CODEX TASK AFTER THRESHOLD APPROVAL

Once thresholds are approved, the task must specify:

- confidence/entropy inputs;
- exact thresholds;
- equality behavior;
- proceed/confirm/defer mapping;
- reset/override behavior;
- tests.

No improvisation.

---

# 101. CHANGE-CONTROL TRIGGERS

Explicit approval is required before:

- changing the human/AI responsibility split;
- removing confirmation;
- removing override;
- removing pause/stop;
- changing the binary EEG interaction protocol;
- adding fully autonomous goal selection;
- adding learned policy networks;
- adding low-level EEG control.

---

# 102. OUT-OF-SCOPE HCI FEATURES

Not required:

- speech interface;
- eye tracking;
- VR;
- AR;
- haptic feedback;
- mobile app;
- multimodal user sensing;
- biometric identity;
- LLM conversational agent.

These may only be added with clear research purpose.

---

# 103. CLAIM BOUNDARIES

Allowed if implemented:

> “The system supports human confirmation, override, pause, and emergency stop.”

Allowed:

> “Autonomy level depends on posterior uncertainty.”

Allowed if measured:

> “The uncertainty-aware policy reduced wrong-goal commitment under the tested simulation.”

Not allowed:

> “Users trust the system.”

Not allowed:

> “The interface reduces cognitive workload.”

Not allowed without a real study:

> “The system is user-friendly.”

Not allowed:

> “The AI decides what the human should want.”

---

# 104. ACCEPTANCE CRITERIA — SHARED AUTONOMY

The shared-autonomy layer is correctly implemented when:

1. human goal authority is preserved;
2. EEG is used for goal-level rather than low-level control;
3. candidate and approved goals are distinct;
4. posterior/uncertainty feed the controller;
5. the controller can proceed, confirm, defer, pause, and stop;
6. exact thresholds are configurable;
7. human confirmation is explicit;
8. override invalidates incorrect commitment;
9. pause halts movement;
10. emergency stop has highest control priority;
11. planner receives only approved goals;
12. safety remains independent;
13. adaptation cannot remove human authority;
14. UI is not the only implementation of control logic;
15. automated/headless experiments remain possible;
16. human/system actions are logged;
17. stale or duplicate commands are handled;
18. binary EEG-to-multiple-goal mapping remains external/configurable;
19. no hidden true-goal leakage enters the controller;
20. the component can be ablated for comparison.

---

# 105. ACCEPTANCE CRITERIA — HUMAN–AI INTERACTION

The HAI layer is acceptable when:

1. system state is visible;
2. uncertainty state is interpretable;
3. candidate goal is visible;
4. approval state is visible;
5. human controls are accessible;
6. stop is always available in active operation;
7. errors are not hidden;
8. no-path/safety blocks are reported;
9. interactions are logged;
10. UI does not make unsupported certainty claims.

---

# 106. OPEN DECISIONS — MUST REMAIN OPEN

## 106.1 Exact confidence thresholds

Not locked.

## 106.2 Exact proceed/confirm/defer policy

Conceptually defined, numerically unresolved.

## 106.3 Resume behavior

Not fully locked.

## 106.4 Bayesian reset after override

Not locked.

## 106.5 Human confirmation semantics for adaptation

Not locked.

## 106.6 EEG-to-multiple-goal interaction protocol

Critical and unresolved.

## 106.7 Whether confirmation is mandatory even under highest confidence

Not locked.

## 106.8 Maximum evidence wait before fallback

Not locked.

## 106.9 Simulated-human policy for automated experiments

Not locked.

No implementation agent may silently finalize these.

---

# 107. DECISIONS REQUIRED BEFORE FINAL SHARED-AUTONOMY EXPERIMENTS

Explicitly approve:

1. BCI goal-selection interaction protocol;
2. proceed/confirm/defer policy;
3. numerical confidence/entropy thresholds;
4. confirmation requirements;
5. override semantics;
6. pause/resume behavior;
7. Bayesian reset behavior after correction;
8. simulated-human rule for automated experiments;
9. maximum evidence/timeout rule;
10. policy version.

Record all in `DECISIONS.md`.

---

# 108. CURRENT SHARED-AUTONOMY SUMMARY

The NeuroCognitive Shared Autonomy system uses a strict division of responsibility: **the human determines WHAT mission objective is intended, while the autonomous system determines HOW to reach that approved objective safely.** EEG-derived motor-imagery evidence is accumulated through Bayesian inference, posterior uncertainty is evaluated, and a shared-autonomy controller decides whether to proceed, request confirmation, defer, pause, or stop. The human retains explicit confirmation, override, pause, and emergency-stop authority throughout the interaction, and emergency stop has the highest control priority. The planner receives only approved goals and remains downstream of intent inference, while a separate safety controller can reject unsafe actions regardless of confidence. The interface must make candidate goal, uncertainty, control state, route, and safety interventions understandable without overstating certainty. Exact confidence thresholds, resume/reset semantics, simulated-human experiment rules, and the critical binary EEG-to-multiple-goal interaction protocol remain unresolved and must be approved before final end-to-end experiments.

---

# 109. NEXT DOCUMENT

The next planned document is:

**`13_AUTONOMOUS_PLANNING_AND_CONTROL.md` — Autonomous Planning, 2D Navigation, A*, Risk-Aware Cost, Replanning, and Control Specification**

That document should define:

- environment-to-planner interface;
- A*;
- state/action representation;
- path cost;
- obstacles;
- hazard/risk cost;
- replanning;
- planner failure;
- path efficiency;
- planner/safety boundary;
- deterministic testing;
- and the unresolved exact risk model / \(\lambda\).

It must preserve the rule that planning receives an approved human goal and does not infer intent.
