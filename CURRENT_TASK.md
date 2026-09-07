# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Current status:** NO ACTIVE IMPLEMENTATION TASK
**Current milestone:** M6 Decoder/Calibration Runtime Adapter
**Task ID:** None
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical branch:** `main`

---

# 1. CURRENT AUTHORITY

```text
NO ACTIVE IMPLEMENTATION TASK
```

## Closed M6-T02

```text
Task ID: M6-T02
Task title: Decoder and Calibration Runtime Adapter
Status: PASS / ACCEPTED / MERGED
Accepted candidate SHA: 8a67d132045c1867ea13a5fc7f2c9a581f05f684
Merge SHA: a78c3a405b2019192bb30bd1cfc6909e336b1992
Governing decisions: D-074, D-075, D-076
```

Accepted verification:

```text
focused M6-T02 tests: 24 passed
replay/CSP+LDA/EEGNet/calibration regressions: 40 passed, 1 known PyTorch padding='same' warning
full pytest: 361 passed, 1 known PyTorch padding='same' warning
git diff --check: PASS
```

M6-T02 preserved offline prerecorded EEG / simulated real-time BCI only, exact class order `("left", "right")`, no artifact loading or persistence contract, and no model or calibrator fitting or selection. U-034, U-035, and U-036 remain unresolved.

M6-T03 is NOT STARTED / NOT AUTHORIZED. Do not begin M6-T03 automatically.