from flask import Response, request, g
from functools import wraps
import jwt, datetime, os, base64, typing

from helpers.cookies import set_cookie, delete_cookie
from helpers.jwt import generate_token_from_payload, extract_payload_from_token
from exceptions.response_error import ResponseError


JWT_EXP = int(os.getenv("JWT_AUTH_TOKEN_EXP_IN_HOURS") or 1)
JWT_PUBLIC_KEY = base64.b64decode(os.getenv("JWT_AUTH_TOKEN_PUBLIC_KEY")).decode()
JWT_PRIVATE_KEY = base64.b64decode(os.getenv("JWT_AUTH_TOKEN_PRIVATE_KEY")).decode()
JWT_TOKEN_COOKIE_NAME = os.getenv("JWT_AUTH_TOKEN_TOKEN_COOKIE_NAME", "token")


def sign_token(get_payload: typing.Callable[[Response], dict]):
    def decorator(f: typing.Callable[..., Response]):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)

            payload = get_payload(response)

            jwt_exp = datetime.datetime.now() + datetime.timedelta(hours=JWT_EXP)

            token = generate_token_from_payload(payload, jwt_exp, JWT_PRIVATE_KEY)

            set_cookie(response, JWT_TOKEN_COOKIE_NAME, token, expires=jwt_exp)

            return response

        return decorated_function

    return decorator


def validate_token(ignore_exp=False, ignore_invalid_token=False):
    def decorator(f: typing.Callable[..., Response]):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                token = request.cookies.get(JWT_TOKEN_COOKIE_NAME, "")

                payload = extract_payload_from_token(token, JWT_PUBLIC_KEY, ignore_exp=ignore_exp)

                g.user_id = payload["id"]
            except:
                if not ignore_invalid_token:
                    raise ResponseError("forbidden", status_code=403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def unsign_token(only_if: typing.Callable[[Response], bool] = None):
    def decorator(f: typing.Callable[..., Response]):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)

            if not only_if or only_if(response):
                delete_cookie(response, JWT_TOKEN_COOKIE_NAME)

            return response

        return decorated_function

    return decorator
