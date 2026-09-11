"""
FDE-MM Lab 03 — Token & Context Budget Mechanics

No API key required.
Uses tiktoken to make prompt growth visible.
"""

import tiktoken

MODEL_FOR_TOKENIZER = "gpt-4o-mini"

try:
    enc = tiktoken.encoding_for_model(MODEL_FOR_TOKENIZER)
except KeyError:
    enc = tiktoken.get_encoding("o200k_base")

SYSTEM = "You are an enterprise insurance claims assistant."
QUESTION = "Should this motor claim be referred for investigation?"

CURRENT_POLICY = """
CURRENT POLICY:
A theft claim submitted within 7 days of a substantial coverage increase
must be referred for investigation.
"""

OLD_POLICY = """
OLD POLICY:
A theft claim requires investigation only if the customer has held the
policy for fewer than 12 months.
"""

UNRELATED = """
TRAVEL POLICY:
Employees travelling domestically may claim hotel expenses according to
their grade and approved city limits.
""" * 20

def count_tokens(text):
    return len(enc.encode(text))

def report(name, text):
    print("\n" + "=" * 78)
    print(name)
    print("=" * 78)
    print(f"Characters: {len(text):,}")
    print(f"Approx tokenizer count: {count_tokens(text):,} tokens")

def budget(context_limit, input_text, reserved_output):
    used = count_tokens(input_text)
    remaining = context_limit - used - reserved_output
    print(f"Context limit used for demo : {context_limit}")
    print(f"Input tokens                : {used}")
    print(f"Reserved output tokens      : {reserved_output}")
    print(f"Remaining budget            : {remaining}")
    if remaining < 0:
        print("WARNING: Budget exceeded.")
    elif remaining < context_limit * 0.1:
        print("WARNING: Very little headroom remains.")

if __name__ == "__main__":
    minimal = SYSTEM + "\n" + QUESTION
    clean = minimal + "\n" + CURRENT_POLICY
    conflicting = clean + "\n" + OLD_POLICY
    noisy = conflicting + "\n" + UNRELATED

    report("1 — Minimal prompt", minimal)
    report("2 — Add relevant policy", clean)
    report("3 — Add conflicting old policy", conflicting)
    report("4 — Add lots of irrelevant context", noisy)

    print("\n" + "=" * 78)
    print("CONTEXT BUDGET DEMO")
    print("=" * 78)
    print("We use an intentionally small 2,000-token context limit for teaching.")
    budget(context_limit=2000, input_text=noisy, reserved_output=400)

    print("\n[FDE TAKEAWAY]")
    print("""
A model can only reason over what reaches its effective context.
More context consumes budget and can introduce conflict/noise.
Ask:
- What MUST be present?
- What can be retrieved on demand?
- What can be summarized?
- What should never be included?
- How much output budget does the business task actually need?
""")
