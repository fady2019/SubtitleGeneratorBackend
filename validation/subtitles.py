from voluptuous import Schema, All, Optional, ALLOW_EXTRA

from validation.shared import validator_executor
from validation.validators import (
    required,
    valid_file,
    valid_string,
    valid_uuid,
    valid_bool,
    subtitle_title_validator,
    not_empty,
    valid_int,
    in_list,
)


SubtileIdSchema = Schema(
    {required("subtitle_id", "subtitle id"): All(valid_string("subtitle id"), valid_uuid("subtitle id"))}, extra=ALLOW_EXTRA
)

SubtitleMediaFileSchema = Schema(
    {required("media_file", "media file"): valid_file("media file", supported_mimetypes=["audio/*", "video/*"])}
)

GenerateSubtileSchema = Schema(
    {
        required("title", "title"): subtitle_title_validator("title"),
        Optional("translate"): valid_bool("translate"),
    }
)

EditSubtitleSchema = Schema({Optional("title"): subtitle_title_validator("title")})

SubtileSegmentIdSchema = Schema({required("segment_id", "segment id"): valid_int("segment id")}, extra=ALLOW_EXTRA)

EditSubtitleSegmentSchema = Schema({Optional("text"): All(valid_string("text"), not_empty("text"))})

SubtitleFileTypeSchema = Schema(
    {required("file_type", "file type"): All(valid_string("file type"), in_list("file type", list=["srt", "txt", "vtt"]))}
)


def subtitle_begin_generation_media_file_validator(data):
    validator_executor(SubtitleMediaFileSchema, data)


def subtitle_begin_generation_validator(data):
    validator_executor(GenerateSubtileSchema, data)


def subtitle_id_validator(data):
    validator_executor(SubtileIdSchema, data)


def edit_subtitle_validator(data):
    validator_executor(EditSubtitleSchema, data)


def subtitle_segment_id_validator(data):
    validator_executor(SubtileSegmentIdSchema, data)


def edit_subtitle_segment_validator(data):
    validator_executor(EditSubtitleSegmentSchema, data)


def subtitle_file_type_validator(data):
    validator_executor(SubtitleFileTypeSchema, data)
