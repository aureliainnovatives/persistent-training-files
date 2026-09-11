# Customer Discovery, Use-Case Prioritization & Success Criteria

> **FDE mindset:** Do not start with *"Which model should we use?"*
> Start with *"Which business problem is worth solving, for whom, and
> how will we know it worked?"*

------------------------------------------------------------------------

## 1. The Discovery Flow

``` mermaid
flowchart LR
    A[Customer Problem] --> B[Discover]
    B --> C[Identify Opportunity]
    C --> D[Prioritize Use Case]
    D --> E[Define Success]
    E --> F[Estimate Value]
    F --> G[POC / Next Step]
```

A discovery conversation should progressively answer:

1.  **What is happening today?**
2.  **Where is the pain or opportunity?**
3.  **Why does it matter?**
4.  **Can AI realistically influence it?**
5.  **What measurable change would make the customer call this
    successful?**

------------------------------------------------------------------------

## 2. Asking the Right Questions

Avoid beginning with technology:

> ❌ "Do you want RAG, agents, or fine-tuning?"

Start with the business workflow.

### Understand the Current Process

-   Walk me through how this process works today.
-   Who performs it, and what triggers it?
-   What information and systems are involved?
-   How often does it happen?
-   Which steps require the most manual effort?

### Find the Pain

-   Where does the process slow down?
-   Where do errors or rework occur?
-   Which decisions are difficult or inconsistent?
-   What happens when the process fails?

### Understand Business Impact

-   Does this affect **cost, revenue, risk, customer experience, or
    productivity**?
-   How many people, customers, or transactions are affected?
-   Is there an SLA, regulatory, or customer impact?

### Understand the AI Opportunity

-   Which step requires understanding, extraction, reasoning,
    summarization, classification, generation, or decision support?
-   What information would AI need?
-   Is that information available?
-   Does AI need live system access?
-   Where would human approval remain necessary?

### Define Success

-   What does a good outcome look like?
-   What metric should improve?
-   What improvement would be meaningful?
-   What must **not** get worse?
-   What would justify moving from POC to production?

------------------------------------------------------------------------

## 3. Bullseye Questions

When discovery time is limited, use these to quickly locate the
opportunity.

  -----------------------------------------------------------------------
  \#                      Bullseye Question       Reveals
  ----------------------- ----------------------- -----------------------
  1                       **What is the single    Problem
                          biggest pain in this    
                          process?**              

  2                       **Who experiences it?** User / stakeholder

  3                       **How often does it     Scale
                          happen?**               

  4                       **What does it cost     Business impact
                          when it happens?**      

  5                       **What part requires    AI opportunity
                          human knowledge or      
                          judgment today?**       

  6                       **What data/information Feasibility
                          would AI need?**        

  7                       **What could go wrong   Risk
                          if AI makes a           
                          mistake?**              

  8                       **What number would     Success criterion
                          prove that this         
                          worked?**               
  -----------------------------------------------------------------------

> **Bullseye:** High pain + high frequency + measurable impact +
> accessible information + manageable risk = a strong candidate for
> further investigation.

------------------------------------------------------------------------

## 4. Banking Example --- Loan Application Review

A bank receives thousands of loan applications. Credit officers manually
review application forms, salary slips, bank statements, supporting
documents, and policy requirements.

The customer initially says:

> **"We want an AI system that can approve loans automatically."**

The FDE should not immediately design the solution.

  -----------------------------------------------------------------------
  Discovery Question                  Example Finding
  ----------------------------------- -----------------------------------
  Where is most time spent?           Reviewing and validating documents

  How long does review take?          \~25 minutes/application

  What causes rework?                 Missing or inconsistent information

  What is the volume?                 20,000 applications/month

  Is final approval high-risk?        Yes

  What could AI assist with?          Extraction, checks, summarization,
                                      recommendation

  What must remain controlled?        Credit eligibility and final
                                      approval

  What would success look like?       Reduce review effort without
                                      increasing credit/compliance risk
  -----------------------------------------------------------------------

Discovery changes the opportunity:

``` text
Initial Request
"AI should approve loans"
        ↓
Discovery
        ↓
Better Opportunity
"AI-assisted loan document review
and credit-officer recommendation"
```

------------------------------------------------------------------------

## 5. Basic Use-Case Prioritization

Customers usually identify several possible AI ideas. Use four simple
dimensions:

  -----------------------------------------------------------------------
  Dimension                           Question
  ----------------------------------- -----------------------------------
  **Business Value**                  If solved, does it materially
                                      matter?

  **Feasibility**                     Do we have the data, systems, and
                                      technical ability?

  **Risk**                            What is the consequence of an
                                      incorrect AI outcome?

  **Measurability**                   Can we clearly prove improvement?
  -----------------------------------------------------------------------

Score each from **1--5**.

  --------------------------------------------------------------------------------------
  Banking Use Case        Value   Feasibility       Risk\*   Measurability Initial View
  ---------------- ------------ ------------- ------------ --------------- -------------
  FAQ assistant               3             5            5               4 Easy win

  Loan document               4             5            4               5 **Strong
  extraction                                                               candidate**

  Credit-officer              5             3            3               4 POC carefully
  recommendation                                                           

  Fully automated             5             2            1               4 High-risk
  loan approval                                                            starting
                                                                           point
  --------------------------------------------------------------------------------------

**Risk score:** 5 = low/manageable risk; 1 = very high risk.

``` mermaid
quadrantChart
    title AI Opportunity Prioritization
    x-axis Low Feasibility --> High Feasibility
    y-axis Low Business Value --> High Business Value
    quadrant-1 Start Here
    quadrant-2 Investigate
    quadrant-3 Deprioritize
    quadrant-4 Quick Wins
    Document Extraction: [0.85, 0.80]
    FAQ Assistant: [0.90, 0.55]
    Credit Recommendation: [0.55, 0.90]
    Automated Approval: [0.30, 0.95]
```

> The highest-value use case is **not automatically the best first use
> case**.

------------------------------------------------------------------------

## 6. Success Criteria --- Define Before the POC

Avoid:

> "Let's build a POC and see whether the customer likes it."

Instead, define success before building.

  -----------------------------------------------------------------------
  Type                                Loan-Review Example
  ----------------------------------- -----------------------------------
  **Business**                        Reduce average manual review time
                                      from 25 min to 10 min

  **Quality**                         ≥95% extraction accuracy on agreed
                                      critical fields

  **Risk**                            No automatic final credit approval

  **Operational**                     Response within agreed processing
                                      time

  **Adoption**                        Credit officers find
                                      recommendations useful in pilot

  **POC Gate**                        Meet agreed metrics on
                                      representative historical
                                      applications
  -----------------------------------------------------------------------

``` text
Business Problem
      ↓
Use Case
      ↓
Metric
      ↓
Target
      ↓
Evaluation
      ↓
Go / Improve / Stop
```

------------------------------------------------------------------------

## 7. High-Level ROI Thinking

At discovery stage, you usually do **not** need a complex financial
model.

Start with:

> **Is the potential value large enough to justify deeper
> investigation?**

### Basic Productivity Hypothesis

``` text
Potential Capacity Benefit
≈
Volume
×
Time Saved per Transaction
```

Example:

``` text
20,000 applications/month
× 15 minutes saved
= 5,000 hours of capacity/month
```

Do **not** immediately call that "5,000 hours of cost saving." Ask:

-   Does saved time actually reduce cost?
-   Does it increase processing capacity?
-   Does it shorten turnaround time?
-   Can employees focus on higher-value work?
-   Could faster processing improve conversion or customer experience?

### Value Is Broader Than Cost

``` text
AI VALUE
├── Productivity  → less manual effort
├── Revenue       → faster conversion / greater capacity
├── Risk          → fewer errors / stronger compliance
├── Customer      → faster, better experience
└── Employee      → less repetitive work
```

Compare the value hypothesis with the expected cost:

``` text
AI Cost
=
Model / infrastructure
+ integration
+ engineering
+ evaluation
+ monitoring
+ human oversight
+ ongoing operations
```

At discovery stage, the goal is **directional ROI**, not false
precision.

------------------------------------------------------------------------

## 8. 5-Minute Discovery Challenge

The customer says:

> **"Our credit officers spend too much time reviewing loan
> applications. We want GenAI."**

As the FDE, write only:

1.  **Three questions you would ask first**
2.  **One specific problem worth investigating**
3.  **One candidate AI use case**
4.  **Two success metrics**
5.  **One value/ROI hypothesis**

**Do not choose the model or architecture yet.**

------------------------------------------------------------------------

## 9. FDE Field Checklist

Before leaving discovery, you should be able to complete:

``` text
Problem:
_____________________________________________

Primary user:
_____________________________________________

Current pain:
_____________________________________________

Scale / frequency:
_____________________________________________

Candidate AI opportunity:
_____________________________________________

Business value:
_____________________________________________

Major risk:
_____________________________________________

Success metric:
_____________________________________________

POC hypothesis:

"If we _______________________________,
then _________________________________
should improve from _______ to _______."
```

## Final Mental Model

``` mermaid
flowchart LR
    P[Problem] --> Q[Questions]
    Q --> O[Opportunity]
    O --> R[Prioritize]
    R --> S[Success Criteria]
    S --> V[Value / ROI]
    V --> POC[POC Hypothesis]
```

> **Discovery is successful when the team can explain the problem,
> value, risk, and measurable outcome before discussing the model or
> architecture.**
