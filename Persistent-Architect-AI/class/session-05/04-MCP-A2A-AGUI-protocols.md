# Agentic Integration Protocols --- Trainer Pointers

## MCP, UTCP, A2A, AG-UI & A2UI

> **Trainer framing:** As agents become production systems, different
> interoperability boundaries emerge. Each protocol addresses a
> different boundary.
>
> **Opening question:** What is on the other side of my agent?

------------------------------------------------------------------------

# 1. Why Are All These Protocols Appearing?

Traditional enterprise integration largely assumed:

``` text
Application
    ↓
API
    ↓
Application
```

Agentic systems introduce several new actors:

``` text
Human
Application
Agent
Other Agent
Tool
Existing API
Generated UI
```

Therefore, one universal protocol is unlikely to solve every
interaction.

``` mermaid
flowchart TB
    USER["👤 Human / User"]
    UI["Application / Frontend"]
    A["🤖 Primary Agent"]
    B["🤖 Remote Agent"]
    MCP["MCP Server"]
    API["Existing API / Service"]
    TOOL["Enterprise Tools"]

    USER --> UI
    UI <-->|"AG-UI"| A
    A -->|"A2UI"| UI
    A <-->|"A2A"| B
    A <-->|"MCP"| MCP
    A -->|"UTCP / Native Protocol"| API
    MCP --> TOOL
    API --> TOOL
```

### Trainer line

> **Don't memorize the acronyms. Identify the integration boundary
> first.**

------------------------------------------------------------------------

# 2. MCP --- Model Context Protocol

## Core question

> **How does an AI application access external capabilities and context
> through a standardized AI-facing interface?**

MCP gives AI applications a standardized protocol for interacting with
servers exposing capabilities such as tools and resources.

## Explain it visually

``` mermaid
flowchart LR
    A["Agent / AI Application"]
    A --> MC["MCP Client"]
    MC <-->|"MCP"| MS["MCP Server"]
    MS --> DB["Database"]
    MS --> API["Enterprise API"]
    MS --> FS["Files"]
    MS --> SaaS["SaaS"]
```

### Speak

The agent does not need to understand every database driver, filesystem
API, or SaaS integration. The MCP server exposes an **AI-oriented
capability boundary**.

Conceptually:

``` text
MCP Server

Tools
├── search_customer
├── create_ticket
└── get_invoice

Resources
├── product documentation
├── policies
└── configuration
```

The agent discovers and uses those capabilities.

## Important architectural point

MCP is **not simply function calling**.

Function calling tells the model:

> These functions exist.

MCP creates a protocol around exposing and consuming capabilities across
system boundaries.

## Enterprise use case

``` mermaid
flowchart LR
    A["Support Agent"]
    --> MCP["Customer Service MCP"]

    MCP --> CRM["CRM"]
    MCP --> KB["Knowledge Base"]
    MCP --> TICKET["Ticketing"]
```

Instead of giving the agent unrestricted CRM/database access, expose
controlled business capabilities.

## Advantages

-   Standardized AI/tool boundary
-   Capability abstraction
-   Reusable integrations
-   Tool discovery
-   Centralized governance opportunity
-   Hides underlying implementation

## Watch-outs

-   Another runtime/server may need operating
-   Another security boundary
-   Poorly designed MCP servers can expose excessive capabilities
-   MCP does not remove authorization requirements

### Trainer line

> **MCP is where I deliberately create an AI-facing capability
> boundary.**

------------------------------------------------------------------------

# 3. UTCP --- Universal Tool Calling Protocol

## Core question

> **Why create another wrapper if my enterprise capability already has a
> perfectly good API?**

UTCP takes a different approach. It describes tools and how to invoke
them through their existing native transports rather than requiring an
AI-specific wrapper around every capability.

## MCP approach

``` mermaid
flowchart LR
    A["Agent"] --> MCP["MCP Server"]
    MCP --> REST["Existing REST API"]
    REST --> SAP["SAP / ServiceNow / CRM"]
```

## UTCP approach

``` mermaid
flowchart LR
    M["UTCP Manual<br/>Tool + Transport + Auth"]
    --> A["Agent / UTCP Client"]

    A -->|"Native REST"| REST["Existing API"]
    A -->|"Native gRPC"| GRPC["gRPC Service"]
    A -->|"Native CLI"| CLI["CLI"]
```

### Speak

Imagine ServiceNow already exposes:

``` text
POST /api/now/table/incident
```

Why necessarily build:

``` text
Agent
 ↓
MCP Server
 ↓
ServiceNow REST API
```

UTCP allows the capability to be described so that a compatible client
understands its transport, endpoint, authentication, and input contract.

Conceptually:

``` text
Tool:
create_incident

Transport:
HTTP

Endpoint:
/api/now/table/incident

Authentication:
OAuth

Input:
incident details
```

The client then invokes the existing interface directly.

## MCP vs UTCP

Do not teach:

> UTCP replaces MCP.

Teach:

``` text
MCP
"Introduce an AI-oriented capability boundary."

UTCP
"Describe an existing capability and reuse
its native transport."
```

## Architecture decision

``` mermaid
flowchart TB
    Q["Agent needs enterprise capability"]

    Q --> D{"Need an AI-specific<br/>capability boundary?"}

    D -->|"Yes"| MCP["MCP Server"]
    D -->|"No — existing API is appropriate"| UTCP["UTCP / Native Interface"]

    MCP --> SYS["Enterprise System"]
    UTCP --> SYS
```

### Trainer line

> **The architectural question is not MCP versus UTCP. It is whether an
> AI-specific intermediary creates enough governance or abstraction
> value to justify itself.**

------------------------------------------------------------------------

# 4. A2A --- Agent2Agent Protocol

## Core question

> **How does one independently operating agent delegate work to and
> collaborate with another agent?**

``` mermaid
flowchart LR
    A["Proposal Agent<br/>LangGraph"]
    A <-->|"A2A"| B["Security Agent<br/>Java"]
    A <-->|"A2A"| C["Pricing Agent<br/>SAP Team"]
    A <-->|"A2A"| D["Legal Agent<br/>External Vendor"]
```

### Speak

These are not necessarily three Python objects inside one application.

They could belong to:

-   Different frameworks
-   Different runtimes
-   Different teams
-   Different cloud platforms
-   Different organizations

A2A gives independently operating agents a common communication model.

------------------------------------------------------------------------

## Five A2A Concepts to Remember

``` mermaid
flowchart LR
    CARD["1. Agent Card<br/>What can you do?"]
    --> MSG["2. Message<br/>What are we communicating?"]
    --> TASK["3. Task<br/>What work are you doing?"]
    --> STATUS["4. Status<br/>Where is the work?"]
    --> ART["5. Artifact<br/>What did you produce?"]
```

### 1. Agent Card

Describes the agent and its capabilities: what it can do, where it can
be reached, and relevant security/capability information.

A useful teaching analogy:

``` text
REST Service → OpenAPI

Agent → Agent Card
```

The analogy is not exact, but it helps explain discovery and contract
thinking.

### 2. Message

Communication exchanged between agents. A message can carry more than
conversational prose and can include structured information.

### 3. Task

A stateful unit of delegated work.

Traditional API:

``` text
Request
  ↓
Response
```

Agent work may look like:

``` text
Task
 ↓
Working
 ↓
Need information
 ↓
Working
 ↓
Artifact
 ↓
Completed
```

### 4. Status

Represents where the delegated work currently stands: submitted,
working, requiring additional input, completed, failed, or another
protocol-defined state.

### 5. Artifact

A concrete output produced by the work.

Think:

``` text
Message
=
communication

Task
=
work being performed

Artifact
=
thing produced
```

## Example

``` mermaid
sequenceDiagram
    participant P as Proposal Agent
    participant S as Security Agent

    P->>S: Discover Agent Card
    S-->>P: Skills + Endpoint + Security

    P->>S: Analyze vendor security
    S-->>P: Task = Working

    S-->>P: Input Required
    P->>S: Vendor = Azure OpenAI

    S-->>P: Task = Working
    S-->>P: Artifact = Security Assessment
    S-->>P: Task = Completed
```

------------------------------------------------------------------------

## MCP vs A2A

``` text
MCP
Agent → Capability

"Search this database."


A2A
Agent → Autonomous Agent

"Take responsibility for performing
this security assessment."
```

``` mermaid
flowchart TB
    P["Proposal Agent"]

    P <-->|"A2A"| S["Security Agent"]

    S --> R["Own Reasoning"]
    S --> M["Own Memory"]
    S <-->|"MCP"| T["Security Tools"]
```

### Trainer lines

> **MCP delegates capability access. A2A delegates work to another
> autonomous system.**

> **Multiple agents do not automatically justify A2A.**

If several agents are merely internal nodes in one application/runtime,
internal orchestration may be sufficient.

Use A2A when a **genuine interoperability boundary** exists.

------------------------------------------------------------------------

# 5. AG-UI --- Agent--User Interaction Protocol

## Core question

> **How does a user-facing application participate in a live, stateful
> agent execution?**

AG-UI is designed around communication between user-facing applications
and agentic backends.

## Why ordinary request/response becomes awkward

``` text
POST /agent

"Investigate payment-service"

            ↓

wait...

            ↓

"The problem is fixed."
```

But the actual execution might have been:

``` text
Started
 ↓
Reading metrics
 ↓
Calling deployment tool
 ↓
Found anomaly
 ↓
Need approval
 ↓
Waiting
 ↓
Approved
 ↓
Rollback
 ↓
Monitoring
 ↓
Finished
```

The application may need visibility into those intermediate events.

------------------------------------------------------------------------

## Think event stream

``` mermaid
sequenceDiagram
    participant U as User
    participant UI as Application
    participant A as Agent

    U->>UI: Investigate incident
    UI->>A: Start Run

    A-->>UI: RUN_STARTED
    A-->>UI: TEXT_MESSAGE_CONTENT
    A-->>UI: TOOL_CALL_START
    A-->>UI: TOOL_CALL_ARGS
    A-->>UI: TOOL_CALL_END
    A-->>UI: STATE_DELTA

    UI-->>U: Show current activity

    A-->>UI: Approval Required
    U->>UI: Approve
    UI->>A: User action

    A-->>UI: RUN_FINISHED
```

Important event concepts to mention:

``` text
RUN_STARTED
RUN_FINISHED
RUN_ERROR

TEXT_MESSAGE_START
TEXT_MESSAGE_CONTENT
TEXT_MESSAGE_END

TOOL_CALL_START
TOOL_CALL_ARGS
TOOL_CALL_END
TOOL_CALL_RESULT

STATE_SNAPSHOT
STATE_DELTA
```

Participants do not need to memorize the names. Explain **why an
event-oriented contract is useful for agent execution**.

------------------------------------------------------------------------

## AG-UI + HITL

``` mermaid
flowchart LR
    AG["Operations Agent"]
    --> INT["HITL Interrupt"]

    INT --> AGUI["AG-UI Events"]

    AGUI --> UI["Operations Console"]

    UI --> H["Human<br/>Approve / Reject"]

    H --> AGUI
    AGUI --> AG
```

### Trainer line

> **HITL tells us where the human participates. AG-UI can help carry
> that participation between the agent runtime and application.**

------------------------------------------------------------------------

# 6. A2UI --- Agent-to-User Interface

## Core question

> **How can an agent describe the UI appropriate for the current task
> without generating arbitrary executable frontend code?**

A2UI uses declarative UI descriptions that a trusted client renderer
interprets using an agreed component catalog.

------------------------------------------------------------------------

## Start With the Bad Approach

User:

> Show hotels around Marina Bay.

LLM generates:

``` text
HTML
CSS
JavaScript
React
```

Potential problems:

``` text
Arbitrary code
Security problems
XSS
Unknown dependencies
Brand inconsistency
Accessibility problems
```

Instead:

``` mermaid
flowchart LR
    U["User Request"]
    --> A["Agent / LLM"]

    CAT["A2UI Component Catalog"]
    --> A

    A --> JSON["Declarative A2UI Description"]

    JSON --> VALIDATE["Schema Validation"]

    VALIDATE --> R["Trusted Renderer"]

    R --> UI["Native Application UI"]
```

### Trainer line

> **The agent describes the interface. The application remains
> responsible for rendering it safely.**

------------------------------------------------------------------------

# 7. The A2UI Component Catalog

This is critical.

Think of a catalog containing general-purpose components such as:

``` text
LAYOUT
Row
Column
List

DISPLAY
Text
Image
Icon
Divider

INTERACTIVE
Button
TextField
CheckBox
Slider
DateTimeInput
ChoicePicker

CONTAINERS
Card
Modal
Tabs
```

The catalog tells the agent which UI concepts it is allowed to express
and the properties those components support.

------------------------------------------------------------------------

# 8. Function Calling for UI --- Teaching Analogy

### Tool calling

``` text
Developer provides:

search_customer()
create_ticket()
get_weather()

        ↓

LLM selects a tool
and provides arguments.
```

### A2UI

``` text
Application provides:

Card
Table
Button
Map
ApprovalPanel

        ↓

LLM selects components
and supplies properties/data.
```

This is a teaching analogy rather than a claim that the mechanisms are
identical.

### Trainer line

> **Tool calling constrains what the agent can ask the system to DO.
> A2UI constrains what the agent can ask the client to RENDER.**

------------------------------------------------------------------------

# 9. Custom Enterprise Components

This is where A2UI becomes particularly interesting to enterprise
architects.

Imagine the application exposes:

``` text
Basic Components
+
Enterprise Components

VendorRiskCard
PurchaseOrderTable
IncidentTimeline
ArchitectureDiagram
ApprovalPanel
DeploymentStatus
Map
```

``` mermaid
flowchart TB
    CAT["Enterprise A2UI Catalog"]

    CAT --> C1["VendorRiskCard"]
    CAT --> C2["ApprovalPanel"]
    CAT --> C3["Map"]
    CAT --> C4["IncidentTimeline"]

    CAT --> LLM["LLM / Agent"]

    LLM --> DESC["A2UI Surface Description"]

    DESC --> R["Enterprise Renderer"]

    R --> DS["Existing Design System"]
```

The LLM does not need to understand your React implementation.

It needs the **catalog contract**.

------------------------------------------------------------------------

# 10. Who Controls What in A2UI?

  Decision                               Responsibility
  -------------------------------------- --------------------------
  A map would help                       Agent
  Show three hotel cards                 Agent
  Hotel data                             Agent/application
  `Map` is an allowed component          Catalog
  Properties accepted by `Map`           Catalog
  Google Maps vs Mapbox                  Developer
  React/Angular/Flutter implementation   Developer
  Colors/fonts/branding                  Design system
  Responsive behavior                    Component implementation
  Allowed actions                        Application policy
  Rendering                              Trusted client

------------------------------------------------------------------------

# 11. A2UI Map Example

User:

> Show me directions from Pune Airport to the hotel.

The agent can conceptually compose:

``` text
Column
│
├── Text
│   "Route to Hotel"
│
├── Map
│   origin = Pune Airport
│   destination = Hotel
│
└── Card
    ├── Distance
    ├── Travel Time
    └── Start Navigation
```

The application maps:

``` text
A2UI Map
    ↓
OurMapComponent
    ↓
Google Maps / Mapbox SDK
```

The protocol-level UI description does not need to know the
implementation details of the mapping SDK.

------------------------------------------------------------------------

# 12. Why A2UI Can Be Safer Than Generated React

``` mermaid
flowchart TB
    LLM["LLM"]

    LLM --> JSON["Declarative Description"]

    JSON --> SCHEMA{"Valid Catalog Schema?"}

    SCHEMA -->|No| BLOCK["Reject"]
    SCHEMA -->|Yes| POLICY{"Allowed Actions?"}

    POLICY -->|No| BLOCK
    POLICY -->|Yes| RENDER["Trusted Renderer"]

    RENDER --> UI["Application UI"]
```

### Trainer line

> **A2UI gives the agent expressive UI capability without giving the
> model arbitrary frontend execution capability.**

------------------------------------------------------------------------

# 13. AG-UI vs A2UI

These two will often be confused.

``` text
AG-UI
────────────────────────

"What is happening between
the application and agent?"

Events
State
Messages
Tool activity
User interaction
Run lifecycle


A2UI
────────────────────────

"What should the application
show?"

Cards
Forms
Tables
Maps
Layouts
Actions
Data bindings
```

### Trainer explanation

**AG-UI** concerns the ongoing interaction channel and runtime events
between the application and agent.

**A2UI** concerns a declarative description of the interface that should
be presented.

They can therefore be complementary rather than competing protocols.

------------------------------------------------------------------------

# 14. Complete Agentic Protocol Stack

This should be the primary summary diagram.

``` mermaid
flowchart TB
    HUMAN["👤 HUMAN"]

    APP["Web / Mobile / Enterprise Application"]

    AGENT["🤖 PRIMARY AGENT"]

    SPECIAL["🤖 SPECIALIST AGENT"]

    MCP["MCP SERVER"]

    API["EXISTING API"]

    SYSTEM["ENTERPRISE SYSTEMS"]

    HUMAN --> APP

    APP <-->|"AG-UI<br/>Events • State • Interaction"| AGENT

    AGENT -->|"A2UI<br/>Declarative UI"| APP

    AGENT <-->|"A2A<br/>Tasks • Messages • Artifacts"| SPECIAL

    AGENT <-->|"MCP<br/>AI-facing capabilities"| MCP

    AGENT -->|"UTCP<br/>Native protocol"| API

    MCP --> SYSTEM
    API --> SYSTEM
```

------------------------------------------------------------------------

# 15. One Enterprise Use Case Connecting Everything

Use an **AI Incident Management Platform**.

User says:

> Investigate the payment-service incident and recover the service.

``` mermaid
flowchart TB
    USER["SRE / Operator"]
    --> UI["Incident Console"]

    UI <-->|"AG-UI"| MAIN["Incident Agent"]

    MAIN -->|"A2UI"| UI

    MAIN <-->|"A2A"| SEC["Security Agent"]

    MAIN <-->|"MCP"| OPS["Operations MCP"]

    MAIN -->|"UTCP / REST"| CMDB["Existing CMDB API"]

    OPS --> LOG["Logs"]
    OPS --> MET["Metrics"]
    OPS --> DEP["Deployment System"]

    MAIN --> HITL{"High-Risk Action?"}

    HITL -->|Yes| UI
    HITL -->|No| EXEC["Execute"]
```

## Tell the story

### UTCP

Read the existing CMDB capability through its native API rather than
automatically introducing another AI-specific wrapper.

### MCP

Access curated operational capabilities such as metrics and deployment
tools through an AI-oriented tool boundary.

### A2A

Ask an independently deployed Security Agent to investigate whether the
incident is security-related.

### AG-UI

Stream investigation progress, state, tool activity, and approval
interactions to the incident console.

### A2UI

Describe an appropriate interface such as:

``` text
IncidentTimeline
+
EvidenceCard
+
DeploymentComparison
+
RollbackApprovalPanel
```

------------------------------------------------------------------------

# 16. Architecture Decision Guide

``` mermaid
flowchart TB
    Q["What does my Agent need?"]

    Q --> TOOL{"Tool / Context?"}
    TOOL -->|Yes| MCP["Consider MCP"]

    Q --> EXIST{"Existing native API?"}
    EXIST -->|Yes| UTCP["Consider UTCP"]

    Q --> AG{"Independent Agent?"}
    AG -->|Yes| A2A["Consider A2A"]

    Q --> UX{"Interactive Agent Frontend?"}
    UX -->|Yes| AGUI["Consider AG-UI"]

    Q --> GEN{"Agent-Generated UI?"}
    GEN -->|Yes| A2UI["Consider A2UI"]
```

------------------------------------------------------------------------

# 17. Five Questions to Remember

## MCP

> **How does my agent access AI-oriented tools and resources?**

## UTCP

> **How can my agent reuse an existing capability through its native
> protocol?**

## A2A

> **How does my agent delegate work to another independently operating
> agent?**

## AG-UI

> **How does my application participate in and represent an ongoing
> agent execution?**

## A2UI

> **How can my agent describe the interface appropriate for the current
> task?**

------------------------------------------------------------------------

# 18. Final Comparison

  Protocol    Boundary                      Think
  ----------- ----------------------------- ----------------------------------
  **MCP**     Agent ↔ Tools / Resources     AI capability boundary
  **UTCP**    Agent ↔ Existing API / Tool   Native capability reuse
  **A2A**     Agent ↔ Agent                 Autonomous task delegation
  **AG-UI**   Application ↔ Agent           Runtime interaction and state
  **A2UI**    Agent → UI                    Declarative generative interface

------------------------------------------------------------------------

# 19. Final Trainer Message

Do not architect:

``` text
MCP
+
UTCP
+
A2A
+
AG-UI
+
A2UI
```

simply because these protocols exist.

A perfectly valid architecture could still be:

``` text
React
  ↓ REST
LangChain Agent
  ↓ MCP
Enterprise Tools
```

The system does not become more agentic merely because more protocols
are introduced.

> **Protocols should follow architectural boundaries. Architectural
> boundaries should not be invented merely to justify protocols.**

The Integration Architect should identify where:

-   tool interoperability,
-   existing API reuse,
-   independent agent collaboration,
-   interactive frontend communication, or
-   generative UI

creates a genuine system boundary, and then introduce the appropriate
protocol.

------------------------------------------------------------------------

# Closing Mental Model

``` text
                         USER
                          │
                          ▼
                     APPLICATION
                     ↕         ↑
                   AG-UI     A2UI
                     ↕         │
                     PRIMARY AGENT
                    /      |       \
                   /       |        \
                 A2A      MCP       UTCP
                  ↓        ↓          ↓
               AGENT     TOOLS    EXISTING APIs
```

> **Identify the boundary first. Choose the protocol second.**
