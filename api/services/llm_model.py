from abc import ABC, abstractmethod
from schemas import ChatOutputSchema


class LLMModel(ABC):
    @abstractmethod
    def generate_response(self, query: str, session_id: str) -> ChatOutputSchema:
        pass
