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
