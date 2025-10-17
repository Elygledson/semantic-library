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
            "pergunta": "Sobre o que o livro Alquimista fala?",
        }
    })


class ChatOutputSchema(BaseModel):
    response: str = Field(..., alias="resposta")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "resposta": "O livro \"O Alquimista\" conta a história de Santiago, um jovem pastor que embarca em uma jornada para encontrar um tesouro pessoal. Ele atravessa desertos e enfrenta diversos desafios ao longo de sua busca. A narrativa mistura elementos de aventura e filosofia, explorando temas como sonhos, destino, autoconhecimento e a realização do potencial humano. É uma obra que incentiva a reflexão sobre seguir os próprios sonhos e compreender o significado da vida."
            }
        }
    )
