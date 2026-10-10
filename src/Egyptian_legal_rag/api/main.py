# main.py
from fastapi import FastAPI, HTTPException , Depends
from pydantic import BaseModel, Field , field_validator
from contextlib import asynccontextmanager

from Egyptian_legal_rag.config.settings import Settings
from Egyptian_legal_rag.rag.Ragpipeline import RagPipeline
from Egyptian_legal_rag.utils.logging_config import setup_logging

import logging


# logger
setup_logging()

logger = logging.getLogger(__name__)

# Global instance

rag_pipeline = RagPipeline()

# life span

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_pipeline

    rag_pipeline = RagPipeline()

    yield

    rag_pipeline = None


#  Dependency 

def get_rag_pipeline() -> RagPipeline:
    return rag_pipeline


app = FastAPI(
    title="Egyptian Legal RAG API",
    description="RAG API for querying the Egyptian Civil Code",
    version="1.0.0",
    lifespan=lifespan
)


# Request / Response Models


### question model

class AskRequest(BaseModel):
    question : str = Field(
        ...,
        min_length=1,
        description="Question about the Egyptian Civil Code"
    )

    ### validate AskRequest model

    @field_validator("question")
    @classmethod
    def validate_question(cls,question: str) -> str:

        question = question.strip()

        if not question:
            raise HTTPException(
                status_code=422,
                detail="Question cannot be empty"
            )

        return question



### response model

class AskResponse(BaseModel):
    answer : str 
    sources : list[str]


###  HealthResponse model

class HealthResponse(BaseModel):
    status: str
    documents_indexed: int


# APIs

@app.get("/")
def read_root():
    return {"message": "Egyptian Legal RAG API is up and running!"}


### health API

@app.get("/health",response_model=HealthResponse)
def health(rag : RagPipeline = Depends(get_rag_pipeline)):
    logger.info("✅ Health check requested")

    return HealthResponse(
        status = "healthy",
        documents_indexed=rag.document_count
        )



### Ask API

@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest , rag : RagPipeline = Depends(get_rag_pipeline)):


    try:
        question = request.question.strip()

        logger.info("ℹ️ recieve a question")

        result = await rag.ask(question)

        if result:
            logger.info("✅ recieve a question")

            return AskResponse(
                answer=result["answer"],
                sources=result["sources"]
            )
    
    except Exception:
        logger.exception("❌ Failed to process question")
        raise
        # raise HTTPException(
        #     status_code=500,
        #     detail="Failed to process the question"
        # )