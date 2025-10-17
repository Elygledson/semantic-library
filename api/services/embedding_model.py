from typing import List
from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    @abstractmethod
    def generate_query_embedding(self, contents: str) -> List[float]:
        pass

    @abstractmethod
    def generate_document_embedding(self, contents: List[str]) -> List[List[float]]:
        pass
