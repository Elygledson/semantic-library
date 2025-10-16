from typing import List
from config import get_db
from sqlalchemy.orm import Session
from services import HybridSearchService
from schemas import HybridSearchResultSchema
from fastapi import APIRouter, Depends, Query

hybrid_search = APIRouter()


@hybrid_search.get(
    "/busca",
    response_model=List[HybridSearchResultSchema],
    summary="Lista todos os documentos mais relevantes"
)
def get_all_relevant_documents(consulta: str, limite: int = Query(default=10, ge=1), db: Session = Depends(get_db)):
    """
    Retorna os documentos mais relevantes.

    Parâmetros:
    - consulta (str): busca textual
    - limite (int, opcional): Quantidade de documentos (default = 10).

    Retorna:
    - List[HybridSearchResultSchema]: Lista completa de documentos mais relevantes.
    """
    return HybridSearchService(db).filter_by_relevance(consulta, limite)
