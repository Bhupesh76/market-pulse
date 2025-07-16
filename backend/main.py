# from fastapi import FastAPI, Query
# from services.news import fetch_news
# from services.price import fetch_price_data
# from utils.momentum import compute_momentum
# from llm import ask_llm
# from cache import cache_response
# from datetime import date

# app = FastAPI()

# @app.get("/api/v1/market-pulse")
# @cache_response(ttl=600)
# async def market_pulse(ticker: str = Query(..., min_length=1)):
#     try:
#         prices = await fetch_price_data(ticker)
#         print("✅ Prices fetched:", prices)

#         momentum_score = compute_momentum(prices)
#         print("📈 Momentum score calculated:", momentum_score)

#         news = await fetch_news(ticker)
#         print("📰 News headlines fetched:", news)

#         # ✅ Await the async LLM function
#         llm_result = await ask_llm(ticker, prices, news, momentum_score)
#         print("🤖 LLM Response:", llm_result)

#         return {
#             "ticker": ticker.upper(),
#             "as_of": str(date.today()),
#             "momentum": {"returns": prices, "score": momentum_score},
#             "news": news,
#             "pulse": llm_result["pulse"],
#             "llm_explanation": llm_result["explanation"]
#         }
#     except Exception as e:
#         print("🔥 ERROR:", e)
#         return {"error": str(e)}
from fastapi import FastAPI, Query
from services.news import fetch_news
from services.price import fetch_price_data
from utils.momentum import compute_momentum
from llm import ask_llm
from cache import cache_response
from datetime import date
import traceback  # ✅ for better error messages

app = FastAPI()

@app.get("/api/v1/market-pulse")
@cache_response(ttl=600)
async def market_pulse(ticker: str = Query(..., min_length=1)):
    try:
        # ✅ Fetch stock price data
        prices = await fetch_price_data(ticker)
        print("✅ Prices fetched:", prices)

        # ✅ Compute momentum score
        momentum_score = compute_momentum(prices)
        print("📈 Momentum score calculated:", momentum_score)

        # ✅ Fetch recent news
        news = await fetch_news(ticker)
        print("📰 News headlines fetched:", news)

        # ✅ Ask LLM (Gemini)
        llm_result = await ask_llm(ticker, prices, news, momentum_score)
        print("🤖 LLM Response:", llm_result)

        # ✅ Return formatted response
        return {
            "ticker": ticker.upper(),
            "as_of": str(date.today()),
            "momentum": {"returns": prices, "score": momentum_score},
            "news": news,
            "pulse": llm_result.get("pulse", "neutral"),
            "llm_explanation": llm_result.get("explanation", "No explanation provided")
        }

    except Exception as e:
        print("🔥 ERROR:\n", traceback.format_exc())  # ✅ print detailed traceback
        return {"error": str(e)}
