from sqlalchemy.orm import Session
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
    def create(
        self, data: TCreateEntityDict | List[TCreateEntityDict], options: CreateOptions | None = None
    ) -> List[TEntity] | TEntity:
        options = update_options(options, get_default_create_options)

        is_list = isinstance(data, List)

        def callback(session: Session):
            # make sure that data is a list
            data_list = data if is_list else [data]
            # get the entity type
            Entity = self._get_entity_type()
            # create entities
            entities = [Entity(**data) for data in data_list]
            # save entities
            session.add_all(entities)
            # return entities
            return entities

        entities = self.start_transaction(callback=callback, default_session=options["session"])

        return entities if is_list else entities[0]
