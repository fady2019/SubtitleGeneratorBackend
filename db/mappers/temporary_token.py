from db.mappers.mapper import Mapper
from db.entities.temporary_token import TemporaryTokenEntity
from db.dtos.temporary_token import TemporaryTokenDTO


class TemporaryTokenMapper(Mapper):
    def to_dto(self, entity: TemporaryTokenEntity | None) -> TemporaryTokenDTO | None:
        if not entity:
            return None

        return TemporaryTokenDTO(
            token=entity.token,
            expiration_date=entity.expiration_date,
            user_id=str(entity.user_id),
            type=entity.type,
        )

    def to_entity(self, dto: TemporaryTokenDTO | None) -> TemporaryTokenEntity | None:
        if not dto:
            return None

        return TemporaryTokenEntity(
            token=dto["token"],
            expiration_date=dto["expiration_date"],
            user_id=dto["user_id"],
            type=dto["type"],
        )
