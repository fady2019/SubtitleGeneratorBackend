from dtos.dto import DTO


class SegmentDTO(DTO):
    segment_id: str
    subtitle_id: str
    text: str
    start: float
    end: float
