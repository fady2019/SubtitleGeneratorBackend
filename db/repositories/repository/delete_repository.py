from sqlalchemy.orm import Session
from typing import Generic, List

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TFilter, TEntity, MethodOptions, update_options


class DeleteOptions(MethodOptions):
    pass


def get_default_delete_options() -> DeleteOptions:
    return {"session": None}


class DeleteRepository(Repository, Generic[TEntity]):
    def delete(self, filter: TFilter[TEntity], options: DeleteOptions | None = None) -> List[TEntity]:
        options = update_options(options, get_default_delete_options)

        def callback(session: Session):
            # get the entity type
            Entity = self._get_entity_type()
            # fetch entities
            entities = session.query(Entity).filter(filter(Entity)).all()
            # delete entities
            for entity in entities:
                session.delete(entity)
            # return entities
            return entities

        return self.start_transaction(callback=callback, default_session=options["session"])
