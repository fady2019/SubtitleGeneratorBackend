from db.repositories.repository.crud_repository import CRUDRepository
from db.entities.segment import SegmentEntity
from db.entity_dicts.segment_entity_dict import CreateSegmentEntityDict, UpdateSegmentEntityDict


class SegmentRepository(CRUDRepository[SegmentEntity, CreateSegmentEntityDict, UpdateSegmentEntityDict]):
    def _get_entity_type(self):
        return SegmentEntity
