# FDE-MM Knowledge Base --- Topic 4

## Model Adaptation Decisioning --- What Should We Actually Change?

### Purpose

Customers frequently jump from poor AI behaviour to "we need to
train/fine-tune our own model." The FDE must translate the observed
defect into the correct intervention: **instructions, context,
retrieval, tools, deterministic logic, model change, or adaptation.**

------------------------------------------------------------------------

## 4.1 Prompt and Instruction Improvement

Prompt changes are appropriate when the model has the required
capability and information but the task, constraints, format, or
decision criteria are unclear. Good prompting can improve behaviour
without changing model weights or architecture. It should not be used to
compensate indefinitely for missing data or fundamental capability
limits.

**FDE lens:** *Use prompt changes to clarify the job---not to pretend
the system has knowledge it does not possess.*

------------------------------------------------------------------------

## 4.2 Context Engineering

When the model needs task-specific policies, examples, history, state,
or constraints, the intervention may be better context rather than model
adaptation. Context can be changed quickly and remains inspectable at
runtime. It is especially useful when information differs by customer,
user, session, or workflow stage.

**FDE lens:** *If the behaviour should change when runtime information
changes, context is usually part of the answer.*

------------------------------------------------------------------------

## 4.3 Retrieval-Augmented Generation

RAG is appropriate when the model needs access to private, current, or
extensive reference knowledge that can be retrieved when needed. It
keeps source knowledge external to model weights and supports provenance
and updates. RAG is less suitable for live transactional state that
should come directly from an authoritative system.

**FDE lens:** *Use retrieval when the problem is "find and use the right
knowledge," not simply because documents exist.*

------------------------------------------------------------------------

## 4.4 Tools and APIs

Tools allow the model to obtain live information or perform actions in
enterprise systems such as ERP, CRM, databases, observability platforms,
or workflow engines. They are essential when correctness depends on
current state rather than static knowledge. Tool design must include
authorization, argument validation, idempotency, and failure handling.

**FDE lens:** *If the answer changes with the state of the business, ask
whether a tool should be the source of truth.*

------------------------------------------------------------------------

## 4.5 Deterministic Rules and Validation

Business rules, calculations, thresholds, eligibility checks, and safety
constraints often belong in deterministic software rather than model
weights. LLMs can interpret unstructured information while code enforces
exact rules. Hybrid architecture frequently provides better reliability
than trying to make the model behave deterministically through prompting
alone.

**FDE lens:** *Use AI for ambiguity; use code for invariants.*

------------------------------------------------------------------------

## 4.6 Model Change

A workload may exceed a model's reasoning, coding, multilingual,
multimodal, context, or tool-use capability. Switching models can be
more effective than adding increasingly complex prompts and
orchestration. The decision should be supported by workload-specific
evaluation rather than reputation or public benchmarks.

**FDE lens:** *Recognize when architecture tuning is fighting a
capability ceiling.*

------------------------------------------------------------------------

## 4.7 Fine-Tuning

Fine-tuning changes model behaviour by adapting weights using
representative examples, and can be useful for stable, repeated task
patterns, style, classification, or specialized behaviour. It is not a
good mechanism for continuously changing facts or live enterprise state.
It also introduces dataset, evaluation, versioning, and lifecycle
responsibilities.

**FDE lens:** *Fine-tune behaviour; retrieve changing knowledge.*

------------------------------------------------------------------------

## 4.8 PEFT / LoRA at Decision Level

Parameter-efficient techniques such as LoRA adapt a subset or low-rank
representation of model parameters rather than retraining the entire
model. FDEs need not derive the mathematics, but should understand the
operational proposition: lower adaptation cost and smaller training
footprint with new deployment/versioning considerations. Suitability
still depends on evidence from evals.

**FDE lens:** *Cheaper adaptation does not remove the need to prove that
adaptation is the correct intervention.*

------------------------------------------------------------------------

## 4.9 Specialist or Custom Models

Some workloads may justify domain-specialized, smaller, locally hosted,
or custom models because of privacy, latency, language, economics, or
specialized capability. This is a strategic architecture decision with
operational consequences for hosting, evaluation, updates, security, and
support. "Own model" should never be treated as an automatic maturity
upgrade.

**FDE lens:** *Choose specialization when the workload economics and
capability evidence justify the lifecycle burden.*

------------------------------------------------------------------------

## 4.10 Intervention Sequencing

Multiple interventions may be required, but they should be tested
incrementally so the team knows what actually improved the outcome. A
useful sequence is instructions → context → retrieval/tools → validation
→ model change → fine-tuning, adjusted for the problem. This reduces
unnecessary complexity and preserves causal evidence.

**FDE lens:** *Select the smallest intervention that fixes the measured
defect.*

------------------------------------------------------------------------

## Use Case --- Legal Contract Review

A customer asks to fine-tune on 50,000 contracts. The FDE decomposes the
requirement into contract retrieval, clause extraction, company-specific
classification, compliance rules, current contract lookup, and drafting
behaviour---then chooses different interventions for each.

## Use Case --- Manufacturing Maintenance

Technicians need manuals, historical tickets, live telemetry, and
approved repair procedures. A robust design may combine RAG for manuals,
tools for sensor state, deterministic safety rules, and model reasoning
rather than fine-tuning everything into one model.

## Decision Flow

``` mermaid
flowchart TD
    A[Observed Problem] --> B{Missing current/private knowledge?}
    B -->|Yes| C[RAG]
    B -->|No| D{Needs live state/action?}
    D -->|Yes| E[Tool / API]
    D -->|No| F{Exact invariant or rule?}
    F -->|Yes| G[Code / Validation]
    F -->|No| H{Stable repeated behaviour gap?}
    H -->|Yes| I[Evaluate Fine-Tuning / PEFT]
    H -->|No| J{Capability ceiling?}
    J -->|Yes| K[Different / Specialist Model]
    J -->|No| L[Prompt / Context]
```

## Trainer Takeaway

> **The FDE's job is not to advocate a technique. It is to identify what
> must change in the system and choose the least complex intervention
> that measurably fixes it.**
