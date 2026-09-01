# Capstone 2 --- HelixCare Patient 360 & Clinical Integration Platform

## Architecture Decision Workbook --- Healthcare \| 4--6 Hours

> **Scenario:** HelixCare Health Network operates 18 hospitals, 46
> outpatient clinics and a digital-care platform across Germany, France
> and the Netherlands. It needs a governed Patient 360 integration layer
> without allowing AI-generated mappings or summaries to silently alter
> clinical truth.

# 1. Business Situation & Production Problem

**What we are doing:** Understand the clinical integration problem
before selecting technology. Patient safety, consent, interoperability
and traceability take precedence over AI sophistication.

HelixCare uses Epic-based EHR instances, a legacy laboratory system,
PACS, Salesforce Health Cloud, pharmacy systems and partner telehealth
platforms. Patient identifiers, consent states and clinical schemas
differ across regions. Duplicate identities and inconsistent mappings
are causing delayed reconciliation and incomplete patient views.

The Chief Digital Officer wants a Patient 360 platform supporting
FHIR-based interoperability, near-real-time updates and assisted
schema/mapping discovery.

**Stakeholders:** CIO; Chief Medical Information Officer (CMIO); Data
Protection Officer (DPO); Head of Integration Architecture; Clinical
Safety Officer; Hospital Operations Director; Platform Engineering Lead.

**Regulatory/design constraints:** GDPR, EU data-residency requirements,
consent/purpose limitation, auditability, healthcare interoperability
using HL7 FHIR; teams must identify any additional country-specific
obligations rather than assume one global policy.

# 2. Team Mission

**What we are doing:** Design a production architecture that integrates
clinical systems while preserving authoritative clinical records. AI may
assist discovery, mapping and operations, but the team must establish
where probabilistic decisions are unacceptable.

Design the Patient 360 integration architecture, its data flows, trust
boundaries, AI/non-AI boundary, operational model and a small validation
prototype.

# 3. Stakeholder & Authority Matrix

**What we are doing:** Identify who can propose, approve and execute
decisions affecting patient data. Clinical and privacy authority must be
explicit.

  -------------------------------------------------------------------------------------------
  Decision       CMIO     DPO      Integration   Clinical   Operations   AI       Final
                                   Architect     Safety                           Authority
  -------------- -------- -------- ------------- ---------- ------------ -------- -----------
  Canonical                                                                       
  patient model                                                                   

  Identity merge                                                                  

  Consent                                                                         
  override                                                                        

  AI-generated                                                                    
  mapping                                                                         

  Production                                                                      
  schema change                                                                   
  -------------------------------------------------------------------------------------------

# 4. Architecture Decision Matrix

**What we are doing:** Select technologies by requirement and risk
rather than preference. Every major choice requires alternatives and
consequences.

  ------------------------------------------------------------------------------
  Decision      Options       Selected    Why?        Rejected       Risk
                Considered                            Alternatives   
  ------------- ------------- ----------- ----------- -------------- -----------
  Language      Python / Java                                        
                / Other                                              

  Integration   Camel /                                              
  framework     Spring                                               
                Integration /                                        
                MuleSoft /                                           
                Other                                                

  API standard  FHIR REST /                                          
                custom REST /                                        
                event                                                

  Operational   PostgreSQL /                                         
  DB            document DB /                                        
                other                                                

  Messaging     Kafka / queue                                        
                / direct API                                         

  AI framework  LangGraph /                                          
                LangChain /                                          
                plain Python                                         
                / None                                               

  Retrieval     pgvector /                                           
  store         vector DB /                                          
                None                                                 

  Gateway       Kong /                                               
                existing                                             
                gateway /                                            
                other                                                

  Deployment    Kubernetes /                                         
                VM / managed                                         
                / hybrid                                             

  Secrets                                                            
  ------------------------------------------------------------------------------

# 5. Decision Sequence

**What we are doing:** Rank the decisions that must be resolved first.
Explain dependencies between privacy, clinical safety, identity, data
and technology.

Rank 1--8:
`[ ] Patient safety  [ ] Consent/privacy  [ ] Identity/mastering  [ ] Source of truth  [ ] Integration contracts  [ ] AI boundary  [ ] Technology  [ ] Deployment`

Explain your top three choices.

# 6. Integration & Data Architecture

**What we are doing:** Design the movement of clinical information
between systems and determine what is authoritative. Include failure,
replay, lineage and regional boundaries.

Required sources: EHR, LIS, PACS metadata, pharmacy, CRM, telehealth.

  --------------------------------------------------------------------------------------------------
  Flow       Source     Destination   FHIR/Event/Batch   SLA        Authoritative   Failure/Replay
                                                                    Source          
  ---------- ---------- ------------- ------------------ ---------- --------------- ----------------
                                                                                    

  --------------------------------------------------------------------------------------------------

Produce: System Context, logical architecture, integration/data flow,
security/trust boundaries and deployment architecture.

# 7. AI / RAG / Fine-Tuning Decision

**What we are doing:** Decide whether AI adds justified value for
mapping, terminology assistance, documentation or operations. Never make
an LLM the clinical system of record.

  Capability                         Rules/Code   LLM   RAG   Agent   Human Why?
  -------------------------------- ------------ ----- ----- ------- ------- ------
  FHIR mapping suggestion                                                   
  Patient identity merge                                                    
  Terminology explanation                                                   
  Integration incident diagnosis                                            
  Clinical record modification                                              

If fine-tuning is proposed, design: approved dataset → de-identification
→ rights/consent check → quality → train/validation/test → training →
clinical evaluation → registry → deployment → monitoring →
rollback/retraining. Explain why RAG/prompting/tools are insufficient.

# 8. Security, Privacy & Compliance Checklist

**What we are doing:** Treat privacy and clinical governance as
architecture inputs. Identify controls that could invalidate the
proposed solution if discovered late.

-   [ ] GDPR lawful basis/purpose defined
-   [ ] Consent enforcement designed
-   [ ] Data minimisation defined
-   [ ] Regional residency addressed
-   [ ] Encryption in transit/at rest
-   [ ] RBAC/ABAC defined
-   [ ] Patient identity merge audited
-   [ ] AI provider data handling assessed
-   [ ] Prompt/RAG data leakage considered
-   [ ] Retention/deletion process defined
-   [ ] Complete audit trail
-   [ ] Human approval for high-risk actions

# 9. Failure & Production Readiness

**What we are doing:** Define safe degraded behaviour when systems or AI
fail. Patient care must not depend on an opaque model remaining
available.

Answer: EHR unavailable? duplicate patient? stale consent? event
delivered twice? mapping wrong? LLM unavailable? malicious retrieved
document? model latency 20s? regional link fails?

# 10. Prototype

**What we are doing:** Validate one risky assumption rather than build
the whole platform. Code is evidence, not the capstone.

Choose one: FHIR mapping assistant; deterministic validation of AI
mapping; patient-data integration flow using synthetic data;
incident-analysis assistant. State hypothesis, success criteria and what
is intentionally excluded.

# 11. ADRs & Final Defence

**What we are doing:** Record five consequential decisions and defend
them to an architecture review board. Reviewers will challenge safety,
privacy, interoperability and reversibility.

Create ADRs for: source of truth; identity/mastering; integration
pattern; AI boundary; deployment/provider.

Be ready to answer: Why this DB? Why event vs REST? Who may merge
identities? Where is consent enforced? What happens without AI? Why
fine-tuning? Where is training data sourced? What is hardest to reverse?

# 12. Deliverables

**What we are doing:** Package reasoning into reviewable architecture
artifacts. A reviewer should be able to trace every major technology to
a requirement and risk.

Submit: stakeholder matrix; prioritisation; decision matrix; 5+
diagrams; compliance checklist; AI decision matrix; fine-tuning pipeline
if applicable; failure design; five ADRs; small prototype; ROI measures.
