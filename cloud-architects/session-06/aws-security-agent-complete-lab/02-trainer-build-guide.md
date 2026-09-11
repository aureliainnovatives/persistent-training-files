# Trainer Reference — AWS Security Agent

## Exact module coverage

This implementation deliberately covers the five requested areas:

```text
Security agent lifecycle and configuration
Threat analysis and modelling
Code review
Security data sources: CloudTrail, findings, vulnerabilities
Risk detection and remediation
```

It is a fresh lab and does not depend on the DevOps Agent or previous AgentCore resources.

---

# 1. Trainer Story

A `payments-api` deployment role has performed suspicious Secrets Manager activity.

Do not reveal the hidden RCA initially. Ask participants to identify:
- data sources;
- tools;
- evidence sequence;
- threat-model fields;
- risk factors;
- action boundaries.

Then reveal/build the prepared Harness.

---

# 2. Create Fresh Harness

```text
Amazon Bedrock AgentCore
 → Harness
 → Create Harness
```

Name:

```text
aws-security-investigation-agent
```

Description:

```text
Evidence-driven AWS security investigation agent that correlates CloudTrail activity,
security findings, vulnerabilities and code/configuration weaknesses, assesses threat
and risk, consults approved response guidance, and requests controlled remediation.
```

Choose an available model.

System prompt:

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

Add all seven inline tools from `01-participant-agent-spec.md`. A consolidated copy/paste JSON reference is provided in `03-harness-tool-schemas.json`.

Wait for READY and copy the Harness ARN.

---

# 3. Configure Project

```bash
cd python_project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export AWS_REGION="ap-south-1"
export HARNESS_ARN="<harness-arn>"

python main.py
```

---

# 4. Hidden Evidence — Trainer Only

## Initial alert

```text
SEC-2026-001
Severity: HIGH
Principal: payments-deploy-role
Resource: payments-api
Indicator: unusual production secret access
```

## CloudTrail-like activity

The role:
1. calls `ListSecrets`;
2. calls `GetSecretValue` for `prod/payments/database`;
3. activity originates from an unexpected source IP/session context.

## Security finding

A GuardDuty/Security Hub-like finding reports anomalous secret-access behavior by the deployment role.

## IAM/code artifact

`payments-deploy-policy.json` contains:

```json
{
  "Effect": "Allow",
  "Action": [
    "secretsmanager:ListSecrets",
    "secretsmanager:GetSecretValue"
  ],
  "Resource": "*"
}
```

This is intentionally broader than the deployment role needs.

## Vulnerability findings

No critical application vulnerability explains the identity-based secret access. This is useful **negative evidence**.

## Intended threat hypothesis

```text
An over-privileged deployment role was used from an anomalous context to enumerate and
read a production database secret. Excessive Secrets Manager permissions increased the
blast radius.
```

Do not overstate who the attacker is; the evidence does not establish a real-world actor.

## Risk

HIGH because:
- production secret accessed;
- privileged role;
- broad secret-read permission;
- possible credential exposure;
- confidentiality and downstream integrity risk.

## Playbook

Recommended:
- contain suspicious role/session;
- restrict IAM to least privilege;
- rotate potentially exposed production secret;
- preserve evidence;
- verify dependent services after rotation;
- high-impact production changes require approval.

---

# 5. Demonstration Flow

A useful broad sequence:

```text
get_security_alert
        ↓
get_cloudtrail_events
        ↓
get_security_findings
        ↓
review_security_code
        ↓
get_vulnerability_findings
        ↓
get_security_playbook
        ↓
request_security_remediation
```

Exact order may vary. Do not teach the sequence as a mandatory workflow unless required by policy.

---

# 6. Threat-Modelling Discussion

After evidence collection, ask the model/participants to structure:

```text
ASSET
Production payment/database secret

PRINCIPAL
payments-deploy-role

ENTRY POINT
Anomalous use of deployment-role session

WEAKNESS
Over-broad Secrets Manager permission

OBSERVED ACTION
ListSecrets + GetSecretValue

POTENTIAL IMPACT
Secret disclosure; downstream DB access

CONTROL GAP
Least privilege

RISK
High

RESPONSE
Contain identity, restrict policy, rotate secret
```

Emphasize:

> Threat modelling connects evidence into an attack-path hypothesis. It does not convert assumptions into facts.

---

# 7. Code Review Teaching Point

This module explicitly requires code review, so do not let it become an afterthought.

The agent calls:

```text
review_security_code("payments-deploy-policy.json")
```

The deterministic tool returns:
- artifact content;
- issue: wildcard resource;
- excessive secret-read capability;
- severity;
- recommendation.

Discuss the separation:

```text
Scanner/tool:
"This policy grants GetSecretValue on Resource:*"

Model:
"This weakness could increase blast radius and is relevant to the observed secret access."
```

The first is deterministic evidence; the second is contextual security reasoning.

---

# 8. Risk Detection

Do not reduce risk to one model-generated number.

Use dimensions:

```text
Evidence confidence
Privilege
Asset sensitivity
Exploitability
Blast radius
CIA impact
Existing controls
```

The model can produce `LOW / MEDIUM / HIGH / CRITICAL` with justification.

---

# 9. Remediation Boundary

The lab action function never actually disables identities or rotates secrets.

```text
Agent
  ↓
request_security_remediation()
  ↓
PENDING_APPROVAL
  ↓
Human / security change workflow
  ↓
Controlled execution
  ↓
Verification
```

This lets you discuss why security agents need stronger authorization boundaries than ordinary informational assistants.

---

# 10. Observability

Verify Transaction Search if needed:

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

Show:
- trace;
- model/tool spans;
- sequence;
- latency;
- errors.

Security-specific question:

> Should raw secrets, tokens or sensitive CloudTrail fields be placed into model context or traces?

Use this to introduce data minimization/redaction.

---

# 11. Production Replacements

```text
get_cloudtrail_events
    → CloudTrail / CloudTrail Lake

get_security_findings
    → Security Hub / GuardDuty

get_vulnerability_findings
    → Amazon Inspector

review_security_code
    → repository scanner / IAM Access Analyzer / IaC policy tooling

get_security_playbook
    → Bedrock Knowledge Base

request_security_remediation
    → Step Functions / Lambda / ticket/change workflow with approval
```

---

# 12. Final Trainer Mental Model

```text
                   SECURITY AGENT
                         |
       +-----------------+------------------+
       |                 |                  |
       v                 v                  v
    DETECT            ANALYZE             RESPOND
       |                 |                  |
 alert/findings      threat model       remediation
 CloudTrail          risk              approval
 vulnerabilities     code weakness         |
       +-----------------+------------------+
                         |
                         v
                 SECURITY POLICY
                         |
                         v
                  OBSERVABILITY
```
