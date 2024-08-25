from dtos_mappers.mapper import Mapper
from db.entities.segment import SegmentEntity
from dtos.segment import SegmentDTO


class SegmentMapper(Mapper[SegmentEntity, SegmentDTO]):
    def to_dto(self, entity):
        if not entity:
            return None

        return SegmentDTO(
            segment_id=entity.segment_id,
            subtitle_id=str(entity.subtitle_id),
            text=entity.text,
            start=entity.start,
            end=entity.end,
        )
