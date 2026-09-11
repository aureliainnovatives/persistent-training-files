import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END


class IncidentState(TypedDict, total=False):
    incident: str
    metrics: str
    deployment_evidence: str
    diagnosis: str

model = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    temperature=0,
)

def intake_incident(state: IncidentState) -> dict:
    """Load mock incident information."""
    return {
        "incident": (
            "INC-1042: checkout-api has an 8% HTTP 5xx rate. "
            "Affected server: app-prod-01."
        )
    }

def collect_diagnostics(state: IncidentState) -> dict:
    """Collect mock infrastructure evidence."""
    return {
        "metrics": (
            "app-prod-01 memory=94%, CPU=72%. "
            "checkout-api is the largest memory consumer."
        )
    }


def inspect_deployment(state: IncidentState) -> dict:
    """Collect mock change/deployment evidence."""
    return {
        "deployment_evidence": (
            "DEP-7781 introduced a promotion cache "
            "14 minutes before incident symptoms began."
        )
    }

def synthesize_diagnosis(state: IncidentState) -> dict:
    """Use the LLM only to reason over already collected evidence."""

    prompt = f"""
        You are an incident architect.

        Use ONLY the evidence below.
        Do not invent missing facts.

        Incident:
        {state.get("incident")}

        Metrics:
        {state.get("metrics")}

        Deployment:
        {state.get("deployment_evidence")}

        Return:
        1. Most likely hypothesis
        2. Evidence
        3. What remains unproven
        4. Recommended next step
        """
    
    response = model.invoke(prompt)
    return {"diagnosis": response.content}



builder = StateGraph(IncidentState)

builder.add_node("intake", intake_incident)
builder.add_node("diagnostics", collect_diagnostics)
builder.add_node("deployment", inspect_deployment)
builder.add_node("synthesis", synthesize_diagnosis)

builder.add_edge(START, "intake")
builder.add_edge("intake", "diagnostics")
builder.add_edge("diagnostics", "deployment")
builder.add_edge("deployment", "synthesis")
builder.add_edge("synthesis", END)

workflow = builder.compile()




if __name__ == "__main__":
    final_state = workflow.invoke({})

    print("\nFINAL DIAGNOSIS\n" + "-" * 60)
    print(final_state["diagnosis"])