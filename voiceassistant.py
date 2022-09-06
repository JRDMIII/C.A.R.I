#!/usr/bin/env python3

import time
import speech_recognition as sr
from gtts import gTTS
import os
import playsound as plays
import pyttsx3

# This module is required for the microphone
import pyaudio

# This subroutine will produce the audio file which the voice assistant will play back
num = 1
def assistantVoice(output):
    global num

    num += 1
    print("Person : ", output)

    engine = pyttsx3.init()
    engine.say(output)
    engine.runAndWait()

# This instantiates an object for recognising voices
rec = sr.Recognizer()
m = sr.Microphone()

def getAudio():
    with m as source:

        audio = rec.listen(source)

        try:
            text = rec.recognize_google(audio)
            print(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not get results from GSR service; {0}".format(e))

        # This list of if statements looks for keywords within the audio being received to decide the correct output
        if "play" in text:
            assistantVoice("i think you want me to play something?")

        if "code" in text:
            assistantVoice("i think you want me to code something?")

        if "homework" in text:
            assistantVoice("Do you want me to show you your homework?")
