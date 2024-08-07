from flask import Response, request, g
from functools import wraps
import jwt, datetime, os, base64, typing

from helpers.cookies import set_cookie, delete_cookie
from exceptions.response_error import ResponseError


JWT_EXP = int(os.getenv("JWT_EXP_IN_HOURS") or 1)
JWT_PUBLIC_KEY = base64.b64decode(os.getenv("JWT_PUBLIC_KEY")).decode()
JWT_PRIVATE_KEY = base64.b64decode(os.getenv("JWT_PRIVATE_KEY")).decode()
JWT_TOKEN_COOKIE_NAME = os.getenv("JWT_TOKEN_COOKIE_NAME", "token")


def sign_token(f: typing.Callable[..., Response]):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        user_id = response.json["id"]

        if not user_id:
            return response

        jwt_exp = datetime.datetime.now() + datetime.timedelta(hours=JWT_EXP)

        token = jwt.encode(
            payload={"id": user_id, "exp": jwt_exp},
            key=JWT_PRIVATE_KEY,
            algorithm="RS256",
        )

        set_cookie(response, JWT_TOKEN_COOKIE_NAME, token, expires=jwt_exp)

        return response

    return decorated_function


def validate_token(ignore_exp=False, ignore_invalid_token=False):
    def decorator(f: typing.Callable[..., Response]):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                token = request.cookies.get(JWT_TOKEN_COOKIE_NAME, "")

                payload = jwt.decode(token, key=JWT_PUBLIC_KEY, algorithms="RS256")

                exp_date = datetime.datetime.fromtimestamp(payload["exp"] or 0)

                if not ignore_exp and exp_date <= datetime.datetime.now():
                    raise Exception()

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

            print(response.json)

            if not only_if or only_if(response):
                delete_cookie(response, JWT_TOKEN_COOKIE_NAME)

            return response

        return decorated_function

    return decorator
