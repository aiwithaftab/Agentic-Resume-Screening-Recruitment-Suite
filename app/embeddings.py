import chromadb
from sentence_transformers import SentenceTransformer

# Create / connect to ChromaDB
chroma_client = chromadb.PersistentClient(path="vector_db")

# Create collection
collection = chroma_client.get_or_create_collection(
    name="resume_embeddings",
    metadata={"hnsw:space": "cosine"}
)

# Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    """Return vector embedding from model"""
    return model.encode([text])[0].tolist()

def add_resume_embedding(resume_id: str, text: str):
    vector = embed_text(text)
    # explicitly include metadatas so the name is easily retrievable
    collection.add(
        documents=[text], 
        embeddings=[vector], 
        metadatas=[{"file_name": resume_id}], 
        ids=[resume_id]
    )
    return True

def semantic_search(query: str, top_k: int = 3):
    query_vector = embed_text(query)
    result = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )
    
    # Extract the IDs and Documents into a list of dictionaries
    formatted_results = []
    if result['ids']:
        for i in range(len(result['ids'][0])):
            formatted_results.append({
                "resume_id": result['ids'][0][i],
                "content_preview": result['documents'][0][i][:200] + "...",
                "distance": round(result['distances'][0][i], 4) if 'distances' in result else None
            })
    
    return formatted_results