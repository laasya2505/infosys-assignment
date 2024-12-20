import google.generativeai as genai
from apikey import api_data
import pyttsx3
import speech_recognition as sr
import webbrowser

# Configure Gemini API
genai.configure(api_key=api_data)
model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
convo = model.start_chat()

# System message for voice assistant
system_message = '''INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE". 
SYSTEM MESSAGE: You are being used to power a voice assistant. As a voice assistant, use short sentences and directly respond to the prompt. Generate only words of value, prioritizing logic and facts.'''
convo.send_message(system_message)

# Initialize pyttsx3 for macOS
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

speak("Hello! How are you?")

# Function to get a reply from Gemini API
def Reply(question):
    try:
        response = convo.send_message(question)
        answer = response.text.strip()
        return answer
    except Exception as e:
        print("Error communicating with Gemini API:", e)
        return "Sorry, I couldn't process that."

# Function to take a voice command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}\n")
        except Exception as e:
            print("Could you say that again, please?")
            return "None"
        return query

# Main logic
if __name__ == '__main__':
    while True:
        query = takeCommand().lower()
        if query == "none":
            continue

        ans = Reply(query)
        print(ans)
        speak(ans)

        if 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
        elif 'bye' in query:
            speak("Goodbye! Have a great day!")
            break
