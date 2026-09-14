# M8 presentation artifacts

These files are presentation-only. They do not contain a new experiment or a rerun of E1–E9.

Generate them deterministically with:

```powershell
python -m src.app.generate_figures
```

Empirical figures read only the accepted M7 result package through `src/app/result_loader.py`:

- `decoder_comparison.png` — accepted E1 aggregate table; 303 trials from 10 protected subjects.
- `abcd_comparison.png` — accepted E6 A/B/C/D table; 38 episodes from 8 sequential participants.
- `cross_subject_summary.png` — accepted E8 subject-wise table; 10 protected subjects.

Explanatory figures are explicitly labeled non-empirical:

- `system_architecture.png` — architecture diagram.
- `sar_route_safety_demo.png` — fixed-probability fixture executed through the accepted Bayes, uncertainty, shared-autonomy, human-authorization, A*, safety, and environment interfaces; no decoder/calibrator or protected EEG is invoked.

Accepted input identities:

- result SHA-256: `b5c7cc2efdbbbab53c65d54aa77542a2e69a71c42d5bdc670e2fd8c34af2dd9b`
- manifest SHA-256: `f837258312adf17ec1a04079c71c5461838a4aff5096541acd993bb94da24306`
- generating scientific software SHA: `a1a696204a8b06263efa8bb57abc610af3f7361e`

Calibration, robustness, and adaptation views reuse the accepted figures in `results/m7/figures/` without modifying them.
