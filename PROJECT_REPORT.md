# GovGuide AI — Project Report

## 1. Title
**GovGuide AI: A Retrieval-Augmented Generative AI Assistant for Government Documents**

## 2. Abstract
GovGuide AI is a Generative AI application designed to make government scheme documents easier to understand. The system allows a user to upload official documents, retrieves relevant passages for a question, and produces a grounded natural-language response. The project combines document processing, information retrieval, prompt engineering, and an LLM layer. A rule-based PM-KISAN eligibility demonstrator is included to show how deterministic rules can complement generative AI.

## 3. Problem
Government documents contain useful information about scheme benefits, eligibility, exclusions, application processes and conditions, but the information may be lengthy and difficult to search. A conversational interface can reduce the effort required to locate and understand relevant clauses.

## 4. Objectives
- Build a practical GenAI application rather than a simple chatbot.
- Implement a basic RAG pipeline.
- Keep factual answers grounded in document evidence.
- Make source evidence visible to the user.
- Demonstrate structured eligibility checking.
- Provide an extensible architecture for other schemes and policy documents.

## 5. Methodology
1. Upload a PDF.
2. Extract page text with PyPDF.
3. Normalize and split text into chunks.
4. Build a TF-IDF vector index.
5. Convert the user's question into the same vector space.
6. Retrieve the Top-K most similar chunks.
7. Supply retrieved evidence plus a grounding instruction to an LLM.
8. Display the generated answer and evidence.

## 6. Technologies
Python, Streamlit, PyPDF, scikit-learn, NumPy, requests, dotenv, and an optional OpenAI-compatible/Ollama LLM endpoint.

## 7. Key Design Decision
The project separates retrieval from generation. This makes the retrieval layer testable independently and allows the LLM provider to be changed without rewriting the document pipeline.

## 8. Expected Outcome
The user can ask natural-language questions about indexed documents and receive answers tied to retrieved evidence. The system can be extended from a single scheme demo into a multi-document government information assistant.

## 9. Future Scope
Transformer embeddings, reranking, OCR, multilingual interfaces, live official-source retrieval, automated citation validation, evaluation metrics, user accounts, and cloud deployment.
