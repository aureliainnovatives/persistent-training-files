# Capstone 4 --- AeroSphere Predictive Maintenance & Engineering Intelligence

## Architecture Decision Workbook --- Aviation \| 4--6 Hours

> **Scenario:** AeroSphere Airlines operates 140 aircraft and wants to
> integrate aircraft telemetry, maintenance records, engineering manuals
> and work orders to reduce unscheduled maintenance while keeping
> safety-critical decisions under certified human authority.

# 1. Business Situation & Production Problem

**What we are doing:** Understand the difference between operational
intelligence and safety-critical maintenance authority. The platform may
surface evidence and recommendations, but architecture must preserve
provenance and engineering accountability.

Telemetry arrives after flights and, for selected aircraft, as
near-real-time health messages. Maintenance records live in an MRO
system; manuals and service bulletins are document-heavy; parts
inventory is in ERP. Engineers spend hours correlating faults across
systems.

**Stakeholders:** Chief Engineering Officer; Director of Maintenance;
Continuing Airworthiness Manager; Safety & Compliance Director;
Integration Architect; Data Engineering Lead; MLOps Lead; Maintenance
Control Engineer.

**Constraints:** aviation safety/airworthiness processes, controlled
engineering documentation, auditability, data provenance, OEM data
licensing, operational availability. Teams must identify applicable
jurisdictional requirements rather than invent certification claims.

# 2. Team Mission

**What we are doing:** Design an integrated engineering intelligence
platform from telemetry ingestion through maintenance recommendation.
Decide which outputs are advisory and which systems remain
authoritative.

# 3. Architecture Priority

**What we are doing:** Sequence decisions so safety and data provenance
are established before AI implementation. Explain why each earlier
decision constrains later ones.

Rank: safety authority; source of truth; telemetry SLA; document
provenance; data model; AI/ML boundary; integration technology;
deployment.

# 4. Technology Decision Matrix

**What we are doing:** Select architecture components based on telemetry
volume, document retrieval, historical analysis and operational
constraints.

  Decision              Options                               Selected   Why   Rejected   Risk
  --------------------- ------------------------------------- ---------- ----- ---------- ------
  Language              Python / Java / hybrid                                            
  Streaming             Kafka / cloud event service / batch                               
  Time-series storage   TSDB / lakehouse / relational                                     
  Operational DB        PostgreSQL / document DB                                          
  Data platform         lakehouse / warehouse / other                                     
  Retrieval             vector / hybrid search / None                                     
  Agent framework       LangGraph / LangChain / None                                      
  Deployment            cloud / edge+cloud / hybrid                                       

# 5. Integration & Data Flow

**What we are doing:** Integrate telemetry, MRO, ERP and controlled
engineering content while retaining timestamps and provenance. Define
late-arriving data, duplicate events and replay.

Sources: aircraft health messages; MRO work orders; parts ERP; OEM
manuals; service bulletins; historical defects.

Build a matrix: source, contract, ingestion mode, SLA, authoritative
owner, retention, replay, data-quality controls.

# 6. AI / ML / RAG Boundary

**What we are doing:** Match predictive models, document retrieval and
generative reasoning to different tasks. Safety-critical maintenance
disposition must have explicit authority.

  ---------------------------------------------------------------------------------------
  Capability         Deterministic   Predictive    RAG/LLM      Agent   Engineer Why
                                             ML                                  
  ---------------- --------------- ------------ ---------- ---------- ---------- --------
  Telemetry                                                                      
  validation                                                                     

  Failure-risk                                                                   
  prediction                                                                     

  Manual retrieval                                                               

  Fault                                                                          
  explanation                                                                    

  Maintenance                                                                    
  recommendation                                                                 

  Aircraft release                                                               
  decision                                                                       
  ---------------------------------------------------------------------------------------

# 7. Model Data Pipeline

**What we are doing:** Design training/evaluation data only if
predictive modelling or fine-tuning is justified. Maintenance labels,
fleet differences and temporal leakage require careful treatment.

Design: raw telemetry → quality → aircraft/configuration context →
feature pipeline → labelled maintenance outcomes → temporal
train/validation/test → model training → engineering evaluation →
registry → deployment → drift → feedback.

If LLM fine-tuning is proposed, separately justify it against RAG over
controlled manuals.

# 8. Safety, Security & Governance

**What we are doing:** Protect engineering data and prevent AI
recommendations from being mistaken for approved maintenance
instructions. Provenance and human authority must remain visible.

Checklist: controlled-document version; source citations; OEM licensing;
RBAC; encryption; audit; prompt injection from documents; model/version
traceability; recommendation confidence; human approval; rollback.

# 9. Failure Architecture

**What we are doing:** Design useful degraded operation when telemetry,
models or document systems fail. An unavailable AI assistant must not
stop established maintenance processes.

Scenarios: telemetry delayed; sensor corrupt; model unavailable; wrong
manual version retrieved; hallucinated procedure; ERP unavailable;
duplicate fault; model drift; network loss.

# 10. Required Views & ADRs

**What we are doing:** Produce architecture artifacts that expose
operational, data and safety boundaries. Record why consequential
decisions were made.

Required: context; telemetry/data flow; logical architecture; model/RAG
architecture; trust/safety boundaries; deployment. ADRs: telemetry
ingestion; storage; predictive model boundary; RAG design; human
authority.

# 11. Prototype

**What we are doing:** Test one high-risk assumption with
synthetic/non-sensitive data. The prototype should validate
architecture, not simulate aircraft certification.

Options: telemetry anomaly pipeline; maintenance-manual RAG; correlation
of synthetic fault + work-order history.

# 12. Architecture Defence

**What we are doing:** Defend safety, provenance, latency and AI choices
to an engineering review board. Be prepared to remove AI where it
creates more risk than value.

Answer: What is authoritative? Can AI issue maintenance instructions?
Why vector search? Why fine-tune? What if retrieved manual is obsolete?
What happens offline? Who signs off recommendations? What is hardest to
reverse?
