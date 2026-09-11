# Customer Success & Field Readiness

> **FDE mindset:** A technically correct solution creates value only
> when the customer understands it, trusts it, adopts it, and can see
> measurable progress.

------------------------------------------------------------------------

## 1. The Field-Readiness Mental Model

``` mermaid
flowchart LR
    A[Understand Stakeholder] --> B[Communicate Value]
    B --> C[Demonstrate]
    C --> D[Handle Concerns]
    D --> E[Drive Adoption]
    E --> F[Prove Outcome]
    F --> G[Expand / Next Step]
```

An FDE operates at the intersection of:

``` text
Technical Credibility
        +
Customer Communication
        +
Business Outcome
        =
Field Readiness
```

The objective is not simply to **show that the AI works**.

The objective is to help the customer answer:

> **"Can I trust this enough to move forward?"**

------------------------------------------------------------------------

# 2. Know Who You Are Talking To

The same AI solution should not be explained identically to every
stakeholder.

  Stakeholder               Usually Cares About
  ------------------------- ---------------------------------------------
  Business Sponsor          Value, outcome, speed, ROI
  Product / Process Owner   Workflow improvement, adoption, usability
  Architect                 Integration, scalability, design trade-offs
  Security / Compliance     Data, access, controls, auditability
  Operations                Reliability, monitoring, support
  End User                  Does this actually make my work easier?

### Example --- Banking Loan Review Assistant

Instead of explaining:

> "We use an LLM with retrieval and structured output."

Change the conversation based on the stakeholder.

**Business Sponsor**

> "The objective is to reduce manual application-review effort while
> keeping final credit decisions under existing controls."

**Architect**

> "The AI retrieves current policy, reads application documents, obtains
> customer information from existing services, and produces a structured
> recommendation."

**Risk / Compliance**

> "The model does not independently approve loans. Evidence,
> recommendation, and decision history remain traceable."

### FDE Question

Before presenting anything, ask:

> **Who is in the room, and what decision do I need them to make?**

------------------------------------------------------------------------

# 3. Handling Stakeholders and Objections

An objection is usually not a request for a longer technical
explanation.

It often signals:

-   uncertainty,
-   perceived risk,
-   missing evidence,
-   unclear value,
-   previous bad experience,
-   or a constraint you have not discovered.

Use a simple pattern:

``` text
LISTEN
   ↓
CLARIFY
   ↓
IDENTIFY THE REAL CONCERN
   ↓
RESPOND WITH EVIDENCE / OPTION
   ↓
CONFIRM
```

## Example Objections

### "How do we know the model will not hallucinate?"

Do not answer:

> "Our model has very high accuracy."

Instead clarify:

-   Which wrong outputs would be unacceptable?
-   Which decisions require authoritative evidence?
-   Where should deterministic validation or human review apply?
-   How will the behaviour be evaluated before production?

------------------------------------------------------------------------

### "Why can't we just use the most powerful model?"

Explore:

-   What workload are we optimizing for?
-   What quality threshold is required?
-   What latency is acceptable?
-   What volume will run through the system?
-   Does a smaller model meet the same success criteria?

The FDE converts a **model preference** into a **workload decision**.

------------------------------------------------------------------------

### "We don't want humans involved."

Ask:

> **Which decisions are safe to automate, and what is the consequence
> when the AI is wrong?**

Automation should be proportional to:

``` text
Confidence + Consequence + Recoverability
```

------------------------------------------------------------------------

# 4. Demo Basics --- Show the Outcome, Not the Technology

A customer demo is not a feature tour.

Use this simple flow:

``` mermaid
flowchart LR
    P[Problem] --> I[Input]
    I --> AI[AI Action]
    AI --> O[Outcome]
    O --> V[Business Value]
```

## Banking Example

### 1. Remind Them of the Problem

> "Credit officers currently spend significant time reviewing documents
> and identifying missing or inconsistent information."

### 2. Use a Realistic Input

Show a representative loan application with supporting documents.

### 3. Demonstrate the AI Action

The solution:

-   extracts important fields,
-   identifies missing information,
-   checks relevant policy,
-   summarizes the application,
-   produces a recommendation with evidence.

### 4. Show the Human Decision Point

``` text
AI Recommendation
       ↓
Evidence + Policy
       ↓
Credit Officer Review
       ↓
Existing Approval Process
```

### 5. Close With the Outcome

> "The objective is not AI making the credit decision. It is reducing
> the effort required for a credit officer to reach a well-supported
> decision."

------------------------------------------------------------------------

# 5. A Good Demo Has Three Layers

  -----------------------------------------------------------------------
  Layer                               What You Demonstrate
  ----------------------------------- -----------------------------------
  **Happy Path**                      The normal workflow works

  **Boundary Case**                   The system handles uncertainty or
                                      missing information

  **Control**                         The system knows when not to act
                                      automatically
  -----------------------------------------------------------------------

A mature AI demo should therefore include at least one moment where the
system says:

> **"I cannot safely complete this automatically."**

That can increase customer confidence rather than weaken the demo.

------------------------------------------------------------------------

# 6. Adoption Mindset

Deployment does not automatically mean adoption.

``` text
Built
  ≠
Used
  ≠
Trusted
  ≠
Value Realized
```

Ask:

-   Who will use the solution?
-   What existing workflow changes?
-   Does AI add another screen or remove work?
-   What behaviour must users learn?
-   How will users provide feedback?
-   What happens when they disagree with AI?
-   Who owns the solution after deployment?

### Useful Adoption Signals

  Signal         Example
  -------------- --------------------------------------------------
  Usage          \% of eligible applications using AI assistance
  Acceptance     \% of recommendations accepted by users
  Override       How often users reject/change AI recommendations
  Time Saved     Review time before vs after
  Quality        Error/rework rate
  Satisfaction   User feedback during pilot

> **Adoption itself is telemetry.** Low usage or high override rates may
> reveal workflow, trust, quality, or training problems.

------------------------------------------------------------------------

# 7. Simple Customer Playbook

## Before the Meeting

``` text
□ Who is attending?
□ What does each stakeholder care about?
□ What decision do we want from this meeting?
□ What customer problem are we demonstrating?
□ Is the demo environment tested?
□ Do we have realistic sample data?
□ What are the likely objections?
□ What evidence can support our claims?
□ What is our fallback if the live demo fails?
```

## During the Meeting

``` text
□ Reconfirm the problem
□ Connect technology to the business workflow
□ Demonstrate the outcome
□ Show limitations honestly
□ Capture objections and constraints
□ Avoid arguing with the customer
□ Confirm success criteria
□ Agree on the next decision
```

## After the Meeting

``` text
□ Summarize decisions
□ Capture unresolved questions
□ Assign owners
□ Record agreed success metrics
□ Document risks / dependencies
□ Define the next milestone
```

------------------------------------------------------------------------

# 8. From POC to Customer Success

A POC should end with a decision, not merely a demo.

``` mermaid
flowchart LR
    A[POC] --> B[Evaluate]
    B --> C{Success Criteria Met?}
    C -->|Yes| D[Pilot / Production Plan]
    C -->|Partially| E[Improve / Retest]
    C -->|No| F[Stop / Reframe]
```

Ask:

### What did we prove?

-   Technical feasibility?
-   Model quality?
-   Workflow improvement?
-   User acceptance?
-   Business value?

### What remains unproven?

-   Production scale?
-   Security?
-   Reliability?
-   Cost?
-   Adoption?
-   Integration complexity?

This prevents:

> **"The demo worked, therefore we are production-ready."**

------------------------------------------------------------------------

# 9. Expansion Mindset

Customer success can reveal the next opportunity.

For example:

``` text
Loan Document Review
        ↓
Successful Pilot
        ↓
Credit Officer Adoption
        ↓
New Opportunities
        ├── Missing-document follow-up
        ├── Policy Q&A
        ├── Application summarization
        └── Portfolio review assistance
```

But expansion should come from **observed customer value**, not from
trying to insert AI into every workflow.

Ask:

> "Now that this workflow is working, where is the next measurable
> bottleneck?"

------------------------------------------------------------------------

# 10. 5-Minute Field Challenge

You are demonstrating the banking loan-review assistant.

The customer's Head of Risk says:

> **"This looks impressive, but I don't trust an LLM anywhere near our
> credit process."**

Prepare a response containing only:

1.  **One clarification question**
2.  **The concern you believe is underneath the objection**
3.  **One architectural/control response**
4.  **One piece of evidence you would offer**
5.  **One next step you would propose**

Do not try to "win" the argument.

Your goal is to make the concern **specific and testable**.

------------------------------------------------------------------------

# 11. FDE Field Card

Before ending a customer interaction, be able to answer:

``` text
CUSTOMER PROBLEM
What are we solving?
________________________________________

STAKEHOLDER
Who needs to believe / approve / use this?
________________________________________

VALUE
What measurable outcome matters?
________________________________________

CONCERN
What is preventing the customer from moving forward?
________________________________________

EVIDENCE
What can we demonstrate or measure?
________________________________________

LIMITATION
What should we explicitly say the system cannot guarantee?
________________________________________

NEXT DECISION
What exactly should happen after this meeting?
________________________________________
```

------------------------------------------------------------------------

# Final Mental Model

``` mermaid
flowchart LR
    T[Technical Solution] --> D[Credible Demo]
    D --> TR[Trust]
    TR --> A[Adoption]
    A --> M[Measured Outcome]
    M --> CS[Customer Success]
    CS --> N[Next Opportunity]
```

> **A strong FDE does not finish with "the solution works." The FDE
> finishes with a customer who understands what was proven, what remains
> risky, and what decision should happen next.**
