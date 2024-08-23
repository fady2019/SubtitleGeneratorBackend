from db.repositories.repository.crud_repository import CRUDRepository
from db.entities.subtitle import SubtitleEntity
from db.entity_dicts.subtitle_entity_dict import CreateSubtitleEntityDict, UpdateSubtitleEntityDict


class SubtitleRepository(CRUDRepository[SubtitleEntity, CreateSubtitleEntityDict, UpdateSubtitleEntityDict]):
    def _get_entity_type(self):
        return SubtitleEntity
