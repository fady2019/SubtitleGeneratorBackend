from typing import TypedDict, Optional


class TSubtitleAudioOptMetadata(TypedDict):
    vocals_extracting: Optional[tuple[str, str]]  # vocals_audio_dir, vocals_audio_path
    silence_trimming: Optional[tuple[str, tuple[float, float]]]  # trimmed_file_path, [start_trim, end_trim]
    reduced: Optional[bool]


class TSubtitleTaskMetadata(TypedDict):
    audio_optimization: Optional[TSubtitleAudioOptMetadata]
