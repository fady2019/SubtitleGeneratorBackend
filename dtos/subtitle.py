from typing import Optional

from dtos.dto import DTO
from db.entities.subtitle import SubtitleStatus


class SubtitleDTO(DTO):
    id: str
    title: str
    status: SubtitleStatus
    language: str
    start_date: str
    finish_date: Optional[str]
    user_id: str


class SubtitleWithTaskIdDTO(SubtitleDTO):
    task_id: Optional[str]
