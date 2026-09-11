# =============================================================================
# MODULE 3.2 — MULTI-AGENT WORKFLOWS & ORCHESTRATION
# TRAINER DEMO
# =============================================================================
#
# This file is intentionally written for classroom readability:
#   1. Configuration
#   2. Mock data/tools or agents
#   3. Workflow construction
#   4. Execution
#
# IMPORTANT:
# - These are teaching demos, not production implementations.
# - Set OPENAI_API_KEY in your environment; never hard-code a real key.
# - Framework APIs evolve. Verify installed package versions before delivery.
#

"""
DEMO 8 — CREWAI: HIERARCHICAL CREW

Concept
-------
Manager
  |---------|----------|
  v         v          v
Cloud    Security    FinOps
Architect Architect   Architect

Teaching point
--------------
A manager coordinates specialist work. Use hierarchy only when centralized
decomposition/coordination provides real value.

Install
-------
python -m pip install -U crewai python-dotenv

Run
---
Create a .env file in this folder (see .env.example).
python 08_crewai_hierarchical.py
"""

import os
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# CONFIGURATION FROM .env
# -----------------------------------------------------------------------------
# Default points to OpenAI's standard API endpoint.
# To use another OpenAI-compatible provider later, change OPENAI_BASE_URL and
# OPENAI_API_KEY in .env. No key should be hard-coded in this source file.

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
    )

# CrewAI and its OpenAI-compatible model integration can read these standard
# environment variables. Re-export the values loaded from .env so the framework
# receives the configured endpoint/model.
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_BASE_URL"] = OPENAI_BASE_URL
os.environ["OPENAI_MODEL_NAME"] = OPENAI_MODEL

from crewai import Agent, Crew, Process, Task


# -----------------------------------------------------------------------------
# 1. SPECIALISTS
# -----------------------------------------------------------------------------

cloud_architect = Agent(
    role="Cloud Architect",
    goal="Assess the target GCP architecture for the application.",
    backstory="Senior application and cloud migration architect.",
)

security_architect = Agent(
    role="Security Architect",
    goal="Identify security, identity and compliance concerns.",
    backstory="Senior enterprise security architect.",
)

finops_architect = Agent(
    role="FinOps Architect",
    goal="Identify major cloud cost drivers and optimization opportunities.",
    backstory="Senior cloud economics and FinOps specialist.",
)


# -----------------------------------------------------------------------------
# 2. TASKS
# -----------------------------------------------------------------------------

architecture_task = Task(
    description=(
        "Assess architecture implications of migrating a Java checkout service "
        "to GCP. Consider availability, scalability and target services."
    ),
    expected_output="Concise architecture findings and key risks.",
    agent=cloud_architect,
)

security_task = Task(
    description=(
        "Assess identity, data protection, network and compliance concerns "
        "for the same GCP migration."
    ),
    expected_output="Concise security findings and required controls.",
    agent=security_architect,
)

cost_task = Task(
    description=(
        "Assess likely cost drivers and FinOps concerns for the same migration."
    ),
    expected_output="Concise cost findings and optimization recommendations.",
    agent=finops_architect,
)


# -----------------------------------------------------------------------------
# 3. HIERARCHICAL CREW
# -----------------------------------------------------------------------------
# CrewAI uses a manager model for the hierarchical process.

crew = Crew(
    agents=[
        cloud_architect,
        security_architect,
        finops_architect,
    ],
    tasks=[
        architecture_task,
        security_task,
        cost_task,
    ],
    process=Process.hierarchical,
    manager_llm=OPENAI_MODEL,
    verbose=True,
)


# -----------------------------------------------------------------------------
# 4. RUN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    result = crew.kickoff()

    print("\nFINAL HIERARCHICAL CREW OUTPUT\n" + "-" * 60)
    print(result)
