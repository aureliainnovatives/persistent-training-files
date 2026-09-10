# AWS DevOps Incident Agent — Participant Build Specification

## Objective

Build a fresh **AWS DevOps Incident Agent** with **Amazon Bedrock AgentCore Harness**. The agent must investigate a production incident using operational evidence, correlate multiple telemetry sources, consult approved operational guidance, recommend remediation, and respect a human-approval boundary for production-changing actions.

This is not a chatbot exercise. The participant should understand the agent architecture, the technical contracts of each tool, the client-side execution model, safety boundaries, testing strategy, and observability.

## Scenario

`checkout-api` is experiencing elevated p95 latency and HTTP 5xx errors.

- Incident: `INC-DEVOPS-001`
- Region: `ap-south-1`
- Incident time: approximately `10:42`
- Business symptom: checkout failures

The agent must determine what is happening from evidence rather than being told the root cause.

## Architecture

```text
Operator
   |
   v
AgentCore Harness
   |
   +-- Model
   +-- System instructions
   +-- Inline tool definitions
   +-- Managed agent loop
   |
   | tool request
   v
Python client
   |
   +-- alerts
   +-- metrics
   +-- logs
   +-- deployments
   +-- ECS health
   +-- runbook
   +-- remediation approval
   |
   | tool result
   v
Harness -> model -> next tool or final answer
```

### Responsibility boundary

**Harness owns:** model configuration, instructions, tool schemas, orchestration/session loop and managed observability.

**Client owns:** implementation of inline functions, calls to operational systems, business/authorization logic, approval enforcement and returning tool results.

An AgentCore Harness inline function is a **tool contract**. Its implementation runs in the caller/client.

---

# 1. Create the Harness

AWS Console:

```text
Amazon Bedrock AgentCore
  → Harness
  → Create Harness
```

**Name**

```text
aws-devops-incident-agent
```

**Description**

```text
Evidence-driven DevOps incident investigation agent that correlates alerts, metrics,
logs, service health, deployments and operational runbooks, then recommends or requests
controlled remediation.
```

Choose a foundation model available in the lab account.

## System prompt

```text
You are an AWS DevOps incident investigation agent.

Your job is to investigate production incidents using evidence from the available tools.

Operating rules:
1. Do not invent operational facts.
2. Gather sufficient evidence before proposing a root cause.
3. Correlate alerts, metrics, logs, service health and recent changes.
4. Do not assume high latency means CPU or memory saturation.
5. Consult the operational runbook before recommending remediation when relevant.
6. Clearly separate observed evidence, likely root cause, confidence and recommended next steps.
7. Production-changing actions such as rollback, restart or scale require approval.
8. Never state that an action was executed unless the remediation tool explicitly returns an executed/success status.
9. If evidence is insufficient or contradictory, say so and identify what additional evidence is required.
10. Prefer the minimum set of useful tool calls, but use additional tools when needed to establish a defensible diagnosis.
```

---

# 2. Add Custom Inline Tools

Create these as **inline/custom functions** in Harness.

## Tool 1 — get_active_alerts

**Description**

```text
Get active operational alerts and incident metadata. Use this to identify the affected
service, severity, region, symptoms and incident timing before deeper investigation.
```

```json
{
  "type": "object",
  "properties": {
    "incident_id": {
      "type": "string",
      "description": "Incident identifier to retrieve, for example INC-DEVOPS-001."
    }
  },
  "required": ["incident_id"]
}
```

## Tool 2 — get_cloudwatch_metrics

**Description**

```text
Retrieve recent service telemetry comparable to Amazon CloudWatch metrics, including
CPU, memory, latency, HTTP 5xx rate and request volume. Use it to compare current
behavior with the normal baseline and test infrastructure saturation hypotheses.
```

```json
{
  "type": "object",
  "properties": {
    "service_name": {
      "type": "string",
      "description": "Service whose operational metrics should be inspected."
    },
    "period_minutes": {
      "type": "integer",
      "description": "Recent time window in minutes.",
      "minimum": 1,
      "maximum": 120
    }
  },
  "required": ["service_name"]
}
```

## Tool 3 — get_application_logs

**Description**

```text
Retrieve recent application log events for a service. Use this to identify errors,
timeouts, exceptions and application-level evidence related to an incident.
```

```json
{
  "type": "object",
  "properties": {
    "service_name": {
      "type": "string",
      "description": "Service whose application logs should be inspected."
    },
    "minutes": {
      "type": "integer",
      "description": "How many recent minutes of logs to inspect.",
      "minimum": 1,
      "maximum": 120
    }
  },
  "required": ["service_name"]
}
```

## Tool 4 — get_recent_deployments

**Description**

```text
Retrieve recent deployments and configuration changes for a service. Use it to determine
whether a release or configuration change correlates with the beginning of an incident.
```

```json
{
  "type": "object",
  "properties": {
    "service_name": {
      "type": "string",
      "description": "Service whose deployment history should be inspected."
    },
    "hours": {
      "type": "integer",
      "description": "Recent deployment-history window in hours.",
      "minimum": 1,
      "maximum": 24
    }
  },
  "required": ["service_name"]
}
```

## Tool 5 — get_ecs_service_health

**Description**

```text
Retrieve ECS-style service and task health. Use it to determine whether tasks are missing,
unhealthy, restarting or otherwise indicate infrastructure health problems.
```

```json
{
  "type": "object",
  "properties": {
    "service_name": {
      "type": "string",
      "description": "Service whose ECS health should be checked."
    }
  },
  "required": ["service_name"]
}
```

## Tool 6 — get_runbook

**Description**

```text
Retrieve approved operational troubleshooting and remediation guidance for a problem
category. Use this after evidence indicates a likely failure mode and before recommending
production remediation.
```

```json
{
  "type": "object",
  "properties": {
    "topic": {
      "type": "string",
      "description": "Problem or remediation topic, such as database connection pool exhaustion."
    }
  },
  "required": ["topic"]
}
```

## Tool 7 — request_remediation

**Description**

```text
Request a controlled production remediation such as rollback, restart or scale. This lab
tool does not automatically perform destructive changes. It returns whether human approval
is required. Use only after gathering evidence and consulting relevant operational guidance.
```

```json
{
  "type": "object",
  "properties": {
    "service_name": {
      "type": "string",
      "description": "Production service targeted by the remediation."
    },
    "action": {
      "type": "string",
      "enum": ["rollback", "restart", "scale"],
      "description": "Requested remediation action."
    },
    "reason": {
      "type": "string",
      "description": "Evidence-based justification for the requested action."
    }
  },
  "required": ["service_name", "action", "reason"]
}
```

---

# 3. Design Guidelines

### Tool descriptions matter

Descriptions guide model tool selection. State what the tool provides, when it should be used and what decision it helps support.

### Keep evidence tools deterministic

The model decides **what to inspect**. Tool code returns facts. Avoid hiding another LLM inside every tool.

### Separate read capabilities from action capabilities

```text
READ:
alerts, metrics, logs, deployments, health, runbook

CONTROLLED ACTION:
request_remediation
```

### Evidence before action

A sensible investigation may resemble:

```text
Alert
  ↓
Metrics + health
  ↓
Logs
  ↓
Recent changes
  ↓
Runbook
  ↓
RCA + confidence
  ↓
Controlled remediation request
```

Do not hard-code this sequence unless business policy requires it. The model should be allowed to choose an efficient sequence.

### Do not leak the root cause into the user prompt

Ask the agent to investigate. Do not tell it what to confirm.

### Production safety

Diagnosis authority and change authority are separate. Rollback/restart/scale require approval in this lab.

---

# 4. Client Implementation Requirements

The Python client must:

1. Read `HARNESS_ARN` and `AWS_REGION` from environment.
2. Create a UUID session ID (AgentCore requires at least 33 characters).
3. Invoke the Harness.
4. Process the streaming response.
5. Detect inline function requests.
6. Execute the matching local handler.
7. Continue the Harness conversation with both the assistant `toolUse` and matching user `toolResult`.
8. Continue until a final response is produced.
9. Print tool calls/results so participants can see the orchestration.

Environment:

```bash
export AWS_REGION="ap-south-1"
export HARNESS_ARN="<your-harness-arn>"
```

---

# 5. Test Prompts

### Investigation

```text
Investigate incident INC-DEVOPS-001. Identify the affected service and determine the most
likely root cause. Use operational evidence rather than guessing. Separate evidence,
root cause, confidence and recommended next steps.
```

### Correlation

```text
Investigate INC-DEVOPS-001. Determine whether this is infrastructure saturation,
application failure, or a recent-change problem. Correlate metrics, logs, service health
and deployment evidence before answering.
```

### Safe remediation

```text
Investigate INC-DEVOPS-001. Determine the likely root cause, consult the relevant
operational runbook, and request the safest remediation if the evidence is strong enough.
Do not bypass production approval requirements.
```

---

# 6. What the Lab Evidence Is Designed to Reveal

The answer is not hard-coded into the prompt. The tools collectively expose:

```text
10:39 deployment v4.7
      DB_POOL_MAX changed 80 → 15

10:42 incident starts

Metrics:
CPU/memory and traffic near baseline
latency and 5xx sharply elevated

ECS:
all six tasks healthy

Logs:
database connection acquisition timeout

Runbook:
connection-pool exhaustion investigation;
rollback correlated bad configuration;
production rollback requires approval
```

A defensible RCA is database connection-pool exhaustion strongly correlated with the v4.7 configuration change.

---

# 7. Observability Exercise

Enable CloudWatch Transaction Search once for the AWS account. After a fresh Harness invocation:

```text
CloudWatch
  → GenAI Observability
  → Bedrock AgentCore
  → Harnesses
```

Also inspect **All traces**.

Discuss:
- model/tool spans;
- ordering;
- latency;
- which evidence changed the hypothesis;
- tool failures;
- total agent latency;
- what should be redacted in production.

---

# 8. Production Evolution

The lab mocks AWS systems so that everyone can run it safely.

```text
Mock metrics          → CloudWatch GetMetricData
Mock logs             → CloudWatch Logs Insights
Mock deployments      → CodeDeploy/ECS/CI-CD API
Mock ECS health       → ECS DescribeServices/DescribeTasks
Mock runbook          → Bedrock Knowledge Base
Approval simulator    → enterprise approval/change workflow
```

The Harness contracts can remain stable while implementations evolve.

## Completion Checklist

- [ ] Harness created
- [ ] Model selected
- [ ] System prompt configured
- [ ] Seven inline tools added
- [ ] Harness READY
- [ ] Harness ARN configured in client
- [ ] Investigation succeeds
- [ ] Multiple evidence sources correlated
- [ ] Runbook consulted
- [ ] Remediation is approval-controlled
- [ ] Trace inspected
