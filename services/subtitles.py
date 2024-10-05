import warnings

warnings.filterwarnings("ignore", category=FutureWarning, message="You are using `torch.load` with `weights_only=False`")

from celery.result import AsyncResult
from werkzeug.datastructures import FileStorage
import os

from celery_tasks.subtitles import SubtitleTasks
from db.repositories.subtitle import SubtitleRepository
from db.entities.subtitle import SubtitleStatus
from response.response import ResponseError
from response.response_messages import ResponseMessage
from dtos.subtitle import SubtitleWithTaskIdDTO
from dtos_mappers.subtitle import SubtitleMapper
from helpers.celery import mark_task_as_revoked, revoke_task
from helpers.file import delete_dir, create_file


MEDIA_FILES_TMP_STORAGE_PATH = os.path.join(*os.getenv("MEDIA_FILES_TMP_STORAGE_PATH", "tmp").split("/"))
MEDIA_FILE_NAME = os.getenv("MEDIA_FILE_NAME")

MAX_NUMBER_OF_SUBTITLES_PER_USER = int(os.getenv("MAX_NUMBER_OF_SUBTITLES_PER_USER", 10))


class SubtitlesService:
    def __init__(self) -> None:
        self.subtitle_repo = SubtitleRepository()
        self.subtitle_mapper = SubtitleMapper()

    #
    #
    #

    def fetch_subtitles(self, user_id: str):
        subtitle_entities = self.subtitle_repo.find(filter=lambda Subtitle: Subtitle.user_id == user_id)
        return self.subtitle_mapper.to_dtos(subtitle_entities)

    #
    #

    def fetch_subtitle(self, user_id: str, subtitle_id: str):
        subtitle_entity = self.subtitle_repo.find(
            filter=lambda Subtitle: (Subtitle.id == subtitle_id) & (Subtitle.user_id == user_id),
            options={"return_first": True},
        )

        return self.subtitle_mapper.to_dto(subtitle_entity)

    #
    #

    def generate_subtitle(self, user_id: str, data: dict = None):
        subtitle_count = self.subtitle_repo.count(filter=lambda Subtitle: Subtitle.user_id == user_id)

        if subtitle_count == MAX_NUMBER_OF_SUBTITLES_PER_USER:
            raise ResponseError(
                {
                    "msg": f"subtitles generation limit reached. you can only generate up to {MAX_NUMBER_OF_SUBTITLES_PER_USER} subtitle(s)",
                    "status_code": 409,
                }
            )

        subtitle_entity = self.subtitle_repo.create(
            {"user_id": user_id, "title": data["title"], "translate": data["translate"]}
        )
        subtitle = self.subtitle_mapper.to_dto(subtitle_entity)

        # SAVE THE MEDIA FILE AS AUDIO FILE
        media_file_dir, media_file_path = self.__get_media_file_path(subtitle["id"])
        media_file: FileStorage = data["media_file"]
        media_file.save(media_file_path)

        # # START EXTRACTING SUBTITLE
        result: AsyncResult = SubtitleTasks.begin_subtitle_generation.apply_async(args=[subtitle, media_file_dir])

        # # SAVE THE TASK_ID IN THE SUBTITLE RECORD
        # # IT'S REQUIRED TO TERMINATE THE TASK (IF THE USER WANTS TO)
        self.subtitle_repo.update(
            filter=lambda Subtitle: Subtitle.id == subtitle["id"], new_data={"task_id": result.task_id}
        )

        return subtitle

    #
    #

    def cancel_subtitle_generation(self, subtitle: SubtitleWithTaskIdDTO):
        if subtitle["status"] not in [SubtitleStatus.SCHEDULED.value, SubtitleStatus.IN_PROGRESS.value]:
            raise ResponseError(ResponseMessage.FAILED_CANCELING_INACTIVE_SUBTITLE_GENERATION)

        revoke_task(subtitle["task_id"])

        if subtitle["status"] == SubtitleStatus.SCHEDULED.value:
            mark_task_as_revoked(subtitle["task_id"])

        self.subtitle_repo.update(
            filter=lambda Subtitle: (Subtitle.id == subtitle["id"]),
            new_data={"status": SubtitleStatus.CANCELED, "task_id": None, "start_date": None},
        )

    #
    #

    def regenerate_subtitle(self, subtitle: SubtitleWithTaskIdDTO):
        if subtitle["status"] not in [SubtitleStatus.FAILED.value, SubtitleStatus.CANCELED.value]:
            raise ResponseError(ResponseMessage.FAILED_SUBTITLE_REGENERATION_INVALID_STATUS)

        media_file_dir, _ = self.__get_media_file_path(subtitle["id"])

        if not os.path.exists(media_file_dir):
            raise ResponseError(ResponseMessage.FAILED_SUBTITLE_MEDIA_FILE_NOT_FOUND)

        self.subtitle_repo.update(
            filter=lambda Subtitle: Subtitle.id == subtitle["id"], new_data={"status": SubtitleStatus.SCHEDULED}
        )

        result: AsyncResult = SubtitleTasks.begin_subtitle_generation.apply_async(args=[subtitle, media_file_dir])

        self.subtitle_repo.update(
            filter=lambda Subtitle: Subtitle.id == subtitle["id"], new_data={"task_id": result.task_id}
        )

    #
    #

    def edit_subtitle(self, subtitle: SubtitleWithTaskIdDTO, date: dict):
        if subtitle["status"] in [SubtitleStatus.SCHEDULED.value, SubtitleStatus.IN_PROGRESS.value]:
            raise ResponseError(ResponseMessage.FAILED_EDITING_ACTIVE_SUBTITLE_GENERATION)

        subtitle_entities = self.subtitle_repo.update(
            filter=lambda Subtitle: Subtitle.id == subtitle["id"],
            new_data={"title": date["title"]},
        )

        return self.subtitle_mapper.to_dto(subtitle_entities[0] if subtitle_entities else None)

    #
    #

    def delete_subtitle(self, subtitle: SubtitleWithTaskIdDTO):
        if subtitle["status"] in [SubtitleStatus.SCHEDULED.value, SubtitleStatus.IN_PROGRESS.value]:
            raise ResponseError(ResponseMessage.FAILED_DELETING_ACTIVE_SUBTITLE_GENERATION)

        # DELETE RECORD IN DB
        self.subtitle_repo.delete(filter=lambda Subtitle: Subtitle.id == subtitle["id"])

        # REMOVE MEDIA FILE DIR
        media_file_dir, _ = self.__get_media_file_path(subtitle["id"])
        delete_dir(media_file_dir, only_if_empty=False)

    #
    #
    #

    # PRIVATE
    def __get_media_file_path(self, subtitle_id: str):
        media_file_dir = os.path.join(MEDIA_FILES_TMP_STORAGE_PATH, subtitle_id)
        return media_file_dir, create_file(media_file_dir, MEDIA_FILE_NAME)
