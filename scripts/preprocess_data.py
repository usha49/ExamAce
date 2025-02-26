import os
import fitz  # PyMuPDF

def extract_text_from_pdfs(pdf_folder):
    texts = {} #using a dictionary to store filenames as keys
    for file_name in os.listdir(pdf_folder):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, file_name)
            doc = fitz.open(pdf_path)
            text = "\n".join([page.get_text() for page in doc])
            texts[file_name] = text  #Store text with PDF filename as key
    return texts


def preprocess_data():
    # Run the extraction
    pdf_folder = "./data/"  # /data ma bhako lai load garna ko lagi
    pdf_texts = extract_text_from_pdfs(pdf_folder)

    # Save extracted text from each PDF separately
    if not os.path.exists("data/extracted_texts"):
        os.makedirs("data/extracted_texts")  # Create folder to store individual text files

    for pdf_name, text in pdf_texts.items():
        text_filename = f"data/extracted_texts/{pdf_name.replace('.pdf', '.txt')}"
        with open(text_filename, "w", encoding="utf-8") as f:
            f.write(text)

    print(f"✅ Extracted text from {len(pdf_texts)} PDFs and saved in 'data/extracted_texts/'!")