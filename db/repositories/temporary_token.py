from db.repositories.repository.create_repository import CreateRepository
from db.repositories.repository.delete_repository import DeleteRepository
from db.repositories.repository.find_repository import FindRepository
from db.entities.temporary_token import TemporaryTokenEntity
from db.dtos.temporary_token import TemporaryTokenDTO
from db.mappers.temporary_token import TemporaryTokenMapper
from exceptions.response_error import ResponseError


class TemporaryTokenRepository(
    CreateRepository[TemporaryTokenEntity, TemporaryTokenDTO],
    DeleteRepository[TemporaryTokenEntity, TemporaryTokenDTO],
    FindRepository[TemporaryTokenEntity, TemporaryTokenDTO],
):
    def __init__(self):
        self.mapper = TemporaryTokenMapper()

    # CERATE
    def _execute_create(self, data, options):
        temp_token_entity = self.mapper.to_entity(data)
        options["session"].add(temp_token_entity)
        return temp_token_entity

    def _after_executing_create(self, entity):
        return self.mapper.to_dto(entity)

    #
    #

    # DELETE
    def _execute_delete(self, filter, options):
        options["session"].query(TemporaryTokenEntity).filter(filter(TemporaryTokenEntity)).delete()
        return None

    def _after_executing_delete(self, entity):
        return self.mapper.to_dto(entity)

    #
    #

    # FIND
    def _execute_find_first(self, filter, options):
        return options["session"].query(TemporaryTokenEntity).filter(filter(TemporaryTokenEntity)).first()

    def _after_executing_find_first(self, entity):
        return self.mapper.to_dto(entity)

    #
    #

    # FIND WITH ERROR
    def _execute_find_first_with_error(self, filter, options):
        temp_token_entity = options["session"].query(TemporaryTokenEntity).filter(filter(TemporaryTokenEntity)).first()

        if not temp_token_entity:
            raise ResponseError(options["error_msg"] or "token not found", status_code=404)

        return temp_token_entity

    def _after_executing_find_first_with_error(self, entity):
        return self.mapper.to_dto(entity)
