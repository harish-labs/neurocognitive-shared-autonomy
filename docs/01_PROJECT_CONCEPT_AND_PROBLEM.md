# 01_PROJECT_CONCEPT_AND_PROBLEM.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Concept, Motivation & Problem Definition

**Document ID:** A-02  
**Document class:** Master Authority Supporting Document  
**Authority level:** Subordinate to `MASTER_PROJECT_SPEC.md`; authoritative for project concept, motivation, and problem definition  
**Status:** Approved-project baseline with explicitly unresolved items preserved  
**Purpose:** Explain why the project exists, what real problem it addresses, why each major conceptual element is necessary, how the Search & Rescue scenario instantiates the problem, and what distinguishes the project from a normal EEG classifier, autonomous-navigation demo, or visualization project.

---

# 0. AUTHORITY AND INTERPRETATION RULE

This document elaborates the project concept defined in `MASTER_PROJECT_SPEC.md`.

It must be read under the following rules:

1. `MASTER_PROJECT_SPEC.md` remains the highest project authority.
2. This document may explain and expand the approved concept, but it may not redefine the project's architecture, scope, research direction, terminology, or technical boundaries.
3. No missing scientific or implementation detail may be invented here.
4. Items that remain unresolved in the master specification remain unresolved in this document.
5. If this document appears to conflict with `MASTER_PROJECT_SPEC.md`, the master specification takes precedence unless the project owner explicitly approves a change and records it through the project change-control process.
6. The Search & Rescue scenario is an application layer for the approved technical system; it is not permission to redesign the EEG, Bayesian, uncertainty, shared-autonomy, safety, or adaptive components.
7. Historical material from the earlier CoSA-U concept may be used only where it supports non-conflicting reasoning about shared autonomy, uncertainty, safety, evaluation, and human control. The current EEG-based Search & Rescue project supersedes the earlier keyboard/joystick-centred architecture.

---

# 1. PROJECT IDENTITY

## 1.1 Locked project title

**NeuroCognitive Shared Autonomy for Search & Rescue — EEG-Based Intent Decoding with Bayesian Goal Inference and Uncertainty-Aware Adaptive Control**

This title is inherited from `MASTER_PROJECT_SPEC.md` and is treated as locked unless explicitly changed by the project owner.

## 1.2 Project concept in one sentence

The project studies whether noisy motor-imagery EEG can be converted into safer and more reliable goal-level control by combining neural decoding, calibrated probabilities, sequential Bayesian intent inference, uncertainty-aware shared autonomy, explicit safety constraints, autonomous path planning, human override, and adaptation in a simple simulated Search & Rescue environment.

## 1.3 Project type

The project is a:

- software-first system,
- research-oriented technical investigation,
- simulated BCI/shared-autonomy system,
- human–AI decision-making system under uncertainty,
- computational-intent-modelling project,
- safety-aware autonomy project,
- and experimental comparison framework.

It is **not** primarily:

- a game,
- a 2D visualization project,
- a 3D simulation project,
- a generic path-planning demo,
- a generic EEG classification benchmark,
- a physical robotics project,
- a medical device,
- or a live BCI deployment.

---

# 2. WHY THIS PROJECT EXISTS

## 2.1 Core motivation

The project is built around a fundamental problem in human–AI autonomy:

> A machine may receive incomplete, noisy, or uncertain evidence of what a human intends, yet the machine must still decide whether to act, how much autonomy to assume, when to defer, and how to prevent unsafe behaviour.

The earlier shared-autonomy research direction already identified the broader problem as one of balancing:

- autonomy versus human control,
- task efficiency versus safety,
- early assistance versus uncertainty about intent,
- and general behaviour versus adaptation to the individual user.

The current project keeps that research logic but grounds the human-intent signal in **motor-imagery EEG** rather than keyboard or joystick input.

## 2.2 Why EEG makes the problem technically meaningful

EEG-based motor-imagery decoding is not perfectly reliable. The system therefore cannot responsibly assume that every predicted class represents a certain human intention.

The current project treats neural decoding as a source of **probabilistic evidence**, not unquestionable command truth.

This is central to the concept:

```text
EEG prediction ≠ certain human intention
```

Instead:

```text
EEG prediction
      ↓
probabilistic evidence
      ↓
sequential belief update
      ↓
uncertainty estimate
      ↓
decision about how much autonomous assistance is appropriate
```

This transformation—from a noisy classifier output into a controlled human–AI decision process—is the main conceptual reason the project is broader than a normal BCI classifier.

---

# 3. THE REAL PROBLEM BEING SOLVED

## 3.1 Direct BCI-control problem

A simplistic BCI system could operate as follows:

```text
EEG signal
   ↓
classifier predicts LEFT or RIGHT
   ↓
convert prediction directly into machine action
```

The problem is that if the classifier is wrong, the machine can immediately perform the wrong action.

In a low-risk toy interface, that may only create inconvenience.

In a safety-relevant task such as Search & Rescue, a wrong action can conceptually correspond to:

- moving toward the wrong rescue objective,
- entering a hazardous region,
- selecting the wrong route,
- committing too early to an incorrectly inferred intention,
- or requiring the human to repeatedly correct the autonomous system.

The project therefore does **not** assume that neural classification should directly equal autonomous execution.

## 3.2 The project problem statement

The project investigates how to make EEG-based human intent usable for autonomous assistance when:

- neural predictions are imperfect,
- the operator's intended goal is not directly observable by the machine,
- evidence may be ambiguous,
- the environment may contain hazards or blocked paths,
- the system must preserve human authority,
- and unsafe autonomous execution must be prevented even when the AI is confident.

The approved formulation is:

> **Can uncertainty-aware shared autonomy improve the reliability and safety of EEG-based intent control compared with direct brain-computer control?**

## 3.3 General shared-autonomy formulation

At a more general level, the conceptual problem can be stated as:

> How should an intelligent autonomous system assist a human when the human's intended goal is uncertain, the environment may be unsafe, and excessive autonomous intervention can itself reduce human control?

The current project answers that broader problem specifically through an EEG-based Search & Rescue system.

---

# 4. WHY THE SEARCH & RESCUE SCENARIO IS USED

## 4.1 Scenario purpose

Search & Rescue provides a concrete safety-relevant application in which:

- there can be multiple candidate objectives,
- some areas may be hazardous,
- some paths may be blocked,
- route choice matters,
- wrong-goal commitment matters,
- uncertainty matters,
- and human override has a natural justification.

This gives the technical architecture a meaningful environment without requiring physical robotics or a visually complex simulator.

## 4.2 What the scenario is not

The Search & Rescue setting is **not** being chosen because the project is mainly about disaster graphics, maps, or rescue-game design.

It exists to make the following technical questions concrete:

- What goal does the operator intend?
- How confident is the system about that intent?
- Should the AI act now or wait for more evidence?
- Should the AI ask for confirmation?
- Which safe route should be used?
- Should an unsafe action be blocked even if the current goal estimate is confident?
- How should the system respond when the human corrects or overrides it?

## 4.3 Visualization principle

The environment should remain a **simple technical 2D simulation**.

It may visually represent:

- the rescue agent,
- candidate rescue targets/victims,
- safe zones,
- medical/resource locations where used,
- blocked cells/paths,
- hazard or risk regions,
- and planned routes.

The purpose of visualization is to make the algorithmic decision process observable and understandable.

No 3D model is required.

---

# 5. CENTRAL HUMAN–AI RESPONSIBILITY DIVISION

The project's central design principle is:

> **The human determines WHAT objective is intended. The AI determines HOW to achieve that objective safely.**

This division is fundamental to the meaning of shared autonomy in this project.

## 5.1 Human role

The human/operator is conceptually responsible for:

- generating the neural intent signal through the motor-imagery task represented in the public EEG dataset,
- remaining the source of intended goal/choice information,
- confirming when the system is uncertain where confirmation is required,
- overriding an incorrect autonomous decision,
- pausing the system,
- and issuing an emergency stop when necessary.

The human is **not** conceptually removed from control after the EEG classifier produces a prediction.

## 5.2 Autonomous-system role

The autonomous system is responsible for:

- decoding EEG evidence,
- representing the decoder output probabilistically,
- calibrating probabilities,
- accumulating evidence over time,
- maintaining a belief/posterior over intended goal or choice,
- estimating uncertainty,
- selecting the appropriate autonomy level,
- planning a route to the inferred goal,
- considering risk/hazard information,
- rejecting unsafe actions,
- replanning when necessary,
- and recording the interaction for evaluation.

The autonomous system must not treat its own inference as infallible.

---

# 6. WHY DIRECT EEG CONTROL IS INSUFFICIENT

Direct EEG-to-action control is intentionally included as a comparison condition because it exposes the central weakness the proposed system is designed to investigate.

A direct system effectively assumes:

```text
current prediction → immediate action
```

The proposed system instead introduces several protective reasoning stages:

```text
current prediction
      ↓
calibrated probability
      ↓
sequential evidence
      ↓
Bayesian posterior
      ↓
uncertainty estimate
      ↓
act / confirm / defer / stop
      ↓
safety filtering
      ↓
autonomous execution
```

The project does not assume in advance that this larger system will outperform direct control on every metric. That must be tested experimentally.

A valid outcome may include trade-offs—for example, greater safety at the cost of slower task completion.

---

# 7. WHY PROBABILITY CALIBRATION IS INCLUDED

A neural model may output a high numerical probability while still being poorly calibrated.

Therefore, the project distinguishes:

- **classifier probability**, and
- **trustworthy confidence for decision-making**.

Probability calibration is included because the downstream shared-autonomy system will make behavioural decisions based on confidence and uncertainty.

If the probabilities are systematically overconfident or underconfident, the autonomy controller may:

- act too early,
- defer too often,
- ask for unnecessary confirmation,
- or incorrectly treat ambiguous EEG evidence as certain.

The exact calibration method is not yet locked and must be selected later through the appropriate technical/research decision process.

---

# 8. WHY BAYESIAN GOAL INFERENCE IS INCLUDED

## 8.1 Intent is treated as latent

The project does not assume that one EEG prediction perfectly reveals the operator's intended goal.

Instead, intention is treated as a **latent state** that must be inferred from imperfect evidence.

The system therefore maintains a belief over possible goal/intention hypotheses.

The conceptual update is:

```text
posterior ∝ likelihood × prior
```

or, in project notation:

```text
P(G | EEG evidence) ∝ P(EEG evidence | G) P(G)
```

The exact formal implementation will be defined in the dedicated Bayesian Goal Inference document.

## 8.2 Why sequential updating matters

A single EEG window or trial can be noisy.

Repeated evidence may provide a more stable intention estimate.

For example, conceptually:

```text
Initial belief:
Goal A = 0.50
Goal B = 0.50

New EEG evidence slightly supports Goal B
      ↓
Posterior shifts toward Goal B

More supporting evidence arrives
      ↓
Posterior becomes stronger
```

This is why the system is designed around **sequential Bayesian evidence accumulation** rather than a single hard classifier label.

## 8.3 What Bayesian inference is not allowed to mean

The word **Bayesian** may only be used if the implemented system performs an actual probabilistic prior/likelihood/posterior update.

It must not be used merely as a label for heuristic confidence smoothing.

---

# 9. WHY UNCERTAINTY IS CENTRAL

The system needs to know not only **what it currently predicts**, but also **how uncertain that prediction is**.

The approved uncertainty mechanism includes entropy over the inferred goal distribution.

Conceptually:

```text
low entropy   → stronger belief / lower ambiguity
high entropy  → weaker belief / greater ambiguity
```

Uncertainty must have a behavioural consequence.

A system cannot legitimately be called **uncertainty-aware** if it calculates an uncertainty number only for display.

The intended behaviour is conceptually:

- high confidence / low uncertainty → greater autonomous execution,
- medium confidence → request confirmation or reduce autonomous authority,
- low confidence / high uncertainty → defer, pause, or ask the human.

Exact threshold values are **not yet approved** and must not be invented.

---

# 10. WHY SHARED AUTONOMY IS INCLUDED

## 10.1 Meaning in this project

Shared autonomy means that neither the human nor the autonomous system exclusively determines all behaviour.

The project separates:

- **human intent/authority**, and
- **machine execution/planning assistance**.

The AI should provide more help when intent is sufficiently clear and less help when intent is ambiguous.

Human override remains possible.

## 10.2 Why this is preferable to pure autonomy

A fully autonomous system would not meaningfully test the BCI or human-intent component.

A fully manual/direct BCI system would not test how autonomous assistance can compensate for uncertainty and execution complexity.

Shared autonomy is therefore the mechanism that allows both sides of the research problem to coexist:

```text
Human intention
      +
Autonomous capability
      +
Uncertainty management
      +
Safety constraints
```

## 10.3 Human authority

Autonomous assistance must not be interpreted as removing user agency.

The final system must preserve meaningful human control through the approved mechanisms such as:

- confirmation,
- override,
- pause,
- and emergency stop.

---

# 11. WHY EXPLICIT SAFETY IS INCLUDED

## 11.1 Safety is separate from goal inference

Correctly inferring a goal does not guarantee that every route or action toward that goal is safe.

Therefore:

```text
correct intent ≠ automatically safe action
```

The safety layer is conceptually independent of the neural decoder and Bayesian goal inference.

## 11.2 Safety behaviour

The planned system can represent safety through mechanisms such as:

- blocked-area constraints,
- hazardous/risk regions,
- unsafe-action rejection,
- replanning,
- uncertainty-triggered deferral,
- and emergency stopping.

The safety controller must materially affect behaviour.

## 11.3 Safety claims

The project may discuss **simulated safety-aware or safety-critical decision-making** only to the extent supported by implemented, measurable safety constraints.

It must not imply:

- certified real-world safety,
- clinical safety,
- physical rescue-system certification,
- or frontier-model alignment research.

---

# 12. WHY ADAPTATION IS INCLUDED

The project includes adaptation from human corrections where scientifically justified.

The intended concept is that repeated interaction may provide information about the user/system relationship, such as:

- prior preference,
- reliability estimates,
- correction history,
- or decision/confidence thresholds.

However, the **exact adaptation mechanism is not yet locked**.

Therefore this document does not claim a specific adaptive-learning algorithm.

The phrase **adaptive control** in the project title must eventually be supported by the actual implemented adaptation.

If the final system only adapts priors, reliability estimates, or thresholds, the documentation must state that precisely and must not imply advanced adaptive-control theory.

---

# 13. EXAMPLE END-TO-END SCENARIO

The following example illustrates the approved concept without resolving the currently open binary-to-multi-goal mapping problem.

Assume the current task presents the operator with an approved set of selectable rescue objectives.

1. Public prerecorded motor-imagery EEG is replayed as the simulated BCI input.
2. EEG preprocessing produces the required trial/window representation.
3. The decoder produces class probabilities rather than only a hard label.
4. Calibration adjusts the confidence representation.
5. Bayesian inference accumulates evidence across observations.
6. The current posterior indicates which available rescue objective is more likely to be intended.
7. Entropy/uncertainty is computed.
8. If confidence is insufficient, the system does not blindly commit; it may defer or request confirmation according to the approved shared-autonomy policy.
9. If confidence is sufficient, the autonomous planner computes a route toward the inferred rescue objective.
10. The route/action is checked against blocked paths, hazards, and safety constraints.
11. Unsafe actions are rejected or replanned.
12. The operator can confirm, override, pause, or stop.
13. Where adaptation is implemented, corrections may update the relevant user/system parameters.
14. The entire process is logged for experimental evaluation.

This is the conceptual system the project is intended to study.

---

# 14. IMPORTANT UNRESOLVED ISSUE: BINARY EEG VS MULTIPLE RESCUE GOALS

The initial approved EEG task is:

**Left-hand motor imagery vs right-hand motor imagery**

using the planned PhysioNet EEG Motor Movement/Imagery dataset direction and initially discussed runs **4, 8, and 12**.

The Search & Rescue scenario has also conceptually included more than two possible goals, such as:

- Victim A,
- Victim B,
- medical/resource point,
- safe zone.

A binary Left/Right decoder cannot automatically select among an arbitrary number of goals.

This remains an explicit unresolved design issue.

Previously identified possible directions include:

1. only two active selectable goals at a time,
2. hierarchical/sequential binary selection,
3. later multiclass EEG,
4. EEG controls an abstract binary decision such as priority A/B while autonomous logic manages the broader mission structure.

**No option is approved merely because it appears in this list.**

The project owner must explicitly approve the mapping mechanism before implementation or documentation treats one as final.

Until then:

- diagrams must not imply a fixed mapping,
- examples must not silently assume four-class EEG,
- evaluation design must not assume a multiclass BCI,
- and ChatGPT/Codex must not invent a solution to this issue.

---

# 15. WHAT MAKES THIS DIFFERENT FROM A NORMAL EEG CLASSIFIER

A normal EEG classification project may end at:

```text
EEG
  ↓
preprocessing
  ↓
classifier
  ↓
accuracy / F1
```

This project does not end there.

Its intended chain is:

```text
EEG
  ↓
preprocessing
  ↓
CSP + LDA / EEGNet
  ↓
calibrated probabilities
  ↓
Bayesian intent inference
  ↓
uncertainty
  ↓
shared-autonomy decision
  ↓
safety filtering
  ↓
autonomous planning
  ↓
human intervention / adaptation
  ↓
end-to-end task evaluation
```

Therefore the classifier is one subsystem inside a broader decision architecture.

The research value comes from studying how uncertain neural evidence should affect autonomous behaviour, not merely from maximizing EEG classification accuracy.

---

# 16. WHAT MAKES THIS DIFFERENT FROM A NORMAL ROBOT-NAVIGATION PROJECT

A normal navigation project may assume the destination is already known and focus on finding a route.

This project introduces an additional uncertainty layer:

> **The autonomous system does not initially know with certainty what the human wants it to do.**

It must first infer the intended objective from neural evidence and decide whether that inference is reliable enough to act upon.

Only then does path planning become meaningful.

Therefore the conceptual hierarchy is:

```text
INTENT PROBLEM
      ↓
UNCERTAINTY PROBLEM
      ↓
AUTONOMY-ALLOCATION PROBLEM
      ↓
SAFETY PROBLEM
      ↓
NAVIGATION PROBLEM
```

This order is important.

The project must not be reduced to “we built a rescue robot simulator.”

---

# 17. WHAT MAKES THIS DIFFERENT FROM A VISUALIZATION PROJECT

The 2D environment is an experimental and explanatory substrate.

Its purpose is to show:

- the current agent state,
- candidate objectives,
- route decisions,
- hazards,
- safety interventions,
- and the effects of human/AI decisions.

The technical contribution is not the rendering.

A simple visualization is preferred if it supports rigorous experimentation and makes the system understandable.

No project quality criterion depends on 3D realism.

---

# 18. INTENDED ACADEMIC / TECHNICAL CONTRIBUTION

The project is intended to demonstrate a complete technical argument rather than a collection of unrelated features.

The central contribution being investigated is the integration of:

- motor-imagery EEG decoding,
- classical and neural decoding comparison,
- calibrated probabilistic output,
- Bayesian latent-intent inference,
- uncertainty-aware autonomy selection,
- shared human–AI control,
- explicit simulated safety constraints,
- autonomous navigation,
- adaptation where implemented,
- and rigorous end-to-end evaluation.

The project should allow experiments that answer questions such as:

- Does sequential intent inference help compared with acting on one EEG prediction?
- Does uncertainty-aware deferral reduce wrong autonomous commitments?
- Does explicit safety logic reduce simulated unsafe actions?
- What efficiency cost is introduced by increased caution?
- How does performance change under EEG variability/noise?
- How does the system behave for unseen subjects or subject-wise evaluation settings?
- Which components actually contribute value according to ablation studies?

These questions must be formalized in the dedicated Objectives, Scope & Research Questions document rather than treated as final hypotheses here.

---

# 19. RESEARCH PHILOSOPHY

## 19.1 Research quality over feature count

The project must prefer:

- clear hypotheses,
- defensible methodology,
- explicit baselines,
- valid train/test separation,
- calibration,
- ablations,
- robustness testing,
- failure analysis,
- reproducibility,
- and honest limitations

over adding more technologies.

## 19.2 Negative or mixed results are valid

The proposed full system must not be engineered so that it is guaranteed to win.

A result such as:

```text
greater safety but slower completion
```

can be scientifically meaningful.

The project must report the trade-off rather than hide it.

## 19.3 No fabricated evidence

No metric, improvement percentage, success rate, safety result, or model comparison may be claimed before it is actually produced by the implementation and experiment pipeline.

---

# 20. STRATEGIC MOTIVATION WITHOUT DISTORTING THE RESEARCH

The project was selected as a flagship because the broader academic interests being targeted include:

- computational cognitive science,
- cognitive AI,
- computational neuroscience,
- neurotechnology / BCI,
- brain-inspired AI,
- HCI / human–AI interaction,
- behavioural AI,
- embodied AI,
- autonomous systems,
- robotics,
- adaptive intelligence,
- bio-inspired AI,
- complex systems,
- safety-critical AI,
- and privacy engineering.

The project is especially intended to add visible evidence in areas that were not already strongly demonstrated by the existing project profile, including:

- EEG/BCI,
- probabilistic cognition,
- Bayesian reasoning,
- human-intent modelling,
- uncertainty-aware autonomy,
- shared autonomy,
- safety-aware autonomous decision-making,
- and rigorous interdisciplinary experimentation.

However, these strategic reasons must never be used to justify adding a technology or claim that does not support the actual research problem.

The project must remain coherent as a technical investigation even if all admissions-related motivation is removed.

---

# 21. SOFTWARE-FIRST CONSTRAINT

The approved project is intentionally software-first.

It does **not** require:

- live EEG acquisition,
- an EEG headset,
- a physical robot,
- a drone,
- IoT hardware,
- ROS 2,
- Gazebo,
- C++,
- or a 3D environment

for the core system to be valid.

ROS 2, Gazebo, C++, PPO/RL, SNNs, multiclass BCI, and advanced uncertainty methods remain possible later extensions only if explicitly approved and if the core system already works.

---

# 22. TECHNOLOGIES THAT MUST NOT BE ADDED WITHOUT A RESEARCH REASON

The project must not add the following merely to make the technology stack appear larger:

- LLMs,
- RAG,
- Gemini/OpenAI API,
- blockchain,
- AWS/cloud architecture,
- Kubernetes,
- IoT hardware,
- physical EEG hardware,
- physical robots,
- complex microservices,
- unnecessary computer vision,
- elaborate 3D visualization,
- mobile applications.

A later addition is allowed only if a clear technical/research requirement appears, the project owner approves the change, and the change is recorded.

---

# 23. TERMINOLOGY AND CLAIM BOUNDARIES

## 23.1 NeuroCognitive

Allowed because the project combines:

- neural EEG signals, and
- computational modelling of latent intention/belief.

It must not imply complete modelling of human cognition or the brain.

## 23.2 EEG-based intent decoding

Allowed only in the constrained project meaning: motor-imagery EEG is used as evidence within an intention/goal-selection framework.

It must not imply arbitrary thought reading.

## 23.3 Bayesian

Allowed only if actual Bayesian updating is implemented.

## 23.4 Uncertainty-aware

Allowed only if uncertainty is calculated and changes system behaviour.

## 23.5 Shared autonomy

Allowed only if both human authority/input and autonomous execution influence behaviour.

## 23.6 Safety-critical / AI safety

Allowed only in the limited simulated context of explicit measurable safety constraints and safe autonomous decision-making under uncertainty.

## 23.7 Adaptive control

Must describe the actual adaptation implemented.

Do not imply advanced adaptive-control theory unless implemented.

## 23.8 Real-time

The current project uses:

**offline EEG replay / simulated real-time BCI**

It must not claim live EEG acquisition.

---

# 24. KNOWN ASSUMPTIONS AND LIMITATIONS AT THE CONCEPT STAGE

The project currently assumes:

- use of public prerecorded EEG,
- motor-imagery decoding as the initial BCI task,
- a software-only simulation,
- a simple 2D Search & Rescue environment,
- an autonomous planner operating on a simplified environment model,
- explicit simulated hazards/safety constraints,
- and human confirmation/override represented through the software interaction layer.

Known limitations include:

- no physical rescue deployment,
- no live BCI acquisition,
- no clinical claim,
- no unrestricted real-world intent decoding,
- inter-subject EEG variability,
- simplified environment dynamics,
- simplified representation of human intention,
- and the unresolved mapping between the initial binary EEG task and a potentially multi-goal Search & Rescue scenario.

These limitations are features of the current research scope and must not be hidden.

---

# 25. HISTORICAL DESIGN NOTE

An earlier project blueprint, **CoSA-U — Cognitive Shared Autonomy Under Uncertainty**, proposed a related system based on noisy human keyboard/joystick commands and stronger ROS 2/C++ robotics integration.

The current project retains compatible conceptual ideas from that work, including:

- uncertain human intent,
- Bayesian reasoning,
- uncertainty-aware assistance,
- explicit safety,
- shared control,
- adaptation,
- ablation,
- robustness testing,
- and rigorous evaluation.

However, the older architecture does **not** override the current project.

The present project is specifically:

- EEG/BCI-based,
- Search & Rescue themed,
- software-first,
- built around CSP/LDA + EEGNet + calibration + Bayesian goal inference + uncertainty + shared autonomy + safety + planning,
- and does not require ROS 2/C++/Gazebo as core components.

No future implementation agent may silently revert to the older keyboard/joystick architecture.

---

# 26. RELATIONSHIP TO THE NEXT DOCUMENTS

This document answers:

> **Why does the project exist and what problem are we solving?**

It does **not** finalize every experimental or implementation detail.

The next authority document, `02_OBJECTIVES_SCOPE_AND_RESEARCH_QUESTIONS.md`, must define:

- the primary objective,
- secondary objectives,
- formal research questions,
- hypotheses,
- project scope,
- out-of-scope boundaries,
- minimum viable system,
- intended final system,
- optional extensions,
- expected outputs,
- and project success criteria.

The later `03_SEARCH_AND_RESCUE_SCENARIO.md` must define the application environment in detail, but it must not resolve the binary EEG-to-multiple-goal problem without explicit project-owner approval.

---

# 27. CURRENT AI-ASSISTED WORKFLOW TERMINOLOGY

The approved tooling terminology for future project work is now:

- **ChatGPT** — project brain / research director / reviewer,
- **Project owner** — final authority and approval layer,
- **Codex** — implementation engineer,
- **Git/GitHub** — persistent source of truth.

This terminology change does not alter the project concept, architecture, methodology, or scientific direction.

The expected control loop is:

```text
ChatGPT researches / designs / reviews
        ↓
Project owner approves
        ↓
Codex implements / tests / runs
        ↓
Git/GitHub records actual work
        ↓
ChatGPT reviews actual code / tests / results
        ↓
Project owner approves next action
```

ChatGPT may recommend changes but may not treat them as approved without project-owner approval.

Codex may report a scientific or architectural problem but may not independently change the research direction or silently simplify the system.

---

# 28. CONCEPT COMPLETION STATEMENT

At the concept level, the project is defined as a study of **safe shared autonomy under uncertain EEG-derived human intent**, instantiated in a simple simulated Search & Rescue environment.

Its conceptual novelty is not any one individual algorithm.

It is the integration and evaluation of the full reasoning chain:

```text
NEURAL EVIDENCE
      ↓
PROBABILISTIC DECODING
      ↓
BAYESIAN INTENT BELIEF
      ↓
UNCERTAINTY
      ↓
HUMAN–AI AUTONOMY DECISION
      ↓
EXPLICIT SAFETY
      ↓
AUTONOMOUS EXECUTION
      ↓
HUMAN CORRECTION / ADAPTATION
```

The project succeeds conceptually only if these components remain connected to the same research problem rather than becoming separate demonstrations.

The unresolved binary-EEG-to-multiple-goal mapping must remain unresolved until explicitly approved.

---

# 29. SOURCE-PRESERVATION NOTE

This document was consolidated from the transferred project context and the current master project specification. It intentionally preserves the newer EEG-based Search & Rescue direction as authoritative while retaining only non-conflicting conceptual reasoning from the earlier CoSA-U shared-autonomy research blueprint.

No external research findings, new algorithms, new datasets, new hardware requirements, or new project objectives have been added in this document.

