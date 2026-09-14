# Portfolio and Resume Positioning

All wording below is bounded to accepted M7 evidence. Use “public prerecorded EEG,” “Offline EEG Replay / Simulated Real-Time BCI,” “software-only research prototype,” and “simulated Search & Rescue.”

## One-line resume bullet

Built and evaluated a reproducible Python research prototype that converts public prerecorded motor-imagery EEG into calibrated Bayesian goal belief, uncertainty-aware shared autonomy, risk-aware A* navigation, and hard-safety-controlled 2D Search & Rescue behavior.

## Two-to-three bullet resume version

- Implemented leakage-aware PhysioNet EEGBCI pipelines with CSP+LDA and EEGNet, validation-only Platt/temperature calibration, and subject-held-out evaluation (303 protected trials; 10 subjects).
- Integrated binary goal evidence, sequential Bayesian inference, posterior entropy, explicit CONFIRM/OVERRIDE/PAUSE/STOP authority, risk-aware A*, and action-level safety veto in a deterministic 2D SAR prototype.
- Built reproducible E1–E9 evaluation with A/B/C/D conditions, six ablations, two robustness families, exact paired inference, immutable provenance, a Streamlit dashboard, and explicit negative-result/claim auditing.

## LinkedIn project entry

**NeuroCognitive Shared Autonomy for Search & Rescue** — A software-only research prototype exploring how uncertain motor-imagery EEG can be converted into goal-level shared autonomy. I implemented public PhysioNet EEG loading/preprocessing, CSP+LDA and EEGNet decoders, model-specific calibration, sequential Bayesian belief, Shannon-entropy control modes, human authority, A* planning, hard safety, offline replay, and reproducible evaluation. On the frozen protected evaluation, CSP+LDA achieved 66.7% accuracy and EEGNet 60.1%; full-system success improved descriptively over direct control but formal D-minus-A comparisons were not significant after Holm correction. The project uses prerecorded EEG and simulated SAR—no live acquisition, real-human efficacy, physical robot, or certified-safety claim.

## Short portfolio card

An end-to-end, evidence-traceable investigation of shared autonomy under uncertain EEG intent: dual decoders, calibration, Bayesian belief, behavioral uncertainty, human authority, risk-aware planning, safety veto, robustness, ablations, and a 14-section Streamlit dashboard.

## Detailed portfolio description

The project asks whether a machine should act immediately on a noisy neural classification. It separates human objective selection from autonomous route execution. A binary Left/Right motor-imagery decoder selects between two currently valid candidates; calibrated probabilities update a latent-goal posterior; entropy and thresholds determine PROCEED, CONFIRM, or DEFER; explicit human commands retain authority; and a risk-aware A* planner proposes actions that an independent safety controller may veto.

The final evaluation is protected and auditable: 109 public source subjects passed through fixed QC, yielding 68 eligible and a frozen 48/10/10 subject split. E1/E2/E8 used 303 trials from all 10 protected subjects; balanced sequential families used 38 episodes from 8 participants. Results were deliberately reported without a composite score: calibration was mixed, adaptation did not improve aggregate success, and the full system did not uniformly win. This combination of implementation depth and negative-result discipline is the central portfolio value.

## Research-style abstract

We implemented a modular shared-autonomy prototype combining public prerecorded motor-imagery EEG, CSP+LDA and EEGNet decoding, model-specific calibration, sequential Bayesian binary-goal inference, posterior entropy, explicit human authority, risk-aware A*, and action-level safety constraints. The protected evaluation comprised 303 trials from 10 held-out subjects and 38 sequential episodes from 8 balanced participants. CSP+LDA exceeded EEGNet on aggregate decoding; calibration effects were metric-dependent; C/D reduced wrong outcomes relative to direct A under a deterministic simulated-human policy but increased evidence latency; adaptation did not change aggregate success; and D-minus-A subject-level tests were not significant after Holm correction. The work supports a reproducible systems investigation, not live-BCI, real-human, clinical, robot-deployment, or certified-safety claims.

## Interview explanation

“I treated EEG output as uncertain evidence, not a command. The hardest architectural choice was preserving semantics: calibrated P(class|EEG) enters only a documented binary candidate boundary, while planning risk never contaminates intent inference. The system accumulates evidence, uses posterior entropy to decide whether to proceed or ask the human, then plans to the approved goal and checks every move against hard constraints. I also froze the final test protocol and preserved failed result versions. The interesting outcome was mixed: shared autonomy improved descriptive task outcomes over direct control, but required more evidence, adaptation added no aggregate gain, a no-Bayes ablation did better, and adjusted statistical tests were non-significant.”

## Technical highlights

- MNE-Python EEGBCI data and traceable epoch provenance
- CSP+LDA and compact EEGNet with leakage-safe fitting boundaries
- validation-only Platt and temperature calibration; ECE/Brier reliability reporting
- explicit binary evidence-to-goal semantics and sequential Bayesian updates
- Shannon entropy with operational PROCEED/CONFIRM/DEFER behavior
- deterministic human command identity, duplicate protection, pause/stop precedence
- bounded explicit-feedback prior personalization
- Gymnasium 2D SAR, risk-aware A*, hard safety, and controlled replanning
- E1–E9, A/B/C/D, six ablations, R1/R2 robustness, subject-level bootstrap/sign-flip/Holm
- fail-closed result provenance, immutable audit artifacts, full automated tests, Streamlit presentation

## Claim-safe numerical highlights

- 303 protected EEG trials across 10 held-out subjects
- CSP+LDA: 66.7% accuracy; EEGNet: 60.1%
- Full D success: 32/38 and 36/38 versus direct A: 25/38 and 23/38 under the frozen deterministic simulated-human protocol
- D-minus-A Holm-adjusted p-values: 0.125 and 0.0625; neither significant at 0.05
- adaptation C→D aggregate success unchanged for both decoder families

Always include the sample/protocol qualifier when using these values.

## Do not claim

- live EEG acquisition or online participant control
- arbitrary thought or semantic-intention decoding
- a real human-subject study or measured workload/usability
- a deployed rescue robot or real rescue effectiveness
- clinical/medical efficacy
- certified or guaranteed safety
- production-ready BCI
- uniform superiority of the full system, Bayes, calibration, or adaptation
