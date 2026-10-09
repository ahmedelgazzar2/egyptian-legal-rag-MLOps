# retrieval.py

import logging
from pathlib import Path

from Egyptian_legal_rag.utils.logging_config import setup_logging
from Egyptian_legal_rag.config.settings import settings 
from Egyptian_legal_rag.data.ingest import load_embeddings

from langchain_community.vectorstores import FAISS

# logger

logger = logging.getLogger(__name__)



# load vector store

def load_vector_store(path, embeddings):
    """ loading a vector store """

    try:
        logger.info(f"🔄 start loading vector store using FAISS for PATH {path}")

        vector_store = FAISS.load_local(
            path, 
            embeddings,
            allow_dangerous_deserialization=True
        )

        if vector_store:
            logger.info(f"✅ vector store loaded from PATH {path} ")
            return vector_store
        else:
            logger.warning(f"⚠️ failed loading vector store from PATH {path}")
    except Exception:
        logger.exception(f"❌failed to load vector store from PATH {path}")
        raise


# retrieval

def load_retrieval(lang : str = 'ar'):
    """ this is a function to load the specific retrieval for every language """

    logger.info(f"🔄 start loading embedding model")
    embeddings = load_embeddings(settings.EMBEDDING_MODEL)
    logger.info(f"✅ embedded model loaded successfuly")

    if lang == 'ar':
        path = settings.VECTOR_STORE_AR
        logger.info(f"ℹ️ go to arabic path")
    elif lang == 'en':
        path = settings.VECTOR_STORE_EN
        logger.info(f"ℹ️ go to english path")
    else:
        logger.error(f"❌ error wrong language detected ")

    logger.info(f"🔄 start loading vector store using FAISS for PATH {path}")
    vector_store = load_vector_store(path,embeddings)
    if vector_store:
        logger.info(f"✅ vector store loaded from PATH {path} ")
    else:
        logger.warning(f"⚠️ failed loading vector store from PATH {path}")

    retrieval = vector_store.as_retriever(search_type=settings.SEARCH_TYPE,search_kwargs={"k": settings.TOP_K})

    if retrieval:
        logger.info(f"✅ return {"arabic" if lang == 'ar' else "english"} retrieval successfully")
        return retrieval
    logger.warning(f"⚠️ failed return {"arabic" if lang == 'ar' else "english"} retrieval")

    
