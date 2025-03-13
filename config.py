import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración del bot
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

MANYCHAT_API_KEY = os.getenv("MANYCHAT_API_KEY")

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")