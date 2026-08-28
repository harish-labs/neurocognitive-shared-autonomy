# 14_SAFETY_CRITICAL_CONTROL.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Safety-Critical Control, Constraint Enforcement, Action Rejection, Fail-Safe Behaviour, and Safety Evaluation

**Document ID:** G-03  
**Document class:** Autonomy & Control / Safety Specification  
**Authority level:** Subordinate to the Master Authority Documents and all previously approved scenario, architecture, data, neuroscience, EEG/ML, calibration/uncertainty, Bayesian, cognitive/adaptive, shared-autonomy, and planning specifications  
**Status:** Authoritative safety-control baseline; exact hazard thresholds and final risk values remain unresolved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND SAFETY BOUNDARY

This document defines the project's **explicit safety-control layer**.

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
13. `12_SHARED_AUTONOMY_AND_HUMAN_AI_INTERACTION.md`
14. `13_AUTONOMOUS_PLANNING_AND_CONTROL.md`

If this document conflicts with a higher-authority document, the higher-authority document wins.

The central safety rule is:

> **The planner proposes. The safety controller authorizes.**

A planned action is not automatically executable.

---

# 1. PURPOSE OF THIS DOCUMENT

This document answers:

> **What does safety mean inside this simulated project?**

> **Which actions must always be rejected?**

> **How does the safety controller interact with planning, uncertainty, human override, and emergency stop?**

> **How are safety violations, interventions, and failure cases measured?**

> **What can and cannot be claimed as “safety-critical”?**

The project demonstrates **measurable simulated safety control**.

It does not demonstrate certified real-world safety.

---

# 2. SAFETY ROLE IN THE ARCHITECTURE

The approved execution path is:

```text
approved human goal
        ↓
A* planner
        ↓
proposed path / action
        ↓
SAFETY CONTROLLER
        ↓
approved / rejected / replan-required
        ↓
environment transition
```

The safety controller is a separate authority layer.

It must remain independent from:

- EEG decoding;
- Bayesian goal inference;
- calibration;
- adaptation;
- route optimization;
- UI presentation.

---

# 3. WHY SAFETY IS SEPARATE FROM PLANNING

A planner solves:

> **What path minimizes the approved cost?**

A safety controller solves:

> **Is the proposed action permitted at all?**

These are not the same problem.

A planner may optimize:

\[
J = \text{distance} + \lambda \cdot \text{risk}
\]

but a hard safety rule may still say:

```text
this cell is forbidden
```

regardless of path cost.

Therefore:

```text
risk-aware planning
≠
hard safety enforcement
```

---

# 4. HARD VS SOFT SAFETY

## 4.1 Hard safety constraint

A condition that must not be violated.

Examples:

- leaving map bounds;
- entering a blocked cell;
- entering a prohibited hazard cell;
- moving while emergency stop is active;
- moving while the system is paused;
- executing an invalid action.

Hard constraints are not tradeable.

---

## 4.2 Soft safety / risk preference

A condition that is undesirable but may be traversable.

Examples:

- moderate hazard zone;
- higher simulated risk region;
- longer exposure to a risk area.

Soft risk belongs primarily in the planning cost.

It does not automatically imply a safety violation.

---

# 5. SAFETY CONTROLLER AUTHORITY

The safety controller must be able to:

```text
APPROVE
REJECT
REQUEST_REPLAN
HALT
```

a proposed action.

It must have authority over planner output.

It must not be possible for the planner to bypass this layer during normal full-system execution.

---

# 6. HUMAN EMERGENCY STOP — HIGHEST PRIORITY

Emergency stop has the highest operational authority.

If emergency stop is active:

```text
proposed action
→ rejected
→ movement halted
```

regardless of:

- EEG confidence;
- posterior probability;
- approved goal;
- path quality;
- adaptation state.

This must be explicitly tested.

---

# 7. HUMAN PAUSE

If the system is paused:

- no autonomous movement should occur;
- planner state may be preserved;
- the safety controller should reject movement execution;
- the event must be logged.

Pause is distinct from emergency stop because it is reversible.

---

# 8. BLOCKED-CELL SAFETY

A blocked cell is impassable.

If the next proposed action enters a blocked cell:

```text
safe = false
intervention = BLOCKED_CELL_REJECTION
```

The action must not be executed.

The system may then request replanning.

---

# 9. OUT-OF-BOUNDS SAFETY

Any action that moves the agent outside the valid map must be rejected.

Example:

```text
agent at top row
action = UP
→ reject
```

This is a hard invariant.

---

# 10. INVALID-ACTION SAFETY

Actions outside the approved action space must be rejected.

Approved initial actions:

```text
UP
DOWN
LEFT
RIGHT
WAIT
```

Anything else should fail explicitly.

---

# 11. HAZARD SAFETY

Hazard handling depends on the final hazard policy.

A hazard may be:

```text
traversable with risk cost
```

or:

```text
prohibited
```

The exact threshold or category at which a hazard becomes forbidden remains unresolved.

This document therefore defines the interface, not the final numerical rule.

---

# 12. PROHIBITED HAZARD

If a cell is designated as prohibited under the final safety policy:

```text
planner proposal
→ safety rejection
```

The cell must not be entered even if it is part of the shortest route.

---

# 13. MODERATE-RISK HAZARD

If a hazard is traversable:

- the planner may incorporate its risk cost;
- the safety controller does not automatically reject it;
- the route may still be valid.

This distinction prevents every risk zone from becoming an obstacle.

---

# 14. SAFETY POLICY INPUT

Conceptually:

```text
SafetyCheckRequest:
    current_state
    proposed_action
    proposed_next_state
    blocked_cells
    risk_map
    hard_constraints
    human_control_state
    safety_policy_id
```

---

# 15. SAFETY POLICY OUTPUT

Conceptually:

```text
SafetyDecision:
    proposed_action
    approved_action
    safe
    intervention_type
    reason
    requires_replan
    safety_policy_id
```

Possible outcomes:

```text
APPROVED
REJECTED
REPLAN_REQUIRED
HALTED
```

---

# 16. SAFETY INTERVENTION TYPES

Recommended conceptual categories:

```text
NONE
OUT_OF_BOUNDS
BLOCKED_CELL
PROHIBITED_HAZARD
PAUSED
EMERGENCY_STOP
INVALID_ACTION
INVALID_STATE
REPLAN_REQUIRED
```

The exact enum naming may differ.

---

# 17. SAFETY CHECK ORDER

A simple deterministic order is preferred.

Conceptually:

```text
1. emergency stop?
2. paused?
3. action valid?
4. next state within bounds?
5. blocked cell?
6. prohibited hazard?
7. other hard constraint?
8. approve
```

The final implementation may refine this order, but precedence must remain explicit.

---

# 18. FAIL-SAFE DEFAULT

If the safety controller cannot determine whether an action is valid because of missing or invalid critical safety state:

> **default to not executing the action**

and report an error.

Example:

```text
risk map missing while a hard hazard rule depends on it
→ halt / fail safely
```

Do not silently assume the action is safe.

---

# 19. FAIL-SAFE IS NOT “STOP EVERYTHING FOREVER”

Fail-safe behavior should be proportional to the failure.

Possible responses include:

- reject one action;
- request replanning;
- pause;
- stop episode.

The system should avoid unnecessary permanent failure when a recoverable replan is possible.

---

# 20. SAFETY AND REPLANNING

A safety rejection may produce:

```text
requires_replan = true
```

Then:

```text
current environment state
→ planner
→ new path
→ safety validation
```

This is appropriate when:

- a route becomes blocked;
- a prohibited hazard appears;
- current path is no longer valid.

---

# 21. SAFETY REJECTION LOOP

The system must avoid infinite cycles:

```text
planner proposes
→ safety rejects
→ planner proposes same action
→ safety rejects
→ ...
```

If repeated replanning cannot find a valid route, return a clear failure state such as:

```text
NO_SAFE_PATH
```

or equivalent.

Exact status name may be implementation-specific.

---

# 22. NO-SAFE-PATH CONDITION

If no path exists that satisfies hard safety constraints:

- autonomous movement must stop;
- the approved goal must not silently change;
- the system should expose the failure;
- the human may intervene.

The planner/safety system must not weaken constraints to force success.

---

# 23. SAFETY AND UNCERTAINTY ARE DIFFERENT

The project contains two different caution mechanisms.

## Intent uncertainty

Concern:

> Are we sure what the human wants?

Response may be:

- defer;
- confirm;
- wait.

## Environmental safety

Concern:

> Is the proposed physical/simulated action permitted?

Response may be:

- reject action;
- replan;
- halt.

These must remain separate.

---

# 24. HIGH CONFIDENCE DOES NOT OVERRIDE SAFETY

Even if:

```text
P(goal A) = very high
```

the system may not:

- cross a blocked cell;
- enter a prohibited hazard;
- ignore emergency stop.

Goal confidence governs **intent commitment**.

It does not authorize unsafe motion.

---

# 25. LOW UNCERTAINTY DOES NOT MEAN SAFE PATH

A correct goal can still have an unsafe route.

Therefore:

```text
correct intent
≠
safe execution
```

Both layers are necessary.

---

# 26. SAFETY AND HUMAN OVERRIDE

If a human override changes the goal:

- old plan should no longer be executed;
- safety controller should reject stale actions if necessary;
- new planning must use the newly approved goal.

---

# 27. STALE ACTION PROTECTION

Actions should be linked to:

- current episode;
- current plan;
- current approved goal;
- current environment state.

A delayed action from an older plan should not be executed if state has changed.

---

# 28. PLAN VERSIONING

Every path should have:

```text
plan_id
```

A proposed action should reference that plan.

If:

```text
plan_id != current active plan
```

the action should be rejected as stale.

This is recommended for robust control.

---

# 29. STATE VERSIONING

A similar concept may use:

```text
state_version
```

or environment step index.

This helps ensure safety checks apply to the same state used by the planner.

Exact implementation is optional but useful.

---

# 30. SAFETY STATE

Conceptual states:

```text
SAFE
INTERVENTION_REQUIRED
REPLAN_REQUIRED
PAUSED
EMERGENCY_STOP
FAILED_SAFE
```

Exact naming may differ.

---

# 31. SAFETY CONTROLLER FILE

Approved architecture:

```text
src/autonomy/safety.py
```

Responsibilities:

- validate proposed action;
- enforce hard constraints;
- enforce stop/pause;
- reject invalid movement;
- detect prohibited hazards;
- request replanning;
- produce safety record.

It must not:

- train models;
- perform Bayesian inference;
- infer goal;
- modify EEG evidence;
- silently change human intent.

---

# 32. SAFETY CONTROLLER SHOULD BE DETERMINISTIC

Given the same:

- state;
- proposed action;
- safety policy;

the decision should be the same.

No stochastic safety logic is required.

---

# 33. HARD SAFETY RULES SHOULD BE EXPLICIT

Prefer:

```python
if next_cell in blocked_cells:
    reject
```

over an opaque learned safety classifier.

The project does not need a neural safety model.

---

# 34. SAFETY POLICY CONFIGURATION

Conceptually:

```yaml
safety:
  policy_id: TBD
  blocked_cells_forbidden: true
  out_of_bounds_forbidden: true
  emergency_stop_enabled: true
  prohibited_hazard_rule: TBD
```

The unresolved hazard rule remains `TBD`.

---

# 35. SAFETY POLICY VERSIONING

Once frozen:

```text
safety_policy_v001
```

should identify the active rule set.

Every experiment should record the policy version.

---

# 36. HAZARD THRESHOLD — UNRESOLVED

If numerical risk values are used, the project may eventually define:

```text
risk >= threshold
→ prohibited
```

The exact threshold is not yet approved.

Do not hard-code one without a documented decision.

---

# 37. HARD-CONSTRAINT SET

The minimum hard-constraint set should include:

```text
map bounds
blocked cells
invalid actions
pause
emergency stop
```

Prohibited-hazard logic becomes part of the hard set once its policy is approved.

---

# 38. WAIT SAFETY

`WAIT` should generally be safe if:

- the current cell is valid;
- no emergency rule requires termination.

However, the experiment may count excessive waiting as task failure/timeout.

That is a task-performance rule, not a hard safety violation.

---

# 39. GOAL-CELL SAFETY

A goal cell must itself be valid.

If a goal lies in a blocked/prohibited location:

- planning should fail;
- safety should prevent entry.

The system must not assume all configured goals are valid.

---

# 40. START-CELL SAFETY

Likewise, an episode should fail validation if the agent starts in:

- blocked cell;
- invalid coordinate;
- prohibited cell.

This should be caught before navigation.

---

# 41. SAFETY AT RESET

On environment reset:

- clear stale stop/pause state according to approved episode reset rules;
- validate initial state;
- validate map;
- reset safety log for the episode.

Do not carry unintended safety state across episodes.

---

# 42. EMERGENCY-STOP RESET

After an emergency stop, resuming normal operation should require an explicit reset or approved resume mechanism.

The exact reset workflow remains implementation-specific but must not happen automatically.

---

# 43. SAFETY EVENT LOG

Every intervention should record:

```text
episode_id
step
plan_id
current_position
proposed_action
proposed_next_position
intervention_type
reason
approved_action
requires_replan
safety_policy_id
timestamp
```

---

# 44. UNSAFE ACTION ATTEMPT

An unsafe action attempt is:

> a proposed action that would violate a hard safety rule if executed.

This metric is important even if the safety controller successfully blocks it.

---

# 45. EXECUTED SAFETY VIOLATION

An executed safety violation is:

> an unsafe action that actually reaches the environment despite the safety layer.

Ideally:

```text
0
```

in the full safety-enabled system.

However, this must be measured rather than assumed.

---

# 46. SAFETY OVERRIDE

A safety override occurs when:

```text
planner proposes action
→ safety rejects/modifies it
```

The project should count these separately from human overrides.

---

# 47. HUMAN OVERRIDE VS SAFETY OVERRIDE

## Human override

Human changes or rejects system intent/control.

## Safety override

Safety controller rejects planner output.

They are separate metrics.

---

# 48. HAZARD ENTRY

Hazard entry should be divided into:

```text
allowed risk-zone entry
```

and:

```text
prohibited hazard violation
```

Do not label every risk-zone visit as a safety failure.

---

# 49. SAFETY METRICS

Approved broader metrics include:

- safety violations;
- attempted unsafe actions;
- hazard entry;
- safety overrides;
- uncertainty deferrals/stops.

This document adds structure to those measures.

---

# 50. POSSIBLE SAFETY METRICS

Final metrics may include:

```text
unsafe_action_attempts
executed_safety_violations
blocked_cell_attempts
prohibited_hazard_attempts
safety_overrides
replans_due_to_safety
emergency_stops
no_safe_path_events
```

Exact final set will be frozen in the Metrics document.

---

# 51. SAFETY RATE METRIC

A possible normalized metric:

\[
SafetyViolationRate
=
\frac{\text{executed violations}}
{\text{total attempted actions}}
\]

This is only a candidate metric.

The final definition belongs in `18_METRICS_AND_EVALUATION.md`.

---

# 52. SAFETY INTERVENTION RATE

Possible:

\[
InterventionRate
=
\frac{\text{safety interventions}}
{\text{total proposed actions}}
\]

Again, final use is not yet locked.

---

# 53. RISK EXPOSURE VS SAFETY

A planner may produce:

- zero hard safety violations;
- but non-zero risk exposure.

This distinction is useful.

The project should avoid claiming:

> “zero risk”

simply because no hard rule was broken.

---

# 54. SAFETY ABLATION

The architecture requires:

```text
Full system
vs
Full - safety
```

in controlled experiments.

This must be implemented carefully.

Disabling safety is allowed only in simulation and only for evaluation.

---

# 55. SAFETY-ABLATION WARNING

Ablation should not create uncontrolled code behavior.

Even in `safety OFF` mode:

- basic software validity such as array bounds should remain protected;
- the experiment may allow otherwise prohibited simulated hazard actions;
- the condition must be explicitly labeled.

Do not crash the program merely to represent unsafe behavior.

---

# 56. HARD SOFTWARE VALIDITY IS NOT AN ABLATABLE SAFETY FEATURE

Examples:

- invalid memory access;
- invalid array index;
- malformed action enum.

These are software errors, not experimental safety behaviors.

They should remain prevented in every condition.

---

# 57. SYSTEM A/B/C/D SAFETY TREATMENT

The final Experimental Design document must define how safety is applied across:

- System A;
- System B;
- System C;
- System D.

The comparison must be fair.

This document does not silently decide whether all baselines keep the same environmental safety layer.

---

# 58. SAFETY STRESS TESTS

Controlled stress tests may include:

- path blocked after planning;
- high-risk shortcut;
- prohibited hazard on shortest route;
- repeated unsafe planner proposal;
- human stop during movement;
- no-safe-path condition.

These should be reproducible.

---

# 59. DYNAMIC HAZARD TEST

Conceptual:

```text
agent plans route
→ hazard state changes
→ next action becomes prohibited
→ safety rejects
→ planner replans
```

This tests planner/safety coordination.

---

# 60. BLOCKAGE TEST

Conceptual:

```text
current path contains cell X
→ X becomes blocked
→ safety rejects entry
→ replan
```

---

# 61. EMERGENCY-STOP TEST

Conceptual:

```text
NAVIGATING
→ emergency stop
→ zero further movement actions
```

This must be a hard integration test.

---

# 62. PAUSE TEST

Conceptual:

```text
NAVIGATING
→ pause
→ no state movement
→ resume
```

Resume behavior must follow the approved policy.

---

# 63. NO-SAFE-PATH TEST

Construct a map where:

- route exists geometrically;
- every route violates a hard safety constraint.

Expected:

```text
NO_SAFE_PATH / fail-safe state
```

not unsafe execution.

---

# 64. SAFETY CONTROLLER UNIT TESTS

Minimum test categories:

1. valid action approved;
2. out-of-bounds rejected;
3. blocked cell rejected;
4. invalid action rejected;
5. paused state rejects movement;
6. emergency stop rejects movement;
7. prohibited hazard rejected once policy exists;
8. replan flag set when appropriate;
9. decision deterministic;
10. safety log fields populated.

---

# 65. INTEGRATION TEST — PLANNER + SAFETY

```text
planner proposes
→ safety checks
→ environment executes only if approved
```

Test both approved and rejected paths.

---

# 66. INTEGRATION TEST — SHARED AUTONOMY + SAFETY

A high-confidence approved goal should still be unable to bypass a safety rule.

---

# 67. INTEGRATION TEST — HUMAN + SAFETY

Emergency stop must dominate even when:

- goal is approved;
- path exists;
- next action is otherwise safe.

---

# 68. FAILURE CASES

The final project should inspect:

## False negative safety failure

Unsafe action is allowed.

## False positive safety intervention

Safe action is unnecessarily rejected.

## Replanning failure

Safety rejects but no valid replan occurs.

## Stale-plan execution

Old action executed after state changed.

## Emergency stop failure

Critical implementation failure.

## Policy mismatch

Planner and safety use inconsistent hazard interpretation.

---

# 69. POLICY CONSISTENCY

Planner and safety may use the same risk map but different semantics.

Example:

```text
planner:
risk = cost

safety:
risk above threshold = forbidden
```

This is acceptable if documented.

It is not acceptable if the two modules interpret the same hazard value inconsistently by accident.

---

# 70. SAFETY MAP CONTRACT

Conceptually:

```text
SafetyMap:
    blocked_cells
    risk_values
    prohibited_cells
    policy_id
```

The exact structure may be integrated with the environment state.

---

# 71. SAFETY POLICY MUST NOT DEPEND ON UI COLOR

A red cell in Streamlit is not a safety rule.

The safety controller must use structured environment data.

---

# 72. SAFETY POLICY MUST NOT DEPEND ON SCREEN STATE

Headless experiments must produce identical safety decisions.

---

# 73. SAFETY AND LOGGING

Every safety event must be machine-readable.

Screenshots may supplement but cannot replace logs.

---

# 74. SAFETY AND REPRODUCIBILITY

A safety outcome must be reproducible from:

```text
map
state
action
policy
human control state
code commit
```

---

# 75. SAFETY AND ADAPTATION

Adaptation must not automatically alter hard safety rules.

This is non-negotiable.

If future work explores adaptive risk tolerance, that requires explicit new scope.

---

# 76. SAFETY AND BAYESIAN CONFIDENCE

Posterior confidence may determine whether a goal is approved.

It must not determine whether a blocked cell becomes legal.

---

# 77. SAFETY AND CALIBRATION

Calibration influences confidence reliability.

It does not replace environmental safety.

---

# 78. SAFETY AND EEG NOISE

Noisier EEG may cause:

- wrong goals;
- more deferral.

Safety may still protect the environment layer after a wrong goal is approved.

This is an important system-level distinction.

---

# 79. WRONG GOAL VS UNSAFE PATH

A system can fail in different ways:

## Wrong goal, safe route

Intent failure.

## Correct goal, unsafe route attempt

Planning/safety failure.

## Wrong goal, unsafe route

Combined failure.

The evaluation should distinguish these.

---

# 80. SAFETY SUCCESS IS NOT TASK SUCCESS

An agent can be perfectly safe by never moving.

Therefore safety metrics must be interpreted alongside:

- task success;
- latency;
- path efficiency;
- human intervention.

---

# 81. TASK SUCCESS IS NOT SAFETY SUCCESS

An agent can reach a goal by crossing prohibited areas.

Therefore task success alone is insufficient.

---

# 82. FAIL-SAFE VS FAIL-OPERATIONAL

The core project prioritizes fail-safe behavior.

If uncertain about a hard safety condition:

```text
do not execute
```

The project does not require sophisticated fail-operational redundancy.

---

# 83. REDUNDANT SAFETY CHANNELS — NOT REQUIRED

No need for:

- dual controllers;
- hardware emergency relay;
- formal redundancy architecture.

This is a software simulation.

---

# 84. FORMAL VERIFICATION — NOT CORE

The project does not require:

- theorem proving;
- model checking;
- formal safety certification.

Unit tests, integration tests, controlled experiments, and measurable constraints are sufficient.

Formal verification may be future work.

---

# 85. CONTROL BARRIER FUNCTIONS — NOT CORE

Advanced continuous-control safety methods such as:

- control barrier functions;
- reachability analysis;

are not required in the discrete 2D core.

---

# 86. SAFETY SHIELD TERMINOLOGY

The safety controller may conceptually act as a **safety shield** because it blocks prohibited actions.

However, do not imply formal shielding guarantees unless the implemented rule set and scope are clearly stated.

---

# 87. SAFETY-CRITICAL TERMINOLOGY

The project may use:

> **safety-critical control**

in the limited context of:

- simulated constraint enforcement;
- action rejection;
- emergency stop;
- measurable violations.

It must not imply:

- certified robotics safety;
- medical-device safety;
- aviation-grade safety;
- real disaster deployment validation.

---

# 88. CLAIM BOUNDARIES

Allowed if implemented:

> “The safety controller rejected actions that violated blocked-cell and prohibited-hazard constraints.”

Allowed:

> “Emergency stop superseded autonomous execution.”

Allowed if measured:

> “The safety layer reduced executed violations in the simulated environment.”

Not allowed:

> “The system is safe for real-world rescue deployment.”

Not allowed:

> “The safety controller guarantees human safety.”

Not allowed:

> “The system is formally verified.”

---

# 89. SIMULATED SAFETY WORDING

Preferred wording:

> **simulated safety constraints**

> **explicit action-rejection safety layer**

> **measurable safety intervention in a 2D Search & Rescue simulation**

These are scientifically accurate.

---

# 90. SAFETY RESULTS TABLE

The final project should support a table conceptually like:

| Condition | Unsafe Attempts | Executed Violations | Safety Overrides | Hazard Entries | Replans | Task Success |
|---|---:|---:|---:|---:|---:|---:|
| Safety ON | measured | measured | measured | measured | measured | measured |
| Safety OFF | measured | measured | measured | measured | measured | measured |

No values are to be inserted before experiments.

---

# 91. SAFETY FAILURE TRACE

For any violation, preserve:

```text
episode
step
goal
position
planner action
safety decision
environment state
policy
outcome
```

This allows debugging.

---

# 92. SAFETY POLICY CHANGE CONTROL

Changing any of the following requires explicit approval:

- hard constraint set;
- prohibited-hazard definition;
- safety precedence;
- emergency-stop semantics;
- safety OFF ablation semantics;
- fail-safe default;
- planner/safety authority order.

---

# 93. CODEX TASK — SAFETY CORE

A suitable Codex task:

> Implement `src/autonomy/safety.py` as a deterministic safety controller. It must accept current state and a proposed action, reject out-of-bounds moves, blocked-cell moves, invalid actions, movement while paused, and all movement while emergency stop is active. Return a structured `SafetyDecision` with reason and replan flag. Add unit tests. Do not choose the final hazard-risk threshold yet and do not modify A*, EEG, Bayesian inference, or shared-autonomy policy.

---

# 94. CODEX TASK — PROHIBITED HAZARD AFTER APPROVAL

Only after the hazard policy is approved:

> Add the approved prohibited-hazard rule to the safety controller. Keep planner risk cost separate. Add tests for traversable-risk cells versus prohibited cells, and verify that hard constraints cannot be overridden by a lower path cost.

---

# 95. CODEX TASK — INTEGRATION

After planner and safety core pass independently:

> Integrate one-step navigation so the planner proposes an action, safety authorizes or rejects it, and only approved actions reach `environment.step()`. Add replan handling and tests for blocked paths, emergency stop, and no-safe-path conditions.

---

# 96. IMPLEMENTATION ORDER

## Stage 1 — Basic hard rules

- bounds;
- blocked cells;
- valid action;
- pause;
- stop.

## Stage 2 — Planner integration

- validate every proposed action.

## Stage 3 — Hazard policy

- add once risk/prohibited thresholds are approved.

## Stage 4 — Replanning

- safety rejection triggers replan.

## Stage 5 — Shared-autonomy integration

- approved goal + human stop/pause.

## Stage 6 — Safety experiments

- ON/OFF;
- blockage;
- hazard;
- stop;
- no-safe-path.

---

# 97. OPEN DECISIONS — MUST REMAIN OPEN

## 97.1 Prohibited-hazard threshold

Not locked.

## 97.2 Exact hazard categories

Not locked.

## 97.3 Exact risk scale

Not locked.

## 97.4 Exact `NO_SAFE_PATH` failure semantics

Concept defined; implementation details not locked.

## 97.5 Resume after emergency stop

Not locked.

## 97.6 Exact safety treatment across A/B/C/D baselines

Not locked.

## 97.7 Final normalized safety metrics

Not locked.

No implementation agent may silently finalize these.

---

# 98. DECISIONS REQUIRED BEFORE FINAL SAFETY EXPERIMENTS

Explicitly approve:

1. final hazard categories;
2. final risk scale;
3. prohibited-hazard rule;
4. hard safety-policy version;
5. safety ON/OFF experimental semantics;
6. no-safe-path termination behavior;
7. emergency-stop reset/resume behavior;
8. final safety metrics;
9. final test maps/stress cases.

Record in:

- `DECISIONS.md`;
- configuration;
- experiment logs.

---

# 99. ACCEPTANCE CRITERIA — SAFETY CONTROLLER

The safety layer is correctly implemented when:

1. every autonomous action passes through safety;
2. invalid actions are rejected;
3. out-of-bounds actions are rejected;
4. blocked-cell actions are rejected;
5. pause blocks movement;
6. emergency stop blocks movement;
7. safety can request replanning;
8. no-safe-path failure is explicit;
9. prohibited hazards are enforced once policy is approved;
10. planner cannot bypass safety;
11. hard constraints remain separate from soft risk cost;
12. safety decisions are deterministic;
13. safety interventions are logged;
14. stale actions can be rejected;
15. safety can be disabled only in controlled simulation ablation;
16. software-validity protections remain active even during ablation;
17. human authority remains above autonomous execution;
18. safety remains independent from EEG confidence and Bayesian belief.

---

# 100. ACCEPTANCE CRITERIA — SAFETY EVALUATION

Safety evaluation is valid when:

1. unsafe attempts are counted;
2. executed violations are counted separately;
3. hazard entry is distinguished from hard violations;
4. safety overrides are recorded;
5. replan events are recorded;
6. emergency stop is tested;
7. safety ON/OFF conditions are explicit;
8. task success is reported alongside safety;
9. negative/failure cases are preserved;
10. no real-world safety claim is made.

---

# 101. CURRENT SAFETY-CONTROL SUMMARY

The NeuroCognitive Shared Autonomy project uses a dedicated **software safety controller** between autonomous planning and environment execution. A* may generate the route, but every proposed movement must be validated before execution. Hard constraints include map boundaries, blocked cells, invalid actions, human pause, and emergency stop, while future prohibited-hazard rules will be added once the exact hazard policy is approved. Soft environmental risk remains part of planning cost and is distinct from hard safety enforcement. The safety controller may approve an action, reject it, request replanning, or halt execution, and emergency stop has the highest authority. Safety events, unsafe action attempts, executed violations, hazard entries, and safety overrides must be logged and evaluated separately from task success. The project may claim explicit measurable **simulated safety control**, but it must not claim certified or real-world Search & Rescue safety. Exact hazard thresholds, final risk categories, no-safe-path semantics, and safety treatment across final A/B/C/D experiments remain unresolved until explicitly approved.

---

# 102. NEXT DOCUMENT

The next planned document is:

**`15_IMPLEMENTATION_BLUEPRINT.md` — Complete Module-by-Module Implementation Blueprint**

That document should convert the approved architecture into implementation tickets for every module, including:

- purpose;
- inputs;
- outputs;
- files;
- dependencies;
- required behavior;
- tests;
- acceptance criteria;
- integration points;
- forbidden changes;
- and milestone order.

It should be written specifically for the **ChatGPT + project owner + Codex** workflow and must preserve every unresolved scientific decision instead of allowing Codex to choose them.
