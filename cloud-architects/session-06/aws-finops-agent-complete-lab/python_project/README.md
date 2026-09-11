# AWS FinOps Agent — Python Project

Fresh AgentCore Harness client implementation for the FinOps lab.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export AWS_REGION="ap-south-1"
export HARNESS_ARN="<your fresh FinOps Harness ARN>"

python main.py
```

The eight Harness inline function names must exactly match `HANDLERS` in `finops_tools.py`.

The lab intentionally mocks billing and operational systems so participants can reason
about FinOps safely. Replace the mocks with Cost Explorer, Cost Anomaly Detection,
CloudWatch/Compute Optimizer, Savings Plans recommendations and AWS Budgets as extensions.
