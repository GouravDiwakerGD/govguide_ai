from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .document_processor import Chunk

@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float

class TfidfRetriever:
    """Lightweight retrieval layer that works without downloading an embedding model.
    Replaceable with SentenceTransformers later without changing the app interface.
    """
    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=20000)
        self.matrix = None
        self.chunks: list[Chunk] = []

    def fit(self, chunks: Sequence[Chunk]) -> None:
        self.chunks = list(chunks)
        if self.chunks:
            self.matrix = self.vectorizer.fit_transform([c.text for c in self.chunks])
        else:
            self.matrix = None

    def search(self, query: str, k: int = 5) -> list[RetrievedChunk]:
        if not self.chunks or self.matrix is None:
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        indices = np.argsort(scores)[::-1][:k]
        return [RetrievedChunk(self.chunks[i], float(scores[i])) for i in indices if scores[i] > 0]
