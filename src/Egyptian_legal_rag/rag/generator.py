# generator.py
import logging
from Egyptian_legal_rag.utils.logging_config import setup_logging
from Egyptian_legal_rag.config.settings import settings 

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 🚀 ✅ 🔄 ⚠️ ❌ ℹ️

# logger

logger = logging.getLogger(__name__)

def load_LLM(model):
    """ this is a function to load my llm """

    try:
        logger.info(f"🔄 {model} loading ")
        llm = ChatGroq(
            model=settings.LLM_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature = 0,
        )

        if llm:
            logger.info(f"✅ {model} loaded successfully")
            return llm
        logger.warning(f"⚠️ can't load {model}")
    except Exception:
        logger.exception(f"❌ error , can't load {model}")


def get_prompt(context,question) -> str:
    """ this is a function to get a prompt template """

    prompt = ChatPromptTemplate.from_template(
        """
            You are a legal assistant specialized in the Egyptian Civil Code.

            Follow these rules strictly:

            1. Answer the question using ONLY the legal articles provided in the context.
            2. Do NOT use external legal knowledge or information that is not explicitly stated in the context.
            3. Mention the relevant article number(s) in your answer.
            4. Answer in the SAME LANGUAGE as the user's question:
            - If the question is in Arabic, answer in Arabic.
            - If the question is in English, answer in English.
            5. Do NOT translate the answer into another language.
            6. If the provided articles do not contain enough information to answer the question, say:
            "No sufficient information found in the Civil Code."
            7. Do not make general legal conclusions from an article that applies only to a specific situation.
            8. If the retrieved articles are not relevant to the question, explicitly say that the provided articles are not sufficient to answer the question.

            Legal Articles:
            {context}

            Question:
            {input}

            Answer:
        """
    )

    logger.info("✅ return prompt template ")
    return prompt

    