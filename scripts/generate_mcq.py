# import sys
# import os
# import chromadb
# import pandas as pd
# import re
# from google.generativeai import GenerativeModel
# from google.api_core import retry
# import time
# from google.api_core.exceptions import DeadlineExceeded

# # Adding the project root folder to Python's search path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from scripts.config import genai  # Import API setup from config.py
# from topics import chapters_and_topics  # Import the dictionary from topics.py

# def generate_mcqs():
#     """Main function to generate MCQs for all chapters and topics."""
#     # Load ChromaDB
#     chroma_client = chromadb.PersistentClient(path="./chroma_storage")
#     db = chroma_client.get_collection(name="nepal_eng_exam_db")

#     # Convert the dictionary into a list of (topic, chapter) pairs
#     queries_with_chapters = []
#     for chapter, topics in chapters_and_topics.items():
#         queries_with_chapters.extend([(topic, chapter) for topic in topics])

#     # Function to generate a query embedding using Google Gemini
#     def get_query_embedding(query_text):
#         retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}
#         try:
#             response = genai.embed_content(
#             model="models/text-embedding-004",
#             content=query_text,
#             task_type="retrieval_query",
#             request_options=retry_policy,
#             )
#             return response["embedding"]
#         except Exception as e:
#             print(f"Embedding failed for query '{query_text}':{e}")
#             return None

#     # Retrieve relevant passage
#     def retrieve_passage(query):
#         query_embedding = get_query_embedding(query)  # Using Gemini embeddings (768D)
#         results = db.query(query_embeddings=[query_embedding], n_results=1)
#         if results["documents"]:
#             return results["documents"][0][0]  # Extract the string from the list
#         return None

#     # Function to extract specific fields using regex
#     def extract_field(text, keyword):
#         """Extracts a field from the text using regex, returns an empty string if not found."""
#         match = re.search(rf"{keyword}[:\s]*([\s\S]*?)(?=\n[A-Z][a-z]*:|\Z)", text)
#         return match.group(1).strip() if match else ""

#     # MCQ generation
#     def generate_mcq(query):
#         passage = retrieve_passage(query)
#         if not passage:
#             return "No relevant content found."
        
#         passage_oneline = passage.replace("\n", " ")
#         query_oneline = query.replace("\n", " ")

#         mcq_prompt = f"""
#         #You are a subject matter expert creating factual, theory-based multiple-choice questions for the Nepal Engineering License Exam.
#         # Use the given passage to generate 5 questions along with four options and indicate the correct answer with the query entered also the difficulty which can be easy and medium only.
#         You are NOT creating reading comprehension questions. Do NOT mention 'passage', 'according to the passage', or 'based on the passage' in any part of the question.
#         The passage below is only for your knowledge to understand the topic. Use it as background information to create independent questions.
#         Ensure the questions:
#         - Are purely text-based (Do not refer to any diagrams, figures, tables, images, or visual content).
#         - Are fact-based, conceptual, or definition-based.
#         - Are framed in a way that does not assume the passage is seen by the person answering.
#         - Do not mention 'passage', 'according to the passage', or similar phrases.
#         - Cover important points from the passage, but avoid asking questions that require visual inspection.
#         - Have short, concise distractors (wrong options) that are realistic.
#         - Avoid introductory or conclusion statements; only provide the questions and answers.

#         Follow this format exactly:
#          Question: <question_text>
#         Options:
#         A) <option_1>
#         B) <option_2>
#         C) <option_3>
#         D) <option_4>
#         Answer: <correct_option name>
#         Explanation: <explanation>
#         Topic: <same as query>
#         Difficulty: <difficulty>
#         ---


#         # QUESTION: {query_oneline}
#         # PASSAGE: {passage_oneline}
#         Ensure each question follows this structure and is separated by "---".
        
#         """

#         model = GenerativeModel("gemini-1.5-flash-latest")

#         #Incresing the timeout to 300 seconds (5 minutes)
#         retry_policy = retry.Retry(
#             predicate = retry.if_exception_type(DeadlineExceeded),
#             deadline=300
#             )
#         try:
#             response = model.generate_content(mcq_prompt,retry=retry_policy)
#             return response.text
#         except DeadlineExceeded as e:
#             print(f" Deadline exceeded for query '{query}' :{e}")
#             return None
#         except Exception as e:
#             print(f"Error generating MCQ for query '{query}':{e}")
#             return None
        
#         response = model.generate_content(mcq_prompt)
#         return response.text

#     # Dictionary to store generated MCQs
#     mcq_dict = {}

#     # Loop through all queries and generate MCQs
#     for query, chapter in queries_with_chapters:
#         mcq_text = generate_mcq(query)
#         time.sleep(1)  # Sleep for 1 second between each query
#         if not mcq_text:
#             continue  # Skip if no MCQs generated

#         questions = mcq_text.strip().split("---")  # Split multiple MCQs
#         for q in questions:
#             q = q.strip()
#             if not q:
#                 continue  # Skip empty sections

#             # Extract fields
#             question = extract_field(q, "Question")
#             answer = extract_field(q, "Answer")
#             explanation = extract_field(q, "Explanation")
#             topic = extract_field(q, "Topic")
#             difficulty = extract_field(q, "Difficulty")

#             # Extract options manually
#             options_text = re.search(r"Options:\n(.+?)\nAnswer:", q, re.DOTALL)
#             if options_text:
#                 options = [opt.strip()[3:] for opt in options_text.group(1).split("\n") if opt.strip()]
#             else:
#                 options = []

#             if question and options:  # Only add non-empty questions with options
#                 mcq_entry = {
#                     "question": question,
#                     "options": options,
#                     "answer": answer,
#                     "explanation": explanation,
#                     "topic": topic,
#                     "difficulty": difficulty,
#                     "chapter": chapter
#                 }

#                 # Group MCQs by chapter
#                 if chapter not in mcq_dict:
#                     mcq_dict[chapter] = []
#                 mcq_dict[chapter].append(mcq_entry)
#             else:
#                 print(f"⚠️ Skipped incomplete question for topic '{topic}' in chapter {chapter}")

#     # Save MCQs to separate CSV files for each chapter
#     for chapter, mcqs in mcq_dict.items():
#         df = pd.DataFrame(mcqs)
#         csv_file = f"results/mcq_data_{chapter}.csv"
#         df.to_csv(csv_file, index=False)
#         print(f"✅ Generated {len(mcqs)} MCQs for chapter {chapter} and saved to '{csv_file}'!")

# # Entry point for standalone execution
# if __name__ == "__main__":
#     generate_mcqs()

import sys
import os
import chromadb
import pandas as pd
import re
from google.generativeai import GenerativeModel
from google.api_core import retry
from google.api_core.exceptions import DeadlineExceeded
import time
import logging

# Adding the project root folder to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.config import genai  # Import API setup from config.py
from topics import chapters_and_topics  # Import the dictionary from topics.py

# Configure logging
logging.basicConfig(level=logging.INFO)

def generate_mcqs():
    """Main function to generate MCQs for all chapters and topics."""
    # Load ChromaDB
    chroma_client = chromadb.PersistentClient(path="./chroma_storage")
    db = chroma_client.get_collection(name="nepal_eng_exam_db")

    # Convert the dictionary into a list of (topic, chapter) pairs
    queries_with_chapters = []
    for chapter, topics in chapters_and_topics.items():
        queries_with_chapters.extend([(topic, chapter) for topic in topics])

    # Function to generate a query embedding using Google Gemini
    def get_query_embedding(query_text):
        retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}
        try:
            response = genai.embed_content(
            model="models/text-embedding-004",
            content=query_text,
            task_type="retrieval_query",
            request_options=retry_policy,
            )
            return response["embedding"]
        except Exception as e:
            logging.error(f"Embedding failed for query '{query_text}': {e}")
            return None

    # Retrieve relevant passage
    def retrieve_passage(query):
        query_embedding = get_query_embedding(query)  # Using Gemini embeddings (768D)
        results = db.query(query_embeddings=[query_embedding], n_results=1)
        if results["documents"]:
            return results["documents"][0][0]  # Extract the string from the list
        return None

    # Function to extract specific fields using regex
    def extract_field(text, keyword):
        """Extracts a field from the text using regex, returns an empty string if not found."""
        match = re.search(rf"{keyword}[:\s]*([\s\S]*?)(?=\n[A-Z][a-z]*:|\Z)", text)
        return match.group(1).strip() if match else ""

    # Retry decorator for generate_content
    @retry.Retry(
        predicate=retry.if_exception_type(DeadlineExceeded),
        deadline=300  # 5 minutes
    )
    def generate_content_with_retry(model, prompt):
        return model.generate_content(prompt)

    # MCQ generation with error handling
    def generate_mcq(query):
        passage = retrieve_passage(query)
        if not passage:
            return "No relevant content found."
        
        passage_oneline = passage.replace("\n", " ")
        query_oneline = query.replace("\n", " ")

        mcq_prompt = f"""
        #You are a subject matter expert creating factual, theory-based multiple-choice questions for the Nepal Engineering License Exam.
        # Use the given passage to generate 5 questions along with four options and indicate the correct answer with the query entered also the difficulty which can be easy and medium only.
        You are NOT creating reading comprehension questions. Do NOT mention 'passage', 'according to the passage', or 'based on the passage' in any part of the question.
        The passage below is only for your knowledge to understand the topic. Use it as background information to create independent questions.
        Ensure the questions:
        - Are purely text-based (Do not refer to any diagrams, figures, tables, images, or visual content).
        - Are fact-based, conceptual, or definition-based.
        - Are framed in a way that does not assume the passage is seen by the person answering.
        - Do not mention 'passage', 'according to the passage', or similar phrases.
        - Cover important points from the passage, but avoid asking questions that require visual inspection.
        - Have short, concise distractors (wrong options) that are realistic.
        - Avoid introductory or conclusion statements; only provide the questions and answers.

        Follow this format exactly:
         Question: <question_text>
        Options:
        A) <option_1>
        B) <option_2>
        C) <option_3>
        D) <option_4>
        Answer: <correct_option name>
        Explanation: <explanation>
        Topic: <same as query>
        Difficulty: <difficulty>
        ---


        # QUESTION: {query_oneline}
        # PASSAGE: {passage_oneline}
        Ensure each question follows this structure and is separated by "---".
        """

        model = GenerativeModel("gemini-1.5-flash-latest")
        
        try:
            response = generate_content_with_retry(model, mcq_prompt)
            return response.text
        except DeadlineExceeded as e:
            logging.error(f"Deadline exceeded for query '{query}': {e}")
            return None
        except Exception as e:
            logging.error(f"Error generating MCQ for query '{query}': {e}")
            return None

    # Dictionary to store generated MCQs
    mcq_dict = {}

    # Loop through all queries and generate MCQs
    for query, chapter in queries_with_chapters:
        logging.info(f"Processing query: {query} (Chapter: {chapter})")
        mcq_text = generate_mcq(query)
        time.sleep(1)  # Sleep for 1 second between each query
        if not mcq_text:
            logging.warning(f"No MCQs generated for query: {query}")
            continue

        questions = mcq_text.strip().split("---")  # Split multiple MCQs
        for q in questions:
            q = q.strip()
            if not q:
                continue  # Skip empty sections

            # Extract fields
            question = extract_field(q, "Question")
            answer = extract_field(q, "Answer")
            explanation = extract_field(q, "Explanation")
            topic = extract_field(q, "Topic")
            difficulty = extract_field(q, "Difficulty")

            # Extract options manually
            options_text = re.search(r"Options:\n(.+?)\nAnswer:", q, re.DOTALL)
            if options_text:
                options = [opt.strip()[3:] for opt in options_text.group(1).split("\n") if opt.strip()]
            else:
                options = []

            if question and options:  # Only add non-empty questions with options
                mcq_entry = {
                    "question": question,
                    "options": options,
                    "answer": answer,
                    "explanation": explanation,
                    "topic": topic,
                    "difficulty": difficulty,
                    "chapter": chapter
                }

                # Group MCQs by chapter
                if chapter not in mcq_dict:
                    mcq_dict[chapter] = []
                mcq_dict[chapter].append(mcq_entry)
            else:
                logging.warning(f"Skipped incomplete question for topic '{topic}' in chapter {chapter}")

    # Save MCQs to separate CSV files for each chapter
    for chapter, mcqs in mcq_dict.items():
        df = pd.DataFrame(mcqs)
        csv_file = f"results/mcq_data_{chapter}.csv"
        df.to_csv(csv_file, index=False)
        logging.info(f"✅ Generated {len(mcqs)} MCQs for chapter {chapter} and saved to '{csv_file}'!")

# Entry point for standalone execution
if __name__ == "__main__":
    generate_mcqs()