"""Generate deterministic M8 presentation figures from accepted stored data only."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from src.app.demo_fixture import build_demo_trace
from src.app.result_loader import load_presentation_data


def generate(output_dir: Path | None = None) -> tuple[Path, ...]:
    data = load_presentation_data()
    target = output_dir or data.repository_root / "results/m8/figures"
    target.mkdir(parents=True, exist_ok=True)
    paths = (
        _architecture(target),
        _decoder(data, target),
        _abcd(data, target),
        _cross_subject(data, target),
        _sar_demo(target),
    )
    return paths


def _architecture(target: Path) -> Path:
    labels = [
        "Public prerecorded\nPhysioNet EEG",
        "Preprocess +\nepoch",
        "CSP+LDA /\nEEGNet",
        "Calibration",
        "Goal evidence +\nBayes + entropy",
        "Shared autonomy +\nhuman authority",
        "A* + safety +\n2D SAR",
    ]
    fig, ax = plt.subplots(figsize=(15, 3.2))
    ax.axis("off")
    for index, label in enumerate(labels):
        x = index * 2.05
        ax.add_patch(FancyBboxPatch((x, 0.6), 1.65, 1.1, boxstyle="round,pad=0.08", fc="#e8f1fb", ec="#174a7e", lw=1.5))
        ax.text(x + 0.825, 1.15, label, ha="center", va="center", fontsize=9)
        if index < len(labels) - 1:
            ax.annotate("", xy=(x + 2.0, 1.15), xytext=(x + 1.68, 1.15), arrowprops={"arrowstyle": "->", "color": "#174a7e"})
    ax.set_xlim(-0.2, len(labels) * 2.05 - 0.25)
    ax.set_ylim(0.2, 2.25)
    ax.set_title("NeuroCognitive Shared Autonomy — Explanatory Architecture (not an empirical result)", weight="bold")
    return _save(fig, target / "system_architecture.png")


def _decoder(data, target: Path) -> Path:
    rows = data.tables["e1_decoder_performance.csv"]
    metrics = ("accuracy", "balanced_accuracy", "macro_f1")
    fig, ax = plt.subplots(figsize=(8, 4.8))
    width = 0.34
    for i, row in enumerate(rows):
        ax.bar([x + (i - 0.5) * width for x in range(3)], [float(row[m]) for m in metrics], width, label=row["decoder_family"])
    ax.set_xticks(range(3), ["Accuracy", "Balanced accuracy", "Macro F1"])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Score")
    ax.set_title("E1 protected held-out decoding · 303 trials / 10 subjects")
    ax.legend()
    ax.grid(axis="y", alpha=0.2)
    return _save(fig, target / "decoder_comparison.png")


def _abcd(data, target: Path) -> Path:
    rows = data.tables["e6_abcd.csv"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    colors = {"csp_lda": "#2b6cb0", "eegnet": "#dd6b20"}
    for family in ("csp_lda", "eegnet"):
        selected = [row for row in rows if row["decoder_family"] == family]
        axes[0].plot([r["condition"] for r in selected], [float(r["success_rate"]) for r in selected], marker="o", label=family, color=colors[family])
        axes[1].plot([r["condition"] for r in selected], [float(r["mean_evidence_count"]) for r in selected], marker="o", label=family, color=colors[family])
    axes[0].set(title="Task success", ylabel="Rate", ylim=(0, 1.05))
    axes[1].set(title="Decision latency", ylabel="Mean accepted EEG observations", ylim=(0, 5.2))
    for ax in axes:
        ax.set_xlabel("Frozen condition")
        ax.grid(alpha=0.2)
        ax.legend()
    fig.suptitle("E6 A/B/C/D comparison · 38 episodes / 8 subjects\nDeterministic simulated-human policy")
    return _save(fig, target / "abcd_comparison.png")


def _cross_subject(data, target: Path) -> Path:
    rows = data.tables["e8_subject_wise.csv"]
    subjects = sorted({int(row["subject_id"]) for row in rows})
    fig, ax = plt.subplots(figsize=(10, 4.8))
    width = 0.36
    for index, family in enumerate(("csp_lda", "eegnet")):
        values = {int(r["subject_id"]): float(r["correctness"]) for r in rows if r["decoder_family"] == family}
        ax.bar([x + (index - 0.5) * width for x in range(len(subjects))], [values[s] for s in subjects], width, label=family)
    ax.set_xticks(range(len(subjects)), [str(s) for s in subjects])
    ax.set(xlabel="Anonymous subject ID", ylabel="Trial correctness", ylim=(0, 1), title="E8 protected cross-subject heterogeneity · n=10")
    ax.grid(axis="y", alpha=0.2)
    ax.legend()
    return _save(fig, target / "cross_subject_summary.png")


def _sar_demo(target: Path) -> Path:
    trace = build_demo_trace()
    path = set(trace["plan"]["path"])
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(2.5, -0.5)
    ax.set_xticks(range(5))
    ax.set_yticks(range(3))
    ax.grid(True)
    for row in range(3):
        for col in range(5):
            if (row, col) in path:
                ax.add_patch(plt.Rectangle((col - 0.5, row - 0.5), 1, 1, color="#c6f6d5", zorder=-1))
    ax.scatter([0], [1], marker="s", s=180, label="start / agent", color="#2b6cb0")
    ax.scatter([4], [1], marker="*", s=260, label="approved victim_a", color="#c53030")
    ax.scatter([2], [0], marker="*", s=220, label="unselected victim_b", color="#718096")
    ax.plot([c for _, c in trace["plan"]["path"]], [r for r, _ in trace["plan"]["path"]], color="#2f855a", lw=2)
    ax.legend(loc="upper right")
    ax.set_title("Deterministic explanatory route · production A* interface\nNot an empirical safety result")
    return _save(fig, target / "sar_route_safety_demo.png")


def _save(fig, path: Path) -> Path:
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


if __name__ == "__main__":
    for generated in generate():
        print(generated)
