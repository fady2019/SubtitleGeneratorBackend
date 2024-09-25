from pydub import AudioSegment
from demucs import separate
import shlex, os

from helpers.file import get_file_name

DEMUSC_OUT_DIR = os.getenv("DEMUSC_OUT_DIR", "tmp/demucs")
DEMUSC_MODAL_NAME = os.getenv("DEMUSC_MODAL_NAME", "mdx_extra")
DEMUSC_STEM_NAME = os.getenv("DEMUSC_STEM_NAME", "vocals")


def extract_vocals(audio_path: str):
    audio_file_name = get_file_name(audio_path)
    command = f"-o {DEMUSC_OUT_DIR} -n {DEMUSC_MODAL_NAME} --two-stems {DEMUSC_STEM_NAME} {audio_path}"
    separate.main(shlex.split(command))

    out_path = os.path.join(DEMUSC_OUT_DIR, DEMUSC_MODAL_NAME, audio_file_name)
    vocals_audio_path = os.path.join(out_path, f"{DEMUSC_STEM_NAME}.wav")

    return out_path, vocals_audio_path


def milliseconds_until_sound_forward(sound: AudioSegment, silence_threshold, chunk_size):
    # MAKING SURE THAT chunk_size IS GREATER THAN ZERO
    assert chunk_size > 0

    frame = 0

    while frame < len(sound) and sound[frame : frame + chunk_size].max_dBFS < silence_threshold:
        frame += chunk_size

    return frame


def milliseconds_until_sound_backward(sound: AudioSegment, silence_threshold, chunk_size):
    # MAKING SURE THAT chunk_size IS GREATER THAN ZERO
    assert chunk_size > 0

    frame = len(sound) - chunk_size

    while frame >= 0 and sound[frame : frame + chunk_size].max_dBFS < silence_threshold:
        frame -= chunk_size

    return frame + chunk_size


def trim_silence(audio_path, output_path, output_format="wav", silence_threshold=-30.0, chunk_size=10):
    audio: AudioSegment = AudioSegment.from_file(audio_path, format="wav")
    start_trim = milliseconds_until_sound_forward(audio, silence_threshold, chunk_size)
    end_trim = milliseconds_until_sound_backward(audio, silence_threshold, chunk_size)
    trimmed = audio[start_trim:end_trim]
    trimmed.export(output_path, format=output_format)
    return start_trim, end_trim
