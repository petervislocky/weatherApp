import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Ensure WEATHER_API_KEY is set in your environment")