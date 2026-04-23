"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from dotenv import load_dotenv
from src.logging import configure_logging
import os

load_dotenv()
logger = configure_logging(log_level="info")


# System Variable fetching  from .env file

mongodb_uri = os.getenv("MONGO_DB_URI", "")
mongodb_dbname = os.getenv("MONGO_DB_NAME")

firebase_api_key = os.getenv("FIREBASE_API_KEY", "")
firebase_authDomain = os.getenv("FIREBASE_AUTH_DOMAIN", "")
firebase_projectId = os.getenv("FIREBASE_PROJECT_ID", "")
firebase_storageBucket = os.getenv("FIREBASE_STORAGEBUCKET", "")
firebase_messagingSenderId = os.getenv("FIREBASE_MESSAGING_SENDER_ID", "")
firebase_appId = os.getenv("FIREBASE_APP_ID", "")
firebase_measurementId = os.getenv("FIREBASE_MEASUREMENT_ID", "")




azure_connection_string = os.getenv("AZURE_CONNECTION_STRING", "")


