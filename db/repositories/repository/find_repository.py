from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import (
    TFilter,
    TEntity,
    TDto,
    MethodOptions,
    FindWithErrorOptions,
    set_default_method_options,
    set_default_find_with_error_options,
)


class FindRepository(Repository, Generic[TEntity, TDto]):
    # FIND FIRST
    @abstractmethod
    def _execute_find_first(self, filter: TFilter, options: MethodOptions) -> TEntity | None:
        pass

    @abstractmethod
    def _after_executing_find_first(self, entity: TEntity | None) -> TDto | None:
        pass

    def find_first(self, filter: TFilter, options: MethodOptions | None = None):
        options = set_default_method_options(options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_find_first(filter, options)

        entity = self.start_transaction(callback=callback, default_session=options["session"])

        return self._after_executing_find_first(entity)

    #
    #

    # FIND FIRST WITH ERROR
    @abstractmethod
    def _execute_find_first_with_error(self, filter: TFilter, options: FindWithErrorOptions) -> TEntity:
        pass

    @abstractmethod
    def _after_executing_find_first_with_error(self, entity: TEntity) -> TDto:
        pass

    def find_first_with_error(self, filter: TFilter, options: FindWithErrorOptions | None = None):
        options = set_default_find_with_error_options(options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_find_first_with_error(filter, options)

        entity = self.start_transaction(callback=callback, default_session=options["session"])

        return self._after_executing_find_first_with_error(entity)
