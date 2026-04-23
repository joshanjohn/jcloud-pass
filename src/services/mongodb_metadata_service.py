"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

import uuid
from typing import Dict, Any, Optional
from datetime import datetime

from src.database.core.mongodb_connection import MongoConnection
from src.utils import logger, get_username_from_email
from src.entities import File, User
from src.factory.metadata_provider import MetadataProvider


class MongoMetadataService(MetadataProvider):
    """
    This class implements metadata service interface for mongodb database.
    """
    def __init__(self, user: User):
        self.user = user

        # creating mongodb collection instance 
        self.db = MongoConnection()
        self.users_col = self.db.get_users_collection()

        self.init_user_records()

    def init_user_records(self): 
        """
        Method that checks if the user records are existing on 
        monogodb database if not they are created. 
        """

        # fetch information from mongodb for user 
        user_record = self.get_user_record(user_id=self.user.id)
        if not user_record:
            logger.warning(f"No user metadata found. Initializing new user profile for {self.user.email}")
            
            # Extract username from email and set as username 
            if self.user.email: 
                self.user.name = get_username_from_email(self.user.email)
            # if no email found then set name to unknown user
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
            # adding user data into mongodb 
            self.create_user(user_data=user_data)
            logger.info(f"Metadata user collection created for {self.user.email} - {self.user.id}")

        else: 
            self.user.name = user_record["name"]

    def get_user_record(self, user_id: str) -> Optional[Dict[str, Any]] | None:
        """
        Method to fetch the user information document from mongodb collections for 
        given user id. if not found return "None"
        """
        try: 
             return self.users_col.find_one({"id": user_id})
        except: 
            return None

    def create_user(self, user_data: Dict[str, Any]) -> None:
        """
        Method to create user record (user_data) into mongodb collections
        """
        self.users_col.insert_one(user_data)

    def add_directory(self, user_id: str, dir_data: Dict[str, Any]) -> bool:
        """
        Method to add a directory record into mongodb collection
        push the the dir_data document into directory collection. 
        
        Returns true for sucessfully entry, or it return false. 
        """
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
        """
        Method to fetch all directory Documents from mongodb database 
        for given user id. 
        """
        return self.users_col.find_one(
            {"id": user_id},
            {"directory": 1, "_id": 0} 
        )

    def create_file_record(self, user_id: str, file: File, path: str) -> None: 
        """
        Method to create single file record into the mogodb direcory data document 
        """
        self.users_col.update_one(
            {   
                "id": user_id, 
                "directory.meta.path": path
            }, 
            {
                 # adding file data
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

    def update_file_record(self, user_id: str, file: File, path: str) -> None:
        """
        Method to updates an existing file record by replacing it with new 
        metadata in mongodb database
        """
        # First remove the existing file record with the same name
        self.users_col.update_one(
            {
                "id": user_id,
                "directory.meta.path": path
            },
            {
                "$pull": {
                    "directory.$.data": {"name": file.name}
                }
            }
        )
        # Then add the new record
        self.create_file_record(user_id, file, path)

    def file_exists(self, user_id: str, filename: str, path: str) -> bool:
        """Method to checks if a file with the given name exists in the specified path 
        for the user. 
        
        Returns true if user file record finds, or return false. 
        """
        # fetching detials of filename name with path 
        user_record = self.users_col.find_one({
            "id": user_id,
            "directory": {
                "$elemMatch": {
                    "meta.path": path,
                    "data.name": filename
                }
            }
        })
        return user_record is not None

    def remove_directory(self, user_id: str, dir_path: str) -> None:
        """
        Method to remove directory record for given directory path and user id 
        from mongodb collections. Only delete is there is no child elements exist. 
        
        Raise exception on attempt to delete folder with files or folder contains inside. 
        """
        # Check if any child directory exists
        is_child_exists = self.users_col.find_one({
            "id": user_id,
            "directory": {
                "$elemMatch": {
                    "meta.path": {
                        "$regex": f"^{dir_path}/"
                    }
                }
            }
        })

        # raising exption if there is child 
        if is_child_exists:
            raise Exception(f"Cannot delete '{dir_path}': it contains subdirectories")

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
            msg = f"Cannot delete '{dir_path}': it contains files"
            logger.warning(msg)
            raise Exception(msg)

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

        if result.modified_count == 0:
            msg = f"Directory '{dir_path}' not found or already deleted"
            logger.warning(msg)
            raise Exception(msg)

        logger.info(f"Deleted directory for path {dir_path}")
        return True

    def remove_file_record(self, user_id: str, file_id: str) -> None:
        """
        Method to remove file records for given file id from mongodb direcotory data collection

        Raise exception when unable to perform deletion or no file record deleted. 
        """
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