# AWS FinOps Agent — Participant Technical Build Specification

## Module scope

This lab directly covers:

1. **FinOps agent lifecycle**
2. **Cost monitoring and anomaly detection**
3. **Resource utilization and right-sizing**
4. **Cost optimization strategies — Savings Plans and scheduling**
5. **Forecasting and budgeting**

The objective is to build an **AWS FinOps Agent** with **Amazon Bedrock AgentCore Harness** that reasons across financial and operational evidence rather than merely suggesting generic cost-cutting.

---

# 1. Scenario

The `retail-platform` workload has produced an unexpected increase in AWS spend during the current month.

The FinOps team wants the agent to determine:

```text
What changed in cost?
      ↓
Is it a genuine anomaly?
      ↓
Which resources/services drive it?
      ↓
Are those resources efficiently utilized?
      ↓
Can we right-size?
      ↓
Can non-production runtime be scheduled?
      ↓
Is stable usage suitable for Savings Plans?
      ↓
What does month-end forecast show?
      ↓
Are we likely to exceed budget?
      ↓
Which action has the best risk-adjusted value?
```

Do not tell the agent the answer in the prompt.

---

# 2. FinOps Agent Lifecycle

```text
MONITOR
   ↓
DETECT ANOMALY
   ↓
ATTRIBUTE COST
   ↓
ANALYZE UTILIZATION
   ↓
IDENTIFY OPTIMIZATION OPTIONS
   ↓
MODEL SAVINGS / COMMITMENT
   ↓
FORECAST
   ↓
CHECK BUDGET
   ↓
APPLY GOVERNANCE
   ↓
REQUEST ACTION
   ↓
MEASURE REALIZED SAVINGS
```

The final step is important: an estimated saving is not a realized saving.

---

# 3. Architecture

```text
FinOps / Cloud Architect
          |
          v
   AgentCore Harness
          |
          +-- Model
          +-- System Prompt
          +-- Inline Tool Contracts
          +-- Managed Agent Loop
          |
          v
   Python Tool Implementations
          |
          +-- Cost summary
          +-- Cost anomalies
          +-- Resource utilization
          +-- Savings Plan analysis
          +-- Schedule analysis
          +-- Forecast + budget
          +-- FinOps policy
          +-- Controlled action
          |
          v
 Evidence + Optimization + Forecast + Governance
```

**Harness owns:** model configuration, system instructions, tool schemas, orchestration and observability.

**Client owns:** implementation of inline tools, AWS/billing integrations, deterministic calculations, policy enforcement, approvals and tool results.

---

# 4. Create AgentCore Harness

```text
Amazon Bedrock AgentCore
 → Harness
 → Create Harness
```

**Name**

```text
aws-finops-optimization-agent
```

**Description**

```text
Evidence-driven AWS FinOps agent that detects cost anomalies, analyzes utilization,
evaluates right-sizing, scheduling and Savings Plans, forecasts budget impact, and
requests governed optimization actions.
```

Select a foundation model available in the lab account.

## System prompt

```text
You are an AWS FinOps analysis and optimization agent.

Your job is to investigate cloud cost behavior using evidence from the available tools and
produce financially responsible, operationally safe recommendations.

Operating rules:
1. Never invent cost, utilization, pricing, commitment, forecast, or budget data.
2. Establish cost context and trend before recommending optimization.
3. Investigate anomalies using cost drivers, resource utilization, workload schedule, and recent changes.
4. Distinguish realized cost, forecast cost, estimated savings, and committed spend.
5. Do not recommend right-sizing solely from low average utilization; consider peaks, workload criticality and schedule.
6. Do not recommend Savings Plans until stable eligible usage and commitment implications have been evaluated.
7. Consult the FinOps policy before requesting an optimization action.
8. Clearly separate observed evidence, anomaly assessment, optimization opportunity, estimated impact, assumptions, confidence, and recommended action.
9. Production-changing actions and financial commitments require approval.
10. Never claim savings were realized or a commitment was purchased unless a tool explicitly reports successful execution.
11. If evidence is insufficient or contradictory, state what additional evidence is required.

```

---

# 5. Configure Inline Custom Tools

## Tool 1 — `get_cost_summary`

**Description**

```text
Retrieve AWS cost summary and trend data for an account, service or workload. Use this to establish current spend, baseline spend, major cost drivers and period-over-period change before diagnosing an anomaly or recommending optimization.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "scope": {
      "type": "string",
      "description": "Account, workload, service or cost-allocation scope to analyze."
    },
    "period": {
      "type": "string",
      "description": "Cost period such as current_month or last_30_days."
    }
  },
  "required": [
    "scope"
  ]
}
```

## Tool 2 — `get_cost_anomalies`

**Description**

```text
Retrieve detected cost anomalies and their likely cost dimensions or services. Use this to determine whether spend materially deviates from the expected baseline and to identify where deeper investigation is needed.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "scope": {
      "type": "string",
      "description": "Account or workload scope to inspect for cost anomalies."
    }
  },
  "required": [
    "scope"
  ]
}
```

## Tool 3 — `get_resource_utilization`

**Description**

```text
Retrieve utilization and capacity evidence for compute resources, including average and peak CPU/memory, instance size, runtime pattern and workload criticality. Use this to evaluate right-sizing or scheduling opportunities without relying on cost alone.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "resource_id": {
      "type": "string",
      "description": "Resource identifier whose utilization and capacity should be analyzed."
    },
    "days": {
      "type": "integer",
      "description": "Historical utilization window in days.",
      "minimum": 1,
      "maximum": 90
    }
  },
  "required": [
    "resource_id"
  ]
}
```

## Tool 4 — `get_commitment_analysis`

**Description**

```text
Retrieve Savings Plans-style commitment analysis for eligible compute usage, including stable hourly spend, coverage, commitment candidates and estimated savings. Use this before recommending a financial commitment.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "scope": {
      "type": "string",
      "description": "Workload or account scope for commitment analysis."
    },
    "term_years": {
      "type": "integer",
      "enum": [
        1,
        3
      ],
      "description": "Savings-plan analysis term."
    }
  },
  "required": [
    "scope",
    "term_years"
  ]
}
```

## Tool 5 — `get_schedule_analysis`

**Description**

```text
Analyze whether non-production resources run outside required business hours and estimate avoidable runtime. Use this to evaluate start/stop scheduling as an alternative or complement to right-sizing and commitments.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "resource_id": {
      "type": "string",
      "description": "Resource to analyze for scheduling opportunity."
    }
  },
  "required": [
    "resource_id"
  ]
}
```

## Tool 6 — `get_forecast_and_budget`

**Description**

```text
Retrieve current budget, month-to-date spend, end-of-period forecast, variance and budget threshold status. Use this to determine whether current cost behavior threatens budget objectives.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "scope": {
      "type": "string",
      "description": "Budget or workload scope to forecast."
    }
  },
  "required": [
    "scope"
  ]
}
```

## Tool 7 — `get_finops_policy`

**Description**

```text
Retrieve approved FinOps governance guidance for right-sizing, scheduling, commitment purchases, budgets and optimization approvals. Use this before requesting a cost optimization action.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "topic": {
      "type": "string",
      "description": "FinOps policy or optimization topic to retrieve."
    }
  },
  "required": [
    "topic"
  ]
}
```

## Tool 8 — `request_finops_action`

**Description**

```text
Request a controlled FinOps action such as rightsize, schedule_stop_start, purchase_savings_plan, or update_budget_alert. This lab does not execute infrastructure changes or financial commitments automatically; it returns the approval requirement.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "target": {
      "type": "string",
      "description": "Resource, workload, account or budget targeted by the action."
    },
    "action": {
      "type": "string",
      "enum": [
        "rightsize",
        "schedule_stop_start",
        "purchase_savings_plan",
        "update_budget_alert"
      ],
      "description": "Requested optimization or governance action."
    },
    "reason": {
      "type": "string",
      "description": "Evidence-based business and technical justification."
    },
    "estimated_monthly_savings": {
      "type": "number",
      "minimum": 0,
      "description": "Estimated monthly savings in USD when applicable."
    }
  },
  "required": [
    "target",
    "action",
    "reason"
  ]
}
```


---

# 6. Technical Design Guidelines

## Cost evidence before recommendation

The agent should not begin with “buy Savings Plans” or “downsize instances.” First establish:
- spend baseline;
- anomaly;
- cost driver;
- utilization;
- workload characteristics;
- forecast/budget impact.

## Cost ≠ utilization

Billing data tells us **what costs money**. Utilization data helps explain whether capacity is appropriately sized.

## Average utilization is insufficient

A resource with 15% average CPU can still have 80% peaks. Right-sizing decisions should consider:
- average;
- peak;
- memory;
- criticality;
- runtime schedule;
- redundancy/performance requirements.

## Savings Plans are commitments

A commitment strategy should be evaluated against stable eligible usage. Do not treat a discount as free savings.

## Scheduling and commitments solve different problems

```text
Scheduling:
avoid paying for resources when they are not required.

Right-sizing:
reduce excess capacity while resources are running.

Savings Plans:
discount stable eligible usage in exchange for commitment.
```

These can complement each other, but avoid committing to usage that should first be eliminated.

## Forecast vs budget

```text
Actual / MTD spend
       ↓
Forecast
       ↓
Expected month-end spend
       ↓
Compare with budget
       ↓
Variance / threshold risk
```

## Optimization authority

```text
ANALYSIS
costs
anomalies
utilization
schedules
commitments
forecast
budget

ACTION
right-size
schedule
purchase commitment
change budget alert
       ↓
APPROVAL / GOVERNANCE
```

Financial commitments deserve an explicit approval boundary.

---

# 7. Python Client Requirements

The Python client must:

1. Read `HARNESS_ARN` and `AWS_REGION` from environment.
2. create a UUID session.
3. invoke Harness.
4. process streaming events.
5. detect inline function requests.
6. execute the matching deterministic handler.
7. return assistant `toolUse` plus matching user `toolResult`.
8. continue until final answer.
9. display tool requests and results.

```bash
export AWS_REGION="ap-south-1"
export HARNESS_ARN="<your-finops-harness-arn>"
```

---

# 8. Test Prompts

### Cost anomaly

```text
Investigate the current-month cost increase for retail-platform. Determine whether there
is a material anomaly, identify the main cost driver, and explain the evidence.
```

### Right-sizing

```text
Investigate retail-platform cost and utilization. Identify any defensible right-sizing
opportunity, considering both average and peak utilization before recommending a change.
```

### Optimization strategy

```text
Analyze retail-platform and compare right-sizing, non-production scheduling and Savings
Plans opportunities. Do not recommend a financial commitment until stable eligible usage
has been evaluated.
```

### Forecast and budget

```text
Analyze current retail-platform spending, forecast month-end cost and determine whether
the workload is likely to exceed budget. Explain the projected variance.
```

### Complete FinOps investigation

```text
Perform a complete FinOps investigation of retail-platform. Analyze the cost anomaly,
resource utilization, right-sizing, scheduling, Savings Plans, forecast and budget.
Consult FinOps policy and request the best supported optimization action without bypassing
approval requirements.
```

---

# 9. Evidence Pattern Designed Into the Lab

```text
Current-month spend increased
        ↓
EC2 is primary anomaly driver
        ↓
dev EC2 resource runs 24x7
        ↓
low average utilization + modest peak
        ↓
scheduling/right-sizing opportunity
        ↓
production compute has stable baseline usage
        ↓
possible Savings Plan candidate
        ↓
month-end forecast exceeds budget
        ↓
agent compares opportunities
        ↓
policy/governance
        ↓
PENDING_APPROVAL
```

The agent should distinguish immediate waste elimination from longer-term commitment optimization.

---

# 10. Observability Exercise

```text
CloudWatch
 → GenAI Observability
 → Bedrock AgentCore
 → Harnesses / All traces
```

Inspect:
- which financial tool was called first;
- whether anomaly evidence preceded optimization;
- whether utilization was checked before right-sizing;
- whether commitment analysis was used before Savings Plans;
- whether forecast/budget data affected prioritization;
- whether policy was consulted before action.

---

# 11. Production Evolution

```text
Mock cost summary       → AWS Cost Explorer
Mock anomaly data       → Cost Anomaly Detection
Mock utilization        → CloudWatch / Compute Optimizer
Mock commitment model   → Cost Explorer / Savings Plans recommendations
Mock schedule analysis  → tags + CloudWatch/runtime data + scheduler
Mock forecast/budget    → Cost Explorer forecast / AWS Budgets
Mock policy             → enterprise FinOps policy / Knowledge Base
Mock action             → governed automation / ticket / approval workflow
```

## Completion checklist

- [ ] Fresh Harness created
- [ ] Eight tools configured
- [ ] Python client connected
- [ ] Cost trend analyzed
- [ ] Anomaly detected/attributed
- [ ] Utilization checked
- [ ] Right-sizing considered
- [ ] Scheduling considered
- [ ] Savings Plan suitability analyzed
- [ ] Forecast produced
- [ ] Budget variance evaluated
- [ ] Policy consulted
- [ ] Action remains approval-controlled
- [ ] Trace inspected
