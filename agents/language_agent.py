# agents/language_agent.py

from fastapi import FastAPI, Body
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Initialize Gemini model (1.5 Flash)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

@app.post("/generate_summary/")
def generate_summary(data: dict = Body(...)):
    """
    Generate a market brief summary using Gemini 1.5 Flash.
    """
    # Prompt
    prompt = f"""
Generate a very short and in points market brief for a portfolio manager based on the following:

- Exposure to Asia tech: {data['exposure']}%
- Stock: {data['ticker']} at ${data['price']} ({data['change']} / {data['change_percent']})
- News sentiment: {data['sentiment_summary']}
- Top headlines:
"""

    for i, headline in enumerate(data['headlines'], start=1):
        prompt += f"\n  {i}. {headline}"

    prompt += "\n\nWrite the response in a professional tone, no more than 3 short sentences."

    # Generate response from Gemini
    response = model.generate_content(prompt)
    return {"summary": response.text.strip()}
