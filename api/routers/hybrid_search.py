import uuid

from typing import List
from config import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request, Response
from services import HybridSearchService, OpenAIModelService
from schemas import HybridSearchResultSchema, ChatOutputSchema, QuerySchema

hybrid_search = APIRouter()


@hybrid_search.post(
    "/busca",
    response_model=List[HybridSearchResultSchema],
    summary="Lista todos os livros mais relevantes dado uma consulta"
)
def get_all_relevant_books(query_schema: QuerySchema, db: Session = Depends(get_db)):
    """
    Retorna os documentos mais relevantes.

    Parâmetros:
    - consulta (str): Busca textual
    - limite (int, opcional): Quantidade de documentos (default = 10).

    Retorna:
    - List[HybridSearchResultSchema]: Lista completa de documentos mais relevantes.
    """
    return HybridSearchService(db).filter_by_relevance(query_schema.query, query_schema.limit)


@hybrid_search.post(
    "/conversacao",
    response_model=ChatOutputSchema,
    summary="Gera uma resposta da IA com base na pergunta fornecida sobre programação em Python."
)
def chat(query_schema: QuerySchema, request: Request, response: Response):
    """
    Endpoint responsável por gerar uma resposta detalhada da IA com base na pergunta fornecida.

    Parâmetros:
    - query_schema (QuerySchema): Objeto contendo a pergunta feita pelo usuário.

    Retorna:
    - ChatOutputSchema: Objeto contendo a resposta textual gerada pela IA.
    """

    session_id: str | None = request.cookies.get("session")

    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session", value=session_id)

    return OpenAIModelService().generate_response(query_schema.query, session_id)
