from abc import ABC, abstractmethod
from sqlalchemy import BinaryExpression, ColumnElement, or_
from typing import Callable

from db.dtos.dto import DTO

TFilter = Callable[..., Callable[[], BinaryExpression[bool] | ColumnElement[bool]]]


class Repository(ABC):
    @abstractmethod
    def create(self, data: DTO) -> DTO:
        pass

    @abstractmethod
    def find_first(self, filter: TFilter) -> DTO | None:
        pass

    @abstractmethod
    def find_first_with_error(self, filter: TFilter) -> DTO:
        pass

    @abstractmethod
    def update(self, filter: TFilter, new_data: DTO) -> DTO | None:
        pass

    def or_filter(self, *filters: tuple[TFilter]):
        return lambda: or_(*[filter() for filter in filters])
