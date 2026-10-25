from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    provider: str = os.getenv("LLM_PROVIDER", "demo")
    api_key: str = os.getenv("LLM_API_KEY", "")
    base_url: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    ollama_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    top_k: int = int(os.getenv("TOP_K", "5"))
    embedding_mode: str = os.getenv("EMBEDDING_MODE", "tfidf")

settings = Settings()
