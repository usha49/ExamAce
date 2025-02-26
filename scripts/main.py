import os
import time
from preprocess_data import preprocess_data
from chunk_text import chunk_text_files
from store_embeddings import store_embeddings
from generate_mcq import generate_mcqs

def main():
    print(" Starting the MCQ generation pipeline...")

    # Step 1: Preprocess data (extract text from PDFs)
    print("\n Step 1: Extracting text from PDFs...")
    preprocess_data()
    time.sleep(1)  # Optional: Add a small delay for better readability

    # Step 2: Chunk the extracted text
    print("\n Step 2: Chunking the extracted text...")
    chunk_text_files()
    time.sleep(1)

    # Step 3: Store embeddings in ChromaDB
    print("\n Step 3: Storing embeddings in ChromaDB...")
    store_embeddings()
    time.sleep(1)

    # Step 4: Generate MCQs
    print("\n Step 4: Generating MCQs...")
    generate_mcqs()

    print("\n Pipeline completed successfully!")

if __name__ == "__main__":
    main()