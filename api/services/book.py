from models import Book
from pydantic import TypeAdapter
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from services import OpenAIEmbeddingService
from repositories import BookRepository, PaginatedResult
from schemas import BookSchema, BookCreateSchema, BookUpdateSchema, PaginatedBooksSchema


class BookService:
    def __init__(self, db: Session):
        self.book_repository = BookRepository(db)
        self.embedding_service = OpenAIEmbeddingService()

    def create(self, book_create_schema: BookCreateSchema) -> BookSchema:
        try:
            embedding: List[List[float]] = self.embedding_service.generate_document_embedding(
                [book_create_schema.summary])

            book = self.book_repository.create(
                book_create_schema, embedding[0])

            return BookSchema.model_validate(book)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Ocorreu um erro ao criar o documento. {e}")

    def get_one(self, book_id: int) -> BookSchema:
        book = self.book_repository.find_one(book_id)

        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Livro com id={book_id} não encontrado."
            )

        return BookSchema.model_validate(book)

    def update(self, id: int, book_update_schema: BookUpdateSchema) -> BookSchema:
        try:
            self.get_one(id)
            updated_book = self.book_repository.update(
                id, book_update_schema=book_update_schema)

            return BookSchema.model_validate(updated_book)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Ocorreu um erro ao criar o documento. {e}")

    def get_all(self) -> List[BookSchema]:
        books = self.book_repository.find_all()
        return TypeAdapter(List[BookSchema]).validate_python(books)

    def get_all_paginated(self, page: int, limit: int, filters: Optional[dict] = None) -> PaginatedBooksSchema:
        paginated: PaginatedResult[Book] = self.book_repository.find_all_paginated(
            page, limit, filters)
        return PaginatedBooksSchema.model_validate(paginated)

    def delete(self, book_id: int) -> None:
        self.book_repository.delete(book_id)
