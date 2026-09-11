# FDE-MM --- Model Mechanics for Forward-Deployed Architects

## Purpose

This module is designed for **Forward-Deployed Engineer (FDE) aspirants
who already operate at Technical Architect / Senior Engineer level**.

The cohort is assumed to already understand foundational concepts such
as:

-   NLP basics
-   tokenization and tokens
-   embeddings and semantic similarity
-   basic Transformer/attention concepts
-   basic RAG and vector databases
-   prompt engineering fundamentals
-   introductory agentic architecture

The purpose is therefore **not to reteach how LLMs work academically**.

The module answers a more valuable FDE question:

> **What must I understand about model behaviour so that I can diagnose
> customer problems, make architecture decisions, select interventions,
> prove quality, and defend production economics?**

------------------------------------------------------------------------

## Learning Philosophy

The module progresses through the following operating model:

``` mermaid
flowchart LR
    A[MODEL<br/>How does it behave?] --> B[BEHAVIOUR<br/>What do we observe?]
    B --> C[FAILURE<br/>Why did it fail?]
    C --> D[INTERVENTION<br/>What should change?]
    D --> E[EVALUATION<br/>Did it improve?]
    E --> F[ECONOMICS<br/>Is it production-worthy?]
```

An architect may ask:

> **How should this AI system be designed?**

An FDE must additionally answer:

> **Why is it behaving this way in the customer's environment, what
> should we change, and how do we prove that the change creates value?**

------------------------------------------------------------------------

# 1. From Model Mechanics to Model Behaviour

## Objective

Understand model mechanics through their **observable production
consequences**, rather than through mathematical implementation detail.

### Key Topics

-   Probabilistic generation and output variability
-   Autoregressive generation and error propagation
-   Temperature, top-p and decoding at an architectural level
-   Deterministic versus probabilistic workloads
-   Instruction following and competing instructions
-   Parametric knowledge versus contextual knowledge
-   Retrieved knowledge versus tool-obtained knowledge
-   Structured-output reliability
-   Why identical-looking requests can produce different outcomes
-   Model capability boundaries

### FDE Decision Model

``` mermaid
flowchart TD
    A[Probabilistic Generation] --> B[Output Variability]
    B --> C{Can the business tolerate variance?}
    C -->|Yes| D[LLM-led solution may fit]
    C -->|No| E[Constrain behaviour]
    E --> F[Rules / Validation / Structured Output]
    E --> G[Human Approval]
    E --> H[Deterministic Software]
```

### FDE Questions

Instead of asking only *which model is strongest?*, ask:

-   How much behavioural variance can this business process tolerate?
-   Is creativity desirable or dangerous here?
-   Which decisions must be deterministic?
-   Which outputs require validation?
-   What happens if the first reasoning step is wrong?
-   Should the model decide, recommend, or merely extract information?
-   What is the blast radius of an incorrect answer?

### Use Case --- Invoice Classification

A finance customer reports:

> "The same invoice was classified correctly yesterday and incorrectly
> today. Is the AI unreliable?"

The FDE investigates:

1.  Was the exact input identical?
2.  Did system instructions change?
3.  Did retrieved context change?
4.  Was a different model/version used?
5.  Are decoding parameters stochastic?
6.  Is the classification constrained to an allowed schema?
7.  Can deterministic rules handle obvious invoice classes before
    invoking the LLM?

**Learning:** Model mechanics become useful when they explain
**business-visible behaviour**.

------------------------------------------------------------------------

# 2. Context Engineering --- Designing the Model's Working Environment

## Objective

Move beyond prompt engineering and understand the complete information
environment available to the model at a particular point in execution.

``` mermaid
flowchart BT
    SP[System Instructions] --> EC[Effective Context]
    RAG[Retrieved Knowledge] --> EC
    CH[Conversation History] --> EC
    EX[Examples] --> EC
    TS[Tool State / Results] --> EC
    MEM[Memory / Business State] --> EC
    POL[Policies / Constraints] --> EC
    EC --> M[Model]
    M --> O[Generated Behaviour]
```

## Key Topics

-   Context window versus memory
-   System, user, retrieved, tool and conversational context
-   Effective context versus available enterprise information
-   Context budgeting
-   Context competition
-   Relevance versus context volume
-   Lost-in-the-middle effects
-   Conflicting context
-   Stale context
-   Context poisoning
-   Ordering and prioritization
-   Output-token budgeting
-   Long-context trade-offs
-   KV-cache implications at architecture level
-   Context compression and summarization

### Context Budget

``` text
| System | Policy | History | Retrieved Docs | Tool Results | User Input | Output Budget |
```

The FDE should repeatedly ask:

> **What exactly does the model know at this point in the execution?**

## Use Case --- Enterprise Policy Assistant

An HR assistant receives 18 retrieved documents for a travel-policy
question. The correct policy is present, but the model answers using an
obsolete policy.

Possible diagnosis:

``` mermaid
flowchart TD
    A[Wrong Policy Answer] --> B{Was correct document retrieved?}
    B -->|No| C[Retrieval Problem]
    B -->|Yes| D{Was obsolete content also present?}
    D -->|Yes| E[Context Conflict / Ranking Problem]
    D -->|No| F[Context Utilization / Reasoning Problem]
```

**FDE lesson:** Adding more documents can reduce quality. Retrieval
success does not automatically imply answer success.

## Use Case --- Customer Support Copilot

The customer wants the last 12 months of conversation history inserted
into every request.

Participants decide:

-   What history actually matters?
-   What should become summarized state?
-   What should be retrieved dynamically?
-   What should never enter the context?
-   How should sensitive information be filtered?
-   How does context size affect latency and cost?

------------------------------------------------------------------------

# 3. Failure Mechanics --- Diagnosing AI Instead of Blaming "Hallucination"

## Objective

Create a systematic failure taxonomy that allows an FDE to identify the
**actual defective layer**.

``` mermaid
flowchart TD
    W[Wrong Business Outcome] --> K[Knowledge Failure]
    W --> C[Context Failure]
    W --> I[Instruction Failure]
    W --> R[Reasoning Failure]
    W --> E[Execution Failure]
    W --> V[Validation Failure]

    K --> K1[Parametric Knowledge]
    K --> K2[Retrieval Failure]

    C --> C1[Missing Context]
    C --> C2[Conflicting / Stale Context]

    R --> R1[Decomposition]
    R --> R2[Logic / Ambiguity]

    E --> E1[Wrong Tool]
    E --> E2[Wrong Arguments]
    E --> E3[API / Permission Failure]
```

## Failure Categories

### Knowledge Failure

The required fact is unavailable or incorrect.

### Retrieval Failure

The knowledge exists but the retrieval system fails to surface it.

### Context Failure

Correct information exists but is missing, diluted, stale,
contradictory, or poorly positioned.

### Instruction Failure

The model misinterprets or violates task constraints.

### Reasoning Failure

The correct evidence is present but the model reaches the wrong
conclusion.

### Execution Failure

Reasoning may be correct, but the wrong tool, parameters, API,
permission, or action is used.

### Validation Failure

An incorrect result is allowed to propagate because the system lacks
verification.

## Use Case --- Expense Policy

The assistant claims that ₹50,000 can be reimbursed when the policy
permits only ₹25,000.

Participants receive evidence incrementally:

**Round 1:** Wrong answer only.\
**Round 2:** Retrieval trace.\
**Round 3:** Correct policy was retrieved.\
**Round 4:** Prompt and competing context.\
**Round 5:** Model reasoning/tool trace.

The team must change its diagnosis as new evidence appears.

**Learning:** "Hallucination" is not a sufficient root-cause analysis.

## Use Case --- Production Incident Agent

An agent correctly diagnoses a database connection issue but restarts
the wrong service.

The model did not necessarily suffer a knowledge failure. The defect
could be:

-   entity resolution,
-   tool selection,
-   tool argument generation,
-   environment mapping,
-   authorization design,
-   missing pre-action validation.

This separates **model correctness** from **system correctness**.

------------------------------------------------------------------------

# 4. Model Adaptation Decisioning --- What Should We Actually Change?

## Objective

Enable architects to respond rigorously when customers say:

> "Can we train the model on our data?"

The first question should be:

> **What behaviour are we trying to change?**

``` mermaid
flowchart TD
    A[Customer AI Problem] --> B{Needs current/private knowledge?}
    B -->|Yes| C[RAG / Tool]
    B -->|No| D{Needs external action or live state?}
    D -->|Yes| E[Tool / API]
    D -->|No| F{Needs repeated behavioural adaptation?}
    F -->|Yes| G[Evaluate Fine-Tuning / PEFT]
    F -->|No| H{Is it a deterministic rule?}
    H -->|Yes| I[Code / Rules Engine]
    H -->|No| J[Prompt / Context Engineering]
```

## Intervention Ladder

1.  Improve instructions
2.  Improve context
3.  Improve retrieval
4.  Add deterministic validation
5.  Add tools/APIs
6.  Change model
7.  Fine-tune / PEFT
8.  Consider specialist/custom model

## What Each Intervention Changes

  Customer Need                          Likely Intervention
  -------------------------------------- ---------------------------------
  Current/private enterprise knowledge   RAG / Tools
  Company-specific instructions          Context / Prompting
  Live transactional information         Tool/API
  Deterministic business rule            Code / Rules
  Stable specialized behaviour           Fine-tuning candidate
  Better general reasoning               Model selection
  Domain-specific capability             Specialist model / adaptation
  Reliable business action               Tooling + validation + controls

## Use Case --- Legal Contract Review

Customer says:

> "We have 50,000 contracts. Fine-tune a model on all of them."

The FDE must determine whether the actual need is:

-   knowledge retrieval,
-   clause extraction,
-   organization-specific classification,
-   stylistic generation,
-   reasoning,
-   current contract lookup,
-   deterministic compliance checking.

Different problems imply different interventions.

## Use Case --- Manufacturing Maintenance

Technicians need current machine telemetry, maintenance manuals,
historical tickets and approved repair procedures.

Fine-tuning cannot supply live sensor state.

A likely architecture combines:

**retrieval + telemetry tools + deterministic safety constraints + model
reasoning.**

------------------------------------------------------------------------

# 5. Model Evaluation & Selection Engineering

## Objective

Move model selection away from vendor preference and public leaderboard
scores toward **workload-specific evidence**.

## Key Topics

-   Benchmark performance versus workload performance
-   Task-specific evaluation
-   Golden datasets
-   Representative test distributions
-   Human evaluation
-   LLM-as-judge
-   Pairwise evaluation
-   Rubrics
-   Structured-output evaluation
-   Tool-call accuracy
-   Failure-segment analysis
-   Quality / latency / cost trade-offs
-   Small versus frontier models
-   Model routing
-   Regression evaluation
-   Model/version change management

### Selection Principle

``` mermaid
flowchart LR
    A[Customer Workload] --> B[Representative Eval Set]
    B --> C[Candidate Models]
    C --> D[Quality]
    C --> E[Latency]
    C --> F[Cost]
    C --> G[Tool Reliability]
    C --> H[Safety / Constraints]
    D --> I[Production Decision]
    E --> I
    F --> I
    G --> I
    H --> I
```

## Use Case --- Insurance Claims Assistant

  Metric                 Model A   Model B   Model C   Model D
  -------------------- --------- --------- --------- ---------
  Task success               96%       92%       88%       83%
  P95 latency              8.2 s     3.4 s     1.8 s     0.9 s
  Cost / 1K tasks         ₹4,200    ₹1,700      ₹620      ₹210
  Tool-call accuracy         97%       96%       90%       81%

Customer constraints:

-   1.5 million requests/month
-   \<3 second target
-   high correctness required for consequential actions
-   most requests are routine
-   complex claims represent approximately 8% of traffic

The exercise deliberately has no obvious "best model."

A possible design is:

``` mermaid
flowchart TD
    A[Incoming Claim] --> B[Risk / Complexity Router]
    B -->|Routine| C[Efficient Model]
    B -->|Complex / High Risk| D[High-Capability Model]
    C --> E[Validation]
    D --> E
    E -->|Pass| F[Response / Action]
    E -->|Fail / Uncertain| G[Escalation]
```

**Learning:** Model selection may actually be **model portfolio
design**.

## Use Case --- Code Modernization

Compare candidate models using customer-specific tasks:

-   Java 8 → Java 21 migration
-   Spring framework modernization
-   unit-test generation
-   security remediation
-   explanation quality
-   compilation success
-   test pass rate

The most impressive conversational model may not produce the highest
**build-and-test success rate**.

------------------------------------------------------------------------

# 6. Model Economics & Production Behaviour

## Objective

Translate model mechanics into production economics and business
outcomes.

## Key Topics

-   Input versus output token economics
-   Time to first token (TTFT)
-   Generation latency
-   Context length impact
-   Caching
-   Batching
-   Quantization at decision level
-   Model routing
-   Retries
-   Human escalation
-   SLA implications
-   Cost per successful task
-   Cost of failure
-   Quality-cost-latency frontier

### Move Beyond Cost per Token

``` mermaid
flowchart LR
    A[Model Cost] --> B[Task Cost]
    B --> C[Retries]
    C --> D[Validation]
    D --> E[Human Escalation]
    E --> F[Cost per Successful Business Outcome]
```

A cheap model with poor success may be more expensive operationally than
a more capable model.

### Example

**Model A**

-   cost/task: ₹3.20
-   success: 96%
-   low escalation

**Model B**

-   cost/task: ₹0.90
-   success: 82%
-   retries: 12%
-   human escalation: 8%

The FDE evaluates **effective business cost**, not only inference price.

## Use Case --- Contact Centre

A cheaper model saves ₹12 lakh/month in inference cost but increases
human escalations by 7%.

Participants calculate whether the "optimization" actually creates value
after including:

-   agent handling time,
-   customer wait time,
-   repeat calls,
-   failed resolutions,
-   escalation cost.

## Use Case --- Document Processing at Scale

A customer processes millions of documents.

Participants evaluate:

-   large model for every page,
-   small model + confidence threshold,
-   deterministic OCR/extraction + LLM only for ambiguity,
-   model cascade,
-   caching repeated content,
-   batch processing.

The goal is **architecture-level unit economics**.

------------------------------------------------------------------------

# 7. Integrated FDE Model-Mechanics Case

## Scenario --- Enterprise Procurement Copilot

A global enterprise wants an AI system that can:

1.  answer procurement-policy questions,
2.  analyze supplier proposals,
3.  compare commercial terms,
4.  access current supplier information,
5.  recommend negotiation positions,
6.  draft communications,
7.  request approval for high-value actions.

The customer initially asks for:

> "One powerful enterprise model trained on all our procurement data."

### Stage 1 --- Behaviour

Determine which activities tolerate probabilistic behaviour and which
require deterministic controls.

### Stage 2 --- Context

Identify what belongs in:

-   system instructions,
-   retrieved policy,
-   supplier master data,
-   conversation state,
-   tool/API results,
-   approval state.

### Stage 3 --- Failure Analysis

Diagnose scenarios such as:

-   obsolete policy used,
-   wrong supplier identified,
-   correct data retrieved but incorrect recommendation produced,
-   correct recommendation but incorrect ERP action attempted.

### Stage 4 --- Intervention

For each defect choose among:

-   prompt/context change,
-   retrieval change,
-   deterministic rule,
-   tool/API,
-   model change,
-   fine-tuning.

### Stage 5 --- Evaluation

Build an evaluation suite covering:

-   policy-answer accuracy,
-   supplier-comparison quality,
-   tool-call correctness,
-   approval compliance,
-   recommendation quality,
-   structured-output validity.

### Stage 6 --- Economics

Compare:

-   frontier model everywhere,
-   smaller model everywhere,
-   routed multi-model architecture.

### Final Deliverable

Teams defend:

``` text
Customer Problem
      ↓
Behavioural Requirements
      ↓
Context Architecture
      ↓
Failure Controls
      ↓
Model / Intervention Decisions
      ↓
Evaluation Strategy
      ↓
Production Economics
```

------------------------------------------------------------------------

# 8. Additional Rapid-Fire FDE Use Cases

These can be used as discussion cards, breakout exercises, or trainer
prompts.

## Banking --- Credit Memo Assistant

The model produces an excellent credit summary but occasionally misses
risk covenants.

**Question:** Is this a model, context, retrieval, evaluation, or
workflow-control problem?

------------------------------------------------------------------------

## Healthcare --- Clinical Documentation

A model summarizes clinician notes accurately but occasionally
introduces unsupported facts.

**Question:** Where should probabilistic generation stop and
deterministic evidence linking begin?

------------------------------------------------------------------------

## Retail --- Product Support Agent

The strongest model meets quality requirements but violates the latency
SLA during peak traffic.

**Question:** Change model, route workloads, cache, shorten context, or
change the UX?

------------------------------------------------------------------------

## Software Engineering --- Legacy Modernization

The model generates convincing modernized code, but only 71% compiles
and 58% passes regression tests.

**Question:** What should the actual model evaluation metric be?

------------------------------------------------------------------------

## Telecom --- Network Incident Assistant

The model diagnoses incidents well but performs poorly when topology
information is stale.

**Question:** Does the model need fine-tuning, better context, or live
tools?

------------------------------------------------------------------------

## Insurance --- Claims Triage

A small model handles 90% of low-risk claims cheaply but performs poorly
on ambiguous cases.

**Question:** Can confidence/risk routing outperform choosing one larger
model for everything?

------------------------------------------------------------------------

# 9. Topics Explicitly De-emphasized

For this cohort, do **not** spend significant training time reteaching:

-   introduction to NLP
-   what tokens are
-   tokenization basics
-   embeddings basics
-   semantic similarity basics
-   Transformer history
-   detailed attention mathematics
-   basic vector database concepts
-   "What is RAG?"
-   generic prompt-engineering tips
-   basic LLM API invocation
-   introductory agent concepts

These concepts may be referenced when needed to explain behaviour, but
they are prerequisites rather than the curriculum.

------------------------------------------------------------------------

# 10. Recommended Training Experience

The module should not become a slide-heavy lecture.

A useful delivery mix is:

-   **Concept framing:** model mechanics translated into FDE decisions
-   **Failure diagnosis:** learners inspect traces/evidence and identify
    the defective layer
-   **Decision labs:** choose RAG, tool, prompt, model, rule,
    fine-tuning, or hybrid
-   **Model-selection exercises:** evaluate quality/latency/cost rather
    than brand names
-   **Customer cases:** defend decisions under business constraints
-   **Integrated case:** carry one enterprise problem across behaviour →
    context → failure → intervention → evaluation → economics

## The Core FDE-MM Mental Model

``` mermaid
flowchart TD
    A[How does the model behave?] --> B[Why does it fail?]
    B --> C{What should change?}
    C --> D[Context]
    C --> E[Retrieval]
    C --> F[Tools]
    C --> G[Rules / Validation]
    C --> H[Model]
    C --> I[Fine-Tuning]
    D --> J[How do we prove improvement?]
    E --> J
    F --> J
    G --> J
    H --> J
    I --> J
    J --> K[Which configuration goes to production?]
    K --> L[What does the decision cost the customer?]
```

------------------------------------------------------------------------

# Expected FDE Capability

At the end of this module, the participant should be able to enter a
customer conversation and answer:

1.  **Why is the model behaving this way?**
2.  **Where is the actual failure occurring?**
3.  **Does this problem require context, retrieval, tooling, rules,
    another model, or fine-tuning?**
4.  **How will we objectively prove that the proposed change improves
    the workload?**
5.  **Which model/configuration should go into production?**
6.  **What are the latency, reliability and economic consequences?**
7.  **How do I explain and defend that decision to the customer?**

That is the difference between merely **knowing model mechanics** and
using **model mechanics as an FDE value-creation capability**.
