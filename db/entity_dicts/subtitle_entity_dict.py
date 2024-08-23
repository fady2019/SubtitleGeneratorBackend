from builtins import str
from datetime import datetime
from db.entities.subtitle import SubtitleStatus
from db.entity_dicts.entity_dict import CreateEntityDict, UpdateEntityDict
from typing import Optional
from uuid import UUID


class CreateSubtitleEntityDict(CreateEntityDict):
    title: Optional[str]
    user_id: UUID


class UpdateSubtitleEntityDict(UpdateEntityDict):
    title: Optional[str]
    status: Optional[SubtitleStatus]
    language: Optional[str]
    finish_date: Optional[datetime]
    task_id: Optional[UUID]