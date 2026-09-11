# Agentic AI --- Fundamentals, Design Patterns & Harness Engineering

> Trainer reference based on the supplied architecture notes.
>
> **Core principle:** More autonomy increases capability, but also
> increases the need for control.

------------------------------------------------------------------------

## 1. Agentic Fundamentals

### Agent

An agent is an AI system designed to complete a task on behalf of a user
rather than merely generate a response. A useful formula is **Model +
Instructions + Context + Tools + Control Loop**.

### Autonomy

Autonomy means the agent decides its next *permitted* action without
needing step-by-step user instructions. It may search, call an API,
delegate, request information, or stop.

### Reasoning

Reasoning evaluates the goal, available context, and observations to
determine the next action. The simplified loop is **Observe → Decide →
Act → Observe → Continue/Stop**.

### Tool Usage

Tools extend the model beyond text generation by connecting it to Python
functions, REST APIs, databases, web search, MCP tools, and enterprise
applications.

``` mermaid
flowchart LR
    G["Goal"] --> C["Context"]
    C --> R["Reason / Decide"]
    R --> A["Act"]
    A --> T["Tool / Agent"]
    T --> O["Observe"]
    O --> D{"Done?"}
    D -->|No| R
    D -->|Yes| E["Stop"]
```

------------------------------------------------------------------------

## 2. Agent Execution Loop

1.  **Receive Goal** --- Establish the outcome the agent is expected to
    achieve. The goal anchors subsequent decisions and stopping
    conditions.
2.  **Understand Context** --- Examine user input, retrieved knowledge,
    application state, files, or prior observations. Relevant context
    improves decision quality.
3.  **Reason / Decide** --- Determine the most appropriate next
    permitted step. This introduces dynamic decision-making compared
    with a fixed workflow.
4.  **Select Tool or Agent** --- Choose an external capability or
    specialist when additional information or action is required.
    Available capabilities should be explicitly bounded.
5.  **Execute Action** --- Invoke the selected function, API, system, or
    agent. Execution should remain subject to permissions and
    operational controls.
6.  **Observe Result** --- Treat the execution result as new evidence
    that may change the agent's understanding. Observations feed the
    next decision.
7.  **Continue, Delegate, Ask or Stop** --- Decide whether to iterate,
    delegate, seek clarification, escalate, or terminate based on goal
    completion.

> **LLM vs Agent:** An LLM primarily generates a response. An agent
> works toward a goal by deciding and taking permitted actions.

------------------------------------------------------------------------

## 3. Common Agentic Design Patterns

### Router

Routes an incoming request to the appropriate tool, workflow, or
specialist. Example: **Customer Query → Billing Agent / Support Agent /
Order Agent**.

### Sequential

Passes the output of one step to the next when activities have
dependencies. Example: **Order → Destination → Weather → Delivery
Recommendation**.

### Parallel

Executes independent tasks simultaneously and combines the results
later. Example: **Price Check + Inventory Check + Risk Check**.

### Supervisor--Worker

A supervisor owns the overall goal and delegates bounded tasks to
specialists. Example: **Supervisor → Data Agent / API Agent / Testing
Agent**.

### Planner--Executor

A planner determines the steps required to achieve the goal, while an
executor performs them. This separates decomposition from execution.

### Evaluator--Optimizer

One component generates an output while another evaluates it and
requests improvement. Example: **Code Generator → Reviewer → Fix →
Re-evaluate**.

### Human-in-the-Loop

The system pauses for human approval before consequential actions.
Example: **Generate Deployment → Architect Approval → Deploy**.

``` mermaid
flowchart TB
    R["Request"] --> Q{"Need?"}
    Q --> A["Router"]
    Q --> B["Sequential"]
    Q --> C["Parallel"]
    Q --> D["Supervisor–Worker"]
    Q --> E["Planner–Executor"]
    Q --> F["Evaluator–Optimizer"]
    Q --> G["Human-in-the-Loop"]
```

------------------------------------------------------------------------

## 4. Choosing the Right Pattern

  Situation               Prefer
  ----------------------- --------------------------------
  Simple task             **Single Agent**
  External capabilities   **Agent + Tools**
  Dependent steps         **Sequential / Chained Tools**
  Independent tasks       **Parallel Execution**
  Distinct domains        **Specialist Agents**
  Complex coordination    **Supervisor or Planner**
  High-risk action        **Human-in-the-Loop**

> **Architecture principle:** Do not use multiple agents when one agent
> with good tools can solve the problem.

------------------------------------------------------------------------

# 5. Harness Engineering

**Harness Engineering** is engineering the environment around a model so
an AI system can operate reliably, safely, and repeatedly.

> **The model provides intelligence; the harness provides reliability
> and control.**

## Harness Layers

### 1. Instructions

Define the role, goal, constraints, priorities, and expected behavior of
the agent. They convert general model capability into task-specific
operating behavior.

### 2. Context

Provides the relevant business, technical, conversational, or task
information required for the current decision. Context engineering
controls what the model should know *now*.

### 3. Tools

Connect the agent to APIs, databases, functions, MCP servers, search
systems, and enterprise applications. Tools turn reasoning into external
observation and action.

### 4. Specifications

Define requirements, contracts, constraints, schemas, acceptance
criteria, and engineering rules. Specifications give generation and
validation a concrete definition of correctness.

### 5. Memory

Maintains useful state and relevant information across steps or
interactions. Memory provides continuity without requiring the complete
history to be repeatedly inserted into context.

### 6. Validation

Checks outputs and actions using schemas, tests, deterministic rules,
acceptance criteria, and evals. Validation provides evidence of
correctness beyond the model's own confidence.

### 7. Permissions

Control which systems, data, tools, and actions an agent may access.
Permissions establish least-privilege boundaries around autonomous
behavior.

### 8. Observability

Captures traces, decisions, tool calls, failures, latency, token usage,
and cost. Observability makes agent behavior diagnosable and
operationally measurable.

### 9. Guardrails

Prevent or constrain unsafe, invalid, policy-violating, or unauthorized
behavior. Guardrails can operate before, during, and after model
execution.

### 10. Human Control

Introduces human approval, review, intervention, or escalation at
defined decision points. It preserves human authority where actions are
consequential or confidence is insufficient.

``` mermaid
flowchart TB
    U["User / Goal"] --> H["AGENT HARNESS"]
    H --> I["1. Instructions"]
    H --> C["2. Context"]
    H --> S["4. Specifications"]
    I --> M["Model / Agent"]
    C --> M
    S --> M
    MEM["5. Memory"] <--> M
    M --> T["3. Tools"]
    P["7. Permissions"] --> T
    T --> V["6. Validation"]
    G["9. Guardrails"] --> M
    M --> O["8. Observability"]
    V --> HC["10. Human Control"]
    V --> R["Controlled Result"]
    HC --> R
```

------------------------------------------------------------------------

## 6. Engineering Evolution

### Prompt Engineering --- "How should I ask the model?"

Focuses on instructions supplied to the model for an interaction. It
improves how intent, constraints, roles, and desired outputs are
communicated.

### Context Engineering --- "What information should the model see?"

Focuses on assembling relevant information for the current decision.
This may include retrieval, state, memory, files, business information,
and tool observations.

### Harness Engineering --- "What system should surround the model?"

Expands the problem to tools, specifications, validation, permissions,
observability, guardrails, memory, and human control. The goal is a
dependable agentic system rather than only a better model interaction.

``` mermaid
flowchart LR
    P["Prompt Engineering<br/>How should I ask?"]
    --> C["Context Engineering<br/>What should it know?"]
    --> H["Harness Engineering<br/>What should surround it?"]
    --> R["Reliable Agentic System"]
```

------------------------------------------------------------------------

## 7. Connection to Specification-Driven Development

Specifications become part of the engineering harness for AI-generated
software. They can include **business requirements, architecture
constraints, API contracts, data schemas, coding standards, acceptance
criteria, test cases, and security requirements**.

``` mermaid
flowchart LR
    S["Specification"] --> A["Agent"] --> G["Generate"]
    G --> V["Validate"] --> E["Evaluate"] --> D{"Correct?"}
    D -->|No| C["Correct"]
    C --> V
    D -->|Yes| H["Approve"]
```

> **SDD principle:** Do not rely only on better prompting; give the
> agent explicit specifications and mechanisms to verify its work.

------------------------------------------------------------------------

## 8. Integration Architect Perspective

### Traditional Architecture

Routing, orchestration, transformation, APIs, pipelines, retries,
security, and monitoring remain core integration concerns. Agentic
systems do not eliminate these established disciplines.

### Agentic Architecture Adds

Agentic architecture introduces LLM-based decision-making, dynamic tool
selection, delegation, reasoning loops, and dynamic workflow execution.
The new concern is controlled autonomy inside an otherwise engineered
system.

### Architect Responsibility

The architect defines where autonomy is useful, where deterministic
workflows are required, and where human control must remain. This
boundary between probabilistic reasoning and deterministic execution
should be an explicit architecture decision.

``` mermaid
flowchart LR
    T["Traditional Architecture<br/>Routing • APIs • Pipelines<br/>Retries • Security • Monitoring"]
    --> A["+ Agentic Capability"]
    A --> L["LLM Decisions<br/>Dynamic Tools<br/>Delegation • Reasoning Loops"]
    L --> C{"Architectural Control"}
    C -->|Predictable| D["Deterministic Workflow"]
    C -->|Adaptive| E["Agentic Decision"]
    C -->|Consequential| H["Human Control"]
```

------------------------------------------------------------------------

# 9. Use Case --- AI-Assisted Software Change

**Goal:** Implement a new API endpoint from an approved requirement.

``` mermaid
flowchart TB
    REQ["Business Requirement / Specification"] --> AG["Coding Agent"]
    CTX["Repository + Architecture Context"] --> AG
    INS["Engineering Instructions"] --> AG
    MEM["Task State / Memory"] --> AG

    AG --> TOOL["Code / Search / Test Tools"]
    PERM["Tool Permissions"] --> TOOL
    TOOL --> TEST["Validation<br/>Tests + Acceptance Criteria"]
    TEST --> OK{"Valid?"}
    OK -->|No| AG
    OK -->|Yes| REVIEW["Human Review / Approval"]

    GRD["Security + Guardrails"] --> AG
    OBS["Traces + Tool Calls + Cost"] --- AG
    REVIEW --> DONE["Approved Change"]
```

The **agent** supplies reasoning and chooses permitted actions;
**tools** let it inspect, modify, and test the repository.
**Specifications and context** define what the work should achieve and
what correct implementation means.

**Permissions, guardrails, validation, observability, and human
approval** convert model intelligence into a controlled engineering
system. That surrounding operational architecture is the **harness**.

------------------------------------------------------------------------

# 10. Quick Reference

``` text
AGENT
= Model
+ Instructions
+ Context
+ Tools
+ Control Loop

HARNESS
= Agent
+ Specifications
+ Memory
+ Validation
+ Permissions
+ Observability
+ Guardrails
+ Human Control
```

> **Final architecture question:** Do not ask only, "How intelligent is
> my model?" Ask: **What can it see? What can it do? What defines
> correctness? What can it access? How do we verify it? How do we
> observe it? When must it stop? And when must a human take control?**
