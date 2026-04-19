from typing import Dict, Any, Optional
import re
import uuid
from datetime import datetime

from src.database.core.mongodb_connection import MongoConnection
from src.utils import logger, get_username_from_email
from src.entities import File, User
from src.factory.metadata_provider import MetadataProvider


class MongoMetadataService(MetadataProvider):
    def __init__(self, user: User):
        self.user = user
        self.db = MongoConnection()
        self.users_col = self.db.get_users_collection()

        self.init_user_records()

    def init_user_records(self): 
        user_record = self.get_user_record(user_id=self.user.id)
        if not user_record:
            logger.warning(f"No user metadata found. Initializing new user profile for {self.user.email}")
            
            # Extract username from email safely, default if None
            if self.user.email: 
                self.user.name = get_username_from_email(self.user.email)
            else: 
                self.user.name = "Unknown User"
            
            timestamp = datetime.now()
            user_data = self.user.model_dump()
            
            # Initialize with a Root directory record to accommodate root-level files
            user_data["directory"] = [
                {
                    "id": str(uuid.uuid4()),
                    "name": "root",
                    "meta": {
                        "size": 0,
                        "created": timestamp,
                        "updated": timestamp,
                        "path": "/"
                    },
                    "data": [

                    ]
                }
            ]

            self.create_user(user_data=user_data)
            logger.info(f"Metadata user collection created for {self.user.email} - {self.user.id}")

        else: 
            self.user.name = user_record["name"]

    def get_user_record(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.users_col.find_one({"id": user_id})

    def create_user(self, user_data: Dict[str, Any]) -> None:
        self.users_col.insert_one(user_data)

    def add_directory(self, user_id: str, dir_data: Dict[str, Any]) -> bool:
        try:
            self.users_col.update_one(
                {"id": user_id},
                {"$push": {"directory": dir_data}}
            )
            return True
        except Exception as e:
            logger.error(f"Failed to add directory for user {user_id}: {str(e)}")
            return False

    def get_all_directories(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.users_col.find_one(
            {"id": user_id},
            {"directory": 1, "_id": 0}
        )

    def create_file_record(self, user_id: str, file: File, path: str) -> None: 
        self.users_col.update_one(
            {   
                "id": user_id, 
                "directory.meta.path": path
            }, 
            {
                "$push": {
                    "directory.$.data": file.model_dump()
                },
                # updating folder metadata
                "$set": {
                    "directory.$.meta.updated": file.meta.updated, 
                    "directory.$.meta.size": file.meta.size, 
                }
            }
        )

    def remove_directory(self, user_id: str, dir_path: str) -> None:
        try:
            logger.info(f"PATH: {dir_path}")

            # Check if any child directory exists
            child_dir = self.users_col.find_one({
                "id": user_id,
                "directory": {
                    "$elemMatch": {
                        "meta.path": {
                            "$regex": f"^{dir_path}/"
                        }
                    }
                }
            })


            if child_dir:
                logger.warning(f"Cannot delete {dir_path}: contains subdirectories")
                return False

            # Check if directory itself has files 
            dir_with_files = self.users_col.find_one({
                "id": user_id,
                "directory": {
                    "$elemMatch": {
                        "meta.path": dir_path,
                        "data.0": {"$exists": True}
                    }
                }
            })


            if dir_with_files:
                logger.warning(f"Cannot delete {dir_path}: contains files")
                return False

            # Delete directory (remove array element)
            result = self.users_col.update_one(
                {"id": user_id},
                {
                    "$pull": {
                        "directory": {
                            "meta.path": dir_path
                        }
                    }
                }
            )

            logger.info(f"Deleted {result.modified_count} directory for path {dir_path}")

            return result.modified_count > 0

        except Exception as e:
            logger.error(
                f"Failed to remove directory {dir_path} for user {user_id}: {str(e)}"
            )
            return False

    def remove_file_record(self, user_id: str, file_id: str) -> None:
        try:
            result = self.users_col.update_one(
                {"id": user_id},
                {"$pull": 
                    {"directory.$[].data": {"id": file_id}
                     }
                }
            )

            if result.modified_count == 0:
                logger.warning(f"File with id '{file_id}' not found via array filter, trying path fallback.")
                
        except Exception as e:
            logger.error(
                f"Failed to remove file record {file_id} for user {self.user.id}: {str(e)}"
            )
            raise