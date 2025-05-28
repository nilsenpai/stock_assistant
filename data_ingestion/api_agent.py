# data_ingestion/api_agent.py

from fastapi import FastAPI, Query
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

# Initialize FastAPI app
app = FastAPI()

@app.get("/get_data/")
def get_data(
    ticker: str = Query(
        ...,  # Required
        examples={
            "example": {
                "summary": "Example Ticker",
                "description": "Enter the stock ticker symbol (e.g., GOOG for Google)",
                "value": "GOOG"
            }
        }
    )
):
    # --- Google Finance Section ---
    finance_params = {
        "engine": "google_finance",
        "q": f"{ticker}:NASDAQ",
        "api_key": API_KEY
    }
    finance_search = GoogleSearch(finance_params)
    finance_results = finance_search.get_dict()

    stock_info = finance_results.get("finance_results", {}).get("stocks", [{}])[0]

    # --- Google News Section ---
    news_params = {
        "engine": "google_news",
        "q": ticker,
        "gl": "us",
        "hl": "en",
        "api_key": API_KEY
    }
    news_search = GoogleSearch(news_params)
    news_results = news_search.get_dict()
    headlines = [item["title"] for item in news_results.get("news_results", [])[:5]]

    # --- Response ---
    return {
        "ticker": stock_info.get("symbol", ticker),
        "price": stock_info.get("price", "N/A"),
        "change": stock_info.get("change", "N/A"),
        "change_percent": stock_info.get("change_percentage", "N/A"),
        "headlines": headlines or ["No recent headlines found"]
    }

