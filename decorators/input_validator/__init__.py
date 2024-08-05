from flask import request
from functools import wraps
from typing import Set, Callable, Any

from .input_source import InputSource


def input_validator(input_source: InputSource, validator: Callable[[], Any], methods: Set[str] = {}):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if len(methods) > 0 and request.method not in methods:
                return f(*args, **kwargs)

            validator(input_source.read())

            return f(*args, **kwargs)

        return decorated_function

    return decorator
