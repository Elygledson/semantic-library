from schemas import UserProfileSchema
from pydantic import BaseModel, Field, ConfigDict


class AuthSchema(BaseModel):
    email: str
    password: str = Field(..., alias="senha")

    model_config = ConfigDict(populate_by_name=True, json_schema_extra={
        "example": {
            "email": "joao.silva@example.com",
            "senha": "minha_senha"
        }
    })


class LoginResponseSchema(BaseModel):
    user: UserProfileSchema = Field(..., alias='usuario')
    token: str
    type: str = Field(..., alias='tipo')

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, json_schema_extra={
        "example": {
            "usuario": {
                "id": 1,
                "nome": "Joao Silva",
                "email": "joao.silva@example.com",
                "criado_em": "2025-10-16T13:45:00-03:00",
                "atualizado_em": "2025-10-16T13:45:00-03:00",
            },
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "tipo": "Bearer"
        }
    })
