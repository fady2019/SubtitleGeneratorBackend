from typing import Generic

from db.repositories.repository.repository_typing import TEntity
from db.repositories.repository.create_repository import CreateRepository, TCreateEntityDict
from db.repositories.repository.find_repository import FindRepository
from db.repositories.repository.update_repository import UpdateRepository, TUpdateEntityDict
from db.repositories.repository.delete_repository import DeleteRepository


class CRUDRepository(
    Generic[TEntity, TCreateEntityDict, TUpdateEntityDict],
    CreateRepository[TEntity, TCreateEntityDict],
    FindRepository[TEntity],
    UpdateRepository[TEntity, TUpdateEntityDict],
    DeleteRepository[TEntity],
):
    pass
