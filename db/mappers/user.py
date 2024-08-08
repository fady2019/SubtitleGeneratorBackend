from db.mappers.mapper import Mapper
from db.entities.user import UserEntity
from db.dtos.user import UserDTO


class UserMapper(Mapper):
    def to_dto(self, entity: UserEntity | None) -> UserDTO | None:
        if not entity:
            return None

        return UserDTO(
            id=str(entity.id),
            first_name=entity.first_name,
            last_name=entity.last_name,
            username=entity.username,
            email=entity.email,
            password=entity.password,
        )

    def to_entity(self, dto: UserDTO | None) -> UserEntity | None:
        if not dto:
            return None

        return UserEntity(
            first_name=dto["first_name"],
            last_name=dto["last_name"],
            username=dto["username"],
            email=dto["email"],
            password=dto["password"],
        )
