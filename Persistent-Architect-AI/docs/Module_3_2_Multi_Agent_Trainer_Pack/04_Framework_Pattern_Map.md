# Framework Pattern Map

## LangChain

-   **Subagents:** supervisor calls specialists as tools; centralized
    control/context isolation.
-   **Router:** classify/decompose → specialists → synthesis.
-   **Handoffs:** state changes active behavior/agent.
-   **Skills:** load specialist context on demand.
-   **Custom workflow:** use LangGraph for bespoke orchestration.

## LangGraph

-   **StateGraph:** typed/shared state connects nodes.
-   **Conditional edges:** deterministic routing from state.
-   **Fan-out/fan-in:** parallel specialists then synthesis.
-   **Cycles:** explicit retry/review/ReAct loops.
-   **Subgraphs:** encapsulated specialist workflows.
-   **Checkpoint/interrupt:** persistence and HITL.

## AutoGen

-   **RoundRobinGroupChat:** fixed turn-taking.
-   **SelectorGroupChat:** model selects next speaker.
-   **Swarm:** handoff-driven control transfer.
-   **Magentic-One:** preset for open-ended tasks.
-   **GraphFlow:** directed agent workflow.

## CrewAI

-   **Crew + Agents + Tasks:** role-based specialists.
-   **Sequential:** ordered task pipeline.
-   **Hierarchical:** manager coordinates/delegates.
-   **Flows:** event/state/router based orchestration.
-   **Hybrid:** Flow controls process; Crew handles open-ended subtask.
