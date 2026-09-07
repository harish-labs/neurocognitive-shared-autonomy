# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Current status:** ACTIVE IMPLEMENTATION TASK
**Current milestone:** M6 Decoder/Calibration Runtime Adapter
**Task ID:** M6-T02
**Task title:** Decoder and Calibration Runtime Adapter
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical branch:** `task/m6-t02-decoder-calibration-adapter`
**Authorization base:** `f72324d32505d736e7a19b5716d5ee13612c6a9a`

---

# 1. ACTIVE TASK - M6-T02

```text
Task ID: M6-T02
Task title: Decoder and Calibration Runtime Adapter
Status: ACTIVE IMPLEMENTATION TASK
Governing decisions: D-074, D-075, D-076
```

## Authorized input boundary

```text
ReplayObservation
canonical source mne.Epochs
already-instantiated, already-fitted decoder
already-instantiated, already-fitted calibrator
```

## Authorized responsibilities

Locate and verify the exact canonical source epoch before inference; preserve canonical channel/order, sampling, MNE Info, timing, replay identity, and provenance; validate decoder/calibrator compatibility and outputs; execute exactly one approved model-specific path; and return deterministic immutable-provenance runtime evidence.

Approved paths:

```text
CSP+LDA: CspLdaDecoder.predict_proba(single_epoch)
         -> already-fitted PlattScalingCalibrator.predict_proba(raw_probabilities)

EEGNet: EEGNetDecoder.predict_logits(single_epoch)
        -> already-fitted TemperatureScalingCalibrator.predict_proba(raw_logits)
```

Class order remains `("left", "right")`. Output provenance may include replay index, canonical trial identity, subject ID, run ID, trial index, source file, event code, semantic label, event sample, model family, class labels, raw decoder output, and calibrated probabilities.

## Required fail-closed validation

Reject replay/source identity or epoch-data mismatch, unsupported or mismatched decoder/calibrator families, class-order changes, invalid row counts, non-finite outputs, probabilities outside [0,1], and probabilities that do not sum to one within reasonable floating-point tolerance. Preserve existing CSP+LDA and EEGNet validators without weakening or bypassing them.

## Forbidden scope

```text
No training, fitting, refitting, model selection, component/checkpoint selection, calibration tuning/evaluation, artifact loading/deserialization/persistence, new preprocessing or epoch semantics, raw EEG loading, continuous-stream interpretation, Bayesian inference, D-051/D-052 goal mapping, evidence accumulation, shared autonomy, human authorization, planning, navigation, adaptation, experiments, metrics/results claims, UI, asynchronous execution, or new dependencies.
```

Preserve D-074, D-075, D-076, offline prerecorded EEG / simulated real-time BCI only, no live EEG or physical hardware claim, one accepted replay epoch/trial per decoder evidence observation, and unresolved U-034/U-035/U-036.

## Required verification

Focused M6-T02 tests, M6-T01 replay regression tests, CSP+LDA regression tests, EEGNet regression tests, calibration regression tests, full pytest, and `git diff --check`.

Stop if work requires a new scientific, dataset-semantic, model/calibrator persistence, decoder, calibration, class-order, replay-identity, dependency, or downstream M6-T03 decision.

M6-T03 is NOT STARTED / NOT AUTHORIZED. Do not implement M6-T02 until work begins on this authorized task; do not begin M6-T03.