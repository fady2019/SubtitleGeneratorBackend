from db.repositories.repository.create_repository import CreateRepository
from db.repositories.repository.delete_repository import DeleteRepository
from db.repositories.repository.find_repository import FindRepository
from db.entities.temporary_token import TemporaryTokenEntity
from db.entity_dicts.temporary_token_entity_dict import CreateTemporaryTokenEntityDict
from response.response import ResponseError


class TemporaryTokenRepository(
    CreateRepository[TemporaryTokenEntity, CreateTemporaryTokenEntityDict],
    DeleteRepository[TemporaryTokenEntity],
    FindRepository[TemporaryTokenEntity],
):
    # CERATE
    def _execute_create(self, data, options):
        token_entities = []

        for token_data in data:
            token_entity = TemporaryTokenEntity(
                token=token_data["token"],
                expiration_date=token_data["expiration_date"],
                type=token_data["type"],
                user_id=token_data["user_id"],
            )

            token_entities.append(token_entity)

        options["session"].add_all(token_entities)

        return token_entities

    #
    #

    # DELETE
    def _execute_delete(self, filter, options):
        options["session"].query(TemporaryTokenEntity).filter(filter(TemporaryTokenEntity)).delete()

    #
    #

    # FIND
    def _execute_find(self, filter, options):
        token_entities = options["session"].query(TemporaryTokenEntity).filter(filter(TemporaryTokenEntity)).all()

        if not token_entities and options["throw_if_not_found"]:
            raise ResponseError(options["error_msg"] or {"msg": "token not found", "status_code": 404})

        return token_entities
