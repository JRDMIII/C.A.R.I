#!/usr/bin/env python3

# This module is what plays the voice assistants voice back to the user
import pyttsx3

# This module will be used to get the current date
import datetime

# This module is required for the microphone and speech recognition
import speech_recognition as sr

# This will return the current date
def return_date():
    date = datetime.date.today()
    today = datetime.datetime.today().weekday() + 1

    days = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}

    if today in days.keys():
        day = str(days[today])

    d1 = date.strftime("%B %d, %Y")
    assistantVoice(day + " " + d1)

def return_day():
    today = datetime.datetime.today().weekday() + 1

    days = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}

    if today in days.keys():
        day = str(days[today])

    assistantVoice(day)


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
        rec.pause_threshold = 1.2
        audio = rec.listen(source, phrase_time_limit=7)
        print("Stopped Listening")

        try:
            text = rec.recognize_google(audio, language='en-US')
            print("You : ", text)
        except:
            print("Google Speech Recognition could not understand audio")
            return "None"

    return text

def process_query():

    # This makes sure that queries will be constantly processed
    while True:
        query = getAudio().lower()
        if " date" in query:
            return_date()
        if " day" in query:
            return_day()

process_query()
