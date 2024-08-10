from datetime import datetime

from db.dtos.dto import DTO
from db.entities.temporary_token import TemporaryTokenType


class TemporaryTokenDTO(DTO):
    token: str
    expiration_date: datetime
    user_id: str
    type: TemporaryTokenType
