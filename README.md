Exam Ace: MCQ generation and Exam taking system for the NEC License exam

This is our major project where we generate MCQ question for NEC license exam implementing RAG algorithm from our customised notes and develop exam taking webapp for practising.

## 🚀 Features

- ✨ Generates a good quality question usiing the model already validated by us
- ⚡ Simulates real exams setting
- 🔒 Personalized Progress Tracking

## 🛠️ Tech Stack

- Python
- Django
- SQLite
- Gemini-1.5-flash-latest
- etc.

🧠 How It Works 
This system is designed as a pipeline to generate multiple-choice questions (MCQs) 
from provided syllabus materials. The key functional components representing the flow of data and processes in the systems are: 
1. Input PDFs 
The system begins with the input of syllabus notes in the form of pdf. These documents serve as the primary source of technical 
content for generating MCQs. 
2. Text Extraction 
The text extraction module processes the input PDFs to extract raw text content. Tools 
such as PyMuPDF are used to remove non-text elements like headers, footers, images, 
and formatting. This step ensures that the extracted text is clean and ready for further 
processing. The output is unstructured text, which is then passed to the next stage. 
3. Chunking 
The extracted text is divided into smaller, manageable chunks of up to 500 words each. 
A sliding window approach is employed, with a 20% overlap between consecutive 
chunks (e.g., 100 words). This overlap ensures that semantic context is preserved across 
chunks, which is critical for maintaining coherence during retrieval and generation. The 
chunking process also adheres to the input size constraints of the generative model 
(Gemini-1.5-Flash). 
4. Google Gemini Embeddings 
Each text chunk is converted into a high-dimensional vector representation using the 
Google Gemini embedding function. These embeddings capture the semantic 
relationships between words and concepts within the text, enabling the system to 
understand and retrieve relevant content based on user queries. The embeddings are 
stored in a vector database for efficient retrieval. 
5. Vector Database (ChromaDB) 
The generated embeddings are indexed and stored in ChromaDB. It organizes the embeddings to facilitate fast similarity searches, ensuring that relevant chunks can be retrieved within milliseconds of a query. 
The database also stores metadata associated with each chunk, such as the source PDF 
and topic, to enable filtering and organization. 
6. Retrieval-Augmented Generation (RAG) 
The RAG pipeline is the core of the system, combining retrieval and generation to 
produce contextually accurate MCQs. When a user submits a query (in our case the specific topics assigned from NEC from which we have to generate the questions, the system performs the following steps:
a. Query Embedding: The query is embedded into a vector using the same 
Gemini embedding model.
b. Similarity Search: ChromaDB retrieves the most relevant chunks based 
on cosine similarity between the query vector and the stored embeddings.
c. MCQ Generation: The retrieved chunks are formatted into a structured prompt 
and fed into the Gemini-1.5-Flash model, which generates MCQs with a correct 
answer and three distractors.
 7. Answer & Distractor Generation 
The system ensures the quality of generated MCQs by validating the correctness of 
answers and the plausibility of distractors. Distractors are generated using semantic 
similarity metrics to ensure they are contextually relevant but distinct from the correct 
answer. The validation step filters out duplicates or ambiguous options, ensuring the 
final output is of high quality. 
8. Database 
The generated MCQs are stored in a structured question bank in a database. This repository allows users to access previously generated questions and 
supports features such as tagging by topic and difficulty level. The 
database ensures scalability and reusability of the generated content. 
9. User Interface 
The user interface (UI) is designed to provide a seamless and intuitive experience for 
users. Built using Django for the backend and HTML/CSS/JavaScript for the frontend, 
the UI allows users to practice generated MCQs independently as well as take timed practice 
tests. The interface also includes features such as progress tracking and performance 
analytics to enhance the learning experience.

End-to-End Workflow 
Input Processing: PDFs are extracted, cleaned, and chunked into manageable 
segments.
 Embedding & Storage: Text chunks are embedded and stored in ChromaDB 
for efficient retrieval.
 Query Handling: User queries are processed, and relevant chunks are retrieved 
using similarity search.
 MCQ Generation: The RAG pipeline generates MCQs using retrieved context 
and validates the output.
 Storage & Display: Generated MCQs are stored in the database and displayed 
to the user via the UI.
 This pipeline ensures that the system generates high-quality, syllabus-aligned MCQs 
while minimizing inaccuracies and hallucinations. The integration of advanced AI 
models and efficient retrieval mechanisms makes the system a powerful tool for NEC 
exam preparation. 
