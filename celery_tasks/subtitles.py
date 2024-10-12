from flask import render_template
from sqlalchemy.orm import Session
from celery import shared_task
from celery.app.task import Task
from polyglot.text import Text, Sentence
import whisper, os, datetime, math

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
    def __divide_sentence(sentence: Sentence, max_len_per_sentence: int = 150):
        words = [word.strip() for word in sentence.split(sep=" ")]

        # MAKING SURE THAT max_len_per_sentence NOT LESS THAN THE LENGTH OF THE LONGEST WORD
        max_len_per_sentence = max(max_len_per_sentence, max(len(word) for word in words))

        # FINDING THE BALANCED SENTENCE LENGTH
        chars_count = len(sentence)
        min_sentences_count = int(math.ceil(chars_count / max_len_per_sentence))
        balanced_sentence_len = int(math.ceil(chars_count / min_sentences_count))

        sub_sentence_word_list = [[[], 0]]

        for idx, word in enumerate(words):
            first_word = len(sub_sentence_word_list[-1][0]) == 0
            chars_count = len(word) + (0 if first_word else 1)

            if idx != len(words) - 1 and sub_sentence_word_list[-1][1] + chars_count > balanced_sentence_len:
                sub_sentence_word_list.append([[], 0])

            sub_sentence_word_list[-1][0].append(word)
            sub_sentence_word_list[-1][1] += chars_count

        return [(" ".join(sentence_words), len(sentence_words)) for (sentence_words, _) in sub_sentence_word_list]

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

            # EXTRACT EACH WORD WITH ITS START & END TIME
            words: list[tuple[str, float, float]] = []  # word, start_time, end_time

            for segment in transcript_result["segments"]:
                for word_info in segment["words"]:
                    word: str = word_info["word"].strip()
                    words.append((word, word_info["start"], word_info["end"]))

            # DIVIDE THE TEXT INTO SMALL SENTENCES (SEGMENTS)
            text = Text(transcript_result["text"])
            sentences: list[Sentence] = text.sentences
            segments_data = []
            word_idx = 0

            for sentence in sentences:
                for sub_sentence, words_count in SubtitleTasks.__divide_sentence(sentence):
                    _, start_time, _ = words[word_idx]
                    _, _, end_time = words[word_idx + words_count - 1]

                    segments_data.append(
                        {
                            "segment_id": len(segments_data),
                            "subtitle_id": subtitle_id,
                            "start": start_time + start_trim_in_sec,
                            "end": end_time + start_trim_in_sec,
                            "text": sub_sentence,
                        }
                    )

                    word_idx += words_count

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
