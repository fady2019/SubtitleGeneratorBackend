from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import (
    TFilter,
    TEntity,
    MethodOptions,
    FindWithErrorOptions,
    set_default_method_options,
    set_default_find_with_error_options,
)


class FindRepository(Repository, Generic[TEntity]):
    # FIND FIRST
    @abstractmethod
    def _execute_find_first(self, filter: TFilter[TEntity], options: MethodOptions) -> TEntity | None:
        pass

    def find_first(self, filter: TFilter[TEntity], options: MethodOptions | None = None):
        options = set_default_method_options(options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_find_first(filter, options)

        return self.start_transaction(callback=callback, default_session=options["session"])

    #
    #

    # FIND FIRST WITH ERROR
    @abstractmethod
    def _execute_find_first_with_error(self, filter: TFilter[TEntity], options: FindWithErrorOptions) -> TEntity:
        pass

    def find_first_with_error(self, filter: TFilter[TEntity], options: FindWithErrorOptions | None = None):
        options = set_default_find_with_error_options(options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_find_first_with_error(filter, options)

        return self.start_transaction(callback=callback, default_session=options["session"])
