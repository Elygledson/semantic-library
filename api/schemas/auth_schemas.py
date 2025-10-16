from pydantic import BaseModel, Field
from schemas import UserProfileSchema


class AuthSchema(BaseModel):
    email: str
    password: str = Field(..., alias="senha")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "email": "joao.silva@example.com",
                "senha": "minha_senha"
            }
        }
    }


class LoginResponseSchema(BaseModel):
    usuario: UserProfileSchema
    token: str
    tipo_token: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "usuario": {
                    "id": 1,
                    "nome": "Joao Silva",
                    "email": "joao.silva@example.com",
                    "criado_em": "2025-10-16T13:45:00-03:00",
                    "atualizado_em": "2025-10-16T13:45:00-03:00",
                    "deletado_em": None
                },
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "tipo_token": "Bearer"
            }
        }
    }
