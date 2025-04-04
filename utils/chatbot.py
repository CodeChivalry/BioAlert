import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load Gemini API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini chatbot function
def get_gemini_reply(prompt):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
