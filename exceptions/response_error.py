from flask import jsonify


class ResponseError(BaseException):
    def __init__(self, msg: str, status_code: int = 500):
        self.msg = msg
        self.status_code = status_code

    def as_response(self):
        return jsonify({"message": self.msg}), self.status_code
