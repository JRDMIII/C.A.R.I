#!/usr/bin/env python3

import csv

# This module is what plays the voice assistants voice back to the user
import pyttsx3

# This module will be used to get the current date
import datetime

# This module is required for the microphone and speech recognition
import speech_recognition as sr

# This will be the module that will be used to search for
import googlesearch

import webbrowser

import requests

def get_name():
    with open("settings.csv", "r") as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            for field in row:
                if "name=" in field:
                    start = field.find("=")
                    start += 1
                    name = field[start:]
                else:
                    pass
    return name

# This will return the current date
def return_date():
    # This uses the datetime module to collect information on the current date and weekday
    date = datetime.date.today()
    today = datetime.datetime.today().weekday() + 1

    # This is a dictionary used to change the numerical value of today to the actual day
    days = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}

    # This checks to see which element of the dictionary matches the value of "today"
    if today in days.keys():
        day = str(days[today])

    d1 = date.strftime("%B %d, %Y")
    assistantVoice("Today is " + day + " " + d1)

def return_weather():
    api_key = "fb18561cf37594bac1cc98d893bc4e22"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = "London"
    complete_url = base_url + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + city_name

    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":

        all_info = x
        main = all_info["main"]

        current_temp_k = main["temp"]
        current_temp = round((current_temp_k - 273.15), 3)
        feels_like_temp_k = main["feels_like"]
        feels_like_temp = round((feels_like_temp_k - 273.15), 3)

        weather = all_info["weather"]

        weather_desc = weather[0]["description"]
        overall_weather_desc = weather[0]["main"]

        complete_script=(
            "The current temperature is " +
            str(current_temp) + " degrees celcius and it will feel like " +
            str(feels_like_temp)+ " degrees celcius. The current weather mentioned is " +
            overall_weather_desc + ", specifically stating "+
            weather_desc
        )

        assistantVoice(complete_script)

    else:
        print(" City Not Found ")

def return_day():
    # This uses the datetime module to find out what the current day is
    today = datetime.datetime.today().weekday() + 1

    # This is a dictionary used to change the numerical value of today to the actual day
    days = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}

    # This checks to see which element of the dictionary matches the value of "today"
    if today in days.keys():
        day = str(days[today])
    else:
        return None

    # This parses the day to the assistant voice subroutine to be spoken
    assistantVoice("It is " + day + " today")

def return_time():
    print("processing request")
    time = str(datetime.datetime.now())
    hour = time[11:13]
    mins = time[14:16]

    # This is opening the settings file and extracting the specific setting for the format of the time
    timeSetting = ""
    with open("settings.csv", "r") as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if "date_format" in str(row):
                timeSetting = str(row[0])
            else:
                pass

    format = timeSetting[12:]
    # This if statement checks to see whether it is the afternoon or not
    isAfternoon = False
    if format == "12":
        hour = int(hour)
        print(hour)
        if hour > 12:
            isAfternoon = True
            hour = hour - 12
            print(hour)
            hour = str(hour)

    # The embedded if statements here check to see what the format is in
    # settings and bases the output on those settings
    if format == "12":
        if isAfternoon:
            assistantVoice("It is " + str(hour) + " " + mins + "pm")
        elif not isAfternoon:
            assistantVoice("It is " + str(hour) + " " + mins + "am")
    if format == "24":
        assistantVoice("It is " + str(hour) + " " + mins)

def return_search(query):
    start = query.find("search ")
    query = query[start + 7:]
    assistantVoice("Looking for " + query)
    results = googlesearch.search(query, num=1)
    searches = []
    for i in results:
        searches.append(i)
        break

    search = searches[0]
    webbrowser.open(search)

def set_hour_format(format):
    settings = []
    with open("settings.csv", "r") as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            try:
                settings.append(row[0])
            except:
                pass

    print(settings)

    for setting in settings:
        if "date_format" in setting:
            settings.remove(setting)
            print(settings)
        else:
            pass

    settings.append(("date_format="+format))
    print(settings)

    with open("settings.csv", "w") as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(settings)

def return_morn_prep():
    name = get_name()
    assistantVoice("Good Morning " + str(name) + ", hope you are feeling well!")

    # This uses the datetime module to collect information on the current date and weekday
    date = datetime.date.today()
    today = datetime.datetime.today().weekday() + 1
    # This is a dictionary used to change the numerical value of today to the actual day
    days = {1: 'Monday', 2: 'Tuesday',
            3: 'Wednesday', 4: 'Thursday',
            5: 'Friday', 6: 'Saturday',
            7: 'Sunday'}
    # This checks to see which element of the dictionary matches the value of "today"
    if today in days.keys():
        day = str(days[today])
    d1 = date.strftime("%B %d, %Y")
    assistantVoice("Today is " + day + " " + d1)
    return_weather()

# This subroutine will produce the audio file which the voice assistant will play back
def assistantVoice(output):
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
        rec.pause_threshold = 1
        audio = rec.listen(source)

        try:
            text = rec.recognize_google(audio, language='en-US')
            print("You : ", text)
        except:
            return "None"
    return text

def process_query():
    # This makes sure that queries will be constantly processed
    while True:
        query = getAudio().lower()
        if "assistant" in query:
            if "what is the date" in query:
                return_date()
            elif "what is the day" in query:
                return_day()
            elif " time" in query:
                if "set " in query or "change" in query:
                    if "24" in query:
                        assistantVoice("Setting time to 24-hour format")
                        set_hour_format("24")
                    if "12" in query:
                        assistantVoice("Setting time to 12-hour format")
                        set_hour_format("12")
                else:
                    print("telling time")
                    return_time()
            elif "search " in query:
                return_search(query)
            elif "thank you" in query or "thanks" in query:
                assistantVoice("You're welcome")
            elif "get" in query or "prepare" in query:
                if "morning" in query or "day" in query:
                    return_morn_prep()


process_query()
