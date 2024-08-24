from db.repositories.segment import SegmentRepository
from dtos_mappers.segment import SegmentMapper


class SegmentsService:
    def __init__(self) -> None:
        self.segment_repo = SegmentRepository()
        self.segment_mapper = SegmentMapper()

    #
    #
    #

    def fetch_segments(self, subtitle_id: str, page: int | str | None, items_per_page: int | str | None):
        segment_entities, count, has_next = self.segment_repo.find_with_pagination(
            filter=lambda Segment: Segment.subtitle_id == subtitle_id,
            order_by=lambda Segment: Segment.segment_id.asc(),
            options={"page": page, "items_per_page": items_per_page},
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
