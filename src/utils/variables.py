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
azure_connection_string = os.getenv("AZURE_CONNECTION_STRING", "")


