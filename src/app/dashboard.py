"""Final Streamlit inspection dashboard for accepted M7 results and M8 demo."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterable, Mapping

from src.app.demo_fixture import build_demo_trace
from src.app.result_loader import PresentationData, headline_metrics, load_presentation_data

SECTIONS = (
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


def _rows(data: PresentationData, filename: str) -> list[dict[str, str]]:
    return [dict(row) for row in data.tables[filename]]


def _image_if_present(st: Any, path: Path, caption: str) -> None:
    if path.is_file():
        st.image(str(path), caption=caption, use_container_width=True)


def render_dashboard(st: Any, data: PresentationData, section: str) -> None:
    """Render one selected section; all empirical values come from ``data``."""
    metrics = headline_metrics(data)
    figures = data.repository_root / "results/m8/figures"
    st.title("NeuroCognitive Shared Autonomy for Search & Rescue")
    st.caption("Software-only research prototype · Public prerecorded EEG · Offline EEG Replay / Simulated Real-Time BCI")

    if section == "Project Overview":
        st.subheader("Can uncertainty-aware shared autonomy make noisy EEG control more reliable and safer?")
        st.info("Human determines WHAT objective is selected. AI determines HOW to achieve it safely.")
        cols = st.columns(4)
        cols[0].metric("Protected subjects", metrics["protected_subjects"])
        cols[1].metric("Sequential subjects", metrics["sequential_subjects"])
        cols[2].metric("Protected EEG trials", metrics["eeg_trials"])
        cols[3].metric("M7 status", "Accepted / Closed")
        st.markdown(
            "PhysioNet EEG → preprocessing/epochs → CSP+LDA and EEGNet → calibration → "
            "Bayesian goal belief → entropy → shared autonomy → human authority → A* → safety → 2D SAR"
        )
        st.warning("The evidence is offline and simulated; it is not a live BCI, real rescue system, or certified safety evaluation.")
    elif section == "Architecture":
        _image_if_present(st, figures / "system_architecture.png", "Explanatory architecture diagram (not an empirical result)")
        st.code(
            "PhysioNet EEG → 7–30 Hz / epochs → CSP+LDA + EEGNet → model-specific calibration\n"
            "→ binary goal evidence → sequential Bayes → posterior entropy → PROCEED / CONFIRM / DEFER\n"
            "→ explicit human authority → approved goal → risk-aware A* → hard-safety veto → 2D SAR",
            language=None,
        )
    elif section == "EEG / Decoder Results":
        st.subheader("Protected held-out decoding (E1/E8, n=10 subjects; 303 trials)")
        st.dataframe(_rows(data, "e1_decoder_performance.csv"), use_container_width=True, hide_index=True)
        _image_if_present(st, figures / "decoder_comparison.png", "Accepted E1 aggregate metrics")
        st.caption("CSP+LDA scored higher in this frozen evaluation; this does not establish universal model superiority.")
    elif section == "Calibration":
        st.subheader("Identity vs model-specific calibration (E2)")
        st.dataframe(_rows(data, "e2_calibration.csv"), use_container_width=True, hide_index=True)
        _image_if_present(st, data.reused_figures["e2_calibration_reliability.png"], "Accepted M7 reliability diagram (hash verified)")
        st.warning("Mixed result: CSP+LDA ECE improved while Brier worsened; EEGNet improved on both stored metrics.")
    elif section == "Bayesian Intent & Uncertainty":
        st.markdown(
            "Calibrated Left/Right probabilities are likelihood weights for the currently exposed candidate A/B pair. "
            "The posterior is updated sequentially; Shannon entropy in bits describes ambiguity."
        )
        st.code("posterior ∝ likelihood × prior\nPROCEED ≥ 0.90 · CONFIRM at update 5 if 0.75–0.90 · otherwise DEFER")
        demo = build_demo_trace()
        st.dataframe(list(demo["updates"]), use_container_width=True, hide_index=True)
        st.caption("Deterministic explanatory fixture above; not a new empirical result.")
    elif section == "Shared Autonomy / A-B-C-D":
        st.subheader("Accepted E6 results (n=8 subjects; 38 fixed-intent episodes)")
        st.dataframe(_rows(data, "e6_abcd.csv"), use_container_width=True, hide_index=True)
        _image_if_present(st, figures / "abcd_comparison.png", "Accepted E6 task success and evidence latency")
        st.caption("B reaches 38/38 under the frozen deterministic simulated-human policy; this measures that policy, not real-human usability.")
    elif section == "Planning & Safety":
        st.markdown(
            "Soft risk changes A* cost (distance + 2 × cumulative destination-cell risk). Blocked and risk=1.00 cells are hard constraints. "
            "Safety checks every proposed transition; STOP and PAUSE retain authority."
        )
        scenarios = data.result["E5"]
        st.json(_thaw(scenarios), expanded=False)
        _image_if_present(st, figures / "sar_route_safety_demo.png", "Deterministic explanatory SAR route and safety boundary")
        st.caption("S1–S7 are deterministic validation scenarios, not a stochastic or real-world safety trial.")
    elif section == "Robustness & Ablations":
        st.subheader("Six frozen ablations")
        st.dataframe(_rows(data, "e7_ablations.csv"), use_container_width=True, hide_index=True)
        st.subheader("R1 evidence flattening and R2 contradictory evidence")
        _image_if_present(st, data.reused_figures["e7_r1_robustness.png"], "Accepted R1 robustness (hash verified)")
        _image_if_present(st, data.reused_figures["e7_r2_robustness.png"], "Accepted R2 robustness (hash verified)")
        st.warning("Degradation is non-monotonic in several conditions because the simulated-human correction policy can turn uncertainty into successful intervention.")
    elif section == "Cross-Subject Evaluation":
        st.subheader("Subject heterogeneity (E8, all n=10 protected subjects)")
        st.dataframe(_rows(data, "e8_subject_wise.csv"), use_container_width=True, hide_index=True)
        _image_if_present(st, figures / "cross_subject_summary.png", "Accepted subject-wise correctness")
        st.caption("Sequential analyses exclude subjects 57 and 84 under the frozen participation rules and use n=8 without replacement.")
    elif section == "Adaptation":
        st.subheader("Bounded prior personalization (E9)")
        st.markdown("Adaptation uses explicit simulated feedback only, after a three-event warm-up, with priors bounded to [0.25, 0.75].")
        _image_if_present(st, data.reused_figures["e9_adaptation_trajectory.png"], "Accepted adaptation trajectory (hash verified)")
        st.dataframe(_rows(data, "e9_adaptation_trajectory.csv"), use_container_width=True, hide_index=True)
        st.warning("C and personalized D had identical success counts: 32/38 for CSP+LDA and 36/38 for EEGNet. No efficacy improvement is claimed.")
    elif section == "Statistics":
        st.subheader("D-079 paired subject-level inference")
        st.dataframe(_rows(data, "d079_statistics.csv"), use_container_width=True, hide_index=True)
        st.caption("n=8, 10,000 paired bootstrap resamples, 256 exact sign flips. Neither D-minus-A comparison is significant after Holm correction at α=0.05.")
    elif section == "Failure Cases & Limitations":
        st.error("Failures and limitations are part of the result, not footnotes.")
        st.dataframe(_rows(data, "failure_taxonomy.csv"), use_container_width=True, hide_index=True)
        st.markdown(
            "- EEG performance varies substantially by subject.\n"
            "- Confidence and Bayesian accumulation can still be wrong or slow.\n"
            "- Intervention burden is measured under a deterministic simulated-human policy.\n"
            "- Episodes are offline repeated-trial constructions; sequential n=8.\n"
            "- The public motor-imagery task does not directly encode rescue semantics.\n"
            "- The environment is a simple 2D simulation: no physical robot, human-subject efficacy, clinical claim, or certified safety.\n"
            "- v5 registers failure categories but does not aggregate category counts."
        )
    elif section == "Reproducibility / Provenance":
        st.success("Accepted M7-T02-R03 v5 · M7 PASS / ACCEPTED / MERGED / CLOSED")
        st.code(
            f"result: {data.result_path.relative_to(data.repository_root)}\n"
            f"result sha256: {data.result_sha256}\n"
            f"manifest: {data.manifest_path.relative_to(data.repository_root)}\n"
            f"manifest sha256: {data.manifest_sha256}\n"
            f"report artifacts: {data.report_manifest_path.relative_to(data.repository_root)}\n"
            f"report-artifact manifest sha256: {data.report_manifest_sha256}\n"
            f"software sha: {data.manifest['software_sha']}"
        )
        st.json(
            {
                "qc_manifest_sha256": data.manifest["qc_manifest_sha256"],
                "split_manifest_sha256": data.manifest["split_manifest_sha256"],
                "episode_manifest_sha256": data.manifest["episode_manifest_sha256"],
                "participation_manifest_sha256": data.manifest["participation_manifest_sha256"],
            }
        )
        st.caption("v1–v3 remain invalid implementation-contract artifacts; v4 remains invalid provenance binding. They are preserved for audit, not reporting.")
    elif section == "Interactive Demo":
        st.warning("Deterministic explanatory demo — not an empirical experiment and not protected EEG output.")
        trace = build_demo_trace()
        st.subheader("1. Fixture provenance and runtime entry boundary")
        st.json(_thaw(trace["fixture_metadata"]), expanded=True)
        st.subheader("2. Posterior, entropy, and autonomy trajectory")
        st.dataframe(list(trace["updates"]), use_container_width=True, hide_index=True)
        st.subheader("3. Final autonomy decision and human-authority boundary")
        st.json(_thaw(trace["decision"]), expanded=True)
        st.json(_thaw(trace["human_authority"]), expanded=True)
        st.subheader("4. Approved goal and A* plan")
        st.write(f"Approved symbolic goal: `{trace['approved_goal']}`")
        st.json(_thaw(trace["plan"]), expanded=True)
        st.subheader("5. Per-action safety checks")
        st.dataframe(list(trace["safety_decisions"]), use_container_width=True, hide_index=True)
        st.subheader("6. Executed trajectory and terminal simulated outcome")
        st.json(_thaw(trace["execution"]), expanded=True)
        st.success(
            f"Mission status: {trace['execution']['status']} · "
            f"goal reached: {trace['execution']['goal_reached']} · "
            f"terminal position: {trace['execution']['terminal_position']}"
        )
        st.caption(
            "The fixture does not run a decoder or calibrator. From the documented probability boundary onward, "
            "accepted production authorization, planning, safety, and environment interfaces generate the trace."
        )
    else:
        raise ValueError(f"Unknown dashboard section: {section}")


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title="NeuroCognitive Shared Autonomy", page_icon="🧠", layout="wide")
    try:
        data = load_presentation_data()
    except Exception as exc:
        st.error(f"Accepted result package failed validation: {exc}")
        st.stop()
    section = st.sidebar.radio("Explore", SECTIONS)
    render_dashboard(st, data, section)


def smoke() -> int:
    """Validate import, accepted data, all section labels, and demo without opening UI."""
    data = load_presentation_data()
    assert len(SECTIONS) == 14
    assert headline_metrics(data)["eeg_trials"] == 303
    trace = build_demo_trace()
    assert trace["plan"]["status"] == "SUCCESS"
    assert trace["execution"]["status"] == "SUCCESS"
    assert trace["execution"]["goal_reached"] is True
    print("M8 dashboard smoke PASS: accepted data, 14 sections, deterministic demo")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    raise SystemExit(smoke() if args.smoke else main())
