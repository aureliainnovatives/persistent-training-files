"""LangChain supervisor demo
pip install -U langchain langchain-openai
export OPENAI_API_KEY="..."
Test: Investigate INC-1042 using operations and deployment specialists.
"""
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
m=ChatOpenAI(model="gpt-4.1-mini",temperature=0)
@tool
def metrics(server:str)->str:
    """Mock server metrics."""; return "app-prod-01 memory=94% cpu=72%"
@tool
def deployments(service:str)->str:
    """Mock deployments."""; return "checkout-api DEP-7781 cache change 14 min before incident"
ops=create_agent(m,[metrics],system_prompt="Operations specialist. Use evidence.")
dep=create_agent(m,[deployments],system_prompt="Deployment specialist. Use evidence.")
@tool
def ask_ops(q:str)->str:
    """Ask operations specialist."""; return str(ops.invoke({"messages":[{"role":"user","content":q}]})["messages"][-1].content)
@tool
def ask_deployment(q:str)->str:
    """Ask deployment specialist."""; return str(dep.invoke({"messages":[{"role":"user","content":q}]})["messages"][-1].content)
boss=create_agent(m,[ask_ops,ask_deployment],system_prompt="Incident supervisor. Delegate then synthesize.")
q=input("You: ") or "Investigate INC-1042 using operations and deployment specialists."
print(boss.invoke({"messages":[{"role":"user","content":q}]})["messages"][-1].content)
