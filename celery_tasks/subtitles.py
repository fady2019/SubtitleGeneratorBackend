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
from dtos.subtitle import SubtitleDTO
from dtos_mappers.subtitle import SubtitleMapper
from helpers.date import to_datetime, get_duration


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
        try:
            # SAVE THE TASK_ID IN THE SUBTITLE RECORD
            # IT'S REQUIRED TO TERMINATE THE TASK (IF THE USER WANTS TO)
            SubtitleTasks.subtitle_repo.update(
                filter=lambda Subtitle: Subtitle.id == subtitle["id"], new_data={"task_id": self.request.id}
            )

            # TRANSCRIBING
            model = whisper.load_model(WHISPER_MODAL)
            result = model.transcribe(audio_path, fp16=False, word_timestamps=False)

            subtitle = SubtitleTasks.__update_subtitle_and_save_segments(subtitle["id"], result)
        except Exception as err:
            print(type(err), err)
            subtitle = SubtitleTasks.__mark_as_failed(subtitle["id"])
            return SubtitleTasks.__send_failure_email(subtitle)

        # DELETE THE AUDIO
        if os.path.exists(audio_path):
            os.remove(audio_path)

        SubtitleTasks.__send_completion_email(subtitle)

    #
    #
    #

    # PRIVATE
    @staticmethod
    def __update_subtitle_and_save_segments(subtitle_id: str, result: dict):
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
                        "start": segment["start"],
                        "end": segment["end"],
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
                "finish_date": datetime.datetime.now(),
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
        start_date = to_datetime(subtitle["start_date"])
        finish_date = to_datetime(subtitle["finish_date"])

        email_template = render_template(
            "emails/subtitle_generation_completed.html",
            **{
                "user_name": f"{user.first_name} {user.last_name}",
                "subtitle_title": subtitle["title"],
                "start_date": start_date,
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
                "start_date": to_datetime(subtitle["start_date"]),
                "subtitle_link": f"{CLIENT_HOST_URL}/subtitles/{subtitle["id"]}",
            },
        )

        # SEND EMAIL
        EmailTasks.send_email.apply_async(args=["Subtitle Generation Failed", [user.email]], kwargs={"html": email_template})
