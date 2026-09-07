# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no implementation task is currently authorized.
**Current status:** NO ACTIVE IMPLEMENTATION TASK
**Current milestone:** M6 Offline EEG Replay Integration
**Task ID:** None
**Task title:** Deterministic Offline EEG Epoch Replay
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Repository instructions:** `AGENTS.md`
**Canonical branch:** `main`
**Last updated:** 2026-09-07

---

# 1. CURRENT AUTHORITY

```text
NO ACTIVE IMPLEMENTATION TASK
```

## Authority

M6-T01 is PASS / ACCEPTED / MERGED. D-074 remains the controlling offline replay evidence contract. One accepted prerecorded EEG epoch/trial produces one decoder evidence observation; replay order is deterministic and auditable; sliding-window, overlapping-window, and continuous-stream EEG evidence semantics remain excluded.

## M6-T01 Closed Verification

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

## M6-T01 Scope Record

```text
Do not run CSP+LDA, EEGNet, calibration, Bayesian inference, D-051/D-052 goal-evidence mapping, candidate A/B selection, shared-autonomy policy, human confirmation, planning, navigation, movement, replanning, adaptation updates, experiments, UI, asynchronous workers/threads/timers/event buses, or new scientific policy.
```

Accepted verification: focused replay tests 10 passed; relevant EEG regressions 29 passed; full pytest 337 passed with 1 known PyTorch padding warning. Preserve offline prerecorded EEG / simulated real-time BCI only; no live EEG claim, no hardware requirement, no direct K-goal decoder, and U-034/U-035/U-036 unresolved.

## M6-T01 Accepted Result

```text
- focused M6-T01 replay tests;
- existing relevant EEG regression tests;
- full pytest regression suite;
- deterministic replay-order verification;
- malformed-input/fail-closed tests;
- duplicate/identity integrity tests;
- clean end-of-replay behavior.
```

## M6 Boundary

Stop and report if implementation requires a new scientific, architectural, dataset-semantic, or evaluation decision. No new dependency is authorized.

M6-T01 is PASS / ACCEPTED / MERGED. M6-T02 is NOT STARTED / NOT AUTHORIZED. No later M6 task may begin automatically.
