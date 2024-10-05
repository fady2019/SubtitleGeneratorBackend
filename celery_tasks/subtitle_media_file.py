from celery import shared_task
import os, ffmpeg

from helpers.audio import extract_vocals, get_audio_duration
from helpers.file import delete_file


MEDIA_FILE_NAME = os.getenv("MEDIA_FILE_NAME")
AUDIO_FILE_NAME = os.getenv("AUDIO_FILE_NAME")
TRIMMED_AUDIO_FILE_NAME = os.getenv("TRIMMED_AUDIO_FILE_NAME")
OPTIMIZED_AUDIO_FILE_NAME = os.getenv("OPTIMIZED_AUDIO_FILE_NAME")


class SubtitleMediaFileTasks:
    @staticmethod
    @shared_task
    def optimize_media_file(media_file_dir: str):
        media_file_path = os.path.join(media_file_dir, MEDIA_FILE_NAME)
        audio_file_path = os.path.join(media_file_dir, AUDIO_FILE_NAME)
        trimmed_audio_file_path = os.path.join(media_file_dir, TRIMMED_AUDIO_FILE_NAME)
        optimized_audio_file_path = os.path.join(media_file_dir, OPTIMIZED_AUDIO_FILE_NAME)

        try:
            # COVERT MEDIA FILE TO AUDIO
            SubtitleMediaFileTasks.__convert_media_file_to_audio(media_file_path, audio_file_path)

            _, vocals_audio_path = extract_vocals(audio_file_path, media_file_dir)

            # REMOVE SILENCE
            SubtitleMediaFileTasks.__remove_silence(vocals_audio_path, trimmed_audio_file_path)
            start_trim = get_audio_duration(audio_file_path) - get_audio_duration(trimmed_audio_file_path)

            # REDUCE AUDIO SAMPLE RATE
            SubtitleMediaFileTasks.__reduce_audio_simple_rate(trimmed_audio_file_path, optimized_audio_file_path)

            return optimized_audio_file_path, start_trim
        except Exception as err:
            raise err

    #
    #
    #

    # PRIVATE
    def __convert_media_file_to_audio(input_path: str, output_path: str):
        try:
            if not os.path.exists(output_path):
                ffmpeg.input(input_path).output(output_path, format="flac", acodec="flac", ar=44100, af="afftdn").run()
        except:
            delete_file(output_path)

    #
    #

    def __remove_silence(input_path: str, output_path: str):
        try:
            if not os.path.exists(output_path):
                ffmpeg.input(input_path).output(output_path, format="flac", af="silenceremove=1:0:-40dB").run()
        except:
            delete_file(output_path)

    #
    #

    def __reduce_audio_simple_rate(input_path: str, output_path: str):
        try:
            if not os.path.exists(output_path):
                silence_duration = 1  # 1 sec
                silent_audio = ffmpeg.input("anullsrc=r=44100:cl=stereo", f="lavfi", t=silence_duration)
                original_audio = ffmpeg.input(input_path)

                ffmpeg.concat(silent_audio, original_audio, v=0, a=1).output(output_path, format="flac", ar=16000).run()
        except:
            delete_file(output_path)
