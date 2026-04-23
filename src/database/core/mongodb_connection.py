"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from pymongo.server_api import ServerApi
from src.utils import mongodb_uri, mongodb_dbname, logger



class MongoConnection: 
    # signleton variables 
    _instance = None
    _initialized = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
        return cls._instance
    

    def __init__(self):
        # check if mongodb connection initialized already 
        if MongoConnection._initialized:
            return
        try: 
            self.client: MongoClient = MongoClient(mongodb_uri, server_api=ServerApi('1'))
            # try pining 
            self.client.admin.command('ping')
            logger.info("You successfully connected to MongoDB!")
            MongoConnection._initialized = True
        except Exception as e: 
            logger.error("Unable to connect to Mongodb")
            logger.error(str(e))


    def get_users_collection(self) -> Collection: 
        """
        method to return the user collection from mongodb instance 
        """
        if hasattr(self, '_users_coll_cache') and self._users_coll_cache is not None:
            return self._users_coll_cache

        db_list = self.client.list_database_names() # listing all database name 
        # checking if mongodb_name is in database, if not create it 
        if mongodb_dbname not in db_list:  
            logger.info("Creating mongodb system's db")  
            db =  self.client[mongodb_dbname]
            db.create_collection("users")
            self._users_coll_cache = db
            return db
            
        self._users_coll_cache = self.client[mongodb_dbname]["users"]
        return self._users_coll_cache
        



