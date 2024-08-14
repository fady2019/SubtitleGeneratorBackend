from voluptuous import Schema, MultipleInvalid, Invalid

from response.response import ResponseError


class CustomInvalid(Invalid):
    def __init__(self, message, status_code, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.status_code = status_code


def validator_executor(schema: Schema, data):
    try:
        try:
            schema(data)
        except MultipleInvalid as err:
            raise err.errors[0]
    except CustomInvalid as err:
        raise ResponseError({"msg": err.error_message, "status_code": err.status_code})
    except Invalid as err:
        raise ResponseError({"msg": err.error_message, "status_code": 422})
