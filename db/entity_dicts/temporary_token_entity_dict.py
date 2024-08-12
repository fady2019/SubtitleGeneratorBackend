from builtins import str
from datetime import datetime
from db.entities.temporary_token import TemporaryTokenType
from db.entity_dicts.entity_dict import CreateEntityDict
from uuid import UUID


class CreateTemporaryTokenEntityDict(CreateEntityDict):
    token: str
    expiration_date: datetime
    user_id: UUID
    type: TemporaryTokenType