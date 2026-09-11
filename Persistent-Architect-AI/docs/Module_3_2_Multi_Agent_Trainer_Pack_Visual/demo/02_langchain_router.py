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
DEMO 2 — LANGCHAIN: ROUTER + SPECIALISTS

Pattern
-------
Request -> Router -> Security / Cost / Platform specialist(s)

Teaching point
--------------
A router does not require agents to debate. It selects the right expertise
for the request, then specialists work independently.

Install
-------
python -m pip install -U langchain langchain-openai pydantic python-dotenv

Run
---
Create a .env file in this folder (see .env.example).
python 02_langchain_router.py

Prompts
-------
1. Assess checkout-api for security and cloud cost concerns.
2. Review checkout-api only for reliability concerns.
3. Assess security, platform reliability and cost.
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

from pydantic import BaseModel, Field
from langchain.agents import create_agent
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
# 2. SPECIALIST AGENTS
# -----------------------------------------------------------------------------

security_agent = create_agent(
    model,
    [],
    system_prompt=(
        "You are a Security Architect. "
        "Identify authentication, authorization, data and runtime risks."
    ),
)

cost_agent = create_agent(
    model,
    [],
    system_prompt=(
        "You are a Cloud FinOps Architect. "
        "Identify major cost drivers and optimization opportunities."
    ),
)

platform_agent = create_agent(
    model,
    [],
    system_prompt=(
        "You are a Platform Architect. "
        "Assess reliability, scalability and operational concerns."
    ),
)

specialists = {
    "security": security_agent,
    "cost": cost_agent,
    "platform": platform_agent,
}


# -----------------------------------------------------------------------------
# 3. STRUCTURED ROUTING DECISION
# -----------------------------------------------------------------------------
# Instead of asking the LLM for free-form text, force it to return a schema.
# This makes routing easier to inspect and validate.

class RoutingDecision(BaseModel):
    specialists: list[str] = Field(
        description=(
            "Specialists required for the request. "
            "Allowed values: security, cost, platform."
        )
    )


router = model.with_structured_output(RoutingDecision)


# -----------------------------------------------------------------------------
# 4. RUN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    default_prompt = "Assess checkout-api for security and cloud cost concerns."
    user_prompt = input("You: ").strip() or default_prompt

    decision = router.invoke(
        "Select only the specialists genuinely required for this request:\n"
        + user_prompt
    )

    print("\nROUTER DECISION")
    print(decision.specialists)

    print("\nSPECIALIST RESPONSES\n" + "-" * 60)

    for specialist_name in decision.specialists:
        agent = specialists.get(specialist_name)

        if agent is None:
            print(f"\nSkipping unknown specialist: {specialist_name}")
            continue

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_prompt}]}
        )

        print(f"\n[{specialist_name.upper()}]")
        print(result["messages"][-1].content)
