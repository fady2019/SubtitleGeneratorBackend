from db.repositories.repository.create_repository import CreateRepository
from db.repositories.repository.delete_repository import DeleteRepository
from db.repositories.repository.find_repository import FindRepository
from db.entities.temporary_token import TemporaryTokenEntity
from db.entity_dicts.temporary_token_entity_dict import CreateTemporaryTokenEntityDict


class TemporaryTokenRepository(
    CreateRepository[TemporaryTokenEntity, CreateTemporaryTokenEntityDict],
    DeleteRepository[TemporaryTokenEntity],
    FindRepository[TemporaryTokenEntity],
):
    def _get_entity_type(self):
        return TemporaryTokenEntity
