from dtos_mappers.mapper import Mapper
from db.entities.subtitle import SubtitleEntity
from dtos.subtitle import SubtitleDTO, SubtitleWithTaskIdDTO


class SubtitleMapper(Mapper[SubtitleEntity, SubtitleDTO]):
    def to_dto(self, entity):
        if not entity:
            return None

        return SubtitleDTO(
            id=str(entity.id),
            title=entity.title,
            status=entity.status.value,
            language=entity.language,
            start_date=entity.start_date.isoformat(),
            finish_date=entity.finish_date.isoformat() if entity.finish_date else None,
            user_id=str(entity.user_id),
        )


class SubtitleWithTaskIdMapper(SubtitleMapper):
    def to_dto(self, entity):
        if not entity:
            return None

        return SubtitleWithTaskIdDTO(
            **super().to_dto(entity),
            task_id=str(entity.task_id) if entity.task_id else None,
        )
