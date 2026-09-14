# CURRENT_TASK.md

## Current Codex Implementation Authority

**Current status:** ACTIVE / AUTHORIZED
**Current milestone:** M8 — Dashboard & Portfolio Release
**Task ID:** M8-T01
**Task title:** Final Dashboard, Scientific Reporting, Demo & Portfolio Release
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical starting branch / SHA:** `main` / `0b279403ed8f5af8cb33b4e7916e512680ecc32e`
**Task branch:** `task/m8-t01-final-presentation-release`

---

# 1. AUTHORIZATION

On 2026-09-14 the Project Owner explicitly authorized M8-T01 as one consolidated presentation, reporting, demo, and portfolio task. M7 remains PASS / ACCEPTED / MERGED / CLOSED, and no M7 task is active.

M8-T01 may consume accepted M1–M7 implementation and result artifacts. It may not alter their scientific semantics or regenerate protected results.

---

# 2. ACCEPTED READ-ONLY SCIENTIFIC SOURCES

- accepted result: `results/m7/final/m7-final-results-v5.json`
- accepted result SHA-256: `b5c7cc2efdbbbab53c65d54aa77542a2e69a71c42d5bdc670e2fd8c34af2dd9b`
- accepted execution manifest: `results/m7/manifest/m7-final-execution-v6-d084-r03-final.json`
- accepted manifest SHA-256: `f837258312adf17ec1a04079c71c5461838a4aff5096541acd993bb94da24306`
- accepted executable/reporting software SHA: `a1a696204a8b06263efa8bb57abc610af3f7361e`

`results/m7/**` is immutable/read-only. Historical v1–v4 artifacts remain audit records and are not accepted reportable sources. Protected experiments E1–E9 must not be rerun.

---

# 3. AUTHORIZED DELIVERABLES

M8-T01 must deliver, within the Project Owner-approved scope:

1. a read-only accepted-result/provenance loader under `src/app/`;
2. a Streamlit dashboard covering overview, architecture, decoder results, calibration, Bayesian inference and uncertainty, A/B/C/D shared autonomy, planning and safety, robustness and ablations, cross-subject evaluation, adaptation, statistics, failure cases and limitations, provenance, and a deterministic presentation demo;
3. traceable M8-only presentation figures under `results/m8/figures/`;
4. final reconciliations of `docs/23_RESULTS_AND_ANALYSIS.md` and `docs/24_DISCUSSION_AND_FINDINGS.md`;
5. `docs/FINAL_TECHNICAL_REPORT.md`;
6. a final release `README.md`;
7. `docs/PORTFOLIO_AND_RESUME_POSITIONING.md`;
8. a runnable walkthrough package in `demo/`;
9. focused M8 tests, full regression verification, dashboard smoke verification, claim audit, provenance/hash audit, and forbidden-file diff audit.

---

# 4. SCIENTIFIC FREEZE

M8 is a presentation consumer only. It must not retrain/refit models or calibrators; rerun protected inference or E1–E9; access protected EEG to create new findings; change preprocessing, QC, eligibility, splits, episodes, thresholds, probability semantics, Bayes, adaptation, A/B/C/D membership, robustness, statistics, planning, risk, safety, or human authority; or select results post hoc.

Empirical values must come from the accepted v5 machine-readable result/tables. Explanatory or deterministic demo fixtures must be labeled non-empirical and must not become reportable experiments.

---

# 5. FILE BOUNDARY

Primary allowed paths:

```text
CURRENT_TASK.md
PROJECT_STATE.md
TODO.md
README.md
requirements.txt
src/app/**
tests/test_m8_*.py
tests/test_dashboard_*.py
docs/23_RESULTS_AND_ANALYSIS.md
docs/24_DISCUSSION_AND_FINDINGS.md
docs/25_FUTURE_WORK.md (status reconciliation only if needed)
docs/FINAL_TECHNICAL_REPORT.md
docs/PORTFOLIO_AND_RESUME_POSITIONING.md
demo/**
results/m8/**
```

The following remain read-only:

```text
src/eeg/**
src/models/**
src/cognitive/**
src/control/**
src/autonomy/**
src/evaluation/**
config.yaml
results/m7/**
accepted model/checkpoint/calibrator artifacts
```

A production/scientific defect requiring a change to a read-only path is a STOP condition and must be reported separately.

---

# 6. CLAIM BOUNDARY

Use: public prerecorded EEG, Offline EEG Replay, Simulated Real-Time BCI, software-only research prototype, and simulated Search & Rescue.

Do not claim live EEG acquisition, unrestricted thought reading, a real human-subject study, physical-robot performance, real rescue deployment, clinical efficacy, certified safety, or production readiness. Preserve negative, mixed, and non-significant findings and actual sample sizes (`n=10` protected subjects for E1/E2/E8 where applicable; `n=8` balanced sequential participants for E3/E4/E6/E7/E9/statistics).

---

# 7. REQUIRED VERIFICATION

Run focused M8 tests, `python -m compileall src tests`, the complete pytest suite, and a non-interactive Streamlit startup smoke. Verify accepted hashes, prove `results/m7/**` and read-only production paths are unchanged, audit every headline number against accepted sources, inspect claim language, run `git diff --check`, and leave a clean committed candidate.

Expected pre-M8 accepted baseline: `511 passed, 16 warnings`. The local checked-in `.venv` interpreter may not be usable; use an available verified Python environment and report the exact command/runtime.

---

# 8. COMPLETION / STOP

Do not merge to `main`, close M8, or mark M8 accepted. Return one candidate commit for ChatGPT scientific/repository review, then stop.

Stop as BLOCKED if accepted artifacts are missing or disagree, a result claim cannot be traced, protected experiments would need to be rerun, a read-only production/science change is required, a new scientific decision is required, or a requested claim exceeds the accepted evidence.
