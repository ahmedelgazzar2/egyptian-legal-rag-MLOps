#test_rag.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock , AsyncMock, patch
from Egyptian_legal_rag.api.main import app

from Egyptian_legal_rag.rag.retrieval import load_retrieval

# Fixtures & Mocks

@pytest.fixture
def mock_rag():
    """ a mock RagPipeline instance  """
    with patch("Egyptian_legal_rag.api.main.RagPipeline") as mock:

        instance = MagicMock()

        instance.ask = AsyncMock(
            return_value = {
            "answer": "وفقاً للمادة 150 من القانون المدني...",
            "sources": ["Article 150", "Article 151"]
            }
        )
        instance.document_count = 1994
        mock.return_value = instance
        yield instance


@pytest.fixture
def client(mock_rag):
    with TestClient(app) as c:
        yield c


# Test Cases

### Unit tests

def test_health_endpoint(client):
    """ this is a function to test the api health endpoint """
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()

    assert data['status'] == "healthy"
    assert "documents_indexed" in data
    assert data['documents_indexed'] == 1994


def test_ask_arabic(client):
    response = client.post("/ask",json={"question": "ما هي شروط العقد؟"})
    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data


def test_ask_english(client):
    response = client.post("/ask",json={"question": "What are contract conditions?"})
    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data


def test_ask_empty_question(client):
    response = client.post("/ask",json={"question": ""})
    assert response.status_code == 422


def test_ask_whitespace_question(client):
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 422


def test_ask_missing_question(client):
    response = client.post("/ask", json={})
    assert response.status_code == 422


### integration test


#####  test retrieval

def test_ar_retriever_returns():
    """ this is a function to test the documents return from retriever for arabic questions """
    retriever = load_retrieval('ar')

    docs = retriever.invoke("ما هي شروط صحة العقد؟")

    assert len(docs) > 0
    assert all(
        isinstance(doc.page_content, str)
        for doc in docs
    )

    assert all(
        "article_number" in doc.metadata
        for doc in docs
    )


def test_en_retriever_returns():
    """ this is a function to test the documents return from retriever for english questions """
    retriever = load_retrieval('en')

    docs = retriever.invoke("What are contract conditions?")

    assert len(docs) > 0
    assert all(
        isinstance(doc.page_content, str)
        for doc in docs
    )

    assert all(
        "article_number" in doc.metadata
        for doc in docs
    )