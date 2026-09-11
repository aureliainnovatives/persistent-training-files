import os

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
HARNESS_ARN = os.getenv("HARNESS_ARN", "")

DEFAULT_PROMPT = (
    "Perform a complete FinOps investigation of retail-platform. Analyze the current cost "
    "increase and anomalies, investigate resource utilization and right-sizing, evaluate "
    "non-production scheduling and Savings Plans opportunities, forecast month-end spend "
    "against budget, consult the FinOps policy, and request the best supported optimization "
    "action without bypassing approval requirements."
)

def validate_config():
    if not HARNESS_ARN:
        raise RuntimeError("HARNESS_ARN is not configured.")
