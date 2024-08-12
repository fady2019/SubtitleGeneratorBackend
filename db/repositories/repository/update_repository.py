from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic, TypeVar

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TFilter, TEntity, MethodOptions, set_default_method_options
from db.entity_dicts.entity_dict import UpdateEntityDict


TUpdateEntityDict = TypeVar("UpdateEntityDict", bound=UpdateEntityDict)


class UpdateRepository(Repository, Generic[TEntity, TUpdateEntityDict]):
    # UPDATE
    @abstractmethod
    def _execute_update(
        self, filter: TFilter[TEntity], new_data: TUpdateEntityDict, options: MethodOptions
    ) -> TEntity | None:
        pass

    def update(self, filter: TFilter[TEntity], new_data: TUpdateEntityDict, options: MethodOptions | None = None):
        options = set_default_method_options(options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_update(filter, new_data, options)

        return self.start_transaction(callback=callback, default_session=options["session"])
