# FDE-MM Knowledge Base --- Topic 6

## Model Economics & Production Behaviour

### Purpose

Token pricing is only the beginning of AI economics. An FDE must connect
model behaviour to **latency, retries, infrastructure, human escalation,
failure cost, SLA performance, and ultimately cost per successful
business outcome.**

------------------------------------------------------------------------

## 6.1 Input versus Output Token Economics

Providers commonly price input and generated tokens differently, and
output generation can be especially expensive and latency-sensitive.
Workloads with huge contexts but short answers behave economically
differently from short prompts that generate long reports. FDEs should
profile the actual token shape of the customer workload.

**FDE lens:** *"Cost per million tokens" is meaningless until you know
how the workload consumes them.*

------------------------------------------------------------------------

## 6.2 Time to First Token (TTFT)

TTFT measures how long the user waits before generation begins and is
strongly felt in interactive applications. Large prompts, model size,
queueing, serving infrastructure, and cache behaviour can influence it.
A system can have acceptable total completion time yet still feel slow
if TTFT is poor.

**FDE lens:** *User-perceived latency starts before the first word
appears.*

------------------------------------------------------------------------

## 6.3 Generation Latency

After the first token, generation speed determines how quickly the
response completes. Long outputs, reasoning-heavy tasks, and slower
models can make synchronous workflows impractical. FDEs should decide
whether the workload needs streaming, shorter outputs, asynchronous
execution, or a different model.

**FDE lens:** *Do not optimize only model intelligence; optimize the
interaction contract.*

------------------------------------------------------------------------

## 6.4 Context-Length Impact

Larger prompts increase processing work, can increase cost and latency,
and may introduce irrelevant information. Context size should therefore
be treated as an operational metric rather than merely a model
capability. Retrieval, compression, caching, and prompt redesign can
reduce unnecessary context.

**FDE lens:** *Every token entering production should have a reason to
be there.*

------------------------------------------------------------------------

## 6.5 Caching

Caching can avoid repeated computation or repeated model calls when
instructions, prefixes, retrieved results, or responses recur. The
design must consider freshness, privacy, cache keys, invalidation, and
whether the provider/runtime supports prompt-prefix caching. Poor
caching can return stale or cross-context information.

**FDE lens:** *Cache only what is safe to reuse and define when it stops
being valid.*

------------------------------------------------------------------------

## 6.6 Batching

Batch processing can improve throughput and economics for
non-interactive workloads such as document classification, enrichment,
evaluation, or offline analysis. It trades immediate responsiveness for
resource efficiency. FDEs should separate workloads that truly need
synchronous inference from those that can be processed asynchronously.

**FDE lens:** *Not every AI request deserves real-time serving.*

------------------------------------------------------------------------

## 6.7 Quantization at Decision Level

Quantization reduces numerical precision to lower model memory and
compute requirements, often enabling cheaper or faster inference with
possible quality trade-offs. FDEs need not implement quantization
kernels, but should understand why deployment format can affect cost,
latency, and model quality. It is most relevant for self-hosted or
controlled serving environments.

**FDE lens:** *Serving optimization is useful only if workload evals
show the quality trade-off is acceptable.*

------------------------------------------------------------------------

## 6.8 Model Routing

Routing allows routine tasks to use economical models while difficult or
high-risk cases use stronger models. This can dramatically change unit
economics without forcing the entire workload onto the cheapest or most
expensive option. Routing criteria and fallback behaviour must
themselves be observable and evaluated.

**FDE lens:** *Spend model capability in proportion to task difficulty
and risk.*

------------------------------------------------------------------------

## 6.9 Retries

Retries improve resilience but can silently multiply inference cost and
latency when models produce invalid output, tools fail, or validation
rejects responses. A cheap model with frequent retries may become more
expensive than a reliable model. Retry rates should be visible in both
reliability and economic dashboards.

**FDE lens:** *Measure the cost of getting a successful answer, not the
price of the first attempt.*

------------------------------------------------------------------------

## 6.10 Human Escalation

Human review is sometimes the correct safety mechanism, but it
introduces labor cost, queueing, and turnaround time. An AI design that
saves inference cost while increasing manual escalations may destroy the
business case. Escalation rate and handling time should therefore be
included in AI unit economics.

**FDE lens:** *Human-in-the-loop is both a risk control and an economic
variable.*

------------------------------------------------------------------------

## 6.11 SLA Implications

Model latency, rate limits, retries, tool dependencies, and provider
availability all affect the end-to-end SLA. The AI component should not
be evaluated independently from the workflow surrounding it. FDEs should
translate model metrics into customer-facing response-time and
availability commitments.

**FDE lens:** *The customer experiences the system SLA, not the model
benchmark.*

------------------------------------------------------------------------

## 6.12 Cost per Successful Task

Cost per request ignores whether the request actually achieved the
desired business result. A more useful metric combines inference,
retrieval, tools, retries, validation, infrastructure, and escalation
and divides them by successful outcomes. This aligns technical
optimization with business value.

**FDE lens:** *Optimize ₹/successful outcome, not merely ₹/API call.*

------------------------------------------------------------------------

## 6.13 Cost of Failure

Incorrect AI decisions can create refunds, compliance incidents,
operational rework, lost customers, downtime, or human investigation
costs. High-risk workloads may justify more expensive models, stronger
validation, or mandatory approval because failure economics dominate
inference economics. Cost modeling should include expected failure
impact.

**FDE lens:** *The cheapest model can be the most expensive architecture
when mistakes are costly.*

------------------------------------------------------------------------

## 6.14 Quality--Cost--Latency Frontier

Improving one dimension often affects the others: stronger models may
improve quality but increase cost and latency, while smaller models may
improve speed and economics but reduce robustness. The FDE's job is to
find an acceptable operating point for the customer's actual
constraints. There may be multiple operating tiers rather than one
global setting.

**FDE lens:** *Optimization is a trade-space, not a single number.*

------------------------------------------------------------------------

## Use Case --- Contact Centre

A cheaper model reduces inference spend by ₹12 lakh/month but raises
human escalations by 7%. Learners include agent handling time, customer
wait, repeat calls, failed resolutions, and churn risk before declaring
the change an optimization.

## Use Case --- Document Processing at Scale

A customer processes millions of documents. Teams compare frontier-model
processing for every page with deterministic extraction, small-model
classification, confidence routing, caching, batching, and escalation
for ambiguous cases.

## Economics Flow

``` mermaid
flowchart LR
    A[Inference Cost] --> B[Task Cost]
    B --> C[Retries]
    C --> D[Tool / Retrieval Cost]
    D --> E[Validation]
    E --> F[Human Escalation]
    F --> G[Failure Impact]
    G --> H[Cost per Successful Outcome]
```

## Trainer Takeaway

> **AI economics becomes useful to an FDE when technical metrics are
> translated into customer unit economics, SLA consequences, and the
> cost of successful outcomes.**
