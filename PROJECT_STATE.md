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

Current module:
M6 Bayesian Episode Integration

Current task:
None

Task status:
NO ACTIVE IMPLEMENTATION TASK

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

M6-T01 and M6-T02 are PASS / ACCEPTED / MERGED / CLOSED. M6-T03 is PASS / ACCEPTED / MERGED / CLOSED. Its approved deterministic calibrated replay-to-Bayesian episode semantics remain unchanged. No scientific or architectural decision was changed by the merge.

M6-R01 is PASS / ACCEPTED / MERGED / CLOSED and provides exact-ref GitHub Actions verification through .github/workflows/verify.yml using the existing requirements.txt and Python 3.12.

# 3. CURRENT AUTHORITY

There is no active implementation task. M6-T04 is NOT STARTED / NOT AUTHORIZED. Do not implement or authorize M6-T04 without separate approval.

Preserve offline prerecorded EEG / simulated real-time BCI only, no live EEG or hardware claim, and no fabricated results.

# 4. REMAINING UNRESOLVED DECISIONS

U-034 — final A/B/C/D component matrix
U-035 — robustness perturbation levels
U-036 — inferential-statistics policy
