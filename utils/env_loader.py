import os
from dotenv import load_dotenv

def load_env():
    # Load .env file
    load_dotenv()

    # Get Telegram API key
    API_KEY = os.getenv("TELEGRAM_API_KEY")

    # Validate API key
    if API_KEY is None:
        raise ValueError("Telegram API key not found.")

    return API_KEY
