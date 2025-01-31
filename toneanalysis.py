import speech_recognition as sr
import pyttsx3
from transformers import pipeline

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speech rate

def speak(text):
    """
    Convert text to speech.
    """
    engine.say(text)
    engine.runAndWait()

def perform_intent_analysis(text):
    """
    Perform intent/emotion analysis on the given text.
    """
    try:
        intent_analyzer = pipeline(
            "text-classification", 
            model="j-hartmann/emotion-english-distilroberta-base"  # Emotion/intent model
        )
        result = intent_analyzer(text)
        return result
    except Exception as e:
        return f"Error in intent analysis: {e}"

def perform_tone_analysis(text):
    """
    Perform tone analysis on the given text.
    """
    try:
        tone_analyzer = pipeline(
            "text-classification", 
            model="bhadresh-savani/bert-base-uncased-emotion"  # Tone/emotion model
        )
        result = tone_analyzer(text)
        return result
    except Exception as e:
        return f"Error in tone analysis: {e}"

def perform_sentiment_analysis(text):
    """
    Perform sentiment analysis on the given text.
    """
    try:
        sentiment_analyzer = pipeline("sentiment-analysis")
        result = sentiment_analyzer(text)
        return result
    except Exception as e:
        return f"Error in sentiment analysis: {e}"

def recognize_speech():
    """
    Recognize speech from the microphone and convert it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak now!")
        speak("Listening... Please speak now!")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand your speech.")
            speak("Sorry, I couldn't understand your speech. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Speech Recognition service error: {e}")
            speak(f"Speech Recognition service error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            speak(f"Error: {e}")
            return None

def explain_results(result, analysis_type):
    """
    Generate an elaborate explanation of the results.
    """
    if isinstance(result, str):  # Handle errors
        return result

    top_result = result[0]
    label = top_result['label']
    score = top_result['score']

    if analysis_type == "intent":
        explanation = f"The intent of your statement is primarily categorized as '{label}' with a confidence score of {score:.2f}. This suggests that your words convey a sense of {label.lower()}."
    elif analysis_type == "tone":
        explanation = f"The tone of your statement is detected as '{label}' with a confidence score of {score:.2f}. This indicates that your tone reflects {label.lower()}."
    elif analysis_type == "sentiment":
        explanation = f"The sentiment of your statement is classified as '{label}' with a confidence score of {score:.2f}. This implies that your statement has a {label.lower()} sentiment."
    else:
        explanation = "Unknown analysis type."

    return explanation

def main():
    print("Welcome to Intent, Tone, and Sentiment Analysis!")
    speak("Welcome to Intent, Tone, and Sentiment Analysis!")
    print("Speak into the microphone to analyze intent, tone, and sentiment (say 'exit' to quit):")
    speak("Please speak into the microphone. Say 'exit' to quit.")

    while True:
        text = recognize_speech()
        if text is None:
            print("\nPlease try speaking again.\n")
            continue
        
        if text.lower() == "exit":
            print("Exiting... Thank you!")
            speak("Exiting. Thank you for using the program!")
            break

        # Intent Analysis
        print("\nPerforming Intent Analysis...")
        speak("Performing intent analysis.")
        intent_result = perform_intent_analysis(text)
        intent_explanation = explain_results(intent_result, "intent")
        print(intent_explanation)
        speak(intent_explanation)

        # Tone Analysis
        print("\nPerforming Tone Analysis...")
        speak("Performing tone analysis.")
        tone_result = perform_tone_analysis(text)
        tone_explanation = explain_results(tone_result, "tone")
        print(tone_explanation)
        speak(tone_explanation)

        # Sentiment Analysis
        print("\nPerforming Sentiment Analysis...")
        speak("Performing sentiment analysis.")
        sentiment_result = perform_sentiment_analysis(text)
        sentiment_explanation = explain_results(sentiment_result, "sentiment")
        print(sentiment_explanation)
        speak(sentiment_explanation)

        print("\n-------------------------------\n")
        speak("Analysis complete. You may speak your next statement.")

if __name__ == "__main__":
    main()
