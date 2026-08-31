# CURRENT_TASK.md

## NeuroCognitive Shared Autonomy for Search & Rescue
### No Active Codex Implementation Ticket

**Purpose:** Hold exactly one active implementation task for Codex, or explicitly record that no task is currently authorized  
**Current status:** NO ACTIVE TASK  
**Current milestone:** EEG decoding implementation sequence through M1-T06  
**Task ID:** NONE AUTHORIZED  
**Task title:** Awaiting next approved implementation ticket  
**Owner:** Project Owner  
**Scientific reviewer:** ChatGPT  
**Implementation engineer:** Codex  
**Repository instructions:** `AGENTS.md`  
**Canonical branch:** `main`  
**Last updated:** 2026-08-31

---

# 1. CURRENT AUTHORIZATION STATE

There is currently no active implementation task authorized for Codex.

Completed, scientifically reviewed, accepted, and merged on canonical `main`:

```text
M1-T01 — PhysioNet EEGBCI Data Loader
M1-T02 — EEG Visualization / Inspection
M1-T03 — EEG Preprocessing & Epochs
M1-T04 — EEG Split Manifest
M1-T05 — CSP+LDA Baseline
M1-T06 — EEGNet / Compact CNN
```

Do not begin another implementation module until a new narrow `CURRENT_TASK.md` ticket is explicitly approved by the Project Owner.

---

# 2. CLOSED TASK RECORD — M1-T06

```text
Task ID:
M1-T06

Task title:
EEGNet / Compact CNN

Final status:
PASS / ACCEPTED / MERGED

Task branch:
task/m1-t06-eegnet-compact-cnn

Accepted task-branch head:
1d6532ab1538fa361ed61c265c1a00577ae0afab

Canonical software merge commit:
6b526d76acb53cd4f632ba87c975b4ede9e89a9c
```

M1-T06 implements the approved leakage-safe EEGNet baseline under D-040 through D-042 and D-045 through D-047.

Accepted implementation facts:

```text
- input batch × 1 × 64 × time
- all 64 channels
- native 160 Hz
- full canonical -1.0 s to +4.0 s epoch
- no CSP-only crop
- F1 = 8
- temporal kernel length 64, same padding
- depth multiplier D = 2
- first average pool (1,4), stride (1,4)
- second average pool (1,8), stride (1,8)
- depthwise spatial-convolution max-norm cap 1.0
- separable F2 = 16, temporal kernel 16
- dropout 0.5
- dense two-logit output
- explicit class order ("left", "right")
- softmax probability output
- cross-entropy + Adam, lr 1e-3, weight_decay 0
- batch size 32
- maximum 200 epochs
- early stopping patience 20
- validation balanced accuracy checkpoint selection
- earliest checkpoint retained on exact validation-score ties
- seed 42
- train partition shuffled; validation/test not shuffled
- protected test/final-test excluded from fitting, tuning, early stopping, and checkpoint selection
```

Final reviewer regression bundle:

```text
48 passed, 1 warning
```

The warning is the non-failing PyTorch `padding='same'` warning for even kernels; it was reviewed and is not an acceptance blocker.

Real-data subject-1 smoke verification using runs 4/8/12:

```text
retained epochs: 13
train / validation / test: 7 / 3 / 3
run 4 rejected: 14
run 8 rejected: 9
run 12 rejected: 9
selected checkpoint epoch: 1
best validation balanced accuracy: 0.5
validation accuracy: 0.6666666666666666
validation balanced accuracy: 0.5
validation loss: 0.6873876452445984
test accuracy: 0.6666666666666666
test balanced accuracy: 0.5
test loss: 0.6873877048492432
class order: ("left", "right")
```

This smoke run is integration evidence only. It is not an EEGNet efficacy result and does not authorize a model-performance claim.

No calibration, Bayesian inference, shared autonomy, planning, safety, replay, or later module was implemented in M1-T06.

---

# 3. GOVERNING DECISIONS NOW CLOSED FOR EEGNET

```text
D-045 — Final EEGNet Architecture
D-046 — Final EEGNet Training Hyperparameters
D-047 — EEGNet Pooling and Depthwise Max-Norm Supplement
```

D-047 supplements D-045 only. D-046 remains unchanged.

Calibration and later scientific decisions remain unresolved unless separately approved in `DECISIONS.md`.

---

# 4. NEXT GOVERNANCE GATE

Before any further implementation:

```text
1. Identify the next narrow implementation task.
2. Check MASTER_PROJECT_SPEC.md, PROJECT_STATE.md, DECISIONS.md, AGENTS.md, and relevant technical documentation.
3. Resolve any scientific/architectural decision that blocks that task.
4. Record the approved decision in DECISIONS.md when applicable.
5. Obtain explicit Project Owner approval for one narrow CURRENT_TASK.md ticket.
6. Only then begin implementation on a task branch.
```

Until that happens:

```text
STOP
STATUS = NO ACTIVE TASK
```
