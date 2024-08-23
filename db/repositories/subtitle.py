from sqlalchemy import update

from db.repositories.repository.create_repository import CreateRepository
from db.repositories.repository.update_repository import UpdateRepository
from db.repositories.repository.find_repository import FindRepository
from db.repositories.repository.delete_repository import DeleteRepository
from db.entities.subtitle import SubtitleEntity
from db.entity_dicts.subtitle_entity_dict import CreateSubtitleEntityDict, UpdateSubtitleEntityDict

from response.response import ResponseError


class SubtitleRepository(
    CreateRepository[SubtitleEntity, CreateSubtitleEntityDict],
    UpdateRepository[SubtitleEntity, UpdateSubtitleEntityDict],
    FindRepository[SubtitleEntity],
    DeleteRepository[SubtitleEntity],
):
    def _execute_create(self, data, options):
        subtitle_entities = []

        for subtitle_data in data:
            subtitle_entity = SubtitleEntity(title=subtitle_data["title"], user_id=subtitle_data["user_id"])
            subtitle_entities.append(subtitle_entity)

        options["session"].add_all(subtitle_entities)

        return subtitle_entities

    #
    #

    def _execute_update(self, filter, new_data, options):
        query = update(SubtitleEntity).where(filter(SubtitleEntity)).values(**new_data).returning(SubtitleEntity)
        result = options["session"].execute(query)
        return [row.tuple()[0] for row in result.fetchall()]

    #
    #

    def _execute_find(self, filter, order_by, options):
        subtitle_entities = (
            options["session"].query(SubtitleEntity).filter(filter(SubtitleEntity)).order_by(order_by(SubtitleEntity)).all()
        )

        if not subtitle_entities and options["throw_if_not_found"]:
            raise ResponseError(options["error_msg"] or {"msg": "subtitle(s) not found", "status_code": 404})

        return subtitle_entities

    #
    #

    def _execute_delete(self, filter, options):
        subtitle_entities = options["session"].query(SubtitleEntity).filter(filter(SubtitleEntity)).all()

        for subtitle_entity in subtitle_entities:
            options["session"].delete(subtitle_entity)
