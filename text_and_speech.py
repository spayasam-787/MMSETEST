import speech_recognition as sr
from gtts import gTTS
import KEYS
import os
import time
import json
import simpleaudio as sa
from pydub import AudioSegment
from pydub.playback import play
import subprocess

# AudioSegment.converter = "C:\\Program Files\\ffmpeg-5.1.2-essentials_build\\bin\\ffmpeg.exe"
# AudioSegment.ffmpeg = "C:\\Program Files\\ffmpeg-5.1.2-essentials_build\\bin\\ffmpeg.exe"
# AudioSegment.ffprobe ="C:\\Program Files\\ffmpeg-5.1.2-essentials_build\\bin\\ffprobe.exe"

r = sr.Recognizer()
r.pause_threshold = 3

def convert_speech_to_text(model = "whisper"):
    """
    Captures audio from the microphone and returns the recognized text.
    """
    with sr.Microphone() as source:
        repeat = False
        # r.adjust_for_ambient_noise(source)
        while True:
            if repeat:
                time.sleep(0.5)
                convert_text_to_speech("Please answer again.")
                time.sleep(0.5)
            audio = r.listen(source, phrase_time_limit=10)
            try:
                if model == "google":
                    text = r.recognize_google(audio)
                    if text == "":
                        repeat = True
                        continue
                    return text
                elif model == "vosk":
                    text = r.recognize_vosk(audio)
                    text = json.loads(text)
                    if text['text'] == "":
                        repeat = True
                        continue
                    return text['text']
                elif model == "whisper":
                    text = str(r.recognize_whisper_api(audio, model='whisper-1' , api_key=KEYS.OPENAI_API_KEY))
                    print(text)
                    if len(text) < 3:
                        repeat = True
                        continue
                    # return text by removing \n at the end if present
                    return text[:-1] if text[-1] == "\n" else text
            except Exception as e:
                print(f"Error: {e}")
                

def convert_text_to_speech(text, lang='en'):
    """
    Converts the given text to speech and saves it as an audio file.
    Returns the filename of the saved audio.
    """
    tts = gTTS(text=text, lang=lang)
    filename = "output.mp3"
    tts.save(filename)
    play_audio(filename)

def play_audio(filename):
    """
    Plays the given audio file.
    """
    audio = AudioSegment.from_file(filename, format="mp3")  # assuming mp3, change format if needed
    play(audio)


if __name__ == "__main__":
    spoken_text = convert_speech_to_text()
    print(spoken_text)
    subprocess.call(["espeak", spoken_text])
