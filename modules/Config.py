import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
    GAS_WEBAPP_URL = os.getenv('GAS_WEBAPP_URL')
    REDIS_URL = os.getenv('REDIS_URL')