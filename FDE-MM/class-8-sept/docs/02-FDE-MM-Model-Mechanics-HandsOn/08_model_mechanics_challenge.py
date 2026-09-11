"""
FDE-MM Lab 08 — Mini Model Mechanics Challenge

A small interactive exercise. No special UI/framework required.
Participants make model-mechanics decisions, then optionally call the model.
"""

from openai import OpenAI

BASE_URL = "https://api.openai.com/v1"
API_KEY = "PASTE_YOUR_KEY_HERE"
MODEL = "gpt-4.1-mini"
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

SCENARIO = """
A retailer wants an AI support assistant.

Facts:
- Return policies change every month.
- Live order status comes from an Order API.
- Most requests are routine.
- High-value refunds require manager approval.
- The customer asks: "Can we fine-tune one very powerful model on everything
  and let it handle the complete process?"
"""

QUESTIONS = [
    "Where should changing return-policy knowledge come from: model weights, RAG, or API?",
    "Where should live order status come from?",
    "Should high-value refund approval be probabilistic or deterministic/governed?",
    "Would you fine-tune immediately? Why?",
    "Would one model necessarily be optimal for all requests?",
]

if __name__ == "__main__":
    print("=" * 78)
    print("SCENARIO")
    print("=" * 78)
    print(SCENARIO)

    answers = []
    for i, q in enumerate(QUESTIONS, 1):
        print(f"\n{i}. {q}")
        answers.append(input("Your answer: ").strip())

    print("\n" + "=" * 78)
    print("YOUR ARCHITECTURE THINKING")
    print("=" * 78)
    for q, a in zip(QUESTIONS, answers):
        print("\nQ:", q)
        print("A:", a)

    print("\n" + "=" * 78)
    print("OPTIONAL MODEL CRITIQUE")
    print("=" * 78)
    print("The model will critique the reasoning, not provide a single 'magic' architecture.")

    joined = "\n".join(f"{i+1}. {a}" for i, a in enumerate(answers))
    response = client.responses.create(
        model=MODEL,
        temperature=0.2,
        max_output_tokens=400,
        input=f"""
You are reviewing an FDE model-mechanics decision exercise.

SCENARIO:
{SCENARIO}

PARTICIPANT ANSWERS:
{joined}

Give concise feedback under:
1. Good decisions
2. Risks/missing considerations
3. Model-mechanics principle to remember

Focus on context vs model weights, live tools, deterministic controls,
evaluation, model selection, and production risk.
""",
    )
    print(response.output_text)
