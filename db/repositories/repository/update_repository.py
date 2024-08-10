from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import (
    TFilter,
    TEntity,
    TUpdateDto,
    TDto,
    MethodOptions,
    set_default_method_options,
)


class UpdateRepository(Repository, Generic[TEntity, TDto, TUpdateDto]):
    # UPDATE
    @abstractmethod
    def _execute_update(self, filter: TFilter, new_data: TUpdateDto, options: MethodOptions) -> TEntity | None:
        pass

    @abstractmethod
    def _after_executing_update(self, entity: TEntity | None) -> TDto | None:
        pass

    def update(self, filter: TFilter, new_data: TUpdateDto, options: MethodOptions | None = None):
        options = set_default_method_options(options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_update(filter, new_data, options)

        entity = self.start_transaction(callback=callback, default_session=options["session"])

        return self._after_executing_update(entity)
