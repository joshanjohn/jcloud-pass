from pymongo.collection import Collection
import uuid

from datetime import datetime
from src.utils.variables import logger
from src.utils.helper import get_username_from_email
from src.database.core.mongodb_connection import MongoConnection
from src.entities.user import User
from src.entities.directory import Dir, DirMetadata


class SystemService(Dire): 
   

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

    
    # create dir 
    def create_dir(self, name: str, dir_path: str): 
        # Create metadata
        timestamp = datetime.now()
        meta = DirMetadata(
            size = 0,
            created=timestamp,
            updated=timestamp,
            path=dir_path
        )
        
        # Generate a unique ID 
        dir_id = str(uuid.uuid4())
        
        # Create directory object
        new_dir = Dir(
            id=dir_id,
            name=name,
            meta=meta, 
            data=[]
        )
        
        # Update MongoDB
        try:
            self.users_col.update_one(
                {"id": self.user.id},
                {"$push": {"directory": new_dir.model_dump()}}
            )
            logger.info(f"Directory '{name}' created for user {self.user.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create directory '{name}' for user {self.user.name}: {str(e)}")
            return False

    # remove dir 
    def delete_dir(self, name: str): 
        pass

    # get all dir 
    def get_all_dir(self): 
        doc = self.users_col.find_one(
            {"id": self.user.id},
            {"directory": 1, "_id": 0}
        )
        return doc

    def _parent_path(self, dir_path: str) -> str:
        """Returns the parent path of a directory path string."""
        parts = dir_path.rsplit("/", 1)
        # parts[0] is empty string for root-level paths like '/docs'
        return parts[0] if len(parts) == 2 and parts[0] else "/"

    # get dirs in a specific path
    def get_dirs_in_path(self, path: str):
        """Returns directories whose immediate parent is the given path."""
        doc = self.users_col.find_one(
            {"id": self.user.id},
            {"directory": 1, "_id": 0}
        )
        if not doc or "directory" not in doc:
            return {"directory": []}

        children = [
            d for d in doc["directory"]
            if self._parent_path(d.get("meta", {}).get("path", "")) == path
        ]
        return {"directory": children}

    # rename dir 
    def rename_dir(self, name: str): 
        pass

    # rename user 
    def rename_user(self, name: str): 
        pass

