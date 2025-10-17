import pytest

from main import app
from config import get_db
from http import HTTPStatus
from unittest.mock import patch
from .conftest import TestingSessionLocal
from fastapi.testclient import TestClient


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def mock_hybrid_search_service():
    with patch("routers.hybrid_search.HybridSearchService") as MockService:
        instance = MockService.return_value
        instance.filter_by_relevance.return_value = [
            {"id": 1, "titulo": "Harry Potter",
                "resumo": "Resumo exemplo", "pontuacao": 0.9}
        ]
        instance._semantich_search.return_value = [
            {"id": 2, "titulo": "Harry Potter",
                "resumo": "Resumo exemplo", "pontuacao": 0.9}
        ]
        yield instance


@pytest.fixture
def mock_generate_response():
    with patch("routers.hybrid_search.OpenAIModelService") as MockOpenAI:
        instance = MockOpenAI.return_value
        instance.generate_response.return_value = {
            "response": "Essa é uma resposta simulada da IA."}
        yield instance


@pytest.mark.order(1)
def test_get_all_relevant_books(client, mock_hybrid_search_service):
    payload = {"query": "Harry Potter"}
    response = client.post("/api/v1/busca", json=payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["titulo"] == "Harry Potter"
    assert data[0]["resumo"] == "Resumo exemplo"


@pytest.mark.order(2)
def test_chat(client, mock_hybrid_search_service, mock_generate_response):
    payload = {"query": "Quem é o autor de Harry Potter?"}
    response = client.post("/api/v1/conversacao", json=payload)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "resposta" in data
    assert data["resposta"] == "Essa é uma resposta simulada da IA."
