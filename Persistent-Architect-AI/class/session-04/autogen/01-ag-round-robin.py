import os
from dotenv import load_dotenv

load_dotenv()



OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    model_client = OpenAIChatCompletionClient(
        model=OPENAI_MODEL,
        api_key = OPENAI_API_KEY,
        base_url = OPENAI_BASE_URL
    )

    

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

    stop_when_approved = TextMentionTermination("APPROVE")


    team = RoundRobinGroupChat(
        participants=[analyst, reviewer],
        termination_condition = stop_when_approved,
        max_turns = 6
    )

    task = (
        "INC-1042: checkout-api 5xx rate is 8%, memory is 94%, "
        "and a cache change was deployed 14 minutes before symptoms. "
        "Develop and review a diagnosis."
    )

    result = await team.run(task = task)

    print("\n TEAM CONVERSATION\n" + "-" * 60)

    for message in result.messages:
        print(f"\n[{message.source}]")
        print(getattr(message, "content", ""))


    await model_client.close()



if __name__ == "__main__":
    asyncio.run(main())