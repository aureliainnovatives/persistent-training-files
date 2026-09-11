# Module 3.4 --- HITL, Protocols & Security

## Trainer Guide --- 2.5 Hours

> **Core questions**
>
> 1.  Where should autonomous AI stop and human authority begin?
> 2.  How do agents, humans, tools, and other agents communicate across
>     trust boundaries?
> 3.  Who can decide, who can execute, and who is accountable?

------------------------------------------------------------------------

## 3.4.1 Why Human-in-the-Loop Exists --- 15 min

Consider an operations agent that observes a production incident and
recommends a rollback.

``` mermaid
flowchart LR
    O["Observe Incident"] --> R["Reason"]
    R --> A["Proposed Action"]
    A --> P{"Authority Boundary"}
    P -->|Low Risk| AUTO["Execute"]
    P -->|High Risk| H["Human Decision"]
    H -->|Approve| E["Execute"]
    H -->|Reject| X["Stop / Re-plan"]
```

HITL should not mean placing a human after every AI decision. It means
deliberately engineering **authority boundaries** around actions where
risk, uncertainty, irreversibility, policy, or accountability justify
human control.

**Trainer pointer:** A model may recommend an action, but recommendation
authority and execution authority do not have to be the same thing.

------------------------------------------------------------------------

## 3.4.2 HITL Design Patterns --- 25 min

### Verification

The agent produces an output and a human verifies it before downstream
use. Useful when AI accelerates analysis but a qualified person remains
accountable for correctness.

### Approval Gate

The agent proposes a consequential action but execution is suspended
until an authorized human approves it. Deployment, financial
transactions, destructive database operations, and external
communications are common examples.

### Exception Escalation

Normal cases remain autonomous while exceptional cases are routed to a
human. This provides scalable oversight without converting every agent
action into a manual workflow.

### Feedback / Correction

A human does more than approve or reject: they provide corrective
information that changes the next agent step. This is useful when the
agent has insufficient evidence or has selected an inappropriate plan.

``` mermaid
flowchart TB
    A["Agent Proposal"] --> G{"Policy / Decision Gate"}
    G -->|Safe| E["Execute Automatically"]
    G -->|Review Required| H["Human Review"]
    G -->|Forbidden| B["Block"]
    H -->|Approve| E
    H -->|Reject| X["Stop / Re-plan"]
    H -->|Feedback| R["Agent Revises"]
    R --> G
```

------------------------------------------------------------------------

## 3.4.3 Decision Gates & Authority --- 20 min

Approval policy should ideally be based on explicit architecture rules
rather than asking the LLM to decide whether its own action is risky.

Possible gate inputs:

-   production impact;
-   financial threshold;
-   destructive operation;
-   security impact;
-   PII or sensitive-data exposure;
-   reversibility;
-   regulatory requirement;
-   evidence quality;
-   action confidence.

``` mermaid
flowchart TB
    A["Proposed Action"] --> R{"Risk Classification"}
    R -->|Low| AUTO["Automatic"]
    R -->|Medium| V["Additional Validation"]
    R -->|High| H["Human Approval"]
    R -->|Prohibited| B["Block"]
    V --> Q{"Validation Passed?"}
    Q -->|Yes| AUTO
    Q -->|No| H
```

**Architecture principle:** The agent may decide *what it wants to do*.
A policy layer should decide *whether it is allowed to do it
autonomously*.

------------------------------------------------------------------------

## 3.4.4 State, UX & Auditability --- 15 min

A useful HITL architecture must survive the pause between proposal and
approval. The workflow therefore needs persisted state, a stable
execution/thread identity, resumability, timeout/escalation behavior,
and an audit record.

``` mermaid
flowchart LR
    A["Agent"] --> P["Pause"]
    P --> S[("Persisted State")]
    S --> U["Approval UI"]
    U --> D{"Decision"}
    D -->|Approve| R["Resume"]
    D -->|Reject| X["Terminate / Re-plan"]
    R --> S
```

A reviewer should see the **proposed action, reason, evidence,
parameters, risk, expected impact, and alternatives**, not merely an
`Approve / Reject` button.

> **Human-in-the-loop without useful decision context can become
> human-as-a-rubber-stamp.**

An audit trail should capture who requested the action, which agent
proposed it, tool arguments, who reviewed it, the decision, comments,
timestamps, and final execution outcome.

------------------------------------------------------------------------

# 3.4.5 Protocol Landscape --- 20 min

Agentic architecture adds new interaction boundaries but does not
replace APIs, queues, events, or traditional integration.

``` mermaid
flowchart LR
    USER["Human"] <-->|"HITL / UI"| A1["Operations Agent"]
    A1 <-->|"Agent-to-Agent"| A2["Security Agent"]
    A1 <-->|"MCP"| TOOL["Tools / Resources"]
    A1 <-->|"REST / Events"| SYS["Enterprise Services"]
```

### API / REST

Still appropriate for deterministic application-to-application
integration. Agentic systems frequently invoke existing APIs rather than
replacing them.

### Events / Messaging

Useful for asynchronous triggers, long-running workflows, decoupling,
and event-driven agent execution. They remain especially important when
work should not depend on a synchronous chat session.

### MCP

Provides a standardized boundary through which AI applications can
discover and invoke exposed tools/resources. Architecturally, treat the
MCP server as another trust boundary requiring authentication,
authorization, validation, and observability.

### Agent-to-Agent Interaction

Relevant when independently operating agents need task delegation,
status exchange, discovery, or result handoff. Agent-to-agent
communication does not eliminate the need for identity, authorization,
bounded delegation, and message validation.

------------------------------------------------------------------------

# 3.4.6 Protocol Security & Trust --- 20 min

``` mermaid
flowchart LR
    U["User Identity"] --> A["Agent / Service Identity"]
    A --> B["Downstream Agent Identity"]
    B --> T["Tool Identity"]
    T --> R["Resource Authorization"]
```

### Authentication

Establish who is making the request: human user, agent runtime, service
account, tool server, or another agent. Do not collapse all identities
into one shared credential.

### Authorization

Authentication answers *who are you?* Authorization answers *what may
you do?* Read, update, delete, approve, and administer should remain
separate capabilities.

### Delegation

If Agent A delegates work to Agent B, authority must remain bounded.
**Delegation of work must not imply delegation of unlimited authority.**

### Credentials & Secrets

Prefer scoped and short-lived credentials where possible, with secrets
managed outside prompts and model-visible context. Never treat an LLM
conversation as a secrets vault.

### Validation & Trust Boundaries

Treat tool responses, external messages, retrieved content, and
agent-to-agent payloads as untrusted input. Validate schemas and defend
against prompt injection or instructions arriving through external
content.

### Auditability

Record identity, delegated authority, requested action, approval, tool
execution, and result so that consequential behavior can be
reconstructed.

------------------------------------------------------------------------

# 3.4.7 Hands-on --- LangChain HITL Approval Agent --- 30 min

The lab implements a small **Production Operations Agent** using
LangChain's current `create_agent` API and `HumanInTheLoopMiddleware`.

The agent has three tools:

``` text
read_service_health     → safe / automatic
restart_service         → human approval required
rollback_deployment     → human approval required
```

Architecture:

``` mermaid
flowchart TB
    U["Incident Request"] --> A["LangChain Agent"]
    A --> READ["read_service_health"]
    READ --> A
    A --> D{"Proposed Tool"}
    D -->|Read| AUTO["Execute Automatically"]
    D -->|Restart| HITL["HITL Middleware"]
    D -->|Rollback| HITL
    HITL --> S[("Checkpoint State")]
    S --> H{"Human Decision"}
    H -->|Approve| TOOL["Execute Tool"]
    H -->|Reject| A
    TOOL --> A
    A --> OUT["Final Response"]
```

The key lesson is that HITL is applied at the **tool boundary**. The LLM
can reason and propose a restart or rollback, but middleware intercepts
the side-effecting tool call before execution.

### Current LangChain behavior used in the lab

`HumanInTheLoopMiddleware` can selectively interrupt specified tool
calls while allowing safe tools to execute normally. A checkpointer and
thread ID preserve state across the interrupt so the run can later
resume with the human decision.

The middleware supports approval decisions such as `approve`, `edit`,
`reject`, and `respond`, depending on the policy configured for the
tool. This lab deliberately uses **approve/reject** to keep the first
classroom demonstration obvious.

------------------------------------------------------------------------

# 3.4.8 Final Architecture Discussion --- 5 min

``` mermaid
flowchart TB
    G["Business Goal"] --> A["Agentic Reasoning"]
    A --> P["Policy / Risk Boundary"]
    P -->|Autonomous| T["Tool"]
    P -->|Human Authority| H["HITL"]
    P -->|Forbidden| B["Block"]
    H -->|Approved| T
    T --> O["Observe"]
    O --> A
    A <-->|"Agent Protocol"| OTHER["Other Agent"]
    T <-->|"MCP / API"| SYS["Enterprise Systems"]
    AUDIT[("Audit + Observability")] --- A
    AUDIT --- H
    AUDIT --- T
```

End with three questions:

> **Who can decide?**
>
> **Who can execute?**
>
> **Who is accountable?**

Those questions connect HITL, protocols, security, harness engineering,
and enterprise integration architecture.
