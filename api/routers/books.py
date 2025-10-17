from config import get_db
from http import HTTPStatus
from services import BookService
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from repositories import AuthenticationRepository
from schemas import BookSchema, BookCreateSchema, PaginatedBooksSchema, UserProfileSchema

book = APIRouter()


@book.post(
    "/livros",
    status_code=HTTPStatus.CREATED,
    response_model=BookSchema,
    summary="Cria um novo livro"
)
def create_book(book_create_schema: BookCreateSchema,
                current_user: UserProfileSchema = Depends(
                    AuthenticationRepository.get_current_user),
                db: Session = Depends(get_db)):
    """
    Cria um novo livro no sistema.

    Parâmetros:
    - book_create_schema (BookCreateSchema): Dados do livro a ser criado.

    Retorna:
    - BookSchema: Dados do livro recém-criado.
    """
    return BookService(db).create(book_create_schema)


@book.get(
    "/livros/paginado",
    response_model=PaginatedBooksSchema,
    summary="Lista livros de forma paginada"
)
def get_all_paginated_books(pagina: int = Query(default=1, ge=1),
                            limite: int = Query(default=10, ge=1),
                            titulo: Optional[str] = Query(
                                default=None, description="Filtra por título (opcional)"),
                            autor: Optional[str] = Query(
                                default=None, description="Filtra por autor (opcional)"),
                            current_user: UserProfileSchema = Depends(
                                AuthenticationRepository.get_current_user),
                            db: Session = Depends(get_db)):
    """
    Retorna uma lista paginada de todos os livros.

    Parâmetros:
    - pagina (int, opcional): Número da página a ser retornada (default = 1).
    - limite (int, opcional): Quantidade de livros por página (default = 10).

    Retorna:
    - List[BookSchema]: Lista de livros da página solicitada.
    """
    filters = {}

    if titulo:
        filters['titulo'] = titulo

    if autor:
        filters['autor'] = autor

    return BookService(db).get_all_paginated(pagina, limite, filters)


@book.get(
    "/livros",
    response_model=List[BookSchema],
    summary="Lista todos os livros"
)
def get_all_books(current_user: UserProfileSchema = Depends(AuthenticationRepository.get_current_user),
                  db: Session = Depends(get_db)):
    """
    Retorna todos os livros para o usuário autenticado.

    Retorna:
    - List[BookSchema]: Lista completa de todos os livros.
    """
    return BookService(db).get_all()


@book.get(
    "/livros/{id}",
    response_model=BookSchema,
    summary="Consulta livro por ID"
)
def get_one_book(id: int,
                 current_user: UserProfileSchema = Depends(
                     AuthenticationRepository.get_current_user),
                 db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um livro específico pelo seu ID.

    Parâmetros:
    - id (int): ID do livro a ser consultado.

    Retorna:
    - BookSchema: Dados do livro solicitado.
    """
    return BookService(db).get_one(id)


@book.delete(
    "/livros/{id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Exclui um livro por ID"
)
def delete_book(id: int,
                current_user: UserProfileSchema = Depends(
                    AuthenticationRepository.get_current_user),
                db: Session = Depends(get_db)):
    """
    Remove um livro específico pelo seu ID.

    Parâmetros:
    - id (int): ID do livro a ser excluído.

    Retorna:
    - Nenhum conteúdo (HTTP 204) se a exclusão for bem-sucedida.
    """
    BookService(db).delete(id)
