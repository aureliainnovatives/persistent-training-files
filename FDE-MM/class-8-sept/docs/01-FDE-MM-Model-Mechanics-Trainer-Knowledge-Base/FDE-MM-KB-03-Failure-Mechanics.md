# FDE-MM Knowledge Base --- Topic 3

## Failure Mechanics --- Diagnosing AI Instead of Blaming "Hallucination"

### Purpose

"Hallucination" is often used as a catch-all label for any incorrect AI
outcome. An FDE needs a more precise failure taxonomy so that the team
fixes the **defective layer** rather than repeatedly changing prompts or
models without evidence.

------------------------------------------------------------------------

## 3.1 Knowledge Failure

A knowledge failure occurs when the model does not possess the factual
or domain capability required for the task and the missing information
is not supplied at runtime. The remedy may be retrieval, tools, a
different model, or adaptation depending on the requirement. Prompt
refinement alone cannot reliably manufacture missing authoritative
knowledge.

**FDE lens:** *First establish whether the required knowledge was
available anywhere in the execution path.*

------------------------------------------------------------------------

## 3.2 Retrieval Failure

The authoritative information exists in the enterprise knowledge source
but is not retrieved, is ranked too low, or is retrieved at the wrong
granularity. Chunking, metadata, query transformation, filters,
reranking, and indexing may all be responsible. The model cannot use
evidence that never reaches its context.

**FDE lens:** *Before blaming generation, verify retrieval recall and
relevance.*

------------------------------------------------------------------------

## 3.3 Context Failure

Correct evidence may have been retrieved but become ineffective because
it is truncated, buried, contradicted, stale, poorly ordered, or
overwhelmed by unrelated content. Context failures sit between retrieval
and reasoning and are easy to misdiagnose. Trace the exact final context
delivered to the model.

**FDE lens:** *"Retrieved successfully" does not mean "presented
effectively."*

------------------------------------------------------------------------

## 3.4 Instruction Failure

The model may misunderstand task requirements, violate constraints,
prioritize another instruction, or interpret ambiguous directions
differently from the designer. This can originate from prompt design,
conflicting policies, examples, user instructions, or injected content.
FDEs should inspect instruction hierarchy and ambiguity before changing
models.

**FDE lens:** *Ask which instruction the model appears to have followed,
not merely which one it violated.*

------------------------------------------------------------------------

## 3.5 Reasoning Failure

In a reasoning failure, the necessary evidence is available but the
model reaches an incorrect conclusion, decomposition, comparison, or
decision. This is different from missing knowledge and may require
better task decomposition, validation, a stronger model, or
deterministic computation. Evaluation should isolate reasoning from
retrieval.

**FDE lens:** *Correct evidence + wrong conclusion is a different defect
from missing evidence.*

------------------------------------------------------------------------

## 3.6 Execution Failure

An agent or AI workflow may reason correctly but select the wrong tool,
construct incorrect arguments, call the wrong environment, encounter an
API failure, or lack permission. The resulting business outcome is wrong
even though the language model's analysis may be sound. Tool traces are
therefore essential production evidence.

**FDE lens:** *Model correctness does not guarantee system correctness.*

------------------------------------------------------------------------

## 3.7 Validation Failure

An upstream component may produce an incorrect or uncertain result, but
the architecture fails to detect it before consequential use. Missing
schema validation, business-rule checks, confidence gates,
reconciliation, or human approval can turn a recoverable model error
into a business incident. Validation is a system responsibility.

**FDE lens:** *The important question is not only "Can the model fail?"
but "Can failure escape?"*

------------------------------------------------------------------------

## 3.8 Entity and Grounding Failure

The model may correctly understand a task but associate it with the
wrong customer, supplier, service, account, environment, or document.
Similar names and ambiguous references make these failures common in
enterprise workflows. Stable identifiers and explicit grounding should
be preferred over free-text entity assumptions.

**FDE lens:** *Before executing an action, verify that the model is
acting on the right thing.*

------------------------------------------------------------------------

## 3.9 Temporal Failure

The model may use information that was once correct but is no longer
valid, such as pricing, inventory, policy versions, deployment state, or
customer status. Temporal correctness is especially important when
retrieval indexes lag behind source systems. Live-state questions often
belong behind tools rather than static knowledge retrieval.

**FDE lens:** *A fact can be accurate historically and still be wrong
operationally.*

------------------------------------------------------------------------

## 3.10 Compound and Cascading Failure

Real production incidents often cross layers: poor retrieval causes weak
reasoning, which produces a bad tool argument, which then passes because
validation is absent. Root-cause analysis should therefore reconstruct
the full execution trajectory rather than stop at the first visible
symptom. This is particularly important for agents and long-running
workflows.

**FDE lens:** *Trace the chain of causality, not just the final wrong
answer.*

------------------------------------------------------------------------

## Use Case --- Expense Policy

The assistant approves ₹50,000 while policy permits only ₹25,000.
Learners progressively receive the retrieval trace, final context,
instructions, model output, and workflow validation logic, and must
update their diagnosis as evidence changes.

## Use Case --- Production Incident Agent

An agent correctly diagnoses a database connectivity problem but
restarts the wrong service. The FDE investigates entity resolution, tool
selection, arguments, environment mapping, authorization, and pre-action
validation rather than labeling the incident a hallucination.

## Failure Diagnostic

``` mermaid
flowchart TD
    A[Wrong Business Outcome] --> B{Was authoritative evidence available?}
    B -->|No| C[Knowledge / Retrieval]
    B -->|Yes| D{Was it correctly represented in context?}
    D -->|No| E[Context Failure]
    D -->|Yes| F{Was conclusion correct?}
    F -->|No| G[Instruction / Reasoning]
    F -->|Yes| H{Was intended action executed correctly?}
    H -->|No| I[Execution Failure]
    H -->|Yes| J{Should system have blocked outcome?}
    J -->|Yes| K[Validation / Governance Failure]
```

## Trainer Takeaway

> **A wrong answer is a symptom. FDE value comes from locating the
> failing layer and selecting the smallest effective intervention.**
