from functools import wraps
import logging

from exceptions.response_error import ResponseError


def app_error_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ResponseError as err:
            return err.as_response()
        except RuntimeError as err:
            return ResponseError("server error", 500).as_response()

    return decorated_function
