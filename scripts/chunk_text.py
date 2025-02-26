import os

def chunk_text(text, chunk_size=500):
    sentences = text.split('. ')
    chunks, current_chunk = [], ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def chunk_text_files():
    # Paths for input and output
    input_folder = "data/extracted_texts/"
    output_folder = "data/chunks/"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    chunk_count = 0

    # Process each extracted text file
    for txt_file in os.listdir(input_folder):
        if txt_file.endswith(".txt"):
            input_path = os.path.join(input_folder, txt_file)
            with open(input_path, "r", encoding="utf-8") as f:
                syllabus_text = f.read()


            # Chunk the text
            text_chunks = chunk_text(syllabus_text)

            # Save each chunk as a separate file
            base_name = txt_file.replace(".txt", "")
            for i, chunk in enumerate(text_chunks):
                chunk_filename = f"{output_folder}/{base_name}_chunk_{i+1}.txt"
                with open(chunk_filename, "w", encoding="utf-8") as f:
                    f.write(chunk)
                chunk_count += 1

    print(f"✅ Generated {chunk_count} chunks and saved in '{output_folder}'!")

