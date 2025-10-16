from typing import List
from config import settings
from services import EmbeddingModel
from langchain_openai import OpenAIEmbeddings


class OpenAIEmbeddingService(EmbeddingModel):
    def __init__(self, model="text-embedding-3-small"):
        self.embedding_model = OpenAIEmbeddings(
            model=model, api_key=settings.AI_SERVICE_KEY)

    def generate_query_embedding(self, contents: str) -> List[float]:
        return self.embedding_model.embed_query(contents)

    def generate_document_embedding(self, contents: str) -> List[float]:
        return self.embedding_model.embed_documents(contents)
