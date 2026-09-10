# AWS DevOps Incident Agent — Python Client

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export AWS_REGION="ap-south-1"
export HARNESS_ARN="<your Harness ARN>"

python main.py
```

Files:
- `main.py` — Harness invocation/inline-function continuation loop.
- `devops_tools.py` — deterministic mock operational integrations.
- `config.py` — environment configuration and default prompt.
- `.env.example` — configuration reference.

The Harness must contain the seven inline tools described in the participant specification,
with names matching `HANDLERS` exactly.

If the current AgentCore SDK in the lab emits a different streaming tool-use event shape,
reuse the known-working stream parser from your existing Harness client. The tool
implementations and contracts in this project remain valid.
