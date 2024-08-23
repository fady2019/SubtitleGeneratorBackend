from voluptuous import Schema, All, Optional

from validation.shared import validator_executor
from validation.validators import required, valid_file, valid_string, valid_uuid, subtitle_title_validator


SubtileIdSchema = Schema(
    {required("subtitle_id", "subtitle id"): All(valid_string("subtitle id"), valid_uuid("subtitle id"))}
)

SubtitleAudioSchema = Schema({required("audio", "audio"): valid_file("audio", supported_mimetypes=["audio/*"])})

SubtileTitleSchema = Schema({required("title", "title"): subtitle_title_validator("title")})

EditSubtitleSchema = Schema({Optional("title"): subtitle_title_validator("title")})


def subtitle_begin_generation_audio_validator(data):
    validator_executor(SubtitleAudioSchema, data)


def subtitle_begin_generation_title_validator(data):
    validator_executor(SubtileTitleSchema, data)


def subtitle_id_validator(data):
    validator_executor(SubtileIdSchema, data)


def edit_subtitle_validator(data):
    validator_executor(EditSubtitleSchema, data)
