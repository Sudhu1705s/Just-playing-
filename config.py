import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # Database configuration
    MONGO_DB_URI = os.getenv("MONGO_DB_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "Cluster0")

    # Other configurations
    OWNER_ID = [int(x) for x in os.getenv("OWNER_ID", "").split()]
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1001234567890"))