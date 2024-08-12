from abc import ABC, abstractmethod

from db.repositories.repository.repository_typing import TEntity
from dtos.dto import DTO


class Mapper(ABC):
    @abstractmethod
    def to_dto(self, entity: TEntity | None) -> DTO | None:
        pass
