# Capstone 6 --- Atlas Manufacturing Supplier Quality & Digital Thread

## Architecture Decision Workbook --- Manufacturing \| 4--6 Hours

> **Scenario:** Atlas Manufacturing produces industrial power systems in
> plants across Germany, Poland and India. Quality incidents require
> engineers to manually correlate supplier certificates, MES events, SAP
> material records, IoT measurements, inspection images and engineering
> specifications.

# 1. Business Situation & Production Problem

**What we are doing:** Frame the challenge as traceability and
quality-decision architecture across IT and OT systems. AI may
accelerate investigation, but product genealogy and quality records must
remain authoritative and auditable.

A defective component discovered in final inspection may require
identifying affected lots, supplier batches, machines, process
parameters and shipped products. Current investigations take 2--5 days.

**Stakeholders:** COO; VP Manufacturing; Global Quality Director; Plant
Manager; OT Security Lead; Enterprise Architect; Supplier Quality
Manager; Data Protection Officer; Data/AI Platform Lead.

**Constraints:** GDPR for employee/supplier personal data, EU data
requirements where applicable, ISO 9001 quality-management processes, OT
network segmentation, supplier confidentiality, immutable traceability
expectations.

# 2. Team Mission

**What we are doing:** Design a production-grade digital-thread
architecture connecting supplier, ERP, MES, IoT and quality systems. The
design must support traceability and assisted root-cause investigation
without allowing AI to rewrite manufacturing facts.

# 3. Stakeholder & Priority Matrix

**What we are doing:** Determine whose decisions govern quality
disposition, OT access and supplier data. Rank business continuity and
compliance ahead of implementation convenience where appropriate.

  ------------------------------------------------------------------------------------------
  Decision         Quality   Plant    OT         Architect   Supplier   AI       Authority
                             Ops      Security               Quality             
  ---------------- --------- -------- ---------- ----------- ---------- -------- -----------
  Lot quarantine                                                                 

  Root-cause                                                                     
  recommendation                                                                 

  Supplier                                                                       
  notification                                                                   

  OT data access                                                                 

  Spec change                                                                    
  ------------------------------------------------------------------------------------------

# 4. Technology Decision Matrix

**What we are doing:** Select components for high-volume telemetry,
transactional genealogy and document/image evidence. Explain whether one
database can realistically serve every workload.

  Decision                Options                            Selected   Why   Rejected   Risk
  ----------------------- ---------------------------------- ---------- ----- ---------- ------
  Language                Python / Java / hybrid                                         
  Streaming               Kafka / MQTT / managed event bus                               
  Genealogy store         relational / graph / other                                     
  Telemetry store         time-series / lakehouse / other                                
  Document store/search   object + search / vector / other                               
  Integration             Camel / custom / iPaaS                                         
  Agent framework         LangGraph / LangChain / None                                   
  Deployment              plant edge / cloud / hybrid                                    

# 5. Integration & Digital Thread

**What we are doing:** Define how supplier and manufacturing records
become traceable without collapsing OT and IT security boundaries.
Preserve identifiers and lineage from supplier batch through finished
product.

Systems: supplier portal/SFTP/API; SAP ERP; MES; SCADA/IoT gateway; QMS;
PLM; document repository.

Create a flow matrix with protocol, cadence, schema, owner, latency,
replay, retention and trust zone.

# 6. Data & AI Decisions

**What we are doing:** Separate authoritative genealogy queries from
probabilistic root-cause reasoning. AI should cite evidence and
uncertainty rather than manufacture causal claims.

Evaluate: specification search; anomaly correlation; supplier-document
extraction; root-cause hypothesis; lot-impact analysis; quarantine
action.

  Capability     SQL/Graph/Rules   ML   RAG/LLM   Agent   Human Why
  ------------ ----------------- ---- --------- ------- ------- -----

# 7. Fine-Tuning / Model Pipeline

**What we are doing:** Design model adaptation only if historical
quality data can support it. Consider class imbalance, changing
processes, supplier variation and confidential engineering data.

If predictive quality ML: raw process data → quality → contextualize
product/machine → labels → temporal/plant split → train → evaluate →
registry → deploy → drift.

If LLM fine-tuning: justify why controlled RAG over specifications, NCRs
and approved procedures is insufficient.

# 8. Security, Compliance & OT Safety

**What we are doing:** Protect plant operations and confidential
engineering data while enabling cross-domain analysis. An AI agent must
never gain broad OT write access by convenience.

Checklist: OT/IT segmentation; read-only telemetry path; service
identity; supplier tenancy; GDPR; encryption; secrets; document
authorization; prompt injection; audit; human approval for
quarantine/process changes.

# 9. Failure Architecture

**What we are doing:** Ensure traceability continues when plants
disconnect or central services fail. Define local buffering,
reconciliation and evidence quality.

Scenarios: plant network disconnected; duplicate IoT events; late MES
data; supplier certificate missing; AI unavailable; wrong specification
retrieved; graph store unavailable; model drift; malicious supplier
document.

# 10. Required Architecture Views

**What we are doing:** Expose the digital thread, trust zones and
analytical architecture separately. Reviewers should trace a defective
serial number back to its evidence sources.

Produce: context; OT/IT trust zones; integration topology;
genealogy/data model; AI/RAG architecture; deployment; model pipeline if
applicable.

# 11. Prototype

**What we are doing:** Prove one difficult integration or reasoning
assumption using synthetic manufacturing data. Focus on traceability or
evidence-backed investigation.

Options: lot genealogy graph; quality-investigation RAG; synthetic IoT
anomaly + MES correlation; supplier certificate extraction +
deterministic validation.

# 12. ADRs, ROI & Defence

**What we are doing:** Record architecture decisions and connect them to
reduced investigation time, scrap and recall risk. Defend both technical
and organizational consequences.

ADRs: OT ingestion; genealogy store; data platform; AI boundary;
edge/cloud deployment.

Metrics: investigation time; traceability completeness; false root-cause
hypotheses; scrap/rework; supplier response time; platform availability.

Review: Why graph DB? Why not? What is authoritative? Can AI quarantine
a lot? What if cloud is unreachable? How is supplier data isolated? Why
fine-tune? Which decision is hardest to reverse?
