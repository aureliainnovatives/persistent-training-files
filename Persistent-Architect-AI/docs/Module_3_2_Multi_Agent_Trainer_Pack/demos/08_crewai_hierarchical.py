"""CrewAI hierarchical demo
pip install -U crewai
export OPENAI_API_KEY="..."
"""
from crewai import Agent,Task,Crew,Process
cloud=Agent(role="Cloud Architect",goal="Assess GCP target architecture",backstory="Migration specialist.")
sec=Agent(role="Security Architect",goal="Assess migration security",backstory="Security specialist.")
cost=Agent(role="FinOps Architect",goal="Assess cloud cost",backstory="FinOps specialist.")
tasks=[
Task(description="Assess GCP architecture for Java checkout service.",expected_output="Architecture findings.",agent=cloud),
Task(description="Assess security/compliance concerns.",expected_output="Security findings.",agent=sec),
Task(description="Assess cost concerns.",expected_output="Cost findings.",agent=cost)]
print(Crew(agents=[cloud,sec,cost],tasks=tasks,process=Process.hierarchical,manager_llm="gpt-4.1-mini",verbose=True).kickoff())
