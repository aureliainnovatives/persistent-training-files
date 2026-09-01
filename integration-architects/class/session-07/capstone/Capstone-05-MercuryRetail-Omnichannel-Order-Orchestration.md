# Capstone 5 --- MercuryRetail Global Omnichannel Order Orchestration

## Architecture Decision Workbook --- Retail \| 4--6 Hours

> **Scenario:** MercuryRetail sells through web, mobile, stores and
> marketplaces across the EU and UK. Peak-sale failures are creating
> overselling, duplicate fulfillment and customer-service incidents
> across inventory, payment, fraud, warehouse and carrier integrations.

# 1. Business Situation & Production Problem

**What we are doing:** Treat the challenge as distributed transaction
and integration architecture first. AI should improve discovery or
operations without replacing deterministic order-state controls.

A single order can interact with Shopify-based storefronts, store POS,
OMS, inventory services, payment providers, fraud services, SAP ERP,
three warehouse systems and multiple carriers. Black Friday volume is
12× normal traffic.

**Stakeholders:** Chief Digital Officer; VP Supply Chain; Head of
E-commerce; Enterprise Integration Architect; Payments Lead; Data
Protection Officer; SRE Manager; Customer Care Director.

**Constraints:** GDPR, PCI DSS where cardholder data enters scope,
consumer-data retention, peak scalability, idempotency, financial
reconciliation, multi-region availability.

# 2. Team Mission

**What we are doing:** Design a resilient order orchestration platform
that preserves state correctness across partial failures. Decide where
synchronous APIs, events, workflows and AI each belong.

# 3. Business Priority Matrix

**What we are doing:** Force explicit trade-offs among consistency,
customer experience, throughput and cost. Rank what the architecture
protects first.

Rank: no duplicate charge; no duplicate fulfillment; inventory accuracy;
checkout latency; availability; recovery; observability; AI assistance.

# 4. Technology Decisions

**What we are doing:** Choose technologies by transaction semantics and
operational requirements. Do not select Kafka, Kubernetes or agents
merely because they are fashionable.

  Decision                Options                                   Selected   Why   Rejected   Risk
  ----------------------- ----------------------------------------- ---------- ----- ---------- ------
  Language                Java / Python / hybrid                                                
  Orchestration           workflow engine / custom / choreography                               
  Messaging               Kafka / queue / PubSub / None                                         
  DB                      PostgreSQL / distributed SQL / NoSQL                                  
  Cache                   Redis / None / other                                                  
  Integration framework   Camel / Spring / other                                                
  Agent framework         LangGraph / None / other                                              
  AI Gateway              Kong / existing / None                                                

# 5. Order State & Integration Design

**What we are doing:** Define order-state ownership and cross-system
contracts. Explicitly design idempotency, retries, compensation,
ordering and eventual consistency.

Create the lifecycle: order received → inventory reserve → fraud →
payment authorize → fulfillment → shipment → notification.

For every step answer: sync/async? idempotency key? timeout? retry?
compensation? DLQ? source of truth? customer-visible state?

# 6. AI Boundary

**What we are doing:** Decide whether AI belongs in runtime transaction
paths or primarily in operations and engineering. Probabilistic
reasoning must not silently change deterministic financial/order state.

Evaluate: integration troubleshooting; incident summarization;
customer-service explanation; carrier exception analysis; routing
recommendation; actual payment/fulfillment execution.

# 7. Data / RAG / Fine-Tuning

**What we are doing:** Design data pipelines only where they support a
concrete business capability. Fine-tuning must have measurable advantage
over tools/RAG/prompting.

If building an operations copilot, consider RAG over runbooks,
architecture docs and incidents plus tools for live order state. If
fine-tuning is proposed, define dataset rights, cleansing, split,
evaluation, registry, deployment and retraining.

# 8. Compliance & Security

**What we are doing:** Identify cardholder, customer and operational
data boundaries. Ensure AI does not expand access beyond the caller's
existing authorization.

Checklist: GDPR; PCI scope; tokenized payment data; RBAC; service
identities; secrets; API gateway; audit; PII minimization; RAG
authorization; prompt injection; production action approval.

# 9. Resilience Scenarios

**What we are doing:** Demonstrate how the order reaches a known state
despite partial failures. Recovery design is more important than a
happy-path demo.

Handle: payment succeeds but response times out; inventory reserve
duplicated; warehouse unavailable; Kafka backlog; carrier API fails; DLQ
grows; AI unavailable; regional outage; retry storm.

# 10. Required Diagrams

**What we are doing:** Visualize business state, technical integration
and operational trust boundaries separately. Reviewers must be able to
trace an order across every system.

Produce: context; order sequence/state; logical components; event/API
topology; data flow; security boundaries; deployment; AI operations flow
if used.

# 11. Prototype & ADRs

**What we are doing:** Validate one distributed-systems assumption. The
prototype should expose failure behaviour, not merely return a
successful response.

Possible prototype: synthetic order workflow with idempotency +
retry/DLQ; event-driven order simulator; AI incident analyzer over
synthetic logs.

Five ADRs: orchestration vs choreography; event technology; state store;
consistency/compensation; AI authority.

# 12. Review Questions

**What we are doing:** Defend the architecture against peak-load,
consistency, compliance and operational challenges.

Why event-driven? What if Kafka is down? Who owns order state? How
prevent double charge? Where is PCI data? Why agent? What happens
without AI? Which component becomes bottleneck at 12× load? What is the
recovery objective?
