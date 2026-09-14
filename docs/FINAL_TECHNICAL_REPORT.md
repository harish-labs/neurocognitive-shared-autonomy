# Final Technical Report

## Abstract

This project implements and evaluates a software-only shared-autonomy system in which public prerecorded motor-imagery EEG supplies uncertain evidence about one of two currently valid objectives. CSP+LDA and EEGNet decoders produce Left/Right probabilities; model-specific calibration, a binary goal-evidence boundary, sequential Bayesian inference, posterior entropy, human confirmation/override, risk-aware A*, and an explicit safety veto transform that evidence into simulated Search & Rescue behavior. The accepted evaluation used 303 protected trials from 10 held-out subjects and 38 fixed-intent sequential episodes from 8 balanced participants. CSP+LDA reached 66.7% accuracy and EEGNet 60.1%. Full-system task success was 32/38 and 36/38, versus direct-control 25/38 and 23/38, but neither D-minus-A subject-level comparison was significant after Holm correction. Calibration was mixed and adaptation did not change aggregate success. The result is a reproducible systems investigation, not evidence of live EEG, human-subject efficacy, physical-robot performance, or certified safety.

## 1. Introduction

Directly converting a noisy EEG classification into action can amplify error. Shared autonomy offers a different division of responsibility: the human determines the objective, while automation plans and executes the route subject to hard safety. The research question is whether uncertainty-aware shared autonomy improves reliability and simulated safety compared with direct EEG control.

## 2. System architecture

![Architecture](../results/m8/figures/system_architecture.png)

The repository separates EEG, models, cognition, control, autonomy, evaluation, and presentation. The dashboard is read-only and contains no fitting or hidden scientific policy.

## 3. Dataset and preprocessing

The source is the PhysioNet EEG Motor Movement/Imagery Database accessed with MNE-Python. Runs 4, 8, and 12 provide T1 imagined left fist and T2 imagined right fist; T0 is excluded from binary model data but retained in provenance. The accepted pipeline standardizes channel names, attaches the `standard_1005` montage, preserves 64 channels at 160 Hz, applies a 7–30 Hz band-pass and average reference, constructs −1.0 s to +4.0 s epochs without baseline subtraction, and rejects epochs above 150 µV peak-to-peak. No ICA or automatic interpolation is used.

The complete-source QC audit retained 68 cross-subject-eligible people from 109 sources and froze a 48/10/10 train/validation/final-test split. The final protected cohort comprised subjects 89, 16, 34, 29, 84, 57, 31, 93, 21, and 76. Subjects never cross partitions.

## 4. EEG decoders

The classical baseline uses CSP fit on approved training data followed by LDA; CSP component count is selected on validation balanced accuracy. The neural model is the accepted compact EEGNet implementation with validation-only checkpoint selection. Both preserve class order `("left", "right")` through inference.

On 303 protected trials, CSP+LDA achieved 0.6667 accuracy, 0.6694 balanced accuracy, and 0.6649 macro F1. EEGNet achieved 0.6007, 0.6092, and 0.5691. The result favors CSP+LDA on this split, while subject-wise values show substantial heterogeneity and do not support a universal ranking.

## 5. Probability calibration

CSP+LDA uses Platt-style calibration and EEGNet temperature scaling, both fit on the validation partition. Identity output remains the baseline. Reliability uses 10 equal-width confidence bins; ECE and Brier are both reported.

CSP+LDA ECE changed 0.0495→0.0397 while Brier changed 0.2219→0.2253. EEGNet ECE changed 0.0732→0.0570 and Brier 0.2297→0.2253. The former is explicitly mixed.

## 6. Goal evidence, Bayesian inference, and uncertainty

At each decision point exactly two valid candidates are exposed. Calibrated Left probability weights candidate A and Right weights B; planner cost and hazard do not alter this intent evidence. Starting from a uniform or bounded personalized prior, each accepted observation applies:

\[
P(G\mid E_{1:t}) \propto P(E_t\mid G)P(G\mid E_{1:t-1}).
\]

The controller commits at posterior ≥0.90. After five updates, confidence 0.75–0.90 requests explicit confirmation; lower confidence defers and holds. Binary Shannon entropy in bits describes uncertainty but never overrides the posterior thresholds independently.

## 7. Shared autonomy and human authority

The controller modes are WAITING, PROCEED, CONFIRM, DEFER, PAUSE, and STOP. CONFIRM never silently approves. OVERRIDE changes the human-approved goal but cannot relax safety. STOP > PAUSE > OVERRIDE > CONFIRM/RESUME > policy > planner > safety > execution. The evaluation's simulated operator is deterministic and uses hidden truth only to choose an explicit command and score outcomes; it is not a real human study.

## 8. Adaptation

Adaptation is subject- and candidate-pair-specific prior personalization. Counts begin at 1/1, update only after explicit approved feedback, require three feedback events before a nonuniform prior, and are bounded to [0.25, 0.75]. It never retrains the decoder or calibrator and never uses hidden ground truth directly.

## 9. SAR environment, planning, and safety

The environment is a deterministic four-connected 2D grid with UP, DOWN, LEFT, RIGHT, and WAIT. Risk levels are 0, 0.25, 0.50, 0.75, and prohibited 1.00. A* uses Manhattan distance and move cost `1 + 2 × destination risk`. Blocked or prohibited cells are non-traversable. Every proposed action passes through safety before environment execution. No safe path holds position without goal substitution; controlled replanning requires an explicit replacement snapshot.

## 10. Offline replay integration

The end-to-end runtime replays stored EEG-derived observations synchronously through decoder, calibration, goal evidence, Bayes, entropy, shared-autonomy authorization, goal approval, planning, safety, and environment transition. It is correctly described as Offline EEG Replay / Simulated Real-Time BCI, never live acquisition.

## 11. Experimental design and metrics

E1–E9 cover decoding, calibration, Bayesian inference, uncertainty/shared autonomy, planning/safety, A/B/C/D, ablations/robustness, cross-subject evaluation, and adaptation. A/B/C/D share frozen episodes: A Direct EEG, B Confidence-Aware, C Bayesian Shared Autonomy, D Full System. Sequential episodes are non-overlapping blocks of exactly five same-subject/same-run/same-class trials. E1/E2/E8 use n=10 and 303 trials; balanced sequential families use n=8 and 38 episodes.

Statistics use one value per subject, 10,000 paired bootstrap resamples with seed 42, two-sided exact sign flips (256 at n=8), and Holm correction within the comparison family. S1–S7 are deterministic software scenarios and receive descriptive, not inferential, reporting.

## 12. Results

| Decoder | A | B | C | D | D mean evidence |
|---|---:|---:|---:|---:|---:|
| CSP+LDA | 25/38 | 38/38 | 32/38 | 32/38 | 4.3684 |
| EEGNet | 23/38 | 38/38 | 36/38 | 36/38 | 4.3947 |

B's perfect result reflects deterministic simulated correction and does not establish minimal human burden. C/D reduced wrong outcomes relative to A but required more observations.

D-minus-A correctness effects were 0.1563 (CI [0.0417, 0.2813], raw/Holm p=0.125/0.125) for CSP+LDA and 0.3167 (CI [0.1667, 0.4625], p=0.03125/0.0625) for EEGNet. Neither cleared adjusted alpha 0.05.

## 13. Ablations and robustness

Removing uncertainty reduced success to 28/38 for CSP+LDA and 24/38 for EEGNet. Removing calibration left CSP+LDA unchanged but reduced EEGNet to 32/38. Removing adaptation or safety did not change success on the risk-zero baseline mission map. `Full - Bayes`, using the approved running-mean replacement, reached 38/38 for both—an important negative result for a universal Bayes-benefit claim.

R1 evidence flattening and R2 contradictory evidence each contain 40 frozen condition cells. Effects were non-monotonic because increased uncertainty could trigger deterministic simulated-human recovery. Robustness therefore must be interpreted jointly with intervention and latency, not task success alone.

## 14. Planning/safety scenarios

S1/S2 verified ordinary and obstacle-aware routes; S3 chose a longer zero-risk path; S4 held on no-safe-path; S5 replanned once after an explicit change; S6 vetoed a prohibited-hazard proposal; S7 halted before movement. These support deterministic implementation claims only.

## 15. Cross-subject evaluation and failure analysis

Correctness varied from 0.5000–0.9063 for CSP+LDA and 0.4167–0.8140 for EEGNet. Subjects 57 and 84 participated in single-trial E1/E2/E8 but lacked balanced sequential episodes and were not replaced. Failure taxonomy includes decoding, calibration, Bayesian, intervention, planning, safety, adaptation, robustness, and provenance categories; v5 does not aggregate category counts.

## 16. Discussion

The evidence supports a conditional systems conclusion. Shared autonomy can improve outcome reliability in this offline simulated protocol, but intervention policy and latency are central to that result. D did not beat C, B achieved the highest task success, calibration was metric-dependent, `Full - Bayes` outperformed Full, adaptation had no aggregate gain, and adjusted inferential tests were non-significant. The project contribution is the integrated, auditable decision chain and honest mapping of its trade-offs.

## 17. Limitations, ethics, and validity

The EEG is public and prerecorded; motor imagery does not encode rescue semantics directly. Sequential episodes are constructed from repeated independent trials. There is no real participant interaction, fatigue, trust, or usability evidence. The cohort is small after QC/participation filtering. The environment is simple and simulated. No physical robot, real rescue deployment, clinical use, unrestricted thought decoding, production readiness, or certified safety claim is made.

Internal-validity protections include frozen splits, validation-only fitting/calibration, no outcome-driven tuning, immutable manifests, and preserved invalid attempts. External validity remains limited to this dataset and protocol.

## 18. Reproducibility

- accepted result SHA-256: `b5c7cc2efdbbbab53c65d54aa77542a2e69a71c42d5bdc670e2fd8c34af2dd9b`
- accepted manifest SHA-256: `f837258312adf17ec1a04079c71c5461838a4aff5096541acd993bb94da24306`
- software SHA: `a1a696204a8b06263efa8bb57abc610af3f7361e`
- split: 48 train / 10 validation / 10 protected final subjects from 68 eligible
- sequential participants: 8; episodes: 38
- operational/bootstrap/R2 seed: 42

The M8 loader verifies the accepted result, execution manifest, and final-report artifact-manifest identities. It validates the artifact manifest's v5 source-result binding, then hash-checks every consumed table and reused M7 figure before presentation, without importing experiment execution or model fitting. The dashboard's separate deterministic demo begins at a fixed calibrated-probability representation—not decoder or protected EEG output—and then exercises the accepted authorization, planning, per-action safety, and environment-execution interfaces through a terminal simulated goal.

## 19. Conclusion and future work

The project implements a complete, claim-bounded EEG-to-shared-autonomy prototype and shows that uncertainty-aware control changes system outcomes, latency, and intervention. Results are mixed rather than uniformly favorable, which defines the next questions: live prospective validation, real human interaction, larger multi-dataset cohorts, stronger calibration and uncertainty methods, longitudinal personalization, dynamic environments, and physical-system safety verification. Those are future studies, not current capabilities.
