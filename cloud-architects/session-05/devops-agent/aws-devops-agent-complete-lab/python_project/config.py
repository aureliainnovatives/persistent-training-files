import os

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
HARNESS_ARN = os.getenv("HARNESS_ARN", "")

DEFAULT_PROMPT = (
    "Investigate incident INC-DEVOPS-001. Determine the likely root cause, "
    "consult the relevant operational runbook, and request the safest remediation "
    "if the evidence is strong enough. Do not bypass production approval requirements."
)

def validate_config():
    if not HARNESS_ARN:
        raise RuntimeError("HARNESS_ARN is not configured.")
