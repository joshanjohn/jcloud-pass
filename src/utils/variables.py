from dotenv import load_dotenv
from src.logging import configure_logging

import os

load_dotenv()


mongodb_uri = os.getenv("MONGO_DB_URI", "")
mongodb_dbname = os.getenv("MONGO_DB_NAME")

firebase_api_key = os.getenv("FIREBASE_API_KEY")
logger = configure_logging(log_level="info")