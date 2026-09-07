# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no implementation task is currently authorized.
**Current status:** ACTIVE IMPLEMENTATION TASK
**Current milestone:** M6 Offline EEG Replay Integration
**Task ID:** M6-T01
**Task title:** Deterministic Offline EEG Epoch Replay
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Repository instructions:** `AGENTS.md`
**Canonical branch:** `main`
**Last updated:** 2026-09-07

---

# 1. ACTIVE TASK — M6-T01

```text
Task ID: M6-T01
Task title: Deterministic Offline EEG Epoch Replay
Phase: M6 Offline EEG Replay Integration
Task branch: task/m6-t01-offline-eeg-replay
Status: ACTIVE IMPLEMENTATION TASK
Governance authorization commit: this commit
```

## Authority

D-074 governs this task. One accepted prerecorded EEG epoch/trial produces one decoder evidence observation. Replay order must be deterministic and auditable. M6-T01 must not introduce sliding-window, overlapping-window, or continuous-stream EEG evidence semantics.

## Authorized implementation scope

```text
- consume already accepted prerecorded/processed EEG epochs;
- replay them in deterministic order;
- expose exactly one epoch/trial per replay observation;
- preserve subject identity;
- preserve run identity;
- preserve original trial/epoch identity;
- preserve deterministic ordering information;
- expose sufficient replay provenance for later downstream audit;
- reject malformed, ambiguous, duplicated, or structurally invalid replay input;
- terminate cleanly at end of replay;
- synchronous deterministic implementation only.
```

## Forbidden scope

```text
Do not run CSP+LDA, EEGNet, calibration, Bayesian inference, D-051/D-052 goal-evidence mapping, candidate A/B selection, shared-autonomy policy, human confirmation, planning, navigation, movement, replanning, adaptation updates, experiments, UI, asynchronous workers/threads/timers/event buses, or new scientific policy.
```

Preserve offline prerecorded EEG / simulated real-time BCI only; no live EEG claim, no hardware requirement, no direct K-goal decoder, and U-034/U-035/U-036 unresolved.

## Required later verification

```text
- focused M6-T01 replay tests;
- existing relevant EEG regression tests;
- full pytest regression suite;
- deterministic replay-order verification;
- malformed-input/fail-closed tests;
- duplicate/identity integrity tests;
- clean end-of-replay behavior.
```

## Stop conditions

Stop and report if implementation requires a new scientific, architectural, dataset-semantic, or evaluation decision. No new dependency is authorized.

After implementing M6-T01, stop. Do not begin a later M6 task automatically.
