from flask import render_template
from sqlalchemy.orm import Session
from celery import shared_task
from celery.app.task import Task
import whisper, os, datetime, ffmpeg

from db.repositories.user import UserRepository
from db.repositories.subtitle import SubtitleRepository
from db.repositories.segment import SegmentRepository
from db.entities.subtitle import SubtitleStatus
from celery_tasks.emails import EmailTasks
from dtos.subtitle import SubtitleDTO
from dtos_mappers.subtitle import SubtitleMapper
from helpers.date import to_datetime, get_duration
from helpers.celery import is_invoked, remove_invoked_task
from helpers.file import delete_file
from helpers.audio import extract_vocals, trim_silence
from helpers.file import delete_dir, delete_file, add_suffix_to_file_name
from helpers.subtitle_task import get_subtitle_task_metadata, set_subtitle_task_metadata, remove_subtitle_task_metadata

WHISPER_MODAL = os.getenv("WHISPER_MODAL")
CLIENT_HOST_URL = os.getenv("CLIENT_HOST_URL")


class SubtitleTasks:
    user_repo = UserRepository()
    subtitle_repo = SubtitleRepository()
    segment_repo = SegmentRepository()
    subtitle_mapper = SubtitleMapper()

    @staticmethod
    @shared_task(bind=True)
    def transcribe(self: Task, subtitle: SubtitleDTO, audio_path: str):
        if is_invoked(self.request.id):
            remove_invoked_task(self.request.id)
            raise Exception("invoked")

        try:
            # UPDATE SUBTITLE DATA
            subtitle_entities = SubtitleTasks.subtitle_repo.update(
                filter=lambda Subtitle: Subtitle.id == subtitle["id"],
                new_data={
                    "status": SubtitleStatus.IN_PROGRESS,
                    "start_date": datetime.datetime.now(),
                    "task_id": self.request.id,
                },
            )

            subtitle = SubtitleTasks.subtitle_mapper.to_dto(subtitle_entities[0])

            # CLEAN & OPTIMIZE AUTO IF NOT ALREADY
            start_trim, _ = SubtitleTasks.__optimize_audio(subtitle["id"], audio_path)

            # TRANSCRIBING
            model = whisper.load_model(WHISPER_MODAL)
            task = "translate" if subtitle["translate"] else "transcribe"
            result = model.transcribe(audio_path, fp16=False, word_timestamps=True, task=task)

            subtitle = SubtitleTasks.__update_subtitle_and_save_segments(
                subtitle["id"], result, start_trim_in_sec=start_trim / 1000
            )
        except Exception as err:
            print(type(err), err)
            subtitle = SubtitleTasks.__mark_as_failed(subtitle["id"])
            return SubtitleTasks.__send_failure_email(subtitle)

        # DELETE THE AUDIO
        delete_file(audio_path)

        # DELETE SUBTITLE TASK METADATA
        remove_subtitle_task_metadata(subtitle["id"])

        SubtitleTasks.__send_completion_email(subtitle)

    #
    #
    #

    # PRIVATE
    @staticmethod
    def __optimize_audio(subtitle_id: str, audio_path: str):
        metadata = get_subtitle_task_metadata(subtitle_id)
        opt_metadata = metadata.get("audio_optimization", {}) if metadata else {}

        try:
            # EXTRACT THE VOCALS
            if "vocals_extracting" not in opt_metadata:
                opt_metadata["vocals_extracting"] = extract_vocals(audio_path)

            vocals_audio_dir, vocals_audio_path = opt_metadata["vocals_extracting"]

            # REMOVE SILENCE
            if "silence_trimming" not in opt_metadata:
                trimmed_file_path = add_suffix_to_file_name(audio_path, "trimmed")
                opt_metadata["silence_trimming"] = trimmed_file_path, trim_silence(vocals_audio_path, trimmed_file_path)

            trimmed_file_path, (start_trim, end_trim) = opt_metadata["silence_trimming"]

            # REDUCE AUDIO SAMPLE RATE & MAKE IT SINGLE CHANNEL
            if "reduced" not in opt_metadata:
                (
                    ffmpeg.input(trimmed_file_path)
                    .output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar=16000)
                    .run(overwrite_output=True)
                )

                opt_metadata["reduced"] = True

            # CLEAR TMP FILES & DIRS
            delete_dir(vocals_audio_dir, only_if_empty=False)
            delete_file(trimmed_file_path)

            return start_trim, end_trim
        except Exception as err:
            raise err
        finally:
            # STORE SUBTITLE AUDIO METADATA
            set_subtitle_task_metadata(subtitle_id, {"audio_optimization": opt_metadata})

    #
    #

    @staticmethod
    def __update_subtitle_and_save_segments(subtitle_id: str, result: dict, start_trim_in_sec: float = 0):
        def cb(session: Session):
            subtitles = SubtitleTasks.subtitle_repo.update(
                filter=lambda Subtitle: Subtitle.id == subtitle_id,
                new_data={
                    "status": SubtitleStatus.COMPLETED,
                    "language": result["language"],
                    "finish_date": datetime.datetime.now(),
                    "task_id": None,
                },
                options={"session": session},
            )

            segments_data = []

            for segment in result["segments"]:
                segments_data.append(
                    {
                        "segment_id": segment["id"],
                        "subtitle_id": subtitle_id,
                        "start": segment["start"] + start_trim_in_sec,
                        "end": segment["end"] + start_trim_in_sec,
                        "text": segment["text"].strip(),
                    }
                )

            SubtitleTasks.segment_repo.create(segments_data, options={"session": session})

            return subtitles[0] if subtitles else None

        subtitle_entity = SubtitleTasks.subtitle_repo.start_transaction(callback=cb)

        return SubtitleTasks.subtitle_mapper.to_dto(subtitle_entity)

    #
    #

    @staticmethod
    def __mark_as_failed(subtitle_id: str):
        subtitles = SubtitleTasks.subtitle_repo.update(
            filter=lambda Subtitle: Subtitle.id == subtitle_id,
            new_data={
                "status": SubtitleStatus.FAILED,
                "start_date": None,
                "finish_date": None,
                "task_id": None,
            },
        )

        subtitle_entity = subtitles[0] if subtitles else None

        return SubtitleTasks.subtitle_mapper.to_dto(subtitle_entity)

    #
    #

    @staticmethod
    def __get_user(user_id: str):
        return SubtitleTasks.user_repo.find(
            filter=lambda User: User.id == user_id,
            options={"throw_if_not_found": True, "return_first": True},
        )

    @staticmethod
    def __send_completion_email(subtitle: SubtitleDTO):
        user = SubtitleTasks.__get_user(subtitle["user_id"])

        # PREPARE EMAIL TEMPLATE
        creation_date = to_datetime(subtitle["created_at"])
        start_date = to_datetime(subtitle["start_date"])
        finish_date = to_datetime(subtitle["finish_date"])

        email_template = render_template(
            "emails/subtitle_generation_completed.html",
            **{
                "user_name": f"{user.first_name} {user.last_name}",
                "subtitle_title": subtitle["title"],
                "creation_date": creation_date,
                "start_date": start_date,
                "finish_date": finish_date,
                "generation_time": get_duration(finish_date - start_date),
                "language": subtitle["language"],
                "subtitle_link": f"{CLIENT_HOST_URL}/subtitles/{subtitle["id"]}",
            },
        )

        # SEND EMAIL
        EmailTasks.send_email.apply_async(
            args=["Subtitle Generation Completed", [user.email]], kwargs={"html": email_template}
        )

    #
    #

    @staticmethod
    def __send_failure_email(subtitle: SubtitleDTO):
        user = SubtitleTasks.__get_user(subtitle["user_id"])

        # PREPARE EMAIL TEMPLATE
        email_template = render_template(
            "emails/subtitle_generation_failed.html",
            **{
                "user_name": f"{user.first_name} {user.last_name}",
                "subtitle_title": subtitle["title"],
                "creation_date": to_datetime(subtitle["created_at"]),
                "subtitle_link": f"{CLIENT_HOST_URL}/subtitles/{subtitle["id"]}",
            },
        )

        # SEND EMAIL
        EmailTasks.send_email.apply_async(args=["Subtitle Generation Failed", [user.email]], kwargs={"html": email_template})
