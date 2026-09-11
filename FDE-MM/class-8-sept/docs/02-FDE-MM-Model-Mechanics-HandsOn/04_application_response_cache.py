"""
FDE-MM Lab 04 — Simple In-Memory Application Response Cache

This is APPLICATION-LEVEL RESPONSE CACHING.
It is intentionally NOT Redis and NOT provider-side KV/prompt caching.

Same model + prompt + parameters -> reuse the stored response.
"""

from openai import OpenAI
import hashlib
import json
import time

BASE_URL = "https://api.openai.com/v1"
API_KEY = "PASTE_YOUR_KEY_HERE"
MODEL = "gpt-4.1-mini"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Process-local memory only. Restarting Python clears the cache.
CACHE = {}

def make_cache_key(model, prompt, temperature, max_output_tokens):
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }
    canonical = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()

def ask(prompt, temperature=0.2, max_output_tokens=120):
    key = make_cache_key(MODEL, prompt, temperature, max_output_tokens)

    print("\n[CACHE KEY]", key[:16] + "...")

    if key in CACHE:
        print("[CACHE HIT] No model API call is made.")
        print("[TOKEN CONSEQUENCE] Provider receives 0 tokens for this cached application response.")
        return CACHE[key]

    print("[CACHE MISS] Calling the model...")
    started = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        input=prompt,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )

    elapsed = time.perf_counter() - started
    result = response.output_text
    CACHE[key] = result

    print(f"[MODEL CALL] Completed in {elapsed:.2f}s")
    if response.usage:
        print(f"[TOKENS] input={response.usage.input_tokens}, output={response.usage.output_tokens}")
        details = getattr(response.usage, "input_tokens_details", None)
        if details:
            print(f"[PROVIDER CACHED TOKENS] {getattr(details, 'cached_tokens', 0)}")
            print("This field is provider-side prompt caching, which is different")
            print("from our Python dictionary response cache.")

    return result

if __name__ == "__main__":
    prompt = "Explain in 3 bullets why an enterprise might use RAG instead of fine-tuning for changing policies."

    print("=" * 78)
    print("FIRST REQUEST")
    print("=" * 78)
    print(ask(prompt))

    print("\n" + "=" * 78)
    print("SECOND IDENTICAL REQUEST")
    print("=" * 78)
    print(ask(prompt))

    print("\n" + "=" * 78)
    print("THIRD REQUEST — CHANGE A PARAMETER")
    print("=" * 78)
    print("Changing temperature changes the cache key, so this is a cache MISS.")
    print(ask(prompt, temperature=0.8))

    print("\n[FDE TAKEAWAY]")
    print("""
Application response caching can eliminate repeated calls, but only when
reusing the previous answer is semantically safe.

Do NOT blindly cache:
- live account balances,
- changing order status,
- per-user sensitive responses,
- outputs whose freshness matters.

Provider prompt/KV caching is different: repeated prompt prefixes may reuse
provider computation while still generating a fresh response.
""")
