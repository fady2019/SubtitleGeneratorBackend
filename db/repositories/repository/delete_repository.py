from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TFilter, TEntity, MethodOptions, update_options


class DeleteOptions(MethodOptions):
    pass


def get_default_delete_options() -> DeleteOptions:
    return {"session": None}


class DeleteRepository(Repository, Generic[TEntity]):
    @abstractmethod
    def _execute_delete(self, filter: TFilter[TEntity], options: DeleteOptions) -> None:
        pass

    def delete(self, filter: TFilter[TEntity], options: DeleteOptions | None = None):
        options = update_options(options, get_default_delete_options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_delete(filter, options)

        return self.start_transaction(callback=callback, default_session=options["session"])
