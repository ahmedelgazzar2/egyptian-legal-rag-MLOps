#src/Egyptian_legal_rag/config/settings.py
from pathlib import Path
<<<<<<< HEAD

=======
>>>>>>> 2a1af8cdf4b8dad8ad79eb06b22353a1b5e1d992
from pydantic_settings import BaseSettings

_HERE = Path(__file__).resolve().parent  # config/
_ROOT = _HERE.parent.parent.parent # root

class Settings(BaseSettings):

    #  Project 
    ROOT_DIR: Path = _ROOT

    # Data 
    DATA_DIR: Path = ROOT_DIR / "data"
    PDF_DIR: Path = DATA_DIR / "raw" / "egyptian-civil-code.pdf"
    VECTOR_STORE_AR: Path = DATA_DIR / "vector_store_ar"
    VECTOR_STORE_EN: Path = DATA_DIR / "vector_store_en"
    JSON_AR: Path = DATA_DIR / "proccessed" / "egyptian-civil-code-ar.json"
    JSON_EN: Path = DATA_DIR / "proccessed" / "egyptian-civil-code-en.json"
<<<<<<< HEAD
    EMBEDDING_MODEL: str = "./data/onnx_model"
=======
>>>>>>> 2a1af8cdf4b8dad8ad79eb06b22353a1b5e1d992

    #  API Keys 
    GROQ_API_KEY: str

    # Models
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
<<<<<<< HEAD
    # EMBEDDING_MODEL: str = DATA_DIR / "onnx_model"
=======
>>>>>>> 2a1af8cdf4b8dad8ad79eb06b22353a1b5e1d992
    LLM_MODEL: str = "openai/gpt-oss-20b"

    # RAG 
    TOP_K: int = 5
    SEARCH_TYPE : str = "similarity"

    model_config = {
<<<<<<< HEAD
        "env_file": str(_ROOT / ".env"),  # root/configs/.env
=======
        "env_file": str(_ROOT / "configs" / ".env"),  # root/configs/.env
>>>>>>> 2a1af8cdf4b8dad8ad79eb06b22353a1b5e1d992
        "env_file_encoding": "utf-8",
    }


settings = Settings()
