import chromadb
from typing import List, Dict, Any
from backend.embeddings import generate_embedding

# Local persistent ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db_data")

# Collection create ya load karein
memory_collection = client.get_or_create_collection(
    name="user_spotify_memory",
    metadata={"description": "Stores user vibe embeddings"}
)

def add_memory_to_vector_db(user_id: str, memory_text: str, metadata: Dict[str, Any]):
    """
    Text ka embedding banata hai aur ChromaDB mein store karta hai.
    """
    embedding = generate_embedding(memory_text)
    doc_id = f"{user_id}_{len(memory_collection.get()['ids']) + 1}"
    
    memory_collection.add(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[memory_text],
        metadatas=[{"user_id": user_id, **metadata}]
    )
    return doc_id

def query_similar_memory(query_text: str, n_results: int = 2):
    """
    User ke text ke sabse similar stored vector memory search karta hai.
    """
    query_vec = generate_embedding(query_text)
    results = memory_collection.query(
        query_embeddings=[query_vec],
        n_results=n_results
    )
    return results