"""
FDE-MM Lab 07 — Structured Output Reliability

Shows the difference between:
1) a nice natural-language answer, and
2) output that downstream software can safely parse and validate.

This demo uses JSON mode for broad compatibility and performs explicit
application validation. If your selected model/provider supports JSON Schema
Structured Outputs, that can provide even stronger schema enforcement.
"""

from openai import OpenAI
import json

BASE_URL = "https://api.openai.com/v1"
API_KEY = "PASTE_YOUR_KEY_HERE"
MODEL = "gpt-4.1-mini"
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

CLAIM = """
Vehicle reported stolen 3 days after a substantial coverage increase.
Current rule: this condition requires investigation.
"""

def validate(data):
    errors = []
    if data.get("risk") not in {"LOW", "MEDIUM", "HIGH"}:
        errors.append("risk must be LOW, MEDIUM, or HIGH")
    if not isinstance(data.get("refer_for_investigation"), bool):
        errors.append("refer_for_investigation must be boolean")
    if not data.get("reason"):
        errors.append("reason is required")
    return errors

if __name__ == "__main__":
    print("=" * 78)
    print("1 — FREE-TEXT OUTPUT")
    print("=" * 78)
    free = client.responses.create(
        model=MODEL,
        temperature=0.2,
        max_output_tokens=120,
        input=f"Assess this claim and explain what should happen:\n{CLAIM}",
    )
    print(free.output_text)
    print("\n[QUESTION] Could downstream code safely assume exact fields exist?")

    print("\n" + "=" * 78)
    print("2 — JSON OUTPUT + APPLICATION VALIDATION")
    print("=" * 78)

    structured = client.responses.create(
        model=MODEL,
        temperature=0.1,
        max_output_tokens=150,
        text={"format": {"type": "json_object"}},
        input=f"""
Return JSON only with exactly these logical fields:
risk: LOW, MEDIUM, or HIGH
refer_for_investigation: true or false
reason: short string

Assess:
{CLAIM}
""",
    )

    print("[RAW MODEL OUTPUT]")
    print(structured.output_text)

    try:
        data = json.loads(structured.output_text)
        print("\n[PARSE] JSON parsed successfully.")
        errors = validate(data)
        if errors:
            print("[BUSINESS VALIDATION] FAILED")
            for e in errors:
                print(" -", e)
        else:
            print("[BUSINESS VALIDATION] PASSED")
            print("[SAFE NEXT STEP] Output has the expected application-level contract.")
    except json.JSONDecodeError as exc:
        print("[PARSE] FAILED:", exc)

    print("\n[FDE TAKEAWAY]")
    print("""
Syntactic validity and business correctness are different:
- valid JSON can contain a wrong risk decision;
- a correct prose answer may be unusable by software;
- production systems need schema + semantic/business validation.
""")
