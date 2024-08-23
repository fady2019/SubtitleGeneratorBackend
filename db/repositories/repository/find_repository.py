from sqlalchemy.orm import Session
from typing import Generic, List

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TFilter, TEntity, TOrderBy, MethodOptions, update_options
from response.response import ResponseError
from response.response_messages import ResponseMessageBase, ResponseMsgInfo


class FindOptions(MethodOptions):
    throw_if_not_found: bool | None
    error_msg: ResponseMessageBase | ResponseMsgInfo | None
    return_first: bool | None


def get_default_find_options() -> FindOptions:
    return {"session": None, "throw_if_not_found": False, "error_msg": None, "return_first": False}


class FindRepository(Repository, Generic[TEntity]):
    def find(
        self,
        filter: TFilter[TEntity],
        order_by: TOrderBy[TEntity] | None = None,
        options: FindOptions | None = None,
    ) -> List[TEntity] | TEntity | None:
        options = update_options(options, get_default_find_options)

        if not order_by:
            order_by = lambda *args: None

        def callback(session: Session):
            # get the entity type
            Entity = self._get_entity_type()
            # fetch entities
            entities = session.query(Entity).filter(filter(Entity)).order_by(order_by(Entity)).all()

            if not entities and options["throw_if_not_found"]:
                default_msg = f'no record(s) found in "{Entity.__tablename__}" table'
                raise ResponseError(options["error_msg"] or {"msg": default_msg, "status_code": 404})

            # return entities
            return entities

        entities = self.start_transaction(callback=callback, default_session=options["session"])

        if options["return_first"]:
            return entities[0] if entities else None

        return entities
