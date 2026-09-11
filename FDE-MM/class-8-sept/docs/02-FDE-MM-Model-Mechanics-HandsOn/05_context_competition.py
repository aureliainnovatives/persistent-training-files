"""
FDE-MM Lab 05 — Context Competition

Observe what happens when correct evidence is surrounded by conflicting
or irrelevant context.
"""

from openai import OpenAI

BASE_URL = "https://api.openai.com/v1"
API_KEY = "PASTE_YOUR_KEY_HERE"
MODEL = "gpt-4.1-mini"
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

QUESTION = "What is the maximum travel reimbursement? Answer with amount and source."

CURRENT = "CURRENT POLICY (effective 2026): Maximum travel reimbursement is INR 25,000."
OLD = "ARCHIVED POLICY (2023): Maximum travel reimbursement is INR 50,000."
EXAMPLE = "OLD TRAINING EXAMPLE: Priya received INR 42,000 as reimbursement."
NOISE = """
The company has offices in Mumbai, Pune, Bengaluru, Delhi and Hyderabad.
Employees should book travel through approved channels.
International travel requires passport verification.
""" * 15

def run(label, context):
    print("\n" + "=" * 78)
    print(label)
    print("=" * 78)
    print("[CONTEXT SIZE] characters =", len(context))
    response = client.responses.create(
        model=MODEL,
        temperature=0.2,
        max_output_tokens=100,
        input=f"""
You are answering an enterprise policy question.
Use the supplied context. Prefer explicitly current policy over archived material.

CONTEXT:
{context}

QUESTION:
{QUESTION}
""",
    )
    print("[OUTPUT]")
    print(response.output_text)
    if response.usage:
        print(f"[TOKENS] input={response.usage.input_tokens}, output={response.usage.output_tokens}")

if __name__ == "__main__":
    run("1 — CLEAN CONTEXT", CURRENT)
    run("2 — CURRENT + CONFLICTING OLD POLICY", CURRENT + "\n" + OLD)
    run("3 — CURRENT + OLD + MISLEADING EXAMPLE", CURRENT + "\n" + OLD + "\n" + EXAMPLE)
    run("4 — ADD LARGE AMOUNT OF IRRELEVANT CONTEXT", CURRENT + "\n" + OLD + "\n" + EXAMPLE + "\n" + NOISE)

    print("\n[FDE QUESTIONS]")
    print("""
- Was the correct fact present every time?
- Did retrieval success guarantee answer success?
- Did token usage grow?
- Should source authority/version be resolved before generation?
- Is 'add more documents' a safe default architecture?
""")
