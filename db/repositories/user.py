from db.repositories.repository.create_repository import CreateRepository
from db.repositories.repository.update_repository import UpdateRepository
from db.repositories.repository.find_repository import FindRepository
from db.entities.user import UserEntity
from db.entity_dicts.user_entity_dict import CreateUserEntityDict, UpdateUserEntityDict
from response.response import ResponseError


class UserRepository(
    CreateRepository[UserEntity, CreateUserEntityDict],
    UpdateRepository[UserEntity, UpdateUserEntityDict],
    FindRepository[UserEntity],
):
    # CERATE
    def _execute_create(self, data, options):
        user_entity = UserEntity(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            email=data["email"],
            password=data["password"],
        )

        options["session"].add(user_entity)

        return user_entity

    #
    #

    # FIND FIRST
    def _execute_find_first(self, filter, options):
        return options["session"].query(UserEntity).filter(filter(UserEntity)).first()

    #
    #

    # FIND FIRST WITH ERROR
    def _execute_find_first_with_error(self, filter, options):
        user_entity = options["session"].query(UserEntity).filter(filter(UserEntity)).first()

        if not user_entity:
            raise ResponseError(options["error_msg"] or {"msg": "user not found", "status_code": 404})

        return user_entity

    #
    #

    # UPDATE
    def _execute_update(self, filter, new_data, options):
        options["session"].query(UserEntity).filter(filter(UserEntity)).update(new_data)
        return None
