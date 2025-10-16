from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserProfileSchema(BaseModel):
    id: int
    name: str = Field(..., alias="nome")
    email: EmailStr
    created_at: datetime = Field(..., alias="criado_em")
    updated_at: datetime = Field(..., alias="atualizado_em")
    deleted_at: Optional[datetime] = Field(None, alias="deletado_em")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "nome": "Joao Silva",
                "email": "joao.silva@example.com",
                "criado_em": "2025-10-16T13:45:00-03:00",
                "atualizado_em": "2025-10-16T13:45:00-03:00",
                "deletado_em": None
            }
        }
    }
