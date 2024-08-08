from db.db_config import create_session
from db.repositories.repository import Repository, TFilter
from db.entities.user import UserEntity
from db.dtos.user import UserDTO, UpdateUserDTO
from db.mappers.user import UserMapper
from exceptions.response_error import ResponseError


class UserRepository(Repository):
    def __init__(self):
        self.mapper = UserMapper()

    def create(self, data: UserDTO) -> UserDTO:
        session = create_session()()

        user = None

        with session:
            user_entity = self.mapper.to_entity(data)
            session.add(user_entity)
            session.commit()
            user = self.mapper.to_dto(user_entity)

        return user

    def find_first(self, filter: TFilter) -> UserDTO | None:
        session = create_session()()

        user = None

        with session:
            user_entity = session.query(UserEntity).filter(filter()).first()
            user = self.mapper.to_dto(user_entity)

        return user

    def find_first_with_error(self, filter: TFilter) -> UserDTO:
        user = self.find_first(filter)

        if not user:
            raise ResponseError("user not found", status_code=404)

        return user

    def update(self, filter: TFilter, new_data: UpdateUserDTO) -> UserDTO | None:
        session = create_session()()

        with session:
            session.query(UserEntity).filter(filter()).update(new_data)
            session.commit()

    def email_filter(self, email: str):
        return lambda: UserEntity.email.ilike(email)

    def username_filter(self, username: str):
        return lambda: UserEntity.username.ilike(username)

    def id_filter(self, id: str):
        return lambda: UserEntity.id == id
