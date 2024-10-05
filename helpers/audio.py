from pydub import AudioSegment
from demucs import separate
import shlex, os

from helpers.file import create_file

DEMUCS_OUT_DIR_NAME = os.getenv("DEMUCS_OUT_DIR_NAME", "source_separation")
DEMUCS_CHUNKS_OUT_DIR_NAME = os.getenv("DEMUCS_CHUNKS_OUT_DIR_NAME", "chunks")
DEMUCS_VOCALS_FILE_NAME = os.getenv("DEMUCS_VOCALS_FILE_NAME", "vocals")
DEMUCS_MODAL_NAME = os.getenv("DEMUCS_MODAL_NAME", "htdemucs")
DEMUCS_STEM_NAME = os.getenv("DEMUCS_STEM_NAME", "vocals")


def extract_vocals(audio_path: str, out_dir: str, only_if_not_exist: bool = True, chunk_size_ms: int = 180000):
    assert chunk_size_ms > 0

    audio: AudioSegment = AudioSegment.from_file(audio_path)
    vocals_audio = AudioSegment.empty()

    main_out_dir = create_file(os.path.join(out_dir, DEMUCS_OUT_DIR_NAME))
    chunks_dir = create_file(os.path.join(main_out_dir, DEMUCS_CHUNKS_OUT_DIR_NAME))
    vocals_audio_path = os.path.join(main_out_dir, DEMUCS_VOCALS_FILE_NAME)

    if only_if_not_exist and os.path.exists(vocals_audio_path):
        return main_out_dir, vocals_audio_path

    for idx, chunk_start in enumerate(range(0, len(audio), chunk_size_ms)):
        chunk_path = os.path.join(chunks_dir, str(idx))

        if not os.path.exists(chunk_path):
            chunk = audio[chunk_start : chunk_start + chunk_size_ms]
            chunk.export(chunk_path, format="flac")

        chunk_demucs_out_dir = os.path.join(main_out_dir, DEMUCS_MODAL_NAME, str(idx))
        chunk_vocals_audio_path = os.path.join(chunk_demucs_out_dir, f"{DEMUCS_STEM_NAME}.flac")

        if not os.path.exists(chunk_vocals_audio_path):
            command = f"--flac -o {main_out_dir} -n {DEMUCS_MODAL_NAME} --two-stems {DEMUCS_STEM_NAME} {chunk_path}"
            separate.main(shlex.split(command))

        vocals_audio += AudioSegment.from_file(chunk_vocals_audio_path)

    vocals_audio.export(vocals_audio_path, format="flac")

    return main_out_dir, vocals_audio_path


def get_audio_duration(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return len(audio)
