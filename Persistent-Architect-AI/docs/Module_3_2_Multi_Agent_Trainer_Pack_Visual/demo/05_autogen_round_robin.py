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
DEMO 5 — AUTOGEN: ROUND-ROBIN TEAM

Pattern
-------
Analyst -> Reviewer -> Analyst -> Reviewer ... until APPROVE

Teaching point
--------------
The speaking order is predictable, but the content is conversational.

Install
-------
python -m pip install -U autogen-agentchat "autogen-ext[openai]" python-dotenv

Run
---
Create a .env file in this folder (see .env.example).
python 05_autogen_round_robin.py
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
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    # -------------------------------------------------------------------------
    # 1. MODEL CLIENT
    # -------------------------------------------------------------------------
    model_client = OpenAIChatCompletionClient(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
    )

    # -------------------------------------------------------------------------
    # 2. TEAM MEMBERS
    # -------------------------------------------------------------------------
    analyst = AssistantAgent(
        name="analyst",
        model_client=model_client,
        system_message=(
            "You are the incident analyst. "
            "Develop an evidence-based diagnosis and state uncertainty."
        ),
    )

    reviewer = AssistantAgent(
        name="reviewer",
        model_client=model_client,
        system_message=(
            "You are the senior reviewer. "
            "Challenge unsupported conclusions. "
            "When the analysis is sufficient, finish your response with APPROVE."
        ),
    )

    # -------------------------------------------------------------------------
    # 3. TERMINATION
    # -------------------------------------------------------------------------
    stop_when_approved = TextMentionTermination("APPROVE")

    # -------------------------------------------------------------------------
    # 4. TEAM
    # -------------------------------------------------------------------------
    team = RoundRobinGroupChat(
        participants=[analyst, reviewer],
        termination_condition=stop_when_approved,
        max_turns=6,
    )

    # -------------------------------------------------------------------------
    # 5. RUN
    # -------------------------------------------------------------------------
    task = (
        "INC-1042: checkout-api 5xx rate is 8%, memory is 94%, "
        "and a cache change was deployed 14 minutes before symptoms. "
        "Develop and review a diagnosis."
    )

    result = await team.run(task=task)

    print("\nTEAM CONVERSATION\n" + "-" * 60)

    for message in result.messages:
        print(f"\n[{message.source}]")
        print(getattr(message, "content", ""))

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
