from werkzeug.security import generate_password_hash

from .user import UserService


class AuthService:
    @staticmethod
    def signup(data: dict):
        data["password"] = generate_password_hash(data["password"])
        return UserService.create_user(data)
