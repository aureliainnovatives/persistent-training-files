# Integration Architecture Capstone Projects --- Index

## Program Purpose

These capstones are designed as **4--6 hour architecture and
decision-making exercises** rather than programming competitions. Teams
are expected to analyse the business problem, identify stakeholders and
constraints, make explicit architecture decisions, design
integration/data/AI/security/deployment views, document trade-offs, and
defend their decisions.

> **Core principle:** The prototype is supporting evidence. The primary
> deliverable is the quality of the architecture and the reasoning
> behind it.

------------------------------------------------------------------------

## Capstone Portfolio

  ----------------------------------------------------------------------------------------------------------------
  \#          Domain          Company / Project Core Architecture Key Technologies /        Compliance /
                                                Challenge         Concepts                  Governance Focus
  ----------- --------------- ----------------- ----------------- ------------------------- ----------------------
  01          Enterprise      Enterprise API    Discover,         OpenAPI, API catalogs,    API governance,
              Integration     Modernization &   rationalize,      semantic search, RAG,     authorization,
                              Integration       govern and safely LangChain/LangGraph where confidential
                              Discovery         evolve a          justified, Python/Java,   documentation,
                                                fragmented        vector/graph/relational   auditability
                                                enterprise API    stores, Kong/API Gateway  
                                                estate                                      

  02          Healthcare      **HelixCare ---   Integrate         HL7 FHIR, EHR, LIS, PACS, GDPR, consent, EU data
                              Patient 360 &     fragmented        pharmacy, messaging,      residency, clinical
                              Clinical          clinical systems  Python/Java, AI-assisted  safety, auditability
                              Integration       while preserving  mapping, RAG              
                              Platform**        clinical truth,                             
                                                consent and                                 
                                                patient identity                            

  03          Banking         **NovaBank ---    Build low-latency Kafka/event streaming,    PCI DSS, GDPR,
                              Real-Time Fraud & fraud integration Java/Python, fraud ML,    PSD2/SCA
                              Payments Decision while separating  LLM/RAG, API Gateway,     considerations,
                              Platform**        deterministic     transactional/fast stores model-risk governance,
                                                rules, predictive                           immutable audit
                                                ML, LLM reasoning                           
                                                and human                                   
                                                authority                                   

  04          Aviation        **AeroSphere ---  Correlate         Telemetry streaming,      Airworthiness/safety
                              Predictive        telemetry,        time-series/lakehouse,    processes,
                              Maintenance &     maintenance       predictive ML, RAG,       controlled-document
                              Engineering       history and       MRO/ERP integration,      provenance, OEM data
                              Intelligence**    controlled        Python/Java               rights, human
                                                engineering                                 engineering approval
                                                knowledge without                           
                                                delegating                                  
                                                safety-critical                             
                                                authority to AI                             

  05          Retail          **MercuryRetail   Maintain correct  Event-driven              GDPR, PCI DSS,
                              --- Global        order state       architecture,             idempotency,
                              Omnichannel Order across payments,  Kafka/queues, workflow    reconciliation,
                              Orchestration**   inventory, fraud, orchestration,            auditability,
                                                warehouses and    Java/Python,              multi-region
                                                carriers during   Camel/Spring, Kong,       resilience
                                                extreme peak load AI-assisted operations    
                                                and partial                                 
                                                failures                                    

  06          Manufacturing   **Atlas           Build             SAP, MES, SCADA/IoT,      ISO 9001 processes,
                              Manufacturing --- traceability      Kafka/MQTT,               GDPR, OT/IT
                              Supplier Quality  across supplier,  graph/relational stores,  segmentation, supplier
                              & Digital         ERP, MES, IoT and lakehouse/time-series,    confidentiality,
                              Thread**          quality systems   RAG/ML, edge-cloud        traceability
                                                while preserving  architecture              
                                                OT boundaries and                           
                                                authoritative                               
                                                manufacturing                               
                                                records                                     
  ----------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Capstone 01 --- Enterprise API Modernization & Integration Discovery

**Domain:** Enterprise Integration / API Management

An enterprise has accumulated hundreds of APIs across legacy
applications, microservices, SaaS platforms and acquisitions. Teams
struggle to discover existing capabilities, understand dependencies,
identify duplicates and estimate the impact of API changes.

### Primary Decisions

-   What becomes the authoritative API catalog?
-   Keyword, semantic or hybrid discovery?
-   Is a vector database required?
-   Is a graph database justified for dependencies?
-   Where should AI be used versus deterministic metadata processing?
-   Is LangGraph/LangChain necessary or is plain application logic
    sufficient?
-   How should OpenAPI specifications, repositories, gateways and
    runtime telemetry be integrated?
-   How are inferred relationships separated from confirmed
    architectural facts?

**Main learning theme:** AI-assisted enterprise API intelligence without
turning the LLM into the system of record.

------------------------------------------------------------------------

# Capstone 02 --- HelixCare Patient 360 & Clinical Integration

**Domain:** Healthcare

HelixCare operates hospitals, outpatient clinics and digital-care
services across multiple European countries. Patient information is
distributed across EHR, laboratory, imaging, pharmacy, CRM and
telehealth systems with inconsistent identifiers and schemas.

### Primary Decisions

-   What is the authoritative clinical source?
-   How should patient identity/mastering work?
-   How should HL7 FHIR be used?
-   Event-driven versus synchronous clinical integration?
-   Where is consent enforced?
-   Can AI recommend mappings?
-   Can AI participate in patient-record modification?
-   Is RAG or fine-tuning justified?
-   How should regional data residency affect deployment?

**Key governance:** GDPR, consent, purpose limitation, clinical safety
and human clinical authority.

------------------------------------------------------------------------

# Capstone 03 --- NovaBank Real-Time Fraud & Payments

**Domain:** Banking / Financial Services

NovaBank processes card, mobile and instant-payment transactions. Fraud
rules, predictive models and investigation workflows are fragmented,
while payment decisions require very low latency and strong
auditability.

### Primary Decisions

-   Streaming versus synchronous processing?
-   Java, Python or hybrid architecture?
-   Which decisions belong to rules versus predictive ML?
-   Where can LLM/RAG assist fraud investigators?
-   Should an AI agent ever block or release a payment?
-   What happens if the fraud model times out?
-   How should model drift and false positives be managed?
-   What data belongs inside the PCI boundary?
-   Is LLM fine-tuning justified over RAG and tools?

**Key governance:** PCI DSS, GDPR, PSD2/SCA considerations, model-risk
governance and immutable decision audit.

------------------------------------------------------------------------

# Capstone 04 --- AeroSphere Predictive Maintenance & Engineering Intelligence

**Domain:** Aviation

AeroSphere wants to correlate aircraft telemetry, maintenance records,
parts information, engineering manuals and service bulletins to reduce
unscheduled maintenance and improve engineering investigation.

### Primary Decisions

-   Streaming, batch or hybrid telemetry ingestion?
-   Time-series database versus lakehouse?
-   How should maintenance records and telemetry be correlated?
-   Predictive ML versus generative AI?
-   RAG over controlled manuals versus LLM fine-tuning?
-   How is engineering-document provenance preserved?
-   What happens when an obsolete manual is retrieved?
-   Which decisions must remain exclusively with qualified engineers?
-   Edge, cloud or hybrid deployment?

**Key governance:** safety/airworthiness processes, controlled
engineering documentation, provenance, OEM data rights and human
engineering authority.

------------------------------------------------------------------------

# Capstone 05 --- MercuryRetail Global Omnichannel Order Orchestration

**Domain:** Retail / E-commerce

MercuryRetail integrates web, mobile, store and marketplace orders with
inventory, payment, fraud, SAP ERP, warehouses and carriers. Peak events
create overselling, duplicate fulfillment, retry storms and inconsistent
order states.

### Primary Decisions

-   Orchestration versus choreography?
-   REST versus event-driven integration?
-   Kafka, queue or another messaging model?
-   Where does authoritative order state live?
-   How is idempotency implemented?
-   What happens when payment succeeds but the response is lost?
-   How should compensation work?
-   Can AI participate in transaction execution or only operations?
-   How should the platform survive 12× peak traffic?

**Key governance:** GDPR, PCI DSS, financial reconciliation,
multi-region resilience and deterministic transaction integrity.

------------------------------------------------------------------------

# Capstone 06 --- Atlas Manufacturing Supplier Quality & Digital Thread

**Domain:** Manufacturing / Industry 4.0

Atlas Manufacturing needs to correlate supplier records, SAP material
data, MES production events, SCADA/IoT measurements, quality records and
engineering specifications to investigate defects and establish complete
product genealogy.

### Primary Decisions

-   How should IT and OT systems integrate?
-   Kafka, MQTT or another ingestion mechanism?
-   Is a graph database justified for genealogy?
-   Where should telemetry live?
-   How should plant-edge and cloud responsibilities be divided?
-   Predictive ML versus RAG/LLM root-cause assistance?
-   Can AI quarantine a production lot?
-   How should supplier information be isolated?
-   What happens when a plant loses connectivity?

**Key governance:** ISO 9001 quality processes, GDPR, OT/IT
segmentation, supplier confidentiality and evidence-backed traceability.

------------------------------------------------------------------------

# Common Architecture Expectations

Every team should produce architecture decisions rather than merely
selecting technologies. Each selected component should answer the
question: **What requirement made this necessary?**

Teams should cover:

1.  Business problem and measurable outcomes
2.  Stakeholders and decision authority
3.  Functional and non-functional requirements
4.  Architecture decision priorities
5.  Technology decision matrix with rejected alternatives
6.  System Context Diagram
7.  Logical Component Architecture
8.  Integration and Data Flow
9.  Data architecture and systems of record
10. AI versus deterministic versus human decision matrix
11. RAG / prompting / tools / fine-tuning decision
12. Security and trust boundaries
13. Failure and resilience architecture
14. Deployment and operational architecture
15. At least five Architecture Decision Records (ADRs)
16. Small prototype validating one or two risky assumptions
17. Business value / ROI
18. Architecture Review Board defence

------------------------------------------------------------------------

# Common Technology Palette

The following are **options, not mandatory technologies**.

``` text
Programming
├── Python
├── Java / Spring Boot
└── Hybrid

Agent / AI Orchestration
├── LangChain
├── LangGraph
├── AutoGen
├── Plain Python
└── None

Integration
├── REST / OpenAPI
├── Apache Camel
├── Kafka / Event Streaming
├── Queues / PubSub
├── Batch / ETL
└── Hybrid

Data
├── PostgreSQL
├── Document DB
├── Graph DB
├── Vector DB / pgvector
├── Time-Series DB
└── Lakehouse

AI
├── Prompting
├── Tool Calling
├── RAG
├── Predictive ML
├── Fine-Tuning
└── No AI

Gateway
├── Kong
├── Existing Enterprise API Gateway
└── Direct Integration where justified
```

> Selecting **None** is a valid architecture decision when the team can
> defend it.

------------------------------------------------------------------------

# Suggested Team Allocation

For approximately 30--40 participants:

    Participants Suggested Setup
  -------------- -----------------------
              30 6 teams × \~5 people
              36 6 teams × 6 people
              40 6 teams × 6--7 people

A useful team structure is:

-   Lead / Solution Architect
-   Integration Architect
-   Data / AI Architect
-   Security & Compliance Owner
-   Platform / Operations Architect
-   Business / Product Representative

Roles are viewpoints for the exercise; they do not need to match
participants' actual job titles.

------------------------------------------------------------------------

# Final Capstone Principle

``` text
Problem
   ↓
Stakeholders
   ↓
Compliance & Risk
   ↓
Requirements
   ↓
Architecture Decisions
   ↓
Data & Integration
   ↓
AI vs Non-AI
   ↓
Technology
   ↓
Security
   ↓
Deployment & Operations
   ↓
Prototype
   ↓
Architecture Defence
```

> **Do not optimise for the number of agents, technologies or lines of
> code. Optimise for defensible architectural decisions, explicit
> trade-offs and a production-ready way of thinking.**
