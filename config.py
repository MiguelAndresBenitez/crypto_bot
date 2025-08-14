from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

TELEGRAM_TOKEN = TOKEN
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
