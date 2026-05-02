from datetime import datetime
import webbrowser
import requests   # needed for weather & location API
import speech_recognition as sr
import pyttsx3
# form ddtrace.bootstrap.sitecustomize import source

weather_api_key = "ade82c3127b942e563833104d11c6008"
# Corpus
greet_messages = ["hi","hello","hey","hey there"]
date_msgs = ["what's the date","date",'tell me date',"today's date"]
time_msgs = ["what's the time","time",'tell me time',"today's time"]
news_intent=["tell me news","news","headlines"]

engine=pyttsx3.init()
engine.setProperty("rate",170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    rec=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=rec.listen(source)
    try:
        query=rec.recognize_google(audio)
        print("Your Query:",query)
        return query.lower()
    except BaseException as ex:
        print("Can't catch that...")

def get_news():
    api_key = "b6f8dbfc419440ca83d8068dd0acabb8"
    news_url = f"={api_key}"
    response=requests.get(news_url)
    data=response.json()
    articles=data['articles']
    total_articles=len(articles)
    for i in range (total_articles):
        print(f"Headline{i+1}:{articles[i]['title']}")

chat = True
while chat:
    msg=listen()
    # msg = input("Enter the message : ").lower()

    if msg in greet_messages:
        print("Hello, how are you?")

    elif msg in date_msgs:
        print(datetime.now().date())

    elif msg in time_msgs:
        current_time = datetime.now().time()
        print(current_time.strftime("%I:%M:%S"))

    elif msg == "bye":
        chat = False

    elif "open" in msg:
        site = msg.split("open ")[-1]
        url = f"https://www.{site}.com"
        webbrowser.open(url)
        print(f"opening {site}...")

    elif "calculate" in msg:
        cal = msg.split()[-1]
        answer = eval(cal)
        print(answer)

    # 🔥 WEATHER AUTO-LOCATION (ADDED ONLY)
    elif "weather" in msg or "temperature" in msg:
        try:
            # get location from IP
            loc = requests.get("http://ip-api.com/json").json()
            lat = loc["lat"]
            lon = loc["lon"]
            city = loc["city"]

            # get weather
            url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
            )
            data = requests.get(url).json()

            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]

            print(f"📍 Location: {city}")
            print(f"🌤 Weather: {desc}")
            print(f"🌡 Temperature: {temp}°C")

        except:
            print("Unable to fetch weather ❌")

    else:
        print("I can't understand.")