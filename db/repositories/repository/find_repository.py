from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic, List

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TFilter, TEntity, TOrderBy, MethodOptions, update_options
from response.response_messages import ResponseMessageBase, ResponseMsgInfo


class FindOptions(MethodOptions):
    throw_if_not_found: bool | None
    error_msg: ResponseMessageBase | ResponseMsgInfo | None
    return_first: bool | None


def get_default_find_options() -> FindOptions:
    return {"session": None, "throw_if_not_found": False, "error_msg": None, "return_first": False}


class FindRepository(Repository, Generic[TEntity]):
    # FIND FIRST
    @abstractmethod
    def _execute_find(
        self, filter: TFilter[TEntity], order_by: TOrderBy[TEntity] | None, options: FindOptions
    ) -> List[TEntity]:
        pass

    def find(
        self,
        filter: TFilter[TEntity],
        order_by: TOrderBy[TEntity] | None = None,
        options: FindOptions | None = None,
    ):
        options = update_options(options, get_default_find_options)

        if not order_by:
            order_by = lambda *args: None

        def callback(session: Session):
            options["session"] = session
            return self._execute_find(filter, order_by, options)

        entities = self.start_transaction(callback=callback, default_session=options["session"])

        if options["return_first"]:
            return entities[0] if entities else None

        return entities
