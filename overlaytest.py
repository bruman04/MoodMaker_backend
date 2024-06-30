from moviepy.editor import *

rawAudio = AudioFileClip("testVideoAudio/testAud.mp3")
rawVideo = VideoFileClip("testVideoAudio/testVid.mp4")

rawAudio = rawAudio.volumex(0.5)
rawAudio = rawAudio.audio_loop(duration=rawVideo.duration)

originalAudio = rawVideo.audio

#merge both audio
newAudio = CompositeAudioClip([originalAudio, rawAudio])


finalVid = rawVideo.set_audio(newAudio)
finalVid.write_videofile("testVideoAudio/processedVideo_2.mp4", fps=60)



