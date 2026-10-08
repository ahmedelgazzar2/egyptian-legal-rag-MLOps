# Ragpipeline.py
import logging 
from langdetect import detect
from Egyptian_legal_rag.utils.logging_config import setup_logging
from Egyptian_legal_rag.config.settings import settings 
from Egyptian_legal_rag.rag.retrieval import load_retrieval
from Egyptian_legal_rag.rag.generator import load_LLM , get_prompt

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


# logger

logger = logging.getLogger(__name__)


class RagPipeline:
    def __init__(self):
        self.retriever_ar = load_retrieval("ar")
        self.retriever_en = load_retrieval("en")
        self.llm          = load_LLM(settings.LLM_MODEL)
        self.prompt       = get_prompt()

    def _get_retiever(self,question : str):
        lang = detect(question)

        if lang == 'ar':
            logger.info("ℹ️ arabic language detected and return arabic retriever")
            return self.retriever_ar
        else:
            logger.info("ℹ️ english language detected and return english retriever")
            return self.retriever_en

    def _format_docs(self,docs):
        return "\n\n".join([
                f"Article {doc.metadata['article_number']}:\n{doc.page_content}"
                for doc in docs
            ])


    # def _get_chain(self,question : str):
        
    #     try:
    #         retrieval = self._get_retiever(question)

    #         chain = (
    #                 {"context": retrieval | self._format_docs, "input": RunnablePassthrough()}
    #                 | self.prompt
    #                 | self.llm
    #                 | StrOutputParser()
    #             )

    #         logger.info("✅ chain returns successfully ")
    #         return chain
    #     except Exception:
    #         logger.exception("❌ error , there is an error while returnning chain ")

    def ask(self,question : str) -> dict:

        retriever = self._get_retiever(question)
        docs = retriever.invoke(question)
        #context = self._format_docs(docs)

        if not retriever or not docs :
            logger.error("❌ error while loading retriever or docs or context")

        chain = (
            {"context": retriever | self._format_docs, "input": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        if chain:
            logger.info("✅ chain created successfully")

        answer = chain.invoke({"input": question})
        if answer:
            logger.info("✅ llm generate answer successfully")

        sources = list(set([
                f"Article {doc.metadata['article_number']}"
                for doc in docs
            ]))
        if sources:
            logger.info("✅ sources loaded successfully")


        logger.info("✅ return answer meta data")
        return {
            "question": question,
            "answer":   answer,
            "sources":  sources
        }
