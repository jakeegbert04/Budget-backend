from google import genai
import os

gemini_client = None
api_key = os.getenv('GEMINI_API_KEY')

def init_gemini(app):
    """Initialize Gemini with Flask app"""
    global gemini_client
    gemini_client = genai.Client(api_key=api_key)
    return gemini_client

def get_gemini_client():
    """Get the initialized Gemini client"""
    if gemini_client is None:
        raise RuntimeError("Gemini not initialized. Call init_gemini() first.")
    return gemini_client