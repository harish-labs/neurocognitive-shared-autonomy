# Final Results and Analysis

## Scope and accepted evidence

This document reports the accepted M7-T02-R03 v5 evaluation only. The canonical source is `results/m7/final/m7-final-results-v5.json` (SHA-256 `b5c7cc2efdbbbab53c65d54aa77542a2e69a71c42d5bdc670e2fd8c34af2dd9b`) under execution manifest `results/m7/manifest/m7-final-execution-v6-d084-r03-final.json` (SHA-256 `f837258312adf17ec1a04079c71c5461838a4aff5096541acd993bb94da24306`) and software SHA `a1a696204a8b06263efa8bb57abc610af3f7361e`.

All empirical values below are traceable to that JSON or the accepted CSV tables generated from it. Historical v1–v4 files are preserved for audit and are not used. E1/E2/E8 use 10 protected final subjects and 303 trials. E3/E4/E6/E7/E9 and D-079 inference use 8 balanced sequential participants and 38 fixed-intent episodes. The latter are deterministic non-overlapping blocks of five acquisition-ordered trials, not natural continuous online sessions.

## E1 and E8 — EEG decoding and cross-subject heterogeneity

| Decoder | Correct / trials | Accuracy | Balanced accuracy | Macro F1 |
|---|---:|---:|---:|---:|
| CSP+LDA | 202/303 | 0.6667 | 0.6694 | 0.6649 |
| EEGNet | 182/303 | 0.6007 | 0.6092 | 0.5691 |

CSP+LDA was higher on these aggregate metrics in the frozen held-out evaluation. This is a result of this split and implementation, not evidence that it universally dominates EEGNet.

Subject-wise correctness was heterogeneous. CSP+LDA ranged from 0.5000 (subject 76) to 0.9063 (29); EEGNet ranged from 0.4167 (57) to 0.8140 (34). Some subjects favored one decoder: subject 84 scored 0.5714 with CSP+LDA and 0.7143 with EEGNet, whereas subject 29 scored 0.9063 versus 0.5938. Aggregate reporting therefore cannot replace subject-level inspection.

## E2 — Probability calibration

| Decoder | Mode | ECE | Brier |
|---|---|---:|---:|
| CSP+LDA | identity | 0.0495 | 0.2219 |
| CSP+LDA | Platt calibrated | 0.0397 | 0.2253 |
| EEGNet | identity | 0.0732 | 0.2297 |
| EEGNet | temperature calibrated | 0.0570 | 0.2253 |

For CSP+LDA, ECE decreased but Brier increased. That is a mixed calibration result and does not support a blanket improvement claim. EEGNet improved on both stored aggregate calibration metrics. Reliability used the frozen 10 equal-width bins; calibration fitting remained validation-only.

## E3 and E4 — Bayesian inference, entropy, and shared autonomy

The binary model consumes calibrated Left/Right probabilities as candidate A/B likelihood weights. It begins from `[0.5, 0.5]` unless the bounded adaptation policy supplies a future-episode prior. The posterior commits at 0.90; after five accepted updates, 0.75–0.90 triggers CONFIRM and lower confidence triggers DEFER. Shannon entropy in bits is the behavioral uncertainty description.

In the accepted sequential evaluation, C produced 32/38 correct task outcomes for CSP+LDA and 36/38 for EEGNet, compared with A's 25/38 and 23/38. The mean accepted evidence counts were 4.3421 and 4.3684 for C, versus one for A. For C, CSP+LDA modes were 19 PROCEED, 10 CONFIRM, and 9 DEFER. This makes the main trade-off explicit: accumulation and human recovery reduced wrong outcomes under the frozen protocol, but required more observations and intervention.

These outcomes include deterministic simulated-human confirmation/correction. They are not autonomous-only accuracy and do not estimate real human workload or usability.

## E5 — Planning and safety

S1–S7 are deterministic, exhaustive software scenarios and are reported descriptively:

- S1 and S2 reached the fixed goal on valid free/obstacle-aware routes.
- S3 selected the six-step zero-risk route around three traversable HIGH-risk cells rather than the shorter risky corridor at lambda 2.0.
- S4 returned `NO_SAFE_PATH` and held position.
- S5 consumed one environment-change event, replanned once, preserved the goal, and reached it.
- S6 rejected the proposed move into a risk-1.00 prohibited cell as `REPLAN_REQUIRED`; no move executed.
- S7 applied emergency STOP before movement and remained halted.

No inferential statistics are attached to these seven deterministic fixtures. They validate implementation behavior in the simulated grid, not real-world rescue safety.

## E6 — Principal A/B/C/D comparison

| Decoder | Condition | Success | Wrong/all | Mean EEG observations |
|---|---|---:|---:|---:|
| CSP+LDA | A | 25/38 | 0.3421 | 1.0000 |
| CSP+LDA | B | 38/38 | 0.0000 | 1.0000 |
| CSP+LDA | C | 32/38 | 0.1579 | 4.3421 |
| CSP+LDA | D | 32/38 | 0.1579 | 4.3684 |
| EEGNet | A | 23/38 | 0.3947 | 1.0000 |
| EEGNet | B | 38/38 | 0.0000 | 1.0000 |
| EEGNet | C | 36/38 | 0.0526 | 4.3684 |
| EEGNet | D | 36/38 | 0.0526 | 4.3947 |

All 38 approved-goal navigation runs succeeded on the frozen baseline mission map with zero risk and no hard-safety violations. That map does not stress safety; E5 provides the dedicated safety evidence.

B's perfect success is inseparable from its deterministic simulated-human correction behavior. C/D traded additional evidence and interventions for fewer wrong outcomes than direct A. D did not improve aggregate success over C for either decoder, so the results do not justify calling D uniformly best.

## E7 — Ablations

The six-condition ablation produced non-additive results. Removing calibration left CSP+LDA success unchanged at 32/38 but reduced EEGNet from 36/38 to 32/38. Removing uncertainty gating reduced CSP+LDA to 28/38 and EEGNet to 24/38. Removing adaptation or safety did not change success on the baseline free/risk-zero map. The approved `Full - Bayes` running-mean replacement reached 38/38 for both decoders, a negative result for any simplistic claim that recursive Bayes was indispensable in this setup.

That 38/38 result should be interpreted with care: the ablation retained uncertainty gating and simulated-human recovery, used a different aggregation rule by design, and was evaluated on only 38 episodes. It motivates further validation rather than post-hoc redesign.

## E7 — Robustness

R1 flattened evidence toward `[0.5, 0.5]` at epsilon 0, 0.25, 0.50, 0.75, and 1.00. R2 swapped evidence at globally selected fractions q 0, 0.10, 0.20, 0.30, and 0.40. Exactly 40 cells were stored for each family.

Responses were not uniformly monotonic. Under R1, direct A stayed unchanged until full flattening, where both decoders reached 19/38, while C/D often improved as flattening forced more simulated-human recovery. Under R2, EEGNet C/D fell at higher contradiction levels (for example D 36/38 at q=0 to 35/38 at q=0.4), but several other cells improved or fluctuated. This is evidence about the coupled system and simulated-human policy, not proof that signal degradation is beneficial.

## E9 — Adaptation

Adaptation personalized only future-episode initial priors from explicit simulated feedback after a three-event warm-up, bounded to `[0.25, 0.75]`. C versus personalized D success was unchanged: 32/38 for CSP+LDA and 36/38 for EEGNet. Mean evidence count changed slightly (4.3421 to 4.3684; 4.3684 to 4.3947). The accepted evaluation therefore demonstrates the mechanism and trajectories but not aggregate efficacy.

## D-079 statistics

| Decoder | D−A correctness effect | 95% paired-bootstrap CI | Raw p | Holm p | n |
|---|---:|---:|---:|---:|---:|
| CSP+LDA | 0.1563 | [0.0417, 0.2813] | 0.1250 | 0.1250 | 8 |
| EEGNet | 0.3167 | [0.1667, 0.4625] | 0.0313 | 0.0625 | 8 |

The unit is the subject. Confidence intervals use 10,000 paired bootstrap resamples with seed 42; p-values use all 256 exact sign flips. Neither comparison is significant after Holm correction at alpha 0.05. The positive descriptive effects should not be upgraded into confirmatory superiority claims.

## Failure analysis

The accepted schema registers preprocessing exclusions, decoder error, miscalibration, misleading Bayesian evidence, CONFIRM, DEFER, simulated override, wrong autonomous commitment, no approved goal, no-safe-path, safety rejection, prohibited hazard, replanning, emergency stop, adaptation events, robustness degradation, and provenance failure. v5 does not aggregate category counts. Inventing counts from the registry would be invalid; the limitation is retained.

Observed system-level failures include direct wrong-goal outcomes, C/D residual wrong outcomes, confidently wrong or biased subject-level behavior, non-uniform calibration, long evidence horizons, and adaptation without aggregate gain. Recoveries include explicit simulated correction, no-safe-path hold, prohibited-action veto, controlled replanning, and emergency stop.

## Evidence-bound conclusion

Within this frozen offline protocol, uncertainty-aware sequential shared autonomy changed behavior and reduced wrong outcomes relative to direct EEG for both decoder families, at the cost of substantially more evidence and simulated-human intervention. The full system did not uniformly dominate: condition B had higher task success under its intervention policy, `Full - Bayes` performed better in the ablation, calibration was mixed, adaptation did not change aggregate success, and inferential D-minus-A results were not significant after Holm correction. The result supports a nuanced systems contribution, not a universal efficacy or safety claim.
