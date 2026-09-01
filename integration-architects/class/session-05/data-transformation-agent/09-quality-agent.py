"""
DATA QUALITY AGENT
Uses deterministic validation results first.
The LLM may classify/remediate only according to explicit guardrails:
safe normalization vs quarantine. It must not invent customer data.
"""
import json, os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE = Path(__file__).resolve().parent
load_dotenv(BASE/".env")

key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

def main():
    invalid = json.loads((BASE/"output"/"invalid.json").read_text())
    if not key:
        print("OPENAI_API_KEY not configured; deterministic validator output remains in output/invalid.json")
        return

    client = OpenAI(api_key=key, base_url=base_url)
    prompt = """You are a governed data-quality agent.
For each invalid record, decide either SAFE_REPAIR or QUARANTINE.
SAFE_REPAIR is allowed only for deterministic formatting/normalization already implied by the rules.
Never invent missing IDs, names, email addresses, phone digits, or state meanings.
Return JSON only: {"decisions":[{"customerId": "...", "action":"SAFE_REPAIR|QUARANTINE","reason":"..."}]}.
Invalid records:
""" + json.dumps(invalid)

    resp = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[{"role":"user","content":prompt}]
    )
    text = resp.choices[0].message.content
    (BASE/"output"/"quality-agent-decisions.json").write_text(text)
    print(text)

if __name__ == "__main__":
    main()
