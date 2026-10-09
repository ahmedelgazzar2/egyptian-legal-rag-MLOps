#test_rag.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from Egyptian_legal_rag.api.main import app
from Egyptian_legal_rag.rag.Ragpipeline import RagPipeline


