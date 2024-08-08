from sqlalchemy.ext.declarative import DeclarativeMeta
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

from db.dtos.dto import DTO

TEntity = TypeVar("Entity", bound=DeclarativeMeta)
TDto = TypeVar("Dto", bound=DTO)


class Mapper(ABC, Generic[TEntity]):
    @abstractmethod
    def to_dto(self, entity: TEntity | None) -> TDto | None:
        pass

    def to_dtos(self, entities: List[TEntity]) -> List[TDto]:
        return [self.to_dto(entity) for entity in entities]

    @abstractmethod
    def to_entity(self, dto: TDto | None) -> TEntity | None:
        pass

    def to_entities(self, dtos: List[TDto]) -> List[TEntity]:
        return [self.to_entity(dto) for dto in dtos]
