#!/usr/bin/env python3

import time
import speech_recognition as sr
from gtts import gTTS
import os
import playsound as plays

# This module is required for the microphone
import pyaudio

# This subroutine will produce the audio file which the voice assistant will play back
num = 1
def assistantVoice(output):
    global num

    num += 1
    print("Person : ", output)

    toBeSaid = gTTS(text=output, lang='en', slow=False)
    # This is where we save the audio file given by gtts
    file = str(num)+".mp3"
    toBeSaid.save("welcome.mp3")

    # This uses the playsound module to play the audio file
    os.system("mpg321 welcome.mp3")
    os.remove(file)

rec = sr.Recognizer()
m = sr.Microphone()
while True:
    with m as source:

        audio = rec.listen(source)

        try:
            text = rec.recognize_google(audio)
            assistantVoice(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not get results from GSR service; {0}".format(e))
