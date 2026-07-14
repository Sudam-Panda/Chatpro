# ===================================================
# app/ai.py
# Google Gemini AI Assistant
# ===================================================

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# ---------------------------------------------------
# Gemini Client
# ---------------------------------------------------

client = genai.Client(api_key=API_KEY)

# ---------------------------------------------------
# Gemini Model
# ---------------------------------------------------

MODEL_NAME = "gemini-3.5-flash"

# Other working models:
# MODEL_NAME = "gemini-flash-latest"
# MODEL_NAME = "gemini-3.1-flash-lite"
# MODEL_NAME = "gemini-2.5-flash"

# ---------------------------------------------------
# AI Response
# ---------------------------------------------------

def get_ai_response(question: str) -> str:

    try:

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=question,

            config=types.GenerateContentConfig(

                temperature=0.7,

                top_p=0.95,

                max_output_tokens=2048,

                 system_instruction="""
You are FlaskChatPro AI Assistant.

Rules:
- Answer naturally like ChatGPT or Gemini.
- Give accurate and detailed answers.
- If the user asks a simple question, give a short answer.
- If the user asks for code, provide complete working code.
- Format code using Markdown.
- Use bullet points when useful.
- Answer questions about:
  • Programming
  • Python
  • Flask
  • Django
  • HTML
  • CSS
  • JavaScript
  • React
  • Node.js
  • SQL
  • AI
  • General knowledge
  • Mathematics
  • Science
- For currency conversions, calculations, weather, and current information, clearly mention if the value is approximate unless live data is available.
- Be friendly and professional.
"""

            )

        )

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        if hasattr(response, "candidates"):
            try:
                return (
                    response.candidates[0]
                    .content.parts[0]
                    .text
                )
            except Exception:
                pass

        return "No response generated."

    except Exception as e:

        print("Gemini Error:", e)

        return "Sorry, AI is currently unavailable."