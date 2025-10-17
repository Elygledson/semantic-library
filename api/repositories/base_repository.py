from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar, Optional

TModel = TypeVar("TModel")
TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")
TID = TypeVar("TID")
T = TypeVar("T")


@dataclass
class PaginatedResult(Generic[T]):
    total: int
    page: int
    limit: int
    items: List[T]
    total_pages: int


class CRUDRepository(ABC, Generic[TModel, TCreate, TUpdate, TID]):
    @abstractmethod
    def create(self, obj_in: TCreate) -> TModel:
        pass

    @abstractmethod
    def find_one(self, id: TID) -> Optional[TModel]:
        pass

    @abstractmethod
    def find_all(self,
                 filters: Optional[dict] = None,
                 relations: Optional[List[str]] = None
                 ) -> List[TModel]:
        pass

    @abstractmethod
    def find_all_paginated(
        self,
        page: int = 1,
        limit: int = 10,
        filters: Optional[dict] = None
    ) -> PaginatedResult[TModel]:
        pass

    @abstractmethod
    def update(self, id: TID, obj_in: TUpdate) -> TModel:
        pass

    @abstractmethod
    def delete(self, id: TID) -> None:
        pass
