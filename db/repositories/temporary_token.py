from db.repositories.repository.create_repository import CreateRepository
from db.repositories.repository.delete_repository import DeleteRepository
from db.repositories.repository.find_repository import FindRepository
from db.entities.temporary_token import TemporaryTokenEntity
from db.entity_dicts.temporary_token_entity_dict import CreateTemporaryTokenEntityDict
from exceptions.response_error import ResponseError


class TemporaryTokenRepository(
    CreateRepository[TemporaryTokenEntity, CreateTemporaryTokenEntityDict],
    DeleteRepository[TemporaryTokenEntity],
    FindRepository[TemporaryTokenEntity],
):
    # CERATE
    def _execute_create(self, data, options):
        temp_token_entity = TemporaryTokenEntity(
            token=data["token"], expiration_date=data["expiration_date"], type=data["type"], user_id=data["user_id"]
        )

        options["session"].add(temp_token_entity)

        return temp_token_entity

    #
    #

    # DELETE
    def _execute_delete(self, filter, options):
        options["session"].query(TemporaryTokenEntity).filter(filter(TemporaryTokenEntity)).delete()
        return None

    #
    #

    # FIND
    def _execute_find_first(self, filter, options):
        return options["session"].query(TemporaryTokenEntity).filter(filter(TemporaryTokenEntity)).first()

    #
    #

    # FIND WITH ERROR
    def _execute_find_first_with_error(self, filter, options):
        temp_token_entity = options["session"].query(TemporaryTokenEntity).filter(filter(TemporaryTokenEntity)).first()

        if not temp_token_entity:
            raise ResponseError(options["error_msg"] or "token not found", status_code=404)

        return temp_token_entity
