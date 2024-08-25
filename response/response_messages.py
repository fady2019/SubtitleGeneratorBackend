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
    SUCCESSFUL_REQUEST_EMAIL_VERIFICATION_ALREADY_VERIFIED = {"msg": "your email is already verified", "status_code": 200}
    SUCCESSFUL_SUBTITLES_FETCHING = {"msg": "subtitles successfully fetched", "status_code": 200}
    SUCCESSFUL_SUBTITLE_FETCHING = {"msg": "subtitle successfully fetched", "status_code": 200}
    SUCCESSFUL_SUBTITLE_GENERATION_BEGINNING = {
        "msg": "subtitle generation successfully began. this process may take some time. we will send you an email as soon as it is complete",
        "status_code": 200,
    }
    SUCCESSFUL_SUBTITLE_GENERATION_CANCELING = {"msg": "subtitle generation successfully canceled", "status_code": 200}
    SUCCESSFUL_SUBTITLE_GENERATION_REBEGINNING = {
        "msg": "subtitle generation successfully rebegan. this process may take some time. we will send you an email as soon as it is complete",
        "status_code": 200,
    }
    SUCCESSFUL_SUBTITLE_EDITING = {"msg": "subtitle successfully edited", "status_code": 200}
    SUCCESSFUL_SUBTITLE_DELETION = {"msg": "subtitle successfully deleted", "status_code": 200}
    SUCCESSFUL_SEGMENTS_FETCHING = {"msg": "segments successfully fetched", "status_code": 200}
    SUCCESSFUL_SEGMENT_EDITING = {"msg": "segments successfully edited", "status_code": 200}

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
    FAILED_USER_HAS_NO_SUBTITLE_WITH_ID = {"msg": "you don't have a subtitle with the entered id", "status_code": 404}
    FAILED_SUBTITLE_NOT_FOUND_WITH_ID = {"msg": "there's no a subtitle with the entered id", "status_code": 404}
    FAILED_AUDIO_FILE_NOT_FOUND = {"msg": "can't find the audio file", "status_code": 404}
    # 409
    FAILED_CANCELING_INACTIVE_SUBTITLE_GENERATION = {
        "msg": "inactive subtitle generation can't be canceled",
        "status_code": 409,
    }
    FAILED_SUBTITLE_REGENERATION_INVALID_STATUS = {
        "msg": "only failed and canceled subtitles can be regenerated",
        "status_code": 409,
    }
    FAILED_EDITING_ACTIVE_SUBTITLE_GENERATION = {"msg": "can't edit active subtitle generation", "status_code": 409}
    FAILED_DELETING_ACTIVE_SUBTITLE_GENERATION = {"msg": "can't delete active subtitle generation", "status_code": 409}
    FAILED_CREATING_SUBTITLE_FILE_INVALID_STATE = {
        "msg": "subtitle file creation failed. the subtitle generation might not be complete yet, or there may be no segments available",
        "status_code": 409,
    }
