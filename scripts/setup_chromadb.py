import chromadb

# Initialize ChromaDB with persistent storage
client = chromadb.PersistentClient(path="./chroma_storage")

# Create a sample collection (optional)
collection = client.get_or_create_collection(name="syllabus_questions")

print("✅ ChromaDB initialized successfully and collection created!")
