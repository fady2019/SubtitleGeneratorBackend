from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
import os, secrets, datetime

from db.repositories.user import UserRepository
from db.repositories.temporary_token import TemporaryTokenRepository
from db.entities.temporary_token import TemporaryTokenType
from dtos_mappers.user import UserMapper
from celery_tasks.emails import EmailTasks
from helpers.date import add_to_datetime
from response.response import ResponseError
from response.response_messages import ResponseMessage


CLIENT_HOST_URL = os.getenv("CLIENT_HOST_URL")
TEMP_TOKEN_LENGTH = int(os.getenv("RESET_PASSWORD_TOKEN_LENGTH", "32"))
TEMP_TOKEN_EXP_IN_HOURS = float(os.getenv("TEMP_TOKEN_EXP_IN_HOURS", "1"))


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.temp_token_repo = TemporaryTokenRepository()

    #
    #
    #

    def signup(self, data: dict):
        data["password"] = generate_password_hash(data["password"])
        user = self.user_repo.create(data)
        self.request_email_verification(user.id)
        return UserMapper().to_dto(user)

    #
    #

    def login(self, data: dict):
        username_or_email, password = data["username_or_email"], data["password"]

        user = self.user_repo.find(
            filter=lambda User: User.email.ilike(username_or_email) | User.username.ilike(username_or_email),
            options={"return_first": True},
        )

        valid_credentials = user != None and check_password_hash(user.password, password)

        if not valid_credentials:
            raise ResponseError(ResponseMessage.FAILED_INVALID_CREDENTIALS)

        if not user.is_verified:
            raise ResponseError(ResponseMessage.FAILED_EMAIL_NOT_VERIFIED, UserMapper().to_dto(user))

        return UserMapper().to_dto(user)

    #
    #

    def change_password(self, user_id: str, data: dict):
        if not user_id:
            return

        current_password, new_password = data["current_password"], data["new_password"]

        user = self.user_repo.find(
            filter=lambda User: User.id == user_id, options={"throw_if_not_found": True, "return_first": True}
        )

        correct_password = check_password_hash(user.password, current_password)

        if not correct_password:
            raise ResponseError(ResponseMessage.FAILED_WRONG_CURRENT_PASSWORD)

        self.user_repo.update(
            filter=lambda User: User.id == user_id,
            new_data={"password": generate_password_hash(new_password)},
        )

    #
    #

    def request_password_reset(self, email: str):
        # get user data
        user = self.user_repo.find(
            filter=lambda User: User.email.ilike(email),
            options={
                "throw_if_not_found": True,
                "error_msg": ResponseMessage.FAILED_USER_NOT_FOUND_WITH_EMAIL,
                "return_first": True,
            },
        )

        temp_token = self.__create_temp_token(user.id, TemporaryTokenType.PASSWORD_RESET)

        email_template = render_template(
            "emails/reset_password.html",
            **{
                "user_name": f"{user.first_name} {user.last_name}",
                "reset_link": f"{CLIENT_HOST_URL}/reset-password/{temp_token.token}",
                "link_expiration_date": temp_token.expiration_date,
            },
        )

        EmailTasks.send_email.apply_async(args=["Password Reset", [user.email]], kwargs={"html": email_template})

    #
    #

    def reset_password(self, data: dict):
        new_password, token = data["new_password"], data["token"]

        temp_token = self.__find_temp_token(token, TemporaryTokenType.PASSWORD_RESET)

        def reset_password_and_delete_token(session: Session):
            self.user_repo.update(
                filter=lambda User: User.id == temp_token.user_id,
                new_data={"password": generate_password_hash(new_password)},
                options={"session": session},
            )

            self.temp_token_repo.delete(
                filter=lambda Token: Token.token == token,
                options={"session": session},
            )

        self.user_repo.start_transaction(reset_password_and_delete_token)

    #
    #

    def request_email_verification(self, user_id: str):
        # get user data
        user = self.user_repo.find(
            filter=lambda User: User.id == user_id,
            options={
                "throw_if_not_found": True,
                "error_msg": ResponseMessage.FAILED_USER_NOT_FOUND_WITH_ID,
                "return_first": True,
            },
        )

        if user.is_verified:
            return True

        temp_token = self.__create_temp_token(user.id, TemporaryTokenType.EMAIL_VERIFICATION)

        email_template = render_template(
            "emails/verify_email.html",
            **{
                "user_name": f"{user.first_name} {user.last_name}",
                "verification_link": f"{CLIENT_HOST_URL}/verify-password/{temp_token.token}",
                "link_expiration_date": temp_token.expiration_date,
            },
        )

        EmailTasks.send_email.apply_async(args=["Email Verification", [user.email]], kwargs={"html": email_template})

        return False

    #
    #

    def verify_email(self, token: str):
        temp_token = self.__find_temp_token(token, TemporaryTokenType.EMAIL_VERIFICATION)

        def verify_email_and_delete_token(session: Session):
            self.user_repo.update(
                filter=lambda User: User.id == temp_token.user_id,
                new_data={"is_verified": True},
                options={"session": session},
            )

            self.temp_token_repo.delete(
                filter=lambda Token: Token.token == token,
                options={"session": session},
            )

        self.user_repo.start_transaction(verify_email_and_delete_token)

    #
    #
    #

    # PRIVATE
    def __create_temp_token(self, user_id: str, token_type: TemporaryTokenType):
        def create_new_token_and_delete_old_tokens(session: Session):
            # delete old (password_reset) token(s) for that user
            self.temp_token_repo.delete(
                filter=lambda Token: (Token.user_id == user_id) & (Token.type == token_type),
                options={"session": session},
            )

            # create the new token
            return self.temp_token_repo.create(
                {
                    "token": secrets.token_urlsafe(TEMP_TOKEN_LENGTH),
                    "expiration_date": add_to_datetime(hours=TEMP_TOKEN_EXP_IN_HOURS),
                    "user_id": user_id,
                    "type": token_type,
                },
                {"session": session},
            )

        return self.temp_token_repo.start_transaction(create_new_token_and_delete_old_tokens)

    #
    #

    def __find_temp_token(self, token: str, type: TemporaryTokenType):
        return self.temp_token_repo.find(
            filter=lambda Token: (Token.token == token)
            & (Token.expiration_date > datetime.datetime.now())
            & (Token.type == type),
            options={
                "throw_if_not_found": True,
                "error_msg": ResponseMessage.FAILED_NOT_EXIST_OR_INVALID_TEMP_TOKEN,
                "return_first": True,
            },
        )
