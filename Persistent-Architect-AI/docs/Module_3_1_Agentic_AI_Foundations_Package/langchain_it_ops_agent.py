"""
LANGCHAIN SINGLE-AGENT DEMO — IT Operations / Incident Triage
==============================================================

Purpose
-------
Demonstrates one LangChain agent using an OpenAI chat model and 5 mock tools.
The LLM decides which tool(s) to call based on the user's request and can chain
multiple tool calls before producing the final response.

Install
-------
python -m pip install -U langchain langchain-openai

Set OpenAI API key
------------------
macOS / Linux:
    export OPENAI_API_KEY="your-api-key"

Windows PowerShell:
    $env:OPENAI_API_KEY="your-api-key"

Run
---
python langchain_it_ops_agent.py

Prompts to test
---------------
1. "What is the current health of server app-prod-01?"
2. "Check memory on app-prod-01 and tell me which process is probably causing the issue."
3. "Investigate INC-1042. Use whatever tools you need and recommend the next action."
4. "Check INC-1042, inspect the affected server, review recent deployments, and tell me whether rollback should be considered."
5. "Investigate the database latency issue on db-prod-01 and give me an evidence-based diagnosis."
6. "Restart nginx on app-prod-01."
   Expected: the agent should NOT execute it because the mock action tool requires approval.
7. "I approve CHG-9001. Restart nginx on app-prod-01."
   Expected: demonstrates an approved mock operational action.

Notes
-----
- All tools return MOCK data. No real server, ticketing system, monitoring
  platform, deployment platform, or service is accessed.
- OPENAI_API_KEY is read from the environment. Do not hard-code production keys.
- Change MODEL_NAME below if your account uses a different tool-capable OpenAI model.
"""

import os
import json
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent


MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


# ---------------------------------------------------------------------------
# MOCK ENTERPRISE DATA
# ---------------------------------------------------------------------------

MOCK_INCIDENTS = {
    "INC-1042": {
        "title": "Checkout API intermittent 5xx errors",
        "severity": "SEV-2",
        "status": "Investigating",
        "affected_service": "checkout-api",
        "affected_server": "app-prod-01",
        "started_at": "2026-08-25T07:42:00+05:30",
        "symptoms": [
            "HTTP 5xx rate increased to 8%",
            "p95 latency increased from 420 ms to 2.8 s",
            "memory pressure alert on app-prod-01",
        ],
    },
    "INC-1043": {
        "title": "Order database latency",
        "severity": "SEV-3",
        "status": "Open",
        "affected_service": "orders-db",
        "affected_server": "db-prod-01",
        "started_at": "2026-08-25T08:05:00+05:30",
        "symptoms": ["p95 query latency above 900 ms"],
    },
}

MOCK_SERVER_METRICS = {
    "app-prod-01": {
        "cpu_percent": 72,
        "memory_percent": 94,
        "disk_percent": 61,
        "load_average": 5.2,
        "network": "normal",
        "health": "degraded",
    },
    "db-prod-01": {
        "cpu_percent": 67,
        "memory_percent": 78,
        "disk_percent": 73,
        "load_average": 3.1,
        "network": "normal",
        "health": "degraded",
    },
}

MOCK_PROCESSES = {
    "app-prod-01": [
        {"pid": 4421, "name": "checkout-api", "cpu_percent": 48, "memory_percent": 63},
        {"pid": 1308, "name": "otel-collector", "cpu_percent": 8, "memory_percent": 7},
        {"pid": 991, "name": "nginx", "cpu_percent": 3, "memory_percent": 2},
    ],
    "db-prod-01": [
        {"pid": 5510, "name": "postgres", "cpu_percent": 55, "memory_percent": 51},
        {"pid": 1102, "name": "backup-agent", "cpu_percent": 4, "memory_percent": 6},
    ],
}

MOCK_DEPLOYMENTS = {
    "checkout-api": [
        {
            "deployment_id": "DEP-7781",
            "version": "checkout-api:2026.08.25.2",
            "deployed_at": "2026-08-25T07:28:00+05:30",
            "change": "New promotion-rule cache",
            "status": "completed",
        },
        {
            "deployment_id": "DEP-7764",
            "version": "checkout-api:2026.08.24.5",
            "deployed_at": "2026-08-24T18:10:00+05:30",
            "change": "Logging update",
            "status": "completed",
        },
    ],
    "orders-db": [],
}


def pretty(data) -> str:
    """Return predictable JSON strings to the agent."""
    return json.dumps(data, indent=2)


# ---------------------------------------------------------------------------
# TOOL 1 — INCIDENT / TICKETING SYSTEM
# ---------------------------------------------------------------------------

@tool
def get_incident(incident_id: str) -> str:
    """Get the current details of an incident from the mock ITSM system."""
    incident_id = incident_id.upper().strip()
    incident = MOCK_INCIDENTS.get(incident_id)

    if not incident:
        return pretty({
            "found": False,
            "incident_id": incident_id,
            "message": "No mock incident found."
        })

    return pretty({
        "found": True,
        "incident_id": incident_id,
        **incident
    })


# ---------------------------------------------------------------------------
# TOOL 2 — MONITORING / SERVER METRICS
# ---------------------------------------------------------------------------

@tool
def get_server_metrics(server_name: str) -> str:
    """Get current CPU, memory, disk, load and health metrics for a mock server."""
    server_name = server_name.lower().strip()
    metrics = MOCK_SERVER_METRICS.get(server_name)

    if not metrics:
        return pretty({
            "found": False,
            "server": server_name,
            "message": "Server is not present in the mock monitoring system."
        })

    return pretty({
        "found": True,
        "server": server_name,
        **metrics
    })


# ---------------------------------------------------------------------------
# TOOL 3 — PROCESS INSPECTION
# ---------------------------------------------------------------------------

@tool
def get_top_processes(server_name: str) -> str:
    """List the highest resource-consuming processes on a mock server."""
    server_name = server_name.lower().strip()
    processes = MOCK_PROCESSES.get(server_name)

    if processes is None:
        return pretty({
            "found": False,
            "server": server_name,
            "message": "No mock process data available."
        })

    ranked = sorted(
        processes,
        key=lambda p: p["cpu_percent"] + p["memory_percent"],
        reverse=True,
    )

    return pretty({
        "found": True,
        "server": server_name,
        "processes": ranked
    })


# ---------------------------------------------------------------------------
# TOOL 4 — DEPLOYMENT HISTORY
# ---------------------------------------------------------------------------

@tool
def get_recent_deployments(service_name: str) -> str:
    """Get recent mock production deployments for a service."""
    service_name = service_name.lower().strip()
    deployments = MOCK_DEPLOYMENTS.get(service_name)

    if deployments is None:
        return pretty({
            "found": False,
            "service": service_name,
            "message": "Service is not present in the mock deployment system."
        })

    return pretty({
        "found": True,
        "service": service_name,
        "deployments": deployments
    })


# ---------------------------------------------------------------------------
# TOOL 5 — OPERATIONAL ACTION WITH MOCK HITL GATE
# ---------------------------------------------------------------------------

@tool
def execute_service_action(
    server_name: str,
    service_name: str,
    action: str,
    approval_id: Optional[str] = None,
) -> str:
    """Execute a MOCK restart, stop, or start action. Requires an approval ID."""
    server_name = server_name.lower().strip()
    service_name = service_name.lower().strip()
    action = action.lower().strip()

    allowed_actions = {"restart", "start", "stop"}

    if action not in allowed_actions:
        return pretty({
            "executed": False,
            "reason": f"Unsupported action '{action}'.",
            "allowed_actions": sorted(allowed_actions),
        })

    if not approval_id:
        return pretty({
            "executed": False,
            "requires_human_approval": True,
            "server": server_name,
            "service": service_name,
            "requested_action": action,
            "message": "Action blocked. Obtain a change/approval ID before execution."
        })

    return pretty({
        "executed": True,
        "mock_execution": True,
        "server": server_name,
        "service": service_name,
        "action": action,
        "approval_id": approval_id,
        "result": f"MOCK: {service_name} {action} completed successfully on {server_name}."
    })


TOOLS = [
    get_incident,
    get_server_metrics,
    get_top_processes,
    get_recent_deployments,
    execute_service_action,
]


SYSTEM_PROMPT = """
You are an enterprise IT Operations Agent.

Your job is to investigate incidents and infrastructure problems using the
available tools, correlate evidence, and recommend the safest next action.

Operating rules:
1. Do not invent monitoring, incident, process, or deployment data.
2. Use tools whenever the user's question requires operational evidence.
3. You may call multiple tools and decide the next tool from previous results.
4. Distinguish observations from your diagnosis.
5. If evidence is insufficient, say what is missing.
6. Never claim that an operational action occurred unless the action tool says
   executed=true.
7. Restart/start/stop actions require a human approval/change ID.
8. Prefer recommendation over action when the user has not explicitly asked
   for an operational change.
9. Keep the final response structured:
   - Situation
   - Evidence
   - Diagnosis
   - Recommended next action
"""


def build_agent():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set.\n"
            'macOS/Linux: export OPENAI_API_KEY="your-api-key"\n'
            'PowerShell:   $env:OPENAI_API_KEY="your-api-key"'
        )

    model = ChatOpenAI(
        api_key="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",
        model=MODEL_NAME,
        temperature=0,
    )

    return create_agent(
        model=model,
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )


def extract_final_text(result) -> str:
    """Extract the final AI response while staying simple for classroom use."""
    messages = result.get("messages", [])
    if not messages:
        return str(result)

    content = messages[-1].content

    if isinstance(content, str):
        return content

    # Some model/runtime combinations return structured content blocks.
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            else:
                parts.append(str(block))
        return "\n".join(parts)

    return str(content)


def main():
    agent = build_agent()

    print("=" * 72)
    print("LangChain IT Operations Agent")
    print(f"Model: {MODEL_NAME}")
    print("5 tools: incident, metrics, processes, deployments, service action")
    print("Type 'exit' to stop.")
    print("=" * 72)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Agent: Goodbye.")
            break

        if not user_input:
            continue

        try:
            result = agent.invoke({
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            })

            print("\nAgent:")
            print(extract_final_text(result))

        except Exception as exc:
            print(f"\nERROR: {exc}")


if __name__ == "__main__":
    main()
