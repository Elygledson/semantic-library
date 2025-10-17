from pydantic import BaseModel, ConfigDict, Field


class HybridSearchResultSchema(BaseModel):
    id: int
    title: str = Field(..., alias="titulo")
    summary: str = Field(..., alias="resumo")
    score: float = Field(..., alias="pontuacao")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, json_schema_extra={
        "example": {
            "id": 42,
            "titulo": "Aplicações de IA na Educação",
            "resumo": "Este artigo discute como a inteligência artificial pode transformar a forma de ensinar e avaliar alunos.",
            "pontuacao": 0.8947
        }
    })


class QuerySchema(BaseModel):
    query: str = Field(..., alias="pergunta")
    limit: int = Field(10, alias="limite", ge=1)

    model_config = ConfigDict(populate_by_name=True, json_schema_extra={
        "example": {
            "pergunta": "Como fazer um loop for em Python?",
        }
    })


class ChatOutputSchema(BaseModel):
    response: str = Field(..., alias="resposta")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "resposta": "A inteligência artificial pode transformar a educação ao personalizar o aprendizado e automatizar avaliações."
            }
        }
    )
