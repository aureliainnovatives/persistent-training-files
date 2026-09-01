# Module 3.2 — Multi-Agent Workflows & Orchestration
## Trainer Visual Notes

> These diagrams are deliberately simple and presentation-friendly. They use Mermaid where a relational diagram helps, plus compact Markdown tables for comparison.

---

## 1. Single Agent → Multi-Agent

### Single Agent
One reasoning authority owns the complete goal and chooses among tools.

```mermaid
flowchart LR
    U[User / Goal] --> A[Single Agent]
    A --> T1[Incident Tool]
    A --> T2[Metrics Tool]
    A --> T3[Deployment Tool]
    A --> T4[Security Tool]
    T1 --> A
    T2 --> A
    T3 --> A
    T4 --> A
    A --> U
```

### Multi-Agent
Responsibility is decomposed across specialists.

```mermaid
flowchart TB
    U[Business Goal] --> S[Supervisor / Orchestrator]
    S --> O[Operations Agent]
    S --> D[Deployment Agent]
    S --> SEC[Security Agent]
    O --> OT[Metrics / Logs]
    D --> DT[CI/CD / Changes]
    SEC --> ST[Security Events]
    O --> S
    D --> S
    SEC --> S
    S --> R[Final Diagnosis / Decision]
```

**Trainer point:** Multi-agent adds specialization, but also coordination, latency, state, cost and new failure modes.

---

## 2. Agent Specification — Define the Contract

```mermaid
flowchart LR
    G[Goal] --> A[Agent]
    I[Inputs] --> A
    A --> O[Expected Output]
    A --> T[Allowed Tools]
    A --> DA[Data Access]
    A --> AU[Authority]
    A --> M[Memory / State]
    A --> GR[Guardrails]
    A --> H[Handoff]
    A --> E[Escalation]
```

**Example — Deployment Agent**
- Goal: correlate deployments with incident symptoms.
- Can: read CI/CD history, compare timestamps, recommend rollback.
- Cannot: execute production rollback.
- Handoff: return evidence + confidence + recommendation to Incident Supervisor.

---

# 3. Topology Visuals

## 3.1 Hierarchical / Supervisor

```mermaid
flowchart TB
    S[Supervisor] --> A[Agent A]
    S --> B[Agent B]
    S --> C[Agent C]
    A --> S
    B --> S
    C --> S
```

**Use when:** central accountability and controlled delegation matter.

---

## 3.2 Router + Specialists

```mermaid
flowchart LR
    Q[Request] --> R{Router}
    R -->|Security| S[Security Agent]
    R -->|Cost| C[FinOps Agent]
    R -->|Platform| P[Platform Agent]
    S --> SYN[Synthesizer]
    C --> SYN
    P --> SYN
```

**Use when:** domains are clear but the required specialist varies by request.

---

## 3.3 Sequential Pipeline

```mermaid
flowchart LR
    A[Research Agent] --> B[Analysis Agent] --> C[Review Agent] --> D[Final Output]
```

**Use when:** stages are ordered and each stage consumes the previous output.

**Risk:** an early error can propagate downstream.

---

## 3.4 Handoff

```mermaid
flowchart LR
    U[User] --> A[Agent A]
    A -->|Transfer control + context| B[Agent B]
    B -->|Transfer if required| C[Agent C]
```

**Use when:** ownership changes as the interaction enters a different stage or domain.

---

## 3.5 Peer-to-Peer

```mermaid
flowchart LR
    A[Agent A] <--> B[Agent B]
    B <--> C[Agent C]
    C <--> A
```

**Use when:** specialists need direct collaboration without a permanent central supervisor.

**Risk:** ownership, loops and global-state consistency.

---

## 3.6 Swarm / Dynamic Handoffs

```mermaid
flowchart TB
    A[Agent A] -->|handoff| B[Agent B]
    B -->|handoff| C[Agent C]
    C -->|handoff| D[Agent D]
    D -->|possible handoff| A
    B -->|alternate route| D
```

**Use when:** the appropriate next specialist emerges dynamically.

**Trainer warning:** flexibility rises, but predictability and governance fall.

---

## 3.7 Graph / State Machine

```mermaid
flowchart LR
    START([Start]) --> IN[Intake]
    IN --> DIAG[Diagnostics]
    DIAG --> RISK{Risk >= threshold?}
    RISK -->|Yes| H[Human Approval]
    RISK -->|No| AUTO[Bounded Auto Action]
    H --> END([End])
    AUTO --> END
```

**Use when:** deterministic policy boundaries must surround agentic reasoning.

---

# 4. Static vs Dynamic Decomposition

```mermaid
flowchart TB
    G[Migration Assessment]

    G --> STATIC[Static Decomposition]
    STATIC --> SA[Architecture]
    STATIC --> SD[Data]
    STATIC --> SS[Security]
    STATIC --> SC[Cost]

    G --> DYNAMIC[Dynamic Decomposition]
    DYNAMIC --> SUP[Supervisor decides required work]
    SUP -->|This workload needs it| GPU[GPU Assessment]
    SUP -->|Sensitive data exists| PRIV[Privacy Review]
    SUP -->|Always relevant| ARCH[Architecture Review]
```

| Static | Dynamic |
|---|---|
| Tasks known in advance | Tasks selected at runtime |
| Predictable | Adaptive |
| Easier to test/audit | Handles ambiguity better |
| Less autonomous | More model-dependent |

---

# 5. Coordination & Shared State

```mermaid
flowchart TB
    ST[(Shared State)]
    A[Diagnostic Agent] -->|suspected_component| ST
    B[Deployment Agent] -->|deployment_correlation| ST
    C[Security Agent] -->|security_risk| ST
    ST --> S[Supervisor]
    S --> R[Decision]
```

**Trainer point:** Shared state is not “dump the whole chat.” Define a schema and give each agent only the context it needs.

### Example state

```yaml
incident_id: INC-1042
affected_service: checkout-api
suspected_component: promotion-cache
deployment_correlation: high
security_risk: low
recommended_action: rollback-review
```

---

# 6. Negotiation / Conflicting Agents

```mermaid
sequenceDiagram
    participant O as Operations Agent
    participant S as Supervisor
    participant SEC as Security Agent
    participant H as Human

    O->>S: Recommend restart
    SEC->>S: Block restart — possible compromise
    S->>SEC: Request supporting evidence
    SEC-->>S: Suspicious process + security event
    S->>H: Escalate conflicting high-risk recommendation
```

**Trainer point:** disagreement needs a resolution policy; “let the agents debate” is not automatically governance.

---

# 7. Cascading Failure

```mermaid
flowchart LR
    A[Agent A<br/>Wrong assumption] --> B[Agent B<br/>Treats it as fact]
    B --> C[Agent C<br/>Builds recommendation]
    C --> S[Supervisor<br/>Confident wrong answer]
```

### Controls

```mermaid
flowchart LR
    E[Evidence] --> P[Provenance]
    P --> V[Validation]
    V --> C[Confidence / Policy Gate]
    C -->|Low confidence| H[Human Escalation]
    C -->|Pass| N[Next Agent]
```

**Remember:** multi-agent systems combine distributed-system failures with probabilistic AI failures.

---

# 8. Multi-Agent Evaluation

```mermaid
flowchart TB
    E[Multi-Agent Evaluation]
    E --> A[Agent-Level]
    E --> W[Workflow-Level]
    A --> A1[Tool correctness]
    A --> A2[Groundedness]
    A --> A3[Policy compliance]
    W --> W1[Routing accuracy]
    W --> W2[Handoff quality]
    W --> W3[Task success]
    W --> W4[Recovery]
    W --> W5[Latency & Cost]
```

| Evaluate | Key question |
|---|---|
| Task success | Did the overall goal complete? |
| Routing | Was the correct specialist selected? |
| Handoff | Did the next agent receive enough context? |
| Groundedness | Are conclusions supported by evidence? |
| Policy | Did any agent exceed authority? |
| Recovery | What happened when an agent/tool failed? |
| Latency | Did orchestration become too slow? |
| Cost | How much model/tool-call amplification occurred? |

---

# 9. Framework Comparison

| Dimension | LangChain | LangGraph | AutoGen | CrewAI |
|---|---|---|---|---|
| Mental model | High-level agents/apps | Stateful graph/runtime | Conversational agent teams | Roles + tasks + crews/flows |
| Control flow | High-level / agent-driven | Explicit graph | Team/speaker driven | Process/flow driven |
| State | Agent/application state | First-class graph state | Conversation/team context | Crew/Flow state |
| Strong fit | Rapid agent composition | Production orchestration | Collaborative agent teams | Business-role workflows |
| Typical patterns | Subagents, router, handoff | Conditional graph, fan-out, cycles | RoundRobin, Selector, Swarm | Sequential, hierarchical, Flow |
| Deterministic boundaries | Medium | **High** | Medium | Medium–High with Flows |
| Best teaching message | Compose agents | Control orchestration | Let agents collaborate | Organize work around roles/tasks |

> Framework capabilities evolve. Use this as an architectural comparison, not a permanent product ranking.

---

# 10. Framework Pattern Map

```mermaid
flowchart TB
    MA[Multi-Agent Architecture]

    MA --> LC[LangChain]
    LC --> LC1[Subagents]
    LC --> LC2[Router]
    LC --> LC3[Handoffs]
    LC --> LC4[Skills]

    MA --> LG[LangGraph]
    LG --> LG1[StateGraph]
    LG --> LG2[Conditional Edges]
    LG --> LG3[Fan-out / Fan-in]
    LG --> LG4[Cycles / Subgraphs]

    MA --> AG[AutoGen]
    AG --> AG1[RoundRobin]
    AG --> AG2[SelectorGroupChat]
    AG --> AG3[Swarm]
    AG --> AG4[GraphFlow]

    MA --> CR[CrewAI]
    CR --> CR1[Sequential Crew]
    CR --> CR2[Hierarchical Crew]
    CR --> CR3[Delegation]
    CR --> CR4[Flows]
```

---

# 11. Framework Selection — Decision Visual

```mermaid
flowchart TD
    Q1{Need explicit state transitions<br/>and deterministic boundaries?}
    Q1 -->|Yes| LG[Consider LangGraph]
    Q1 -->|No| Q2{Primary abstraction is<br/>conversational team collaboration?}
    Q2 -->|Yes| AG[Consider AutoGen]
    Q2 -->|No| Q3{Business roles/tasks are<br/>the natural abstraction?}
    Q3 -->|Yes| CR[Consider CrewAI]
    Q3 -->|No| LC[Start with LangChain high-level agents]
```

**Trainer caveat:** This is a teaching heuristic—not a product-selection rule. Real selection must include deployment, observability, state, HITL, ecosystem, skills and governance requirements.

---

# 12. Demo Progression

```mermaid
flowchart LR
    D1[LangChain<br/>Supervisor] --> D2[LangChain<br/>Router]
    D2 --> D3[LangGraph<br/>StateGraph]
    D3 --> D4[LangGraph<br/>Conditional Gate]
    D4 --> D5[AutoGen<br/>Round Robin]
    D5 --> D6[AutoGen<br/>Selector]
    D6 --> D7[CrewAI<br/>Sequential]
    D7 --> D8[CrewAI<br/>Hierarchical]
```

### What to ask after every demo

```text
Who owns the goal?
      ↓
Who owns state?
      ↓
Who chooses the next agent?
      ↓
What is deterministic?
      ↓
What terminates execution?
      ↓
Where is HITL?
      ↓
How does failure propagate?
      ↓
What did multi-agent cost us?
```

---

# 13. Final Architecture Message

```mermaid
flowchart LR
    P[Problem] --> B[Agent Boundaries]
    B --> T[Topology]
    T --> S[State]
    S --> C[Coordination]
    C --> F[Failure Model]
    F --> G[Governance]
    G --> FW[Framework]
```

> **Do not start with the framework. Start with the architecture.**

And always finish with:

> **Did multi-agent materially improve the solution, or did we merely distribute one problem across more LLM calls?**
