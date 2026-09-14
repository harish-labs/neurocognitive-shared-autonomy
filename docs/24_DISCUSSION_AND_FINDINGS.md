# Final Discussion and Findings

## Answer to the research question

The accepted evidence gives a qualified answer: under the frozen offline EEG replay and deterministic simulated-human protocol, uncertainty-aware sequential shared autonomy produced fewer wrong task outcomes than direct EEG control for both decoder families, but the benefit came with longer evidence accumulation and intervention. The full system was not uniformly superior, and the subject-level D-minus-A comparisons did not remain statistically significant after Holm correction.

That is scientifically more useful than a simple winner statement. The project demonstrates how decoding, probability quality, belief accumulation, uncertainty gates, human authority, planning, and hard safety interact—and where those interactions can fail.

## What worked

- Both decoders produced above-chance aggregate held-out performance, with CSP+LDA higher on the frozen aggregate accuracy, balanced accuracy, and macro-F1 metrics.
- Model-specific calibration reduced aggregate ECE for both decoders; EEGNet also improved Brier Score.
- Sequential C/D conditions reduced wrong outcomes relative to direct A under the defined simulated-human policy.
- Uncertainty gating was behaviorally consequential: removing it sharply reduced success in the ablation.
- The planner chose a longer zero-risk path when the weighted risk cost justified it.
- No-safe-path, prohibited-hazard rejection, one-event replanning, and emergency stop behaved as specified in deterministic S1–S7 validation.
- Provenance controls detected and preserved invalid v1–v4 artifacts before v5 acceptance.

## What did not work or remained mixed

- EEGNet did not outperform CSP+LDA on aggregate held-out decoding.
- CSP+LDA calibration improved ECE but worsened Brier Score, so calibration benefit depends on the metric.
- D did not improve task success over C for either decoder.
- Prior personalization did not change aggregate success and slightly increased mean evidence count.
- The `Full - Bayes` running-mean ablation achieved 38/38 for both decoders, so the data do not establish recursive Bayes as the best aggregation method in this protocol.
- Robustness curves were non-monotonic because degradation could trigger simulated-human recovery; they do not support a simple graceful-degradation narrative.
- Neither formal D-minus-A comparison was significant after Holm correction.

## Decoder and calibration interpretation

CSP+LDA's 66.7% accuracy versus EEGNet's 60.1% is compatible with the value of compact classical methods on limited and heterogeneous motor-imagery EEG. It does not show that neural models are intrinsically worse. Subject 84 favored EEGNet, while subject 29 strongly favored CSP+LDA, illustrating model-by-subject interaction.

Calibration must be judged separately from classification. Lower ECE alone did not mean uniformly better probabilities for CSP+LDA because Brier worsened. EEGNet's improvement on both metrics is cleaner, but ECE remained nonzero and subject-level calibration varied.

## Bayesian benefit and cost

Bayesian accumulation provides a coherent latent-goal belief and an auditable posterior trajectory. In C it accompanied fewer wrong outcomes than A, but the causal contribution cannot be isolated from human correction and threshold policy by that comparison alone. The higher mean evidence count—about 4.3 rather than 1—represents real decision latency within the offline episode model.

The ablation result is especially important: removing recursive Bayes while retaining a running mean, uncertainty thresholds, and simulated-human behavior increased success. That does not invalidate the Bayesian implementation; it shows that the chosen evidence model and small fixed horizon are not automatically optimal.

## Uncertainty and human authority

Entropy affected whether the controller proceeded, requested confirmation, or deferred. This satisfies the operational meaning of uncertainty-aware control. It does not make entropy a correctness guarantee: a posterior may be confident and wrong. Explicit confirmation/override provides recovery, while PAUSE and STOP preserve human authority and safety retains low-level veto.

Condition B's 38/38 success reveals both a strength and a limitation. Immediate confidence screening plus deterministic correction can recover every episode in this fixture, but it externalizes burden to a simulated operator. No result here measures actual response time, fatigue, trust, or usability.

## Planning and safety

The A* planner is deliberately conventional; the contribution is its placement after human goal approval and before independent safety checking. Soft risk is traded against distance, whereas blocked and prohibited cells are never made cheap enough to traverse. The S1–S7 suite verified these contracts, including holding position when no safe route exists.

These are implementation and simulated-environment findings. They cannot establish certified safety, robustness to real sensors, or effectiveness in actual Search & Rescue.

## Robustness and generalization

Evidence flattening and contradiction affected conditions differently. In some C/D cells, worse evidence caused more successful simulated correction, producing apparent improvement. This interaction is a warning against treating task success alone as a pure signal-robustness metric. Future work should report intervention burden jointly and test with real participants or a richer human-response model.

Cross-subject heterogeneity is substantial, with trial correctness near chance for several subjects and much higher for others. The final protected cohort had 10 subjects, but balanced sequential inference had only 8. This small sample constrains statistical power and external validity.

## Adaptation

The implemented adaptation is bounded prior personalization, not model retraining or advanced adaptive control. It correctly used explicit feedback, warm-up, bounds, isolation, and reset. Its lack of aggregate success gain is a valid negative result. More episodes, longitudinal data, or different personalization targets would require new prospective approval and evaluation.

## Validity and limitations

Internal validity is strengthened by subject-held-out splits, validation-only calibration, frozen policies, exact provenance, protected-test gating, and immutable invalid-run history. Construct validity remains limited because Left/Right motor imagery is an interface signal for a binary candidate choice, not rescue-semantic cognition. External validity is limited by one public prerecorded dataset, offline repeated-trial episodes, deterministic simulated human behavior, and a simple 2D environment.

The work makes no claim of live EEG acquisition, unrestricted thought reading, real-human efficacy, clinical benefit, physical-robot performance, real rescue deployment, production readiness, or certified safety. Failure categories exist, but accepted v5 does not provide aggregate failure-category counts.

## Scientific contribution

The contribution is an end-to-end, modular, leakage-aware research platform that joins two EEG decoders, model-specific calibration, an explicit evidence-to-goal boundary, sequential latent-goal inference, behavioral uncertainty, meaningful human authority, risk-aware planning, hard-safety veto, and reproducible multi-level evaluation. Its strongest lesson is conditional: shared autonomy can convert uncertain neural evidence into more reliable simulated task behavior, but performance depends on intervention policy, aggregation semantics, subject variability, and latency. The architecture makes those dependencies visible rather than hiding them behind one score.
