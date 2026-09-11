"""Mock security systems used by the AgentCore Harness inline tools."""

from copy import deepcopy
from datetime import datetime

INCIDENT = {
    "incident_id": "SEC-2026-001",
    "severity": "HIGH",
    "status": "INVESTIGATING",
    "detected_at": "2026-09-09T14:16:00+05:30",
    "principal": "payments-deploy-role",
    "resource": "payments-api",
    "indicator": "Unusual production secret access by deployment role",
    "region": "ap-south-1",
}

CLOUDTRAIL = {
    "payments-deploy-role": [
        {
            "eventTime": "2026-09-09T14:12:08+05:30",
            "eventName": "ListSecrets",
            "eventSource": "secretsmanager.amazonaws.com",
            "sourceIPAddress": "198.51.100.24",
            "userAgent": "aws-cli",
            "response": "Success",
        },
        {
            "eventTime": "2026-09-09T14:13:11+05:30",
            "eventName": "GetSecretValue",
            "eventSource": "secretsmanager.amazonaws.com",
            "resource": "prod/payments/database",
            "sourceIPAddress": "198.51.100.24",
            "userAgent": "aws-cli",
            "response": "Success",
        },
    ]
}

FINDINGS = {
    "payments-api": [
        {
            "finding_id": "FIND-7781",
            "source": "GuardDuty-like detector",
            "severity": "HIGH",
            "title": "Anomalous Secrets Manager access by deployment role",
            "principal": "payments-deploy-role",
            "resource": "prod/payments/database",
            "evidence": "Secret read from source/session context not observed in normal deployment activity.",
        }
    ],
    "payments-deploy-role": [
        {
            "finding_id": "FIND-7781",
            "source": "GuardDuty-like detector",
            "severity": "HIGH",
            "title": "Anomalous Secrets Manager access by deployment role",
            "principal": "payments-deploy-role",
            "resource": "prod/payments/database",
            "evidence": "Secret read from source/session context not observed in normal deployment activity.",
        }
    ]
}

VULNERABILITIES = {
    "payments-api": [
        {
            "id": "CVE-2026-LAB-101",
            "severity": "LOW",
            "package": "example-logging-lib",
            "status": "OPEN",
            "relevance": "No known path from this issue to AWS identity credential or Secrets Manager access.",
        }
    ]
}

ARTIFACTS = {
    "payments-deploy-policy.json": {
        "type": "IAM policy",
        "content": {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": [
                    "ecs:UpdateService",
                    "ecs:DescribeServices",
                    "secretsmanager:ListSecrets",
                    "secretsmanager:GetSecretValue"
                ],
                "Resource": "*"
            }]
        },
        "review_findings": [
            {
                "severity": "HIGH",
                "issue": "Overly broad Secrets Manager read permission",
                "evidence": "secretsmanager:GetSecretValue is allowed with Resource:*",
                "recommendation": "Restrict secret access to only explicitly required deployment resources; remove secret-read permission if not required."
            }
        ]
    }
}

PLAYBOOK = {
    "title": "Playbook - Suspicious Privileged Identity and Secret Access",
    "investigation": [
        "Preserve CloudTrail and correlated finding evidence.",
        "Validate whether the API activity is expected for the role.",
        "Review effective IAM permissions and recent policy changes.",
        "Determine which secrets were accessed.",
        "Assess whether vulnerable workloads provide a plausible alternative attack path.",
    ],
    "remediation": [
        "Contain suspicious credentials/session according to incident policy.",
        "Reduce excessive IAM permissions to least privilege.",
        "Rotate secrets that may have been exposed.",
        "Validate dependent workloads after rotation.",
        "Continue monitoring for follow-on activity.",
    ],
    "approval": "Credential disablement, IAM changes, workload quarantine and production secret rotation require human approval in this lab."
}


def get_security_alert(incident_id: str):
    if incident_id != INCIDENT["incident_id"]:
        return {"error": f"Security incident {incident_id} not found"}
    return deepcopy(INCIDENT)


def get_cloudtrail_events(principal: str, minutes: int = 60):
    events = CLOUDTRAIL.get(principal)
    if events is None:
        return {"error": f"No CloudTrail-like events found for {principal}"}
    return {"principal": principal, "minutes": minutes, "events": deepcopy(events)}


def get_security_findings(resource: str):
    return {"resource": resource, "findings": deepcopy(FINDINGS.get(resource, []))}


def get_vulnerability_findings(resource: str):
    return {"resource": resource, "findings": deepcopy(VULNERABILITIES.get(resource, []))}


def review_security_code(artifact_name: str):
    artifact = ARTIFACTS.get(artifact_name)
    if artifact is None:
        return {
            "error": f"Artifact {artifact_name} not found",
            "available_artifacts": list(ARTIFACTS.keys()),
        }
    result = deepcopy(artifact)
    result["artifact_name"] = artifact_name
    return result


def get_security_playbook(topic: str):
    q = topic.lower()
    if any(x in q for x in ["secret", "identity", "credential", "iam", "privilege"]):
        result = deepcopy(PLAYBOOK)
        result["requested_topic"] = topic
        return result
    return {"error": f"No security playbook found for topic: {topic}"}


def request_security_remediation(target: str, action: str, reason: str):
    allowed = {
        "disable_credentials",
        "restrict_iam",
        "quarantine_workload",
        "rotate_secret",
        "block_public_access",
    }
    if action not in allowed:
        return {"status": "REJECTED", "reason": "Unsupported action", "allowed_actions": sorted(allowed)}

    return {
        "request_id": f"SECCHG-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "target": target,
        "action": action,
        "reason": reason,
        "risk_control": "HUMAN_APPROVAL",
        "status": "PENDING_APPROVAL",
        "executed": False,
        "message": "The requested high-impact security change has not been executed. Human approval is required.",
    }


HANDLERS = {
    "get_security_alert": get_security_alert,
    "get_cloudtrail_events": get_cloudtrail_events,
    "get_security_findings": get_security_findings,
    "get_vulnerability_findings": get_vulnerability_findings,
    "review_security_code": review_security_code,
    "get_security_playbook": get_security_playbook,
    "request_security_remediation": request_security_remediation,
}


def execute_tool(name, arguments):
    if name not in HANDLERS:
        raise ValueError(f"No local implementation for inline function: {name}")
    return HANDLERS[name](**arguments)
