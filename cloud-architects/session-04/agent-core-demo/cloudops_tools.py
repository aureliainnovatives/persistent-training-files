"""Local implementations of the Harness inline functions."""

import os
import boto3


# -------------------------------------------------------------------
# Demo incident data
# -------------------------------------------------------------------

INCIDENTS = {
    "INC-2026-0908-017": {
        "incident_id": "INC-2026-0908-017",
        "service": "checkout-api",
        "severity": "SEV-2",
        "status": "INVESTIGATING",
        "started_at": "2026-09-08T10:42:00+05:30",
        "symptoms": [
            "Checkout requests timing out",
            "HTTP 5xx elevated",
            "p95 latency elevated",
        ],
        "region": "ap-south-1",
    }
}


# -------------------------------------------------------------------
# Demo operational metrics
# -------------------------------------------------------------------

METRICS = {
    "checkout-api": {
        "service_name": "checkout-api",
        "baseline": {
            "cpu_percent": 42,
            "memory_percent": 58,
            "p95_latency_ms": 210,
            "http_5xx_percent": 0.3,
            "requests_per_second": 820,
        },
        "current": {
            "cpu_percent": 46,
            "memory_percent": 61,
            "p95_latency_ms": 2450,
            "http_5xx_percent": 12.8,
            "requests_per_second": 835,
        },
        "ecs": {
            "desired_tasks": 6,
            "running_tasks": 6,
            "healthy_tasks": 6,
        },
        "recent_signals": [
            "Database connection acquisition timeout observed",
            "No material CPU or memory saturation",
            "All ECS tasks remain healthy",
        ],
    }
}


# -------------------------------------------------------------------
# Tool 1: Incident details
# -------------------------------------------------------------------

def get_incident_details(incident_id: str):
    return INCIDENTS.get(
        incident_id,
        {"error": f"Incident {incident_id} not found"},
    )


# -------------------------------------------------------------------
# Tool 2: Service metrics
# -------------------------------------------------------------------

def get_service_metrics(
    service_name: str,
    metric_period_minutes: int = 15,
):
    data = METRICS.get(service_name)

    if not data:
        return {"error": f"Service {service_name} not found"}

    result = dict(data)
    result["metric_period_minutes"] = metric_period_minutes

    return result


# -------------------------------------------------------------------
# Tool 3: Bedrock Knowledge Base retrieval
# -------------------------------------------------------------------

def search_knowledge_base(query: str):
    """
    Search the configured Amazon Bedrock Knowledge Base and return
    the most relevant document chunks.
    """

    knowledge_base_id = os.getenv("KNOWLEDGE_BASE_ID")
    region = os.getenv("AWS_REGION", "ap-south-1")

    if not knowledge_base_id:
        return {
            "error": (
                "KNOWLEDGE_BASE_ID environment variable is not configured."
            )
        }

    client = boto3.client(
        "bedrock-agent-runtime",
        region_name=region,
    )

    try:
        response = client.retrieve(
            knowledgeBaseId=knowledge_base_id,
            retrievalQuery={
                "text": query
            },
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": 5
                }
            },
        )

        results = []

        for item in response.get("retrievalResults", []):
            result = {
                "text": item.get("content", {}).get("text", ""),
                "score": item.get("score"),
            }

            # Include source metadata when available
            if "location" in item:
                result["location"] = item["location"]

            if "metadata" in item:
                result["metadata"] = item["metadata"]

            results.append(result)

        return {
            "query": query,
            "knowledge_base_id": knowledge_base_id,
            "results": results,
        }

    except Exception as exc:
        return {
            "error": str(exc),
            "query": query,
        }


# -------------------------------------------------------------------
# Inline function dispatcher
# -------------------------------------------------------------------

HANDLERS = {
    "get_incident_details": get_incident_details,
    "get_service_metrics": get_service_metrics,
    "search_knowledge_base": search_knowledge_base,
}


def execute_tool(name, arguments):
    if name not in HANDLERS:
        raise ValueError(
            f"No local implementation for inline function: {name}"
        )

    return HANDLERS[name](**arguments)