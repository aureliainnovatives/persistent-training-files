"""Deterministic mock FinOps data sources for the AgentCore Harness lab."""

from copy import deepcopy
from datetime import datetime

COST_SUMMARY = {
    "retail-platform": {
        "currency": "USD",
        "normal_monthly_run_rate": 18400,
        "month_to_date_spend": 15120,
        "current_month_forecast": 23900,
        "period_over_period_change_percent": 29.9,
        "major_cost_drivers": [
            {"service": "EC2", "current_estimated_month": 12100, "normal_month": 8900},
            {"service": "RDS", "current_estimated_month": 6100, "normal_month": 5900},
            {"service": "Other", "current_estimated_month": 5700, "normal_month": 3600},
        ],
    }
}

ANOMALIES = {
    "retail-platform": [
        {
            "anomaly_id": "COST-ANOM-001",
            "service": "EC2",
            "resource_id": "i-dev-analytics-01",
            "detected_change": "Resource changed from business-hours runtime to continuous 24x7 runtime.",
            "estimated_incremental_monthly_cost": 720,
            "confidence": "HIGH",
        }
    ]
}

UTILIZATION = {
    "i-dev-analytics-01": {
        "instance_type": "m6i.2xlarge",
        "environment": "development",
        "workload_criticality": "LOW",
        "average_cpu_percent": 9,
        "peak_cpu_percent": 31,
        "average_memory_percent": 22,
        "peak_memory_percent": 43,
        "current_runtime": "24x7",
        "rightsize_candidate": "m6i.large",
        "estimated_rightsize_monthly_savings": 310,
        "note": "Validate application memory headroom and performance before changing size.",
    }
}

SCHEDULES = {
    "i-dev-analytics-01": {
        "environment": "development",
        "current_schedule": "24x7",
        "required_schedule": "08:00-20:00 IST Monday-Friday",
        "estimated_runtime_reduction_percent": 64,
        "estimated_monthly_savings": 460,
        "operational_constraint": "Must be available before the development team's 08:00 start.",
    }
}

COMMITMENTS = {
    "retail-platform": {
        "eligible_scope": "stable production compute after excluding development waste",
        "stable_eligible_hourly_spend_usd": 8.20,
        "current_commitment_coverage_percent": 18,
        "one_year_candidate_hourly_commitment_usd": 6.50,
        "estimated_monthly_savings": 390,
        "estimated_savings_percent_on_covered_usage": 18,
        "guidance": "Eliminate avoidable runtime and right-size first; commit only to stable remaining eligible usage.",
    }
}

BUDGET = {
    "retail-platform": {
        "currency": "USD",
        "monthly_budget": 21000,
        "month_to_date_spend": 15120,
        "forecast_month_end": 23900,
        "forecast_variance_usd": 2900,
        "forecast_variance_percent": 13.8,
        "budget_status": "FORECAST_TO_EXCEED",
        "alert_thresholds_percent": [80, 100],
    }
}

POLICY = {
    "title": "FinOps Optimization and Commitment Policy",
    "rules": [
        "Validate workload criticality and peak utilization before right-sizing.",
        "Prefer eliminating unnecessary runtime before purchasing commitments.",
        "Non-production scheduling requires workload-owner approval.",
        "Production right-sizing requires change approval and post-change monitoring.",
        "Savings Plan purchases require finance/FinOps approval and must be based on stable eligible usage.",
        "Estimated savings must not be reported as realized savings.",
        "Budget threshold changes require FinOps owner approval.",
    ],
}


def get_cost_summary(scope: str, period: str = "current_month"):
    data = COST_SUMMARY.get(scope)
    if not data:
        return {"error": f"No cost summary found for {scope}"}
    result = deepcopy(data)
    result.update({"scope": scope, "period": period})
    return result


def get_cost_anomalies(scope: str):
    return {"scope": scope, "anomalies": deepcopy(ANOMALIES.get(scope, []))}


def get_resource_utilization(resource_id: str, days: int = 30):
    data = UTILIZATION.get(resource_id)
    if not data:
        return {"error": f"No utilization data found for {resource_id}"}
    result = deepcopy(data)
    result.update({"resource_id": resource_id, "analysis_days": days})
    return result


def get_commitment_analysis(scope: str, term_years: int):
    data = COMMITMENTS.get(scope)
    if not data:
        return {"error": f"No commitment analysis found for {scope}"}
    result = deepcopy(data)
    result.update({"scope": scope, "term_years": term_years})
    if term_years == 3:
        result["note"] = "Three-year term increases commitment risk; lab data does not provide a separate 3-year recommendation."
    return result


def get_schedule_analysis(resource_id: str):
    data = SCHEDULES.get(resource_id)
    if not data:
        return {"error": f"No schedule analysis found for {resource_id}"}
    result = deepcopy(data)
    result["resource_id"] = resource_id
    return result


def get_forecast_and_budget(scope: str):
    data = BUDGET.get(scope)
    if not data:
        return {"error": f"No forecast/budget data found for {scope}"}
    result = deepcopy(data)
    result["scope"] = scope
    return result


def get_finops_policy(topic: str):
    result = deepcopy(POLICY)
    result["requested_topic"] = topic
    return result


def request_finops_action(target: str, action: str, reason: str, estimated_monthly_savings: float = 0):
    allowed = {"rightsize", "schedule_stop_start", "purchase_savings_plan", "update_budget_alert"}
    if action not in allowed:
        return {"status": "REJECTED", "reason": "Unsupported action", "allowed_actions": sorted(allowed)}

    return {
        "request_id": f"FINOPS-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "target": target,
        "action": action,
        "reason": reason,
        "estimated_monthly_savings_usd": estimated_monthly_savings,
        "status": "PENDING_APPROVAL",
        "approval_required": True,
        "executed": False,
        "realized_savings_usd": 0,
        "message": "The optimization has not been executed. Approval is required before infrastructure or financial changes.",
    }


HANDLERS = {
    "get_cost_summary": get_cost_summary,
    "get_cost_anomalies": get_cost_anomalies,
    "get_resource_utilization": get_resource_utilization,
    "get_commitment_analysis": get_commitment_analysis,
    "get_schedule_analysis": get_schedule_analysis,
    "get_forecast_and_budget": get_forecast_and_budget,
    "get_finops_policy": get_finops_policy,
    "request_finops_action": request_finops_action,
}


def execute_tool(name, arguments):
    if name not in HANDLERS:
        raise ValueError(f"No local implementation for inline function: {name}")
    return HANDLERS[name](**arguments)
