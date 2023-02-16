#!/usr/bin/env python3
import time

import pyjokes

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

import application_database as db
import gestureRecognition as gr
import hardware as hd

def return_jokes():
    joke = pyjokes.get_joke(language="en", category="neutral")
    assistantVoice(joke)

def return_tasks():
    token = 'secret_L8AKRecNOCHoc0cC1hRehIek3F58MSMaO8z4JcRHi2v'

    database_id = 'fca0e258b64e46b6a56330bc04a73857'

    payload = {
        "filter": {"property": "Progress",
                   "multi_select": {
                       "contains": "In Progress"
                   }},
        "page_size": 100
    }
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    # This is the URL that will be used to get information on the database
    readURL = f"https://api.notion.com/v1/databases/{database_id}/query"

    # Notion API requires you to pass in the value get in order to retrieve information from a database
    res = requests.post(readURL, json=payload, headers=headers)
    # This is used to remove characters that are giving us errors and mistakes in outputs
    temp = res.text.replace("]", "")
    # This is used to split the long string into a list which can be searched through
    response = temp.split(",")
    if response == ['{"object":"list"', '"results":[', '"next_cursor":null', '"has_more":false', '"type":"page"', '"page":{}}']:
        return None
    else:
        assistantVoice("Your tasks are: ")
        time.sleep(0.1)
        for line in response:
            # This looks through each element of the list created to find the URLs then leaves just the name of the tasks
            if "url" in line:
                # This removes the extra part of the tasks from it so it will just show the name of the tasks
                assistantVoice(line[29:-35])
                time.sleep(0.3)

    return None

# This will return the current date
def return_date():
    # This uses the datetime module to collect information on the current date and weekday
    date = datetime.date.today()

    date = date.strftime("%B %d, %Y")
    return date

def return_weather():
    api_key = "fb18561cf37594bac1cc98d893bc4e22"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = "London"
    complete_url = base_url + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + city_name

    response = requests.get(complete_url)
    all_info = response.json()

    if all_info["cod"] != "404":

        main = all_info["main"]

        current_temp = round((main["temp"] - 273.15), 3)
        feels_like_temp = round((main["feels_like"] - 273.15), 3)

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

    # This returns the string equivalent of the day to the subroutine from which it was once called
    return day

def return_time():
    time = str(datetime.datetime.now())
    hour, mins = time[11:13], time[14:16]

    format = database.get_time_format()[0]
    # This if statement checks to see whether it is the afternoon or not
    isAfternoon = False
    if format == "12":
        hour = int(hour)
        if hour > 12:
            isAfternoon = True
            hour = str(hour - 12)

    # The embedded if statements here check to see what the format is in
    # settings and bases the output on those settings
    if format == "12":
        if isAfternoon:
            return str(hour), mins, " P M"
        elif not isAfternoon:
            return str(hour), mins, " A M"
    if format == "24":
        return str(hour), mins, ""

def return_search(query):
    # This is altering the string from the query in order to only get the search result back
    start = query.find("search ")
    query = query[start + 7:]

    # This gives an update message to the user while the search is being performed
    assistantVoice("Looking for " + query)

    # This creates a list of results which come from searching up the query on the user's preferred browser
    results = googlesearch.search(query, num=1)
    searches = []

    # This takes the first search from the list of results and opens the linkn on the web browser
    for i in results:
        searches.append(i)
        break

    search = searches[0]
    webbrowser.open(search)

def return_morn_prep():
    name = str(database.get_name())
    assistantVoice("Good Morning " + str(name) + ", hope you are feeling well!")

    hardware.deviceToggle("b", True)
    hardware.deviceToggle("p1", False)

    # This fetches all the values from the return subroutines and saves them to local variables
    hour, mins, format = return_time()
    day, date = return_day(), return_date()


    assistantVoice("It is " + hour + " " + mins + format)
    assistantVoice("Today is " + day + " " + date)
    return_weather()

    assistantVoice("Device energy usage:")
    time.sleep(0.1)
    assistantVoice(hardware.showEnergyUsage())

    return_tasks()
    assistantVoice("Hope you have a great day!")

def return_night_prep():
    name = str(database.get_name())[2:-3]
    assistantVoice("Good Evening " + str(name) + ", hope you are feeling well and ready to sleep!")

    hardware.deviceToggle("p1", True)

    # This fetches all the values from the return subroutines and saves them to local variables
    hour, mins, format = return_time()
    day, date = return_day(), return_date()

    assistantVoice("It is " + hour + " " + mins + format)
    assistantVoice("Today is " + day + " " + date)
    return_weather()

    hardware.deviceToggle("b", False)

    assistantVoice("The lights have been turned off and the fan is now on")
    time.sleep(0.1)
    assistantVoice("Make sure you have set all the alarms you need to!")
    time.sleep(0.1)
    assistantVoice("Have a very good night")



    # This is the sequence to make the light perform goodnight in morse code in a very soft light

    hardware.changeLightSettings(160, 0, 5, "invalid")

    hardware.deviceToggle("b", True)
    time.sleep(0.3)
    hardware.deviceToggle("b", False)
    time.sleep(0.05)
    hardware.deviceToggle("b", True)
    time.sleep(0.3)
    hardware.deviceToggle("b", False)
    time.sleep(0.05)
    hardware.deviceToggle("b", True)
    time.sleep(0.08)
    hardware.deviceToggle("b", False)
    time.sleep(0.8)
    hardware.deviceToggle("b", True)
    time.sleep(0.3)
    hardware.deviceToggle("b", False)
    time.sleep(0.05)
    hardware.deviceToggle("b", True)
    time.sleep(0.08)
    hardware.deviceToggle("b", False)


# This subroutine will produce the audio file which the voice assistant will play back
def assistantVoice(output):
    print("Person : ", output)
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
        # query = getAudio().lower()
        query = "hey assistant tell me a joke"
        if query == "None":
            break
        elif "assistant" in query:
            query = query.split(" and ")
            print(query)
            for request in query:
                if " joke" in request:
                    return_jokes()
                elif "what is the date" in request:
                    day = return_day()
                    date = return_date()
                    assistantVoice("Today is " + day + " " + date)
                elif "what is the day" in request:
                    assistantVoice("It is " + return_day() + " today")
                elif " time" in request:
                    if "set " in request or "change" in request:
                        if "24" in request:
                            assistantVoice("Setting time to 24-hour format")
                            database.set_time_format("24")
                        if "12" in request:
                            assistantVoice("Setting time to 12-hour format")
                            database.set_time_format("12")
                    else:
                        hour, mins, format = return_time()
                        assistantVoice("It is " + hour + " " + mins + format)
                elif "search " in request:
                    return_search(request)

                # === All of these are statements referring to the hardware === #
                elif "turn" in request or "switch" in request:
                    if "all" in request and "on" in request:
                        assistantVoice("Turning all devices on now")
                        hardware.allDevicesOn()
                    if "all" in request and "off" in request:
                        assistantVoice("Turning all devices off now")
                        hardware.allDevicesOff()
                    if "fan" in request or "plug one" in request:
                        assistantVoice("Toggling fan state now")
                        hardware.deviceToggle("p1", "toggle")
                    if "desk" in request or "plug two" in request:
                        assistantVoice("Toggling desk L.E.D. state now")
                        hardware.deviceToggle("p2", "toggle")
                    if "light" in request or "bulb" in request:
                        assistantVoice("Toggling room light state now")
                        hardware.deviceToggle("b", "toggle")
                elif "increase" in request:
                    if "saturation" in request:
                        assistantVoice(hardware.increaseSaturation())
                    else:
                        assistantVoice(hardware.increaseHue())
                elif "decrease" in request:
                    if "saturation" in request:
                        assistantVoice(hardware.decreaseSaturation())
                    else:
                        assistantVoice(hardware.decreaseHue())
                elif "energy usage" in request:
                    assistantVoice(hardware.showEnergyUsage())

                elif "thank you" in request or "thanks" in request:
                    assistantVoice("You're welcome")
                elif "get" in request or "prepare" in request:
                    if "morning" in request or "day" in request:
                        return_morn_prep()
                    if "night" in request or "sleep" in request or "bed" in request:
                        return_night_prep()
                elif "tell" in request or "give" in request:
                    if "tasks" in request:
                        return_tasks()
                elif "hand" in request:
                    if "gesture" in request or "signs" in request:
                        hand_gesture = -1
                        while hand_gesture == -1:
                            hand_gesture, not_found = gr.gestureRec()
                            if hand_gesture == 1:
                                hardware.deviceToggle("p1", "toggle")
                            elif hand_gesture == 2:
                                hardware.deviceToggle("p2", "toggle")
                            elif hand_gesture == 3:
                                hardware.deviceToggle("b", "toggle")
                            elif hand_gesture == 4:
                                hardware.allDevicesOn()
                            elif hand_gesture == 5:
                                hardware.allDevicesOff()

if __name__ == "__main__":
    database = db.database()
    engine = pyttsx3.init()
    hardware = hd.Hardware(database.get_plug1IP(), database.get_plug2IP(), database.get_bulbIP(), "damiolatunji4tj@gmail.com", "party39ta3")

    while True:
        process_query()
