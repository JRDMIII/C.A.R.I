#!/usr/bin/env python3

import csv

# This module is what plays the voice assistants voice back to the user
import pyttsx3

# This module will be used to get the current date
import datetime

# This module is required for the microphone and speech recognition
import speech_recognition as sr

from googlesearch import search

import webbrowser

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

def return_time():
    time = str(datetime.datetime.now())
    hour = time[11:13]
    min = time[14:16]

    dateLine = ""
    with open("settings.csv", "r") as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if "date_format" in str(row):
                dateLine = str(row[0])
            else:
                pass

        format = dateLine[12:]
        isAfternoon = False
        if format == "12":
            hour = int(hour)
            if hour > 12:
                isAfternoon = True
                hour = hour - 12
                hour = str(hour)

    if format=="12":
        if isAfternoon:
            assistantVoice("It is " + hour + " " + min + "pm")
        elif not isAfternoon:
            assistantVoice("It is " + hour + " " + min + "am")

def set_hour_format(format):
    with open("settings.csv", "w") as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([("date_format=" + format)])

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
        rec.pause_threshold = 2
        audio = rec.listen(source)
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
        if "what is the date" in query:
            return_date()
        elif "what is the day" in query:
            return_day()
        elif " time" in query:
            if "set " in query:
                if "24" in query:
                    assistantVoice("Setting time to 24-hour format")
                    set_hour_format("24")
                if "12" in query:
                    assistantVoice("Setting time to 12-hour format")
                    set_hour_format("12")

            else:
                return_time()
        elif "search " in query:
            start = query.find("search ")
            query = query[start + 7:]
            print(query)
            assistantVoice("Looking for " + query)
            webbrowser.open(query)
        if "thank you" in query or "thanks" in query:
            assistantVoice("You're welcome")


process_query()
