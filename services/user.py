from .shared import TFilter, Service
from db.user import User
from db.db_config import create_session


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
    def find_first_by(filter: TFilter):
        session = create_session()()

        user = None

        with session:
            user = session.query(User).filter(filter()).first()

        return user

    @staticmethod
    def email_filter(email: str):
        return lambda: User.email.ilike(email)

    @staticmethod
    def username_filter(username: str):
        return lambda: User.username.ilike(username)
