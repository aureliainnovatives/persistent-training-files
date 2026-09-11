""""
pip install transformers
"""

from transformers import AutoTokenizer

#MODEL_NAME = "distilbert-base-uncased" # "gpt2"
MODEL_NAME =   "gpt2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

text = "Hello, I am Mayur Patil and I am happy to be here in AI Education Program"

encoded = tokenizer(
    text,
    add_special_tokens=True,
    return_attention_mask=True,
    return_tensors=None,
)

token_ids = encoded["input_ids"]
tokens = tokenizer.convert_ids_to_tokens(token_ids)
decoded_text = tokenizer.decode(token_ids, skip_special_tokens=False)

print(f"\nOriginal text: {text}")
print(f"\nToken IDs: {token_ids}")
print(f"\nTokens: {tokens}")
print(f"\nReconstructed text: {decoded_text}")