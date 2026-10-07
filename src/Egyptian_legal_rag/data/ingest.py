import json
import logging
from pathlib import Path
from Egyptian_legal_rag.config.settings import settings 

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# logger

logger = logging.getLogger(__name__)