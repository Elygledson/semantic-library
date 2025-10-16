from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class BookCreateSchema(BaseModel):
    author: str = Field(..., alias="autor")
    title: str = Field(..., alias="titulo")
    summary: str = Field(..., alias="resumo")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "autor": "Machado de Assis",
                "titulo": "Dom Casmurro",
                "resumo": "Um clássico da literatura brasileira que explora ciúmes, dúvida e traição."
            }
        }
    }


class BookUpdateSchema(BaseModel):
    author: str = Field(..., alias="autor")
    title: str = Field(..., alias="titulo")
    summary: str = Field(..., alias="resumo")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "autor": "Machado de Assis",
                "titulo": "Dom Casmurro - Edição Revisada",
                "resumo": "Versão revisada do clássico sobre ciúmes e ambiguidade de sentimentos."
            }
        }
    }


class BookSchema(BaseModel):
    id: int
    author: str = Field(..., alias="autor")
    title: str = Field(..., alias="titulo")
    summary: str = Field(..., alias="resumo")
    created_at: datetime = Field(..., alias="criado_em")
    updated_at: datetime = Field(..., alias="atualizado_em")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "autor": "Clarice Lispector",
                "titulo": "A Hora da Estrela",
                "resumo": "Uma narrativa introspectiva sobre a vida e a alienação de Macabéa.",
                "criado_em": "2025-10-16T14:20:00-03:00",
                "atualizado_em": "2025-10-16T14:20:00-03:00",
            }
        }
    }


class PaginatedBooksSchema(BaseModel):
    total: int
    pagina: int
    limite: int
    itens: List[BookSchema]
    total_paginas: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
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
                        "criado_em": "2025-10-16T13:45:00-03:00",
                        "atualizado_em": "2025-10-16T13:45:00-03:00",
                    },
                    {
                        "id": 2,
                        "autor": "Clarice Lispector",
                        "titulo": "A Hora da Estrela",
                        "resumo": "Uma narrativa introspectiva sobre Macabéa.",
                        "criado_em": "2025-10-16T14:20:00-03:00",
                        "atualizado_em": "2025-10-16T14:20:00-03:00",
                    }
                ]
            }
        }
    }
