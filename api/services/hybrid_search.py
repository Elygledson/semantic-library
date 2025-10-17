from models import Book
from typing import List
from pydantic import TypeAdapter
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from services import OpenAIEmbeddingService
from schemas import HybridSearchResultSchema


class HybridSearchService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = OpenAIEmbeddingService()

    def _semantich_search(self, query_text: str, limit: int):
        """
        Realiza busca semântica com embeddings.
        """
        query_embedding: List[float] = self.embedding_service.generate_query_embedding(
            query_text)

        semantic_subq = (
            select(
                Book.id.label("id"),
                Book.title.label("title"),
                Book.summary.label("summary"),
                func.rank().over(
                    order_by=Book.embedding.cosine_distance(
                        query_embedding)
                ).label("rank"),
            )
            .order_by(Book.embedding.cosine_distance(query_embedding))
            .limit(limit)
            .subquery()
        )

        return semantic_subq
    
    def _search_full_text(self, query_text: str, limit: int):
        """
        Realiza busca textual com PostgreSQL full-text search.
        """
        ts_query = func.plainto_tsquery("portuguese", query_text)

        keyword_subq = (
            select(
                Book.id.label("id"),
                Book.title.label("title"),
                Book.summary.label("summary"),
                func.rank().over(
                    order_by=func.ts_rank_cd(
                        func.to_tsvector(
                            "portuguese", Book.summary),
                        ts_query
                    ).desc()
                ).label("rank"),
            )
            .where(
                func.to_tsvector("portuguese", Book.summary).op(
                    "@@")(ts_query)
            )
            .order_by(
                func.ts_rank_cd(
                    func.to_tsvector(
                        "portuguese", Book.summary), ts_query
                ).desc()
            )
            .limit(limit)
            .subquery()
        )
        
        return keyword_subq
        

    def filter_by_relevance(self, query_text: str, limit: int, k: int = 10) -> List[HybridSearchResultSchema]:
        """
        Busca híbrida: combina semelhança de embeddings e busca textual.
        """
        semantic_subq = self._semantich_search(query_text, limit)
        keyword_subq = self._search_full_text(query_text)

        stmt = (
            select(
                semantic_subq.c.id,
                semantic_subq.c.title.label('titulo'),
                semantic_subq.c.summary.label('resumo'),
                (
                    func.coalesce(1.0 / (k + semantic_subq.c.rank), 0.0) +
                    func.coalesce(1.0 / (k + keyword_subq.c.rank), 0.0)
                ).label("pontuacao")
            )
            .outerjoin(keyword_subq, semantic_subq.c.id == keyword_subq.c.id)
            .order_by(
                (
                    func.coalesce(1.0 / (k + semantic_subq.c.rank), 0.0) +
                    func.coalesce(1.0 / (k + keyword_subq.c.rank), 0.0)
                ).desc()
            )
            .limit(limit)
        )

        results = self.db.execute(stmt).mappings().all()
        return TypeAdapter(List[HybridSearchResultSchema]).validate_python(results)
