# Demo Runbook

  -----------------------------------------------------------------------
  Framework         Demo 1            Demo 2            Teaching point
  ----------------- ----------------- ----------------- -----------------
  LangChain         Supervisor +      Router +          High-level
                    specialist agents specialists       composition

  LangGraph         Incident          Conditional       Explicit
                    StateGraph        escalation        state/control

  AutoGen           Round-robin       Selector team     Conversational
                    review team                         team coordination

  CrewAI            Sequential crew   Hierarchical crew Role/task
                                                        collaboration
  -----------------------------------------------------------------------

## Prompts / talking questions

-   Who owns the goal and state?
-   Who decides the next agent?
-   Is context shared or isolated?
-   What remains deterministic?
-   What terminates the workflow?
-   Where would HITL fit?
-   How could hallucination cascade?
-   What extra model calls/cost did multi-agent introduce?
