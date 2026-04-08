from dotenv import load_dotenv
import os

load_dotenv()


mongodb_uri = os.getenv("MONGO_DB_URI", "")
mongodb_dbname = os.getenv("MONGO_DB_NAME")

firebase_api_key = os.getenv("FIREBASE_API_KEY")



