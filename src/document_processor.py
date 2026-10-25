from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import re

from pypdf import PdfReader

@dataclass
class Chunk:
    text: str
    source: str
    page: int | None = None
    chunk_id: str = ""


def extract_text_from_pdf(file_path: str | Path) -> list[tuple[int, str]]:
    reader = PdfReader(str(file_path))
    pages = []
    for idx, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = re.sub(r"\s+", " ", text).strip()
        pages.append((idx, text))
    return pages


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(len(words), start + chunk_size // 5)
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        if end == len(words):
            break
        start = max(0, end - overlap // 5)
    return chunks


def build_chunks_from_pdf(file_path: str | Path) -> list[Chunk]:
    path = Path(file_path)
    chunks: list[Chunk] = []
    counter = 1
    for page_no, text in extract_text_from_pdf(path):
        for piece in chunk_text(text):
            chunks.append(Chunk(piece, path.name, page_no, f"{path.stem}-{counter}"))
            counter += 1
    return chunks


def build_chunks_from_text(text: str, source: str = "uploaded_text") -> list[Chunk]:
    return [Chunk(piece, source, None, f"{source}-{i}") for i, piece in enumerate(chunk_text(text), start=1)]
