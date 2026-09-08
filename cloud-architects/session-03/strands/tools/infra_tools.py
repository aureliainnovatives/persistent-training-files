"""
Simulated infrastructure tools.

These deliberately use local deterministic data so the lab needs no AWS
credentials. Replace these implementations with boto3/API/MCP integrations
later without changing the overall agent design.
"""

import json
from pathlib import Path
from strands import tool

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def _load(name):
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)

@tool
def get_cloudwatch_metrics(service: str) -> dict:
    """Get recent simulated CloudWatch-style metrics for a named service.
    Use this when investigating latency, CPU, memory, request volume or 5xx errors.
    """
    data = _load("metrics.json")
    return data.get(service, {"error": f"No metrics found for {service}"})

@tool
def get_application_logs(service: str) -> dict:
    """Get recent simulated application log events for a service.
    Use this to investigate errors, timeouts, exceptions and dependency failures.
    """
    data = _load("logs.json")
    return data.get(service, {"error": f"No logs found for {service}"})

@tool
def get_recent_deployments(service: str) -> dict:
    """Get recent simulated deployment history for a service.
    Use this to correlate an incident with a release or configuration change.
    """
    data = _load("deployments.json")
    return data.get(service, {"error": f"No deployments found for {service}"})

@tool
def get_instance_health(service: str) -> dict:
    """Get simulated compute/instance health for a service.
    Use this to determine whether infrastructure hosts are unhealthy.
    """
    data = _load("health.json")
    return data.get(service, {"error": f"No health data found for {service}"})

@tool
def read_runbook(topic: str) -> dict:
    """Read a simulated operations runbook.
    Use this after identifying a likely failure mode and needing safe remediation guidance.
    """
    data = _load("runbooks.json")
    topic_lower = topic.lower()
    for key, value in data.items():
        if key.lower() in topic_lower or topic_lower in key.lower():
            return {key: value}
    return {"available_runbooks": list(data.keys())}
