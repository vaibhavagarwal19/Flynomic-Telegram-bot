import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    BASE_API_URL = os.getenv("BASE_API_URL", "https://api.flynomic.com")
    FLYNOMIC_API_KEY = os.getenv("FLYNOMIC_API_KEY")
    WEBSITE_URL = os.getenv("WEBSITE_URL", "https://flynomic.com")
