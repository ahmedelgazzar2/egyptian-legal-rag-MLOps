#src/Egyptian_legal_rag/config/settings.py
from pathlib import Path
from pydantic_settings import BaseSettings

_HERE = Path(__file__).resolve().parent  # config/
_ROOT = _HERE.parent.parent.parent # root

class Settings(BaseSettings):

    # ── Project ──
    ROOT_DIR: Path = _ROOT

    # ── Data ──
    DATA_DIR: Path = ROOT_DIR / "data"
    PDF_DIR: Path = DATA_DIR / "egyptian-civil-code.pdf"
    VECTOR_STORE_AR: Path = DATA_DIR / "vector_store_ar"
    VECTOR_STORE_EN: Path = DATA_DIR / "vector_store_en"
    JSON_AR: Path = DATA_DIR / "egyptian-civil-code-ar.json"
    JSON_EN: Path = DATA_DIR / "egyptian-civil-code-en.json"

    # ── API Keys ──
    GROQ_API_KEY: str

    # ── Models ──
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    LLM_MODEL: str = "openai/gpt-oss-20b"

    # ── RAG ──
    TOP_K: int = 5

    model_config = {
        "env_file": str(_ROOT / "configs" / ".env"),  # root/configs/.env
        "env_file_encoding": "utf-8",
    }


settings = Settings()
