from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    @abstractmethod
    def generate_query_embedding(self):
        pass

    @abstractmethod
    def generate_document_embedding(self):
        pass
