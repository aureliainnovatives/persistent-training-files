import os

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
HARNESS_ARN = os.getenv("HARNESS_ARN", "")

DEFAULT_PROMPT = (
    "Perform a complete investigation of security incident SEC-2026-001. "
    "Correlate audit activity, findings, vulnerabilities and relevant code/configuration evidence. "
    "Produce a threat model and risk assessment, consult the approved security playbook, "
    "and request the safest remediation if the evidence is sufficient. "
    "Do not bypass approval requirements."
)

def validate_config():
    if not HARNESS_ARN:
        raise RuntimeError("HARNESS_ARN is not configured.")
