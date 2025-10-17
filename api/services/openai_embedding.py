from typing import List
from config import settings
from services import EmbeddingModel
from langchain_openai import OpenAIEmbeddings


class OpenAIEmbeddingService(EmbeddingModel):
    def __init__(self, model: str = "text-embedding-3-small"):
        """
        Inicializa o serviço de embeddings com o modelo especificado.

        Args:
            model (str, optional): Nome do modelo de embeddings da OpenAI.
                                   Padrão é "text-embedding-3-small".
        """
        self.embedding_model = OpenAIEmbeddings(
            model=model, api_key=settings.AI_SERVICE_KEY)

    def generate_query_embedding(self, contents: str) -> List[float]:
        """
        Gera o embedding para uma string de consulta (query).

        Args:
            contents (str): Texto da consulta a ser convertido em embedding.

        Returns:
            List[float]: Vetor de embedding da consulta.
        """
        return self.embedding_model.embed_query(contents)

    def generate_document_embedding(self, contents: List[str]) -> List[List[float]]:
        """
        Gera embeddings para um ou mais documentos.

        Args:
            contents (List[str]): Documento(s) a serem convertidos em embeddings.

        Returns:
            List[List[float]]: - Lista de vetores de embedding se `contents` for uma lista de documentos.
        """
        return self.embedding_model.embed_documents(contents)
