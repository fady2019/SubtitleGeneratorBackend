from db.repositories.repository.create_repository import CreateRepository
from db.repositories.repository.update_repository import UpdateRepository
from db.repositories.repository.find_repository import FindRepository
from db.entities.user import UserEntity
from db.dtos.user import UserDTO, UpdateUserDTO
from db.mappers.user import UserMapper
from exceptions.response_error import ResponseError


class UserRepository(
    CreateRepository[UserEntity, UserDTO],
    UpdateRepository[UserEntity, UserDTO, UpdateUserDTO],
    FindRepository[UserEntity, UserDTO],
):
    def __init__(self):
        self.mapper = UserMapper()

    # CERATE
    def _execute_create(self, data, options):
        user_entity = self.mapper.to_entity(data)
        options["session"].add(user_entity)
        return user_entity

    def _after_executing_create(self, entity):
        return self.mapper.to_dto(entity)

    #
    #

    # FIND FIRST
    def _execute_find_first(self, filter, options):
        return options["session"].query(UserEntity).filter(filter(UserEntity)).first()

    def _after_executing_find_first(self, entity):
        return self.mapper.to_dto(entity)

    #
    #

    # FIND FIRST WITH ERROR
    def _execute_find_first_with_error(self, filter, options):
        user_entity = options["session"].query(UserEntity).filter(filter(UserEntity)).first()

        if not user_entity:
            raise ResponseError(options["error_msg"] or "user not found", status_code=404)

        return user_entity

    def _after_executing_find_first_with_error(self, entity):
        return self.mapper.to_dto(entity)

    #
    #

    # UPDATE
    def _execute_update(self, filter, new_data, options):
        options["session"].query(UserEntity).filter(filter(UserEntity)).update(new_data)
        return None

    def _after_executing_update(self, entity):
        return self.mapper.to_dto(entity)
