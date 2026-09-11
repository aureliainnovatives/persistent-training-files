# FDE-MM Knowledge Base --- Topic 2

## Context Engineering --- Designing the Model's Working Environment

### Purpose

Context engineering is the discipline of controlling **what information,
instructions, state, and evidence the model sees at inference time**.
For an FDE, the central debugging question is: **"What exactly did the
model know at this point in execution?"**

------------------------------------------------------------------------

## 2.1 Context Window versus Memory

A context window is the finite information supplied to a model for a
particular inference; it is not persistent memory by itself. Application
memory is an external mechanism that decides what prior information
should be retained, retrieved, summarized, or reintroduced. An FDE must
distinguish model capacity from the application's state-management
strategy.

**FDE lens:** *A large context window does not eliminate the need to
engineer memory.*

------------------------------------------------------------------------

## 2.2 System, User, Retrieved, Tool and Conversational Context

The effective model input can contain system policies, user
instructions, retrieved documents, tool results, examples, and
conversation history. Each source has a different authority, freshness,
and reliability profile. Production debugging therefore requires tracing
the complete assembled context rather than inspecting only the visible
user prompt.

**FDE lens:** *The prompt the customer sees is only one component of the
prompt the model effectively receives.*

------------------------------------------------------------------------

## 2.3 Effective Context versus Available Enterprise Information

An enterprise may possess the correct information in SharePoint, a
database, CRM, or policy repository, but the model can only act on
information actually made available during execution. "The data exists"
and "the model had the data" are fundamentally different claims. FDEs
must trace the path from source system to effective context.

**FDE lens:** *Debug information flow, not merely information
existence.*

------------------------------------------------------------------------

## 2.4 Context Budgeting

Every instruction, retrieved passage, example, tool result, conversation
turn, and expected output competes for finite context capacity and
attention. Context budgeting deliberately allocates space according to
business importance rather than filling the window indiscriminately. It
also influences latency and inference cost.

**FDE lens:** *Context is a production resource and should be budgeted
like compute or memory.*

------------------------------------------------------------------------

## 2.5 Context Competition

Multiple pieces of relevant-looking information may compete for
influence, especially when policies, examples, retrieved documents, and
conversation history disagree. A model may follow a lower-value signal
even though the correct evidence is technically present. FDEs should
reduce ambiguity and establish clear authority between context sources.

**FDE lens:** *Presence of correct information does not guarantee
dominance of correct information.*

------------------------------------------------------------------------

## 2.6 Relevance versus Context Volume

Supplying more documents can reduce performance when irrelevant or
weakly relevant material dilutes the evidence needed for the task.
Retrieval quality should therefore optimize useful evidence, not simply
maximize token volume. Smaller, cleaner context can outperform a much
larger context.

**FDE lens:** *More context is not automatically more intelligence.*

------------------------------------------------------------------------

## 2.7 Lost-in-the-Middle Effects

Models can use long contexts impressively, but information placement and
surrounding noise can still influence how reliably evidence is used.
Critical information buried among large amounts of content may receive
less effective attention than expected. Architects should therefore test
long-context behaviour on the actual workload instead of assuming
advertised context capacity equals uniform utilization.

**FDE lens:** *"It fits in the window" is not the same as "the model
will reliably use it."*

------------------------------------------------------------------------

## 2.8 Conflicting Context

Enterprise systems commonly contain duplicate, outdated, or
contradictory policies and records. If conflicting evidence reaches the
model without authority metadata, versioning, or precedence rules, the
model is forced to resolve a governance problem probabilistically. The
architecture should resolve known conflicts before generation whenever
possible.

**FDE lens:** *Do not delegate enterprise source-of-truth governance to
token prediction.*

------------------------------------------------------------------------

## 2.9 Stale Context

A response can be linguistically perfect and still be operationally
wrong because its context is outdated. FDEs should classify information
by freshness requirements and decide whether it belongs in static
retrieval, refreshed indexes, caches, or live APIs. Freshness should
become an explicit NFR for time-sensitive AI workloads.

**FDE lens:** *Ask not only "Is this information correct?" but also
"Correct as of when?"*

------------------------------------------------------------------------

## 2.10 Context Poisoning

Retrieved documents, tool outputs, user-provided content, or external
pages may contain malicious or misleading instructions that attempt to
influence model behaviour. Context should therefore be treated as
untrusted data unless explicitly governed. Isolation, provenance,
filtering, instruction hierarchy, and tool authorization become
architectural controls.

**FDE lens:** *Retrieved text is evidence, not automatically trusted
instruction.*

------------------------------------------------------------------------

## 2.11 Ordering and Prioritization

The way context is assembled can affect model behaviour: authoritative
policies, task instructions, examples, retrieved evidence, and user
content should have deliberate structure and precedence. Good context
engineering makes the model's operating environment easier to interpret.
This is particularly important when multiple teams independently
contribute prompts or middleware.

**FDE lens:** *Context assembly is architecture, not string
concatenation.*

------------------------------------------------------------------------

## 2.12 Output-Token Budgeting

Input context and generated output share practical resource constraints,
and long expected responses can increase latency and cost. An FDE should
define how much output the business task actually requires and constrain
generation accordingly. Structured summaries, bounded explanations, or
staged generation can be preferable to unrestricted output.

**FDE lens:** *Do not spend generation tokens that create no business
value.*

------------------------------------------------------------------------

## 2.13 Long-Context Trade-offs

Large context windows can simplify some retrieval and document-analysis
workloads, but they can also increase latency, cost, irrelevant
evidence, and troubleshooting complexity. The decision should compare
long-context prompting with retrieval, summarization, hierarchical
processing, and tools. There is no universal "put everything in context"
architecture.

**FDE lens:** *Long context is an option in the design space, not a
replacement for information architecture.*

------------------------------------------------------------------------

## 2.14 KV-Cache Implications at Architecture Level

During generation, models reuse previously computed representations of
prior tokens through the key-value cache, which affects latency and
memory consumption. FDEs do not need kernel-level implementation detail,
but should understand why repeated prefixes, long contexts, and caching
strategies can influence serving economics. This connects prompt design
to infrastructure behaviour.

**FDE lens:** *Prompt structure can have runtime consequences beyond
token count.*

------------------------------------------------------------------------

## 2.15 Context Compression and Summarization

Long conversations and agent histories often need to be compressed into
smaller representations to remain useful and economical. Summarization
saves context but can discard details, introduce distortion, or erase
provenance. FDEs should decide what must remain verbatim, what can be
summarized, and what can be retrieved on demand.

**FDE lens:** *Compression is lossy---decide deliberately what the
system is allowed to forget.*

------------------------------------------------------------------------

## Use Case --- Enterprise Travel Policy Assistant

An HR assistant retrieves 18 documents and answers using an obsolete
travel policy even though the current policy was also retrieved.
Participants diagnose whether the failure lies in retrieval, ranking,
conflicting context, authority metadata, or context utilization.

``` mermaid
flowchart TD
    A[Wrong Policy Answer] --> B{Was current policy retrieved?}
    B -->|No| C[Retrieval Failure]
    B -->|Yes| D{Was obsolete policy also present?}
    D -->|Yes| E[Conflict / Ranking / Authority Problem]
    D -->|No| F[Context Utilization / Reasoning]
```

## Topic 2 Mental Model

``` mermaid
flowchart LR
    A[Enterprise Information] --> B[Select]
    B --> C[Prioritize]
    C --> D[Assemble Context]
    D --> E[Model Behaviour]
    E --> F[Trace & Evaluate]
    F --> B
```

## Trainer Takeaway

> **Context engineering determines the model's working reality. An FDE
> must control what enters that reality, what receives priority, and how
> it is traced.**
