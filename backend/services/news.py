import httpx
import os

from dotenv import load_dotenv
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
print("🔑 News API Key:", NEWS_API_KEY)


async def fetch_news(ticker: str):
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    return [{"title": a["title"], "description": a["description"], "url": a["url"]} for a in data.get("articles", [])[:5]]