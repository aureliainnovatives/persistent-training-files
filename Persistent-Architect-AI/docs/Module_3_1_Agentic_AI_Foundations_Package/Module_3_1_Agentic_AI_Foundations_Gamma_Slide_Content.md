# Module 3.1 — Agentic AI Foundations
**Audience:** Senior Technical & Business Architects  
**Duration:** 4 hours  
**Purpose:** Gamma-ready slide content


## Slide 1 — Agentic AI Foundations
- From model-centric AI to governed systems that can reason, retrieve, decide and act.
- Architect lens: autonomy × control × observability × business accountability.

**Speaker/design note:** Opening: this is not an 'agents 101' session. The objective is to reason about agentic systems as enterprise architecture.

## Slide 2 — Why Agentic Architecture Is an Architecture Problem
- LLMs generate; agents pursue goals.
- Once AI can select tools, change state, call systems and initiate transactions, the design problem expands beyond model quality.
- The architecture must control what the system may know, decide, do, remember, spend and escalate.

**Speaker/design note:** Use a simple progression: answer → recommend → decide → act. Risk rises sharply as we move toward action.

## Slide 3 — Module 3.1 Architecture Map
- 1. Agent vs Agentic AI and maturity
- 2. Retrieval and vector databases
- 3. Agent anatomy and control-loop patterns
- 4. Development approaches, guardrails and budgets
- 5. Responsible AI and governance
- 6. Enterprise data security and governance
- 7. Build and review a single-agent solution

**Speaker/design note:** Show the module as one system: foundation → knowledge → reasoning/control → implementation → governance/security → hands-on.

## Slide 4 — LLM, Assistant, Agent, Agentic System
- LLM: generates an output from context.
- Assistant: conversational interface around one or more model capabilities.
- Agent: goal-directed software entity that can reason about next steps, use tools/state, and execute within boundaries.
- Agentic system: one or more agents plus workflows, tools, memory, policies, evaluation, observability and human governance.

**Speaker/design note:** Stress that 'agent' is not synonymous with chatbot.

## Slide 5 — The Architectural Threshold: From Response to Action
- Generation risk: Is the answer correct?
- Decision risk: Is the selected action appropriate?
- Execution risk: Is the agent authorized to perform it?
- Systemic risk: Can repeated autonomous actions create cascading impact?

**Speaker/design note:** Senior discussion: a hallucinated paragraph is different from a hallucinated payment instruction.

## Slide 6 — What Makes a System Agentic?
- Goal orientation
- Multi-step planning or dynamic next-step selection
- Tool/API interaction
- State and memory
- Environment feedback
- Ability to revise/retry
- Bounded autonomy and stopping conditions

**Speaker/design note:** Use these as architecture signals, not a rigid academic definition.

## Slide 7 — Agent-First Does Not Mean Agent-Everything
- Agent-first asks: where can goal-directed autonomy create value?
- Deterministic workflows remain superior for stable, regulated and fully specified processes.
- Use agents where ambiguity, dynamic context, tool choice or adaptive reasoning matter.
- Keep deterministic controls around irreversible, high-risk and policy-sensitive actions.

**Speaker/design note:** Important executive misconception to eliminate.

## Slide 8 — Enterprise Agent Adoption Maturity
- Level 0 — Model access: prompts and isolated generation.
- Level 1 — Grounded assistants: enterprise retrieval, no autonomous action.
- Level 2 — Tool-enabled agents: bounded tools, explicit user supervision.
- Level 3 — Workflow agents: multi-step execution, persistent state, evaluation and escalation.
- Level 4 — Governed agentic platforms: reusable capabilities, policy, observability, cost controls and cross-team governance.
- Level 5 — Adaptive agentic enterprise: dynamic orchestration with strong automated assurance and human accountability.

**Speaker/design note:** Present as a capability maturity model, not a race to Level 5.

## Slide 9 — Maturity Is Limited by the Weakest Control Plane
- Model capability alone does not create maturity.
- Identity and access
- Data governance
- Tool governance
- Evaluation
- Observability
- Human escalation
- FinOps / token economics
- Operational ownership

**Speaker/design note:** Ask: could a company with a frontier model but no tool authorization be called mature?

## Slide 10 — Architecture Decision: How Much Autonomy?
- Low autonomy: retrieve and recommend.
- Medium autonomy: plan and execute reversible tasks with checkpoints.
- High autonomy: execute consequential actions under policies and exception-based human oversight.
- Choose autonomy based on impact, reversibility, confidence, regulation, observability and recovery capability.

**Speaker/design note:** Introduce autonomy as an explicit NFR/design decision.

## Slide 11 — Enterprise Scenario: Procurement Exception Agent
- Objective: investigate a supplier price-increase request.
- Agent retrieves contract and historical pricing, calls approved market-data tools, identifies deviations, and recommends disposition.
- It may draft a negotiation response.
- It may NOT approve a price increase above threshold without human authorization.

**Speaker/design note:** Use this scenario throughout the module to connect retrieval, tools, security, governance and HITL.

## Slide 12 — Retrieval Is the Agent's Knowledge Interface
- Agents cannot rely on model parameters for enterprise truth.
- Retrieval supplies current, private and task-specific context.
- For agents, retrieval may occur repeatedly during a plan—not only once before generation.
- Retrieval design affects correctness, latency, cost and security.

**Speaker/design note:** Transition to vector databases.

## Slide 13 — Retrieval Architecture: Beyond 'Put It in a Vector DB'
- Ingestion → parsing → chunking → enrichment → embeddings → index.
- Query → intent/context → filtering → candidate retrieval → reranking → context assembly.
- Agent → reasoning/tool loop → additional retrieval when required.
- Authorization must survive every stage.

**Speaker/design note:** Gamma can turn this into an architecture flow.

## Slide 14 — Dense, Sparse and Hybrid Retrieval
- Dense: semantic similarity; strong for meaning and paraphrase.
- Sparse/lexical: exact terms, identifiers, product codes and legal language.
- Hybrid: combines semantic and lexical evidence.
- Reranking: improves final relevance after broad candidate retrieval.
- Architect choice depends on corpus, query types, latency and precision requirements.

**Speaker/design note:** Avoid presenting one retrieval mode as universally best.

## Slide 15 — Vector Store Selection — Architect Criteria
- Index scale and update patterns
- Metadata filtering
- Hybrid search and reranking integration
- Latency/SLA
- Multi-tenancy and isolation
- Authorization integration
- Regional/data-residency requirements
- Observability and operational complexity
- Cost and portability

**Speaker/design note:** Keep vendor-neutral as requested by the source's 'landscape, indexing, performance' framing.

## Slide 16 — Retrieval Failure Modes
- Wrong chunk retrieved
- Correct document but stale version
- Relevant content excluded by chunking
- Unauthorized content retrieved
- Poisoned or manipulated knowledge
- Too much context dilutes reasoning
- Repeated retrieval creates latency/token explosion

**Speaker/design note:** Senior architects should design for failure, not only happy-path relevance.

## Slide 17 — Agent Anatomy: The Enterprise View
- Reasoning/model layer
- Planner / task decomposition
- Executor / control loop
- Tools and connectors
- Working state and memory
- Retrieval/knowledge
- Policy and guardrails
- Evaluator
- Telemetry and audit
- Human escalation

**Speaker/design note:** Show as a reference architecture.

## Slide 18 — Planner vs Executor
- Planner answers: what sequence of work may achieve the goal?
- Executor answers: what should be done now, with which tool and parameters?
- Separating planning from execution can improve control and inspection.
- But excessive planning increases tokens, latency and opportunities for drift.

**Speaker/design note:** Architecture trade-off: explicit plan vs dynamic ReAct loop.

## Slide 19 — Memory Is Not One Thing
- Conversation/context memory: current interaction.
- Working memory/state: intermediate task facts and execution state.
- Long-term memory: retained facts/preferences/history.
- Episodic traces: prior actions/outcomes that may inform future behavior.
- Enterprise rule: every persistent memory needs ownership, retention, access and deletion semantics.

**Speaker/design note:** This is where business architects should challenge 'remember everything'.

## Slide 20 — Pattern 1 — ReAct
- Reason → choose action/tool → observe result → reason again.
- Strength: adaptive and simple for dynamic tool use.
- Risk: loops, unnecessary calls, prompt/tool manipulation and unpredictable cost.
- Controls: tool allow-list, max iterations, timeout, evaluation and stopping rules.

**Speaker/design note:** Use a visual loop.

## Slide 21 — Pattern 2 — Plan-and-Solve
- Create an explicit plan, then execute steps.
- Strength: inspectable decomposition and useful for complex multi-step tasks.
- Risk: initial plan may be wrong or become stale as environment changes.
- Controls: re-planning triggers, checkpoints and step validation.

**Speaker/design note:** Compare with ReAct.

## Slide 22 — Pattern 3 — Reflection
- Agent critiques an intermediate or completed result and attempts improvement.
- Useful where quality benefits from iterative review.
- Risk: self-critique is not independent assurance; it can reinforce the same error.
- Use bounded reflection plus external evaluation for consequential tasks.

**Speaker/design note:** Key senior point: reflection ≠ governance.

## Slide 23 — Deterministic Workflow vs Agentic Control Loop
- Workflow: predefined sequence; predictable transitions.
- Agent: dynamically chooses next action based on goal, context and observations.
- Hybrid architecture is often strongest: deterministic outer workflow + agentic reasoning inside bounded stages.
- The question is not 'workflow or agent?' but 'where should variability be allowed?'

**Speaker/design note:** This is a major architecture decision slide.

## Slide 24 — Low-Code/No-Code vs Code-First
- Low-code: rapid assembly, managed connectors, governance convenience, lower implementation barrier.
- Code-first: deeper control, custom orchestration, testing, portability and complex integration.
- Evaluate: extensibility, governance, deployment model, observability, testing, skills, lock-in and lifecycle ownership.
- Enterprise platforms may intentionally combine both.

**Speaker/design note:** Do not turn this into a product comparison.

## Slide 25 — Guardrails Are a Layered Control System
- Input: classify, validate, detect malicious instructions.
- Context/retrieval: enforce permissions and trusted sources.
- Planning: constrain goals, tools and allowable actions.
- Tool execution: schema validation, authorization, transaction limits.
- Output: policy, safety and sensitive-data checks.
- Post-action: audit, evaluation, anomaly detection and rollback/escalation.

**Speaker/design note:** Guardrails should not be described as a single prompt.

## Slide 26 — Budget Controls Are Architecture Controls
- Token budget per task/session
- Maximum iterations and tool calls
- Model routing by task complexity
- Caching and reuse
- Timeouts and concurrency limits
- Cost-aware retrieval/context limits
- Per-team/application chargeback and quotas

**Speaker/design note:** Tie financial control to runaway loops and platform scale.

## Slide 27 — Responsible AI Changes When AI Can Act
- Fairness: who may be affected by decisions/actions?
- Accountability: who owns the outcome?
- Safety: what harmful action paths exist?
- Privacy: what data is observed, inferred, stored or transmitted?
- Transparency: can the action be explained and reconstructed?
- Digital trust: can users understand the agent's authority and limits?

**Speaker/design note:** Source places Responsible AI in one governance home; retain that framing.

## Slide 28 — Governance: Principle → Enforceable Control
- Policy statement alone is insufficient.
- Convert policy into: approved models/tools, risk tiers, evaluation gates, identity rules, approval thresholds, audit requirements, deployment controls and incident processes.
- Governance must operate across design-time, deployment-time and run-time.

**Speaker/design note:** Architects should make governance executable where possible.

## Slide 29 — The Enterprise Agent Data Path
- User → agent runtime → prompt/context → retrieval → memory → tools/APIs → model provider → output/action → traces/logs.
- Sensitive data can cross multiple boundaries during one task.
- Security review must follow the complete data path, not only the model endpoint.

**Speaker/design note:** Gamma: data-flow diagram.

## Slide 30 — Identity and Authorization: The Agent Is Not the User
- Distinguish user identity, agent/service identity and tool/system identity.
- Propagate authorization intentionally.
- Apply least privilege and scoped credentials.
- Do not let prompt text grant authority.
- Re-check permissions when retrieving data and executing tools.

**Speaker/design note:** This is foundational for enterprise deployment.

## Slide 31 — Security & Governance Failure Scenarios
- Agent retrieves another business unit's confidential data.
- Long-term memory exposes information across users.
- Tool credential permits broader action than the user is entitled to.
- External model receives restricted data.
- Logs retain secrets or regulated information.
- Retrieved content manipulates the agent into unsafe tool use.

**Speaker/design note:** Ask participants to identify which control plane should stop each scenario.

## Slide 32 — Single-Agent Reference Architecture
- Channels/API
- Agent runtime
- Planner/executor
- Retrieval service
- Memory/state
- Tool gateway
- Policy/guardrail layer
- Model gateway
- Evaluation/telemetry
- Identity/secrets
- Human escalation

**Speaker/design note:** Use as the blueprint for the hands-on.

## Slide 33 — Hands-on Challenge
- Build a single agent for an enterprise decision-support workflow.
- Required: retrieval + at least two tools + bounded memory/state + guardrails + budget + audit trace.
- Agent must know when to stop and when to escalate.
- Do not optimize only for demo success; expose failure behavior.

**Speaker/design note:** Suggested scenario can be procurement exception, incident triage, contract review or customer escalation.

## Slide 34 — Agent Specification Before Code
- Business objective and success criteria
- Allowed inputs and data
- Tools and permissions
- State/memory policy
- Decision boundaries
- Stopping conditions
- Escalation/HITL conditions
- Evaluation criteria
- Latency/cost envelope
- Audit requirements

**Speaker/design note:** For senior audience, require architecture contract before implementation.

## Slide 35 — Evaluate the Agent as a System
- Task success
- Groundedness / evidence quality
- Correct tool selection
- Correct tool parameters
- Policy compliance
- Unauthorized-action rate
- Latency
- Token/tool cost
- Recovery from failure
- Escalation quality

**Speaker/design note:** Model accuracy alone is not enough.

## Slide 36 — Architecture Review: Five Questions
- What is the agent authorized to decide?
- What is it authorized to do?
- What enterprise truth does it rely on?
- How do we detect and contain failure?
- Who remains accountable for the outcome?

**Speaker/design note:** Use this as the review rubric after hands-on.

## Slide 37 — 3.1 Takeaway — Agentic AI Is Controlled Delegation
- The enterprise is delegating bounded reasoning and action to software.
- More autonomy requires stronger identity, policy, evaluation, observability and recovery.
- Retrieval, memory and tools make agents useful—and simultaneously expand the attack and failure surface.
- Architecture maturity is the ability to increase useful autonomy without losing control.

**Speaker/design note:** Close the module with the core architectural thesis.