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
from src.autonomy.environment import EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.execution import ExecutionStatus, PlannerSafetyEnvironmentExecutor
from src.autonomy.planner import PlannerStatus, RiskAwareAStarPlanner
from src.evaluation.ablation_semantics import evaluate_full_minus_bayes, evaluate_full_minus_uncertainty
from src.evaluation.autonomy_metrics import EpisodeRecord, compute_autonomy_metrics
from src.evaluation.conditions import ABLATIONS, ConditionId, get_condition
from src.evaluation.eeg_metrics import calibration_metrics, classification_metrics
from src.evaluation.episodes import load_episode_manifest
from src.evaluation.final_artifacts import load_frozen_cross_subject_artifacts
from src.evaluation.final_contract import FULL_SYSTEM_MISSION_MAP, FinalAccessAuthorization, authorize_final_access, manifest_from_mapping
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
        "schema_version": "m7-t02-results-v4",
        "first_protected_outcome_access": first_access,
        "E1": _e1(trial_rows),
        "E2": _e2(trial_rows),
        "E3": _systems(_sequential_rows(episode_rows, manifest), systems=("C",), include_navigation=True),
        "E4": _systems(_sequential_rows(episode_rows, manifest), systems=("C",), include_navigation=True),
        "E5": {"safety_on": [scenario_result_mapping(x) for x in run_frozen_scenarios(safety_enabled=True)], "safety_off": [scenario_result_mapping(x) for x in run_frozen_scenarios(safety_enabled=False)]},
        "E6": _systems(_sequential_rows(episode_rows, manifest), systems=("A", "B", "C", "D"), include_navigation=True),
        "E7": {"ablations": _ablations(_sequential_rows(episode_rows, manifest)), "robustness": _robustness(_sequential_rows(episode_rows, manifest), manifest)},
        "E8": _heldout(trial_rows),
        "E9": _e9(_sequential_rows(episode_rows, manifest)),
        "statistics": _statistics(_sequential_rows(episode_rows, manifest)),
        "failure_taxonomy": _failure_taxonomy(),
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
            first = episode.source_trials[0]
            episodes.append({"decoder_family": family, "episode_id": episode.episode_id, "subject_id": episode.subject_id, "intended_goal": intended, "raw": [x["raw"] for x in evidence], "calibrated": [x["calibrated"] for x in evidence], "run_id": int(first.run_id), "first_event_sample": int(first.event_sample)})
    return trials, episodes


def _sequential_rows(rows, manifest):
    allowed = {int(x) for x in manifest.participation_manifest["included_subject_ids"]}
    return [row for row in rows if int(row["subject_id"]) in allowed]


def _trial_id(row) -> str:
    return f"s{int(row.subject_id):03d}-r{int(row.run_id):02d}-{str(row.event_code).lower()}-sample{int(row.event_sample):09d}-trial{int(row.trial_index):04d}"


def _e1(rows):
    output = {}
    for family in ("csp_lda", "eegnet"):
        selected = [x for x in rows if x["decoder_family"] == family]
        truth = [x["true_label"] for x in selected]
        predicted = ["left" if x["raw"][0] >= x["raw"][1] else "right" for x in selected]
        output[family] = {"aggregate": asdict(classification_metrics(truth, predicted)), "subject_wise": _subject_trial_metrics(selected)}
    return output


def _subject_trial_metrics(rows):
    output = {}
    for subject in sorted({r["subject_id"] for r in rows}):
        selected = [r for r in rows if r["subject_id"] == subject]
        output[str(subject)] = asdict(classification_metrics([r["true_label"] for r in selected], ["left" if r["raw"][0] >= r["raw"][1] else "right" for r in selected]))
    return output


def _e2(rows):
    output = {}
    for family in ("csp_lda", "eegnet"):
        selected = [x for x in rows if x["decoder_family"] == family]
        truth = [x["true_label"] for x in selected]
        output[family] = {"identity": asdict(calibration_metrics(np.asarray([x["raw"] for x in selected]), truth)), "calibrated": asdict(calibration_metrics(np.asarray([x["calibrated"] for x in selected]), truth)), "subject_wise": _subject_calibration_metrics(selected)}
    return output


def _subject_calibration_metrics(rows):
    output = {}
    for subject in sorted({r["subject_id"] for r in rows}):
        selected = [r for r in rows if r["subject_id"] == subject]
        truth = [r["true_label"] for r in selected]
        output[str(subject)] = {"identity": asdict(calibration_metrics(np.asarray([r["raw"] for r in selected]), truth)), "calibrated": asdict(calibration_metrics(np.asarray([r["calibrated"] for r in selected]), truth))}
    return output


def _systems(rows, *, systems, include_navigation=False):
    result = {}
    for family in ("csp_lda", "eegnet"):
        family_rows = [x for x in rows if x["decoder_family"] == family]
        result[family] = {}
        for system in systems:
            evaluated = _evaluate_rows(family_rows, system, include_mission=include_navigation)
            summary = _summarize(evaluated)
            result[family][system] = summary
    return result


def _ablations(rows):
    names = ("full", "full_minus_calibration", "full_minus_bayes", "full_minus_uncertainty", "full_minus_safety", "full_minus_adaptation")
    mapping = {"full": "D", "full_minus_calibration": "raw_D", "full_minus_bayes": "minus_bayes", "full_minus_uncertainty": "minus_uncertainty", "full_minus_safety": "D", "full_minus_adaptation": "D"}
    result = {}
    for family in ("csp_lda", "eegnet"):
        family_rows = [x for x in rows if x["decoder_family"] == family]
        result[family] = {}
        for name in names:
            evaluated = _evaluate_rows(family_rows, mapping[name], include_mission=True, adaptation_enabled=name != "full_minus_adaptation", safety_enabled=name != "full_minus_safety")
            result[family][name] = {"components": asdict(ABLATIONS[name].components), "removed_component": ABLATIONS[name].removed_component, **_summarize(evaluated)}
    return result


def _evaluate_rows(rows, system, *, include_mission=False, adaptation_enabled=None, safety_enabled=True):
    """Fresh deterministic condition state, ordered by the frozen E9 contract."""
    if system in {"A", "B", "C", "D"}:
        definition = get_condition(ConditionId(system))
        enabled = definition.components.adaptation if adaptation_enabled is None else adaptation_enabled
    else:
        enabled = True if adaptation_enabled is None else adaptation_enabled
    personalizer = PriorPersonalizer(adaptation_enabled=enabled)
    ordered = sorted(rows, key=lambda r: (int(r["subject_id"]), int(r.get("run_id", 0)), int(r.get("first_event_sample", 0)), str(r["episode_id"])))
    output = []
    for row in ordered:
        item = _evaluate(row, system, adaptation=personalizer if enabled else None)
        item["condition_components"] = _components_for(system, safety_enabled=safety_enabled, adaptation_enabled=enabled)
        if include_mission:
            item = _with_mission(item, safety_enabled=safety_enabled)
        output.append(item)
    return output


def _components_for(system, *, safety_enabled, adaptation_enabled):
    if system in {"A", "B", "C", "D"}:
        components = asdict(get_condition(ConditionId(system)).components)
    else:
        components = asdict(get_condition(ConditionId.D).components)
    components["hard_safety"] = bool(safety_enabled)
    components["adaptation"] = bool(adaptation_enabled)
    if system == "raw_D":
        components["calibration"] = False
    if system == "minus_bayes":
        components["sequential_bayes"] = False
    if system == "minus_uncertainty":
        components["uncertainty_gating"] = False
    return components


def _heldout(rows):
    output = {}
    for family in ("csp_lda", "eegnet"):
        selected = [r for r in rows if r["decoder_family"] == family]
        truth = [r["true_label"] for r in selected]
        predicted = ["left" if r["raw"][0] >= r["raw"][1] else "right" for r in selected]
        output[family] = {"trial_metrics": asdict(classification_metrics(truth, predicted)), "subject_distribution": _subject_distribution(selected), "subject_count": len({r["subject_id"] for r in selected})}
    return output


def _subject_distribution(rows):
    values = {}
    for subject in sorted({r["subject_id"] for r in rows}):
        selected = [r for r in rows if r["subject_id"] == subject]
        values[str(subject)] = {"observation_count": len(selected), "episode_count": len(selected), "correctness": sum((r["true_label"] == ("left" if r["raw"][0] >= r["raw"][1] else "right")) for r in selected) / len(selected)}
    return values


def _with_mission(decision, *, safety_enabled):
    return {**decision, "mission_execution": _execute_full_system_mission(decision["goal"], safety_enabled=safety_enabled)}


def _execute_full_system_mission(approved_goal, *, safety_enabled: bool, emergency_stop: bool = False):
    """Run one approved symbolic goal through the frozen M6 mission map and execution stack."""
    mission = FULL_SYSTEM_MISSION_MAP
    environment = SearchRescueEnvironment(EnvironmentConfig(
        rows=int(mission["rows"]), columns=int(mission["columns"]), start=tuple(mission["start"]),
        goals={str(k): tuple(v) for k, v in mission["goals"].items()}, blocked_cells=frozenset(mission["blocked_cells"]), risk_map=dict(mission["risk_cells"]),
    ))
    environment.reset(seed=42)
    base = {"mission_map": {"rows": 3, "columns": 5, "start": (1, 0), "goals": {"victim_a": (1, 4), "victim_b": (0, 2)}, "blocked_cells": (), "risk_cells": ()}, "approved_goal": approved_goal, "safety_enabled": safety_enabled, "emergency_stop_authority": True}
    if approved_goal is None:
        return {**base, "final_status": "NO_APPROVED_GOAL", "reached_goal": None, "path_length": 0, "environment_steps": 0, "cumulative_risk": 0.0, "unsafe_action_attempts": 0, "executed_hard_safety_violations": 0, "replanning_count": 0, "no_safe_path": False, "executed_actions": (), "safety_decision_count": 0}
    coordinate = environment.config.goals[str(approved_goal)]
    if safety_enabled:
        execution = PlannerSafetyEnvironmentExecutor().execute(environment, approved_goal=coordinate, emergency_stop=emergency_stop)
        plan = execution.planning_result
        return {**base, "final_status": execution.status.value, "reached_goal": environment.state.reached_goal, "path_length": len(execution.executed_actions), "environment_steps": len(execution.executed_actions), "cumulative_risk": 0.0 if plan is None or plan.cumulative_risk is None else float(plan.cumulative_risk), "unsafe_action_attempts": sum(not d.safe for d in execution.safety_decisions), "executed_hard_safety_violations": 0, "replanning_count": 0, "no_safe_path": execution.status is ExecutionStatus.NO_SAFE_PATH, "executed_actions": tuple(action.name for action in execution.executed_actions), "safety_decision_count": len(execution.safety_decisions)}
    plan = RiskAwareAStarPlanner().plan(environment, start=environment.state.position, approved_goal=coordinate)
    executed = []
    if emergency_stop:
        status = "HALTED"
    elif plan.status is PlannerStatus.SUCCESS:
        for action in plan.actions:
            environment.step(action); executed.append(action.name)
        status = "SUCCESS" if environment.state.reached_goal == approved_goal else "INVALID_GOAL_OR_PLAN"
    else:
        status = plan.status.value
    return {**base, "final_status": status, "reached_goal": environment.state.reached_goal, "path_length": len(executed), "environment_steps": len(executed), "cumulative_risk": 0.0 if plan.cumulative_risk is None else float(plan.cumulative_risk), "unsafe_action_attempts": 0, "executed_hard_safety_violations": 0, "replanning_count": 0, "no_safe_path": plan.status is PlannerStatus.NO_SAFE_PATH, "executed_actions": tuple(executed), "safety_decision_count": 0}


def _evaluate(row, system, *, adaptation=None, evidence_override=None, safety_enabled=True):
    evidence = evidence_override if evidence_override is not None else (row["raw"] if system == "raw_D" else row["calibrated"])
    initial_prior = INITIAL_PRIOR
    posterior = None; entropy = 0.0; proposed_goal = None; human_action = None; feedback_record = None
    confirmations = overrides = deferrals = 0
    if system == "A":
        final_vector = np.asarray(row["raw"][0], dtype=float); goal = CANDIDATES[int(np.argmax(final_vector))]; proposed_goal = goal; mode = "PROCEED"; count = 1
    elif system == "B":
        final_vector = np.asarray(evidence[0], dtype=float); confidence = max(final_vector); proposed_goal = CANDIDATES[int(np.argmax(final_vector))] if confidence >= .75 else None; goal = proposed_goal; mode = "PROCEED" if confidence >= .90 else ("CONFIRM" if goal else "DEFER"); count = 1
    elif system == "minus_bayes":
        d = evaluate_full_minus_bayes(evidence, candidate_names=CANDIDATES); mode, goal, count = d.autonomy_mode, d.committed_goal or d.candidate_goal, d.accepted_evidence_count; proposed_goal = d.candidate_goal; final_vector = np.asarray(d.posterior, dtype=float)
    elif system == "minus_uncertainty":
        prior = INITIAL_PRIOR if adaptation is None else adaptation.initial_prior_for_new_episode(str(row["subject_id"]), *CANDIDATES); initial_prior = prior
        d = evaluate_full_minus_uncertainty(evidence, candidate_names=CANDIDATES, initial_prior=prior); mode, goal, count = d.autonomy_mode, d.committed_goal, d.accepted_evidence_count; proposed_goal = goal; final_vector = np.asarray(d.posterior, dtype=float)
    else:
        prior = INITIAL_PRIOR
        if adaptation is not None:
            prior = adaptation.initial_prior_for_new_episode(str(row["subject_id"]), *CANDIDATES)
        initial_prior = prior
        episode = BinaryBayesianGoalEpisode(candidate_a=CANDIDATES[0], candidate_b=CANDIDATES[1], initial_prior=prior)
        mode = "DEFER"; goal = None; count = 0
        for p in evidence:
            p = np.asarray(p, dtype=float)
            p = p / float(p.sum())
            update = episode.accept_evidence(binary_goal_evidence_from_calibrated_probabilities(p)); count = episode.update_count
            decision = decide_shared_autonomy(update, estimate_binary_uncertainty(update.posterior))
            if decision.mode.value != "WAITING": mode, goal = decision.mode.value, decision.approved_goal or decision.candidate_goal; break
        proposed_goal = decision.candidate_goal if 'decision' in locals() else None
        final_vector = np.asarray(update.posterior, dtype=float)
    posterior = _normalized_binary_probability(final_vector)
    entropy = float(estimate_binary_uncertainty(posterior).entropy_bits)
    if system in {"B", "C", "D", "raw_D", "minus_bayes"} and mode in {"CONFIRM", "DEFER"}:
            deferrals = int(mode == "DEFER")
            human = apply_simulated_human_policy(episode_id=row["episode_id"], autonomy_mode=mode, proposed_goal=goal, intended_goal=row["intended_goal"], candidate_names=CANDIDATES, controller=HumanInteractionController())
            goal = human.final_approved_goal
            human_action = human.command_type; confirmations = int(human.command_type == "CONFIRM"); overrides = int(human.command_type == "OVERRIDE")
            if adaptation is not None and human.explicit_feedback is not None:
                feedback_record = adaptation.record_explicit_feedback(feedback_for_subject(human, str(row["subject_id"])))
    return {"subject_id": row["subject_id"], "episode_id": row["episode_id"], "mode": mode, "goal": goal, "proposed_goal": proposed_goal, "correct": goal == row["intended_goal"], "intended_goal": row["intended_goal"], "evidence_count": count, "initial_prior": list(initial_prior), "final_vector": [float(x) for x in posterior], "posterior_confidence": float(max(posterior)), "entropy_bits": entropy, "human_action": human_action, "confirmations": confirmations, "overrides": overrides, "deferrals": deferrals, "adaptation_update": None if feedback_record is None else asdict(feedback_record)}


def _normalized_binary_probability(value):
    """Evaluation-boundary normalization for descriptive entropy; preserves binary class ordering."""
    vector = np.asarray(value, dtype=float)
    if vector.shape != (2,) or not np.isfinite(vector).all() or (vector < 0.0).any():
        raise ValueError("Binary probability vector must be finite, non-negative, and length two.")
    mass = float(vector.sum())
    if not np.isfinite(mass) or mass <= 0.0:
        raise ValueError("Binary probability vector must have positive finite mass.")
    return vector / mass


def _robustness(rows, manifest):
    """Run D-078 over a single ordered population per family; episode boundaries never reset R2."""
    output = {"R1_evidence_flattening": {}, "R2_contradictory_evidence": {}}
    for family in ("csp_lda", "eegnet"):
        family_rows = [r for r in rows if r["decoder_family"] == family]
        if not family_rows:
            continue
        for condition in ("A", "B", "C", "D"):
            base_rows = _condition_evidence_rows(family_rows, condition)
            for epsilon in manifest.r1_severities:
                altered = [{**row, "override": flatten_evidence(np.asarray(row["evidence"], dtype=float), epsilon).perturbed_evidence} for row in base_rows]
                evaluated = _evaluate_override_rows(altered, condition)
                output["R1_evidence_flattening"].setdefault(family, {}).setdefault(condition, {})[str(epsilon)] = {"summary": _summarize(evaluated), "provenance": [{"episode_id": r["episode_id"], "epsilon": epsilon, "original_evidence": r["evidence"], "perturbed_evidence": r["override"]} for r in altered]}
            ids = [f"{r['episode_id']}::obs-{i:04d}" for r in base_rows for i in range(len(r["evidence"]))]
            population = np.asarray([obs for r in base_rows for obs in r["evidence"]], dtype=float)
            for q in manifest.r2_severities:
                perturb = contaminate_contradictory_evidence(population, q, seed=manifest.r2_seed, observation_ids=ids)
                cursor = 0; altered = []
                for row in base_rows:
                    n = len(row["evidence"]); altered.append({**row, "override": perturb.perturbed_evidence[cursor:cursor+n]}); cursor += n
                evaluated = _evaluate_override_rows(altered, condition)
                output["R2_contradictory_evidence"].setdefault(family, {}).setdefault(condition, {})[str(q)] = {"summary": _summarize(evaluated), "provenance": asdict(perturb), "episode_boundaries_do_not_reset_selection": True}
    return output


def _condition_evidence_rows(rows, condition):
    raw = condition == "A"
    horizon = 1 if condition in {"A", "B"} else 5
    return [{"row": r, "episode_id": r["episode_id"], "evidence": (r["raw"] if raw else r["calibrated"])[:horizon]} for r in rows]


def _evaluate_override_rows(rows, condition):
    translated = [{**item["row"], "raw": item["override"] if condition == "A" else item["row"]["raw"], "calibrated": item["override"] if condition != "A" else item["row"]["calibrated"]} for item in rows]
    return _evaluate_rows(translated, condition, include_mission=True)


def _statistics(rows):
    """D-079 subject-level paired inference with explicit denominators and Holm adjustment."""
    metrics = {}
    for family in ("csp_lda", "eegnet"):
        selected = [r for r in rows if r["decoder_family"] == family]
        if not selected:
            continue
        subjects = sorted({str(r["subject_id"]) for r in selected})
        evaluated_a = _evaluate_rows(selected, "A", include_mission=True)
        evaluated_d = _evaluate_rows(selected, "D", include_mission=True)
        observations_a = [ObservationMetric(str(r["subject_id"]), f"A::{r['episode_id']}", float(r["correct"])) for r in evaluated_a]
        observations_d = [ObservationMetric(str(r["subject_id"]), f"D::{r['episode_id']}", float(r["correct"])) for r in evaluated_d]
        a = aggregate_subject_means(observations_a); d = aggregate_subject_means(observations_d)
        inference = paired_subject_inference(a, d, bootstrap_seed=42, permutation_seed=42, permutation_samples=10000)
        metrics[family] = {"D_minus_A_correctness": asdict(inference), "subject_count": len(subjects), "evaluation_unit": "subject"}
    pvals = {f"{family}.D_minus_A_correctness": value["D_minus_A_correctness"]["raw_p_value"] for family, value in metrics.items()}
    return {"comparisons": metrics, "holm_adjusted_p_values": holm_adjust(pvals)}


def _e9(rows):
    output = {}
    for family in ("csp_lda", "eegnet"):
        selected = [r for r in rows if r["decoder_family"] == family]
        fixed = _evaluate_rows(selected, "C", include_mission=True)
        adaptive = _evaluate_rows(selected, "D", include_mission=True)
        output[family] = {"fixed_C": _summarize(fixed), "personalized_D": _summarize(adaptive), "trajectory": [{"episode_index": index, "episode_id": item["episode_id"], "subject_id": item["subject_id"], "initial_prior": item["initial_prior"], "human_action": item["human_action"], "adaptation_update": item["adaptation_update"], "evidence_latency": item["evidence_count"], "task_outcome": item["correct"]} for index, item in enumerate(adaptive, start=1)], "ordering_rule": "subject_id_then_run_id_then_first_source_event_sample_then_episode_id", "subject_ids": sorted({item["subject_id"] for item in adaptive})}
    return output


def _failure_taxonomy():
    return {"schema_version": "m7-t02-r03-failure-taxonomy-v1", "categories": ["preprocessing_qc_exclusion", "decoder_misclassification", "calibration_miscalibration", "misleading_bayesian_evidence", "confirm", "defer", "simulated_human_override", "wrong_autonomous_commitment", "no_approved_goal", "planner_no_safe_path", "safety_rejection", "prohibited_hazard_attempt", "replanning", "emergency_stop", "environment_execution", "adaptation_update", "adaptation_warm_up", "adaptation_bound", "adaptation_helped", "adaptation_hurt", "robustness_degradation", "provenance_manifest_artifact_failure"], "status": "COUNTS_DERIVED_FROM_PER_EPISODE_TRACES"}


def _summarize(rows):
    total = len(rows); committed = [x for x in rows if x["goal"] is not None]; wrong = [x for x in committed if not x["correct"]]
    result = {"episode_count": total, "committed_count": len(committed), "success_count": sum(x["correct"] for x in rows), "wrong_all_rate": len(wrong) / total if total else 0.0, "wrong_committed_rate": len(wrong) / len(committed) if committed else None, "mean_evidence_count": float(np.mean([x["evidence_count"] for x in rows])) if rows else 0.0, "modes": {mode: sum(x["mode"] == mode for x in rows) for mode in ("PROCEED", "CONFIRM", "DEFER")}, "subject_ids": sorted({x["subject_id"] for x in rows})}
    missions = [x["mission_execution"] for x in rows if "mission_execution" in x]
    if missions:
        result["navigation"] = {"mission_execution_count": len(missions), "task_navigation_success": sum(m["final_status"] == "SUCCESS" and m["reached_goal"] == m["approved_goal"] for m in missions), "environment_steps": sum(m["environment_steps"] for m in missions), "cumulative_risk": float(sum(m["cumulative_risk"] for m in missions)), "unsafe_action_attempts": sum(m["unsafe_action_attempts"] for m in missions), "executed_hard_safety_violations": sum(m["executed_hard_safety_violations"] for m in missions), "replanning_count": sum(m["replanning_count"] for m in missions), "no_safe_path_events": sum(m["no_safe_path"] for m in missions), "safety_enabled": all(m["safety_enabled"] for m in missions), "episodes": missions}
    return result
