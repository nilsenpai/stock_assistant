from fastapi import FastAPI, Body
from transformers import pipeline

app = FastAPI()

# Load sentiment model once at startup
classifier = pipeline("sentiment-analysis")

@app.post("/analyze_sentiment/")
def analyze_sentiment(headlines: list = Body(...)):
    """
    Takes a list of headlines and returns sentiment analysis results.
    """
    results = classifier(headlines)
    return {"results": results}
