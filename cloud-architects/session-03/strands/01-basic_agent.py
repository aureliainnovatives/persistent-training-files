""""
Basic Agent
pip install -r requirements.txt
"""

from strands import Agent
from model_config import get_model

simple_agent = Agent(
    model = get_model(),
    system_prompt = "You are a AWS Infrastructure expert. You are helpful, polite, honest, and accurate.",
)


response = simple_agent(
        "Explain why an application might show high latency even when EC2 CPU is normal."
)

print("\n\n------ Agent Response ------ \n")
print(response)
