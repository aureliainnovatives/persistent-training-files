# Framework Comparison

  -------------------------------------------------------------------------------
  Framework         Mental model      Strong fit        Multi-agent patterns
  ----------------- ----------------- ----------------- -------------------------
  **LangChain**     High-level agent  Tool agents and   Subagents, router,
                    framework         rapid composition handoffs, skills

  **LangGraph**     Stateful          Explicit          StateGraph, conditional
                    graph/runtime     orchestration,    routing, fan-out, cycles,
                                      persistence, HITL subgraphs

  **AutoGen         Conversational    Dynamic           RoundRobin,
  AgentChat**       agents/teams      collaboration     SelectorGroupChat, Swarm,
                                                        Magentic-One, GraphFlow

  **CrewAI**        Role/task crews + Business-role     Sequential/hierarchical
                    flows             teams and hybrid  crews, delegation,
                                      automation        event-driven Flows
  -------------------------------------------------------------------------------

## LangChain vs LangGraph

-   LangChain is the higher-level agent/application layer.
-   Current LangChain `create_agent` uses a LangGraph-based runtime
    underneath.
-   Use LangGraph directly when state transitions, branching,
    parallelism, persistence or custom orchestration must be explicit.

## Selection questions

1.  Deterministic or dynamically selected flow?
2.  Persistent state?
3.  Shared or isolated context?
4.  Parallel fan-out?
5.  HITL pause/resume?
6.  Traceability?
7.  Failure/retry model?
8.  Token/model-call amplification?
9.  Role/task abstraction or lower-level runtime?
10. Can orchestration be tested independently?

**Takeaway:** Don't ask "Which framework is best?" Ask "Which execution
model matches the architecture?"
