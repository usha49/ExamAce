import sys
import os
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

# Adding the project root folder to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.config import genai  # Import API setup from config.py

# Define Embedding Function
class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True  # Specify document embedding mode

    def __call__(self, input: Documents) -> Embeddings:
        response = genai.embed_content(
            model="models/text-embedding-004",
            content=input,
            task_type="retrieval_document" if self.document_mode else "retrieval_query",
        )
        return response["embedding"]

def store_embeddings():
    # Initialize ChromaDB
    embed_fn = GeminiEmbeddingFunction()
    chroma_client = chromadb.PersistentClient(path="./chroma_storage")
    db = chroma_client.get_or_create_collection(name="nepal_eng_exam_db", embedding_function=embed_fn)

    # Read chunked text from multiple files
    chunks_folder = "data/chunks/"
    chunk_files = [f for f in os.listdir(chunks_folder) if f.endswith(".txt")]

    chunk_count = 0

    for i, chunk_file in enumerate(chunk_files):
        chunk_path = os.path.join(chunks_folder, chunk_file)

        with open(chunk_path, "r", encoding="utf-8") as f:
            chunk_content = f.read().strip()

        if chunk_content:  # Only store non-empty chunks
            db.add(
                documents=[chunk_content],
                ids=[f"{chunk_file.replace('.txt', '')}"]
            )
            chunk_count += 1

    print(f"✅ Stored {chunk_count} chunks in ChromaDB!")