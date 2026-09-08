from strands import Agent
from model_config import get_model
from tools.infra_tools import get_instance_health, get_cloudwatch_metrics

agent = Agent(
    model = get_model(),
    tools = [get_instance_health, get_cloudwatch_metrics],
    system_prompt = """You are an infrastructure health assistant.
Use tools rather than inventing operational facts.
Explain which evidence you used.
    """
)


response = agent(
    "Check checkout-api, is the infrastructure unhealthy or overloaded?"
)

print("\n\n------ Agent Response ------ \n")
print(response)
