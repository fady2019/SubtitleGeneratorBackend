from voluptuous import Schema, All, Optional, ALLOW_EXTRA

from validation.shared import validator_executor
from validation.validators import (
    required,
    valid_file,
    valid_string,
    valid_uuid,
    subtitle_title_validator,
    not_empty,
    valid_int,
)


SubtileIdSchema = Schema(
    {required("subtitle_id", "subtitle id"): All(valid_string("subtitle id"), valid_uuid("subtitle id"))}, extra=ALLOW_EXTRA
)

SubtitleAudioSchema = Schema({required("audio", "audio"): valid_file("audio", supported_mimetypes=["audio/*"])})

SubtileTitleSchema = Schema({required("title", "title"): subtitle_title_validator("title")})

EditSubtitleSchema = Schema({Optional("title"): subtitle_title_validator("title")})

SubtileSegmentIdSchema = Schema({required("segment_id", "segment id"): valid_int("segment id")}, extra=ALLOW_EXTRA)

EditSubtitleSegmentSchema = Schema({Optional("text"): All(valid_string("text"), not_empty("text"))})


def subtitle_begin_generation_audio_validator(data):
    validator_executor(SubtitleAudioSchema, data)


def subtitle_begin_generation_title_validator(data):
    validator_executor(SubtileTitleSchema, data)


def subtitle_id_validator(data):
    validator_executor(SubtileIdSchema, data)


def edit_subtitle_validator(data):
    validator_executor(EditSubtitleSchema, data)


def subtitle_segment_id_validator(data):
    validator_executor(SubtileSegmentIdSchema, data)


def edit_subtitle_segment_validator(data):
    validator_executor(EditSubtitleSegmentSchema, data)
