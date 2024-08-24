from flask import request
from abc import abstractmethod, ABC


class InputSource(ABC):
    @abstractmethod
    def read(self):
        pass


class RequestJson(InputSource):
    def read(self):
        return request.json


class RequestViewArgs(InputSource):
    def read(self):
        return request.view_args


class RequestFiles(InputSource):
    def read(self):
        return {k: v for k, v in request.files.items()}


class RequestForm(InputSource):
    def read(self):
        return {k: v for k, v in request.form.items()}


class RequestArgs(InputSource):
    def read(self):
        return {k: v for k, v in request.args.items()}
