from builtins import float, int, str
from db.entity_dicts.entity_dict import CreateEntityDict, UpdateEntityDict
from typing import Optional
from uuid import UUID


class CreateSegmentEntityDict(CreateEntityDict):
    segment_id: int
    start: float
    end: float
    text: str
    subtitle_id: UUID


class UpdateSegmentEntityDict(UpdateEntityDict):
    text: Optional[str]