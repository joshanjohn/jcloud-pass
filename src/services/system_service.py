from pymongo.collection import Collection

from src.utils import logger, get_username_from_email
from src.database.core.mongodb_connection import MongoConnection
from src.entities.user import User

from src.services.directory_service import DirectoryService

class SystemService(DirectoryService):
   

    def __init__(self, user: User):

        # if no user info (user id) is provided 
        if not user:
            logger.error("No user provided in system service")
            raise ValueError("No user provided in system service")
       
        self.user: User = user

        mongodb_instance = MongoConnection()
        self.users_col: Collection = mongodb_instance.get_users_collection()

        self.init_system()

       
    def init_system(self):
        # Try to find user
        doc = self.users_col.find_one({"id": self.user.id})
        if not doc:
            # creating user document in database 
            logger.info("No document found in MongoDB for user")
            # set username as email domain initially. 
            self.user.name = get_username_from_email(self.user.email)
            user_data = self.user.model_dump()
            user_data["directory"] = []

            self.users_col.insert_one(user_data)
            logger.info(f"Mongodb user collection initiated for {self.user.name} - {self.user.email}")
            return
        # update name from fetched doc 
        self.user.name = doc["name"]
        logger.info(f"User Collection found for {self.user.name} - {self.user.email}")


    def get_current_user(self) -> User: 
        return self.user

    def rename_user(self, name: str): 
        pass

