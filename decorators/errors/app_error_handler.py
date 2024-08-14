from werkzeug.exceptions import HTTPException
from functools import wraps

from response.response import ResponseError


def app_error_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ResponseError as err:
            return err
        except HTTPException as err:
            return ResponseError({"msg": err.description, "status_code": err.code})
        except Exception as err:
            print(type(err), err)
            return ResponseError({"msg": "server error", "status_code": 500})

    return decorated_function
