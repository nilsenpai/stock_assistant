from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from gtts import gTTS
from playsound import playsound
import uuid
import speech_recognition as sr
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.query_gemini import query_gemini
from utils.clean_gemini_response import clean_response

# ---------------------- TTS (gTTS-based) ----------------------
def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        filename = f"temp_{uuid.uuid4().hex}.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        st.error(f"Error in speaking: {e}")

# ---------------------- Speech Recognition ----------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("Sorry, I didn't catch that.")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
    return ""


INVESTMENT_FILE = "user_data/investment.txt"

def save_investment_info(text):
    with open(INVESTMENT_FILE, "w") as f:
        f.write(text)

def load_investment_info():
    if os.path.exists(INVESTMENT_FILE):
        with open(INVESTMENT_FILE, "r") as f:
            return f.read()
    return ""


st.title("📈 Share-Market Assistant")

# Section to collect investment preferences
if not os.path.exists(INVESTMENT_FILE):
    st.subheader("📝 Tell me about your investment preferences")
    user_pref = st.text_area("Describe your risk tolerance, goals, preferred sectors, etc.")
    if st.button("Save Investment Info"):
        save_investment_info(user_pref)
        st.success("Saved! Now you can start chatting with your assistant.")
        st.session_state.spoken = False
        st.stop()
else:
    st.sidebar.success("Investment profile loaded ✅")
    investment_context = load_investment_info()

# Ask question by voice
if st.button("🎤 Start Listening"):
    st.session_state.spoken = False
    user_text = listen()

    if user_text:
        prompt = f"User Investment Info: {investment_context}\n\nUser Query: {user_text}"
        response = query_gemini(prompt)
        cleaned_response = clean_response(response)

        st.markdown(f"**Assistant:** {cleaned_response}")

        # Speak the response once
        if "spoken" not in st.session_state:
            st.session_state.spoken = False

        if not st.session_state.spoken:
            speak(cleaned_response)
            st.session_state.spoken = True


