from services.shared import TFilter, Service
from db.user import User
from db.db_config import create_session
from exceptions.response_error import ResponseError


class UserService(Service):
    @staticmethod
    def create_user(data: dict):
        session = create_session()()

        user = None

        with session:
            user_row = User(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                username=data.get("username"),
                email=data.get("email"),
                password=data.get("password"),
            )

            session.add(user_row)
            session.commit()

            user = user_row.to_dict(include_email=True)

        return user

    @staticmethod
    def find_first_by(filter: TFilter, throw_error_if_not_found=False):
        session = create_session()()

        user = None

        with session:
            user = session.query(User).filter(filter()).first()

        if throw_error_if_not_found and not user:
            raise ResponseError("user not found", status_code=404)

        return user

    @staticmethod
    def update_user(filter: TFilter, data: dict):
        session = create_session()()

        with session:
            session.query(User).filter(filter()).update(data)
            session.commit()

    @staticmethod
    def email_filter(email: str):
        return lambda: User.email.ilike(email)

    @staticmethod
    def username_filter(username: str):
        return lambda: User.username.ilike(username)

    @staticmethod
    def id_filter(id: str):
        return lambda: User.id == id
