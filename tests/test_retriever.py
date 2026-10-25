from src.document_processor import build_chunks_from_text
from src.retriever import TfidfRetriever


def test_retrieval_returns_relevant_chunk():
    chunks = build_chunks_from_text(
        "PM-KISAN provides income support to eligible landholding farmer families. "
        "The guidelines describe exclusions for certain categories. "
        "The application process is described separately."
    )
    r = TfidfRetriever()
    r.fit(chunks)
    results = r.search("landholding farmer families", k=2)
    assert results
    assert "landholding" in results[0].chunk.text.lower()
