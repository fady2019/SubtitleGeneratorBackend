import warnings

warnings.filterwarnings("ignore", category=FutureWarning, message="You are using `torch.load` with `weights_only=False`")

from celery.result import AsyncResult
from werkzeug.datastructures import FileStorage
import os

from celery_tasks.subtitles import SubtitleTasks
from db.repositories.subtitle import SubtitleRepository
from db.repositories.segment import SegmentRepository
from db.entities.subtitle import SubtitleStatus
from response.response import ResponseError
from response.response_messages import ResponseMessage
from dtos.subtitle import SubtitleWithTaskIdDTO
from dtos_mappers.subtitle import SubtitleMapper

TMP_STORAGE_PATH = os.path.join(*os.getenv("UPLOADED_AUDIOS_TMP_STORAGE_PATH", "tmp").split("/"))
os.makedirs(TMP_STORAGE_PATH, exist_ok=True)


class SubtitlesService:
    def __init__(self) -> None:
        self.subtitle_repo = SubtitleRepository()
        self.segment_repo = SegmentRepository()
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
        subtitle_entity = self.subtitle_repo.create({"user_id": user_id, "title": data["title"]})
        subtitle = self.subtitle_mapper.to_dto(subtitle_entity)

        # SAVE THE AUDIO FILE
        audio: FileStorage = data["audio"]
        audio_path = self.__get_audio_path(subtitle["id"])
        audio.save(audio_path)

        # START EXTRACTING SUBTITLE
        SubtitleTasks.transcribe.apply_async(args=[subtitle, audio_path])

        return subtitle

    #
    #

    def cancel_subtitle_generation(self, subtitle: SubtitleWithTaskIdDTO):
        if subtitle["status"] != SubtitleStatus.IN_PROGRESS.value:
            raise ResponseError(ResponseMessage.FAILED_CANCELING_INACTIVE_SUBTITLE_GENERATION)

        result = AsyncResult(subtitle["task_id"])
        result.revoke(terminate=True, signal="SIGKILL")

        self.subtitle_repo.update(
            filter=lambda Subtitle: (Subtitle.id == subtitle["id"]),
            new_data={"status": SubtitleStatus.CANCELED, "task_id": None},
        )

    #
    #

    def regenerate_subtitle(self, subtitle: SubtitleWithTaskIdDTO):
        if subtitle["status"] not in [SubtitleStatus.FAILED.value, SubtitleStatus.CANCELED.value]:
            raise ResponseError(ResponseMessage.FAILED_SUBTITLE_REGENERATION_INVALID_STATUS)

        audio_path = self.__get_audio_path(subtitle["id"])

        if not os.path.exists(audio_path):
            raise ResponseError(ResponseMessage.FAILED_AUDIO_FILE_NOT_FOUND)

        SubtitleTasks.transcribe.apply_async(args=[subtitle, audio_path])

        self.subtitle_repo.update(
            filter=lambda Subtitle: Subtitle.id == subtitle["id"], new_data={"status": SubtitleStatus.IN_PROGRESS}
        )

    #
    #

    def edit_subtitle(self, subtitle: SubtitleWithTaskIdDTO, date: dict):
        if subtitle["status"] == SubtitleStatus.IN_PROGRESS.value:
            raise ResponseError(ResponseMessage.FAILED_EDITING_ACTIVE_SUBTITLE_GENERATION)

        subtitle_entities = self.subtitle_repo.update(
            filter=lambda Subtitle: Subtitle.id == subtitle["id"],
            new_data={"title": date["title"]},
        )

        return self.subtitle_mapper.to_dto(subtitle_entities[0] if subtitle_entities else None)

    #
    #

    def delete_subtitle(self, subtitle: SubtitleWithTaskIdDTO):
        if subtitle["status"] == SubtitleStatus.IN_PROGRESS.value:
            raise ResponseError(ResponseMessage.FAILED_DELETING_ACTIVE_SUBTITLE_GENERATION)

        # DELETE RECORD IN DB
        self.subtitle_repo.delete(filter=lambda Subtitle: Subtitle.id == subtitle["id"])

        # REMOVE AUDIO IF EXISTS
        audio_path = self.__get_audio_path(subtitle["id"])

        if os.path.exists(audio_path):
            os.remove(audio_path)

    #
    #
    #

    # PRIVATE
    def __get_audio_path(self, subtitle_id: str):
        return os.path.join(TMP_STORAGE_PATH, f"{subtitle_id}")
