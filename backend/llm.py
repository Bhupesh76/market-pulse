# import os
# import json
# from dotenv import load_dotenv
# import google.generativeai as genai

# load_dotenv()

# # Configure Gemini API with your key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# print("🔑 Gemini API Key Loaded")

# # Use correct model
# model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# async def ask_llm(ticker, returns, news, score):
#     news_text = "\n".join([f"- {n['title']}: {n['description']}" for n in news])
#     prompt = f"""
# You are a stock analyst assistant.

# Given the 5-day returns: {returns} with momentum score {score},
# and the following headlines:
# {news_text}

# Answer:
# - What is the market pulse (bullish, neutral, bearish)?
# - Why (based on the returns and the news)?
# Return the result strictly as a JSON object:
# {{ "pulse": ..., "explanation": ... }}
# """

#     print("📤 Prompt to Gemini:\n", prompt)

#     try:
#         # ✅ Use async method to avoid blocking
#         response = await model.generate_content_async(prompt)
#         print("📥 Gemini Response:\n", response.text)
#         return json.loads(response.text)
#     except Exception as e:
#         print("🔥 LLM Error:", e)
#         return {"pulse": "neutral", "explanation": "LLM response could not be parsed"}

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing Gemini API Key!")

genai.configure(api_key=api_key)
print("🔑 Gemini API Key Loaded")

# ✅ Corrected model name
model = genai.GenerativeModel("gemini-1.5-pro-latest")

async def ask_llm(ticker, returns, news, score):
    news_text = "\n".join([f"- {n['title']}: {n['description']}" for n in news])
    prompt = f"""
You are a stock analyst assistant.

Given the 5-day returns: {returns} with momentum score {score},
and the following headlines:
{news_text}

Answer:
- What is the market pulse (bullish, neutral, bearish)?
- Why (based on the returns and the news)?
Return the result strictly as a JSON object:
{{ "pulse": ..., "explanation": ... }}
"""
    print("📤 Prompt to Gemini:\n", prompt)

    try:
        response = model.generate_content(prompt)
        print("📥 Gemini Response:\n", response.text)

        return json.loads(response.text)
    except Exception as e:
        return {
            "pulse": "neutral",
            "explanation": f"Gemini failed: {e}"
        }
