# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### Current Codex Implementation Authority

**Current status:** ACTIVE IMPLEMENTATION TASK — BLOCKED PENDING CI VERIFICATION
**Current milestone:** M6 Bayesian Episode Integration
**Task ID:** M6-T03
**Task title:** Calibrated EEG Evidence -> Bayesian Decision Episode
**Owner:** Project Owner
**Scientific reviewer:** ChatGPT
**Implementation engineer:** Codex
**Canonical branch:** `task/m6-t03-bayesian-episode-integration`

---

# 1. ACTIVE TASK — M6-T03

```text
Task ID: M6-T03
Task title: Calibrated EEG Evidence -> Bayesian Decision Episode
Status: AUTHORIZED / IMPLEMENTED CANDIDATE / BLOCKED PENDING CI VERIFICATION
Reviewed candidate: fe35d8de5966a439fbde5b999bd35deedf82f7ff
Merge authorization: NO
```

M6-T03 is the sole active implementation task. Its code review is satisfactory after terminal-iterator remediation, but acceptance remains blocked until required tests execute successfully in the repository-controlled verification workflow.

Required verification remains:

```text
focused M6-T03 tests
M6-T02/runtime-adapter regression
Bayesian regression
full pytest
git diff --check
```

Do not merge M6-T03 until those checks pass.

---

# 2. CLOSED REMEDIATION — M6-R01

```text
Task ID: M6-R01
Task title: Reproducible Python Verification CI
Status: PASS / ACCEPTED / MERGED / CLOSED
Accepted candidate SHA: 9030350dcd5a2d210ddd284c498c97027589c11e
Software merge SHA: a0dc2ebc8d4d7ad5ecdcd99449602afd701c05a9
Workflow path: .github/workflows/verify.yml
```

M6-R01 established a minimal GitHub Actions verification workflow using `workflow_dispatch`, explicit ref input, `ubuntu-latest`, Python 3.12, installation from `requirements.txt`, exact 40-character SHA integrity checking, full pytest execution, and `git diff --check`.

M6-R01 introduced no scientific changes, no source-code changes, no test changes, no dependency changes, no secrets, and no M6-T03 changes.

The workflow is now on the default branch and is intended to verify the exact unmerged M6-T03 candidate:

```text
fe35d8de5966a439fbde5b999bd35deedf82f7ff
```

---

# 3. PRESERVED BOUNDARIES

```text
offline prerecorded EEG / simulated real-time BCI only
no live EEG claim
exact binary class order ("left", "right")
left -> candidate A
right -> candidate B
initial prior = (0.5, 0.5)
commitment threshold = 0.90
maximum evidence updates = 5
unresolved after update 5 = DEFER
no forced argmax
M6-T04 NOT STARTED / NOT AUTHORIZED
U-034 unresolved
U-035 unresolved
U-036 unresolved
```

Do not start M6-T04.

---

# 4. NEXT ACTION

Use the merged verification workflow on default `main` to verify the exact M6-T03 candidate SHA:

```text
fe35d8de5966a439fbde5b999bd35deedf82f7ff
```

If all required checks pass, stop for ChatGPT review before M6-T03 merge.
