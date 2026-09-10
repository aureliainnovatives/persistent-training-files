"""Deterministic implementations for AgentCore Harness inline functions."""

from copy import deepcopy
from datetime import datetime

INCIDENTS = {
    "INC-DEVOPS-001": {
        "incident_id": "INC-DEVOPS-001",
        "service": "checkout-api",
        "severity": "SEV-2",
        "status": "INVESTIGATING",
        "region": "ap-south-1",
        "started_at": "2026-09-09T10:42:00+05:30",
        "symptoms": ["Checkout requests timing out", "HTTP 5xx elevated", "p95 latency elevated"],
    }
}

METRICS = {
    "checkout-api": {
        "baseline": {"cpu_percent": 42, "memory_percent": 58, "p95_latency_ms": 210,
                     "http_5xx_percent": 0.3, "requests_per_second": 820},
        "current": {"cpu_percent": 46, "memory_percent": 61, "p95_latency_ms": 2450,
                    "http_5xx_percent": 12.8, "requests_per_second": 835},
    }
}

LOGS = {
    "checkout-api": [
        {"timestamp": "2026-09-09T10:42:18+05:30", "level": "ERROR",
         "message": "HikariPool-1 - Connection is not available, request timed out after 30000ms."},
        {"timestamp": "2026-09-09T10:42:19+05:30", "level": "ERROR",
         "message": "java.sql.SQLTransientConnectionException: connection acquisition timeout"},
        {"timestamp": "2026-09-09T10:43:02+05:30", "level": "WARN",
         "message": "POST /checkout completed with HTTP 500 after 30120ms"},
    ]
}

DEPLOYMENTS = {
    "checkout-api": [
        {"deployed_at": "2026-09-09T10:39:00+05:30", "version": "v4.7", "status": "SUCCEEDED",
         "change_summary": "Checkout DB connection-pool tuning",
         "configuration_changes": {"DB_POOL_MAX": {"before": 80, "after": 15}}},
        {"deployed_at": "2026-09-08T16:10:00+05:30", "version": "v4.6", "status": "SUCCEEDED",
         "change_summary": "Logging improvements", "configuration_changes": {}},
    ]
}

ECS_HEALTH = {
    "checkout-api": {
        "cluster": "production", "desired_tasks": 6, "running_tasks": 6,
        "healthy_tasks": 6, "task_restarts_last_hour": 0, "deployment_status": "COMPLETED",
    }
}

RUNBOOK = {
    "title": "Runbook - Database Connection Pool Exhaustion",
    "symptoms": ["Connection acquisition timeout", "High API latency", "Elevated HTTP 5xx",
                 "CPU and memory may remain normal"],
    "investigation": [
        "Confirm service tasks are healthy.",
        "Compare latency and error rate with baseline.",
        "Inspect logs for connection acquisition failures.",
        "Inspect recent deployments and configuration changes.",
        "Compare current connection-pool configuration with last known good configuration.",
        "Check whether traffic materially increased.",
    ],
    "reference": {"checkout-api_normal_db_pool_max": 80},
    "remediation": (
        "If exhaustion begins immediately after a deployment that changed pool configuration, "
        "establish correlation and prepare rollback. Production rollback requires human approval. "
        "After an approved change, monitor latency, 5xx, task health and DB connectivity."
    ),
}


def get_active_alerts(incident_id: str):
    return deepcopy(INCIDENTS.get(incident_id, {"error": f"Incident {incident_id} not found"}))


def get_cloudwatch_metrics(service_name: str, period_minutes: int = 15):
    data = METRICS.get(service_name)
    if not data:
        return {"error": f"Metrics for {service_name} not found"}
    result = deepcopy(data)
    result.update({"service_name": service_name, "period_minutes": period_minutes})
    return result


def get_application_logs(service_name: str, minutes: int = 15):
    events = LOGS.get(service_name)
    if events is None:
        return {"error": f"Logs for {service_name} not found"}
    return {"service_name": service_name, "minutes": minutes, "events": deepcopy(events)}


def get_recent_deployments(service_name: str, hours: int = 4):
    deployments = DEPLOYMENTS.get(service_name)
    if deployments is None:
        return {"error": f"Deployment history for {service_name} not found"}
    return {"service_name": service_name, "hours": hours, "deployments": deepcopy(deployments)}


def get_ecs_service_health(service_name: str):
    health = ECS_HEALTH.get(service_name)
    if not health:
        return {"error": f"ECS health for {service_name} not found"}
    result = deepcopy(health)
    result["service_name"] = service_name
    return result


def get_runbook(topic: str):
    q = topic.strip().lower()
    if "connection" in q and ("pool" in q or "database" in q):
        return deepcopy(RUNBOOK)
    return {"error": f"No runbook found for topic: {topic}",
            "available_topics": ["database connection pool exhaustion"]}


def request_remediation(service_name: str, action: str, reason: str):
    allowed = {"rollback", "restart", "scale"}
    if action not in allowed:
        return {"status": "REJECTED", "reason": f"Unsupported action: {action}",
                "allowed_actions": sorted(allowed)}
    if service_name not in METRICS:
        return {"status": "REJECTED", "reason": f"Unknown service: {service_name}"}

    return {
        "request_id": f"CHG-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "service_name": service_name,
        "action": action,
        "status": "PENDING_APPROVAL",
        "approval_required": True,
        "executed": False,
        "reason": reason,
        "message": "Human approval is required before this production-changing action can execute.",
    }


HANDLERS = {
    "get_active_alerts": get_active_alerts,
    "get_cloudwatch_metrics": get_cloudwatch_metrics,
    "get_application_logs": get_application_logs,
    "get_recent_deployments": get_recent_deployments,
    "get_ecs_service_health": get_ecs_service_health,
    "get_runbook": get_runbook,
    "request_remediation": request_remediation,
}


def execute_tool(name, arguments):
    if name not in HANDLERS:
        raise ValueError(f"No local implementation for inline function: {name}")
    return HANDLERS[name](**arguments)
