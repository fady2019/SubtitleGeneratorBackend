from dtos.dto import DTO


class SegmentDTO(DTO):
    segment_id: int
    subtitle_id: str
    text: str
    start: float
    end: float
