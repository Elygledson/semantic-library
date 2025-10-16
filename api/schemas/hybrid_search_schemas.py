from pydantic import BaseModel, Field


class HybridSearchResultSchema(BaseModel):
    id: int
    title: str = Field(..., alias="titulo")
    summary: str = Field(..., alias="resumo")
    score: float = Field(..., alias="pontuacao")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": 42,
                "titulo": "Aplicações de IA na Educação",
                "resumo": "Este artigo discute como a inteligência artificial pode transformar a forma de ensinar e avaliar alunos.",
                "pontuacao": 0.8947
            }
        }
    }
