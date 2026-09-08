from strands import Agent, tool
from model_config import get_model
from tools.infra_tools import (
    get_instance_health, get_cloudwatch_metrics, get_application_logs,
    get_recent_deployments, read_runbook
)

model = get_model()

observability_agent = Agent(
    model=model,
    tools = [get_cloudwatch_metrics, get_application_logs, get_instance_health],
    system_prompt="""You are an observability specialist.
Investigate metrics, logs and compute health. Return evidence only,
plus your technical interpretation."""
)


change_agent = Agent(
    model = model,
    tools = [get_recent_deployments, read_runbook],
    system_prompt="""You are a deployment/change specialist.
Investigate recent changes and relevant runbooks. Return evidence,
change correlation and safe remediation guidance."""
)

@tool
def ask_observability_agent(query: str) -> str:
    """Ask the observability specialist to investigate metrics, logs and host health."""
    return str(observability_agent(query))

@tool
def ask_change_specialist(question: str) -> str:
    """Ask the change specialist to investigate deployments, changes and runbooks."""
    return str(change_agent(question))


coordinator = Agent(
    model = model,
    tools = [ask_observability_agent, ask_change_specialist],
    system_prompt="""You are the incident commander.
Delegate investigation to specialist agents when useful.
Correlate their evidence and provide:
1. Incident summary
2. Evidence
3. Most likely root cause
4. Confidence
5. Safe next action

Never claim that an action was executed unless a tool explicitly says it was."""
)

response = coordinator(
    "Investigate the checkout-api incident that began around 10:42 and produce an RCA."
)


print("\n\n------ Agent Response ------ \n")
print(response)