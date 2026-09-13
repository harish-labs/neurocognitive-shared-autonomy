"""Deterministic execution and accounting for the frozen M7-T02 S1-S7 suite."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from src.autonomy.environment import Action, EnvironmentConfig, SearchRescueEnvironment
from src.autonomy.execution import ExecutionStatus, PlannerSafetyEnvironmentExecutor
from src.autonomy.planner import PlannerStatus, RiskAwareAStarPlanner
from src.autonomy.replanning import ControlledReplanningCoordinator, ReplanTrigger
from src.autonomy.safety import SafetyController
from src.evaluation.final_contract import OPERATIONAL_SEED, SCENARIOS, ScenarioDefinition


class ScenarioExecutionError(ValueError):
    """Raised when deterministic scenario execution violates its frozen contract."""


@dataclass(frozen=True)
class ScenarioResult:
    scenario_id: str
    safety_enabled: bool
    environment: dict[str, Any]
    initial_state: tuple[int, int]
    goal: tuple[int, int]
    initial_plan_status: str
    initial_path: tuple[tuple[int, int], ...]
    initial_actions: tuple[str, ...]
    safety_decisions: tuple[dict[str, Any], ...]
    executed_actions: tuple[str, ...]
    visited_positions: tuple[tuple[int, int], ...]
    final_state: tuple[int, int]
    final_status: str
    reached_goal: bool
    planner_success: bool
    path_length: int
    movement_cost: float | None
    cumulative_risk: float | None
    risk_weighted_cost: float | None
    total_path_cost: float | None
    replanning_count: int
    unsafe_action_attempts: int
    executed_hard_safety_violations: int
    no_safe_path: bool
    unreachable: bool
    emergency_stop_success: bool | None
    environment_change_event_id: str | None
    environment_change_consumed: bool


def run_frozen_scenarios(*, safety_enabled: bool) -> tuple[ScenarioResult, ...]:
    return tuple(run_frozen_scenario(scenario, safety_enabled=safety_enabled) for scenario in SCENARIOS)


def run_frozen_scenario(scenario: ScenarioDefinition, *, safety_enabled: bool) -> ScenarioResult:
    if scenario not in SCENARIOS:
        raise ScenarioExecutionError("Only exact frozen S1-S7 definitions may be executed.")
    environment = _environment(scenario)
    environment.reset(seed=OPERATIONAL_SEED)
    planner = RiskAwareAStarPlanner()
    initial_plan = planner.plan(environment, start=scenario.start, approved_goal=scenario.goal)

    if scenario.scenario_id == "S5":
        return _run_s5(scenario, environment, initial_plan, safety_enabled=safety_enabled)
    if scenario.scenario_id == "S6":
        return _run_s6(scenario, environment, initial_plan, safety_enabled=safety_enabled)
    if safety_enabled:
        execution = PlannerSafetyEnvironmentExecutor().execute(
            environment,
            approved_goal=scenario.goal,
            emergency_stop=scenario.inject_emergency_stop,
        )
        result = _from_execution(scenario, environment, initial_plan, execution)
    else:
        result = _without_safety(scenario, environment, initial_plan)
    _validate_expected(scenario, result)
    return result


def scenario_result_mapping(result: ScenarioResult) -> dict[str, Any]:
    return asdict(result)


def _environment(scenario: ScenarioDefinition, *, replacement: bool = False) -> SearchRescueEnvironment:
    start = scenario.replacement_start if replacement else scenario.start
    blocked = scenario.replacement_blocked_cells if replacement else scenario.blocked_cells
    if start is None:
        raise ScenarioExecutionError("Replacement scenario requires a frozen replacement start.")
    return SearchRescueEnvironment(
        EnvironmentConfig(
            rows=scenario.rows,
            columns=scenario.columns,
            start=start,
            goals={scenario.goal_name: scenario.goal},
            blocked_cells=frozenset(blocked),
            risk_map=dict(scenario.risk_cells),
        )
    )


def _from_execution(scenario, environment, plan, execution) -> ScenarioResult:
    safety = tuple(
        {
            "status": decision.status.value,
            "proposed_action": _action_name(decision.proposed_action),
            "approved_action": None if decision.approved_action is None else decision.approved_action.name,
            "safe": decision.safe,
            "intervention_type": decision.intervention_type.value,
            "requires_replan": decision.requires_replan,
            "current_position": decision.current_position,
            "proposed_next_position": decision.proposed_next_position,
        }
        for decision in execution.safety_decisions
    )
    return ScenarioResult(
        scenario_id=scenario.scenario_id,
        safety_enabled=True,
        environment=_scenario_environment_mapping(scenario),
        initial_state=scenario.start,
        goal=scenario.goal,
        initial_plan_status=plan.status.value,
        initial_path=plan.path,
        initial_actions=tuple(action.name for action in plan.actions),
        safety_decisions=safety,
        executed_actions=tuple(action.name for action in execution.executed_actions),
        visited_positions=execution.visited_positions,
        final_state=execution.final_position,
        final_status=execution.status.value,
        reached_goal=execution.status is ExecutionStatus.SUCCESS,
        planner_success=plan.status is PlannerStatus.SUCCESS,
        path_length=len(execution.executed_actions),
        movement_cost=plan.movement_cost,
        cumulative_risk=plan.cumulative_risk,
        risk_weighted_cost=plan.risk_cost,
        total_path_cost=plan.path_cost,
        replanning_count=0,
        unsafe_action_attempts=sum(not decision.safe for decision in execution.safety_decisions),
        executed_hard_safety_violations=0,
        no_safe_path=execution.status is ExecutionStatus.NO_SAFE_PATH,
        unreachable=execution.status is ExecutionStatus.INVALID_GOAL_OR_PLAN,
        emergency_stop_success=(len(execution.executed_actions) == 0 if scenario.inject_emergency_stop else None),
        environment_change_event_id=None,
        environment_change_consumed=False,
    )


def _without_safety(scenario, environment, plan) -> ScenarioResult:
    executed: list[str] = []
    visited = [scenario.start]
    if scenario.inject_emergency_stop:
        status = "HALTED"
    elif plan.status is PlannerStatus.NO_SAFE_PATH:
        status = "NO_SAFE_PATH"
    elif plan.status is not PlannerStatus.SUCCESS:
        status = "INVALID_GOAL_OR_PLAN"
    else:
        for action in plan.actions:
            environment.step(action)
            executed.append(action.name)
            visited.append(environment.state.position)
        status = "SUCCESS" if environment.state.position == scenario.goal else "INVALID_GOAL_OR_PLAN"
    return ScenarioResult(
        scenario_id=scenario.scenario_id,
        safety_enabled=False,
        environment=_scenario_environment_mapping(scenario),
        initial_state=scenario.start,
        goal=scenario.goal,
        initial_plan_status=plan.status.value,
        initial_path=plan.path,
        initial_actions=tuple(action.name for action in plan.actions),
        safety_decisions=(),
        executed_actions=tuple(executed),
        visited_positions=tuple(visited),
        final_state=environment.state.position,
        final_status=status,
        reached_goal=status == "SUCCESS",
        planner_success=plan.status is PlannerStatus.SUCCESS,
        path_length=len(executed),
        movement_cost=plan.movement_cost,
        cumulative_risk=plan.cumulative_risk,
        risk_weighted_cost=plan.risk_cost,
        total_path_cost=plan.path_cost,
        replanning_count=0,
        unsafe_action_attempts=0,
        executed_hard_safety_violations=0,
        no_safe_path=status == "NO_SAFE_PATH",
        unreachable=status == "INVALID_GOAL_OR_PLAN",
        emergency_stop_success=(len(executed) == 0 if scenario.inject_emergency_stop else None),
        environment_change_event_id=None,
        environment_change_consumed=False,
    )


def _run_s5(scenario, environment, initial_plan, *, safety_enabled: bool) -> ScenarioResult:
    replacement = _environment(scenario, replacement=True)
    replacement.reset(seed=OPERATIONAL_SEED)
    if safety_enabled:
        replan = ControlledReplanningCoordinator().replan(
            environment,
            replacement,
            event_id=scenario.environment_change_event_id,
            trigger=ReplanTrigger.ENVIRONMENT_CHANGED,
            approved_goal=scenario.goal,
        )
        if replan.execution_result is None:
            raise ScenarioExecutionError("Frozen S5 replanning did not produce an execution trace.")
        base = _from_execution(scenario, replacement, initial_plan, replan.execution_result)
        result = ScenarioResult(
            **{
                **asdict(base),
                "final_status": replan.status.value,
                "replanning_count": 1,
                "environment_change_event_id": str(replan.event_id),
                "environment_change_consumed": replan.consumed_event,
            }
        )
    else:
        replacement_plan = RiskAwareAStarPlanner().plan(replacement, start=scenario.start, approved_goal=scenario.goal)
        base = _without_safety(scenario, replacement, replacement_plan)
        result = ScenarioResult(
            **{
                **asdict(base),
                "initial_plan_status": initial_plan.status.value,
                "initial_path": initial_plan.path,
                "initial_actions": tuple(action.name for action in initial_plan.actions),
                "replanning_count": 1,
                "environment_change_event_id": scenario.environment_change_event_id,
                "environment_change_consumed": True,
            }
        )
    _validate_expected(scenario, result)
    return result


def _run_s6(scenario, environment, initial_plan, *, safety_enabled: bool) -> ScenarioResult:
    action = Action[scenario.safety_probe_action or ""]
    decision = SafetyController().check(
        environment,
        current_position=scenario.start,
        proposed_action=action,
    )
    if safety_enabled:
        safety_decisions = ({
            "status": decision.status.value,
            "proposed_action": action.name,
            "approved_action": None,
            "safe": decision.safe,
            "intervention_type": decision.intervention_type.value,
            "requires_replan": decision.requires_replan,
            "current_position": decision.current_position,
            "proposed_next_position": decision.proposed_next_position,
        },)
        executed: tuple[str, ...] = ()
        visited = (scenario.start,)
        status = decision.status.value
        violations = 0
    else:
        environment.step(action)
        safety_decisions = ()
        executed = (action.name,)
        visited = (scenario.start, environment.state.position)
        status = "EXECUTED_WITHOUT_HARD_SAFETY"
        violations = 1
    result = ScenarioResult(
        scenario_id="S6",
        safety_enabled=safety_enabled,
        environment=_scenario_environment_mapping(scenario),
        initial_state=scenario.start,
        goal=scenario.goal,
        initial_plan_status=initial_plan.status.value,
        initial_path=initial_plan.path,
        initial_actions=tuple(item.name for item in initial_plan.actions),
        safety_decisions=safety_decisions,
        executed_actions=executed,
        visited_positions=visited,
        final_state=environment.state.position,
        final_status=status,
        reached_goal=False,
        planner_success=initial_plan.status is PlannerStatus.SUCCESS,
        path_length=len(executed),
        movement_cost=float(len(executed)),
        cumulative_risk=(1.0 if executed else 0.0),
        risk_weighted_cost=(2.0 if executed else 0.0),
        total_path_cost=(3.0 if executed else 0.0),
        replanning_count=0,
        unsafe_action_attempts=1,
        executed_hard_safety_violations=violations,
        no_safe_path=False,
        unreachable=False,
        emergency_stop_success=None,
        environment_change_event_id=None,
        environment_change_consumed=False,
    )
    _validate_expected(scenario, result)
    return result


def _validate_expected(scenario: ScenarioDefinition, result: ScenarioResult) -> None:
    if scenario.scenario_id == "S4" and (not result.no_safe_path or result.path_length != 0):
        raise ScenarioExecutionError("S4 must report NO_SAFE_PATH with zero movement.")
    if scenario.scenario_id == "S5" and (result.replanning_count != 1 or not result.environment_change_consumed):
        raise ScenarioExecutionError("S5 must consume exactly one stable environment-change event.")
    if scenario.scenario_id == "S6" and result.safety_enabled and result.final_status != "REPLAN_REQUIRED":
        raise ScenarioExecutionError("S6 safety-on probe must require replanning.")
    if scenario.scenario_id == "S7" and result.emergency_stop_success is not True:
        raise ScenarioExecutionError("S7 must execute zero movement after emergency STOP.")


def _scenario_environment_mapping(scenario: ScenarioDefinition) -> dict[str, Any]:
    return {
        "rows": scenario.rows,
        "columns": scenario.columns,
        "start": scenario.start,
        "goals": {scenario.goal_name: scenario.goal},
        "blocked_cells": scenario.blocked_cells,
        "risk_cells": scenario.risk_cells,
        "replacement_start": scenario.replacement_start,
        "replacement_blocked_cells": scenario.replacement_blocked_cells,
    }


def _action_name(value: object) -> str:
    return value.name if isinstance(value, Action) else str(value)
