from pymongo.collation import Collation

from src.utils.variables import logger
from src.database.core.mongodb_connection import MongoConnection
from src.entities.user import User


class SystemService: 
   

    def __init__(self, user: User):
        mongodb_instance = MongoConnection()
        self.user_col: Collation = mongodb_instance.get_user_collection()

        
        if not user:
            logger.error("No user provided in system service")
            raise ValueError("No user provided in system service")

        self.user = user

        self.init_system()
       

    def init_system(self):
        # Try to find user
        doc = self.user_col.find_one({"id": self.user.id})

        if not doc:
            logger.info("No document found in MongoDB for user")

            # Ensure directory exists when creating
            user_data = self.user.model_dump()
            user_data["directory"] = []

            self.user_col.insert_one(user_data)
            logger.info(f"Mongodb user collection initiated for {self.user.name}")
            return

        logger.info(f"User Collection found for {self.user.name}")

    # create dir 
    def create_dir(self, name: str): 
        pass

    # remove dir 
    def delete_dir(self, name: str): 
        pass

    # get all dir 
    def get_all_dir(self): 
        doc = self.user_col.find_one(
            {"id": self.user.id},
            {"directory": 1, "_id": 0}
        )
        return doc 

    # rename dir 
    def rename_dir(self, name: str): 
        pass

    # rename user 
    def rename_user(self, name: str): 
        pass

