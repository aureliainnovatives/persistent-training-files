# Module 3.1 --- Agentic AI Foundations

## Trainer Talking Pointers

### 3.1.1 Agent vs Agentic AI; Agent-First Paradigm & Adoption Maturity Model

-   **Agent vs Agentic AI:** An agent is a goal-oriented unit that can
    reason, use tools and act. Agentic AI is the broader architecture
    where autonomy, workflows, state, tools and governance work
    together.
-   **Agent-first paradigm:** Start by asking where adaptive reasoning
    and bounded autonomy create value---not by converting every workflow
    into an agent.
-   **Adoption maturity:** Think progression from model usage → grounded
    assistants → tool-enabled agents → workflow agents → governed
    agentic platforms. More autonomy requires stronger controls.

### 3.1.2 Vector Databases & Retrieval for Agents

-   **Why retrieval matters:** Enterprise agents need current/private
    business knowledge beyond what the model learned during training.
    Retrieval provides this grounding at runtime.
-   **Retrieval architecture:** Think ingestion → chunking →
    embeddings/index → search/filter → reranking → context. Agents may
    retrieve repeatedly while executing a task.
-   **Architect concerns:** Relevance, indexing strategy, latency,
    freshness, metadata filtering, access control and cost matter as
    much as vector similarity.

### 3.1.3 Agent Anatomy: Planner, Executor, Memory, Tools

-   **Planner:** Decides what needs to happen and decomposes the goal
    into steps. Planning may be explicit or dynamically revised.
-   **Executor + tools:** Executes the next step using APIs, databases,
    applications or functions. Tool permissions define what the agent
    can actually do.
-   **Memory/state:** Maintains conversation context, intermediate task
    state or longer-term information. Persistent memory must have
    access, retention and governance rules.

### 3.1.4 Agent Design Patterns --- ReAct, Plan-and-Solve, Reflection

-   **ReAct:** Reason → Act → Observe → repeat. Useful when the next
    step depends on changing tool results, but needs limits to prevent
    loops.\
    **Example:** An IT support agent checks a server alert → queries
    monitoring logs → observes high memory usage → checks running
    processes → identifies the likely offender → recommends or executes
    the next approved action. Each observation determines the next
    action.

-   **Plan-and-Solve:** Generate a plan first and then execute it.
    Better for structured multi-step problems, but plans may require
    revision.\
    **Example:** A cloud migration agent receives: "Assess this
    application for GCP migration." It first plans: inspect architecture
    → identify dependencies → assess database → map target services →
    identify risks → prepare recommendation. It then executes those
    steps.

-   **Reflection:** Agent reviews its own output and tries to improve
    it. Useful for quality improvement, but self-reflection is not
    independent validation.\
    **Example:** A solution-architecture agent creates a proposed
    architecture and then critiques it against security, scalability,
    cost and availability requirements. It detects a single point of
    failure and generates an improved design.

**Easy way to remember:** ReAct = **decide the next step as you go**;
Plan-and-Solve = **plan first, execute second**; Reflection = **produce,
critique, improve**.

### 3.1.5 Developing Agentic Solutions --- Low-Code/No-Code & Coding Frameworks

-   **Low-code/no-code:** Faster for standard enterprise workflows and
    managed integrations; useful where governance and rapid delivery
    matter.
-   **Code-first:** Better when architecture needs custom orchestration,
    testing, complex integrations, portability or deeper runtime
    control.
-   **Selection:** Choose based on extensibility, governance,
    observability, testing, deployment model, skills and lock-in---not
    framework popularity.

### 3.1.6 Guardrails & Budget Controls

-   **Guardrails:** Apply controls around input, retrieval, planning,
    tool execution and output. A guardrail is an architecture layer, not
    simply a system prompt.
-   **Bounded execution:** Restrict tools, permissions, iterations,
    timeouts and high-impact actions. Define when the agent must stop or
    escalate.
-   **Budget controls:** Limit tokens, model usage, tool calls and
    execution time; use caching/model routing where appropriate to
    control production cost.

### 3.1.7 Responsible AI & Governance

-   **Core concerns:** Fairness, accountability, safety, privacy and
    digital trust become more important when AI can take actions rather
    than only generate content.
-   **Governance:** Translate policy into enforceable
    controls---approved models/tools, evaluation gates, audit trails,
    approval thresholds and incident processes.
-   **Accountability:** Always identify who owns the agent's decisions
    and outcomes. Autonomous execution does not remove human/business
    accountability.

### 3.1.8 Data Security & Governance

-   **Follow the data path:** User → agent → retrieval/memory → model →
    tools → output → logs. Sensitive information may cross several
    boundaries in one request.
-   **Access control:** Separate user identity, agent/service identity
    and tool identity. Apply least privilege and verify authorization
    during retrieval and execution.
-   **Enterprise risks:** Watch for permission leakage, over-privileged
    tools, cross-user memory, sensitive logs and restricted data sent to
    external model providers.

### 3.1.9 Hands-on --- Build a Single-Agent Solution

-   **Build:** Create one agent with a clear objective,
    retrieval/knowledge access, tools, bounded state and a defined
    stopping condition.
-   **Observe:** Trace retrieval, reasoning steps, tool calls, latency,
    token usage and failures rather than judging only the final answer.
-   **Review:** Ask what the agent can decide, what it can execute, when
    it must escalate, what could fail and what controls are required
    before production.
