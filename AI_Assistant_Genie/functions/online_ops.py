
import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

def Get_Ip_Address():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def Search_On_Wikipedia(keyword):
    results = wikipedia.summary(keyword, auto_suggest=False, sentences=4)
    return results

def Search_YouTube(video):
    kit.playonyt(video)

def Google_Search(query):
    kit.search(query)

def Get_News():
    NEWS_API_KEY = config("NEWS_API_KEY")
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]

OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
def Get_Weather(CITY):
    CITY = config("CITY")
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']