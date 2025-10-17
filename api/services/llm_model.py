from typing import Optional, List
from abc import ABC, abstractmethod
from schemas import ChatOutputSchema, HybridSearchResultSchema


class LLMModel(ABC):
    @abstractmethod
    def generate_response(self, query_text: str, session_id: str, documents: Optional[List[HybridSearchResultSchema]] = None) -> ChatOutputSchema:
        pass
