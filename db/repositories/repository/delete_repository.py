from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TFilter, TEntity, MethodOptions, set_default_method_options


class DeleteRepository(Repository, Generic[TEntity]):
    @abstractmethod
    def _execute_delete(self, filter: TFilter[TEntity], options: MethodOptions) -> TEntity | None:
        pass

    def delete(self, filter: TFilter[TEntity], options: MethodOptions | None = None):
        options = set_default_method_options(options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_delete(filter, options)

        return self.start_transaction(callback=callback, default_session=options["session"])
