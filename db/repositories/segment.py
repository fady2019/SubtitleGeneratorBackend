from db.repositories.repository.create_repository import CreateRepository
from db.repositories.repository.find_repository import FindRepository
from db.entities.segment import SegmentEntity
from db.entity_dicts.segment_entity_dict import CreateSegmentEntityDict
from response.response import ResponseError


class SegmentRepository(CreateRepository[SegmentEntity, CreateSegmentEntityDict], FindRepository[SegmentEntity]):
    def _execute_create(self, data, options):
        segment_entities = []

        for segment_data in data:
            segment_entity = SegmentEntity(
                segment_id=segment_data["segment_id"],
                subtitle_id=segment_data["subtitle_id"],
                start=segment_data["start"],
                end=segment_data["end"],
                text=segment_data["text"],
            )

            segment_entities.append(segment_entity)

        options["session"].add_all(segment_entities)

        return segment_entities

    #
    #

    def _execute_find(self, filter, order_by, options):
        segments_entities = (
            options["session"].query(SegmentEntity).filter(filter(SegmentEntity)).order_by(order_by(SegmentEntity)).all()
        )

        if not segments_entities and options["throw_if_not_found"]:
            raise ResponseError(options["error_msg"] or {"msg": "segment(s) not found", "status_code": 404})

        return segments_entities
