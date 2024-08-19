from typing import TypedDict, TypeVar


class DTO(TypedDict):
    pass


TDto = TypeVar("DTO", bound=type[DTO])
