from flask import Response
from functools import wraps
import jwt, datetime, os, base64, typing

JWT_EXP = int(os.getenv("JWT_EXP_IN_HOURS") or 1)
JWT_PUBLIC_KEY = base64.b64decode(os.getenv("JWT_PUBLIC_KEY")).decode()
JWT_PRIVATE_KEY = base64.b64decode(os.getenv("JWT_PRIVATE_KEY")).decode()
SECONDS_IN_HOUR = 3600


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

        response.set_cookie("token", token, expires=jwt_exp, httponly=True)

        return response

    return decorated_function
