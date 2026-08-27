from sentence_transformers import SentenceTransformer
from typing import List

# Lightweight and ultra-fast model for text embeddings (384 dimensions)
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def generate_embedding(text: str) -> List[float]:
    """
    Converts any text string into a mathematical 384-dimensional vector embedding.
    """
    if not text or not text.strip():
        return []
    embedding = model.encode(text)
    return embedding.tolist()