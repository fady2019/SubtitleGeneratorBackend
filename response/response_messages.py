from typing import TypedDict
import enum


class ResponseMsgInfo(TypedDict):
    msg: str
    status_code: int


class ResponseMessageBase(enum.Enum):
    def __init__(self, value):
        if not isinstance(value, dict):
            raise ValueError(f'Expected value of type "dict", got "{type(value).__name__}"')

        annotations = ResponseMsgInfo.__annotations__

        if len(value) != len(annotations):
            raise ValueError(f"Expected to find {len(annotations)} key(s) in the dict, got {len(value)} key(s)")

        for key, key_type in annotations.items():
            if key not in value or type(value[key]) != key_type:
                raise ValueError(
                    f'Expected to find "{key}" in the dict with type of "{key_type.__name__}", got "{type(value.get(key)).__name__}"'
                )


class ResponseMessage(ResponseMessageBase):
    # Successful Responses
    # 200
    SUCCESSFUL_SIGNUP = {
        "msg": "successfully signed up, please check your inbox for an email verification link",
        "status_code": 200,
    }
    SUCCESSFUL_LOGIN = {"msg": "successfully logged in", "status_code": 200}
    SUCCESSFUL_AUTO_LOGIN_WITH_USER = {"msg": "successfully logged in automatically", "status_code": 200}
    SUCCESSFUL_AUTO_LOGIN_WITH_NO_USER = {"msg": "please login", "status_code": 200}
    SUCCESSFUL_LOGOUT = {"msg": "successfully logged out", "status_code": 200}
    SUCCESSFUL_PASSWORD_CHANGE = {"msg": "password successfully changed", "status_code": 200}
    SUCCESSFUL_REQUEST_PASSWORD_RESET = {
        "msg": "request successfully sent, please check your inbox for a reset link",
        "status_code": 200,
    }
    SUCCESSFUL_PASSWORD_RESET = {"msg": "password successfully reset", "status_code": 200}
    SUCCESSFUL_REQUEST_EMAIL_VERIFICATION = {
        "msg": "request successfully sent, please check your inbox for a verification link",
        "status_code": 200,
    }
    SUCCESSFUL_EMAIL_VERIFICATION = {"msg": "email successfully verified", "status_code": 200}

    #
    #
    #

    # Failed Responses
    # 400
    FAILED_NOT_EXIST_OR_INVALID_TEMP_TOKEN = {"msg": "invalid or not exist token", "status_code": 400}
    # 401
    FAILED_INVALID_CREDENTIALS = {"msg": "invalid credentials, please try again with the valid ones", "status_code": 401}
    FAILED_WRONG_CURRENT_PASSWORD = {"msg": "the current password is wrong", "status_code": 401}
    # 403
    FAILED_INVALID_AUTH_TOKEN = {"msg": "forbidden. please login", "status_code": 403}
    FAILED_EMAIL_NOT_VERIFIED = {
        "msg": "your email is not verified yet. please check your inbox for a verification link",
        "status_code": 403,
    }
    # 404
    FAILED_USER_NOT_FOUND_WITH_EMAIL = {"msg": "there's no user with the entered email", "status_code": 404}
    FAILED_USER_NOT_FOUND_WITH_ID = {"msg": "there's no user with the entered id", "status_code": 404}
