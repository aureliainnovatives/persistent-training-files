# FDE-MM — Model Mechanics Hands-On Pack

This pack is designed for instructor-led experimentation. Every Python file is standalone, heavily commented, and prints **what is changing, what to observe, and why it matters to an FDE**.



## Setup

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

For Hugging Face GPT-2, the first run downloads the model from Hugging Face.

| Parameter              | Say this in class                                                         |
| ---------------------- | ------------------------------------------------------------------------- |
| **Temperature**        | "How sharply should we favor the model's preferred tokens?"               |
| **Top-K**              | "How many top candidates are allowed into the sampling pool?"             |
| **Top-P**              | "How much cumulative probability mass is allowed into the sampling pool?" |
| **Seed**               | "Can I reproduce the pseudo-random sampling experiment?"                  |
| **Repetition penalty** | "How much should previously used tokens be discouraged?"                  |
| **Max new tokens**     | "How much output am I allowing the model to generate?"                    |
## Files

| File | Demonstrates |
|---|---|
| `01_openai_inference_mechanics.py` | OpenAI-compatible inference, temperature, top-p, output budget, repeated runs, token usage |
| `02_hf_gpt2_generation_mechanics.py` | Greedy decoding, sampling, temperature, top-k, top-p, repetition penalty |
| `03_token_and_context_budget.py` | Token calculation, context growth, context budget, output reservation |
| `04_application_response_cache.py` | Simple in-memory response cache and token/call savings |
| `05_context_competition.py` | Clean context vs noisy/conflicting context |
| `06_failure_mechanics.py` | Knowledge, context, instruction and validation failures |
| `07_structured_output_reliability.py` | Free text vs JSON/structured output + application validation |
| `08_model_mechanics_challenge.py` | Small participant challenge combining model-mechanics decisions |

## Recommended Delivery Sequence

```text
Inference
   ↓
Decoding / Sampling
   ↓
Tokens & Context Budget
   ↓
Caching
   ↓
Context Competition
   ↓
Failure Mechanics
   ↓
Structured Output
   ↓
Decision Challenge
```

## Important: OpenAI Credentials

As requested for this training pack, `01`, `04`, `05`, `06`, `07`, and `08` keep `BASE_URL`, `API_KEY`, and `MODEL` directly in code.

Replace:

```python
BASE_URL = "https://api.openai.com/v1"
API_KEY = "PASTE_YOUR_KEY_HERE"
MODEL = "gpt-4.1-mini"
```

before running.

**Do not commit a real API key to Git or share the edited files.** Hard-coding is used here only to make the classroom mechanics obvious.

## OpenAI Parameter Note

The examples use the Responses API and demonstrate `temperature`, `top_p`, and `max_output_tokens`. Parameter support can vary by model or OpenAI-compatible provider. The scripts catch unsupported-parameter errors and explain what to change.

For the cleanest classroom demonstration of sampling controls, use a model/endpoint that supports temperature and top-p. The GPT-2 file exposes these generation controls locally and very visibly.

## Caching: Two Different Concepts

`04_application_response_cache.py` implements **application-level response caching**:

```text
same request → dictionary lookup → reuse previous answer → no model call
```

This is intentionally simple and easy to inspect.

Provider-side **prompt/KV caching** is different: the provider may reuse computation for repeated prompt prefixes while still generating a new response. When the API reports it, OpenAI usage metadata can include `cached_tokens`. The OpenAI demos print this field when available.

## FDE Questions to Ask Throughout

1. What behaviour changed?
2. Which model mechanic caused or influenced it?
3. Is the behaviour acceptable for this workload?
4. Should we change the model, context, decoding, validation, or application architecture?
5. How would we measure whether the intervention actually improved the business task?
