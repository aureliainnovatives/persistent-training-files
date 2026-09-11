"""LangChain router demo
pip install -U langchain langchain-openai pydantic
export OPENAI_API_KEY="..."
Test: Assess checkout-api for security and cost concerns.
"""
from pydantic import BaseModel,Field
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
m=ChatOpenAI(model="gpt-4.1-mini",temperature=0)
agents={x:create_agent(m,[],system_prompt=f"You are the {x} architecture specialist.") for x in ["security","cost","platform"]}
class Route(BaseModel): specialists:list[str]=Field(description="security, cost and/or platform")
q=input("You: ") or "Assess checkout-api for security and cost concerns."
r=m.with_structured_output(Route).invoke("Select specialists: "+q)
for x in r.specialists:
    if x in agents:
        out=agents[x].invoke({"messages":[{"role":"user","content":q}]})
        print(f"\n{x.upper()}: {out['messages'][-1].content}")
