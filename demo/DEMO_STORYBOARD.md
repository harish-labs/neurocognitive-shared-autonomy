# Demo Storyboard

| Shot | Dashboard section | Visual focus | Required narration |
|---:|---|---|---|
| 1 | Project Overview | research question and four metrics | software-only, prerecorded EEG |
| 2 | Architecture | full left-to-right pipeline | human WHAT / AI HOW |
| 3 | EEG / Decoder Results | aggregate and subject metrics | 303 trials, n=10, CSP higher here |
| 4 | Calibration | table and M7 reliability plot | CSP mixed; EEGNet improved both metrics |
| 5 | Bayesian Intent & Uncertainty | explanatory posterior trace | fixture, not empirical result |
| 6 | Shared Autonomy / A-B-C-D | success/latency figure | 38 episodes, n=8, simulated human |
| 7 | Planning & Safety | route and S1–S7 evidence | soft risk vs hard veto |
| 8 | Robustness & Ablations | six ablations and R1/R2 plots | non-monotonic coupled behavior |
| 9 | Cross-Subject Evaluation | subject bars | heterogeneity; n=10 vs n=8 |
| 10 | Adaptation | prior trajectory | mechanism worked; no aggregate gain |
| 11 | Statistics | paired effects and adjusted p | neither significant after Holm |
| 12 | Failure Cases & Limitations | failure registry | counts not aggregated in v5 |
| 13 | Reproducibility / Provenance | hashes and SHAs | v5 accepted; v1–v4 audit only |
| 14 | Interactive Demo | fixed probabilities → posterior/entropy → authorization → plan → safety checks → executed positions → terminal goal | deterministic explanatory fixture; no decoder/calibrator or protected EEG output |

## Recording checklist

- Use a 16:9 browser window and 125% or lower display scaling.
- Collapse long tables after showing their headers and key rows.
- Keep the “not empirical” demo warning visible.
- Do not hide mixed/negative findings.
- End with the limitations, not a deployment claim.
- Record narration externally; the repository intentionally contains no fabricated video file.
