# FDE-MM Knowledge Base --- Topic 1

## From Model Mechanics to Model Behaviour

### Purpose

The objective is **not to revisit Transformer internals**, but to
connect model mechanics to what an FDE actually observes in a customer
environment. For every concept, the learner should be able to answer:

> **What behaviour does this create, why does it matter, and what
> architectural decision follows?**

------------------------------------------------------------------------

## 1.1 Probabilistic Generation and Output Variability

An LLM does not retrieve a fixed answer; it predicts a probability
distribution over possible next tokens and generates from that
distribution. Consequently, semantically identical inputs can produce
different wording, reasoning paths, or even conclusions. For an FDE, the
critical question is whether the business process can tolerate this
variability---or requires validation, constraints, or deterministic
logic.

**FDE lens:** *Where is variability acceptable, and where does it become
business risk?*

------------------------------------------------------------------------

## 1.2 Autoregressive Generation and Error Propagation

LLMs generate output sequentially, with every newly generated token
becoming part of the context for subsequent generation. An incorrect
assumption early in a response can therefore influence everything
generated afterward, creating a cascading failure. This becomes
particularly important in long reasoning chains, code generation,
planning, and multi-step agent workflows.

**FDE lens:** *How far can an early model mistake propagate before the
system detects it?*

------------------------------------------------------------------------

## 1.3 Temperature, Top-p and Decoding at an Architectural Level

Temperature and top-p influence how the model selects among probable
next tokens: tighter decoding generally produces more consistent
outputs, while broader sampling increases variation. These settings
should not simply be treated as API tuning parameters; they should
reflect the workload's tolerance for creativity and uncertainty.
Contract extraction and code transformation require a very different
decoding strategy from marketing ideation.

**FDE lens:** *Decoding configuration should follow the business
behaviour required---not developer preference.*

------------------------------------------------------------------------

## 1.4 Deterministic versus Probabilistic Workloads

Some enterprise tasks tolerate interpretation---summarization,
recommendation, classification---while others require exact execution,
such as financial calculations, authorization checks, or compliance
thresholds. An FDE should identify which parts of a workflow genuinely
benefit from probabilistic intelligence and which should remain
deterministic. Strong AI architectures frequently combine LLM reasoning
with rules, code, schemas, validators, and approval gates.

**FDE lens:** *Don't ask, "Can the LLM do this?" Ask, "Should the LLM be
allowed to decide this?"*

------------------------------------------------------------------------

## 1.5 Instruction Following and Competing Instructions

A model may simultaneously receive system instructions, application
policies, user requests, retrieved documents, examples, conversation
history, and tool responses. These inputs can conflict, be ambiguous, or
unintentionally influence behaviour, even when each component appears
reasonable independently. FDE debugging therefore requires inspecting
the **complete effective context**, not merely the user's prompt.

**FDE lens:** *When the model disobeys an instruction, first determine
what other instruction or context it was attempting to satisfy.*

------------------------------------------------------------------------

## 1.6 Parametric Knowledge versus Contextual Knowledge

**Parametric knowledge** is information and capability encoded into the
model during training; **contextual knowledge** is information supplied
at inference time through prompts, documents, history, or application
state. This distinction matters because changing the prompt cannot
reliably add broad model capability, while retraining is unnecessary
when the requirement is simply to provide current enterprise
information. The FDE must diagnose which type of knowledge is actually
missing.

**FDE lens:** *Does the model need to become different, or does it
simply need better information at runtime?*

------------------------------------------------------------------------

## 1.7 Retrieved Knowledge versus Tool-Obtained Knowledge

Retrieval usually supplies relatively static knowledge---policies,
manuals, contracts, documentation---while tools can obtain live or
transactional state from APIs, databases, ERP, CRM, telemetry, and other
systems. A supplier policy may belong in RAG, while the supplier's
current outstanding balance should come from an authoritative system.
Confusing these mechanisms creates stale, unreliable enterprise AI
systems.

**FDE lens:** *If the answer can change between two requests, ask
whether retrieval is really the correct source.*

------------------------------------------------------------------------

## 1.8 Structured-Output Reliability

Enterprise applications frequently need JSON, schemas, classifications,
function arguments, SQL, or other machine-consumable output rather than
natural-language prose. A response can be semantically correct but
operationally useless if it violates the required schema, omits
mandatory fields, or invents enum values. Structured generation should
therefore be combined with schema enforcement, validation, retries, and
business-rule checks where necessary.

**FDE lens:** *"The answer looks correct" is different from "the
downstream system can safely execute it."*

------------------------------------------------------------------------

## 1.9 Why Identical-Looking Requests Can Produce Different Outcomes

Two requests that appear identical to a user may reach the model with
different conversation histories, retrieved documents, system
instructions, tool states, model versions, routing decisions, or
decoding settings. Even genuinely identical effective inputs can still
exhibit variability because generation may be stochastic. Production
troubleshooting therefore requires tracing the **entire inference
environment**, not merely comparing visible prompts.

**FDE lens:** *Reproducibility starts by asking whether the two
executions were actually identical.*

------------------------------------------------------------------------

## 1.10 Model Capability Boundaries

Models differ not only in benchmark scores but in reasoning depth,
instruction following, multilingual capability, tool use, context
handling, coding ability, multimodality, latency, and reliability under
complex tasks. Increasing prompt complexity cannot indefinitely
compensate for an underlying capability limitation. An FDE must
recognize when to improve context or orchestration---and when the
workload genuinely requires a different model or system design.

**FDE lens:** *Know when you are debugging the application and when you
are fighting the capability ceiling of the model.*

------------------------------------------------------------------------

## Topic 1 Mental Model

``` mermaid
flowchart LR
    A[Model Mechanics] --> B[Observable Behaviour]
    B --> C[Business Consequence]
    C --> D{Acceptable?}
    D -->|Yes| E[Use Model Behaviour]
    D -->|No| F[Engineer Controls]
    F --> G[Context]
    F --> H[Validation]
    F --> I[Deterministic Logic]
    F --> J[Human Gate]
    F --> K[Different Model]
```

## Trainer Takeaway

> **Model mechanics matter to an FDE when they help explain, predict,
> constrain, or exploit model behaviour in a real customer system.**

During delivery, continually connect the mechanics back to three
questions:

1.  **What behaviour will the customer observe?**
2.  **What business or production risk does that behaviour create?**
3.  **What architectural control or decision should the FDE make because
    of it?**
