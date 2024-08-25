from typing import List, Tuple
import io

from dtos.segment import SegmentDTO
from services.subtitle_file import SubtitleFileBase, SubtitleTxtFile, SubtitleSrtFile, SubtitleVttFile


class SubtitleFileCreator:
    def create(self, file_type: str, segments: List[SegmentDTO]) -> Tuple[io.BytesIO, str]:
        subtitle_file: SubtitleFileBase = None

        if file_type == "txt":
            subtitle_file = SubtitleTxtFile()
        elif file_type == "srt":
            subtitle_file = SubtitleSrtFile()
        elif file_type == "vtt":
            subtitle_file = SubtitleVttFile()
        else:
            raise Exception("unsupported subtitle file type")

        file, mimetype = subtitle_file.create(segments)

        return io.BytesIO(file.getvalue().encode("utf-8")), mimetype
