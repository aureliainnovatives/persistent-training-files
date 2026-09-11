# =============================================================================
# MODULE 3.2 — MULTI-AGENT WORKFLOWS & ORCHESTRATION
# TRAINER DEMO
# =============================================================================
#
# This file is intentionally written for classroom readability:
#   1. Configuration
#   2. Mock data/tools or agents
#   3. Workflow construction
#   4. Execution
#
# IMPORTANT:
# - These are teaching demos, not production implementations.
# - Set OPENAI_API_KEY in your environment; never hard-code a real key.
# - Framework APIs evolve. Verify installed package versions before delivery.
#

"""
DEMO 1 — LANGCHAIN: SUPERVISOR + SPECIALIST AGENTS

Pattern
-------
User
  |
  v
Incident Supervisor
  |----------------------|
  v                      v
Operations Agent    Deployment Agent
  |                      |
Metrics Tool        Deployment Tool

Install
-------
python -m pip install -U langchain langchain-openai python-dotenv

Run
---
Create a .env file in this folder (see .env.example).
python 01_langchain_supervisor.py

Prompts to try
--------------
1. Investigate INC-1042 using operations and deployment evidence.
2. Check whether checkout-api degradation may be related to a deployment.
3. Only ask the Operations specialist about app-prod-01.
"""

import os
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# CONFIGURATION FROM .env
# -----------------------------------------------------------------------------
# Default points to OpenAI's standard API endpoint.
# To use another OpenAI-compatible provider later, change OPENAI_BASE_URL and
# OPENAI_API_KEY in .env. No key should be hard-coded in this source file.

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
    )

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


# -----------------------------------------------------------------------------
# 1. MODEL
# -----------------------------------------------------------------------------

model = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    temperature=0,
)


# -----------------------------------------------------------------------------
# 2. MOCK TOOLS
# -----------------------------------------------------------------------------

@tool
def get_server_metrics(server_name: str) -> str:
    """Return mock production metrics for a server."""
    if server_name.lower() == "app-prod-01":
        return (
            "Server: app-prod-01\n"
            "CPU: 72%\n"
            "Memory: 94%\n"
            "Health: DEGRADED\n"
            "Observation: checkout-api is the largest memory consumer."
        )

    return f"No mock metrics found for {server_name}."


@tool
def get_recent_deployments(service_name: str) -> str:
    """Return mock recent deployment history for a service."""
    if service_name.lower() == "checkout-api":
        return (
            "Service: checkout-api\n"
            "Deployment: DEP-7781\n"
            "Change: new promotion cache\n"
            "Timing: deployed 14 minutes before incident symptoms started."
        )

    return f"No mock deployment history found for {service_name}."


# -----------------------------------------------------------------------------
# 3. SPECIALIST AGENTS
# -----------------------------------------------------------------------------
# Each specialist receives only the tools needed for its responsibility.
# This demonstrates specialization and context/tool isolation.

operations_agent = create_agent(
    model=model,
    tools=[get_server_metrics],
    system_prompt=(
        "You are the Operations Specialist. "
        "Use server metrics as evidence. "
        "Do not invent infrastructure facts."
    ),
)

deployment_agent = create_agent(
    model=model,
    tools=[get_recent_deployments],
    system_prompt=(
        "You are the Deployment Specialist. "
        "Check whether recent changes correlate with the reported problem. "
        "Do not claim causation without evidence."
    ),
)


# -----------------------------------------------------------------------------
# 4. WRAP SPECIALISTS AS TOOLS
# -----------------------------------------------------------------------------
# The supervisor does not directly call infrastructure tools.
# Instead, it delegates work to specialist agents.

@tool
def ask_operations_specialist(question: str) -> str:
    """Delegate an operations/infrastructure question to the Operations Agent."""
    result = operations_agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return str(result["messages"][-1].content)


@tool
def ask_deployment_specialist(question: str) -> str:
    """Delegate a deployment/change question to the Deployment Agent."""
    result = deployment_agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return str(result["messages"][-1].content)


# -----------------------------------------------------------------------------
# 5. SUPERVISOR AGENT
# -----------------------------------------------------------------------------

supervisor = create_agent(
    model=model,
    tools=[
        ask_operations_specialist,
        ask_deployment_specialist,
    ],
    system_prompt=(
        "You are the Incident Supervisor.\n"
        "Decide which specialist(s) are needed.\n"
        "Delegate rather than inventing evidence.\n"
        "Correlate specialist findings and provide:\n"
        "1. Evidence\n"
        "2. Likely diagnosis\n"
        "3. Recommended next action\n"
        "Clearly distinguish correlation from proven causation."
    ),
)


# -----------------------------------------------------------------------------
# 6. RUN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    default_prompt = (
        "Investigate INC-1042. checkout-api is degraded on app-prod-01. "
        "Use operations and deployment evidence and recommend the next action."
    )

    user_prompt = input("You: ").strip() or default_prompt

    result = supervisor.invoke(
        {"messages": [{"role": "user", "content": user_prompt}]}
    )

    print("\nSUPERVISOR RESPONSE\n" + "-" * 60)
    print(result["messages"][-1].content)
