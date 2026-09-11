"""AutoGen SelectorGroupChat demo
pip install -U autogen-agentchat "autogen-ext[openai]"
export OPENAI_API_KEY="..."
"""
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
async def main():
    m=OpenAIChatCompletionClient(model="gpt-4.1-mini")
    ops=AssistantAgent("operations",model_client=m,description="Metrics specialist",system_message="Analyze operations.")
    sec=AssistantAgent("security",model_client=m,description="Security specialist",system_message="Analyze security.")
    dep=AssistantAgent("deployment",model_client=m,description="Change specialist",system_message="Analyze deployment; say TERMINATE when sufficient.")
    team=SelectorGroupChat([ops,sec,dep],model_client=m,termination_condition=TextMentionTermination("TERMINATE"),max_turns=6)
    x=await team.run(task="Investigate checkout 5xx, memory 94%, deployment 14 min earlier.")
    for msg in x.messages: print(f"\n[{msg.source}] {getattr(msg,'content','')}")
    await m.close()
asyncio.run(main())
