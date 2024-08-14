import jwt

from helpers.date import add_to_datetime, is_in_future


def generate_token_from_payload(payload: dict, expire_in_hours: int, private_key: str, algorithm="RS256"):
    expiration_date = add_to_datetime(hours=expire_in_hours)

    token = jwt.encode(
        payload={
            "data": payload,
            "expiration_date": expiration_date.timestamp(),
        },
        key=private_key,
        algorithm=algorithm,
    )

    return token, expiration_date


def extract_payload_from_token(token: str, public_key: str, algorithms: list[str] = "RS256", ignore_exp: bool = False):
    payload: dict = jwt.decode(token, key=public_key, algorithms=algorithms)

    if not ignore_exp and not is_in_future(payload["expiration_date"] or 0):
        raise Exception("token expired")

    return payload["data"]
