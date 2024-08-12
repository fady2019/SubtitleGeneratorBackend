from flask import Response, request, g
from functools import wraps
from typing import Callable, TypedDict
import os, base64

from db.repositories.user import UserRepository
from dtos_mappers.user import UserMapper
from helpers.cookies import set_cookie, delete_cookie
from helpers.jwt import generate_token_from_payload, extract_payload_from_token
from exceptions.response_error import ResponseError


JWT_EXP_IN_HOURS = float(os.getenv("JWT_AUTH_TOKEN_EXP_IN_HOURS", "1"))
JWT_PUBLIC_KEY = base64.b64decode(os.getenv("JWT_AUTH_TOKEN_PUBLIC_KEY")).decode()
JWT_PRIVATE_KEY = base64.b64decode(os.getenv("JWT_AUTH_TOKEN_PRIVATE_KEY")).decode()
JWT_TOKEN_COOKIE_NAME = os.getenv("JWT_AUTH_TOKEN_TOKEN_COOKIE_NAME", "token")

user_repo = UserRepository()


class Payload(TypedDict):
    user_id: str


def sign_token(get_payload: Callable[[Response], Payload]):
    def decorator(f: Callable[..., Response]):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)

            payload = get_payload(response)

            if payload == None:
                return response

            token, expiration_date = generate_token_from_payload(payload, JWT_EXP_IN_HOURS, JWT_PRIVATE_KEY)

            set_cookie(response, JWT_TOKEN_COOKIE_NAME, token, expires=expiration_date)

            return response

        return decorated_function

    return decorator


def validate_token(ignore_exp=False, ignore_invalid_token=False):
    def decorator(f: Callable[..., Response]):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                token = request.cookies.get(JWT_TOKEN_COOKIE_NAME, "")

                payload: Payload = extract_payload_from_token(token, JWT_PUBLIC_KEY, ignore_exp=ignore_exp)

                user = user_repo.find_first(filter=lambda User: User.id == payload["user_id"])

                if not user:
                    raise Exception()

                g.user = UserMapper().to_dto(user)
            except:
                if not ignore_invalid_token:
                    raise ResponseError("forbidden", status_code=403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def unsign_token(only_if: Callable[[Response], bool] = None):
    def decorator(f: Callable[..., Response]):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)

            if not only_if or only_if(response):
                delete_cookie(response, JWT_TOKEN_COOKIE_NAME)

            return response

        return decorated_function

    return decorator
