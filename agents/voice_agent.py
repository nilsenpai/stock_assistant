import speech_recognition as sr
import pyttsx3
import re
import os
import requests  # For calling Gemini API

# Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        print("Voice already speaking — skipped to prevent crash.")


def listen() -> str:
    """Listen from mic and return recognized text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand.")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return ""

def clean_markdown(text: str) -> str:
    """Remove Markdown syntax to improve speech output."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)  # code blocks
    text = re.sub(r"`([^`]*)`", r"\1", text)  # inline code
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)  # links
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*([^*]+)\*", r"\1", text)  # italic
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)  # headers
    text = re.sub(r"\n+", " ", text)  # newlines to space
    return text.strip()

def query_gemini_api(prompt: str) -> str:
    """
    Query Gemini API and return the text response.
    Make sure you set your GEMINI_API_KEY environment variable.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    url = "https://api.gemini.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gemini-2.0-flash",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    res_json = response.json()


    message_text = res_json["choices"][0]["message"]["content"]
    return message_text

def main():
    speak("Hello! I am your assistant. How can I help you?")
    while True:
        user_input = listen()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "stop"):
            speak("Goodbye!")
            break

        try:
            ai_response = query_gemini_api(user_input)
        except Exception as e:
            print(f"API Error: {e}")
            speak("Sorry, I had trouble connecting to the AI service.")
            continue

        print(f"Raw AI response:\n{ai_response}")
        cleaned = clean_ma_
