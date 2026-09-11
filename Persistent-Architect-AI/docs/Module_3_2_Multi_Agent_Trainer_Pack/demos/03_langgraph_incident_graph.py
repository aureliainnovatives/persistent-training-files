"""LangGraph StateGraph demo
pip install -U langgraph langchain-openai
export OPENAI_API_KEY="..."
"""
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
class S(TypedDict,total=False): incident:str; metrics:str; deployment:str; diagnosis:str
m=ChatOpenAI(model="gpt-4.1-mini",temperature=0)
def intake(s): return {"incident":"INC-1042 checkout 5xx"}
def diag(s): return {"metrics":"memory=94%, cpu=72%"}
def dep(s): return {"deployment":"cache change 14 min earlier"}
def synth(s): return {"diagnosis":m.invoke(f"Diagnose only from evidence: {s}").content}
g=StateGraph(S)
for n,f in [("intake",intake),("diag",diag),("dep",dep),("synth",synth)]: g.add_node(n,f)
g.add_edge(START,"intake");g.add_edge("intake","diag");g.add_edge("diag","dep");g.add_edge("dep","synth");g.add_edge("synth",END)
print(g.compile().invoke({})["diagnosis"])
