# Trainer Reference — AWS FinOps Agent

## Exact module coverage

```text
FinOps agent lifecycle
Cost monitoring and anomaly detection
Resource utilization and right-sizing
Cost optimization strategies: Savings Plans, scheduling
Forecasting and budgeting
```

This is a fresh AgentCore Harness implementation.

---

# 1. Trainer Scenario

`retail-platform` current-month AWS spend is materially above its normal run rate.

Participants should first brainstorm:
- which cost data is required;
- which operational data is required;
- how anomaly detection differs from optimization;
- right-sizing evidence;
- scheduling evidence;
- Savings Plans prerequisites;
- forecasting/budget;
- governance and approval.

---

# 2. Create Fresh Harness

```text
Amazon Bedrock AgentCore
 → Harness
 → Create Harness
```

Name:

```text
aws-finops-optimization-agent
```

Description:

```text
Evidence-driven AWS FinOps agent that detects cost anomalies, analyzes utilization,
evaluates right-sizing, scheduling and Savings Plans, forecasts budget impact, and
requests governed optimization actions.
```

Use an available model.

System prompt:

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

Add all eight inline functions from `01-participant-agent-spec.md`. Copy/paste definitions are also in `03-harness-tool-schemas.json`.

Wait for READY and copy the ARN.

---

# 3. Python Setup

```bash
cd python_project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export AWS_REGION="ap-south-1"
export HARNESS_ARN="<fresh-finops-harness-arn>"

python main.py
```

---

# 4. Hidden Scenario — Trainer Reference

## Cost summary

Normal monthly run rate:

```text
$18,400
```

Current month forecast before optimization:

```text
$23,900
```

EC2 is the largest increase.

## Anomaly

A dev EC2 instance `i-dev-analytics-01` began running continuously rather than business hours.

Estimated anomalous cost:

```text
~$720/month incremental
```

## Utilization

`i-dev-analytics-01`:
- instance class represented as `m6i.2xlarge`;
- average CPU 9%;
- peak CPU 31%;
- average memory 22%;
- peak memory 43%;
- non-production;
- currently 24x7.

This creates both right-sizing and scheduling opportunities.

## Scheduling

Required usage:

```text
08:00–20:00 IST, Monday–Friday
```

24x7 runtime is unnecessary.

The scheduling tool estimates approximately 64% runtime reduction.

## Production commitment

Production compute has stable baseline eligible usage. The mock commitment analysis shows a plausible 1-year Savings Plan opportunity.

Teaching point:

> First remove obvious waste. Then evaluate what stable usage remains worth committing to.

## Budget

Monthly budget:

```text
$21,000
```

Forecast:

```text
$23,900
```

Projected overrun:

```text
$2,900 / 13.8%
```

## Intended optimization reasoning

The agent should normally prioritize:
1. eliminate unnecessary dev runtime through scheduling;
2. consider right-sizing the oversized dev resource;
3. evaluate Savings Plan for genuinely stable production usage;
4. monitor forecast after changes.

Do not demand this exact ordering if the agent provides a defensible alternative.

---

# 5. Teaching the Lifecycle

```text
MONITOR
Cost summary / budget
     ↓
DETECT
Cost anomaly
     ↓
ATTRIBUTE
EC2 / resource
     ↓
UNDERSTAND
Utilization + schedule
     ↓
OPTIMIZE
right-size / schedule / commitment
     ↓
FORECAST
month-end impact
     ↓
GOVERN
FinOps policy
     ↓
ACT
approval-controlled request
     ↓
MEASURE
realized savings
```

---

# 6. Discussion Points

After cost summary:

> Do we know *why* cost increased, or only that it increased?

After anomaly:

> Is the anomaly automatically waste?

No. It identifies unexpected spend requiring explanation.

After utilization:

> Why should we inspect peaks instead of only average CPU?

After schedule analysis:

> Which is better here: committing to this usage or eliminating unnecessary runtime?

After commitment analysis:

> What usage should we commit to — today's total usage, or stable usage after waste reduction?

After forecast:

> How does budget pressure change prioritization?

After policy:

> Which recommendations are technical changes and which are financial commitments?

---

# 7. Optimization Comparison

```text
RIGHT-SIZING
Question: Are we paying for excess capacity?
Evidence: utilization + peaks
Risk: performance/capacity

SCHEDULING
Question: Are we paying while resource is unnecessary?
Evidence: required operating hours
Risk: availability if schedule is wrong

SAVINGS PLANS
Question: Is remaining eligible usage stable enough to commit?
Evidence: stable baseline / coverage
Risk: commitment to spend
```

---

# 8. Forecasting and Budgeting

Teach the distinction:

```text
ACTUAL
money already consumed

FORECAST
expected future/month-end spend

BUDGET
governance target

VARIANCE
forecast - budget
```

An agent should not report forecast savings as realized savings.

---

# 9. Approval Boundary

`request_finops_action()` returns:

```text
PENDING_APPROVAL
```

because:
- right-sizing changes production/infrastructure configuration;
- scheduling changes availability;
- Savings Plans create financial commitment;
- budget changes affect governance.

---

# 10. Observability

Verify Transaction Search if required:

```bash
aws xray get-trace-segment-destination --region ap-south-1
```

Then:

```text
CloudWatch
 → GenAI Observability
 → Bedrock AgentCore
 → Harnesses
```

Ask participants to identify:
- tool selection;
- evidence sequence;
- unnecessary calls;
- whether commitment was recommended prematurely;
- whether forecast influenced action.

---

# 11. Production Integrations

```text
get_cost_summary
 → Cost Explorer

get_cost_anomalies
 → Cost Anomaly Detection

get_resource_utilization
 → CloudWatch + Compute Optimizer

get_commitment_analysis
 → Savings Plans recommendations

get_schedule_analysis
 → resource tags + runtime patterns

get_forecast_and_budget
 → Cost Explorer Forecast + AWS Budgets

get_finops_policy
 → approved policy / Bedrock Knowledge Base

request_finops_action
 → ticket / workflow / controlled automation
```

---

# 12. Final Mental Model

```text
                     FINOPS AGENT
                          |
        +-----------------+------------------+
        |                 |                  |
        v                 v                  v
      COST            UTILIZATION         BUSINESS
        |                 |                  |
 anomaly/trend       right-size          forecast
 attribution         schedule            budget
        |                 |                  |
        +-----------------+------------------+
                          |
                          v
                     OPTIMIZE
                          |
             +------------+------------+
             |            |            |
          right-size   schedule   Savings Plans
             |            |            |
             +------------+------------+
                          |
                          v
                 GOVERNANCE / APPROVAL
                          |
                          v
                 REALIZED SAVINGS
