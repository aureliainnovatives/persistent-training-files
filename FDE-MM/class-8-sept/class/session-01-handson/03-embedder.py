""""
pip install sentence-transformers
"""

from sentence_transformers import SentenceTransformer

model_name = "sentence-transformers/all-MiniLM-L6-v2"

sentences = [
    "The customer wants to reduce support ticket resolution time.",
    "The organisation wants faster incident resolution.",
    "The weather in Pune is pleasant today.",
]

model = SentenceTransformer(model_name)

embeddings = model.encode(sentences, normalize_embeddings=True)

similarity_scores = model.similarity(embeddings, embeddings)

print(f"Model: {model}")
print(f"Embeddings Shape: {embeddings.shape}")

print(embeddings[0][:10])

print(similarity_scores)



