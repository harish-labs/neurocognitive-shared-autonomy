# 13_AUTONOMOUS_PLANNING_AND_CONTROL.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Autonomous Planning, 2D Navigation, A*, Risk-Aware Cost, Replanning, and Control Specification

**Document ID:** G-02  
**Document class:** Autonomy & Control / Planning Specification  
**Authority level:** Subordinate to the Master Authority Documents and all previously approved scenario, architecture, data, neuroscience, EEG/ML, calibration/uncertainty, Bayesian, cognitive/adaptive, and shared-autonomy specifications  
**Status:** Authoritative planning/control baseline; the exact hazard-risk model and risk-weight parameter remain explicitly unresolved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND NON-INTERPRETATION RULE

This document defines the planning and autonomous-control layer used after a human objective has been sufficiently inferred and approved.

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

If this document conflicts with any higher-authority document, the higher-authority document wins.

The central planning rule is:

> **The planner receives an approved human objective. It does not infer what the human wants.**

The planning layer must not:

- reinterpret EEG;
- modify Bayesian belief;
- choose a different goal merely because it is easier;
- override human stop/pause;
- bypass the safety controller;
- silently decide the unresolved EEG-to-goal mapping;
- or invent a final risk model before approval.

---

# 1. PURPOSE OF THIS DOCUMENT

This document answers:

> **How does the autonomous agent move through the 2D Search & Rescue environment after a goal is approved?**

> **What information does the planner receive?**

> **How is A* used?**

> **How are blocked paths and hazards represented?**

> **What is the relationship between risk-aware planning and hard safety constraints?**

> **When does the system replan?**

> **What counts as planning success, failure, and path efficiency?**

> **How is autonomous movement kept modular, testable, and reproducible?**

---

# 2. ROLE OF THE PLANNING LAYER

The planning layer exists to solve the "HOW" part of the project.

The human/shared-autonomy system determines:

```text
WHAT goal is intended
```

The planner determines:

```text
HOW to reach that approved goal
```

Conceptually:

```text
approved goal
+ current environment state
+ obstacles
+ risk map
        ↓
A* planner
        ↓
candidate path
        ↓
safety controller
        ↓
approved next action
        ↓
environment transition
```

---

# 3. PLANNING IS DOWNSTREAM OF INTENT INFERENCE

The planner must not receive raw EEG.

It should receive only:

- the approved goal;
- the current agent position;
- environment map;
- blocked cells;
- risk/hazard information;
- planner configuration.

This preserves a clean architectural separation:

```text
EEG / intent system
    decides goal

Planner
    decides route
```

---

# 4. APPROVED CORE PLANNER

The initial approved planner is:

> **A\***

A* is appropriate because:

- the environment is a simple 2D grid;
- shortest-path planning is transparent;
- risk-aware cost can be incorporated;
- behavior is deterministic under fixed tie-breaking/configuration;
- the project does not require a novel planning algorithm.

The planner is a supporting autonomy component, not the primary research novelty.

---

# 5. WHY A* IS PREFERRED OVER RL FOR THE CORE

The core research question concerns:

- uncertain EEG intent;
- Bayesian belief;
- shared autonomy;
- safety;
- human oversight.

Using reinforcement learning as the primary planner would introduce additional complexity unrelated to the central question.

A* provides:

- predictable behavior;
- easier testing;
- easier failure analysis;
- reproducibility;
- clear optimality assumptions under a defined cost.

Therefore RL/PPO remains optional future work only.

---

# 6. ENVIRONMENT REPRESENTATION

The approved simulation remains a simple 2D technical environment.

A grid-based representation is preferred.

Conceptually:

```text
Grid[y][x]
```

Each cell may contain or reference:

- free space;
- blocked obstacle;
- hazard/risk value;
- rescue goal;
- safe zone;
- resource point;
- agent position.

The exact internal representation may differ as long as these semantics are preserved.

---

# 7. GRID COORDINATES

Coordinates should be explicit.

One acceptable convention is:

```text
(row, column)
```

or:

```text
(y, x)
```

The chosen convention must remain consistent across:

- environment;
- planner;
- safety;
- visualization;
- logs;
- tests.

Do not silently mix:

```text
(x, y)
```

and:

```text
(row, column)
```

---

# 8. AGENT STATE

At minimum, the planner needs:

```text
current_position
approved_goal
```

The environment may additionally expose:

- current path;
- current episode;
- current hazard configuration;
- current blocked cells.

Orientation is not required in the initial discrete grid.

---

# 9. APPROVED ACTION SPACE

The current initial discrete action set is:

```text
UP
DOWN
LEFT
RIGHT
WAIT
```

No diagonal movement is currently required.

This makes:

- cost definition simpler;
- path length interpretable;
- testing easier.

Diagonal motion may only be introduced through an explicit scope change.

---

# 10. MOVEMENT TRANSITIONS

For a grid position:

```text
(r, c)
```

conceptual motion is:

```text
UP    → (r-1, c)
DOWN  → (r+1, c)
LEFT  → (r, c-1)
RIGHT → (r, c+1)
WAIT  → (r, c)
```

The environment/safety layer must reject invalid transitions.

---

# 11. BLOCKED CELLS

Blocked cells represent impassable regions.

Examples:

- collapsed wall;
- rubble;
- inaccessible corridor;
- structurally blocked area.

Blocked cells must be treated as:

> **hard non-traversable constraints**

They are not merely expensive cells.

The planner should not generate a path through them.

The safety controller should also reject any attempted blocked-cell action.

---

# 12. HAZARD / RISK CELLS

Hazard cells represent elevated risk.

Unlike hard obstacles, some hazard cells may be:

- traversable at increased cost;
- or prohibited entirely.

The exact hazard categories and numerical values remain unresolved.

This distinction allows the project to represent:

```text
hard constraints
vs
soft risk preferences
```

---

# 13. HARD VS SOFT RISK

## Hard constraint

Example:

```text
collapsed wall
```

or:

```text
forbidden hazard
```

The action is not permitted.

## Soft risk

Example:

```text
moderate smoke zone
```

The path may be traversable but less desirable.

This difference is critical.

Do not represent all safety as a single weighted cost.

---

# 14. BASE PATH COST

Without risk, the simplest path cost is:

\[
g(n)
\]

equal to the cumulative movement cost from start to node \(n\).

For orthogonal grid movement, a standard step cost can conceptually be:

\[
1
\]

per move.

The exact implementation should keep cost units simple and documented.

---

# 15. A* EVALUATION FUNCTION

A* uses:

\[
f(n)=g(n)+h(n)
\]

where:

- \(g(n)\) = cost from start to \(n\);
- \(h(n)\) = heuristic estimate from \(n\) to goal.

---

# 16. HEURISTIC

For a 4-connected orthogonal grid, Manhattan distance is a natural heuristic:

\[
h(n)
=
|r_n-r_g|
+
|c_n-c_g|
\]

This is suitable when:

- movement is only up/down/left/right;
- step cost is uniform or risk cost is non-negative.

If the final cost model changes materially, heuristic admissibility/consistency should be reassessed.

---

# 17. HEURISTIC REQUIREMENT

The planner should use a heuristic that is:

- mathematically appropriate for the movement model;
- documented;
- deterministic;
- easy to test.

No complex learned heuristic is required.

---

# 18. RISK-AWARE PATH COST

The approved conceptual planning objective is:

\[
J = \text{distance} + \lambda \cdot \text{risk}
\]

This can be represented incrementally as:

\[
g(n)
=
\sum_{\text{steps}}
\left(
c_{move}
+
\lambda r(cell)
\right)
\]

where:

- \(c_{move}\) = movement cost;
- \(r(cell)\) = risk assigned to a traversed cell;
- \(\lambda\) = risk-weight parameter.

---

# 19. RISK MODEL — UNRESOLVED

The project has not yet locked:

- hazard categories;
- numerical risk scale;
- whether risk applies on entry or occupancy;
- whether risk is additive;
- whether risk is normalized;
- whether risk depends on time;
- whether some hazards are hard forbidden.

Therefore the planner must keep risk representation configurable.

---

# 20. RISK WEIGHT \(\lambda\) — UNRESOLVED

The exact value of:

\[
\lambda
\]

is not approved.

It controls the trade-off between:

```text
short route
```

and:

```text
safer route
```

A large \(\lambda\) can make the planner highly risk-averse.

A small \(\lambda\) can make the planner prioritize distance.

No value should be selected silently.

---

# 21. RISK-WEIGHT SELECTION PRINCIPLE

The final \(\lambda\) should be chosen through:

- a clearly defined scenario;
- sensitivity analysis;
- validation;
- or explicit design rationale.

Do not tune \(\lambda\) repeatedly on final test maps simply to make the system look safest.

---

# 22. SHORTEST VS SAFEST ROUTE TRADE-OFF

A useful scenario may contain:

```text
Route A
shorter
higher risk

Route B
longer
lower risk
```

The planner should be able to show how the selected risk policy changes route choice.

This supports interpretable evaluation.

---

# 23. HARD SAFETY CANNOT BE TRADED AWAY

Even with:

\[
\lambda=0
\]

a hard blocked cell remains forbidden.

Risk cost and hard safety must remain distinct.

This is a core architecture requirement.

---

# 24. PLANNER INPUT CONTRACT

Conceptually:

```text
PlanningRequest:
    start
    approved_goal
    map_dimensions
    blocked_cells
    risk_map
    planner_config
    map_id
```

Optional fields:

```text
episode_id
replan_reason
```

---

# 25. PLANNER OUTPUT CONTRACT

Conceptually:

```text
PlanningResult:
    start
    goal
    path
    path_cost
    movement_cost
    risk_cost
    status
    expanded_nodes
    planner_id
```

Possible statuses:

```text
SUCCESS
NO_PATH
INVALID_START
INVALID_GOAL
REPLAN_REQUIRED
```

---

# 26. PATH REPRESENTATION

A path should be an ordered list of coordinates:

```text
[start, ..., goal]
```

or an ordered list of actions.

The implementation may preserve both.

For reproducibility, the result should make it possible to reconstruct:

- visited route;
- path length;
- action sequence.

---

# 27. NEXT-ACTION EXTRACTION

Given a valid path:

```text
current_position
→ next_position
```

the planner/controller can derive:

```text
UP / DOWN / LEFT / RIGHT
```

The safety controller then validates that action.

---

# 28. WAIT ACTION

`WAIT` allows the agent to remain stationary.

It may be useful when:

- paused;
- waiting for confirmation;
- uncertainty blocks commitment;
- replanning is pending.

`WAIT` should not be treated as progress toward the goal unless specifically required by an experiment.

---

# 29. GOAL VALIDATION

Before planning:

- goal must lie inside map;
- goal must not be blocked;
- goal must be an approved mission objective;
- goal identifier must match environment state.

If invalid, the planner should fail explicitly.

---

# 30. START VALIDATION

The start position must:

- lie inside map;
- not be blocked;
- correspond to current environment state.

Invalid start should fail clearly.

---

# 31. NO-PATH CONDITION

If no valid route exists:

```text
status = NO_PATH
```

The planner must not:

- teleport;
- ignore obstacles;
- silently choose a different goal.

The human-approved objective remains unchanged.

The controller may:

- report failure;
- await environment change;
- request human intervention.

---

# 32. REPLANNING

Replanning means computing a new path after the previous path becomes invalid or undesirable under approved conditions.

Potential triggers include:

- newly blocked route;
- changed hazard map;
- changed approved goal;
- human override;
- failed safety check;
- environment change.

---

# 33. REPLANNING DOES NOT REQUIRE DYNAMIC PHYSICS

The core environment may remain mostly static.

Controlled changes can be introduced for experiments.

Examples:

```text
after step 5, block cell (r,c)
```

or:

```text
increase risk in region X
```

This is sufficient to test replanning.

---

# 34. REPLAN TRIGGER CONTRACT

Conceptually:

```text
ReplanRequest:
    reason
    current_position
    approved_goal
    current_map
    previous_path
```

Reasons may include:

```text
PATH_BLOCKED
HAZARD_CHANGED
SAFETY_REJECTED
GOAL_CHANGED
MANUAL_REQUEST
```

---

# 35. REPLANNING AND GOAL CHANGES

If the approved goal changes:

- old path becomes invalid;
- current movement should halt safely;
- new planning request should use the new approved goal.

The planner itself does not decide why the goal changed.

---

# 36. REPLANNING AND SAFETY

If safety rejects the next action because conditions changed:

```text
safety
→ REPLAN_REQUIRED
```

may be returned.

The planner recomputes from the current state.

---

# 37. PATH EXECUTION

The planner should not execute the entire path without intermediate control checks.

Preferred loop:

```text
plan path
→ propose next action
→ safety check
→ execute one action
→ observe new state
→ continue / replan
```

This preserves safety authority during navigation.

---

# 38. OPEN-LOOP PATH EXECUTION — NOT PREFERRED

Avoid:

```text
generate path
→ execute all actions blindly
```

because:

- environment may change;
- human may pause;
- safety state may change.

Stepwise execution is more compatible with shared autonomy.

---

# 39. PLANNER–ENVIRONMENT INTERFACE

The planner reads environment information.

The environment performs state transition.

Conceptually:

```text
environment.get_state()
        ↓
planner.plan(...)
        ↓
safety.check(...)
        ↓
environment.step(action)
```

The planner must not directly mutate environment state.

---

# 40. PLANNER–SAFETY INTERFACE

The planner proposes.

The safety controller authorizes.

This relationship is mandatory.

```text
planner
→ proposed action/path
→ safety controller
→ approved/rejected action
```

---

# 41. PLANNER–SHARED-AUTONOMY INTERFACE

The planner receives:

```text
approved_goal
```

not:

```text
candidate_goal
```

unless a specific experimental baseline explicitly allows direct commitment.

This keeps intent uncertainty from leaking into planning assumptions.

---

# 42. PLANNER DOES NOT USE EEG CONFIDENCE DIRECTLY

The planner should not alter route cost based on:

```text
EEG confidence
```

unless a future approved experiment explicitly defines such coupling.

Current architecture:

```text
uncertainty
→ autonomy decision

approved goal
→ planner
```

---

# 43. ENVIRONMENTAL RISK VS INTENT UNCERTAINTY

These are separate quantities.

## Intent uncertainty

How uncertain the system is about what the human wants.

## Environmental risk

How undesirable/dangerous a location/path is.

Do not combine them into one generic score.

---

# 44. PATH LENGTH

For orthogonal movement, path length may be measured as:

```text
number of movement actions
```

excluding or including `WAIT` depending on the final metric definition.

The Metrics document must define this precisely.

---

# 45. PATH COST

Path cost may include:

```text
distance component
+
risk component
```

It is not identical to path length.

Final results should distinguish them.

---

# 46. PATH EFFICIENCY

One possible definition is:

\[
Efficiency
=
\frac{\text{reference optimal cost}}
{\text{actual path cost}}
\]

or another approved formulation.

The exact metric is not yet locked.

The Metrics document must freeze it.

---

# 47. REFERENCE OPTIMAL PATH

A useful reference may be the best path under:

- the same cost function;
- same map;
- same constraints.

Do not compare actual risk-aware route against a distance-only optimum without saying so.

---

# 48. PLANNER COMPLETENESS EXPECTATION

A* should find a path if one exists under its graph/cost model, assuming standard implementation conditions.

The project does not need to prove new theoretical results about A*.

Correct implementation is sufficient.

---

# 49. TIE-BREAKING

When multiple nodes have equal A* priority, tie-breaking can affect path shape.

The implementation should be deterministic under fixed configuration.

Possible tie-breaking may use:

- insertion order;
- secondary heuristic;
- coordinate order.

The exact rule is not scientifically central, but should remain stable for reproducibility.

---

# 50. DETERMINISM

Given identical:

- map;
- start;
- goal;
- risk map;
- planner config;

the planner should return the same path where practical.

If randomized tie-breaking is used, the seed must be recorded.

Randomization is not needed for the core.

---

# 51. CLOSED SET / OPEN SET

A standard A* implementation may maintain:

```text
open set
closed/visited information
came_from
g_score
f_score
```

The exact data structure is an implementation detail.

Correctness and clarity matter more than optimization tricks.

---

# 52. PRIORITY QUEUE

A priority queue is appropriate for A*.

Implementation may use:

```text
heapq
```

or equivalent Python standard functionality.

No external planning library is required.

---

# 53. HEURISTIC ADMISSIBILITY

If the heuristic never overestimates remaining cost, A* can retain standard optimality guarantees for the defined graph/cost assumptions.

If risk is non-negative and Manhattan distance represents only minimum movement cost, Manhattan may remain admissible.

Any non-standard heuristic modification must be justified.

---

# 54. RISK-AWARE HEURISTIC — NOT REQUIRED

The heuristic does not need to estimate future risk.

A simpler admissible distance heuristic is sufficient.

Risk may remain entirely in:

\[
g(n)
\]

This keeps implementation transparent.

---

# 55. RISK MAP

Conceptually:

```text
risk_map[r][c]
```

may contain non-negative values.

Requirements:

- dimensions match environment;
- blocked cells handled separately;
- all values finite;
- semantics documented.

Exact scale unresolved.

---

# 56. NEGATIVE RISK VALUES — PROHIBITED

Risk cost should not contain negative values in the core model.

Negative risk could make hazardous routes artificially rewarding and complicate A* assumptions.

If a future utility model includes rewards, it must be defined separately.

---

# 57. HAZARD TYPES

Conceptual hazard categories may include:

```text
LOW
MEDIUM
HIGH
FORBIDDEN
```

or a numerical scale.

No final category system is currently locked.

---

# 58. RISK NORMALIZATION — UNRESOLVED

The risk scale may need normalization if:

```text
distance cost
```

and:

```text
risk cost
```

differ greatly in magnitude.

Exact normalization remains unresolved.

---

# 59. \(\lambda\) SENSITIVITY ANALYSIS

Once a risk model is approved, a useful controlled experiment may vary \(\lambda\).

Possible observations:

- path length;
- risk exposure;
- route selection;
- task completion.

This helps demonstrate the cost trade-off.

The exact values must be selected before final evaluation.

---

# 60. RISK EXPOSURE

A useful metric may be:

\[
R_{path}
=
\sum_{cell\in path}r(cell)
\]

or another approved measure.

This is not yet formally locked.

The Metrics document should define final risk exposure.

---

# 61. SAFETY VIOLATION IS NOT RISK EXPOSURE

A route may pass through moderate-risk cells without violating a hard safety rule.

Therefore distinguish:

```text
risk exposure
```

from:

```text
safety violation
```

---

# 62. STATIC ENVIRONMENT FIRST

The first environment/planner implementation should be static.

This allows validation of:

- A*;
- obstacles;
- risk cost;
- path correctness.

Dynamic obstacles should be added only after this works.

---

# 63. CONTROLLED DYNAMIC CHANGES

Later, deterministic changes may be introduced.

Example:

```text
at step k:
    block cell X
```

or:

```text
update hazard in region Y
```

The change should be recorded in experiment configuration.

---

# 64. NO RANDOM DISASTER SIMULATOR REQUIREMENT

The core does not need:

- fire spread simulation;
- flood physics;
- collapse physics;
- crowd simulation.

These would distract from the research question.

---

# 65. PLANNER FAILURE CASES

The project should explicitly test:

## No path

Goal unreachable.

## Invalid goal

Goal outside map or blocked.

## Invalid start

Start impossible.

## Risk-dominated route

Planner chooses a longer safer path.

## \(\lambda\)-misconfiguration

Route becomes excessively conservative or unsafe.

## Replan failure

No new route after environment change.

## Safety rejection loop

Planner repeatedly proposes unsafe actions.

These failures must be inspectable.

---

# 66. SAFETY-REJECTION LOOP

If:

```text
planner
→ action
→ safety rejects
→ replan
→ same action
→ reject
```

the system should detect repeated failure rather than loop indefinitely.

Possible response:

```text
FAILED
NO_SAFE_PATH
```

Exact error status may be refined.

---

# 67. TIMEOUT / STEP LIMIT

The environment may use:

```text
max_steps
```

to prevent endless episodes.

The exact limit is not locked.

It should be configurable and logged.

---

# 68. WAIT AND TIMEOUT

If the agent waits due to:

- uncertainty;
- pause;
- confirmation;

the experiment must define whether WAIT counts toward:

```text
step limit
```

or:

```text
task completion time
```

This metric detail remains for the Experimental Design/Metrics documents.

---

# 69. GOAL REACHING

A goal is reached when the agent enters the designated goal cell or satisfies another explicitly defined terminal condition.

The simplest core rule is:

```text
agent_position == goal_position
```

This is sufficient for the 2D simulation.

---

# 70. MULTIPLE GOALS IN ENVIRONMENT

The map may contain multiple mission targets.

The planner should accept one:

```text
approved_goal
```

at a time.

It does not solve the BCI selection problem.

---

# 71. GOAL IDENTIFIER VS POSITION

A goal should have both:

```text
goal_id
position
```

where practical.

This allows logs to distinguish:

```text
Victim_A
```

from raw coordinate:

```text
(8, 12)
```

---

# 72. GOAL MOVEMENT — NOT CORE

Goals/victims are static in the core scenario.

Moving victims are not required.

---

# 73. MULTI-AGENT PLANNING — NOT CORE

The project uses a single simulated rescue agent.

No:

- swarm planning;
- multi-agent coordination;
- collision avoidance between agents.

---

# 74. PLANNER OUTPUT LOGGING

Every planning call should record where practical:

```text
plan_id
episode_id
start
goal
path
path_length
movement_cost
risk_cost
total_cost
status
expanded_nodes
lambda
risk_policy_id
map_id
Git commit/config
```

---

# 75. REPLAN LOGGING

Each replan should additionally record:

```text
replan_reason
previous_plan_id
current_position
map change
new_plan_id
```

---

# 76. MAP VERSIONING

Every experimental map should have a stable identity.

Example:

```text
map_basic_001
map_risk_001
map_replan_001
```

If a map changes, preserve a new version rather than silently modifying a reportable test map.

---

# 77. MAP CONFIGURATION

Conceptual representation:

```yaml
map:
  id: map_risk_001
  rows: TBD
  cols: TBD
  start: [...]
  goals: [...]
  blocked_cells: [...]
  hazards: [...]
```

The exact file format may be YAML/JSON or another transparent format.

---

# 78. PLANNER CONFIGURATION

Conceptually:

```yaml
planner:
  algorithm: astar
  heuristic: manhattan
  movement_cost: 1.0
  risk_lambda: TBD
  tie_breaking: TBD
```

`TBD` remains intentional.

---

# 79. RISK CONFIGURATION

Conceptually:

```yaml
risk:
  policy_id: TBD
  scale: TBD
  forbidden_threshold: TBD
```

No final values are approved.

---

# 80. REPRODUCIBILITY

A planner result should be reproducible from:

```text
map
start
goal
risk configuration
planner configuration
code commit
```

No manual clicking should be required to recreate a reported path.

---

# 81. UNIT TEST — EMPTY GRID

Map:

```text
no obstacles
no risk
```

Expected:

- valid shortest path;
- Manhattan path length.

---

# 82. UNIT TEST — SINGLE OBSTACLE

Place an obstacle on the direct path.

Expected:

- route goes around;
- no blocked-cell entry.

---

# 83. UNIT TEST — NO PATH

Enclose the goal with blocked cells.

Expected:

```text
NO_PATH
```

No crash.

---

# 84. UNIT TEST — INVALID GOAL

Goal outside map or blocked.

Expected:

- explicit invalid-goal error/status.

---

# 85. UNIT TEST — WAIT

If WAIT is passed to environment:

- position unchanged;
- state valid;
- step/time semantics as configured.

---

# 86. UNIT TEST — RISK-FREE EQUIVALENCE

With:

```text
all risk = 0
```

risk-aware A* should reduce to the standard distance-based behavior.

---

# 87. UNIT TEST — HIGH-RISK SHORTCUT

Construct:

```text
short risky path
long safe path
```

For a sufficiently high test-only \(\lambda\):

- safe route should be preferred.

For \(\lambda=0\):

- shortest route should be preferred.

These are unit/integration tests using synthetic values, not final methodology choices.

---

# 88. UNIT TEST — HARD HAZARD

A forbidden cell must never appear in the path.

---

# 89. UNIT TEST — REPLANNING

Start with valid path.

Then block one future path cell.

Expected:

- replan from current position;
- new valid route if one exists.

---

# 90. UNIT TEST — DETERMINISM

Same request twice should produce same path under fixed configuration.

---

# 91. INTEGRATION TEST — SHARED AUTONOMY TO PLANNER

Conceptual:

```text
approved goal
→ planner
→ valid route
```

Candidate but unapproved goal must not trigger planning in the normal full-system path.

---

# 92. INTEGRATION TEST — PLANNER TO SAFETY

Conceptual:

```text
planner proposes next action
→ safety validates
→ environment executes
```

Verify safety can reject.

---

# 93. INTEGRATION TEST — HUMAN STOP

During navigation:

```text
STOP
```

must prevent further environment steps even if the planner has a complete path.

---

# 94. INTEGRATION TEST — NO-PATH

Goal approved but no path exists.

Expected:

- planner reports failure;
- autonomous movement stops;
- goal is not silently changed.

---

# 95. PLANNER METRICS

Potential planning metrics include:

- path found/not found;
- path length;
- total path cost;
- risk cost;
- expanded nodes;
- replanning count;
- planning runtime.

Not every metric must be headline research evidence.

The Metrics document will define final use.

---

# 96. SYSTEM-LEVEL METRICS CONNECTED TO PLANNING

Planning influences:

- mission completion;
- task time;
- path efficiency;
- hazard exposure;
- safety interventions.

These are system-level metrics.

---

# 97. PLANNING RUNTIME

A* runtime may be recorded.

However, in a small grid this is not expected to be a major performance bottleneck.

Do not turn optimization of A* runtime into a separate project.

---

# 98. NO NEED FOR GPU

Planning runs on CPU.

No GPU is required.

---

# 99. NO NEED FOR ROS 2 IN CORE

A* and the 2D environment are sufficient for the current project.

ROS 2 remains an optional future extension.

---

# 100. NO NEED FOR GAZEBO IN CORE

Gazebo is not required.

The technical 2D simulator remains authoritative.

---

# 101. NO NEED FOR CONTINUOUS CONTROL

The core does not require:

- velocity;
- acceleration;
- steering angle;
- dynamics;
- motor torques.

This is a discrete navigation problem.

---

# 102. NO NEED FOR SLAM

The map is known in the core scenario.

The project does not require:

- localization;
- mapping;
- SLAM;
- lidar;
- camera mapping.

---

# 103. NO NEED FOR COMPUTER VISION

Victims, obstacles, and hazards are environment entities.

They do not need visual detection.

Computer vision is intentionally out of scope.

---

# 104. NO NEED FOR TRAJECTORY OPTIMIZATION

A* grid paths are sufficient.

Continuous trajectory smoothing is optional and unnecessary for the core.

---

# 105. PLANNER DOES NOT LEARN

The core A* planner is deterministic algorithmic planning.

It does not train from data.

This is acceptable and intentional.

---

# 106. PLANNING AND ADAPTATION

Adaptation should not silently modify A* behavior.

If future adaptation changes:

```text
risk lambda
```

or planner policy, that would be a new adaptation target requiring explicit approval.

Current adaptation candidates focus on cognitive/shared-autonomy parameters.

---

# 107. PLANNING AND HUMAN PREFERENCE

The current human input specifies the goal, not route preference.

A future system could allow:

```text
prefer safer route
```

or:

```text
prefer faster route
```

as explicit human preference.

This is not core.

---

# 108. RISK MODEL VALIDITY

The risk model is an abstraction.

It does not represent:

- real fire probability;
- structural-collapse probability;
- medical risk;
- certified hazard exposure.

The final report must describe it as:

> **simulated environmental risk cost**

---

# 109. SEARCH & RESCUE CLAIM BOUNDARY

Allowed:

> “The planner navigates a simulated 2D Search & Rescue environment with obstacles and configurable hazard costs.”

Not allowed:

> “The planner is validated for real disaster environments.”

---

# 110. PATH-SAFETY CLAIM BOUNDARY

Allowed if implemented:

> “A* planning incorporated configurable simulated risk cost.”

Allowed if implemented:

> “The safety controller prevented entry into prohibited hazard cells.”

Not allowed:

> “The route is objectively safest in the real world.”

---

# 111. REPLANNING CLAIM BOUNDARY

Allowed:

> “The agent replans when a simulated path becomes blocked.”

Not allowed:

> “The system handles arbitrary dynamic disasters.”

---

# 112. FAILURE ANALYSIS REQUIREMENT

Final analysis should include:

- one normal path;
- one risk trade-off path;
- one no-path case;
- one replanning case;
- one safety rejection case;
- any observed planner/safety loop failure.

These should use actual experiment artifacts.

---

# 113. PATH VISUALIZATION

The technical dashboard may show:

```text
agent
approved goal
planned path
blocked cells
risk regions
```

The path should correspond to the actual planner result.

Do not draw an idealized path that differs from logged actions.

---

# 114. RESULTS ARTIFACTS

Planning experiments may generate:

```text
path.json
episode_log.csv
map_config.yaml
planner_metrics.json
route_plot.png
```

Exact filenames may differ.

The important requirement is traceability.

---

# 115. CODE ARCHITECTURE

Approved files:

```text
src/autonomy/environment.py
src/autonomy/planner.py
src/autonomy/safety.py
src/autonomy/shared_controller.py
```

This document mainly governs:

```text
environment.py
planner.py
```

Safety receives its own dedicated next document.

---

# 116. PLANNER FILE RESPONSIBILITY

`planner.py` should contain:

- A*;
- heuristic;
- risk-aware cost;
- path reconstruction;
- planner result.

It should not contain:

- EEG;
- Bayes;
- human confirmation;
- Streamlit.

---

# 117. ENVIRONMENT FILE RESPONSIBILITY

`environment.py` should contain:

- map;
- agent position;
- action transitions;
- terminal state;
- reset;
- deterministic seed/config.

It should not contain:

- model training;
- Bayesian inference;
- calibration;
- hidden safety logic beyond basic state validity.

---

# 118. SAFETY FILE RESPONSIBILITY

`safety.py` should contain:

- action validation against explicit safety rules;
- hard hazard constraints;
- emergency-stop enforcement;
- safety intervention logging.

Detailed behavior belongs in the next document.

---

# 119. CODEX TASK — ENVIRONMENT FIRST

A suitable Codex task:

> Implement only the simple 2D Gymnasium Search & Rescue environment with configurable map size, start position, goal entities, blocked cells, hazard values, actions UP/DOWN/LEFT/RIGHT/WAIT, seeded reset, and deterministic state transitions. Do not implement A*, EEG, Bayes, shared autonomy, or safety policy yet. Add unit tests for bounds, blocked cells, legal motion, goal reaching, reset, and invalid map configurations.

---

# 120. CODEX TASK — A* SECOND

After environment validation:

> Implement A* in `src/autonomy/planner.py` against the existing environment state contract. Use 4-connected movement and a documented Manhattan heuristic. Support blocked cells, configurable non-negative risk cost, path reconstruction, no-path handling, and deterministic output. Keep `risk_lambda` configurable and do not choose its final project value. Add analytical unit tests. Do not implement shared-autonomy or safety policy.

---

# 121. CODEX TASK — REPLANNING THIRD

After A* works:

> Add replanning support triggered by an explicit changed environment state or planner request. Preserve previous plan ID and reason. Add deterministic tests where a path becomes blocked after several steps. Do not add random disaster dynamics.

---

# 122. IMPLEMENTATION ORDER

Recommended order:

## Stage 1 — Environment mechanics

- grid;
- actions;
- goals;
- blocked cells;
- hazards.

## Stage 2 — Standard A*

- no risk;
- deterministic shortest path.

## Stage 3 — Risk-aware cost

- configurable risk map;
- configurable \(\lambda\).

## Stage 4 — Safety interface

- planner proposals passed to safety.

## Stage 5 — Replanning

- controlled path blockage/hazard change.

## Stage 6 — Shared-autonomy integration

- approved goal from controller.

## Stage 7 — Full EEG integration

- intent inference selects/approves goal;
- planner executes.

---

# 123. OPEN DECISIONS — MUST REMAIN OPEN

## 123.1 Exact map dimensions

Configurable; no final universal size locked.

## 123.2 Exact hazard categories

Not locked.

## 123.3 Exact risk scale

Not locked.

## 123.4 Exact \(\lambda\)

Critical planning parameter; not locked.

## 123.5 Forbidden-hazard threshold

Not locked.

## 123.6 Path-efficiency formula

Not locked.

## 123.7 Maximum episode steps

Not locked.

## 123.8 WAIT accounting in metrics

Not locked.

## 123.9 Exact replan triggers for all final experiments

Conceptual triggers defined; final experimental set not locked.

## 123.10 Tie-breaking convention

Implementation detail not yet locked.

No agent may silently convert these into scientific constants.

---

# 124. DECISIONS REQUIRED BEFORE FINAL PLANNING EXPERIMENTS

Explicitly approve and record:

1. final experimental map set;
2. movement-cost definition;
3. risk representation;
4. hazard categories/values;
5. hard forbidden-hazard rule;
6. \(\lambda\);
7. path-efficiency metric;
8. episode-step limit;
9. dynamic/replanning scenario rules;
10. planner-policy version.

Record in `DECISIONS.md` and configuration.

---

# 125. ACCEPTANCE CRITERIA — ENVIRONMENT

The environment is valid when:

1. state is deterministic under fixed config;
2. actions behave correctly;
3. map bounds are enforced;
4. blocked cells cannot be traversed;
5. hazards can be represented;
6. goals can be represented independently of EEG mapping;
7. goal reaching is detected;
8. reset works;
9. invalid maps fail clearly;
10. state can be logged.

---

# 126. ACCEPTANCE CRITERIA — PLANNER

The planner is valid when:

1. it receives only approved goal/environment data;
2. A* is implemented correctly;
3. heuristic is documented;
4. blocked cells are excluded;
5. valid shortest path is found in simple risk-free tests;
6. no-path conditions are handled explicitly;
7. risk-aware cost can be enabled;
8. risk cost is non-negative;
9. \(\lambda\) is configurable;
10. path is reconstructable;
11. output is deterministic under fixed settings;
12. planner does not mutate environment directly;
13. planner does not bypass safety;
14. replanning is supported;
15. planner can be tested without EEG.

---

# 127. ACCEPTANCE CRITERIA — CONTROL INTEGRATION

Planning/control integration is valid when:

1. only approved goals trigger planning;
2. planner proposes one step/path at a time;
3. safety can reject actions;
4. human pause stops execution;
5. emergency stop halts execution;
6. goal change invalidates old path;
7. environment changes can trigger replan;
8. no-path does not silently change goal;
9. all actions are logged;
10. path/task metrics can be computed.

---

# 128. CURRENT PLANNING & CONTROL SUMMARY

The autonomous planning layer implements the **HOW** part of the NeuroCognitive Shared Autonomy system. After a human objective is inferred and approved, a deterministic A*-based planner receives the current 2D Search & Rescue environment, the agent's position, the approved goal, blocked cells, and configurable hazard information. It computes a route using a standard cost \(f(n)=g(n)+h(n)\), with Manhattan distance as the appropriate initial heuristic for the approved four-direction grid. Risk-aware planning is conceptually represented by \(J=\text{distance}+\lambda\cdot\text{risk}\), but the exact hazard model, risk scale, forbidden-hazard rule, and \(\lambda\) remain unresolved and must be approved before final experiments. Blocked cells and other hard safety constraints are never tradeable through path cost. The planner proposes routes/actions, while the separate safety controller authorizes or rejects execution. Navigation proceeds stepwise so human pause/stop, safety intervention, and replanning remain possible. The planner never interprets EEG, modifies Bayesian intent, or substitutes another goal because it is easier.

---

# 129. NEXT DOCUMENT

The next planned document is:

**`14_SAFETY_CRITICAL_CONTROL.md` — Safety-Critical Control, Constraint Enforcement, Action Rejection, Fail-Safe Behaviour, and Safety Evaluation Specification**

That document should define:

- hard vs soft safety constraints;
- blocked-cell rejection;
- prohibited-hazard handling;
- safety-controller authority;
- emergency stop;
- fail-safe defaults;
- safety intervention records;
- safety/replanning interaction;
- uncertainty-related deferral vs environmental safety;
- safety violations;
- unsafe-action attempts;
- ablation;
- testing;
- and claim boundaries.

It must preserve the project's limited claim: **simulated measurable safety control**, not certified real-world safety.
