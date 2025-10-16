import math

from models import Book
from pytz import timezone
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload, Session
from schemas import BookCreateSchema, BookUpdateSchema
from repositories import CRUDRepository, PaginatedResult


class BookRepository(CRUDRepository[Book, BookCreateSchema, BookUpdateSchema, int]):
    def __init__(self, db: Session):
        self.db = db

    def create(self, book_create_schema: BookCreateSchema, embedding: List[float]) -> Book:
        new_book = Book(author=book_create_schema.author,
                        title=book_create_schema.title,
                        summary=book_create_schema.summary,
                        embedding=embedding)

        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        return new_book

    def find_one(self, id: int) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id == id, Book.deleted_at.is_(None)).first()

    def find_all(self, filters: Optional[dict] = None, relations: Optional[List[str]] = None) -> List[Book]:
        load_options = []

        query = self.db.query(Book)

        if filters:
            for field, value in filters.items():
                if value is None or value == "":
                    continue

                if hasattr(Book, field):
                    column = getattr(Book, field)
                    if isinstance(value, str):
                        query = query.filter(column.ilike(f"%{value}%"))
                    else:
                        query = query.filter(column == value)

        if relations:
            load_options = [joinedload(getattr(Book, rel))
                            for rel in relations]
            query = query.options(*load_options)

        return query.all()

    def find_all_paginated(self, page: int = 1, limit: int = 10) -> PaginatedResult[Book]:
        total = self.db.query(Book).count()

        offset = (page - 1) * limit

        itens = (
            self.db.query(Book)
            .offset(offset)
            .limit(limit)
            .all()
        )

        total_pages = math.ceil(total / limit) if total > 0 else 1

        return PaginatedResult(
            total=total,
            pagina=page,
            limite=limit,
            itens=itens,
            total_paginas=total_pages
        )

    def update(self, id: int, book_update_schema: BookUpdateSchema) -> Book:
        pass

    def delete(self, id: int) -> None:
        try:
            book = self.db.query(Book).filter(Book.id == id).first()

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Livro com id={id} não encontrado ou já excluído."
                )

            book.deleted_at = datetime.now(timezone.utc)
            self.db.add(book)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e
