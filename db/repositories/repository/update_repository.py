from sqlalchemy import update
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, List

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TFilter, TEntity, MethodOptions, update_options
from db.entity_dicts.entity_dict import UpdateEntityDict


TUpdateEntityDict = TypeVar("UpdateEntityDict", bound=UpdateEntityDict)


class UpdateOptions(MethodOptions):
    pass


def get_default_update_options() -> UpdateOptions:
    return {"session": None}


class UpdateRepository(Repository, Generic[TEntity, TUpdateEntityDict]):
    def update(
        self, filter: TFilter[TEntity], new_data: TUpdateEntityDict, options: UpdateOptions | None = None
    ) -> List[TEntity]:
        options = update_options(options, get_default_update_options)

        def callback(session: Session):
            # get the entity type
            Entity = self._get_entity_type()
            # update entities
            query = update(Entity).where(filter(Entity)).values(**new_data).returning(Entity)
            # save entities
            result = session.execute(query)
            # return updated entities
            return [row.tuple()[0] for row in result.fetchall()]

        return self.start_transaction(callback=callback, default_session=options["session"])
