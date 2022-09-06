#!/usr/bin/env python3

import time
import speech_recognition as sr
from gtts import gTTS
import os
import playsound as plays
import pyttsx3

# This module is required for the microphone
import pyaudio

def commandCheck(audioInput):
    # This list of if statements looks for keywords within the audio being received to decide the correct output
    if "hello" in audioInput:
        assistantVoice("i think you want me to play something?")

    if "play" in audioInput:
        assistantVoice("i think you want me to play something?")

    if "code" in audioInput:
        assistantVoice("i think you want me to code something?")

    if "homework" in audioInput:
        assistantVoice("Do you want me to show you your homework?")

# This subroutine will produce the audio file which the voice assistant will play back
num = 1
def assistantVoice(output):
    global num

    num += 1
    print("Person : ", output)

    engine = pyttsx3.init()
    engine.say(output)
    engine.runAndWait()


# This subroutine is used to
def getAudio():
    # This instantiates an object for recognising voices
    rec = sr.Recognizer()
    m = sr.Microphone()

    with m as source:

        # This begins recording audio coming from our mic source
        print("Speak...")
        audio = rec.listen(source, phrase_time_limit=7)
        print("Stop.")

        try:
            text = rec.recognize_google(audio, language='en-US')
            print("You : ", text)
            return text
        except:
            print("Google Speech Recognition could not understand audio")

while True:
    getAudio()
