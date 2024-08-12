from dtos_mappers.mapper import Mapper
from db.entities.user import UserEntity
from dtos.user import UserDTO


class UserMapper(Mapper):
    def to_dto(self, entity: UserEntity | None) -> UserDTO | None:
        if not entity:
            return None

        return {
            "id": str(entity.id),
            "first_name": entity.first_name,
            "last_name": entity.last_name,
            "username": entity.username,
            "email": entity.email,
        }
