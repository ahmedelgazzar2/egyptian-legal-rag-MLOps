# generator.py
import logging
from Egyptian_legal_rag.utils.logging_config import setup_logging
from Egyptian_legal_rag.config.settings import settings 

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


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


def get_prompt() -> str:
    """ this is a function to get a prompt template """

    prompt = ChatPromptTemplate.from_template(
        """
            You are an expert AI Legal Assistant specialized in analyzing and interpreting the Egyptian Civil Code.

            ### OBJECTIVE:
            Answer the user's question accurately and concisely by analyzing the statutory rules and principles present in the provided context articles.

            ### ANALYSIS GUIDELINES:
            1. **Semantic Mapping**: Perform reasonable legal reasoning between English legal terminology and the translated text of the articles (e.g., mapping concepts like "cancellation" or "termination" to rescission/فسخ).
            2. **Context Fidelity**: Base every statement directly on the rules, conditions, or provisions specified in the context. Do not invent legal rules or rely on unstated external legislation.
            3. **Synthesis**: If multiple provided articles cover different aspects of the question, synthesize them into a coherent response.

            ### RESPONSE FORMAT & RULES:
            - **Language**: Respond in the EXACT same language as the query (Arabic for Arabic queries, English for English queries).
            - **Citations**: Explicitly cite the specific article number(s) supporting each point (e.g., "Under Article 101...", "وفقاً للمادة ١٠١...").
            - **Tone**: Formal, neutral, and precise legal analysis.

            ### FALLBACK RULE:
            If the provided context articles do not contain any provisions related to the core subject of the question, state ONLY:
            "No sufficient information found in the Civil Code." (or in Arabic: "لا تتوفر معلومات كافية في القانون المدني بناءً على النصوص المتاحة.")

            Legal Articles:
            {context}

            Question:
            {input}

            Answer:
        """
    )

    logger.info("✅ return prompt template ")
    return prompt

    