import jwt
from datetime import datetime

from exceptions.response_error import ResponseError


def generate_token_from_payload(payload: dict, expire_in: datetime, private_key: str, algorithm="RS256"):
    token = jwt.encode(
        payload={
            "data": payload,
            "expire_in": expire_in.timestamp(),
        },
        key=private_key,
        algorithm=algorithm,
    )

    return token


def extract_payload_from_token(token: str, public_key: str, algorithms: list[str] = "RS256", ignore_exp: bool = False):
    payload: dict = jwt.decode(token, key=public_key, algorithms=algorithms)

    expire_in = datetime.fromtimestamp(payload["expire_in"] or 0)

    if not ignore_exp and expire_in <= datetime.now():
        raise ResponseError("token expired", status_code=401)

    return payload["data"]
