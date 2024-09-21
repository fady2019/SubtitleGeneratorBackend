import warnings

warnings.filterwarnings("ignore", category=FutureWarning, message="You are using `torch.load` with `weights_only=False`")

from celery.result import AsyncResult
from werkzeug.datastructures import FileStorage
import os, ffmpeg

from celery_tasks.subtitles import SubtitleTasks
from db.repositories.subtitle import SubtitleRepository
from db.entities.subtitle import SubtitleStatus
from response.response import ResponseError
from response.response_messages import ResponseMessage
from dtos.subtitle import SubtitleWithTaskIdDTO
from dtos_mappers.subtitle import SubtitleMapper
from helpers.celery import mark_task_as_invoked


TMP_STORAGE_PATH = os.path.join(*os.getenv("UPLOADED_AUDIOS_TMP_STORAGE_PATH", "tmp").split("/"))
os.makedirs(TMP_STORAGE_PATH, exist_ok=True)

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
        audio_path = self.__save_subtitle_media_file_as_audio(data["media_file"], subtitle["id"])

        # # START EXTRACTING SUBTITLE
        result: AsyncResult = SubtitleTasks.transcribe.apply_async(args=[subtitle, audio_path])

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

        result = AsyncResult(subtitle["task_id"])
        result.revoke(terminate=True, signal="SIGKILL")

        if subtitle["status"] == SubtitleStatus.SCHEDULED.value:
            mark_task_as_invoked(subtitle["task_id"])

        self.subtitle_repo.update(
            filter=lambda Subtitle: (Subtitle.id == subtitle["id"]),
            new_data={"status": SubtitleStatus.CANCELED, "task_id": None, "start_date": None},
        )

    #
    #

    def regenerate_subtitle(self, subtitle: SubtitleWithTaskIdDTO):
        if subtitle["status"] not in [SubtitleStatus.FAILED.value, SubtitleStatus.CANCELED.value]:
            raise ResponseError(ResponseMessage.FAILED_SUBTITLE_REGENERATION_INVALID_STATUS)

        audio_path = self.__get_audio_path(subtitle["id"])

        if not os.path.exists(audio_path):
            raise ResponseError(ResponseMessage.FAILED_SUBTITLE_MEDIA_FILE_NOT_FOUND)

        self.subtitle_repo.update(
            filter=lambda Subtitle: Subtitle.id == subtitle["id"], new_data={"status": SubtitleStatus.SCHEDULED}
        )

        result: AsyncResult = SubtitleTasks.transcribe.apply_async(args=[subtitle, audio_path])

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

        # REMOVE AUDIO IF EXISTS
        audio_path = self.__get_audio_path(subtitle["id"])

        if os.path.exists(audio_path):
            os.remove(audio_path)

    #
    #
    #

    def __save_subtitle_media_file_as_audio(self, media_file: FileStorage, subtitle_id: str):
        try:
            audio_path = self.__get_audio_path(subtitle_id)
            media_file_path = f"{audio_path}__media_file"

            media_file.save(media_file_path)

            ffmpeg.input(media_file_path).output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar=16000).run()

            return audio_path
        except Exception as err:
            print(err)
            # WHEN FAILING TO SAVE THE FILE REMOVE THE SUBTITLE FROM THE DB
            self.subtitle_repo.delete(filter=lambda Subtitle: Subtitle.id == subtitle_id)

            raise ResponseError(ResponseMessage.FAILED_CANT_LOAD_SUBTITLE_MEDIA_FILE)
        finally:
            if os.path.exists(media_file_path):
                os.remove(media_file_path)

    # PRIVATE
    def __get_audio_path(self, subtitle_id: str):
        return os.path.join(TMP_STORAGE_PATH, f"{subtitle_id}")
