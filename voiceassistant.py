# STT/TTS algorithm

# These are the modules that will be installed into python

# This recognises and translates the incoming voice
import speech_recognition as sr

import pyaudio

# This is the module we will use to speak the text recieved
import pyttsx3

# Instantiating an obj of the recogniser class
rec = sr.Recognizer()

def speaktext(command):

    # Initialise the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# This is an infinite loop which will constantly look for the user speaking
while True:

    # to handle exceptions when the program begins
    # to un a try except loop is used here
    try:
        # Use the microphone selected as the source of input
        with sr.Microphone() as source2:
            # Adjusting the recogniser to ambient noise
            # The longer the duration the more noises it will
            #  be able to block out
            rec.adjust_for_ambient_noise(source2, duration=0.2)

            # Listens for user input
            audio2 = rec.listen(source2)

            # Using google to recognise audio
            MyText = rec.recognize_google(audio2)
            MyText = MyText.lower()

            print("Did you say" + MyText)
            speaktext(MyText)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Unkown Error Occured")
