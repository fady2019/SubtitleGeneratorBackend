from typing import TypedDict, Optional

from db.entities.subtitle import SubtitleStatus
from db.repositories.segment import SegmentRepository
from dtos_mappers.segment import SegmentMapper
from services.subtitle_file.subtitle_file_creator import SubtitleFileCreator
from dtos.subtitle import SubtitleWithTaskIdDTO
from response.response import ResponseError
from response.response_messages import ResponseMessage


class SegmentsService:
    def __init__(self) -> None:
        self.segment_repo = SegmentRepository()
        self.segment_mapper = SegmentMapper()
        self.subtitle_file_creator = SubtitleFileCreator()

    #
    #
    #

    def fetch_segments(self, subtitle_id: str, options: dict = {}):
        segment_entities, count, has_next = self.segment_repo.find_with_pagination(
            filter=lambda Segment: (
                (Segment.subtitle_id == subtitle_id)
                & (Segment.text.icontains(options.get("segment_search", ""), autoescape=True))
            ),
            order_by=lambda Segment: Segment.segment_id.asc(),
            options={"page": options.get("page"), "items_per_page": options.get("items_per_page")},
        )

        return {
            "segments": self.segment_mapper.to_dtos(segment_entities),
            "count": count,
            "has_next": has_next,
        }

    #
    #

    def edit_segment(self, subtitle_id: str, segment_id: int, data: dict):
        segment_entities = self.segment_repo.update(
            filter=lambda Segment: (Segment.subtitle_id == subtitle_id) & (Segment.segment_id == segment_id),
            new_data={"text": data["text"]},
        )

        return self.segment_mapper.to_dto(segment_entities[0] if segment_entities else None)

    #
    #

    def create_file(self, subtitle: SubtitleWithTaskIdDTO, file_type: str):
        segment_entities = []

        if subtitle["status"] == SubtitleStatus.COMPLETED.value:
            segment_entities = self.segment_repo.find(
                filter=lambda Segment: Segment.subtitle_id == subtitle["id"],
                order_by=lambda Segment: Segment.segment_id.asc(),
            )

        if not len(segment_entities):
            raise ResponseError(ResponseMessage.FAILED_CREATING_SUBTITLE_FILE_INVALID_STATE)

        segments = self.segment_mapper.to_dtos(segment_entities)

        return self.subtitle_file_creator.create(file_type, segments)
