""""
pip install -r requirements.txt


Pattern
-------
User
  |
  v
Incident Supervisor
  |----------------------|
  v                      v
Operations Agent    Deployment Agent
  |                      |
Metrics Tool        Deployment Tool

"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


model = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key = OPENAI_API_KEY,
    base_url = OPENAI_BASE_URL,
    temperature=0,
)

@tool
def get_server_metrics(server_name: str) -> str:
    """Return mock production metrics for a server."""
    if server_name.lower() == "app-prod-01":
        return (
            "Server: app-prod-01\n"
            "CPU: 72%\n"
            "Memory: 94%\n"
            "Health: DEGRADED\n"
            "Observation: checkout-api is the largest memory consumer."
        )

    return f"No mock metrics found for {server_name}."


@tool
def get_recent_deployments(service_name: str) -> str:
    """Return mock recent deployment history for a service."""
    if service_name.lower() == "checkout-api":
        return (
            "Service: checkout-api\n"
            "Deployment: DEP-7781\n"
            "Change: new promotion cache\n"
            "Timing: deployed 14 minutes before incident symptoms started."
        )

    return f"No mock deployment history found for {service_name}."



operations_agent = create_agent(
    model = model,
    tools = [get_server_metrics],
    system_prompt = (
        "You are the Operations Specialist. "
        "Use server metrics as evidence. "
        "Do not invent infrastructure facts."
    )
)

deployment_agent = create_agent(
    model=model,
    tools=[get_recent_deployments],
    system_prompt=(
        "You are the Deployment Specialist. "
        "Check whether recent changes correlate with the reported problem. "
        "Do not claim causation without evidence."
    ),
)


# SUPERVISOR AGENT
@tool
def ask_operations_specialist(question: str) -> str:
    """Delegate an operations/infrastructure question to the Operations Agent."""
    result = operations_agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return str(result["messages"][-1].content)




@tool
def ask_deployment_specialist(question: str) -> str:
    """Delegate a deployment/change question to the Deployment Agent."""
    result = deployment_agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return str(result["messages"][-1].content)





supervisor = create_agent(
    model=model,
    tools=[
        ask_operations_specialist,
        ask_deployment_specialist,
    ],
    system_prompt=(
        "You are the Incident Supervisor.\n"
        "Decide which specialist(s) are needed.\n"
        "Delegate rather than inventing evidence.\n"
        "Correlate specialist findings and provide:\n"
        "1. Evidence\n"
        "2. Likely diagnosis\n"
        "3. Recommended next action\n"
        "Clearly distinguish correlation from proven causation."
    ),
)

if __name__ == "__main__":

    default_prompt = (
        "Investigate INC-1042. checkout-api is degraded on app-prod-01. "
        "Use operations and deployment evidence and recommend the next action."
    )
    
    user_prompt = input("Enter a prompt: ")

    result = supervisor.invoke(
        {"messages": [{"role": "user", "content": user_prompt}]}
    )

    print("\nSUPERVISOR RESPONSE\n" + "-" * 60)
    print(result["messages"][-1].content) 