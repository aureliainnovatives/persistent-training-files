# 3.2 Trainer Talking Pointers

## 3.2.1 Single Agent → Multi-Agent

-   Single agent owns one goal and chooses tools; multi-agent
    distributes responsibilities across specialists.
-   Split when domains, permissions, context, expertise or
    accountability genuinely differ.
-   **Example:** Incident Supervisor delegates diagnostics, deployment
    analysis and security review.
-   **Remember:** every additional agent adds model calls, context
    transfer, latency, state and failure modes.

## 3.2.2 Agent Specification & Boundaries

-   Define: goal, inputs, outputs, tools, data access, authority, state,
    guardrails, handoff and escalation.
-   Different system prompts alone are not strong architectural
    boundaries.
-   **Example:** Deployment Agent may inspect CI/CD and recommend
    rollback but cannot execute it.

## 3.2.3 Topologies

-   **Hierarchical:** supervisor → specialists; centralized
    accountability.
-   **Peer-to-peer:** specialists hand work directly; flexible but
    ownership is harder.
-   **Swarm:** control moves dynamically; powerful but difficult to
    predict/govern.
-   Ask: **Who owns the final goal when agents disagree?**

## 3.2.4 Decomposition & Delegation

-   **Static:** predefined tasks; predictable and auditable.
-   **Dynamic:** supervisor decomposes at runtime; adaptive but less
    deterministic.
-   Delegation should include outcome, relevant context, constraints and
    expected output.
-   **Example:** GCP migration → architecture + data + security + cost →
    recommendation.

## 3.2.5 Coordination, Messages & Shared State

-   Coordination can use supervisor mediation, direct messages, shared
    state, events or handoffs.
-   Do not copy the whole conversation to every specialist; provide
    minimum useful context.
-   Shared state needs schema and ownership.
-   **Example:** Diagnostics writes `suspected_component`; Deployment
    reads it and checks relevant releases.

## 3.2.6 Negotiation / Conflict

-   Resolve disagreement using supervisor, evaluator, deterministic
    policy or human.
-   Multiple LLM agents agreeing is not independent verification.
-   **Example:** Ops recommends restart; Security blocks action due to
    suspected compromise.

## 3.2.7 Failure Handling

-   Expect timeout, tool failure, malformed output, loops, repeated
    delegation and partial completion.
-   Controls: retries, timeout, recursion/iteration limits, circuit
    breakers, fallback and escalation.
-   Preserve provenance: one hallucination can cascade through
    downstream agents.
-   **Remember:** distributed-system failures + probabilistic AI
    failures.

## 3.2.8 Evaluation

-   Evaluate agent quality **and** workflow quality.
-   Measure task success, routing, handoff quality, tool correctness,
    groundedness, policy compliance, recovery, latency and cost.
-   Inspect traces: who acted, why delegated, what evidence moved, where
    failure occurred.

## 3.2.9 Framework Selection

-   Architecture first: problem → boundaries → topology → state →
    coordination → failures → governance → framework.
-   LangChain: high-level agents/patterns. LangGraph: explicit
    state/graph orchestration. AutoGen: conversational teams. CrewAI:
    role/task crews + flows.
-   Choose by control, state, HITL, observability, deployment and team
    skill.

## 3.2.10 Hands-on

-   Implement one problem with multiple specialists.
-   Compare against the 3.1 single-agent version.
-   Ask: **Did multi-agent improve the system, or only increase
    complexity?**
