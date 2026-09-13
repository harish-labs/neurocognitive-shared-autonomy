"""Bayesian, shared-autonomy, planning, safety, and full-system metrics."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from src.autonomy.planner import PlannerStatus, PlanningResult
from src.autonomy.safety import SafetyDecision


class AutonomyMetricError(ValueError):
    """Raised when episode records cannot support unambiguous metrics."""


@dataclass(frozen=True)
class EpisodeRecord:
    episode_id: str
    subject_key: str
    true_goal: str
    committed_goal: str | None
    posterior_confidence: float
    entropy_bits: float
    accepted_evidence_count: int
    autonomy_mode: str
    confirmations: int = 0
    overrides: int = 0
    deferrals: int = 0
    pauses: int = 0
    stops: int = 0
    navigation_steps: int = 0
    path_length: int | None = None
    cumulative_risk: float | None = None
    path_cost: float | None = None
    replanning_count: int = 0
    proposed_actions: int = 0
    executed_actions: int = 0
    unsafe_action_attempts: int = 0
    executed_hard_safety_violations: int = 0
    no_safe_path: bool = False
    unreachable: bool = False
    reached_goal: str | None = None

    def validate(self) -> None:
        for name in ("episode_id", "subject_key", "true_goal", "autonomy_mode"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name):
                raise AutonomyMetricError(f"{name} must be a non-empty string.")
        if not 0.0 <= self.posterior_confidence <= 1.0:
            raise AutonomyMetricError("posterior_confidence must be within [0, 1].")
        if not 0.0 <= self.entropy_bits <= 1.0 + 1e-12:
            raise AutonomyMetricError("binary entropy_bits must be within [0, 1].")
        integer_fields = (
            "accepted_evidence_count", "confirmations", "overrides", "deferrals", "pauses", "stops",
            "navigation_steps", "replanning_count", "proposed_actions", "executed_actions",
            "unsafe_action_attempts", "executed_hard_safety_violations",
        )
        if any(isinstance(getattr(self, name), bool) or not isinstance(getattr(self, name), int) or getattr(self, name) < 0 for name in integer_fields):
            raise AutonomyMetricError("Episode counts must be non-negative integers.")
        if self.executed_actions > self.proposed_actions:
            raise AutonomyMetricError("executed_actions cannot exceed proposed_actions.")
        if self.executed_hard_safety_violations > self.executed_actions:
            raise AutonomyMetricError("Executed violations cannot exceed executed actions.")
        if self.path_length is not None and (isinstance(self.path_length, bool) or self.path_length < 0):
            raise AutonomyMetricError("path_length must be a non-negative integer when available.")
        for name in ("cumulative_risk", "path_cost"):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise AutonomyMetricError(f"{name} must be non-negative when available.")


@dataclass(frozen=True)
class RateMetric:
    numerator: int
    denominator: int
    rate: float | None
    denominator_unit: str


@dataclass(frozen=True)
class AutonomyMetrics:
    evaluation_unit: str
    evaluated_episodes: int
    committed_episodes: int
    correct_commitments: int
    commitment_correctness: RateMetric
    wrong_goal: RateMetric
    conditional_wrong_goal: RateMetric
    task_success: RateMetric
    proceed: RateMetric
    confirm: RateMetric
    defer: RateMetric
    confirmation_count: int
    override_count: int
    deferral_count: int
    pause_count: int
    stop_count: int
    human_intervention_count: int
    mean_posterior_confidence: float
    mean_entropy_bits: float
    posterior_episode_count: int
    mean_accepted_evidence_count: float
    decision_latency_episode_count: int
    total_navigation_steps: int
    path_length_sum: int
    path_length_episode_count: int
    cumulative_risk_sum: float
    cumulative_risk_episode_count: int
    path_cost_sum: float
    path_cost_episode_count: int
    replanning_count: int
    unsafe_action_attempts: int
    executed_hard_safety_violations: int
    safety_violation_rate: RateMetric
    no_safe_path_count: int
    unreachable_count: int


@dataclass(frozen=True)
class PlanningSafetyMetrics:
    evaluation_unit: str
    planning_request_count: int
    planning_success: RateMetric
    no_safe_path_count: int
    invalid_planning_request_count: int
    path_length_sum: int
    cumulative_risk_sum: float
    path_cost_sum: float
    replanning_count: int
    proposed_action_count: int
    unsafe_action_attempts: int
    executed_action_count: int
    executed_hard_safety_violations: int
    safety_violation_rate: RateMetric


def compute_planning_safety_metrics(
    planning_results: list[PlanningResult] | tuple[PlanningResult, ...],
    safety_decisions: list[SafetyDecision] | tuple[SafetyDecision, ...],
    *,
    replanning_count: int,
    executed_action_count: int,
    executed_hard_safety_violations: int,
) -> PlanningSafetyMetrics:
    """Account directly from accepted M4/M5 planner and safety result contracts."""
    if not planning_results:
        raise AutonomyMetricError("At least one controlled planning result is required.")
    if any(not isinstance(result, PlanningResult) for result in planning_results):
        raise AutonomyMetricError("planning_results must contain accepted PlanningResult values.")
    if any(not isinstance(decision, SafetyDecision) for decision in safety_decisions):
        raise AutonomyMetricError("safety_decisions must contain accepted SafetyDecision values.")
    counts = (replanning_count, executed_action_count, executed_hard_safety_violations)
    if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in counts):
        raise AutonomyMetricError("Planning/safety counts must be non-negative integers.")
    if executed_action_count > len(safety_decisions):
        raise AutonomyMetricError("Executed actions cannot exceed recorded safety proposals.")
    if executed_hard_safety_violations > executed_action_count:
        raise AutonomyMetricError("Executed hard-safety violations cannot exceed executed actions.")
    successes = [result for result in planning_results if result.status is PlannerStatus.SUCCESS]
    for result in successes:
        if None in (result.path_cost, result.movement_cost, result.cumulative_risk, result.risk_cost):
            raise AutonomyMetricError("Successful planning results require complete cost accounting.")
    invalid_count = sum(result.status in {PlannerStatus.INVALID_START, PlannerStatus.INVALID_GOAL} for result in planning_results)
    valid_count = len(planning_results) - invalid_count
    unsafe = sum(not decision.safe for decision in safety_decisions)
    return PlanningSafetyMetrics(
        evaluation_unit="controlled_planning_safety_scenario",
        planning_request_count=len(planning_results),
        planning_success=_rate(len(successes), valid_count, "valid_planning_request"),
        no_safe_path_count=sum(result.status is PlannerStatus.NO_SAFE_PATH for result in planning_results),
        invalid_planning_request_count=invalid_count,
        path_length_sum=sum(len(result.actions) for result in successes),
        cumulative_risk_sum=sum(float(result.cumulative_risk) for result in successes),
        path_cost_sum=sum(float(result.path_cost) for result in successes),
        replanning_count=replanning_count,
        proposed_action_count=len(safety_decisions),
        unsafe_action_attempts=unsafe,
        executed_action_count=executed_action_count,
        executed_hard_safety_violations=executed_hard_safety_violations,
        safety_violation_rate=_rate(executed_hard_safety_violations, executed_action_count, "executed_action"),
    )


def compute_autonomy_metrics(records: list[EpisodeRecord] | tuple[EpisodeRecord, ...]) -> AutonomyMetrics:
    if not records:
        raise AutonomyMetricError("At least one full-system episode is required.")
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, EpisodeRecord):
            raise AutonomyMetricError("All inputs must be EpisodeRecord instances.")
        record.validate()
        if record.episode_id in seen:
            raise AutonomyMetricError("episode_id values must be unique.")
        seen.add(record.episode_id)

    total = len(records)
    committed = [record for record in records if record.committed_goal is not None]
    correct = sum(record.committed_goal == record.true_goal for record in committed)
    wrong = len(committed) - correct
    success = sum(record.reached_goal == record.true_goal and not record.no_safe_path and not record.unreachable for record in records)
    mode_counts = {mode: sum(record.autonomy_mode == mode for record in records) for mode in ("PROCEED", "CONFIRM", "DEFER")}
    path_records = [record for record in records if record.path_length is not None]
    risk_records = [record for record in records if record.cumulative_risk is not None]
    cost_records = [record for record in records if record.path_cost is not None]
    executed_actions = sum(record.executed_actions for record in records)
    violations = sum(record.executed_hard_safety_violations for record in records)
    confirmations = sum(record.confirmations for record in records)
    overrides = sum(record.overrides for record in records)
    deferrals = sum(record.deferrals for record in records)
    pauses = sum(record.pauses for record in records)
    stops = sum(record.stops for record in records)
    return AutonomyMetrics(
        evaluation_unit="full_system_episode",
        evaluated_episodes=total,
        committed_episodes=len(committed),
        correct_commitments=correct,
        commitment_correctness=_rate(correct, len(committed), "committed_episode"),
        wrong_goal=_rate(wrong, total, "evaluated_episode"),
        conditional_wrong_goal=_rate(wrong, len(committed), "committed_episode"),
        task_success=_rate(success, total, "evaluated_episode"),
        proceed=_rate(mode_counts["PROCEED"], total, "evaluated_episode"),
        confirm=_rate(mode_counts["CONFIRM"], total, "evaluated_episode"),
        defer=_rate(mode_counts["DEFER"], total, "evaluated_episode"),
        confirmation_count=confirmations,
        override_count=overrides,
        deferral_count=deferrals,
        pause_count=pauses,
        stop_count=stops,
        human_intervention_count=confirmations + overrides + pauses + stops,
        mean_posterior_confidence=mean(record.posterior_confidence for record in records),
        mean_entropy_bits=mean(record.entropy_bits for record in records),
        posterior_episode_count=total,
        mean_accepted_evidence_count=mean(record.accepted_evidence_count for record in records),
        decision_latency_episode_count=total,
        total_navigation_steps=sum(record.navigation_steps for record in records),
        path_length_sum=sum(record.path_length for record in path_records if record.path_length is not None),
        path_length_episode_count=len(path_records),
        cumulative_risk_sum=sum(record.cumulative_risk for record in risk_records if record.cumulative_risk is not None),
        cumulative_risk_episode_count=len(risk_records),
        path_cost_sum=sum(record.path_cost for record in cost_records if record.path_cost is not None),
        path_cost_episode_count=len(cost_records),
        replanning_count=sum(record.replanning_count for record in records),
        unsafe_action_attempts=sum(record.unsafe_action_attempts for record in records),
        executed_hard_safety_violations=violations,
        safety_violation_rate=_rate(violations, executed_actions, "executed_action"),
        no_safe_path_count=sum(record.no_safe_path for record in records),
        unreachable_count=sum(record.unreachable for record in records),
    )


def _rate(numerator: int, denominator: int, denominator_unit: str) -> RateMetric:
    return RateMetric(numerator, denominator, numerator / denominator if denominator else None, denominator_unit)
