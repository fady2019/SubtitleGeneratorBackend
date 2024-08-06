from flask import Response
import os
from datetime import datetime

COOKIE_HTTP_ONLY = os.getenv("COOKIE_HTTP_ONLY", "").lower() == "true"
COOKIE_SAME_SITE = os.getenv("COOKIE_SAME_SITE")
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "").lower() == "true"
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN")


def set_cookie(response: Response, key: str, value: str, expires: str | datetime | int | float | None = None):
    response.set_cookie(
        key=key,
        value=value,
        expires=expires,
        httponly=COOKIE_HTTP_ONLY,
        samesite=COOKIE_SAME_SITE,
        secure=COOKIE_SECURE,
        domain=COOKIE_DOMAIN,
    )
