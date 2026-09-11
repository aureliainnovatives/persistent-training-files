"""
FDE-MM Lab 01 — OpenAI-Compatible Inference Mechanics

Goal:
Observe how inference controls affect model behaviour.

IMPORTANT:
Credentials are deliberately in code for this classroom demo, as requested.
Do NOT commit a real API key to source control.
"""

from openai import OpenAI

# ---------------------------------------------------------------------------
# EDIT THESE THREE VALUES
# ---------------------------------------------------------------------------
BASE_URL = "https://api.openai.com/v1"
API_KEY = "PASTE_YOUR_KEY_HERE"
MODEL = "gpt-4.1-mini"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

PROMPT = """
You are advising an insurance company.
A customer reports a stolen vehicle three days after substantially increasing
insurance coverage. Give a short risk assessment in no more than 70 words.
"""

def banner(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)

def show_usage(response):
    """Print token accounting returned by the provider."""
    usage = getattr(response, "usage", None)
    if not usage:
        print("[USAGE] No usage object returned by this endpoint.")
        return

    print(f"[USAGE] input_tokens  = {getattr(usage, 'input_tokens', 'n/a')}")
    print(f"[USAGE] output_tokens = {getattr(usage, 'output_tokens', 'n/a')}")
    print(f"[USAGE] total_tokens  = {getattr(usage, 'total_tokens', 'n/a')}")

    details = getattr(usage, "input_tokens_details", None)
    if details:
        print(f"[USAGE] cached_tokens = {getattr(details, 'cached_tokens', 0)}")
        print("        ^ Provider-side cached prompt tokens, if supported/reported.")

def call_model(label, *, temperature=None, top_p=None, max_output_tokens=120):
    banner(label)

    print(f"[CONFIG] model             = {MODEL}")
    print(f"[CONFIG] temperature       = {temperature}")
    print(f"[CONFIG] top_p             = {top_p}")
    print(f"[CONFIG] max_output_tokens = {max_output_tokens}")

    if temperature is not None:
        print("[OBSERVE] Higher temperature generally permits more output variation.")
    if top_p is not None:
        print("[OBSERVE] Lower top_p narrows sampling to a smaller probability mass.")
    print("[NOTE] Normally tune temperature OR top_p, rather than aggressively changing both.")

    kwargs = {
        "model": MODEL,
        "input": PROMPT,
        "max_output_tokens": max_output_tokens,
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
    if top_p is not None:
        kwargs["top_p"] = top_p

    try:
        response = client.responses.create(**kwargs)
        print("\n[MODEL OUTPUT]")
        print(response.output_text)
        print()
        show_usage(response)
        return response
    except Exception as exc:
        print("\n[REQUEST FAILED]")
        print(exc)
        print("\nSome models/providers do not expose every sampling parameter.")
        print("Try a compatible model, or remove the unsupported parameter.")
        return None

if __name__ == "__main__":
    banner("EXPERIMENT 1 — Low vs High Temperature")
    print("We keep the business prompt constant and change sampling behaviour.")

    call_model(
        "1A — LOWER TEMPERATURE: expect relatively constrained behaviour",
        temperature=0.1,
        max_output_tokens=120,
    )
    call_model(
        "1B — HIGHER TEMPERATURE: observe whether wording/reasoning varies more",
        temperature=1.2,
        max_output_tokens=120,
    )

    banner("EXPERIMENT 2 — TOP-P / NUCLEUS SAMPLING")
    print("Now vary top_p separately. We intentionally do not set temperature.")
    call_model(
        "2A — NARROWER TOP-P",
        top_p=0.2,
        max_output_tokens=120,
    )
    call_model(
        "2B — WIDER TOP-P",
        top_p=1.0,
        max_output_tokens=120,
    )

    banner("EXPERIMENT 3 — OUTPUT TOKEN BUDGET")
    call_model(
        "3A — SMALL OUTPUT BUDGET",
        temperature=0.2,
        max_output_tokens=40,
    )
    call_model(
        "3B — LARGER OUTPUT BUDGET",
        temperature=0.2,
        max_output_tokens=180,
    )

    banner("EXPERIMENT 4 — SAME REQUEST, MULTIPLE RUNS")
    print("Run the same configuration three times.")
    print("Question: does an LLM behave like a deterministic REST lookup?\n")
    for i in range(1, 4):
        call_model(
            f"Repeated run {i}",
            temperature=0.8,
            max_output_tokens=100,
        )

    banner("FDE TAKEAWAY")
    print("""
Do not choose inference parameters because they 'look standard'.
Choose them because the workload has a required behaviour.

Examples:
- creative ideation may tolerate variation;
- extraction/classification should usually be more constrained;
- consequential decisions need validation even if decoding is constrained;
- max_output_tokens is both a behavioural and cost/latency control.
""")
