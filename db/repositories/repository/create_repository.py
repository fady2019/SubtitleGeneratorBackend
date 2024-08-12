from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic, TypeVar

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TEntity, MethodOptions, set_default_method_options
from db.entity_dicts.entity_dict import CreateEntityDict


TCreateEntityDict = TypeVar("CreateEntityDict", bound=CreateEntityDict)


class CreateRepository(Repository, Generic[TEntity, TCreateEntityDict]):
    # CREATE
    @abstractmethod
    def _execute_create(self, data: TCreateEntityDict, options: MethodOptions) -> TEntity:
        pass

    def create(self, data: TCreateEntityDict, options: MethodOptions | None = None):
        options = set_default_method_options(options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_create(data, options)

        return self.start_transaction(callback=callback, default_session=options["session"])
