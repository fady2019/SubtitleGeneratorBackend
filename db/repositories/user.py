from db.repositories.repository.crud_repository import CRUDRepository
from db.entities.user import UserEntity
from db.entity_dicts.user_entity_dict import CreateUserEntityDict, UpdateUserEntityDict


class UserRepository(CRUDRepository[UserEntity, CreateUserEntityDict, UpdateUserEntityDict]):
    def _get_entity_type(self):
        return UserEntity
