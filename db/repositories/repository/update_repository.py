from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic, TypeVar, List

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TFilter, TEntity, MethodOptions, update_options
from db.entity_dicts.entity_dict import UpdateEntityDict


TUpdateEntityDict = TypeVar("UpdateEntityDict", bound=UpdateEntityDict)


class UpdateOptions(MethodOptions):
    return_updated: bool | None


def get_default_update_options() -> UpdateOptions:
    return {"session": None, "return_updated": False}


class UpdateRepository(Repository, Generic[TEntity, TUpdateEntityDict]):
    # UPDATE
    @abstractmethod
    def _execute_update(
        self, filter: TFilter[TEntity], new_data: TUpdateEntityDict, options: UpdateOptions
    ) -> List[TEntity] | None:
        pass

    def update(self, filter: TFilter[TEntity], new_data: TUpdateEntityDict, options: UpdateOptions | None = None):
        options = update_options(options, get_default_update_options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_update(filter, new_data, options)

        return self.start_transaction(callback=callback, default_session=options["session"])
