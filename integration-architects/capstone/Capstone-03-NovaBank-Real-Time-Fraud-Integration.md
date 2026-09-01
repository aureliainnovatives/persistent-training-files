# Capstone 3 --- NovaBank Real-Time Fraud & Payments Decision Platform

## Architecture Decision Workbook --- Banking \| 4--6 Hours

> **Scenario:** NovaBank Europe processes card, mobile and
> instant-payment transactions across the EU. It must modernize fraud
> integration without increasing payment latency or allowing an AI agent
> to autonomously block/release high-value transactions without governed
> controls.

# 1. Business Situation & Production Problem

**What we are doing:** Frame the problem as a regulated, low-latency
decision system rather than an AI demo. Availability, auditability,
false-positive cost and security are first-class architecture
constraints.

Payment events arrive from card processors, mobile banking, SEPA instant
payments, merchant acquiring and account systems. Fraud rules, an
existing ML scorer and manual investigation tools are fragmented.
Operations sees inconsistent decisions and slow investigations.

**Stakeholders:** Chief Risk Officer; Chief Information Security
Officer; Head of Payments; Head of Fraud Operations; Enterprise
Integration Architect; Model Risk Manager; DPO; SRE Lead.

**Constraints:** GDPR, PCI DSS for cardholder-data environments,
PSD2/SCA considerations, model-risk governance, immutable decision
audit, strict latency/SLA. Teams must validate which obligations apply
to their chosen data flow.

# 2. Team Mission

**What we are doing:** Design the integration and decision architecture
from transaction ingestion through scoring, policy and investigation.
Separate deterministic authorization, ML scoring, LLM reasoning and
human authority.

Design a resilient fraud platform capable of high-volume real-time
decisions plus AI-assisted investigation.

# 3. Decision Priority Matrix

**What we are doing:** Decide what must be fixed before selecting
frameworks. Rank decisions according to regulatory and business impact.

Rank:
`[ ] Transaction SLA  [ ] PCI boundary  [ ] Fraud authority  [ ] Event contracts  [ ] Data retention  [ ] ML/LLM boundary  [ ] Technology  [ ] UI`

    Rank Decision   Why Now?   What Depends on It?
  ------ ---------- ---------- ---------------------
                               

# 4. Technology Matrix

**What we are doing:** Compare technology against latency, resilience,
security and operational requirements. Adding an agent is optional and
must be justified.

  ----------------------------------------------------------------------------
  Decision       Options       Choice      Why         Rejected    Trade-off
  -------------- ------------- ----------- ----------- ----------- -----------
  Language       Java / Python                                     
                 / hybrid                                          

  Streaming      Kafka /                                           
                 managed event                                     
                 bus / queue                                       

  Transaction DB PostgreSQL /                                      
                 distributed                                       
                 SQL / other                                       

  Feature/fast   Redis / DB /                                      
  store          managed                                           
                 feature store                                     
                 / None                                            

  ML serving     managed /                                         
                 container /                                       
                 existing                                          
                 scorer                                            

  Agent          LangGraph /                                       
  framework      LangChain /                                       
                 None                                              

  API gateway    Kong / bank                                       
                 gateway /                                         
                 other                                             

  Deployment     Kubernetes /                                      
                 managed /                                         
                 hybrid                                            
  ----------------------------------------------------------------------------

# 5. Decision Pipeline

**What we are doing:** Define the exact sequence from payment event to
business action. Mark every point where latency, failure or human
authority changes the path.

Create a flow covering: ingest → validate → enrich → rules → ML score →
policy decision → approve/challenge/block → case creation →
investigation → feedback.

For each step record: owner, maximum latency, authoritative input, retry
policy, idempotency strategy and audit record.

# 6. AI vs ML vs Rules vs Human

**What we are doing:** Distinguish predictive ML from generative AI and
deterministic policy. Do not let an LLM become a payment authorization
engine merely because it can reason about a case.

  Decision                        Rules   ML   LLM/RAG   Agent   Human Final Choice/Why
  ----------------------------- ------- ---- --------- ------- ------- ------------------
  Transaction validation                                               
  Fraud probability                                                    
  Regulatory policy                                                    
  Case summarisation                                                   
  Investigator recommendation                                          
  Release blocked payment                                              

# 7. Model/Fine-Tuning Architecture

**What we are doing:** If model adaptation is proposed, design its full
lifecycle and governance. Historical fraud labels can be biased, delayed
and highly sensitive.

Decide separately for predictive fraud ML and any LLM fine-tuning.
Include data lineage, feature generation, label quality, temporal split,
offline evaluation, model registry, champion/challenger, deployment,
drift, feedback and rollback.

Answer: Why fine-tune an LLM rather than use RAG over fraud
policies/case knowledge?

# 8. Security & Compliance

**What we are doing:** Establish trust boundaries around payment data,
credentials, models and investigators. Security controls must exist
outside prompts.

-   [ ] PCI DSS scope identified
-   [ ] PAN/tokenisation strategy
-   [ ] GDPR purpose/minimisation
-   [ ] PSD2/SCA impact assessed
-   [ ] Encryption/key management
-   [ ] Service identity
-   [ ] Secrets management
-   [ ] Model access controls
-   [ ] Case-level authorization
-   [ ] Prompt injection/data exfiltration controls
-   [ ] Immutable audit
-   [ ] Model decision traceability

# 9. Failure Architecture

**What we are doing:** Decide what happens under partial failure without
causing a payment outage or uncontrolled fraud exposure. Every fallback
creates a business risk that must be explicitly accepted.

Design responses for: event bus unavailable; fraud scorer timeout;
duplicate event; stale feature; LLM unavailable; policy store
unavailable; false-positive spike; model drift; compromised credential;
investigator tool unavailable.

# 10. Required Architecture Views

**What we are doing:** Show the system from business, integration, AI
and operational perspectives. One diagram cannot communicate every trust
and latency boundary.

Produce: context; real-time transaction flow; logical components;
data/model pipeline; security/PCI trust boundaries; deployment;
observability.

# 11. Prototype & Review

**What we are doing:** Validate one architectural risk with a small
experiment. A polished chatbot does not compensate for a weak payment
architecture.

Possible prototype: synthetic event stream + deterministic rules + mock
scorer + AI case summarizer; or fraud-investigation RAG with synthetic
cases.

Create five ADRs and defend: event architecture; data stores; ML/LLM
boundary; failure policy; deployment/security boundary.

# 12. Success Measures

**What we are doing:** Tie architecture to fraud reduction without
ignoring customer friction and cost. Optimizing one metric can damage
another.

Define targets for fraud loss, false positives, decision latency,
investigation time, availability, manual review rate, model drift and
cost per transaction.
