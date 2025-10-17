import pytest

from main import app
from config import get_db
from http import HTTPStatus
from fastapi.testclient import TestClient
from .conftest import TestingSessionLocal


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


@pytest.mark.order(1)
def test_create_book(client):
    payload = {
        "autor": "J. K. Rowling",
        "titulo": "Harry Potter e a Pedra Filosofal",
        "resumo": "Primeiro livro da saga Harry Potter.",
        "data_publicacao": "1997-06-26"
    }
    response = client.post("api/v1/livros", json=payload)
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["titulo"] == payload["titulo"]
    assert data["autor"] == payload["autor"]


@pytest.mark.order(2)
def test_get_all_books(client):
    response = client.get("api/v1/livros")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) >= 1
    assert any(book["titulo"] ==
               "Harry Potter e a Pedra Filosofal" for book in data)


@pytest.mark.order(3)
def test_get_book_by_id(client):
    all_books = client.get("api/v1/livros").json()
    book_id = all_books[0]["id"]

    response = client.get(f"api/v1/livros/{book_id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == book_id


@pytest.mark.order(4)
def test_delete_book(client):
    all_books = client.get("api/v1/livros").json()
    book_id = all_books[0]["id"]

    response = client.delete(f"api/v1/livros/{book_id}")
    assert response.status_code == HTTPStatus.NO_CONTENT

    response_get = client.get(f"api/v1/livros/{book_id}")
    assert response_get.status_code == HTTPStatus.NOT_FOUND
