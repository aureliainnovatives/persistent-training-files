"""CrewAI sequential demo
pip install -U crewai
export OPENAI_API_KEY="..."
"""
from crewai import Agent,Task,Crew,Process
a=Agent(role="Diagnostic Architect",goal="Find likely root cause",backstory="Senior SRE.")
b=Agent(role="Remediation Architect",goal="Recommend safe remediation",backstory="Production architect.")
t1=Task(description="Analyze checkout 5xx=8%, memory=94%, cache change 14 min earlier.",expected_output="Evidence-based diagnosis.",agent=a)
t2=Task(description="Review diagnosis and recommend safe next action.",expected_output="Action, risk, approval need.",agent=b)
print(Crew(agents=[a,b],tasks=[t1,t2],process=Process.sequential,verbose=True).kickoff())
