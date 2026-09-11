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
DEMO 3 — LANGGRAPH: EXPLICIT STATE GRAPH

Flow
----
START -> Intake -> Diagnostics -> Deployment Analysis -> Synthesis -> END

Teaching point
--------------
LangGraph makes state and transitions explicit. The outer workflow can remain
deterministic while an LLM is used only where reasoning is valuable.

Install
-------
python -m pip install -U langgraph langchain-openai python-dotenv

Run
---
Create a .env file in this folder (see .env.example).
python 03_langgraph_incident_graph.py
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

from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END


# -----------------------------------------------------------------------------
# 1. DEFINE WORKFLOW STATE
# -----------------------------------------------------------------------------

class IncidentState(TypedDict, total=False):
    incident: str
    metrics: str
    deployment_evidence: str
    diagnosis: str


# -----------------------------------------------------------------------------
# 2. MODEL
# -----------------------------------------------------------------------------

model = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    temperature=0,
)


# -----------------------------------------------------------------------------
# 3. GRAPH NODES
# -----------------------------------------------------------------------------
# In a real implementation these nodes could call APIs, databases or agents.

def intake_incident(state: IncidentState) -> dict:
    """Load mock incident information."""
    return {
        "incident": (
            "INC-1042: checkout-api has an 8% HTTP 5xx rate. "
            "Affected server: app-prod-01."
        )
    }


def collect_diagnostics(state: IncidentState) -> dict:
    """Collect mock infrastructure evidence."""
    return {
        "metrics": (
            "app-prod-01 memory=94%, CPU=72%. "
            "checkout-api is the largest memory consumer."
        )
    }


def inspect_deployment(state: IncidentState) -> dict:
    """Collect mock change/deployment evidence."""
    return {
        "deployment_evidence": (
            "DEP-7781 introduced a promotion cache "
            "14 minutes before incident symptoms began."
        )
    }


def synthesize_diagnosis(state: IncidentState) -> dict:
    """Use the LLM only to reason over already collected evidence."""
    prompt = f"""
You are an incident architect.

Use ONLY the evidence below.
Do not invent missing facts.

Incident:
{state.get("incident")}

Metrics:
{state.get("metrics")}

Deployment:
{state.get("deployment_evidence")}

Return:
1. Most likely hypothesis
2. Evidence
3. What remains unproven
4. Recommended next step
"""

    response = model.invoke(prompt)
    return {"diagnosis": response.content}


# -----------------------------------------------------------------------------
# 4. BUILD THE GRAPH
# -----------------------------------------------------------------------------

builder = StateGraph(IncidentState)

builder.add_node("intake", intake_incident)
builder.add_node("diagnostics", collect_diagnostics)
builder.add_node("deployment", inspect_deployment)
builder.add_node("synthesis", synthesize_diagnosis)

builder.add_edge(START, "intake")
builder.add_edge("intake", "diagnostics")
builder.add_edge("diagnostics", "deployment")
builder.add_edge("deployment", "synthesis")
builder.add_edge("synthesis", END)

workflow = builder.compile()


# -----------------------------------------------------------------------------
# 5. RUN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    final_state = workflow.invoke({})

    print("\nFINAL DIAGNOSIS\n" + "-" * 60)
    print(final_state["diagnosis"])
