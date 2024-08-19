from abc import ABC, abstractmethod
from typing import List, Generic, Optional

from db.repositories.repository.repository_typing import TEntity
from dtos.dto import TDto


class Mapper(ABC, Generic[TEntity, TDto]):
    @abstractmethod
    def to_dto(self, entity: Optional[TEntity]) -> Optional[TDto]:
        pass

    def to_dtos(self, entities: List[TEntity]) -> List[TDto]:
        return [self.to_dto(entity) for entity in entities]
