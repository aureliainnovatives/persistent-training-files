"""
FDE-MM Lab 02 — GPT-2 Generation Mechanics with Hugging Face

PURPOSE
-------
Use GPT-2 to make decoding/generation mechanics visible.

GPT-2 is useful pedagogically because Hugging Face exposes generation
parameters directly.

This is NOT a recommendation to use GPT-2 for modern enterprise workloads.
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed


# ============================================================================
# MODEL AND PROMPT
# ============================================================================

# Hugging Face model identifier.
# "gpt2" downloads the original GPT-2 model and tokenizer from Hugging Face.
MODEL_NAME = "gpt2"

# Keep the SAME prompt across experiments.
# This allows us to observe how generation settings alone change the output.
PROMPT = "The most important risk when deploying AI in a bank is"


print("=" * 78)
print("LOADING GPT-2")
print("=" * 78)
print("First run may download model files from Hugging Face.")


# Tokenizer converts text into token IDs understood by GPT-2.
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load the pretrained GPT-2 causal language model.
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Put the model into inference/evaluation mode.
# This disables training-specific behaviour such as dropout.
model.eval()

# Convert our text prompt into tensors that can be passed to the model.
inputs = tokenizer(PROMPT, return_tensors="pt")


# ============================================================================
# COMMON GENERATION FUNCTION
# ============================================================================

def generate(title, **generation_args):
    """
    Run one generation experiment.

    generation_args allows each experiment to supply different parameters
    such as temperature, top_k, top_p and repetition_penalty.
    """

    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)

    print("[PROMPT]", PROMPT)

    # Print every parameter so participants can see exactly what changed
    # between one experiment and another.
    print("[PARAMETERS]")
    for k, v in generation_args.items():
        print(f"  {k} = {v}")

    # torch.no_grad() tells PyTorch we are only performing inference.
    # No gradients are required, reducing memory/computation overhead.
    with torch.no_grad():

        output = model.generate(

            # Tokenized prompt supplied to the model.
            **inputs,

            # GPT-2 has no dedicated padding token by default.
            # We reuse EOS (end-of-sequence) as the padding token.
            pad_token_id=tokenizer.eos_token_id,

            # Insert experiment-specific generation parameters.
            **generation_args,
        )

    print("\n[OUTPUT]")

    # Convert generated token IDs back into human-readable text.
    print(
        tokenizer.decode(
            output[0],
            skip_special_tokens=True
        )
    )


# ============================================================================
# EXPERIMENTS
# ============================================================================

if __name__ == "__main__":

    # ========================================================================
    # EXPERIMENT 1 — GREEDY DECODING
    # ========================================================================

    generate(
        "EXPERIMENT 1 — GREEDY DECODING",

        # do_sample=False disables random sampling.
        # At each step, the model chooses its highest-scoring next token.
        do_sample=False,

        # Generate at most 50 NEW tokens after the original prompt.
        # This controls response length, computation and inference cost.
        max_new_tokens=50,
    )

    print("\n[OBSERVE]")
    print("Greedy decoding removes sampling, but deterministic generation")
    print("does NOT mean the answer is factually correct.")


    # ========================================================================
    # EXPERIMENT 2 — SAMPLING
    # ========================================================================

    # Fix the pseudo-random generator so experiments are reproducible.
    # Using the same seed helps isolate the parameter we intentionally change.
    set_seed(42)

    generate(
        "EXPERIMENT 2 — SAMPLING",

        # do_sample=True enables probabilistic token sampling.
        # The model can choose among likely alternatives instead of argmax only.
        do_sample=True,

        # Temperature controls how sharp or flat the probability distribution is.
        # 1.0 leaves the distribution at its normal sampling scale.
        temperature=1.0,

        # Maximum number of NEW tokens generated after the prompt.
        # It is different from total sequence length because prompt tokens are excluded.
        max_new_tokens=50,
    )

    print("\n[OBSERVE]")
    print("Sampling allows alternatives instead of always choosing argmax.")


    # ========================================================================
    # EXPERIMENT 3A — LOW TEMPERATURE
    # ========================================================================

    set_seed(42)

    generate(
        "EXPERIMENT 3A — LOW TEMPERATURE",

        # Sampling must be enabled for temperature to influence token selection.
        do_sample=True,

        # Low temperature sharpens probability differences.
        # High-probability tokens become relatively more dominant.
        temperature=0.3,

        # top_k=0 disables Top-K filtering in Hugging Face generation.
        # This helps us isolate TEMPERATURE as the main changed variable.
        top_k=0,

        # Limit generation to 50 new tokens.
        max_new_tokens=50,
    )


    # ========================================================================
    # EXPERIMENT 3B — HIGH TEMPERATURE
    # ========================================================================

    # Reset to the SAME seed used in 3A.
    # Now temperature is the primary intentional difference.
    set_seed(42)

    generate(
        "EXPERIMENT 3B — HIGH TEMPERATURE",

        # Enable probabilistic sampling.
        do_sample=True,

        # Higher temperature flattens the probability distribution.
        # Lower-probability alternatives therefore receive relatively more chance.
        temperature=1.5,

        # Disable Top-K filtering so we can focus on temperature.
        top_k=0,

        # Generate at most 50 new tokens.
        max_new_tokens=50,
    )

    print("\n[OBSERVE]")
    print("Temperature reshapes the token probability distribution.")
    print("Low temperature -> distribution becomes sharper.")
    print("High temperature -> distribution becomes flatter.")


    # ========================================================================
    # EXPERIMENT 4A — TOP-K = 10
    # ========================================================================

    set_seed(42)

    generate(
        "EXPERIMENT 4A — TOP-K = 10",

        # Enable probabilistic sampling.
        do_sample=True,

        # Keep temperature constant across both Top-K experiments.
        # This makes Top-K the parameter we are primarily studying.
        temperature=0.8,

        # Only the 10 highest-probability candidate tokens remain eligible
        # for sampling at each generation step.
        top_k=10,

        # Generate at most 50 new tokens.
        max_new_tokens=50,
    )


    # ========================================================================
    # EXPERIMENT 4B — TOP-K = 100
    # ========================================================================

    set_seed(42)

    generate(
        "EXPERIMENT 4B — TOP-K = 100",

        # Sampling remains enabled.
        do_sample=True,

        # Same temperature as Experiment 4A.
        temperature=0.8,

        # Allow sampling from the top 100 candidates.
        # This creates a wider candidate pool than top_k=10.
        top_k=100,

        # Generate at most 50 new tokens.
        max_new_tokens=50,
    )

    print("\n[OBSERVE]")
    print("top_k limits HOW MANY candidate tokens can participate in sampling.")
    print("top_k=10  -> narrower candidate pool")
    print("top_k=100 -> wider candidate pool")


    # ========================================================================
    # EXPERIMENT 5A — TOP-P = 0.3
    # ========================================================================

    set_seed(42)

    generate(
        "EXPERIMENT 5A — TOP-P = 0.3",

        # Enable probabilistic sampling.
        do_sample=True,

        # Keep temperature constant while comparing Top-P.
        temperature=0.8,

        # Disable Top-K filtering.
        # We want Top-P to determine the candidate set in this experiment.
        top_k=0,

        # Top-P / nucleus sampling keeps the smallest set of likely tokens
        # whose cumulative probability reaches approximately 30%.
        top_p=0.3,

        # Generate at most 50 new tokens.
        max_new_tokens=50,
    )


    # ========================================================================
    # EXPERIMENT 5B — TOP-P = 0.95
    # ========================================================================

    set_seed(42)

    generate(
        "EXPERIMENT 5B — TOP-P = 0.95",

        # Enable sampling.
        do_sample=True,

        # Same temperature as 5A.
        temperature=0.8,

        # Again disable Top-K filtering.
        top_k=0,

        # Keep enough candidate tokens to cover approximately 95%
        # of the probability mass — normally a much wider candidate set.
        top_p=0.95,

        # Generate at most 50 new tokens.
        max_new_tokens=50,
    )

    print("\n[OBSERVE]")
    print("top_p controls candidate tokens by PROBABILITY MASS, not token count.")
    print("top_p=0.30 -> narrower nucleus")
    print("top_p=0.95 -> wider nucleus")


    # ========================================================================
    # EXPERIMENT 6A — NO EXTRA REPETITION PENALTY
    # ========================================================================

    set_seed(42)

    generate(
        "EXPERIMENT 6A — NO EXTRA REPETITION PENALTY",

        # Enable sampling.
        do_sample=True,

        # Moderate temperature.
        temperature=0.8,

        # Sample from a nucleus covering 90% of probability mass.
        top_p=0.9,

        # 1.0 means no additional repetition penalty.
        # Previously generated tokens are not penalized by this mechanism.
        repetition_penalty=1.0,

        # Slightly longer generation gives repetition more opportunity to appear.
        max_new_tokens=70,
    )


    # ========================================================================
    # EXPERIMENT 6B — REPETITION PENALTY = 1.3
    # ========================================================================

    set_seed(42)

    generate(
        "EXPERIMENT 6B — REPETITION PENALTY = 1.3",

        # Sampling remains enabled.
        do_sample=True,

        # Same temperature as 6A.
        temperature=0.8,

        # Same Top-P as 6A.
        top_p=0.9,

        # Values above 1.0 penalize tokens that have already appeared.
        # This can reduce repetitive generation, but excessive penalties can hurt quality.
        repetition_penalty=1.3,

        # Same output budget as 6A.
        max_new_tokens=70,
    )


    # ========================================================================
    # FINAL FDE TAKEAWAY
    # ========================================================================

    print("\n" + "=" * 78)
    print("FDE TAKEAWAY")
    print("=" * 78)

    print("""
do_sample
    Controls whether generation samples probabilistically or chooses
    the highest-scoring token.

temperature
    Changes the SHAPE of the probability distribution.

top_k
    Restricts sampling to a fixed NUMBER of top candidate tokens.

top_p
    Restricts sampling using cumulative PROBABILITY MASS.

repetition_penalty
    Discourages tokens that have already appeared.

max_new_tokens
    Controls the maximum generation/output budget.

set_seed
    Controls the pseudo-random sequence so experiments can be reproduced.

IMPORTANT:

These parameters influence HOW the model generates.

They do NOT provide:
    - factual correctness
    - grounding
    - business-rule enforcement
    - safety
    - validation
    - production reliability

FDE thinking:

    Model
      ↓
    Decoding configuration
      ↓
    Model output
      ↓
    Grounding / Validation / Business Controls
      ↓
    Production outcome
""")