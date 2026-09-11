"""LangGraph conditional routing demo
pip install -U langgraph
Change risk_score between 0.4 and 0.9.
"""
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
class S(TypedDict,total=False): risk_score:float; decision:str
def assess(s): return {"risk_score":s.get("risk_score",.9)}
def route(s): return "human" if s["risk_score"]>=.7 else "auto"
def human(s): return {"decision":"HUMAN APPROVAL REQUIRED"}
def auto(s): return {"decision":"BOUNDED AUTO-REMEDIATION"}
g=StateGraph(S);g.add_node("assess",assess);g.add_node("human",human);g.add_node("auto",auto)
g.add_edge(START,"assess");g.add_conditional_edges("assess",route,{"human":"human","auto":"auto"});g.add_edge("human",END);g.add_edge("auto",END)
print(g.compile().invoke({"risk_score":.9}))
