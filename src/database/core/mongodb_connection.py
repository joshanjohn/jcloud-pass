from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from pymongo.server_api import ServerApi
from src.utils.variables import mongodb_uri, mongodb_dbname
import logging


class MongoConnection: 
    _instance = None
    _initialized = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
        return cls._instance
    

    def __init__(self):
        if MongoConnection._initialized:
            return
        try: 
            self.client: MongoClient = MongoClient(mongodb_uri, server_api=ServerApi('1'))
            self.client.admin.command('ping')
            logging.info("You successfully connected to MongoDB!")
            MongoConnection._initialized = True
        except Exception as e: 
            logging.error("Unable to connect to Mongodb")
            logging.error(str(e))


    def get_user_collection(self) -> Coll: 
        db_list = self.client.list_database_names()
        if mongodb_dbname not in db_list:  
            logging.info("Creating mongodb system's db")  
            db =  self.client[mongodb_dbname]
            db.create_collection("users")
            return db
        return self.client[mongodb_dbname]["users"]
        



