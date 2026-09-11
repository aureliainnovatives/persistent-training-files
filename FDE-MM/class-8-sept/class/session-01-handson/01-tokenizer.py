""""
pip install tiktoken
"""

import tiktoken

def demo_tokenizer(text: str, encoding_name: str = "gpt2") -> None:

    encoding = tiktoken.get_encoding(encoding_name)

    token_ids = encoding.encode(text)
    reconstruct_text = encoding.decode(token_ids)

    print(f"=" * 70)
    print(f"Original text: {text}")
    print(f"Token IDs: {token_ids}")
    print(f"Reconstructed text: {reconstruct_text}")
    print(f"=" * 70)


if __name__ == "__main__":
    demo_tokenizer("Hello, I am Mayur Patil and I am happy to be here in AI Education Program")