from pathlib import Path

p = Path("PROJECT_STATE.md")
text = p.read_text(encoding="utf-8")

def repl(old: str, new: str) -> None:
    global text
    if old not in text:
        raise SystemExit(f"Missing PROJECT_STATE text: {old[:120]!r}")
    text = text.replace(old, new, 1)

repl(
"""`DECISIONS.md` resolves U-001 through U-009 as D-031 through D-039. The affected numbered methodology documents are aligned on canonical `main`:

```text
docs/06_DATASET_AND_DATA_PIPELINE.md
docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md
docs/15_IMPLEMENTATION_BLUEPRINT.md
```

No scientific/documentation alignment blocker remains for drafting M1-T03. Implementation remains unauthorized until `CURRENT_TASK.md` contains an explicitly approved active ticket.""",
"""`DECISIONS.md` resolves U-001 through U-009 as D-031 through D-039 and U-010 through U-012 as D-040 through D-042.

The approved preprocessing and split/evaluation methodology is aligned on canonical project documents, including:

```text
docs/06_DATASET_AND_DATA_PIPELINE.md
docs/08_EEG_SIGNAL_PROCESSING_AND_ML.md
docs/15_IMPLEMENTATION_BLUEPRINT.md
docs/17_EXPERIMENTAL_DESIGN.md
docs/18_METRICS_AND_EVALUATION.md
```

No active implementation ticket exists. A narrow split-manifest implementation still requires explicit Project Owner authorization in `CURRENT_TASK.md`."""
)

repl(
"""EEG Data Loader:
- src/eeg/loader.py implemented
- tests/test_loader.py implemented
- 10 loader tests passed
- real EEGBCI subject 1 runs 4 / 8 / 12 loaded successfully
- 64 channels verified
- 160 Hz verified
- T0 / T1 / T2 annotations observed
- standard_1005 montage attached
- local reusable MNE cache used
- no preprocessing or modeling implemented

EEG Visualization / Inspection:
- src/eeg/visualization.py implemented
- tests/test_visualization.py implemented
- 16 total loader + visualization tests passed
- real EEGBCI subject 1 runs 4 / 8 / 12 inspected successfully
- raw traces, PSD, sensor layout, and annotation overview generated
- 64 channels verified
- 160 Hz verified
- T0 / T1 / T2 present
- standard_1005 montage preserved
- no preprocessing or modeling implemented
- offline prerecorded EEG inspection only""",
"""EEG Data Loader:
- src/eeg/loader.py implemented
- tests/test_loader.py implemented
- 10 loader tests passed
- real EEGBCI subject 1 runs 4 / 8 / 12 loaded successfully
- 64 channels, 160 Hz, T0/T1/T2, and standard_1005 montage verified

EEG Visualization / Inspection:
- src/eeg/visualization.py implemented
- tests/test_visualization.py implemented
- loader + visualization regression coverage passed at acceptance
- real subject 1 runs 4 / 8 / 12 inspected with raw traces, PSD, sensors, and annotation overview

EEG Preprocessing / Epochs:
- src/eeg/preprocessing.py and src/eeg/epochs.py implemented
- tests/test_preprocessing.py and tests/test_epochs.py implemented
- final targeted preprocessing/epoch review: 9 passed
- final loader regression review: 10 passed
- real subject 1 runs 4 / 8 / 12 smoke-verified
- 7–30 Hz filter, average reference, 64-channel order, 160 Hz, -1.0-to-4.0 s epochs, baseline=None, T0 exclusion, 150 µV rejection with reason/threshold provenance, and *-epo.fif persistence contract verified
- high real-data rejection counts were preserved as an observation, not used to change D-035"""
)

repl(
"""Current state:

```text
None currently blocking repository consistency for M1-T03 preparation.
```

M1-T03 remains blocked from implementation only because no active `CURRENT_TASK.md` ticket has been explicitly approved. Do not invent technical blockers before actual implementation.""",
"""Current state:

```text
M1-T03 has no open implementation blocker after acceptance.
Split-manifest implementation is not active.
```

The next split-manifest task is blocked only by the absence of a separately approved active `CURRENT_TASK.md` ticket. Do not invent technical blockers before actual implementation."""
)

repl(
"""## Dataset semantics

```text
T0 = rest
T1 = imagined left fist
T2 = imagined right fist
```""",
"""## Split / validation protocol

```text
Within-subject:
deterministic class-stratified 60/20/20 at original-trial level

Primary cross-subject:
fixed subject-held-out 70/15/15

Held-out assignment:
seed 42
versioned frozen subject manifest before model fitting
for a full eligible 109-subject cohort: 76 train / 16 validation / 17 final test

Protection:
no subject, original-trial, or derived-window leakage across protected partitions
final-test subjects are excluded from fitting/tuning/calibration/adaptation
```

## Dataset semantics

```text
T0 = rest
T1 = imagined left fist
T2 = imagined right fist
```"""
)

repl(
"""EEG → preprocessing:
NOT STARTED

Preprocessing → decoder:
NOT STARTED""",
"""EEG loader → preprocessing / epochs:
PASS for the accepted M1-T03 path

Preprocessing / epochs → split manifest:
NOT STARTED / NOT AUTHORIZED

Split manifest → decoder:
NOT STARTED"""
)

repl(
"""E8 — Cross-subject evaluation:
BLOCKED""",
"""E8 — Cross-subject evaluation:
PROTOCOL APPROVED / IMPLEMENTATION NOT STARTED"""
)

p.write_text(text, encoding="utf-8")
