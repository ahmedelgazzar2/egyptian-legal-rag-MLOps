# Ragpipeline.py
import logging

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langdetect import detect

from Egyptian_legal_rag.config.settings import settings
from Egyptian_legal_rag.rag.generator import get_prompt, load_LLM
from Egyptian_legal_rag.rag.retrieval import (
    load_embeddings,
    load_retrieval,
    load_vector_store,
)

# logger

logger = logging.getLogger(__name__)


class RagPipeline:
    def __init__(self):
        self.retriever_ar = load_retrieval("ar")
        self.retriever_en = load_retrieval("en")
        self.llm = load_LLM(settings.LLM_MODEL)
        self.prompt = get_prompt()
        self.embeddings = load_embeddings(settings.EMBEDDING_MODEL)
        self.vector_store_ar = load_vector_store(
            settings.VECTOR_STORE_AR, self.embeddings
        )
        self.vector_store_en = load_vector_store(
            settings.VECTOR_STORE_AR, self.embeddings
        )

    @property
    def document_count(self) -> int:
        """getting the number of indexing documents"""

        n_documents = (
            self.vector_store_ar.index.ntotal + self.vector_store_en.index.ntotal
        )
        return n_documents

    def _get_retiever(self, question: str):
        lang = detect(question)

        if lang == "ar":
            logger.info("ℹ️ arabic language detected and return arabic retriever")
            return self.retriever_ar
        else:
            logger.info("ℹ️ english language detected and return english retriever")
            return self.retriever_en

    def _format_docs(self, docs):
        return "\n\n".join(
            [
                f"Article {doc.metadata['article_number']}:\n{doc.page_content}"
                for doc in docs
            ]
        )

    async def ask(self, question: str) -> dict:

        retriever = self._get_retiever(question)
        docs = retriever.invoke(question)
        # context = self._format_docs(docs)

        if not retriever or not docs:
            logger.error("❌ error while loading retriever or docs or context")

        chain = (
            {"context": retriever | self._format_docs, "input": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        if chain:
            logger.info("✅ chain created successfully")

        answer = await chain.ainvoke(question)
        if answer:
            logger.info("✅ llm generate answer successfully")

        sources = list({f"Article {doc.metadata['article_number']}" for doc in docs})
        sources = set(sources)
        if sources:
            logger.info("✅ sources loaded successfully")

        logger.info("✅ return answer meta data")
        return {"question": question, "answer": answer, "sources": sources}
