# Module 3.4 --- Architecture Diagrams

These diagrams are separated so they can be copied directly into trainer
notes or presentation material.

## 1. Authority Boundary

``` mermaid
flowchart LR
    O["Observe"] --> R["Reason"]
    R --> A["Proposed Action"]
    A --> Q{"Authority Boundary"}
    Q -->|Low Risk| AUTO["Execute"]
    Q -->|High Risk| HUMAN["Human Decision"]
    HUMAN -->|Approve| EXEC["Execute"]
    HUMAN -->|Reject| REPLAN["Re-plan / Stop"]
```

## 2. Risk-Based Decision Gate

``` mermaid
flowchart TB
    ACTION["Proposed Agent Action"] --> RISK{"Risk Classification"}
    RISK -->|Low| AUTO["Automatic"]
    RISK -->|Medium| VALID["Additional Validation"]
    RISK -->|High| APPROVE["Human Approval"]
    RISK -->|Prohibited| BLOCK["Block"]
    VALID --> CONF{"Validation Passed?"}
    CONF -->|Yes| AUTO
    CONF -->|No| APPROVE
```

## 3. Pause / Persist / Resume

``` mermaid
flowchart LR
    A["Agent"] --> P["Pause"]
    P --> STATE[("Persisted State")]
    STATE --> H["Human Review"]
    H --> D{"Decision"}
    D -->|Approve| RESUME["Resume"]
    D -->|Reject| STOP["Stop / Re-plan"]
```

## 4. Protocol Boundaries

``` mermaid
flowchart LR
    USER["Human"] <-->|"HITL / UI"| AGENT1["Operations Agent"]
    AGENT1 <-->|"Agent-to-Agent"| AGENT2["Security Agent"]
    AGENT1 <-->|"MCP"| TOOL["Tools / Resources"]
    AGENT1 <-->|"REST / Events"| API["Enterprise Services"]
```

## 5. Identity Chain

``` mermaid
flowchart LR
    U["User Identity"] --> A["Agent Identity"]
    A --> B["Delegated Agent Identity"]
    B --> T["Tool / Service Identity"]
    T --> R["Resource Authorization"]
```

## 6. Hands-on Architecture

``` mermaid
flowchart TB
    U["Incident"] --> A["LangChain Operations Agent"]
    A --> READ["Read Health — Auto"]
    READ --> A
    A --> ACT{"Requested Action"}
    ACT -->|Restart| H["Human Approval"]
    ACT -->|Rollback| H
    H -->|Approve| TOOL["Execute"]
    H -->|Reject| A
    TOOL --> VERIFY["Observe Result"]
    VERIFY --> A
```
