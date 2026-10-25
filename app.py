from pathlib import Path
import streamlit as st

from src.config import settings
from src.document_processor import build_chunks_from_pdf, build_chunks_from_text, Chunk
from src.retriever import TfidfRetriever
from src.llm import generate_answer
from src.eligibility import check_pm_kisan_demo

st.set_page_config(page_title="GovGuide AI", page_icon="🏛️", layout="wide")

ROOT = Path(__file__).parent
DEMO_DOC = ROOT / "data/documents/PM-KISAN_Demo_Source_Summary.txt"

if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "retriever" not in st.session_state:
    st.session_state.retriever = TfidfRetriever()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sources" not in st.session_state:
    st.session_state.sources = []


def index_demo_document():
    text = DEMO_DOC.read_text(encoding="utf-8")
    chunks = build_chunks_from_text(text, DEMO_DOC.name)
    st.session_state.chunks = chunks
    st.session_state.retriever.fit(chunks)


def add_pdf(uploaded):
    import tempfile
    suffix = Path(uploaded.name).suffix or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getbuffer())
        tmp_path = tmp.name
    chunks = build_chunks_from_pdf(tmp_path)
    st.session_state.chunks.extend(chunks)
    st.session_state.retriever.fit(st.session_state.chunks)
    return len(chunks)

if not st.session_state.chunks:
    index_demo_document()

st.markdown("# 🏛️ GovGuide AI")
st.caption("RAG-powered assistant for simplifying and navigating government documents")

with st.sidebar:
    st.header("📚 Knowledge Base")
    st.write(f"**Indexed chunks:** {len(st.session_state.chunks)}")
    st.write(f"**LLM provider:** `{settings.provider}`")
    st.write(f"**Retrieval:** TF-IDF semantic-style lexical retrieval")

    uploaded = st.file_uploader("Upload an official PDF", type=["pdf"])
    if uploaded and st.button("➕ Index PDF", use_container_width=True):
        try:
            n = add_pdf(uploaded)
            st.success(f"Indexed {n} chunks from {uploaded.name}.")
        except Exception as exc:
            st.error(f"Could not process PDF: {exc}")

    if st.button("↻ Reset to demo document", use_container_width=True):
        st.session_state.chunks = []
        st.session_state.messages = []
        index_demo_document()
        st.rerun()

    st.divider()
    st.subheader("Response style")
    style = st.selectbox("Choose style", ["Simple English", "Hindi-friendly English", "Formal", "Explain like a beginner"])

    st.info("This project is educational. For current rules, dates, deadlines and official decisions, verify the source on the relevant government portal.")

left, right = st.columns([1.8, 1])

with left:
    st.subheader("💬 Ask the document")
    for role, content in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(content)

    prompt = st.chat_input("e.g. What are the major PM-KISAN exclusions?")
    if prompt:
        st.session_state.messages.append(("user", prompt))
        results = st.session_state.retriever.search(prompt, k=settings.top_k)
        try:
            answer = generate_answer(prompt, results, style=style)
        except Exception as exc:
            answer = f"The LLM call failed: {exc}\n\nYou can switch to `LLM_PROVIDER=demo` or configure an API-compatible provider in `.env`."
        st.session_state.messages.append(("assistant", answer))
        st.session_state.sources = results
        st.rerun()

with right:
    st.subheader("✅ Eligibility Checker")
    st.caption("PM-KISAN demo rules only — not an official determination.")
    with st.form("eligibility"):
        landholder = st.checkbox("I am a landholding farmer/farmer family", value=True)
        institutional = st.checkbox("I am an institutional land holder")
        constitutional = st.checkbox("I fall under a listed constitutional/elected-office exclusion")
        govt_employee = st.checkbox("I fall under a listed government employee exclusion")
        income_tax = st.checkbox("A family member paid income tax in the previous assessment year")
        professional = st.checkbox("A family member is a registered practicing professional in a listed category")
        submitted = st.form_submit_button("Check eligibility", use_container_width=True)
    if submitted:
        result = check_pm_kisan_demo({
            "landholder": landholder,
            "institutional_land": institutional,
            "constitutional_or_elected": constitutional,
            "govt_employee": govt_employee,
            "income_tax": income_tax,
            "professional_body": professional,
        })
        if result.status.startswith("Likely"):
            st.success(result.status)
        else:
            st.error(result.status)
        for label, status in result.checks:
            st.write(f"**{label}:** {status}")
        if result.reasons:
            st.write("**Why:**")
            for reason in result.reasons:
                st.write("- " + reason)

st.divider()
st.subheader("📌 Retrieved evidence")
if st.session_state.sources:
    for idx, r in enumerate(st.session_state.sources, start=1):
        page = f"Page {r.chunk.page}" if r.chunk.page else "Text source"
        with st.expander(f"{idx}. {r.chunk.source} — {page} — score {r.score:.3f}"):
            st.write(r.chunk.text)
else:
    st.write("Ask a question to see the evidence retrieved for the answer.")

st.divider()
st.caption("GovGuide AI • Academic project prototype • Retrieval-grounded responses • Verify against official government sources")
