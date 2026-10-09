import json
import logging
from pathlib import Path
from Egyptian_legal_rag.utils.logging_config import setup_logging
from Egyptian_legal_rag.config.settings import settings 

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# logger

logger = logging.getLogger(__name__)

# load json 
def load_json(path):
    """ function to load json files """
    logger.info(f"🚀 starting loading json file from {path}")

    try:
        logger.info(f"🔄 loading json file from {path}")

        with open(path, 'r', encoding='utf-8') as f:
            articles = json.load(f)

        if articles:
            logger.info(f"✅ json file loaded well from {path} with length {len(articles)}")
            return articles
        
        logger.warning(f"⚠️ empty file")
    
    except Exception:
        logger.exception(f"❌ error , can't load file from {path}")




# convert json to documents

def convert_json_to_docs(articles,lang):
    """function to detect your article language and convert json to documents"""
    logger.info(f"🚀 starting converting json file to documents")
    docs_ar = []
    doc_en = []

    if lang == "ar":
        logger.info(f"ℹ️ arabic language detected ")
        logger.info(f"🚀 start converting arabic json files into documents")
        for article in articles:
            combined_text = (
                f"مادة {article['article_number']}\n"
                f"{article['text']}"
            )

            doc = Document(
                page_content=combined_text,
                metadata={
                    "article_number": article['article_number'],
                    'is_repealed':    article['is_repealed'],
                    "source":         f"Article {article['article_number']}"
                }
            )

            docs_ar.append(doc)
        if docs_ar:  
            logger.info(f"✅ arabic json file converted into documents")
            return docs_ar
        logger.warning(f"⚠️ empty arabic documents")
    else:
        for article in articles:

            combined_text = (
                f"Article {article['article_number']}\n"
                f"{article['text']}"
            )

            doc = Document(
                page_content=combined_text,
                metadata={
                    "article_number": article['article_number'],
                    'is_repealed':    article['is_repealed'],
                    "source":         f"Article {article['article_number']}"
                }
            )

            doc_en.append(doc)

        if doc_en:  
            logger.info(f"✅ english json file converted into documents")
            return doc_en
        logger.warning(f"⚠️ empty english documents")


# loading embedding 

def load_embeddings(model_name : str):
    """ loading the embedded model  """
    try:
        logger.info(f"🚀 start loading the embedded model {model_name}")

        embeddings = HuggingFaceEmbeddings(model_name=model_name)

        if embeddings:
            logger.info(f"✅ embedded model {model_name} loaded ")
            return embeddings
        
        logger.warning(f"⚠️ i can't load embedded model {model_name}")
    except Exception:
        logger.exception(f"error when loading embedded model {model_name}")
        raise



# create and save vector store

def Create_vector_store(path,docs,embeddings):
    """ create and save vector store """

    try:
        logger.info(f"🚀 start creating vector store using FAISS for PATH {path}")

        vector_store = FAISS.from_documents(docs, embeddings)

        if vector_store:
            logger.info(f"✅ vector store created for PATH {path} ") 
        else:
            logger.warning(f"⚠️ failed to create vector store for PATH {path}")

        vector_store.save_local(Path(path))
        logger.info(f"✅ Saving vector store locally at PATH {path} ") 
    except Exception:
        logger.exception(f"❌failed creating or saving vector store for PATH {path}")
        raise



if __name__ == "__main__":

    setup_logging()
    try:
        arabic_articles = load_json(settings.JSON_AR)
        english_articles = load_json(settings.JSON_EN)

        docs_ar = convert_json_to_docs(arabic_articles,lang='ar')
        docs_en = convert_json_to_docs(english_articles, lang="en")
        print("arabic document type",docs_ar[0])
        print("english document type",docs_en[0])


        embeddings = load_embeddings(settings.EMBEDDING_MODEL)

        Create_vector_store(settings.VECTOR_STORE_AR,docs_ar,embeddings)
        Create_vector_store(settings.VECTOR_STORE_EN,docs_en,embeddings)

    except Exception:
        logger.exception(f"❌failed to ingest data")