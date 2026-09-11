"""
MODULE 3.4 — LANGCHAIN HUMAN-IN-THE-LOOP DEMO

Purpose
-------
Show a very visible enterprise control boundary:

    safe read tool          -> executes automatically
    restart / rollback      -> pauses for human approval

Current LangChain concepts demonstrated:
- create_agent
- HumanInTheLoopMiddleware
- InMemorySaver checkpointing
- thread_id
- Command(resume=...)
- approve / reject decisions

Recommended prompts are in TRY-ME.md.
"""

import os
import uuid
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


# ---------------------------------------------------------------------------
# 1. ENVIRONMENT
# ---------------------------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY", "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")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
    )


# ---------------------------------------------------------------------------
# 2. MOCK ENTERPRISE TOOLS
# ---------------------------------------------------------------------------
# These tools deliberately do NOT touch a real production environment.
# Their printed output makes tool execution obvious during classroom demos.

SERVICE_STATE = {
    "payment-service": {
        "status": "unhealthy",
        "error_rate": "38%",
        "current_version": "v2.7",
        "previous_version": "v2.6",
    },
    "inventory-service": {
        "status": "healthy",
        "error_rate": "0.8%",
        "current_version": "v4.2",
        "previous_version": "v4.1",
    },
}


@tool
def read_service_health(service_name: str) -> str:
    """Read current health information for a service. This is a safe read-only action."""
    print(f"\n[TOOL EXECUTED] read_service_health({service_name!r})")

    state = SERVICE_STATE.get(service_name)
    if not state:
        return f"No service named {service_name!r} exists in the demo."

    return (
        f"{service_name}: status={state['status']}, "
        f"error_rate={state['error_rate']}, "
        f"current_version={state['current_version']}, "
        f"previous_version={state['previous_version']}"
    )


@tool
def restart_service(service_name: str) -> str:
    """Restart a production service. This is a consequential side-effecting action."""
    print("\n" + "!" * 72)
    print(f"[PROTECTED TOOL EXECUTED] restart_service({service_name!r})")
    print("!" * 72)

    if service_name not in SERVICE_STATE:
        return f"Restart failed: unknown service {service_name!r}."

    SERVICE_STATE[service_name]["status"] = "healthy"
    SERVICE_STATE[service_name]["error_rate"] = "0.5%"
    return f"{service_name} restarted successfully and is now healthy."


@tool
def rollback_deployment(service_name: str, target_version: str) -> str:
    """Rollback a production service to a specified version."""
    print("\n" + "!" * 72)
    print(
        f"[PROTECTED TOOL EXECUTED] "
        f"rollback_deployment({service_name!r}, {target_version!r})"
    )
    print("!" * 72)

    if service_name not in SERVICE_STATE:
        return f"Rollback failed: unknown service {service_name!r}."

    SERVICE_STATE[service_name]["current_version"] = target_version
    SERVICE_STATE[service_name]["status"] = "healthy"
    SERVICE_STATE[service_name]["error_rate"] = "0.3%"

    return (
        f"{service_name} rolled back to {target_version}. "
        "Service health is now healthy."
    )


# ---------------------------------------------------------------------------
# 3. MODEL
# ---------------------------------------------------------------------------

model = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0,
)


# ---------------------------------------------------------------------------
# 4. HITL POLICY
# ---------------------------------------------------------------------------
#
# read_service_health:
#     Safe read-only tool -> NO approval.
#
# restart_service / rollback_deployment:
#     Side-effecting production actions -> HUMAN APPROVAL REQUIRED.
#
# The important teaching point:
# We are NOT relying only on a prompt saying "please ask before restarting".
# Middleware intercepts protected tool calls at the execution boundary.

hitl = HumanInTheLoopMiddleware(
    interrupt_on={
        "read_service_health": False,
        "restart_service": {
            "allowed_decisions": ["approve", "reject"],
            "description": "Production service restart requires operator approval.",
        },
        "rollback_deployment": {
            "allowed_decisions": ["approve", "reject"],
            "description": "Production rollback requires operator approval.",
        },
    }
)


# ---------------------------------------------------------------------------
# 5. CHECKPOINTER
# ---------------------------------------------------------------------------
#
# HITL needs state to survive while execution is paused.
# InMemorySaver is intentionally used only for this classroom demo.
# Production systems should use durable persistence appropriate to the platform.

checkpointer = InMemorySaver()


# ---------------------------------------------------------------------------
# 6. CREATE THE LANGCHAIN AGENT
# ---------------------------------------------------------------------------

agent = create_agent(
    model=model,
    tools=[
        read_service_health,
        restart_service,
        rollback_deployment,
    ],
    middleware=[hitl],
    checkpointer=checkpointer,
    system_prompt=(
        "You are a production operations assistant. "
        "Use tools when useful. "
        "Read service health before recommending consequential action. "
        "Never claim a restart or rollback happened unless the corresponding "
        "tool actually executed. "
        "Explain the evidence behind operational recommendations."
    ),
)


# ---------------------------------------------------------------------------
# 7. SMALL OUTPUT HELPERS
# ---------------------------------------------------------------------------

def print_messages(result):
    """Print the latest agent-visible messages in a classroom-friendly form."""
    messages = result.get("messages", []) if isinstance(result, dict) else []

    if not messages:
        return

    print("\n--- AGENT OUTPUT -----------------------------------------------")
    for message in messages[-4:]:
        content = getattr(message, "content", None)
        if content:
            role = type(message).__name__
            print(f"\n[{role}]\n{content}")


def get_interrupts(result):
    """Return interrupt objects from the standard dictionary invoke result."""
    if not isinstance(result, dict):
        return []
    return result.get("__interrupt__", []) or []


def show_interrupt(interrupt_obj):
    """Display the pending HITL request without assuming a custom UI."""
    value = getattr(interrupt_obj, "value", interrupt_obj)

    print("\n" + "=" * 72)
    print("HUMAN APPROVAL REQUIRED")
    print("=" * 72)
    print(value)
    print("=" * 72)


# ---------------------------------------------------------------------------
# 8. RUN + HUMAN APPROVAL LOOP
# ---------------------------------------------------------------------------

def run_demo(user_prompt: str):
    # A stable thread ID identifies this paused/resumable execution.
    config = {
        "configurable": {
            "thread_id": f"module-3-4-{uuid.uuid4()}"
        }
    }

    # Initial execution.
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        },
        config=config,
    )

    # An agent may hit more than one approval boundary.
    while True:
        interrupts = get_interrupts(result)

        if not interrupts:
            print_messages(result)
            return result

        # This classroom demo handles the first pending interrupt.
        # The configured tools normally generate one protected call at a time.
        show_interrupt(interrupts[0])

        decision = input("\nApprove this action? [y/n]: ").strip().lower()

        if decision in {"y", "yes"}:
            resume_payload = {
                "decisions": [
                    {"type": "approve"}
                ]
            }
        else:
            reason = input(
                "Optional rejection reason "
                "(press Enter for default): "
            ).strip()

            resume_payload = {
                "decisions": [
                    {
                        "type": "reject",
                        "message": reason or (
                            "Operator rejected this production action. "
                            "Do not execute it; explain alternatives."
                        ),
                    }
                ]
            }

        # Resume the SAME thread from the checkpoint.
        result = agent.invoke(
            Command(resume=resume_payload),
            config=config,
        )


# ---------------------------------------------------------------------------
# 9. CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(
        """
================================================================
 MODULE 3.4 — LANGCHAIN HITL DEMO
================================================================

Safe:
  read_service_health -> automatic

Protected:
  restart_service     -> human approval
  rollback_deployment -> human approval

Try:
  Check payment-service and restart it if appropriate.

See TRY-ME.md for additional prompts.
================================================================
"""
    )

    prompt = input("Incident / request: ").strip()

    if not prompt:
        prompt = (
            "Check payment-service. If it is unhealthy, "
            "restart it if that is the appropriate recovery action."
        )

    run_demo(prompt)
