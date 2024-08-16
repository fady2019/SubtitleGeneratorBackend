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
        user_entities = []

        for user_data in data:
            user_entity = UserEntity(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
            )

            user_entities.append(user_entity)

        options["session"].add_all(user_entities)

        return user_entities

    #
    #

    # FIND
    def _execute_find(self, filter, options):
        user_entities = options["session"].query(UserEntity).filter(filter(UserEntity)).all()

        if not user_entities and options["throw_if_not_found"]:
            raise ResponseError(options["error_msg"] or {"msg": "user(s) not found", "status_code": 404})

        return user_entities

    #
    #

    # UPDATE
    def _execute_update(self, filter, new_data, options):
        options["session"].query(UserEntity).filter(filter(UserEntity)).update(new_data)

        if not options["return_updated"]:
            return None

        return options["session"].query(UserEntity).filter(filter(UserEntity)).all()
