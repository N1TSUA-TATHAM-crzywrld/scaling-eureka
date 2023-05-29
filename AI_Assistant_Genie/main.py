import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from pprint import pprint
import pyttsx3
from decouple import config
from datetime import datetime
import speech_recognition as sr
from random import choice
from utils import opening_text

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def Speak(text):
    engine.say(text)
    engine.runAndWait()

def Greetings():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 11):
        Speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        Speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        Speak(f"Good Evening {USERNAME}")
    Speak(f"I am {BOTNAME}. How may I assist you?")

def Listen_For_User():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            Speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                Speak("Good night, take care!")
            else:
                Speak('Have a good day!')
            exit()
    except Exception:
        Speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query


if __name__ == '__main__':
    Greetings()
    while True:
        query = Listen_For_User().lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            Speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            Speak('What do you want to search on Wikipedia, sir?')
            search_query = Listen_For_User().lower()
            results = search_on_wikipedia(search_query)
            Speak(f"According to Wikipedia, {results}")
            Speak("For your convenience, I am printing it on the screen sir.")
            print(results)

        elif 'youtube' in query:
            Speak('What do you want to play on Youtube, sir?')
            video = Listen_For_User().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            Speak('What do you want to search on Google, sir?')
            query = Listen_For_User().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            Speak('On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            Speak("What is the message sir?")
            message = Listen_For_User().lower()
            send_whatsapp_message(number, message)
            Speak("I've sent the message sir.")

        elif "send an email" in query:
            Speak("On what email address do I send sir? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            Speak("What should be the subject sir?")
            subject = Listen_For_User().capitalize()
            Speak("What is the message sir?")
            message = Listen_For_User().capitalize()
            if send_email(receiver_address, subject, message):
                Speak("I've sent the email sir.")
            else:
                Speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

        elif 'joke' in query:
            Speak(f"Hope you like this one sir")
            joke = get_random_joke()
            Speak(joke)
            Speak("For your convenience, I am printing it on the screen sir.")
            pprint(joke)

        elif "advice" in query:
            Speak(f"Here's an advice for you, sir")
            advice = get_random_advice()
            Speak(advice)
            Speak("For your convenience, I am printing it on the screen sir.")
            pprint(advice)

        elif "trending movies" in query:
            Speak(f"Some of the trending movies are: {get_trending_movies()}")
            Speak("For your convenience, I am printing it on the screen sir.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            Speak(f"I'm reading out the latest news headlines, sir")
            Speak(get_latest_news())
            Speak("For your convenience, I am printing it on the screen sir.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            Speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            Speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            Speak(f"Also, the weather report talks about {weather}")
            Speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")