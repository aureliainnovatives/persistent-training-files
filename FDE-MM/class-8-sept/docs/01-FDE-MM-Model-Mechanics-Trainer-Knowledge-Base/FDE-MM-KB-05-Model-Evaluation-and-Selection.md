# FDE-MM Knowledge Base --- Topic 5

## Model Evaluation & Selection Engineering

### Purpose

Model selection should not be driven by brand, leaderboard position, or
a single generic benchmark. An FDE builds **representative workload
evidence** and chooses the model or model portfolio that best satisfies
quality, latency, reliability, safety, and economic constraints.

------------------------------------------------------------------------

## 5.1 Benchmark Performance versus Workload Performance

Public benchmarks measure specific capabilities under controlled
conditions; customer workloads contain unique terminology, data
distributions, instructions, integrations, and failure costs. A high
benchmark score is useful evidence but not proof of production
suitability. FDEs should treat benchmarks as screening signals and
workload evals as decision evidence.

**FDE lens:** *The customer's workload is the benchmark that ultimately
matters.*

------------------------------------------------------------------------

## 5.2 Task-Specific Evaluation

Evaluation should measure the actual business task: extraction accuracy,
policy correctness, code compilation, tool execution, resolution
success, or decision quality. Generic "response quality" often hides the
failure mode that matters operationally. Metrics should be derived from
intended business behaviour and risk.

**FDE lens:** *Evaluate what the system is paid to accomplish.*

------------------------------------------------------------------------

## 5.3 Golden Datasets

A golden dataset contains representative, reviewed examples with
expected outcomes or evaluation criteria. It provides a stable basis for
comparing prompts, models, retrieval strategies, and releases. The
dataset should include normal cases, edge cases, ambiguous cases, and
high-risk failures---not only easy demonstrations.

**FDE lens:** *Without a stable eval set, model improvement becomes
anecdotal.*

------------------------------------------------------------------------

## 5.4 Representative Test Distributions

A test set can produce misleading results if it does not resemble
production traffic. FDEs should segment workloads by language,
complexity, customer type, document class, risk, or other meaningful
dimensions. Aggregate accuracy can conceal severe failure in a small but
consequential segment.

**FDE lens:** *Measure performance where the business actually operates,
including the tails.*

------------------------------------------------------------------------

## 5.5 Human Evaluation

Humans remain important when quality depends on domain judgment,
usefulness, tone, nuance, or business acceptability that cannot be fully
captured automatically. Human evaluation needs explicit rubrics and
calibrated reviewers to reduce inconsistency. It is expensive, so it
should be targeted where human judgment adds real signal.

**FDE lens:** *Human evaluation is valuable when expertise---not merely
preference---is required.*

------------------------------------------------------------------------

## 5.6 LLM-as-Judge

A capable model can evaluate outputs against a rubric, reference, or
pair of alternatives at much larger scale than human review. However,
judge models can have bias, positional effects, and blind spots, so
their judgments should be calibrated against trusted human examples.
They are an evaluation instrument, not an unquestionable oracle.

**FDE lens:** *Evaluate the evaluator before trusting automated
evaluation.*

------------------------------------------------------------------------

## 5.7 Pairwise Evaluation

Instead of assigning an absolute score, pairwise evaluation asks which
of two candidate outputs better satisfies defined criteria. This can
make comparative model or prompt testing easier and more stable for
subjective tasks. It is especially useful when selecting between two
production candidates.

**FDE lens:** *When absolute quality is hard to score, ask which
candidate wins and why.*

------------------------------------------------------------------------

## 5.8 Evaluation Rubrics

Rubrics convert vague expectations such as "good answer" into explicit
criteria like correctness, completeness, grounding, policy compliance,
actionability, and tone. A good rubric mirrors customer priorities and
assigns greater importance to consequential failures. Rubrics also
improve consistency across human and automated judges.

**FDE lens:** *If success cannot be described clearly, it cannot be
evaluated reliably.*

------------------------------------------------------------------------

## 5.9 Structured-Output Evaluation

Machine-consumable outputs should be evaluated for schema validity,
required fields, allowed values, semantic correctness, and downstream
executability. Natural-language quality alone is insufficient when the
response becomes an API payload or workflow input. Separate syntax
validity from business correctness.

**FDE lens:** *Valid JSON can still be a wrong business decision.*

------------------------------------------------------------------------

## 5.10 Tool-Call Accuracy

Agentic workloads require evaluation of tool selection, argument
construction, ordering, authorization boundaries, and final task
completion. A model may produce an excellent explanation while invoking
the wrong tool or parameters. Tool-call correctness should therefore be
measured independently from final prose quality.

**FDE lens:** *For agents, evaluate the trajectory---not just the final
sentence.*

------------------------------------------------------------------------

## 5.11 Failure-Segment Analysis

Overall averages can hide critical weaknesses. Evaluation should
identify where failures cluster: long documents, specific languages,
ambiguous instructions, particular tools, rare customer types, or
high-risk actions. Segment-level evidence tells the FDE what to fix and
whether routing or escalation is appropriate.

**FDE lens:** *Do not ask only "How accurate?" Ask "Wrong where?"*

------------------------------------------------------------------------

## 5.12 Quality / Latency / Cost Trade-offs

The highest-quality model may be too slow or expensive, while the
cheapest model may create unacceptable retries and escalations.
Selection therefore sits on a multi-objective frontier rather than a
single ranking. Customer SLAs and business risk determine the acceptable
operating point.

**FDE lens:** *There is rarely a universally best model---only a best
fit under constraints.*

------------------------------------------------------------------------

## 5.13 Small versus Frontier Models

Smaller models can offer lower cost, lower latency, easier hosting, and
sufficient quality for bounded tasks; frontier models may provide
stronger reasoning and robustness for complex cases. A mature
architecture can exploit both rather than forcing one model across all
workloads. Evaluation should reveal where each model is sufficient.

**FDE lens:** *Use expensive intelligence where it changes the outcome.*

------------------------------------------------------------------------

## 5.14 Model Routing

Routing sends different requests to different models based on
complexity, risk, modality, language, or confidence. It can improve
economics while preserving quality for difficult cases. Routing itself
must be evaluated because incorrect routing can become a new source of
failure.

**FDE lens:** *Model selection can be a runtime decision rather than a
one-time procurement decision.*

------------------------------------------------------------------------

## 5.15 Regression Evaluation

Prompts, models, retrieval pipelines, tools, and policies evolve, so
previously working behaviour can regress. A repeatable eval suite should
run before significant releases and model-version changes. Regression
evaluation turns AI changes into an engineering lifecycle rather than
manual demo verification.

**FDE lens:** *A model upgrade is still a production change and must
earn its way through evals.*

------------------------------------------------------------------------

## 5.16 Model and Version Change Management

Hosted models may change versions, deprecate endpoints, alter pricing,
or exhibit different behaviour after migration. FDEs should maintain
version visibility, controlled rollout, evaluation gates, rollback
strategy, and telemetry. The customer should not discover behavioural
drift before the engineering team does.

**FDE lens:** *Treat model versions as governed dependencies.*

------------------------------------------------------------------------

## Use Case --- Insurance Claims Assistant

Four models differ across task success, P95 latency, cost, and tool-call
accuracy. With 1.5M monthly requests and only 8% complex claims,
learners discover that a routed portfolio may outperform choosing one
"best" model.

``` mermaid
flowchart TD
    A[Incoming Claim] --> B[Risk / Complexity Router]
    B -->|Routine| C[Efficient Model]
    B -->|Complex / High Risk| D[High-Capability Model]
    C --> E[Validation]
    D --> E
    E -->|Pass| F[Complete]
    E -->|Uncertain| G[Escalate]
```

## Use Case --- Code Modernization

Models are evaluated on Java migration tasks using compilation success,
regression-test pass rate, security findings, and maintainability---not
conversational impressiveness.

## Trainer Takeaway

> **Model selection is an evidence-backed workload engineering decision.
> The FDE owns the bridge between eval results and production choice.**
