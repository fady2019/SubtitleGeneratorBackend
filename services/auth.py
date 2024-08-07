from werkzeug.security import generate_password_hash, check_password_hash

from services.shared import Service
from services.user import UserService
from exceptions.response_error import ResponseError


class AuthService(Service):
    @staticmethod
    def signup(data: dict):
        data["password"] = generate_password_hash(data["password"])
        return UserService.create_user(data)

    @staticmethod
    def login(data: dict):
        username_or_email = data["username_or_email"]
        password = data["password"]

        user_row = UserService.find_first_by(
            UserService.or_filter(
                UserService.email_filter(username_or_email), UserService.username_filter(username_or_email)
            )
        )

        valid_credentials = user_row != None and check_password_hash(user_row.password, password)

        if not valid_credentials:
            raise ResponseError("invalid credentials, please try again with the valid ones", status_code=401)

        return user_row.to_dict(include_email=True)

    @staticmethod
    def auto_login(user_id: str):
        if not user_id:
            return

        user_row = UserService.find_first_by(UserService.id_filter(user_id))

        return user_row.to_dict(include_email=True) if user_row else None

    @staticmethod
    def change_password(user_id: str, data: dict):
        if not user_id:
            return

        current_password = data["current_password"]
        new_password = data["new_password"]

        user_row = UserService.find_first_by(UserService.id_filter(user_id), throw_error_if_not_found=True)

        correct_password = check_password_hash(user_row.password, current_password)

        if not correct_password:
            raise ResponseError("the current password is wrong", status_code=401)

        UserService.update_user(
            UserService.id_filter(user_id),
            data={"password": generate_password_hash(new_password)},
        )
