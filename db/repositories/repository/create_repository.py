from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic, TypeVar, List

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TEntity, MethodOptions, update_options
from db.entity_dicts.entity_dict import CreateEntityDict


TCreateEntityDict = TypeVar("CreateEntityDict", bound=CreateEntityDict)


class CreateOptions(MethodOptions):
    pass


def get_default_create_options() -> CreateOptions:
    return {"session": None}


class CreateRepository(Repository, Generic[TEntity, TCreateEntityDict]):
    # CREATE
    @abstractmethod
    def _execute_create(self, data: List[TCreateEntityDict], options: CreateOptions) -> List[TEntity]:
        pass

    def create(self, data: TCreateEntityDict | List[TCreateEntityDict], options: CreateOptions | None = None):
        options = update_options(options, get_default_create_options)

        is_list = isinstance(data, List)

        def callback(session: Session):
            options["session"] = session
            create_data = data if is_list else [data]
            return self._execute_create(create_data, options)

        entities = self.start_transaction(callback=callback, default_session=options["session"])

        return entities if is_list else entities[0]
