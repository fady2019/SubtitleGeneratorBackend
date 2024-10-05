from flask import render_template
from sqlalchemy.orm import Session
from celery import shared_task
from celery.app.task import Task
import whisper, os, datetime

from db.repositories.user import UserRepository
from db.repositories.subtitle import SubtitleRepository
from db.repositories.segment import SegmentRepository
from db.entities.subtitle import SubtitleStatus
from celery_tasks.emails import EmailTasks
from celery_tasks.subtitle_media_file import SubtitleMediaFileTasks
from dtos.subtitle import SubtitleDTO
from dtos_mappers.subtitle import SubtitleMapper
from helpers.date import to_datetime, get_duration
from helpers.celery import is_revoked, remove_revoked_task
from helpers.file import delete_dir


WHISPER_MODAL = os.getenv("WHISPER_MODAL")
CLIENT_HOST_URL = os.getenv("CLIENT_HOST_URL")


class SubtitleTasks:
    user_repo = UserRepository()
    subtitle_repo = SubtitleRepository()
    segment_repo = SegmentRepository()
    subtitle_mapper = SubtitleMapper()

    @staticmethod
    @shared_task(bind=True)
    def begin_subtitle_generation(self: Task, subtitle: SubtitleDTO, media_file_dir: str):
        if is_revoked(self.request.id):
            remove_revoked_task(self.request.id)
            raise Exception("revoked")

        try:
            # UPDATE SUBTITLE INIT STATE
            subtitle = SubtitleTasks.__update_subtitle_init_state(subtitle["id"], self.request.id)

            # CLEAN & OPTIMIZE MEDIA FILE IF NOT ALREADY
            audio_path, start_trim = SubtitleTasks.__optimize_audio(media_file_dir)
            start_trim_in_sec = start_trim / 1000.0

            # GENERATE THE TRANSCRIPTION
            transcript_result = SubtitleTasks.__transcribe(subtitle, audio_path)

            # SAVE THE SUBTITLE SEGMENTS IN DB
            subtitle = SubtitleTasks.__update_subtitle_and_save_segments(
                transcript_result, subtitle["id"], start_trim_in_sec
            )
        except:
            subtitle = SubtitleTasks.__mark_as_failed(subtitle["id"])
            return SubtitleTasks.__send_failure_email(subtitle)

        # DELETE THE AUDIOS
        delete_dir(media_file_dir, only_if_empty=False)

        SubtitleTasks.__send_completion_email(subtitle)

    #
    #
    #

    # PRIVATE
    @staticmethod
    def __update_subtitle_init_state(subtitle_id: str, task_id: str):
        subtitle_entities = SubtitleTasks.subtitle_repo.update(
            filter=lambda Subtitle: Subtitle.id == subtitle_id,
            new_data={
                "status": SubtitleStatus.IN_PROGRESS,
                "start_date": datetime.datetime.now(),
                "task_id": task_id,
            },
        )

        return SubtitleTasks.subtitle_mapper.to_dto(subtitle_entities[0])

    #
    #

    @staticmethod
    def __optimize_audio(media_file_dir: str):
        audio_path, start_trim = SubtitleMediaFileTasks.optimize_media_file(media_file_dir)
        return audio_path, start_trim

    #
    #

    @staticmethod
    def __transcribe(subtitle: SubtitleDTO, audio_path: str):
        # TRANSCRIBING
        model = whisper.load_model(WHISPER_MODAL)
        task = "translate" if subtitle["translate"] else "transcribe"
        return model.transcribe(audio_path, fp16=False, word_timestamps=True, task=task)

    #
    #

    @staticmethod
    def __update_subtitle_and_save_segments(transcript_result: dict, subtitle_id: str, start_trim_in_sec: float):
        def cb(session: Session):
            subtitles = SubtitleTasks.subtitle_repo.update(
                filter=lambda Subtitle: Subtitle.id == subtitle_id,
                new_data={
                    "status": SubtitleStatus.COMPLETED,
                    "language": transcript_result["language"],
                    "finish_date": datetime.datetime.now(),
                    "task_id": None,
                },
                options={"session": session},
            )

            segments_data = []

            for segment in transcript_result["segments"]:
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

    #
    #

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
