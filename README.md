# GovGuide AI — Government/Document AI Assistant

A full-fledged academic Generative AI project that uses Retrieval-Augmented Generation (RAG) to help users understand government scheme documents. The demo is grounded on PM-KISAN material from the Government of India and is designed so new PDFs/schemes can be added through the UI.

## Problem statement
Government schemes and public-service documents are often lengthy, formal, and difficult for citizens and students to navigate. Users need a conversational way to ask questions, find relevant clauses, understand eligibility, and identify required information without reading an entire document.

## What the project demonstrates
- Generative AI / LLM integration
- RAG pipeline
- PDF text extraction
- Document chunking
- Retrieval with TF-IDF + cosine similarity
- Grounded prompting
- Source/evidence display
- Rule-based eligibility assistant
- Simple-language answer modes
- Upload-and-index workflow
- LLM-provider abstraction: demo mode, Ollama, or OpenAI-compatible endpoint

## Architecture
```text
                   +-----------------------+
                   |   Government PDF      |
                   +-----------+-----------+
                               |
                         Text extraction
                               |
                           Chunking
                               |
                       +-------v-------+
                       | TF-IDF Index  |
                       +-------+-------+
                               |
User question ---> Retriever --+--> Top-K evidence
                               |
                       +-------v-------+
                       | Grounded LLM  |
                       +-------+-------+
                               |
                         Final answer
                               |
                    +----------+----------+
                    | Source references  |
                    +---------------------+
```

## Features
### 1. Chat with documents
Upload a government PDF and ask questions about it. The application retrieves the most relevant chunks before generating a response.

### 2. Grounded answers
The system instructs the LLM to answer from retrieved context and avoid inventing facts.

### 3. Evidence panel
The UI shows the exact chunks retrieved for the last question so a teacher can inspect the RAG step.

### 4. Eligibility checker
A PM-KISAN-focused educational rules module demonstrates how structured eligibility questions can be combined with document-grounded reasoning.

### 5. Beginner-friendly explanations
The same retrieved evidence can be requested in simple English, Hindi-friendly English, formal language, or beginner mode.

## Run locally
1. Install Python 3.10+.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Copy `.env.example` to `.env`.
5. Start Streamlit.

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## LLM modes
### Demo mode
Default. No API key is required. The system returns the strongest grounded excerpts instead of making an external LLM call. This is useful for testing the RAG pipeline and teacher demonstrations.

### Ollama
Set in `.env`:
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2
```
Run an Ollama model locally, then start the app.

### OpenAI-compatible endpoint
Set:
```env
LLM_PROVIDER=openai_compatible
LLM_API_KEY=your-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your-model
```
The code uses the common `/chat/completions` interface, so it can also be adapted to another compatible provider.

## Demo document
`data/documents/PM-KISAN_Demo_Source_Summary.txt` is a concise project-created summary of the official PM-KISAN operational guidelines. It includes the official source URL and clearly says it is a demo summary. For a stronger live demo, upload the current official PDF from the PM-KISAN portal through the app.

Official PM-KISAN source:
https://pmkisan.gov.in/Documents/RevisedPM-KISANOperationalGuidelines%28English%29.pdf

## Example demo questions
- What is PM-KISAN?
- What benefit is described in the guidelines?
- Who is considered a farmer family?
- What are the major exclusions?
- Are certain government employees excluded?
- Explain the exclusions in simple English.
- Where should I verify the current rules?

## How to explain the project to a teacher
**Problem:** Long government documents are difficult to search and understand.

**Solution:** I built a RAG-based Generative AI assistant. Documents are extracted and chunked, the chunks are indexed, and a user question retrieves the most relevant evidence. The retrieved evidence is then supplied to an LLM with a grounding prompt so the response is based on the document rather than only the model's memory.

**Why RAG:** It makes domain-specific answers easier to update and inspect, and it lets the system show supporting evidence.

**Extra module:** I added a structured eligibility checker for PM-KISAN to demonstrate how deterministic business rules can work alongside an LLM. The checker is explicitly educational and does not replace an official government eligibility determination.

## Limitations and future work
- Replace TF-IDF with a transformer embedding model for stronger semantic retrieval.
- Add reranking for better Top-K evidence.
- Add OCR for scanned PDFs.
- Add multilingual Hindi translation using an LLM or translation model.
- Add live official-source search with citation validation.
- Add evaluation datasets and retrieval/answer faithfulness metrics.
- Add authentication and per-user document collections.

## Academic integrity / safety note
This is an academic prototype. Government rules, benefits, deadlines, and eligibility can change. The app should never be presented as an official government decision-maker. Users must verify current information on the relevant government portal.
