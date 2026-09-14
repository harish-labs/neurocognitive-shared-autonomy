"""Deterministic, manifest-authorized M7-T02 protected evaluation runner."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

import numpy as np

from src.cognitive.adaptation import ExplicitFeedbackObservation, FeedbackAction, PriorPersonalizer
from src.cognitive.bayes import BinaryBayesianGoalEpisode, EpisodeStatus, INITIAL_PRIOR, binary_goal_evidence_from_calibrated_probabilities
from src.cognitive.uncertainty import estimate_binary_uncertainty
from src.control.human_interaction import HumanInteractionController
from src.control.shared_autonomy import AutonomyMode, decide_shared_autonomy
from src.evaluation.ablation_semantics import evaluate_full_minus_bayes, evaluate_full_minus_uncertainty
from src.evaluation.eeg_metrics import calibration_metrics, classification_metrics
from src.evaluation.episodes import load_episode_manifest
from src.evaluation.final_artifacts import load_frozen_cross_subject_artifacts
from src.evaluation.final_contract import FinalAccessAuthorization, authorize_final_access, manifest_from_mapping
from src.evaluation.final_data import load_subject_epochs
from src.evaluation.planning_scenarios import run_frozen_scenarios, scenario_result_mapping
from src.evaluation.robustness import contaminate_contradictory_evidence, flatten_evidence
from src.evaluation.statistics import ObservationMetric, aggregate_subject_means, holm_adjust, paired_subject_inference
from src.evaluation.simulated_human import apply_simulated_human_policy, feedback_for_subject


CANDIDATES = ("victim_a", "victim_b")


def execute_final_program(*, manifest_path: str | Path, processed_directory: str | Path, output_path: str | Path) -> dict[str, Any]:
    """Execute E1--E9 only after final-contract authorization succeeds."""

    authorization = authorize_final_access(manifest_path)
    payload = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    manifest = manifest_from_mapping(payload)
    bundle = load_frozen_cross_subject_artifacts(manifest.artifacts)
    episode_manifest = load_episode_manifest(manifest.episode_manifest_path)
    first_access = {
        "event": "first_protected_decoder_outcome_access",
        "authorization_manifest_sha256": authorization.manifest_sha256,
        "software_sha": authorization.software_sha,
        "final_subject_ids": list(authorization.final_subject_ids),
    }
    trial_rows, episode_rows = _predict_final_data(bundle, authorization, processed_directory, episode_manifest)
    results = {
        "schema_version": "m7-t02-results-v1",
        "first_protected_outcome_access": first_access,
        "E1": _e1(trial_rows),
        "E2": _e2(trial_rows),
        "E3": _systems(episode_rows, systems=("A", "C")),
        "E4": _systems(episode_rows, systems=("C",)),
        "E5": {"safety_on": [scenario_result_mapping(x) for x in run_frozen_scenarios(safety_enabled=True)], "safety_off": [scenario_result_mapping(x) for x in run_frozen_scenarios(safety_enabled=False)]},
        "E6": _systems(episode_rows, systems=("A", "B", "C", "D")),
        "E7": _ablations(episode_rows),
        "E8": _robustness(episode_rows, manifest),
        "E9": _systems(episode_rows, systems=("C", "D")),
        "statistics": _statistics(episode_rows),
        "protected_final_subject_ids": list(authorization.final_subject_ids),
        "sequential_subject_ids": list(manifest.participation_manifest["included_subject_ids"]),
    }
    rendered = json.dumps(results, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    destination = Path(output_path).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.read_text(encoding="utf-8") != rendered:
        raise ValueError("Protected result path already contains different immutable content.")
    destination.write_text(rendered, encoding="utf-8", newline="\n")
    return results


def _predict_final_data(bundle, authorization: FinalAccessAuthorization, processed_directory, episode_manifest):
    trials: list[dict[str, Any]] = []
    indexed: dict[str, dict[str, dict[str, Any]]] = {"csp_lda": {}, "eegnet": {}}
    for subject_id in authorization.final_subject_ids:
        epochs = load_subject_epochs(processed_directory, subject_id)
        rows = epochs.metadata.reset_index(drop=True)
        for family, decoder, calibrator in (("csp_lda", bundle.csp_decoder, bundle.csp_calibrator), ("eegnet", bundle.eegnet_decoder, bundle.eegnet_calibrator)):
            raw = decoder.predict_proba(epochs)
            calibrated = calibrator.predict_proba(decoder.predict_logits(epochs) if family == "eegnet" else raw)
            for index, metadata in rows.iterrows():
                key = _trial_id(metadata)
                item = {"subject_id": int(subject_id), "trial_id": key, "true_label": str(metadata.semantic_label), "raw": [float(x) for x in raw[index]], "calibrated": [float(x) for x in calibrated[index]]}
                trials.append({"decoder_family": family, **item})
                indexed[family][key] = item
    episodes: list[dict[str, Any]] = []
    for episode in episode_manifest.episodes:
        if episode.subject_id not in authorization.final_subject_ids:
            continue
        intended = "victim_a" if episode.intended_class == "left" else "victim_b"
        keys = [trial.canonical_trial_id for trial in episode.source_trials]
        for family in indexed:
            evidence = [indexed[family][key] for key in keys]
            episodes.append({"decoder_family": family, "episode_id": episode.episode_id, "subject_id": episode.subject_id, "intended_goal": intended, "raw": [x["raw"] for x in evidence], "calibrated": [x["calibrated"] for x in evidence]})
    return trials, episodes


def _trial_id(row) -> str:
    return f"s{int(row.subject_id):03d}-r{int(row.run_id):02d}-{str(row.event_code).lower()}-sample{int(row.event_sample):09d}-trial{int(row.trial_index):04d}"


def _e1(rows):
    output = {}
    for family in ("csp_lda", "eegnet"):
        selected = [x for x in rows if x["decoder_family"] == family]
        truth = [x["true_label"] for x in selected]
        predicted = ["left" if x["raw"][0] >= x["raw"][1] else "right" for x in selected]
        output[family] = asdict(classification_metrics(truth, predicted))
    return output


def _e2(rows):
    output = {}
    for family in ("csp_lda", "eegnet"):
        selected = [x for x in rows if x["decoder_family"] == family]
        truth = [x["true_label"] for x in selected]
        output[family] = {"identity": asdict(calibration_metrics(np.asarray([x["raw"] for x in selected]), truth)), "calibrated": asdict(calibration_metrics(np.asarray([x["calibrated"] for x in selected]), truth))}
    return output


def _systems(rows, *, systems):
    result = {}
    for family in ("csp_lda", "eegnet"):
        family_rows = [x for x in rows if x["decoder_family"] == family]
        result[family] = {}
        for system in systems:
            adaptation = PriorPersonalizer(adaptation_enabled=(system == "D"))
            evaluated = [_evaluate(x, system, adaptation=adaptation if system == "D" else None) for x in family_rows]
            result[family][system] = _summarize(evaluated)
    return result


def _ablations(rows):
    names = ("full", "full_minus_calibration", "full_minus_bayes", "full_minus_uncertainty", "full_minus_safety", "full_minus_adaptation")
    mapping = {"full": "D", "full_minus_calibration": "raw_D", "full_minus_bayes": "minus_bayes", "full_minus_uncertainty": "minus_uncertainty", "full_minus_safety": "D", "full_minus_adaptation": "C"}
    return {family: {name: _summarize([_evaluate(x, mapping[name]) for x in rows if x["decoder_family"] == family]) for name in names} for family in ("csp_lda", "eegnet")}


def _evaluate(row, system, *, adaptation=None, evidence_override=None, safety_enabled=True):
    evidence = evidence_override if evidence_override is not None else (row["raw"] if system == "raw_D" else row["calibrated"])
    if system == "A":
        goal = CANDIDATES[int(np.argmax(row["raw"][0]))]; mode = "PROCEED"; count = 1
    elif system == "B":
        p = evidence[0]; confidence = max(p); goal = CANDIDATES[int(np.argmax(p))] if confidence >= .75 else None; mode = "PROCEED" if confidence >= .90 else ("CONFIRM" if goal else "DEFER"); count = 1
    elif system == "minus_bayes":
        d = evaluate_full_minus_bayes(evidence, candidate_names=CANDIDATES); mode, goal, count = d.autonomy_mode, d.committed_goal or d.candidate_goal, d.accepted_evidence_count
    elif system == "minus_uncertainty":
        d = evaluate_full_minus_uncertainty(evidence, candidate_names=CANDIDATES); mode, goal, count = d.autonomy_mode, d.committed_goal, d.accepted_evidence_count
    else:
        prior = INITIAL_PRIOR
        if adaptation is not None:
            prior = adaptation.initial_prior_for_new_episode(str(row["subject_id"]), *CANDIDATES)
        episode = BinaryBayesianGoalEpisode(candidate_a=CANDIDATES[0], candidate_b=CANDIDATES[1], initial_prior=prior)
        mode = "DEFER"; goal = None; count = 0
        for p in evidence:
            update = episode.accept_evidence(binary_goal_evidence_from_calibrated_probabilities(p)); count = episode.update_count
            decision = decide_shared_autonomy(update, estimate_binary_uncertainty(update.posterior))
            if decision.mode.value != "WAITING": mode, goal = decision.mode.value, decision.approved_goal or decision.candidate_goal; break
        if system in {"C", "D", "raw_D"} and mode in {"CONFIRM", "DEFER"}:
            human = apply_simulated_human_policy(episode_id=row["episode_id"], autonomy_mode=mode, proposed_goal=goal, intended_goal=row["intended_goal"], candidate_names=CANDIDATES, controller=HumanInteractionController())
            goal = human.final_approved_goal
            if adaptation is not None and human.explicit_feedback is not None:
                adaptation.record_explicit_feedback(feedback_for_subject(human, str(row["subject_id"])))
    return {"subject_id": row["subject_id"], "episode_id": row["episode_id"], "mode": mode, "goal": goal, "correct": goal == row["intended_goal"], "evidence_count": count}


def _robustness(rows, manifest):
    """Run D-078 over a single ordered population per family; episode boundaries never reset R2."""
    output = {"R1_evidence_flattening": {}, "R2_contradictory_evidence": {}}
    for family in ("csp_lda", "eegnet"):
        family_rows = [r for r in rows if r["decoder_family"] == family]
        for epsilon in manifest.r1_severities:
            perturbed = []
            provenance = []
            for row in family_rows:
                result = flatten_evidence(np.asarray(row["calibrated"], dtype=float), epsilon)
                perturbed.append(_evaluate(row, "C", evidence_override=result.perturbed_evidence))
                provenance.append({"episode_id": row["episode_id"], "epsilon": epsilon, "original_evidence": result.original_evidence, "perturbed_evidence": result.perturbed_evidence})
            output["R1_evidence_flattening"].setdefault(family, {})[str(epsilon)] = {"summary": _summarize(perturbed), "provenance": provenance}
        ordered_ids = [f"{r['episode_id']}::obs-{i:04d}" for r in family_rows for i in range(len(r["calibrated"]))]
        population = np.asarray([obs for r in family_rows for obs in r["calibrated"]], dtype=float)
        for q in manifest.r2_severities:
            result = contaminate_contradictory_evidence(population, q, seed=manifest.r2_seed, observation_ids=ordered_ids)
            cursor = 0; evaluated = []
            for row in family_rows:
                n = len(row["calibrated"]); local = result.perturbed_evidence[cursor:cursor+n]; cursor += n
                evaluated.append(_evaluate(row, "C", evidence_override=local))
            output["R2_contradictory_evidence"].setdefault(family, {})[str(q)] = {"summary": _summarize(evaluated), "provenance": asdict(result), "episode_boundaries_do_not_reset_selection": True}
    return output


def _statistics(rows):
    """D-079 subject-level paired inference with explicit denominators and Holm adjustment."""
    metrics = {}
    for family in ("csp_lda", "eegnet"):
        selected = [r for r in rows if r["decoder_family"] == family]
        subjects = sorted({str(r["subject_id"]) for r in selected})
        observations_a = [ObservationMetric(str(r["subject_id"]), f"A::{r['episode_id']}", float(_evaluate(r, "A")["correct"])) for r in selected]
        observations_d = [ObservationMetric(str(r["subject_id"]), f"D::{r['episode_id']}", float(_evaluate(r, "D")["correct"])) for r in selected]
        a = aggregate_subject_means(observations_a); d = aggregate_subject_means(observations_d)
        inference = paired_subject_inference(a, d, bootstrap_seed=42, permutation_seed=42, permutation_samples=10000)
        metrics[family] = {"D_minus_A_correctness": asdict(inference), "subject_count": len(subjects), "evaluation_unit": "subject"}
    pvals = {f"{family}.D_minus_A_correctness": value["D_minus_A_correctness"]["raw_p_value"] for family, value in metrics.items()}
    return {"comparisons": metrics, "holm_adjusted_p_values": holm_adjust(pvals)}


def _summarize(rows):
    total = len(rows); committed = [x for x in rows if x["goal"] is not None]; wrong = [x for x in committed if not x["correct"]]
    return {"episode_count": total, "committed_count": len(committed), "success_count": sum(x["correct"] for x in rows), "wrong_all_rate": len(wrong) / total if total else 0.0, "wrong_committed_rate": len(wrong) / len(committed) if committed else None, "mean_evidence_count": float(np.mean([x["evidence_count"] for x in rows])) if rows else 0.0, "modes": {mode: sum(x["mode"] == mode for x in rows) for mode in ("PROCEED", "CONFIRM", "DEFER")}, "subject_ids": sorted({x["subject_id"] for x in rows})}
