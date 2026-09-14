from __future__ import annotations

import ast
from pathlib import Path

from src.app.dashboard import SECTIONS, smoke
from src.app.result_loader import repository_root


def test_dashboard_has_all_authorized_sections_and_headless_smoke() -> None:
    assert SECTIONS == (
        "Project Overview",
        "Architecture",
        "EEG / Decoder Results",
        "Calibration",
        "Bayesian Intent & Uncertainty",
        "Shared Autonomy / A-B-C-D",
        "Planning & Safety",
        "Robustness & Ablations",
        "Cross-Subject Evaluation",
        "Adaptation",
        "Statistics",
        "Failure Cases & Limitations",
        "Reproducibility / Provenance",
        "Interactive Demo",
    )
    assert smoke() == 0


def test_result_loader_has_no_experiment_or_model_imports() -> None:
    path = repository_root() / "src/app/result_loader.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert not any(name.startswith("src.evaluation") for name in imports)
    assert not any(name.startswith("src.models") for name in imports)
    assert not any(name.startswith("src.eeg") for name in imports)


def test_final_documents_preserve_sample_sizes_and_negative_findings() -> None:
    root = repository_root()
    documents = (
        root / "README.md",
        root / "docs/23_RESULTS_AND_ANALYSIS.md",
        root / "docs/24_DISCUSSION_AND_FINDINGS.md",
        root / "docs/FINAL_TECHNICAL_REPORT.md",
        root / "docs/PORTFOLIO_AND_RESUME_POSITIONING.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in documents)
    for required in (
        "303",
        "10 protected",
        "38",
        "8",
        "not significant after Holm",
        "adaptation did not",
        "public prerecorded EEG",
    ):
        assert required.lower() in combined.lower()


def test_m8_figure_inventory_is_presentation_only() -> None:
    figure_dir = repository_root() / "results/m8/figures"
    expected = {
        "system_architecture.png",
        "decoder_comparison.png",
        "abcd_comparison.png",
        "cross_subject_summary.png",
        "sar_route_safety_demo.png",
    }
    assert {path.name for path in figure_dir.glob("*.png")} == expected
