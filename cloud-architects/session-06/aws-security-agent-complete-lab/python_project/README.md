# AWS Security Agent — Python Project

Fresh client-side implementation for the AgentCore Harness security lab.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export AWS_REGION="ap-south-1"
export HARNESS_ARN="<your fresh security Harness ARN>"

python main.py
```

## Files

- `main.py` — Harness invocation and inline-function continuation loop.
- `security_tools.py` — deterministic mock security systems.
- `config.py` — environment and default investigation prompt.
- `.env.example` — configuration template.

The seven function names in the Harness must exactly match `HANDLERS` in `security_tools.py`.

The mocks are deliberate: participants can learn agent architecture without requiring a real security compromise. Later replace them with CloudTrail, Security Hub/GuardDuty, Inspector, IAM/code analysis and approved remediation workflows.
