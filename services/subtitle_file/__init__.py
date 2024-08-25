from abc import ABC, abstractmethod
from typing import List, Tuple
import io

from dtos.segment import SegmentDTO


class SubtitleFileBase(ABC):
    @abstractmethod
    def create(self, segments: List[SegmentDTO]) -> Tuple[io.IOBase, str]:
        pass


class TimeBasedSubtitleFileBase(SubtitleFileBase):
    def time_units(self, seconds: float):
        hrs, rem = divmod(seconds, 3600)
        mins, secs = divmod(rem, 60)
        millisecs = int((secs % 1) * 1000)
        return hrs, mins, secs, millisecs


class SubtitleTxtFile(SubtitleFileBase):
    def create(self, segments: List[SegmentDTO]):
        content = "\n".join([segment["text"] for segment in segments])
        return io.StringIO(content), "text/plain"


class SubtitleSrtFile(TimeBasedSubtitleFileBase):
    def create(self, segments: List[SegmentDTO]):
        content = ""

        for segment in segments:
            content += f"{str(segment["segment_id"] + 1)}\n"
            content += f"{self.format_time(segment['start'])} --> {self.format_time(segment['end'])}\n"
            content += f"{segment['text']}\n\n"

        return io.StringIO(content), "application/x-subrip"

    def format_time(self, seconds: float):
        hrs, mins, secs, millisecs = self.time_units(seconds)
        return f"{int(hrs):02}:{int(mins):02}:{int(secs):02},{millisecs:03}"


class SubtitleVttFile(TimeBasedSubtitleFileBase):
    def create(self, segments: List[SegmentDTO]):
        content = "WEBVTT\n\n"

        for segment in segments:
            content += f"{self.format_time(segment['start'])} --> {self.format_time(segment['end'])}\n"
            content += f"{segment['text']}\n\n"

        return io.StringIO(content), "text/vtt"

    def format_time(self, seconds: float):
        hrs, mins, secs, millisecs = self.time_units(seconds)
        return f"{int(hrs):02}:{int(mins):02}:{int(secs):02}.{millisecs:03}"
