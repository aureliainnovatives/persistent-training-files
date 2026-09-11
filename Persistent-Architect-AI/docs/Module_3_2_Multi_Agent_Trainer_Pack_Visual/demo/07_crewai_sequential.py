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
DEMO 7 — CREWAI: SEQUENTIAL CREW

Flow
----
Diagnostic Architect -> Remediation Architect

Teaching point
--------------
The workflow order is predefined. Agent specialization exists inside a
deterministic task pipeline.

Install
-------
python -m pip install -U crewai python-dotenv

Run
---
Create a .env file in this folder (see .env.example).
python 07_crewai_sequential.py
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
# 1. AGENTS
# -----------------------------------------------------------------------------

diagnostic_architect = Agent(
    role="Incident Diagnostic Architect",
    goal="Identify the most likely root cause from the supplied evidence.",
    backstory=(
        "You are a senior production reliability architect. "
        "You distinguish evidence, hypothesis and missing information."
    ),
    verbose=True,
)

remediation_architect = Agent(
    role="Remediation Architect",
    goal="Recommend the safest next action based on the diagnosis.",
    backstory=(
        "You are a senior SRE responsible for safe production changes "
        "and appropriate human approvals."
    ),
    verbose=True,
)


# -----------------------------------------------------------------------------
# 2. TASKS
# -----------------------------------------------------------------------------

diagnosis_task = Task(
    description=(
        "Analyze this incident:\n"
        "- checkout-api HTTP 5xx rate = 8%\n"
        "- app-prod-01 memory = 94%\n"
        "- promotion-cache change deployed 14 minutes before symptoms\n"
        "Do not claim causation unless evidence supports it."
    ),
    expected_output=(
        "Evidence-based diagnosis containing likely hypothesis, "
        "supporting evidence, confidence and missing evidence."
    ),
    agent=diagnostic_architect,
)

remediation_task = Task(
    description=(
        "Review the diagnosis produced by the previous task. "
        "Recommend the safest next action. "
        "State whether human/change approval is required."
    ),
    expected_output=(
        "Recommended action, operational risk, approval requirement "
        "and verification step."
    ),
    agent=remediation_architect,
)


# -----------------------------------------------------------------------------
# 3. CREW
# -----------------------------------------------------------------------------

crew = Crew(
    agents=[
        diagnostic_architect,
        remediation_architect,
    ],
    tasks=[
        diagnosis_task,
        remediation_task,
    ],
    process=Process.sequential,
    verbose=True,
)


# -----------------------------------------------------------------------------
# 4. RUN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    result = crew.kickoff()

    print("\nFINAL CREW OUTPUT\n" + "-" * 60)
    print(result)
