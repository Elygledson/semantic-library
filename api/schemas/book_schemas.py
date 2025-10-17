from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class BookCreateSchema(BaseModel):
    author: str = Field(..., alias="autor")
    title: str = Field(..., alias="titulo")
    summary: str = Field(..., alias="resumo")
    publication_date: date = Field(..., alias="data_publicacao")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "autor": "Machado de Assis",
                "titulo": "Dom Casmurro",
                "resumo": "Um clássico da literatura brasileira que explora ciúmes, dúvida e traição.",
                "data_publicacao": "2025-10-16",
            }
        }
    )


class BookUpdateSchema(BaseModel):
    author: Optional[str] = Field(None, alias="autor")
    title: Optional[str] = Field(None, alias="titulo")
    summary: Optional[str] = Field(None, alias="resumo")
    publication_date: Optional[date] = Field(None, alias="data_publicacao")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, json_schema_extra={
        "example": {
            "autor": "Machado de Assis",
            "titulo": "Dom Casmurro - Edição Revisada",
            "resumo": "Versão revisada do clássico sobre ciúmes e ambiguidade de sentimentos.",
            "data_publicacao": "2025-10-16",
        }
    })


class BookSchema(BaseModel):
    id: int
    author: str = Field(..., alias="autor")
    title: str = Field(..., alias="titulo")
    summary: str = Field(..., alias="resumo")
    publication_date: date = Field(..., alias="data_publicacao")
    created_at: datetime = Field(..., alias="criado_em")
    updated_at: datetime = Field(..., alias="atualizado_em")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, json_schema_extra={
        "example": {
            "id": 1,
            "autor": "Clarice Lispector",
            "titulo": "A Hora da Estrela",
            "resumo": "Uma narrativa introspectiva sobre a vida e a alienação de Macabéa.",
            "data_publicacao": "2025-10-16",
            "criado_em": "2025-10-16T14:20:00-03:00",
            "atualizado_em": "2025-10-16T14:20:00-03:00",
        }
    })


class PaginatedBooksSchema(BaseModel):
    total: int
    page: int = Field(..., alias="pagina")
    limit: int = Field(..., alias="limite")
    items: List[BookSchema] = Field(..., alias="itens")
    total_pages: int = Field(..., alias="total_paginas")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, json_schema_extra={"json_schema_extra": {
        "example": {
            "total": 2,
            "pagina": 1,
            "limite": 10,
            "total_paginas": 1,
            "itens": [
                {
                    "id": 1,
                    "autor": "Machado de Assis",
                    "titulo": "Dom Casmurro",
                    "resumo": "Um clássico da literatura brasileira.",
                    "data_publicacao": "2025-10-16",
                    "criado_em": "2025-10-16T13:45:00-03:00",
                    "atualizado_em": "2025-10-16T13:45:00-03:00",
                },
                {
                    "id": 2,
                    "autor": "Clarice Lispector",
                    "titulo": "A Hora da Estrela",
                    "resumo": "Uma narrativa introspectiva sobre Macabéa.",
                    "data_publicacao": "2025-10-16",
                    "criado_em": "2025-10-16T14:20:00-03:00",
                    "atualizado_em": "2025-10-16T14:20:00-03:00",
                }
            ]
        }
    }})
