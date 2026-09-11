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
DEMO 4 — LANGGRAPH: CONDITIONAL ROUTING / HUMAN ESCALATION

Flow
----
Assess Risk
   |
   +-- risk < 0.70  -> bounded automatic path
   |
   +-- risk >= 0.70 -> human approval path

Install
-------
python -m pip install -U langgraph

Run
---
python 04_langgraph_conditional_escalation.py

Try
---
Change INPUT_RISK_SCORE from 0.90 to 0.40 and run again.
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
from langgraph.graph import StateGraph, START, END


# -----------------------------------------------------------------------------
# 1. STATE
# -----------------------------------------------------------------------------

class RiskState(TypedDict, total=False):
    risk_score: float
    decision: str


# -----------------------------------------------------------------------------
# 2. NODES
# -----------------------------------------------------------------------------

def assess_risk(state: RiskState) -> dict:
    """In production this could be an evaluator, policy engine or agent."""
    return {"risk_score": state.get("risk_score", 0.90)}


def choose_path(state: RiskState) -> str:
    """Deterministic policy boundary."""
    if state["risk_score"] >= 0.70:
        return "human"
    return "automatic"


def request_human_approval(state: RiskState) -> dict:
    return {
        "decision": (
            "ESCALATE: risk is high. Human approval is required "
            "before any consequential action."
        )
    }


def allow_bounded_action(state: RiskState) -> dict:
    return {
        "decision": (
            "AUTOMATIC PATH: risk is below threshold. "
            "Only the pre-approved bounded action may proceed."
        )
    }


# -----------------------------------------------------------------------------
# 3. GRAPH
# -----------------------------------------------------------------------------

builder = StateGraph(RiskState)

builder.add_node("assess_risk", assess_risk)
builder.add_node("human_approval", request_human_approval)
builder.add_node("bounded_action", allow_bounded_action)

builder.add_edge(START, "assess_risk")

builder.add_conditional_edges(
    "assess_risk",
    choose_path,
    {
        "human": "human_approval",
        "automatic": "bounded_action",
    },
)

builder.add_edge("human_approval", END)
builder.add_edge("bounded_action", END)

workflow = builder.compile()


# -----------------------------------------------------------------------------
# 4. RUN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    INPUT_RISK_SCORE = 0.90

    result = workflow.invoke({"risk_score": INPUT_RISK_SCORE})

    print(f"Risk score: {result['risk_score']}")
    print(f"Decision: {result['decision']}")
