import streamlit as st
from dotenv import load_dotenv
import os
import requests
import re
import pyttsx3
import speech_recognition as sr

load_dotenv()

INVESTMENT_FILE = "user_data/investment.txt"

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Listening... Please speak now.")
            audio = r.listen(source, timeout=5)
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        st.warning(f"Voice input failed: {e}")
        return ""

def clean_markdown(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n+", " ", text)
