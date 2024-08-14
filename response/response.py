from flask import Response as FlaskResponse
import json

from response.response_messages import ResponseMessageBase, ResponseMsgInfo


class Response(FlaskResponse):
    def __init__(
        self, response_msg: ResponseMessageBase | ResponseMsgInfo, data: dict = None, mimetype: str = "application/json"
    ):
        response_body = {}

        if data:
            response_body["data"] = data

        if isinstance(response_msg, ResponseMessageBase):
            response_msg = response_msg.value

        response_body["message"] = response_msg["msg"]

        super().__init__(json.dumps(response_body), response_msg["status_code"], mimetype=mimetype)

        self.custom_data = data


class ResponseError(Response, BaseException):
    pass
