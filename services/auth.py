from flask import render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
import os, secrets, datetime

from db.repositories.user import UserRepository
from db.repositories.temporary_token import TemporaryTokenRepository
from db.entities.temporary_token import TemporaryTokenType
from exceptions.response_error import ResponseError
from helpers.email import send_email
from helpers.date import add_to_datetime


RP_LINK_HOST = os.getenv("RESET_PASSWORD_LINK_HOST")
RP_TOKEN_LENGTH = int(os.getenv("RESET_PASSWORD_TOKEN_LENGTH", "32"))
RP_EXP_IN_HOURS = int(os.getenv("RESET_PASSWORD_TOKEN_EXP_IN_HOURS", "1"))


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.temp_token_repo = TemporaryTokenRepository()

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

    def request_password_reset(self, email: str):
        # get user data
        user = self.user_repo.find_first_with_error(
            self.user_repo.email_filter(email), {"error_msg": "there's no user with the entered email"}
        )

        def create_new_token_and_delete_old_tokens(session: Session):
            # delete old (password_reset) token(s) for that user
            self.temp_token_repo.delete(
                self.temp_token_repo.and_filter(
                    self.temp_token_repo.user_id_filter(user["id"]),
                    self.temp_token_repo.type_filter(TemporaryTokenType.PASSWORD_RESET),
                ),
                {"session": session},
            )

            # create the new token
            return self.temp_token_repo.create(
                {
                    "token": secrets.token_urlsafe(RP_TOKEN_LENGTH),
                    "expiration_date": add_to_datetime(hours=RP_EXP_IN_HOURS),
                    "user_id": user["id"],
                    "type": TemporaryTokenType.PASSWORD_RESET,
                },
                {"session": session},
            )

        temp_token = self.temp_token_repo.start_transaction(create_new_token_and_delete_old_tokens)

        email_template = render_template(
            "emails/reset_password.html",
            **{
                "user_name": f'{user["first_name"]} {user["last_name"]}',
                "reset_link": f'{RP_LINK_HOST or request.host_url}reset-password/{temp_token["token"]}',
                "link_expiration_date": temp_token["expiration_date"],
            },
        )

        send_email("Password Reset", [user["email"]], html=email_template)

    def reset_password(self, data: dict):
        new_password, token = data["new_password"], data["token"]

        temp_token = self.temp_token_repo.find_first_with_error(
            self.temp_token_repo.and_filter(
                self.temp_token_repo.token_filter(token),
                self.temp_token_repo.expiration_date_gt_filter(datetime.datetime.now()),
            ),
            {"error_msg": "invalid token"},
        )

        user_id = temp_token["user_id"]

        def reset_password_and_delete_token(session: Session):
            self.user_repo.update(
                self.user_repo.id_filter(user_id),
                {"password": generate_password_hash(new_password)},
                {"session": session},
            )

            self.temp_token_repo.delete(
                self.temp_token_repo.token_filter(temp_token["token"]),
                {"session": session},
            )

        self.user_repo.start_transaction(reset_password_and_delete_token)
