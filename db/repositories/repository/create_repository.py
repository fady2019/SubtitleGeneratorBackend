from sqlalchemy.orm import Session
from abc import abstractmethod
from typing import Generic

from db.repositories.repository.repository import Repository
from db.repositories.repository.repository_typing import TEntity, TDto, MethodOptions, set_default_method_options


class CreateRepository(Repository, Generic[TEntity, TDto]):
    # CREATE
    @abstractmethod
    def _execute_create(self, data: TDto, options: MethodOptions) -> TEntity:
        pass

    @abstractmethod
    def _after_executing_create(self, entity: TEntity) -> TDto:
        pass

    def create(self, data: TDto, options: MethodOptions | None = None):
        options = set_default_method_options(options)

        def callback(session: Session):
            options["session"] = session
            return self._execute_create(data, options)

        entity = self.start_transaction(callback=callback, default_session=options["session"])

        return self._after_executing_create(entity)
