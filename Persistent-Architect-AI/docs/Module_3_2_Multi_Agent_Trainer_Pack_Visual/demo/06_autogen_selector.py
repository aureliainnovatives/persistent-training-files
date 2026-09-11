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
DEMO 6 — AUTOGEN: SELECTOR GROUP CHAT

Pattern
-------
A model selects the next specialist based on the evolving shared conversation.

Install
-------
python -m pip install -U autogen-agentchat "autogen-ext[openai]" python-dotenv

Run
---
Create a .env file in this folder (see .env.example).
python 06_autogen_selector.py
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

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    model_client = OpenAIChatCompletionClient(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
    )

    # Descriptions are important because the selector uses them when deciding
    # which specialist should speak next.
    operations = AssistantAgent(
        name="operations",
        description="Specialist for CPU, memory, latency, logs and runtime health.",
        model_client=model_client,
        system_message="Analyze operational evidence only.",
    )

    deployment = AssistantAgent(
        name="deployment",
        description="Specialist for releases, CI/CD, changes and rollback analysis.",
        model_client=model_client,
        system_message="Analyze deployment/change evidence only.",
    )

    security = AssistantAgent(
        name="security",
        description="Specialist for compromise, access and security implications.",
        model_client=model_client,
        system_message=(
            "Analyze security implications. "
            "When enough evidence has been considered, you may end with TERMINATE."
        ),
    )

    team = SelectorGroupChat(
        participants=[operations, deployment, security],
        model_client=model_client,
        termination_condition=TextMentionTermination("TERMINATE"),
        max_turns=6,
    )

    result = await team.run(
        task=(
            "Investigate checkout-api: HTTP 5xx spike, memory 94%, "
            "and a deployment occurred 14 minutes earlier. "
            "Determine what should be investigated and the likely next action."
        )
    )

    print("\nSELECTED TEAM CONVERSATION\n" + "-" * 60)

    for message in result.messages:
        print(f"\n[{message.source}]")
        print(getattr(message, "content", ""))

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
