import httpx
import os

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
print("🔑 Alpha Vantage API Key:", API_KEY)



async def fetch_price_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    try:
        daily = list(data["Time Series (Daily)"].items())[:6]
        daily_returns = []
        for i in range(1, 6):
            close_today = float(daily[i-1][1]['4. close'])
            close_prev = float(daily[i][1]['4. close'])
            daily_returns.append(round((close_today - close_prev)/close_prev, 4))
        return daily_returns[::-1]
    except:
        return [0, 0, 0, 0, 0]  # fallback
