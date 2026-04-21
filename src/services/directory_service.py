import uuid
from datetime import datetime
from fastapi import UploadFile

from src.utils import logger, get_parent_path
from src.entities import Dir, Metadata, User, File
from src.services.mongodb_metadata_service import MongoMetadataService
from src.services.azure_storage_service import AzureStorageService

class DirectoryService:
    def __init__(self, user: User):
        self.user = user
    
        self.metadata_service = MongoMetadataService(user=user)
        self.storage_service = AzureStorageService(user_id=user.id)
    
    def get_user(self): 
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
        meta = Metadata(
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

    def delete_dir(self, name: str, dir_id: str, dir_path: str) -> bool: 
        logger.info(f"Deleting directory: {dir_path}")
        return self.metadata_service.remove_directory(user_id=self.user.id, dir_path=dir_path)

    def delete_file(self, file_id: str,  blob_name: str) -> bool:
        logger.info(f"Deleting file id:{file_id} ;blob name: {blob_name}")
        blob_name
        try:
            storage_success = self.storage_service.delete_file(blob_name)
            
            meta_success = self.metadata_service.remove_file_record(self.user.id, file_id)
            
            return storage_success and meta_success
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False

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



    def check_file_exists(self, filename: str, path: str) -> bool:
        """Helper to check if file exists in metadata."""
        return self.metadata_service.file_exists(self.user.id, filename, path)

    def upload_file(self, file: UploadFile, data: bytes, path: str, override: bool = False) -> bool: 

        # Build the full path
        clean_path = path.strip("/")
        logger.info(f"CLEAN PATH: {clean_path}")
        logger.info(f"PATH: {path}")

        full_path = ""
        if clean_path:
            full_path = f"{clean_path}/{file.filename}"
        else:
            full_path = file.filename
        
        # Check if file exists before proceeding if override is False
        if not override and self.check_file_exists(file.filename, path):
            raise Exception(f"FILE_EXISTS:{file.filename}")

        timestamp = datetime.now()
        
        meta = Metadata(
            size = file.size,
            created=timestamp,
            updated=timestamp,
            path=full_path
        )

        file_obj: File = File(
            id=str(uuid.uuid4()),
            name=file.filename,
            meta=meta
        )

        try: 
            if override:
                self.metadata_service.update_file_record(user_id=self.user.id, file=file_obj, path=path)
            else:
                self.metadata_service.create_file_record(user_id=self.user.id, file=file_obj, path=path)
                
            self.storage_service.upload_file(blob_name=full_path, file_data=data)
           
            return True
        except Exception as e: 
            logger.error(f"Error uploading file: {str(e)}")
            return False 
        


    def get_files_in_path(self, path: str):
        blobs = self.storage_service.list_dirs(path)
        
        # Get metadata from MongoDB for IDs
        doc = self.metadata_service.get_all_directories(self.user.id)
        if not doc or "directory" not in doc:
            logger.warning(f"No directory metadata found for user {self.user.id}")
            return blobs
            
        # Standardize path for matching
        lookup_path = path if path.startswith("/") else "/" + path
        if not lookup_path.endswith("/") and lookup_path != "/":
            pass # Keep as is

        folder_meta = next((d for d in doc["directory"] if d.get("meta", {}).get("path") == lookup_path), None)
        
        if not folder_meta or "data" not in folder_meta:
            logger.debug(f"No metadata entry for path: {lookup_path}")
            return blobs
            
        # Merge IDs into blobs
        id_map = { f["name"]: f["id"] for f in folder_meta["data"] if "name" in f and "id" in f }
        
        for b in blobs:
            b["id"] = id_map.get(b["name"], "")
            if not b["id"]:
                logger.warning(f"File {b['name']} in storage has no matching metadata ID in DB.")
            
        return blobs

    def download_file(self, full_path: str): 
        return self.storage_service.download_blob(full_path)