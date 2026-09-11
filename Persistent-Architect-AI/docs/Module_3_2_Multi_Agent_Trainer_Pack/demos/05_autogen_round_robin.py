"""AutoGen RoundRobin demo
pip install -U autogen-agentchat "autogen-ext[openai]"
export OPENAI_API_KEY="..."
"""
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
async def main():
    m=OpenAIChatCompletionClient(model="gpt-4.1-mini")
    a=AssistantAgent("analyst",model_client=m,system_message="Diagnose incident evidence.")
    r=AssistantAgent("reviewer",model_client=m,system_message="Critique; end with APPROVE when adequate.")
    team=RoundRobinGroupChat([a,r],termination_condition=TextMentionTermination("APPROVE"),max_turns=6)
    x=await team.run(task="5xx=8%, memory=94%, cache deployed 14 min earlier. Diagnose.")
    for msg in x.messages: print(f"\n[{msg.source}] {getattr(msg,'content','')}")
    await m.close()
asyncio.run(main())
