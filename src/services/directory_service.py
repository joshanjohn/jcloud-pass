import uuid
from datetime import datetime

from src.utils import logger, get_parent_path
from src.entities.user import User
from src.entities.directory import Dir, DirMetadata
from src.services.mongodb_metadata_service import MongoMetadataService
from src.services.azure_storage_service import AzureStorageService

class DirectoryService:
    def __init__(self, user: User):
        self.user = user
    
        self.metadata_service = MongoMetadataService(user=user)
        self.storage_service = AzureStorageService(user_id=user.id)
    
    def get_user(self): 
        logger.info(f"UPDATED USER (from dict service) : {self.user.model_dump()}")
        return self.user

    def create_dir(self, name: str, dir_path: str) -> bool: 
        parent_path = get_parent_path(dir_path)
        logger.info(f"PARENT PATH={parent_path}")
        
        existing_dirs = self.get_dirs_in_path(parent_path)
        
        # Check for duplicates in the target parent path
        for d in existing_dirs.get("directory", []):
            if d.get("name", "").lower() == name.lower():
                raise Exception(f"A folder named '{name}' already exists in this location.")

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
        
        # Update via MetadataService
        try:
            success = self.metadata_service.add_directory(self.user.id, new_dir.model_dump())
            if success:
                logger.info(f"Directory '{name}' created for user {self.user.name}")
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Failed to create directory '{name}' for user {self.user.name}: {str(e)}")
            return False

    def delete_dir(self, name: str): 
        pass

    def get_all_dir(self): 
        doc = self.metadata_service.get_all_directories(self.user.id)
        return doc
    
    def get_dirs_in_path(self, path: str):
        """Returns directories whose immediate parent is the given path."""
        doc = self.metadata_service.get_all_directories(self.user.id)
        if not doc or "directory" not in doc:
            return {"directory": []}

        children = [
            d for d in doc["directory"]
            if get_parent_path(d.get("meta", {}).get("path", "")) == path
        ]
        return {"directory": children}

    def rename_dir(self, name: str): 
        pass
