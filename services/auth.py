from werkzeug.security import generate_password_hash, check_password_hash

from db.repositories.user import UserRepository
from exceptions.response_error import ResponseError


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def signup(self, data: dict):
        data["password"] = generate_password_hash(data["password"])
        user = self.user_repo.create(data)
        del user["password"]
        return user

    def login(self, data: dict):
        username_or_email, password = data["username_or_email"], data["password"]

        user = self.user_repo.find_first(
            self.user_repo.or_filter(
                self.user_repo.email_filter(username_or_email), self.user_repo.username_filter(username_or_email)
            )
        )

        valid_credentials = user != None and check_password_hash(user["password"], password)

        if not valid_credentials:
            raise ResponseError("invalid credentials, please try again with the valid ones", status_code=401)

        del user["password"]

        return user

    def change_password(self, user_id: str, data: dict):
        if not user_id:
            return

        current_password, new_password = data["current_password"], data["new_password"]

        user = self.user_repo.find_first_with_error(self.user_repo.id_filter(user_id))

        correct_password = check_password_hash(user["password"], current_password)

        if not correct_password:
            raise ResponseError("the current password is wrong", status_code=401)

        self.user_repo.update(self.user_repo.id_filter(user_id), {"password": generate_password_hash(new_password)})
