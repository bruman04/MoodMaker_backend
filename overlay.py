from moviepy.editor import *
from flask import session
from s3_helper import upload
import io
import tempfile

def audio_overlay(video, audio):
    print("audio_overlay start")
    rawAudio = AudioFileClip(audio)
    rawVideo = VideoFileClip(video)

    rawAudio = rawAudio.volumex(0.5)
    rawAudio = rawAudio.audio_loop(duration=rawVideo.duration)

    originalAudio = rawVideo.audio

    #merge both audio
    newAudio = CompositeAudioClip([originalAudio, rawAudio])

    finalVid = rawVideo.set_audio(newAudio)

    #temp file for storing output vid
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as output_video_file:
        output_video_path = output_video_file.name

    # finalVid.write_videofile(new_filename, fps=60)
    finalVid.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

    return output_video_path
