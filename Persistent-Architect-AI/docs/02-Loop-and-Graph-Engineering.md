# Loop Engineering & Graph Engineering

## Companion to Agentic Fundamentals & Harness Engineering

> **Purpose:** A short trainer reference connecting Harness Engineering
> to Loop Engineering and Graph Engineering using one continuous
> software-engineering use case.
>
> **Positioning:** These concepts are complementary. Harness Engineering
> controls the agent's operating environment; Loop Engineering controls
> iteration and completion; Graph Engineering controls coordination and
> execution topology.

------------------------------------------------------------------------

# 1. Where This Fits

The progression is:

``` text
Agentic Fundamentals
        ↓
Agent + Autonomy + Tools + Patterns
        ↓
Harness Engineering
"How do I CONTROL the agent?"
        ↓
Loop Engineering
"How does it KEEP WORKING until done?"
        ↓
Graph Engineering
"How does COMPLEX WORK coordinate?"
```

A useful layered view:

``` mermaid
flowchart TB
    G["GRAPH ENGINEERING<br/>Coordination & Execution Topology"]
    G --> L1["LOOP<br/>Iterative Work"]
    G --> L2["LOOP<br/>Iterative Work"]
    G --> HN["Human / Deterministic Node"]

    L1 --> H1["HARNESS<br/>Controls & Boundaries"]
    L2 --> H2["HARNESS<br/>Controls & Boundaries"]

    H1 --> A1["Agent"]
    H2 --> A2["Agent"]
```

> **Key message:** Graph, Loop, and Harness are not competing
> alternatives. A production graph can contain multiple loops, and every
> autonomous agent or loop should operate within appropriate harness
> controls.

------------------------------------------------------------------------

# 2. Running Use Case --- AI-Assisted Software Change

Assume the requirement is:

> Add a new `/customer-risk` API endpoint according to an approved API
> specification, implement the code, test it, perform security review,
> and prepare it for deployment.

The simplest implementation is:

``` mermaid
flowchart LR
    R["Requirement"] --> A["Coding Agent"] --> C["Generated Code"]
```

This may work for a prototype, but it does not answer important
production questions:

-   What repository information can the agent access?
-   Which tools may it execute?
-   What specification defines correctness?
-   What if generated code fails?
-   How many times should it retry?
-   Who performs security review?
-   Who approves deployment?
-   How do multiple responsibilities coordinate?

Those questions lead naturally from **Harness → Loop → Graph
Engineering**.

------------------------------------------------------------------------

# 3. Harness Engineering --- Control the Environment

Harness Engineering surrounds model intelligence with the controls
needed for reliable operation.

``` mermaid
flowchart TB
    REQ["Requirement"] --> H["AGENT HARNESS"]

    H --> I["Instructions"]
    H --> C["Context"]
    H --> S["Specifications"]
    H --> M["Memory"]
    H --> T["Tools"]
    H --> P["Permissions"]
    H --> V["Validation"]
    H --> O["Observability"]
    H --> G["Guardrails"]
    H --> HC["Human Control"]

    H --> A["Coding Agent"]
```

For our software-change use case:

-   **Instructions** define engineering behavior.
-   **Context** provides repository and architecture information.
-   **Specifications** define the API contract and acceptance criteria.
-   **Tools** provide code search, editing, terminal, and testing.
-   **Permissions** constrain what the agent may access or execute.
-   **Validation** checks tests and contracts.
-   **Observability** records actions, failures, latency, and cost.
-   **Guardrails** constrain unsafe behavior.
-   **Human control** protects consequential operations.

But one question remains:

> **What happens when validation fails?**

That introduces Loop Engineering.

------------------------------------------------------------------------

# 4. Loop Engineering

## Definition

**Loop Engineering designs how an agent repeatedly acts, observes,
verifies, corrects, and eventually stops.**

The important engineering problem is not merely allowing the model to
"try again." It is explicitly defining **iteration, state, verification,
budgets, stopping conditions, recovery, and escalation**.

``` mermaid
flowchart LR
    G["Goal"] --> A["Act"]
    A --> O["Observe"]
    O --> V["Verify"]
    V --> D{"Goal Satisfied?"}

    D -->|Yes| E["Exit"]
    D -->|No| R["Reason / Correct"]
    R --> A
```

------------------------------------------------------------------------

## 4.1 Use Case --- Coding Agent

The coding agent generates the endpoint and runs tests.

``` mermaid
flowchart TB
    R["API Specification"] --> A["Coding Agent"]
    A --> CODE["Generate / Modify Code"]
    CODE --> TEST["Run Tests"]
    TEST --> PASS{"Tests Pass?"}

    PASS -->|Yes| DONE["Implementation Complete"]
    PASS -->|No| OBS["Capture Test Failure"]
    OBS --> FIX["Reason About Failure"]
    FIX --> CODE
```

The system now has an **execution loop**.

The human does not need to repeatedly type:

``` text
Fix it
Run tests
Fix the error
Try again
```

The architecture itself defines what happens after failure.

------------------------------------------------------------------------

# 5. A Production Loop Needs More Than Retry

A naive loop can run indefinitely:

``` text
Generate
   ↓
Test
   ↓
Fail
   ↓
Generate
   ↓
Fail
   ↓
Generate
   ↓
Fail
   ↓
💸 Cost + Latency + Risk
```

A properly engineered loop needs explicit controls.

``` mermaid
flowchart TB
    A["Agent Action"] --> V["Validate"]
    V --> OK{"Successful?"}

    OK -->|Yes| END["Exit Successfully"]

    OK -->|No| B{"Retry Budget<br/>Remaining?"}

    B -->|Yes| F["Capture Failure + Update State"]
    F --> A

    B -->|No| H["Human Escalation / Fallback"]
```

## Important Loop Controls

### Stop Condition

Defines machine-checkable evidence that the task is complete, such as
all tests passing or an acceptance criterion being satisfied. Without a
stop condition, the system cannot reliably distinguish useful iteration
from endless activity.

### Retry / Iteration Budget

Limits the number of attempts, tokens, time, or cost available to the
loop. A bounded loop prevents persistent failure from becoming
uncontrolled resource consumption.

### State

Preserves observations, failures, attempted solutions, and progress
between iterations. Without useful state, the agent may repeatedly make
the same mistake.

### Verification

Determines whether the latest action actually improved or completed the
task. Strong loops rely on tests, schemas, deterministic rules, evals,
or independent validation rather than model confidence alone.

### Recovery / Fallback

Defines what happens when normal iteration cannot solve the problem. The
system may use another strategy, invoke a specialist, revert a change,
or move to a deterministic fallback.

### Human Escalation

Transfers control to a human when retry budgets are exhausted,
confidence is low, or the action becomes consequential. Human
intervention should be an engineered state transition rather than an
accidental last resort.

------------------------------------------------------------------------

# 6. Advantages & Disadvantages of Loop Engineering

  -----------------------------------------------------------------------
  Advantages                          Disadvantages / Risks
  ----------------------------------- -----------------------------------
  Supports longer autonomous work     Infinite or ineffective loops

  Enables self-correction             Token and tool cost amplification

  Reduces repeated human prompting    Agent may repeat the wrong
                                      hypothesis

  Works well with machine-verifiable  Requires strong stopping criteria
  tasks                               

  Can recover from temporary failures More state and operational
                                      complexity

  Makes validation part of execution  Harder when success is subjective
  -----------------------------------------------------------------------

> **Trainer line:** **Never give an agent a loop without engineering its
> exit.**

------------------------------------------------------------------------

# 7. When Should We Use a Loop?

### Good candidates

-   Generate code → run tests → correct failures.
-   Generate SQL → validate syntax/results → correct.
-   Research → evaluate evidence gaps → continue research.
-   Diagnose incident → inspect evidence → refine hypothesis.
-   Generate document → evaluate against explicit criteria → improve.

### Poor candidates

-   Simple one-shot summarization.
-   Tasks with no meaningful verification mechanism.
-   High-risk actions where repeated autonomous attempts increase blast
    radius.
-   Tasks where human judgment is inherently the acceptance criterion.

------------------------------------------------------------------------

# 8. From Loop to Graph Engineering

Our coding loop solves only part of the software-change requirement.

We still need:

``` text
Planning
Development
Testing
Security Review
Architecture Validation
Human Approval
Deployment
Monitoring
```

These responsibilities may have different:

-   tools,
-   permissions,
-   context,
-   expertise,
-   execution rules,
-   failure handling.

This is where **Graph Engineering** becomes useful.

------------------------------------------------------------------------

# 9. Graph Engineering

## Definition

**Graph Engineering designs how agents, deterministic functions, tools,
validators, humans, state, branches, and loops coordinate to achieve a
larger goal.**

Instead of thinking only about one autonomous worker, we explicitly
model the **nodes, transitions, routing decisions, shared state,
parallel branches, loops, and termination paths** of the system.

------------------------------------------------------------------------

# 10. Graph Engineering Use Case

``` mermaid
flowchart TB
    R["Approved Requirement"] --> P["Planner"]

    P --> DEV["Developer Agent"]
    P --> SEC["Security Agent"]

    DEV --> TEST["Run Automated Tests"]
    TEST --> PASS{"Tests Pass?"}

    PASS -->|No| DEV
    PASS -->|Yes| REV["Code / Architecture Review"]

    SEC --> REV

    REV --> OK{"Approved?"}

    OK -->|No| DEV
    OK -->|Yes| HUMAN["Human Approval"]

    HUMAN --> DEP["Deploy"]
    DEP --> MON["Monitor"]

    MON --> HEALTH{"Healthy?"}
    HEALTH -->|No| DIAG["Diagnose"]
    DIAG --> DEV
    HEALTH -->|Yes| DONE["Complete"]
```

Notice that this graph contains **different kinds of nodes**.

### Agentic Nodes

Planner, Developer, Security, and Diagnosis may use LLM reasoning to
make adaptive decisions.

### Deterministic Nodes

Automated tests, schema validation, policy checks, deployment scripts,
and health checks can remain normal deterministic software.

### Human Nodes

Architecture approval or production deployment authorization may
deliberately remain human decisions.

### Loops

Developer → Test → Developer and Deploy → Monitor → Diagnose are loops
embedded inside the larger graph.

> **Key message:** **A graph does not mean every node must be an AI
> agent.**

------------------------------------------------------------------------

# 11. Core Graph Engineering Concepts

### Nodes

Nodes represent units of work such as agents, functions, validators,
APIs, human approvals, or deterministic processes. A good graph makes
responsibility at each node explicit.

### Edges

Edges define how execution moves between nodes. They may represent fixed
sequencing, conditional routing, failure recovery, escalation, or
loop-back behavior.

### State

State carries the information required across the graph, such as
requirements, plans, generated artifacts, test results, security
findings, and execution status. Shared state should be deliberately
designed rather than becoming an uncontrolled transcript.

### Conditional Routing

Routing decides which path should execute based on current state or
observations. Conditions may be deterministic rules or, where justified,
agentic decisions.

### Parallel Branches

Independent work can execute concurrently, such as development and
security analysis. Parallelism can reduce latency but introduces
synchronization and result-merging concerns.

### Loops

Graphs can contain one or many iterative cycles for correction,
validation, recovery, or monitoring. Loop behavior should retain
explicit budgets and exit conditions even when embedded in a graph.

### Human Gates

Humans can be first-class nodes rather than external exceptions. This
allows architecture to explicitly represent where autonomy ends and
human authority begins.

### Failure Paths

Production graphs should define what happens when nodes timeout, tools
fail, agents produce invalid output, or downstream systems are
unavailable. The failure topology is as important as the happy path.

------------------------------------------------------------------------

# 12. Advantages & Disadvantages of Graph Engineering

  -----------------------------------------------------------------------
  Advantages                          Disadvantages / Risks
  ----------------------------------- -----------------------------------
  Explicitly models complex           Higher architecture complexity
  coordination                        

  Mixes deterministic and agentic     More state to manage
  execution                           

  Supports specialization and         More difficult debugging
  permission boundaries               

  Enables parallel execution          Synchronization complexity

  Makes human gates explicit          Increased latency in large graphs

  Supports controlled recovery paths  More observability requirements

  Useful for long-running business    Can become over-engineered quickly
  processes                           
  -----------------------------------------------------------------------

> **Trainer line:** **Use a graph because the work has meaningful
> structure---not because multiple agents look sophisticated.**

------------------------------------------------------------------------

# 13. Harness vs Loop vs Graph

  -----------------------------------------------------------------------
  Engineering Discipline  Core Question           Primary Concern
  ----------------------- ----------------------- -----------------------
  **Prompt Engineering**  How should I ask the    Instructions
                          model?                  

  **Context Engineering** What information should Relevant working
                          the model see?          context

  **Harness Engineering** What environment should Reliability, safety,
                          surround and control    tools and control
                          the agent?              

  **Loop Engineering**    How should work         Iteration and
                          continue, verify and    completion
                          stop?                   

  **Graph Engineering**   How should complex work Orchestration and
                          coordinate?             execution topology
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 14. Putting Everything Together

``` mermaid
flowchart TB
    GRAPH["GRAPH ENGINEERING<br/>System Coordination"]

    GRAPH --> LOOP1["Implementation Loop"]
    GRAPH --> LOOP2["Operations Loop"]
    GRAPH --> HUMAN["Human Approval"]
    GRAPH --> STATIC["Deterministic Validation"]

    LOOP1 --> HAR1["HARNESS"]
    LOOP2 --> HAR2["HARNESS"]

    HAR1 --> AG1["Developer Agent"]
    HAR2 --> AG2["Operations Agent"]

    HAR1 --> C1["Context"]
    HAR1 --> T1["Tools"]
    HAR1 --> P1["Permissions"]
    HAR1 --> V1["Validation"]
    HAR1 --> G1["Guardrails"]

    HAR2 --> C2["Context"]
    HAR2 --> T2["Tools"]
    HAR2 --> P2["Permissions"]
    HAR2 --> V2["Validation"]
    HAR2 --> G2["Guardrails"]
```

The architecture can therefore be understood as:

``` text
GRAPH
  │
  ├── Agent / Function / Human
  │
  ├── LOOP
  │     │
  │     └── HARNESS
  │           │
  │           └── AGENT
  │
  ├── LOOP
  │     └── HARNESS
  │           └── AGENT
  │
  └── Deterministic Workflow
```

------------------------------------------------------------------------

# 15. Architecture Decision Guidance

Start with the simplest architecture that can reliably solve the
problem:

``` mermaid
flowchart LR
    A["Single Agent"]
    --> B["Agent + Tools"]
    --> C["Harnessed Agent"]
    --> D["Bounded Loop"]
    --> E["Multiple Specialized Responsibilities"]
    --> F["Execution Graph"]
```

Do **not** automatically move from left to right.

Ask:

1.  Can one agent solve the task?
2.  Does it merely need better tools?
3.  Does increased autonomy require stronger harness controls?
4.  Does the task genuinely require iteration?
5.  Can success be verified?
6.  Are multiple responsibilities genuinely distinct?
7.  Do they need different permissions, context, or expertise?
8.  Does explicit graph orchestration provide enough value to justify
    its complexity?

------------------------------------------------------------------------

# 16. Connection to LangGraph

**Graph Engineering is the architecture concept; LangGraph is one
framework that can implement graph-shaped agentic workflows.**

For example:

``` python
builder.add_edge(START, "planner")
builder.add_edge("planner", "developer")
builder.add_conditional_edges("test", route_after_test)
builder.add_edge("review", END)
```

The code expresses nodes and edges, but the important architecture
decisions happen before framework syntax:

``` text
Problem
  ↓
Responsibilities
  ↓
Deterministic vs Agentic Boundaries
  ↓
State
  ↓
Routing
  ↓
Loops
  ↓
Failure Paths
  ↓
Human Control
  ↓
Framework
```

> **Do not start with LangGraph and search for a graph. Design the
> execution architecture first, then choose the framework.**

------------------------------------------------------------------------

# 17. Final Trainer Summary

``` text
HARNESS ENGINEERING
"What controls the agent?"
        │
        ▼
Tools • Permissions • Context • Specifications
Validation • Memory • Guardrails • Observability
Human Control

LOOP ENGINEERING
"How does work continue?"
        │
        ▼
Act → Observe → Verify → Correct
        ↑                 │
        └─────────────────┘
Stop Conditions • Budgets • Escalation

GRAPH ENGINEERING
"How does complex work coordinate?"
        │
        ▼
Nodes • Edges • State • Routing • Parallelism
Loops • Humans • Failure Paths
```

### Final architectural message

> **Harness Engineering controls autonomy. Loop Engineering controls
> iteration. Graph Engineering controls coordination.**

And the Integration Architect's responsibility remains:

> **Decide where deterministic execution is sufficient, where agentic
> reasoning creates value, where iteration should be autonomous, and
> where human authority must remain.**
