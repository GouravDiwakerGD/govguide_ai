from __future__ import annotations
import requests
from typing import Iterable

from .config import settings
from .retriever import RetrievedChunk

SYSTEM_PROMPT = """You are GovGuide AI, a careful assistant for explaining government schemes and official documents.
Rules:
1. Answer only from the supplied context when factual details are requested.
2. Never invent eligibility criteria, amounts, dates, documents, deadlines, or procedures.
3. If the context does not support the answer, say that the available document does not establish it.
4. Cite the source as [Source: filename, page X] when a page is available.
5. Use simple language unless the user asks for technical language.
6. You are an informational assistant, not a government authority or legal advisor.
"""

def make_context(results: Iterable[RetrievedChunk]) -> str:
    blocks = []
    for r in results:
        page = f", page {r.chunk.page}" if r.chunk.page else ""
        blocks.append(f"[Source: {r.chunk.source}{page}]\n{r.chunk.text}")
    return "\n\n".join(blocks)


def demo_answer(question: str, results: list[RetrievedChunk]) -> str:
    if not results:
        return "I could not find supporting information in the indexed documents. Please upload the relevant official document."
    evidence = []
    for r in results[:3]:
        snippet = r.chunk.text.strip()
        if len(snippet) > 420:
            snippet = snippet[:420].rsplit(" ", 1)[0] + "..."
        page = f", page {r.chunk.page}" if r.chunk.page else ""
        evidence.append(f"• {snippet} [Source: {r.chunk.source}{page}]")
    return "Demo mode (no LLM API configured). Here are the most relevant grounded excerpts:\n\n" + "\n\n".join(evidence)


def generate_answer(question: str, results: list[RetrievedChunk], style: str = "Simple English") -> str:
    context = make_context(results)
    if settings.provider == "demo":
        return demo_answer(question, results)

    base_url = settings.base_url
    model = settings.model
    api_key = settings.api_key
    if settings.provider == "ollama":
        base_url = settings.ollama_url
        model = settings.ollama_model
        api_key = api_key or "ollama"

    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Answer style: {style}\n\nContext:\n{context}\n\nQuestion: {question}"},
        ],
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    resp = requests.post(url, json=payload, headers=headers, timeout=90)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()
