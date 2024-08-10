from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TFilter, TEntity, TDto, MethodOptions, set_default_method_options


class DeleteRepository(Repository, Generic[TEntity, TDto]):
    @abstractmethod
    def _execute_delete(self, filter: TFilter[TEntity], options: MethodOptions) -> TEntity | None:
        pass

    @abstractmethod
    def _after_executing_delete(self, entity: TEntity | None) -> TDto | None:
        pass

    def delete(self, filter: TFilter[TEntity], options: MethodOptions | None = None):
        options = set_default_method_options(options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_delete(filter, options)

        entity = self.start_transaction(callback=callback, default_session=options["session"])

        return self._after_executing_delete(entity)
