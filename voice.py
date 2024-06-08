import speech_recognition as sr
import pyttsx3
import wikipedia
import requests
from googlesearch import search
from bs4 import BeautifulSoup

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """Listen for audio and convert it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            speak("Sorry, my speech service is down.")
            return None

def get_weather(city):
    """Get the current weather for a city."""
    api_key = "f4d0bb8f57f9d1a424faffea63fc8388"  # Replace with your OpenWeather API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather_description = data['weather'][0]['description']
        temperature = main['temp']
        weather_report = f"The weather in {city} is {weather_description} with a temperature of {temperature} degrees Celsius."
        return weather_report
    else:
        return "Sorry, I couldn't retrieve the weather information right now."

def get_summary(topic):
    """Get a summary from Wikipedia for a given topic."""
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"There are multiple results for {topic}. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any information on that topic."

def get_google_results(query):
    """Get the top Google search results for a query."""
    try:
        search_results = search(query, num=5, stop=5, pause=2)
        results = []
        for url in search_results:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else url
            results.append(f"Title: {title}\nURL: {url}")
        return "\n\n".join(results)
    except Exception as e:
        return f"Sorry, I couldn't perform the search. Error: {str(e)}"

def main():
    speak("Hello, how can I help you today?")
    while True:
        command = listen()
        if command:
            if "exit" in command or "bye" in command:
                speak("Goodbye!")
                break
            elif "hello" in command:
                speak("Hello! How are you?")
            elif "your name" in command:
                speak("I am your voice assistant.")
            elif "weather" in command:
                speak("Sure, please tell me the city name.")
                city = listen()
                if city:
                    weather_report = get_weather(city)
                    speak(weather_report)
            elif "tell me about" in command:
                topic = command.replace("tell me about", "").strip()
                summary = get_summary(topic)
                speak(summary)
            elif "search for" in command:
                query = command.replace("search for", "").strip()
                results = get_google_results(query)
                speak("Here are the top results I found.")
                speak(results)
            else:
                speak("I did not understand that. Can you please repeat?")

if __name__ == "__main__":
    main()
