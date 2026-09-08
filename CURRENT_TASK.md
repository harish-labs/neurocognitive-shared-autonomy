# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Current status:** ACTIVE REMEDIATION TASK
**Current milestone:** M6 Verification Infrastructure Remediation
**Task ID:** M6-R01
**Task title:** Reproducible Python Verification CI
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical branch:** `task/m6-r01-reproducible-verification-ci`
**Authorization base:** `f3aa0a5313fb6224332d689ae37ce622d2e9ceb9`

---

# 1. ACTIVE TASK — M6-R01

```text
Task ID: M6-R01
Task title: Reproducible Python Verification CI
Status: AUTHORIZED / IMPLEMENTATION NOT STARTED
Purpose: establish repository-controlled reproducible Python verification because the current Windows host cannot execute Python and no usable WSL/Docker environment is available.
```

M6-R01 is the sole active implementation/remediation task.

## M6-T03 suspended verification state

```text
Task: M6-T03 — Calibrated EEG Evidence -> Bayesian Decision Episode
Status: BLOCKED — runtime verification environment unavailable
Reviewed candidate: fe35d8de5966a439fbde5b999bd35deedf82f7ff
Merge authorization: NO
```

M6-T03 is not closed. Its approved scientific and implementation scope remains unchanged. Do not modify or merge M6-T03 during M6-R01.

## Authorized M6-R01 objective

Establish a minimal GitHub Actions verification workflow capable of checking out and testing an explicit branch, tag, or commit SHA in a clean Linux Python environment.

Authorized implementation may add one workflow file such as:

```text
.github/workflows/verify.yml
```

Required workflow properties:

```text
workflow_dispatch with required ref input
ubuntu-latest
Python 3.12
install from requirements.txt
print/verify resolved git SHA
python -m pytest -q -p no:cacheprovider
git diff --check
fail closed on checkout/ref/test/install failure
```

When a 40-character commit SHA is supplied, `git rev-parse HEAD` must resolve to that exact SHA or the workflow must fail.

The workflow must be capable, after M6-R01 is accepted and merged, of manually verifying the unmerged M6-T03 candidate:

```text
fe35d8de5966a439fbde5b999bd35deedf82f7ff
```

## Explicitly out of scope

```text
modifying src/
modifying tests/
modifying requirements.txt
modifying config.yaml
modifying MASTER_PROJECT_SPEC.md
modifying DECISIONS.md
modifying RESEARCH_LOG.md
modifying M6-T03 source or tests
merging M6-T03
changing Bayesian or scientific semantics
Docker infrastructure
WSL requirements
cloud services beyond GitHub Actions
repository secrets or external credentials
privileged/self-hosted runners
experiment infrastructure
M6-T04 implementation
```

Use official GitHub Actions only as required for checkout/Python setup. Do not add new project dependencies.

Preserve:

```text
offline prerecorded EEG / simulated real-time BCI only
no live EEG claim
U-034 unresolved
U-035 unresolved
U-036 unresolved
M6-T04 NOT STARTED / NOT AUTHORIZED
```

## Required M6-R01 verification

Before acceptance, verify that:

```text
workflow YAML is valid
workflow_dispatch is present
manual ref input is required
exact-ref integrity check is implemented
Python 3.12 is explicit
requirements.txt installation is explicit
pytest execution is explicit
git diff --check is explicit
no secrets are required
no source/scientific files changed
```

Stop and report if M6-R01 requires a scientific decision, dependency change, source-code change, M6-T03 modification/merge, or M6-T04 work.

Do not start M6-T04.
