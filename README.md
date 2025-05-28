# 📈 Voice-Based Investment Assistant

A smart, voice-controlled assistant that helps users make better investment decisions based on their individual preferences. Built with **Streamlit**, **Gemini API**, and **speech recognition**, this app enables natural, spoken interaction and delivers personalized financial insights.

---

## 🚀 Features

- 🎤 Voice-based input and output
- 🧠 AI-powered responses using Gemini 2.0
- 💬 Text and audio feedback (gTTS)
- 🧾 User investment profile saving and loading
- 🛑 Control buttons to stop listening/speaking
- 🪄 Cleaned summaries for visual vs. voice output

---

## 🛠️ Tech Stack

- Python 3.10+
- Streamlit
- Gemini API (via Google Generative AI)
- `speech_recognition` for voice input
- `gTTS` + `playsound` for text-to-speech
- `.env` for secure API key management

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/voice-investment-assistant.git
   cd voice-investment-assistant

## Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate   # On Windows

## Install dependencies:
pip install -r requirements.txt

## Create a .env file in the root folder:
GEMINI_API_KEY=your_actual_api_key
