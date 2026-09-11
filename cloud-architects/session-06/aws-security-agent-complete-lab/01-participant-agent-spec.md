# AWS Security Agent — Participant Technical Build Specification

## Module scope

This lab is built specifically around:

1. **Security agent lifecycle and configuration**
2. **Threat analysis and modelling**
3. **Code review**
4. **Security data sources — CloudTrail, findings, vulnerabilities**
5. **Risk detection and remediation**

The objective is to build an **AWS Security Investigation Agent** using **Amazon Bedrock AgentCore Harness**. It must investigate rather than guess, correlate security evidence, identify an attack path/security weakness, assess risk, consult approved response guidance, and place high-impact remediation behind an approval boundary.

---

# 1. Scenario

Security Operations creates incident:

```text
SEC-2026-001
```

A deployment role associated with `payments-api` has generated unusual AWS API activity.

Your agent must determine:

```text
What happened?
      ↓
Which identity/resource is involved?
      ↓
What does CloudTrail show?
      ↓
Are there correlated security findings?
      ↓
Are vulnerabilities relevant?
      ↓
Did code/configuration create an attack path?
      ↓
What is the threat model?
      ↓
What is the risk?
      ↓
What remediation is appropriate?
      ↓
Does it require approval?
```

Do not encode the answer into the user prompt.

---

# 2. Security Agent Lifecycle

```text
DETECT
  ↓
TRIAGE
  ↓
COLLECT EVIDENCE
  ↓
CORRELATE
  ↓
THREAT MODEL
  ↓
RISK ASSESS
  ↓
CONSULT PLAYBOOK
  ↓
REMEDIATE / REQUEST APPROVAL
  ↓
VERIFY + OBSERVE
```

This lifecycle is the mental model participants should preserve even when the underlying security services change.

---

# 3. Architecture

```text
Security Analyst
      |
      v
AgentCore Harness
      |
      +-- Foundation Model
      +-- System Instructions
      +-- Inline Tool Contracts
      +-- Agent Loop
      |
      v
Client-side Python Functions
      |
      +-- Security Alert
      +-- CloudTrail Events
      +-- Security Findings
      +-- Vulnerability Findings
      +-- Code/IAM Review
      +-- Security Playbook
      +-- Controlled Remediation
      |
      v
Harness / Model
      |
      v
Evidence + Threat Model + Risk + Remediation
```

**Harness owns:** model configuration, instructions, tool contracts, orchestration/session loop and managed observability.

**Client owns:** inline-function implementation, security-system integration, deterministic validation, authorization and approval enforcement.

---

# 4. Create AgentCore Harness

AWS Console:

```text
Amazon Bedrock AgentCore
 → Harness
 → Create Harness
```

**Name**

```text
aws-security-investigation-agent
```

**Description**

```text
Evidence-driven AWS security investigation agent that correlates CloudTrail activity,
security findings, vulnerabilities and code/configuration weaknesses, assesses threat
and risk, consults approved response guidance, and requests controlled remediation.
```

Select a model available in the training account.

## System prompt

```text
You are an AWS Security Investigation Agent.

Your job is to investigate cloud-security incidents using evidence from the available tools.

Operating rules:
1. Never invent identities, events, vulnerabilities, findings, code defects, or remediation status.
2. Gather evidence before assigning a threat hypothesis or risk.
3. Correlate security alerts, CloudTrail activity, security findings, IAM posture, vulnerabilities, and code/configuration evidence when relevant.
4. Clearly separate observed evidence, threat hypothesis, affected assets, risk, confidence, and recommended remediation.
5. Treat a security finding as evidence, not automatically as proof of compromise.
6. Use code/configuration review to identify the security weakness that may have enabled or amplified the incident.
7. Consult the approved security response playbook before requesting remediation.
8. High-impact actions such as disabling credentials, quarantining a workload, changing IAM permissions, or blocking production access require approval.
9. Never claim that remediation was executed unless a tool explicitly reports successful execution.
10. If evidence is incomplete or contradictory, state the uncertainty and identify additional evidence required.

```

---

# 5. Configure Inline Custom Tools

## Tool 1 — `get_security_alert`

**Description**

```text
Retrieve the initial security incident/alert, including severity, affected identity or resource, detection time and observed indicators. Use this to establish investigation scope before deeper analysis.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "incident_id": {
      "type": "string",
      "description": "Security incident identifier, for example SEC-2026-001."
    }
  },
  "required": [
    "incident_id"
  ]
}
```

## Tool 2 — `get_cloudtrail_events`

**Description**

```text
Retrieve CloudTrail-like AWS API activity for an identity or resource over a recent time window. Use this to investigate who performed which API actions, from where, and whether sensitive or unusual AWS operations occurred.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "principal": {
      "type": "string",
      "description": "IAM principal, role, user, or session to investigate."
    },
    "minutes": {
      "type": "integer",
      "description": "Recent activity window in minutes.",
      "minimum": 1,
      "maximum": 1440
    }
  },
  "required": [
    "principal"
  ]
}
```

## Tool 3 — `get_security_findings`

**Description**

```text
Retrieve correlated GuardDuty/Security Hub-style security findings for an asset or principal. Use this to identify detections, severity, suspicious behavior and affected resources that may support or challenge a threat hypothesis.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "resource": {
      "type": "string",
      "description": "Resource, workload, or principal for which security findings should be retrieved."
    }
  },
  "required": [
    "resource"
  ]
}
```

## Tool 4 — `get_vulnerability_findings`

**Description**

```text
Retrieve Inspector-style vulnerability findings for a workload or software component. Use this to determine whether known vulnerabilities materially affect the incident risk or attack path.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "resource": {
      "type": "string",
      "description": "Workload, image, instance, package, or resource to inspect for vulnerabilities."
    }
  },
  "required": [
    "resource"
  ]
}
```

## Tool 5 — `review_security_code`

**Description**

```text
Review a named deployment/configuration artifact for predefined security weaknesses such as excessive IAM permissions, unsafe secret handling, public exposure, or insecure configuration. Use this when code or configuration may have enabled the security incident.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "artifact_name": {
      "type": "string",
      "description": "Name of the code, IAM policy, deployment template, or configuration artifact to review."
    }
  },
  "required": [
    "artifact_name"
  ]
}
```

## Tool 6 — `get_security_playbook`

**Description**

```text
Retrieve approved security investigation and remediation guidance for a threat or weakness. Use this before recommending or requesting containment/remediation so the response follows enterprise security procedure.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "topic": {
      "type": "string",
      "description": "Security threat, weakness, or remediation topic to look up."
    }
  },
  "required": [
    "topic"
  ]
}
```

## Tool 7 — `request_security_remediation`

**Description**

```text
Request a controlled security remediation such as disable_credentials, restrict_iam, quarantine_workload, rotate_secret, or block_public_access. The lab does not execute high-impact production changes; it returns the approval requirement. Use only after evidence and playbook guidance support the action.
```

**JSON input schema**

```json
{
  "type": "object",
  "properties": {
    "target": {
      "type": "string",
      "description": "Identity, workload, resource, or configuration targeted by remediation."
    },
    "action": {
      "type": "string",
      "enum": [
        "disable_credentials",
        "restrict_iam",
        "quarantine_workload",
        "rotate_secret",
        "block_public_access"
      ],
      "description": "Requested security remediation."
    },
    "reason": {
      "type": "string",
      "description": "Evidence-based reason for the remediation request."
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

## Security data is evidence

Do not allow the model to invent CloudTrail activity or vulnerabilities. Operational/security facts come from tools.

## Finding ≠ confirmed compromise

A finding raises or lowers confidence. The model must correlate it with audit activity and affected resources.

## Threat model

For this lab, ask the agent to reason in a compact structure:

```text
Asset
Threat Actor / Principal
Entry Point
Weakness
Observed Actions
Potential Impact
Existing Controls
Risk
```

The model may infer a threat hypothesis, but it must identify which parts are observed and which are inferred.

## Code review

The code-review tool is deterministic in the lab. It exposes a predefined IAM/configuration artifact and identified weaknesses. The LLM interprets the security consequence.

## Risk

Risk should consider:
- evidence strength;
- privilege level;
- affected asset sensitivity;
- exploitability/attack path;
- blast radius;
- vulnerability relevance;
- potential confidentiality/integrity/availability impact.

## Remediation authority

```text
INVESTIGATE / READ
security alert
CloudTrail
findings
vulnerabilities
code/configuration
playbook

CHANGE / CONTAIN
disable credentials
restrict IAM
quarantine workload
rotate secret
block public access
        ↓
APPROVAL REQUIRED
```

---

# 7. Python Client Requirements

The client must:

1. Read `HARNESS_ARN` and `AWS_REGION` from environment.
2. Create a UUID session ID.
3. Invoke AgentCore Harness.
4. process the response stream.
5. detect inline tool requests.
6. execute the corresponding deterministic Python function.
7. return the assistant `toolUse` and matching user `toolResult`.
8. continue until a final response is produced.
9. display tool requests/results for learning and debugging.

```bash
export AWS_REGION="ap-south-1"
export HARNESS_ARN="<your-harness-arn>"
```

---

# 8. Test Prompts

### Investigation

```text
Investigate security incident SEC-2026-001. Determine what happened and which assets or
identities are affected. Use security evidence rather than assumptions. Separate observed
evidence from your threat hypothesis.
```

### Threat analysis

```text
Investigate SEC-2026-001. Correlate audit activity, security findings, vulnerabilities
and configuration evidence. Produce a compact threat model covering asset, principal,
entry point, weakness, observed actions, potential impact and risk.
```

### Code review

```text
Investigate SEC-2026-001 and determine whether code, IAM policy or deployment configuration
contributed to the incident. Do not infer a weakness without reviewing the relevant artifact.
```

### Risk + remediation

```text
Perform a complete investigation of SEC-2026-001. Assess the security risk, consult the
approved response playbook, and request the safest remediation if evidence is sufficient.
Do not bypass approval requirements.
```

---

# 9. Expected Evidence Pattern

The lab is intentionally designed so the agent must correlate:

```text
Alert
  ↓
deployment role used unexpectedly
  ↓
CloudTrail
  ↓
role enumerated secrets and read one production secret
  ↓
security finding
  ↓
unusual secret-access behavior
  ↓
IAM/code review
  ↓
role policy contains overly broad secretsmanager:GetSecretValue
  ↓
vulnerability data
  ↓
no critical workload CVE explaining this identity behavior
  ↓
Threat hypothesis
  ↓
over-privileged deployment role used to access production secret
  ↓
Risk
  ↓
HIGH
  ↓
Playbook
  ↓
restrict IAM + rotate exposed secret / credential containment
  ↓
PENDING_APPROVAL
```

The vulnerability tool is deliberately useful even when the result is negative: it helps eliminate an alternative attack path.

---

# 10. Observability

After invocation:

```text
CloudWatch
 → GenAI Observability
 → Bedrock AgentCore
 → Harnesses / All traces
```

Inspect:
- complete security-investigation trace;
- model spans;
- tool spans;
- order of evidence collection;
- latency;
- errors;
- whether remediation was requested prematurely.

Discussion:
1. Which evidence materially changed the threat hypothesis?
2. Did the model distinguish finding from proof?
3. Did it use negative vulnerability evidence correctly?
4. Did it review configuration before blaming IAM?
5. Did it consult the playbook before remediation?
6. What sensitive data should be redacted from traces?

---

# 11. Production Evolution

```text
Mock CloudTrail      → CloudTrail / CloudTrail Lake
Mock findings        → Security Hub / GuardDuty
Mock vulnerabilities → Amazon Inspector
Mock code review     → repository/IaC scanner/policy analyzer
Mock playbook        → Bedrock Knowledge Base / approved SOP
Mock remediation     → controlled security automation + approval workflow
```

## Completion checklist

- [ ] Fresh Harness created
- [ ] System prompt configured
- [ ] Seven inline tools configured
- [ ] Python client connected
- [ ] Incident triage succeeds
- [ ] CloudTrail evidence inspected
- [ ] Security findings correlated
- [ ] Vulnerability evidence considered
- [ ] Code/IAM artifact reviewed
- [ ] Threat model produced
- [ ] Risk assessed
- [ ] Playbook consulted
- [ ] Remediation remains approval-controlled
- [ ] Agent trace inspected
