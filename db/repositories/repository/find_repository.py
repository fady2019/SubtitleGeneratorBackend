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


class CountOptions(MethodOptions):
    pass


class FindWithPaginationOptions(MethodOptions):
    page: int | str | None
    items_per_page: int | str | None


def get_default_find_options() -> FindOptions:
    return {"session": None, "throw_if_not_found": False, "error_msg": None, "return_first": False}


def get_default_count_options() -> CountOptions:
    return {"session": None}


def get_default_find_with_pagination_options() -> FindWithPaginationOptions:
    return {"session": None, "page": 1, "items_per_page": 20}


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

    def count(self, filter: TFilter[TEntity], options: CountOptions | None = None) -> int:
        options = update_options(options, get_default_count_options)

        def callback(session: Session):
            # get the entity type
            Entity = self._get_entity_type()
            # count entities
            return session.query(Entity).filter(filter(Entity)).count()

        return self.start_transaction(callback=callback, default_session=options["session"])

    def find_with_pagination(
        self,
        filter: TFilter[TEntity],
        order_by: TOrderBy[TEntity] | None = None,
        options: FindWithPaginationOptions | None = None,
    ) -> tuple[List[TEntity], int, bool]:
        options = update_options(options, get_default_find_with_pagination_options)

        if not order_by:
            order_by = lambda *args: None

        def callback(session: Session):
            # get the entity type
            Entity = self._get_entity_type()
            # fetch entities
            page = int(options["page"])
            items_per_page = int(options["items_per_page"])
            entities = (
                session.query(Entity)
                .filter(filter(Entity))
                .order_by(order_by(Entity))
                .limit(items_per_page)
                .offset((page - 1) * items_per_page)
                .all()
            )
            # count all entities
            count = self.count(filter)
            # check if there next page
            has_next = count > (page * items_per_page)

            return entities, count, has_next

        return self.start_transaction(callback=callback, default_session=options["session"])
