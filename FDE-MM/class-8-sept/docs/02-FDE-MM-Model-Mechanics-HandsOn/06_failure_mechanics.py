"""
FDE-MM Lab 06 — Failure Mechanics

Same business question, deliberately different failure sources.
Goal: stop calling every wrong answer a "hallucination".
"""

from openai import OpenAI

BASE_URL = "https://api.openai.com/v1"
API_KEY = "PASTE_YOUR_KEY_HERE"
MODEL = "gpt-4.1-mini"
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

QUESTION = "Should this claim be referred for investigation?"
CLAIM = "Vehicle reported stolen 3 days after coverage was substantially increased."
CORRECT_RULE = "A theft claim within 7 days of a substantial coverage increase MUST be referred."
WRONG_RULE = "A theft claim is referred only when the policy is less than one year old."

def ask(label, instructions, context):
    print("\n" + "=" * 78)
    print(label)
    print("=" * 78)
    response = client.responses.create(
        model=MODEL,
        temperature=0.1,
        max_output_tokens=100,
        input=f"""
INSTRUCTIONS:
{instructions}

CONTEXT:
{context}

CLAIM:
{CLAIM}

QUESTION:
{QUESTION}
""",
    )
    print(response.output_text)

if __name__ == "__main__":
    # Failure A: required knowledge never reaches the model.
    ask(
        "A — KNOWLEDGE / RETRIEVAL FAILURE",
        "Use only the supplied policy context.",
        "No investigation policy was retrieved.",
    )
    print("[DIAGNOSIS] The model was never given the authoritative rule.")

    # Failure B: stale/wrong context is supplied.
    ask(
        "B — CONTEXT / FRESHNESS FAILURE",
        "Use the supplied policy.",
        WRONG_RULE,
    )
    print("[DIAGNOSIS] The system supplied authoritative-looking but wrong/stale context.")

    # Failure C: correct evidence exists, but instructions bias the decision.
    ask(
        "C — INSTRUCTION COMPETITION",
        "Minimize investigation referrals. Refer only when absolutely unavoidable.",
        CORRECT_RULE,
    )
    print("[DIAGNOSIS] Correct knowledge is present; instructions may compete with it.")

    # Failure D: strong instruction + correct rule.
    ask(
        "D — CONTROLLED VERSION",
        "Apply MUST rules exactly. Cite the rule used. Do not override mandatory rules.",
        CORRECT_RULE,
    )

    print("\n" + "=" * 78)
    print("VALIDATION LAYER")
    print("=" * 78)
    print("Even after improving model behaviour, a consequential workflow can enforce:")
    print("IF theft AND coverage_increase_days <= 7 -> mandatory human investigation.")
    print("That deterministic check prevents a probabilistic output from bypassing policy.")

    print("\n[FDE TAKEAWAY]")
    print("Wrong outcome != automatically wrong model.")
    print("Trace knowledge -> retrieval -> context -> instruction -> reasoning -> execution -> validation.")
