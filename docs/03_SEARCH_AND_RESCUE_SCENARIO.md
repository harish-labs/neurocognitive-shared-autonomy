# 03_SEARCH_AND_RESCUE_SCENARIO.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Search & Rescue Simulation Specification

**Document ID:** B-01  
**Document class:** Application / Scenario Specification  
**Authority level:** Subordinate to `MASTER_PROJECT_SPEC.md`, `01_PROJECT_CONCEPT_AND_PROBLEM.md`, and `02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md`  
**Status:** Authoritative scenario baseline with unresolved design choices explicitly preserved  
**Project title:** **NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

---

# 0. AUTHORITY AND CHANGE-CONTROL RULE

This document defines **where the approved research problem is instantiated and how the Search & Rescue application scenario behaves**.

It does not redefine:

- the project's primary research question;
- the EEG methodology;
- the Bayesian formulation;
- the uncertainty framework;
- the shared-autonomy principle;
- the safety requirements;
- or the overall technical architecture.

If this document conflicts with a Master Authority Document, the Master Authority Document wins unless the project owner explicitly approves a change.

The scenario must remain:

- **software-first**;
- **simple and technically interpretable**;
- **2D**;
- suitable for controlled experiments;
- suitable for reproducible evaluation;
- and subordinate to the scientific objectives.

The scenario must **not** become a graphics, game-development, 3D-modelling, or digital-twin project.

---

# 1. PURPOSE OF THE SCENARIO

The Search & Rescue scenario exists to provide a concrete, safety-relevant environment in which the project can test the following central problem:

> **Can uncertain EEG-derived human intent be converted into reliable, safe goal-level assistance without allowing the autonomous system to take excessive or unjustified control?**

The application scenario gives practical meaning to each major technical component:

- EEG decoding provides uncertain evidence of human intent;
- Bayesian inference accumulates that evidence;
- uncertainty determines whether the system should act, confirm, or defer;
- shared autonomy separates human objective selection from autonomous execution;
- the planner determines how to reach an approved objective;
- the safety controller constrains unsafe behaviour;
- adaptation can use human corrections or repeated interaction;
- experiments measure reliability, safety, task success, and failure.

The Search & Rescue setting is therefore an **experimental testbed**, not a claim that the prototype is ready for real-world rescue deployment.

---

# 2. CORE SCENARIO CONCEPT

A simulated autonomous rescue agent operates inside a simplified disaster-affected environment.

The environment may contain:

- one start position;
- one rescue agent;
- multiple candidate rescue objectives;
- victims or victim locations;
- a safe/evacuation zone;
- an optional medical or resource point;
- blocked paths;
- hazardous regions;
- safer and riskier alternative routes;
- static obstacles;
- and, if later approved for robustness testing, limited dynamic changes.

The human operator possesses the intended mission objective.

The autonomous agent does **not** initially assume that objective with certainty.

EEG-derived evidence is used to infer the operator's intended choice or goal.

The system then decides how much autonomous assistance is justified.

---

# 3. CENTRAL HUMAN–AUTONOMY RESPONSIBILITY SPLIT

The scenario must preserve the project's central rule:

> **The human determines WHAT should be achieved.**

> **The autonomous system determines HOW to achieve the approved objective safely.**

This distinction is mandatory.

## Human responsibility

The human operator is responsible for:

- expressing the intended goal/choice through the approved EEG interaction mechanism;
- confirming when the system requests confirmation;
- correcting a wrong interpretation;
- overriding autonomous behaviour when necessary;
- pausing the system;
- and triggering an emergency stop.

## Autonomous-system responsibility

The autonomous system is responsible for:

- interpreting EEG-derived evidence probabilistically;
- maintaining belief over possible intentions/goals;
- estimating uncertainty;
- deciding whether it has enough evidence to assist;
- planning a route;
- considering hazards and blocked areas;
- enforcing safety rules;
- replanning when needed;
- executing the selected route in simulation;
- and logging its behaviour.

The autonomous agent must not reinterpret the operator's mission objective merely because another route or target would be easier.

---

# 4. SIMULATION STYLE

The simulation is intentionally minimal.

It should resemble a technical research environment rather than a game.

The preferred representation is a **2D grid-based or equivalently simple discrete environment**.

A configurable grid around **15 × 15 cells** is an appropriate initial engineering default because it is large enough to contain alternative routes and hazards while remaining easy to test. The exact dimensions are a configurable implementation parameter, not a scientific claim.

No 3D modelling is required.

No photorealistic rendering is required.

No Blender environment is required.

No physics engine is required for the core system.

No physical robot is required.

---

# 5. CORE ENVIRONMENT ENTITIES

The scenario should support the following entity types.

## 5.1 Rescue agent

The rescue agent is the simulated autonomous mobile entity.

Minimum state information should include:

- current grid position;
- current selected/approved mission goal, if one exists;
- current path;
- current safety state;
- current shared-autonomy state;
- and whether the agent is active, paused, waiting for confirmation, or stopped.

The environment may use an orientation variable if useful, but orientation is not mandatory for the initial discrete implementation.

---

## 5.2 Start location

Each episode begins with the rescue agent at a known start position.

The start point should be separated from the candidate objectives sufficiently to require meaningful planning.

---

## 5.3 Victim / rescue-target locations

Victims are candidate rescue objectives.

A victim location represents a mission destination such as:

- reach victim;
- inspect victim location;
- deliver assistance;
- or mark the victim as reached/rescued in the simplified simulation.

The simulation does not need to model medicine, physiology, triage, or physical rescue mechanics.

The purpose of the victim entity is to provide a **goal whose selection and safe navigation can be evaluated**.

---

## 5.4 Safe / evacuation zone

A safe zone represents a low-risk mission destination.

Depending on the final experiment, it can act as:

- a candidate goal;
- a return destination;
- an evacuation endpoint;
- or a reference safe state.

Whether the safe zone is directly selectable through EEG depends on the unresolved goal-mapping decision and must not be assumed here.

---

## 5.5 Medical / resource point

A medical or resource point is an optional scenario entity.

It can represent:

- first-aid resources;
- emergency supplies;
- communication equipment;
- or another rescue resource.

It exists to make the environment capable of representing different mission goals.

It is **not mandatory in every experimental map**.

---

## 5.6 Static obstacles

Static obstacles represent impassable structures such as:

- collapsed walls;
- rubble;
- damaged infrastructure;
- inaccessible rooms;
- or blocked corridors.

The planner must treat these as non-traversable.

---

## 5.7 Hazard / risk zones

Hazard zones represent traversable or non-traversable areas that carry elevated risk.

Examples may include:

- fire-affected region;
- structurally unstable area;
- smoke zone;
- electrical hazard;
- flooded area;
- or another abstract danger class.

The core project does **not** need to model real fire dynamics, structural engineering, fluid simulation, or toxic exposure.

The hazard exists as a **formal risk variable used by planning and safety logic**.

The exact numerical risk model is still unresolved.

---

# 6. MAP DESIGN PRINCIPLES

Every experimental map should be designed to test the research system rather than provide visual variety.

Maps should allow at least some of the following:

- multiple candidate goals;
- one or more blocked direct routes;
- a shorter but riskier route;
- a longer but safer route;
- ambiguity between goals during early intent inference;
- meaningful replanning;
- and at least one opportunity for the safety controller to matter.

Maps must not be designed so that:

- only one route is possible in every episode;
- every goal is trivially distinguishable;
- the planner always chooses the same path regardless of risk;
- or the safety controller never receives an unsafe proposal.

The environment should be simple enough that failures can be inspected manually.

---

# 7. POSSIBLE GOAL TYPES

Conceptually, the Search & Rescue environment may contain goals such as:

- Victim A;
- Victim B;
- another victim/rescue location;
- medical/resource point;
- safe/evacuation zone;
- or another explicitly approved mission target.

However, **the number of visible candidate goals in the environment and the number of goals directly selectable through the EEG interface are not necessarily the same thing**.

This distinction is critical because the initial EEG decoder is binary.

---

# 8. CRITICAL UNRESOLVED ISSUE — EEG OUTPUT TO GOAL MAPPING

The approved initial EEG task is:

> **Left-hand motor imagery vs Right-hand motor imagery.**

The scenario can conceptually contain more than two mission goals.

A binary classifier cannot automatically map one-to-one to an arbitrary number of rescue goals.

This document therefore **does not choose the mapping**.

The previously identified options remain:

1. only two active selectable goals at a time;
2. hierarchical/sequential binary selection;
3. later multiclass EEG;
4. EEG controls a binary abstract choice or priority while the autonomous mission layer handles the broader set of goals.

No option is considered approved merely because it is convenient for implementation.

The final mapping must be approved by the project owner before the goal-selection interface and related experiments are frozen.

Until that decision is made, scenario code should separate:

```text
environment goal representation
```

from:

```text
EEG-to-goal selection policy
```

This separation allows the environment to be built without prematurely locking the unresolved BCI mapping.

---

# 9. EEG-CONTROLLED DECISIONS

The EEG interface is intended to control **goal-level human intention**, not low-level continuous navigation.

The EEG component should not be treated as a joystick.

The EEG side may eventually determine:

- which of two currently active choices is intended;
- which branch of a hierarchical goal-selection procedure is intended;
- or another owner-approved binary decision.

The exact policy is unresolved.

The EEG interface must **not** directly control:

- every individual grid movement;
- obstacle avoidance;
- A* routing;
- hazard avoidance;
- replanning;
- or safety enforcement.

This preserves the project's shared-autonomy philosophy.

---

# 10. AUTONOMY-CONTROLLED DECISIONS

Once an objective is sufficiently established and approved under the shared-autonomy policy, the autonomous system handles:

- route generation;
- route execution;
- blocked-cell avoidance;
- hazard-aware path selection;
- safety-rule enforcement;
- replanning;
- waiting when required;
- and stopping when a safety or human-control condition demands it.

Autonomy must remain subordinate to:

- explicit safety constraints;
- human override;
- human pause;
- emergency stop;
- and the uncertainty/confirmation policy.

---

# 11. ALLOWED AGENT ACTIONS

The approved initial discrete action space is:

```text
UP
DOWN
LEFT
RIGHT
WAIT
```

These actions are sufficient for the core 2D research simulation.

Additional actions must not be added unless they serve a clear scientific purpose.

The environment should reject or shield actions that:

- leave the map;
- enter a blocked cell;
- violate an approved hard safety constraint;
- or conflict with emergency-stop state.

---

# 12. ENVIRONMENT STATE

A minimum environment state should support:

- agent position;
- map boundaries;
- candidate goal locations;
- blocked cells;
- hazard/risk information;
- current target/approved objective;
- current path;
- episode status;
- and safety state.

A compact formal representation may be conceptually written as:

\[
s_t =
[\text{agent position},
\text{goal configuration},
\text{obstacle map},
\text{risk map},
\text{mission state}]
\]

Additional state may be introduced only when required by the final implementation.

---

# 13. INTENT / BELIEF STATE

The environment state and the cognitive belief state must remain conceptually separate.

The cognitive layer maintains a belief such as:

\[
P(G_i \mid E_{1:t})
\]

for candidate intention hypotheses.

The environment should not expose the true intended goal to the Bayesian inference module as privileged information during normal inference.

The true intended goal may exist in experiment metadata for evaluation, but it must not be used as an input to the inference algorithm.

This distinction is necessary to avoid invalid evaluation.

---

# 14. UNCERTAINTY STATES

The shared-autonomy layer should support at least three conceptual states:

## High-confidence state

The posterior evidence is sufficiently strong for the approved autonomy policy to proceed with greater autonomous assistance.

## Intermediate-confidence state

The system does not have enough evidence for unrestricted commitment and may request confirmation or reduce assistance.

## Low-confidence state

The system should defer, pause, or explicitly request human input rather than confidently act on weak evidence.

The exact thresholds are **not yet approved**.

Example threshold values previously discussed must remain examples only until experimental tuning/validation is formally defined.

---

# 15. MISSION PHASES

A complete episode can be represented through the following conceptual phases.

## Phase 1 — Initialization

The environment loads:

- map;
- agent start position;
- candidate goals;
- obstacles;
- hazards;
- experiment condition;
- and configuration.

---

## Phase 2 — EEG evidence presentation / replay

A segment or sequence of prerecorded EEG-derived observations is replayed in simulated real-time.

The decoder outputs class probabilities.

---

## Phase 3 — Probability calibration

If the selected decoder requires calibration, raw probabilities are transformed using the approved calibration method.

---

## Phase 4 — Bayesian intent update

The Bayesian module updates the posterior over current intention/goal hypotheses.

---

## Phase 5 — Uncertainty assessment

Entropy or the approved uncertainty measure is computed.

---

## Phase 6 — Shared-autonomy decision

Depending on posterior and uncertainty, the system may:

- proceed;
- request confirmation;
- wait;
- or defer.

---

## Phase 7 — Planning

The autonomous planner computes a route to the approved goal.

---

## Phase 8 — Safety evaluation

The proposed path/action is checked against:

- obstacles;
- hard constraints;
- hazard rules;
- and other safety requirements.

---

## Phase 9 — Execution / replanning

The simulated rescue agent moves through the environment.

If the environment changes or the selected route becomes invalid, the system replans where required.

---

## Phase 10 — Human intervention if needed

The human can:

- confirm;
- override;
- pause;
- or emergency-stop.

---

## Phase 11 — Episode completion

The episode ends on:

- successful goal completion;
- explicit stop;
- unrecoverable failure;
- timeout/step limit;
- or another approved terminal condition.

---

## Phase 12 — Logging

The system records the episode configuration, decisions, outcomes, safety events, interventions, and metrics.

---

# 16. EXAMPLE MISSION — CONCEPTUAL ONLY

The following example illustrates the intended interaction without resolving the binary-goal mapping.

A rescue agent begins in a damaged building map.

The map contains:

- a victim in one area;
- another possible mission target elsewhere;
- a safe zone;
- a blocked corridor;
- and a hazardous region that makes the shortest geometric route undesirable.

The operator intends one of the currently selectable mission choices.

The system receives prerecorded motor-imagery EEG evidence.

The decoder produces uncertain probabilities.

Rather than acting immediately on one prediction, the Bayesian module accumulates evidence.

If the posterior remains ambiguous, the system waits or asks for confirmation.

If the intended mission becomes sufficiently supported, the autonomous planner determines a route.

The safety controller rejects blocked or impermissibly hazardous actions.

The agent then moves autonomously toward the approved target.

If the operator identifies an incorrect interpretation, the operator can override or stop the system.

The episode records:

- decoder output;
- calibrated probabilities;
- posterior;
- entropy;
- selected goal;
- planner path;
- safety events;
- interventions;
- completion status;
- and task metrics.

This example defines the **behavioural pattern**, not the final EEG-to-goal mapping.

---

# 17. HAZARD AND RISK BEHAVIOUR

The environment must support a distinction between:

```text
impassable
```

and:

```text
traversable but risky
```

cells or regions.

This enables the planner and safety controller to demonstrate meaningful behaviour.

The approved conceptual path cost is:

\[
J = \text{distance} + \lambda \cdot \text{risk}
\]

where:

- distance measures path cost/length;
- risk represents environment hazard;
- \(\lambda\) controls the importance of avoiding risk.

The exact risk scale, hazard values, and \(\lambda\) are unresolved.

They must be defined later through the planning/safety and experimental-design documents.

The safety system may also define hard constraints that cannot be traded away by path cost.

For example:

- a blocked cell should remain forbidden regardless of route length;
- an explicitly forbidden hazard cell should not become acceptable merely because it shortens the path.

---

# 18. REPLANNING

Replanning is part of the approved autonomy behaviour.

Replanning may be triggered by:

- a newly blocked route;
- a changed hazard state;
- human override;
- a changed approved goal;
- or another approved scenario event.

The core simulation does not require highly realistic dynamic disaster physics.

Controlled deterministic or seeded scenario changes are preferable for experiments.

---

# 19. HUMAN INTERACTION CONTROLS

The system must support at least the following conceptual human actions:

## Confirm

Approve the system's inferred intention/goal or proposed commitment.

## Override

Reject the current interpretation or autonomous commitment and provide the approved correction mechanism.

## Pause

Temporarily prevent further autonomous progression.

## Emergency stop

Immediately terminate autonomous movement for the episode or until explicitly reset.

The exact UI representation is an implementation detail.

These functions must be visible in logs if used during experiments.

---

# 20. SAFETY CONTROLLER REQUIREMENTS WITHIN THE SCENARIO

The safety controller must have authority to prevent actions that violate scenario safety rules.

It should be capable of:

- blocking motion into impassable cells;
- rejecting invalid coordinates;
- preventing prohibited hazard entry;
- enforcing emergency-stop state;
- forcing replanning when the current path becomes unsafe;
- and recording safety interventions.

Safety must not be implemented only as a visual warning.

A safety rule that never changes agent behaviour is not sufficient evidence of a safety controller.

---

# 21. FAILURE CASES THE SCENARIO MUST SUPPORT

The environment should allow the project to observe and analyze failures such as:

## EEG / decoder failures

- incorrect Left/Right prediction;
- unstable probability output;
- overconfident incorrect prediction;
- poorly calibrated confidence.

## Bayesian failures

- posterior commits to the wrong goal;
- evidence accumulation is too slow;
- prior dominates evidence improperly;
- posterior oscillates.

## Shared-autonomy failures

- system acts too early;
- system defers too often;
- excessive confirmation burden;
- incorrect goal assistance.

## Planning failures

- planner fails to find available path;
- inefficient route;
- risk cost produces undesirable route;
- replanning fails.

## Safety failures

- attempted blocked-cell entry;
- hazardous-zone violation;
- unsafe action not intercepted;
- false-positive safety intervention.

## Human-interaction failures

- override not respected;
- pause not respected;
- emergency stop not respected;
- correction does not update the system as intended.

## Generalization failures

- strong within-subject EEG results but poor unseen-subject behaviour;
- calibration degrades across subjects;
- uncertainty does not increase when predictions become noisier.

These failures must be reportable, not hidden.

---

# 22. EPISODE TERMINATION CONDITIONS

An episode may terminate under conditions such as:

- intended/approved mission target successfully reached;
- human emergency stop;
- maximum step/time limit reached;
- no safe path exists;
- unrecoverable invalid state;
- or experiment-defined failure.

The exact step limit is a configurable parameter and must be recorded.

---

# 23. CORE SCENARIO METRICS

The scenario should support measurement of:

## Task performance

- mission success;
- wrong-goal completion;
- completion time/steps;
- path length;
- path efficiency;
- replanning count.

## Human interaction

- confirmations;
- overrides;
- pauses;
- emergency stops;
- intervention frequency.

## Safety

- attempted unsafe actions;
- executed safety violations;
- hazard entries;
- blocked-cell attempts;
- safety overrides.

## Cognitive/shared-autonomy behaviour

- goal inference accuracy;
- posterior confidence;
- entropy;
- decision latency;
- deferral frequency;
- premature commitment.

These metrics will be formally defined in the Metrics & Evaluation document.

---

# 24. VISUALIZATION REQUIREMENTS

Visualization must remain simple and functional.

A suitable display may show:

- a 2D grid;
- agent position;
- candidate goal locations;
- blocked cells;
- hazard zones;
- current planned path;
- currently inferred/approved target;
- posterior probabilities;
- uncertainty/entropy;
- autonomy state;
- safety events;
- and human controls.

The visualization may use simple symbols, labels, or cells.

The project does not require:

- 3D;
- realistic victim models;
- advanced animation;
- cinematic effects;
- digital-twin fidelity;
- or game-like graphics.

The visualization exists so an evaluator can understand **why the system acted**, not merely watch movement.

---

# 25. STREAMLIT ROLE

Streamlit is the approved initial interface framework.

Its role is to provide a technical dashboard for:

- loading/selecting experiment conditions;
- viewing EEG replay status;
- displaying decoder probabilities;
- displaying Bayesian posterior;
- displaying uncertainty;
- visualizing the 2D environment;
- showing planner path;
- showing safety/shared-autonomy state;
- supporting confirmation/override/pause/stop;
- and reviewing experiment outcomes.

The Streamlit interface is not the primary research contribution.

The system must still operate through reproducible scripts/tests without depending on manual UI interaction for every experiment.

---

# 26. EXPERIMENTAL MAP CLASSES

The scenario should eventually support several controlled map categories.

These categories are conceptual and may be implemented incrementally.

## Class A — Basic navigation map

Purpose:

- validate environment;
- validate planner;
- validate goal reaching.

Characteristics:

- limited obstacles;
- no complex hazards;
- obvious feasible routes.

---

## Class B — Alternative-route map

Purpose:

- evaluate planning choice.

Characteristics:

- multiple possible routes;
- different path lengths.

---

## Class C — Risk-aware map

Purpose:

- evaluate hazard/risk planning and safety.

Characteristics:

- shorter risky route;
- longer safer route;
- at least one hard obstacle.

---

## Class D — Replanning map

Purpose:

- evaluate route update.

Characteristics:

- controlled route blockage or hazard change after planning.

---

## Class E — Intent-ambiguity map

Purpose:

- evaluate shared autonomy under uncertain goal inference.

Characteristics:

- candidate goals structured so that early evidence does not trivially determine the correct target;
- requires genuine confidence/uncertainty handling.

Exact map generation rules belong in later implementation/experimental documents.

---

# 27. STATIC VERSUS DYNAMIC ENVIRONMENT

The **core environment should begin static**.

This reduces unnecessary complexity and allows the EEG/shared-autonomy problem to be isolated.

Dynamic changes may later be introduced for stress testing, such as:

- a path becoming blocked;
- a hazard value changing;
- or an obstacle appearing.

Dynamic behaviour must be controlled and reproducible.

Random dynamic complexity should not be introduced simply to make the simulation appear realistic.

---

# 28. MULTI-AGENT / DRONE / SWARM STATUS

Earlier ideation considered more elaborate rescue concepts such as drone swarms.

Those ideas are **not part of the current locked core scenario**.

The approved core uses a **single simulated rescue agent** unless the project owner later approves multi-agent expansion.

This restriction keeps the research focused on:

- EEG intent;
- Bayesian reasoning;
- uncertainty;
- shared autonomy;
- safety;
- and controlled evaluation.

---

# 29. REAL-WORLD INTERPRETATION BOUNDARY

The simulator represents an abstract research problem.

It does not claim to model:

- complete disaster-response operations;
- rescue logistics;
- medical triage;
- real victim behaviour;
- real robot dynamics;
- radio communication;
- structural collapse;
- fire spread;
- battery chemistry;
- terrain physics;
- or emergency-service procedure.

Therefore final documentation must use wording such as:

> **simulated Search & Rescue environment**

or:

> **2D Search & Rescue research scenario**

and must not imply operational deployment readiness.

---

# 30. ETHICAL AND HUMAN-CONTROL PRINCIPLES

Even in simulation, the system should embody the following principles:

- human mission intent remains authoritative;
- uncertainty should increase caution rather than false confidence;
- autonomous assistance should be interruptible;
- the system should expose uncertainty rather than hide it;
- emergency stop must supersede autonomous action;
- results must not be presented as proof of safety in real disaster settings.

If a future human-subject study is added, it will require a separate ethics/privacy protocol.

---

# 31. REPRODUCIBILITY REQUIREMENTS

Every scenario run used for reported results should record, where applicable:

```text
episode ID
map ID
random seed
configuration
Git commit
EEG subject / trial information
decoder/model version
calibration version
true experimental goal
inferred posterior
uncertainty
selected/approved goal
planned path
agent actions
safety overrides
human interventions
terminal condition
metrics
timestamp
```

The true experimental goal is permitted in logs for evaluation but must not leak into the intent-inference input.

---

# 32. SCENARIO DEVELOPMENT ORDER

The scenario should be implemented in the following order.

## Stage 1 — Environment mechanics

Implement:

- grid;
- agent;
- goals;
- obstacles;
- actions;
- terminal states.

Test without EEG.

---

## Stage 2 — A* planning

Provide explicit artificial goals to the planner.

Verify:

- valid paths;
- blocked paths;
- unreachable goals;
- deterministic behaviour.

---

## Stage 3 — Hazard and safety layer

Add:

- risk zones;
- hard constraints;
- safety rejection;
- risk-aware route behaviour.

---

## Stage 4 — Shared-autonomy interface

Connect artificial/synthetic goal probabilities first.

Do not wait for the final EEG model to test the autonomy logic.

---

## Stage 5 — EEG integration

Connect:

```text
EEG decoder
→ calibration
→ Bayesian inference
→ shared-autonomy decision
→ planner/safety
```

only after each subsystem works independently.

---

## Stage 6 — Experimental automation

Run the scenario without relying on manual dashboard interaction for every episode.

---

## Stage 7 — Streamlit visualization

Use the UI to demonstrate and inspect the already functioning system.

This ordering preserves the approved development philosophy:

> **functionality and scientific verification before presentation polish.**

---

# 33. ACCEPTANCE CRITERIA FOR THIS SCENARIO DOCUMENT

The Search & Rescue scenario is correctly implemented when:

1. a simple 2D environment exists;
2. the agent has a valid discrete action space;
3. candidate goals can be represented independently of EEG mapping;
4. blocked regions are enforced;
5. hazard/risk regions can be represented;
6. A* can plan to an approved goal;
7. safety logic can alter/reject actions;
8. shared autonomy can wait, defer, confirm, or proceed;
9. human override/pause/stop is respected;
10. environment state and cognitive belief state remain separated;
11. true-goal metadata does not leak into the inference system;
12. the system can be run reproducibly;
13. failure cases can be logged;
14. the environment remains simple enough for controlled experiments;
15. no 3D or physical hardware is required;
16. the unresolved EEG-to-goal mapping remains unassumed until owner approval.

---

# 34. CURRENT LOCKED SCENARIO SUMMARY

The approved application setting is a **simple 2D Search & Rescue research environment** containing a simulated autonomous rescue agent, candidate rescue objectives, blocked paths, hazard/risk zones, and safe or resource locations where useful. The human operator expresses goal-level intent through prerecorded motor-imagery EEG, while the autonomous system performs route planning and safe execution. EEG is not used as a low-level movement joystick. Bayesian inference accumulates uncertain EEG evidence, uncertainty determines whether the system should proceed or defer, and the human retains confirmation, override, pause, and emergency-stop authority. A* is the initial planner, explicit safety logic constrains unsafe behaviour, and the interface is a technical visualization rather than a 3D simulation. The environment may conceptually contain more than two goals, but the initial EEG decoder is binary Left-vs-Right; the exact mapping between that binary output and multiple Search & Rescue goals remains unresolved and must not be decided without explicit project-owner approval.

---

# 35. NEXT DEPENDENCY

This scenario specification provides the application assumptions needed for the next document:

**`04_SYSTEM_ARCHITECTURE.md` — Complete Technical Architecture**

The architecture document must define exact module boundaries and data flow while preserving every unresolved item identified here.
