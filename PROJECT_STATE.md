# PROJECT_STATE.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Live Project State

**Purpose:** Authoritative live record of what is actually true now about the project.
**Workflow:** ChatGPT + Project Owner + Codex + Git/GitHub
**Last updated:** 2026-09-08

---

# 1. STATUS AT A GLANCE

```text
Project phase:
M1-T01 through M1-T10 accepted and merged.
M4-T01 through M4-T05 accepted and merged.
M5-T01 through M5-T04 accepted and merged.
PRE-M6-R01 through PRE-M6-R06 accepted and merged.
PRE-M6-R07A — Master Authority Reconciliation: PASS / ACCEPTED / MERGED.
PRE-M6-R07B — Secondary Documentation Reconciliation: PASS / ACCEPTED / MERGED.
Final Pre-M6 audit: PASS / CLOSED.
M6-T01: PASS / ACCEPTED / MERGED / CLOSED.
M6-T02: PASS / ACCEPTED / MERGED / CLOSED.
M6-R01: PASS / ACCEPTED / MERGED / CLOSED.
M6-T03: PASS / ACCEPTED / MERGED / CLOSED.
M6-T04: AUTHORIZED / IMPLEMENTATION NOT STARTED.

Current module:
M6 — End-to-End EEG Integration

Current task:
M6-T04 — Intent Authorization -> Navigation Bridge

Task status:
ACTIVE IMPLEMENTATION TASK

Authorized task branch:
task/m6-t04-intent-navigation-bridge

M6-T04 authorization base:
afae16fac406d32a106af341171b6dc64520b04d

M6-T03 accepted candidate:
fe35d8de5966a439fbde5b999bd35deedf82f7ff

M6-T03 software merge:
a4a6a309dd94aaa110ee6367ff3e40ba13c9a456

M6-T03 verification run:
34195749631

M6-T03 verification:
373 passed, 1 warning

M6-T03 warning:
known PyTorch padding='same' convolution warning

Verification workflow:
.github/workflows/verify.yml

Latest approved scientific/architectural decision register entry:
D-076 — M6 Decoder/Calibrator Runtime Injection Contract

Latest valid reportable experiment:
None yet
```

The project remains an **offline prerecorded EEG / simulated real-time BCI** system. No live EEG, physical robot, certified safety, human-subject result, or end-to-end EEG-driven mission-execution claim is authorized.

# 2. ACCEPTED IMPLEMENTATION STATE

M6-T01, M6-T02, and M6-T03 are PASS / ACCEPTED / MERGED / CLOSED. M6-T03 provides the accepted deterministic calibrated replay-to-one-bounded-Bayesian-episode integration and preserves exact candidate/posterior/provenance semantics.

M6-R01 is PASS / ACCEPTED / MERGED / CLOSED and provides exact-ref GitHub Actions verification through `.github/workflows/verify.yml` using the existing `requirements.txt` and Python 3.12.

Accepted M5 interfaces already provide:

```text
shared-autonomy policy decisions
human confirmation / override / pause / stop state
policy-to-human authorization bridge
fresh authorization-gated zero-movement navigation start
interruptible one-step navigation
replacement-snapshot replanning
```

M6-T04 must compose these accepted interfaces rather than redesign them.

# 3. CURRENT AUTHORITY — M6-T04

The Project Owner explicitly approved proceeding with M6-T04 on 2026-09-08.

M6-T04 is the sole active implementation task.

Authorized objective:

```text
BayesianReplayEpisodeResult
  -> accepted BayesianEpisodeResult structural handoff
  -> accepted binary uncertainty
  -> accepted shared-autonomy decision
  -> accepted human-interaction authorization bridge
  -> NavigationRuntime.start_navigation() only when fresh authorization permits
```

The M6-T04 execution boundary is **zero movement**. It may establish a `READY` navigation plan but must not call `advance_one_step()` or any replanning API.

Authorized implementation files:

```text
src/control/intent_navigation_bridge.py
tests/test_intent_navigation_bridge.py
```

Do not modify accepted M1/M4/M5/M6-T01/T02/T03 modules without separate reviewer-approved remediation.

M6-T04 must preserve:

```text
exact binary A/B candidate identity
accepted posterior and update count from M6-T03
accepted entropy calculation
accepted PROCEED / WAITING / CONFIRM / DEFER thresholds
human authority and confirmation semantics
exact symbolic mission-goal identity
fresh execution authorization
zero movement at navigation start
safety veto before every later environment transition
```

M6-T05 and M6-T06 remain NOT STARTED / NOT AUTHORIZED. M7 is not authorized.

# 4. REMAINING UNRESOLVED DECISIONS

```text
U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
```

These experimental-analysis decisions do not block the currently authorized M6-T04 composition task and must remain unresolved.

# 5. CLAIM / SCOPE BOUNDARIES

Preserve:

```text
public prerecorded EEG / offline replay / simulated real-time BCI only
no live EEG or hardware claim
human determines WHAT; AI determines HOW
accepted binary EEG evidence semantics; no fabricated direct K-goal decoder
no threshold or Bayesian-policy changes
no reportable experiments or efficacy claims
no M6-T05/M6-T06/M7 implementation without separate authorization
```
