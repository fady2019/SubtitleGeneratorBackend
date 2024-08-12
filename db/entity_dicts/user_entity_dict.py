from builtins import bool, str
from db.entity_dicts.entity_dict import CreateEntityDict, UpdateEntityDict
from typing import Optional


class CreateUserEntityDict(CreateEntityDict):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class UpdateUserEntityDict(UpdateEntityDict):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_verified: Optional[bool]