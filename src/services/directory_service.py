import uuid
from datetime import datetime
from pymongo.collection import Collection

from src.utils import logger, get_parent_path
from src.entities.user import User
from src.entities.directory import Dir, DirMetadata


class DirectoryService:
    # Properties inherited from SystemService
    user: User
    users_col: Collection

    def create_dir(self, name: str, dir_path: str) -> bool: 
        parent_path = get_parent_path(dir_path)
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

    def delete_dir(self, name: str): 
        pass

    def get_all_dir(self): 
        doc = self.users_col.find_one(
            {"id": self.user.id},
            {"directory": 1, "_id": 0}
        )
        return doc
    
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
            if get_parent_path(d.get("meta", {}).get("path", "")) == path
        ]
        return {"directory": children}

    def rename_dir(self, name: str): 
        pass
