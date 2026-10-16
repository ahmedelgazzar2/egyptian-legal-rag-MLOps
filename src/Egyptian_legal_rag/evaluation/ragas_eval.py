# ragas_eval.py
import sys
import types

dummy_module = types.ModuleType("langchain_community.chat_models.vertexai")
dummy_module.ChatVertexAI = type("ChatVertexAI", (object,), {})
sys.modules["langchain_community.chat_models.vertexai"] = dummy_module

import os

# 💡 قطع الاتصال نهائياً بأي سيرفر لـ OpenAI وخداع المكتبة
os.environ["OPENAI_API_KEY"] = "sk-dummy-key-not-needed"
os.environ["OPENAI_API_BASE"] = "http://localhost:9999/v1"  # عنوان وهمي يمنع إرسال أي طلب حقيقي للخارج

import logging
import pandas as pd
from datasets import Dataset
from langchain_groq import ChatGroq
from Egyptian_legal_rag.evaluation.config.config import eval_data
from Egyptian_legal_rag.config.settings import settings 
from Egyptian_legal_rag.data.ingest import load_embeddings
from Egyptian_legal_rag.rag.generator import load_LLM

from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import HuggingFaceEmbeddings
from ragas.metrics import Faithfulness, AnswerRelevancy,ContextPrecision, ContextRecall
# from ragas.metrics.collections import (
#     answer_relevancy,
#     context_precision,
#     context_recall,
#     faithfulness,
# )


# logger

logger = logging.getLogger(__name__)


# METRICS = [
#     Faithfulness(llm=evaluator_llm),
#     AnswerRelevancy(llm=evaluator_llm, embeddings=embedding_model),  # هذا هو المسؤول عن الـ 401
#     ContextPrecision(llm=evaluator_llm),
#     ContextRecall(llm=evaluator_llm),
# ]

def evaluate_results(records: list[dict], evaluator_llm, evaluator_embeddings) -> dict[str, float]:
    """
    Each record must contain:
        question, answer, contexts, ground_truth
    """
    if not records:
        logger.error("❌ Cannot evaluate an empty dataset")
        return {}

    # 💡 تعريف المقاييس هنا يضمن أنها تستخدم الكائنات الجاهزة تماماً
    metrics = [
        Faithfulness(llm=evaluator_llm),
        AnswerRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),
        ContextPrecision(llm=evaluator_llm),
        ContextRecall(llm=evaluator_llm),
    ]

    dataset = Dataset.from_list(records)
    
    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
    )       

    scores = result.to_pandas()

    return {
        metric: scores[metric].mean()
        for metric in [
            "faithfulness",
            # "answer_relevancy",
            "context_precision",
            "context_recall",
        ]
    }

if __name__ == "__main__":
    llm = load_LLM(settings.LLM_MODEL)
    logger.info("✅ model loaded")
    evaluator_llm = LangchainLLMWrapper(llm)

    embedding_model = HuggingFaceEmbeddings(model=settings.EMBEDDING_MODEL)

    result = evaluate_results(eval_data, evaluator_llm, embedding_model)
    
    if result:
        logging.info("✅ evaluate_results work well")
        logging.info(result)
    else:  
        logging.error("❌ failed to evaluate data")