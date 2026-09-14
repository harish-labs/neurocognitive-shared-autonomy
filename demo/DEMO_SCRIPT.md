# Eight-Minute Demo Script

## 0:00–0:40 — Problem

“A noisy EEG classification should not become an action automatically. This project asks whether explicit uncertainty, human authority, autonomous planning, and hard safety can make EEG-based control more reliable in a simulated task.”

Show **Project Overview** and state: “The human determines what goal is intended; the AI determines how to reach it safely.”

## 0:40–1:20 — Architecture

Show **Architecture**. Walk left to right from prerecorded PhysioNet EEG through decoding, calibration, Bayes, entropy, shared autonomy, goal approval, A*, and the safety veto. Say that the dashboard is read-only.

## 1:20–2:05 — EEG and calibration

Show **EEG / Decoder Results**. “On 303 protected trials from 10 subjects, CSP+LDA reached 66.7% accuracy and EEGNet 60.1%. Subjects varied substantially.”

Show **Calibration**. “CSP ECE improved but Brier worsened; EEGNet improved on both. Calibration was not uniformly beneficial.”

## 2:05–2:55 — Bayes and uncertainty

Show **Bayesian Intent & Uncertainty**. Explain the fixed candidate A/B boundary, posterior update, entropy, 0.90 commitment, and five-update CONFIRM/DEFER horizon. Label the displayed trace explanatory, not empirical.

## 2:55–3:45 — A/B/C/D

Show **Shared Autonomy / A-B-C-D**. “Direct A succeeded in 25/38 and 23/38 episodes. C/D reached 32/38 and 36/38, but needed about 4.4 observations. B reached 38/38 because the deterministic simulated operator corrected uncertain decisions—this is not free autonomy or real-human evidence.”

## 3:45–4:35 — Planning and safety

Show **Planning & Safety**. Explain soft risk versus hard prohibition. Mention the longer safe S3 route, S4 no-safe-path hold, S5 single replan, S6 prohibited-cell veto, and S7 emergency stop. State that these are deterministic simulated scenarios.

## 4:35–5:20 — Robustness and ablations

Show **Robustness & Ablations**. “Removing uncertainty hurt both decoders. Removing Bayes with the pre-approved running-mean replacement performed better. Robustness was non-monotonic because degraded evidence could trigger simulated-human recovery.”

## 5:20–6:00 — Subjects and adaptation

Show **Cross-Subject Evaluation** and emphasize variability and n=10 versus n=8. Show **Adaptation**: “The bounded prior changed for some subject streams, but aggregate success did not improve.”

## 6:00–6:40 — Statistics and failures

Show **Statistics**. “Neither D-minus-A comparison was significant after Holm correction.” Show **Failure Cases & Limitations** and name offline EEG, repeated-trial episodes, simulated human, simple 2D environment, and missing aggregate taxonomy counts.

## 6:40–7:20 — Provenance

Show **Reproducibility / Provenance**. Point to the result hash, manifest hash, software SHA, split/QC/episode provenance, and preserved invalid v1–v4 history.

## 7:20–8:00 — Deterministic mission demo

Show **Interactive Demo**. “Fixed calibrated evidence is accumulated by the production Bayesian interface; entropy falls; the policy proceeds to victim A; production A* generates the displayed route. This fixture explains the interfaces and is not an empirical result.”

Close: “The contribution is not a claim that the full system always wins. It is an auditable platform showing when uncertain neural evidence, human intervention, and safety-aware autonomy help—and what they cost.”
