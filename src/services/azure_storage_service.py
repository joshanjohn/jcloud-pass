from collections import defaultdict
import hashlib
from src.database.core.azure_blob_connection import AzureBlobConnection
from src.utils import logger
from typing import Iterator, List, Dict, Any
from src.factory.storage_provider import StorageProvider

class AzureStorageService(StorageProvider):
    def __init__(self, user_id: str):
        self.conn = AzureBlobConnection()
        self.container_client = self.conn.get_user_container(user_id)

    def upload_file(self, blob_name: str, file_data: bytes) -> bool:
        try:
            blob_client = self.container_client.get_blob_client(blob=blob_name)
            blob_client.upload_blob(file_data, overwrite=True)
            logger.info(f"Successfully uploaded {blob_name} to Azure Blob")
            return True
        except Exception as e:
            logger.error(f"Failed to upload {blob_name} to Azure Blob: {str(e)}")
            return False

    def download_file(self, blob_name: str) -> bytes:
        try:
            blob_client = self.container_client.get_blob_client(blob=blob_name)
            return blob_client.download_blob().readall()
        except Exception as e:
            logger.error(f"Failed to download {blob_name} from Azure Blob: {str(e)}")
            return b""

    def delete_file(self, blob_name: str) -> bool:
        try:
            blob_client = self.container_client.get_blob_client(blob=blob_name)
            blob_client.delete_blob()
            logger.info(f"Successfully deleted {blob_name} from Azure Blob")
            return True
        except Exception as e:
            logger.error(f"Failed to delete {blob_name} from Azure Blob: {str(e)}")
            return False

    def list_dirs(self, dir_path: str) -> list:
        try:
            # Azure Blob prefix needs trailing slash if querying inside a directory to prevent partial prefix matches
            prefix = dir_path.lstrip("/")
            if prefix and not prefix.endswith("/"):
                prefix += "/"
                
            blobs_iter = self.container_client.list_blobs(name_starts_with=prefix)
            blobs_list = []
            for blob in blobs_iter:
                # Ensure the blob is an immediate child of the current directory prefix
                # If there are any extra slashes after the prefix, it's in a subdirectory
                remainder = blob.name[len(prefix):]
                if "/" in remainder:
                    continue  # Skip blobs in subdirectories
                    
                blobs_list.append({
                    "name": remainder,
                    "path": blob.name,
                    "size": blob.size,
                    "last_modified": blob.last_modified
                })
            return blobs_list
        except Exception as e:
            logger.error(f"Failed to list blobs for {dir_path} in Azure Blob: {str(e)}")
            return []

    def download_blob(self, blob_name: str) -> Iterator[bytes]:
        try:
            blob_name = blob_name.lstrip("/")
            blob_client = self.container_client.get_blob_client(blob=blob_name)
            return blob_client.download_blob().chunks()
        except Exception as e:
            logger.error(f"Failed to stream {blob_name} from Azure Blob: {str(e)}")
            return None


    def duplicated_blob(self) -> List[Dict[str, Any]]:
        """
            Azure service to find the duplicated blob for signed user using md5 hash of each blob 
            and return the group of duplicated blob values.
        """
        try:
            blobs_iter = self.container_client.list_blobs(include=["metadata"])
            
            groups: Dict[str, list] = defaultdict(list) 

            for blob in blobs_iter:
                filename = blob.name.split("/")[-1]

                # Fetch full blob properties to read content_settings.content_md5
                blob_client = self.container_client.get_blob_client(blob=blob.name)
                props = blob_client.get_blob_properties()


                # retrive content_md5 hash, if not found set to None
                stored_md5 = (
                    props.content_settings.content_md5
                    if props.content_settings
                    else None
                )

                if stored_md5:
                    # if hash is in binary format the convert to string 
                    content_hash = (
                        stored_md5.hex() # convert hex string
                        if isinstance(stored_md5, (bytes, bytearray))
                        else str(stored_md5)
                    )
                else:
                    # Fallback: download blob and compute SHA-256 locally
                    logger.debug(
                        f"No stored MD5 for '{blob.name}', downloading to compute hash."
                    )
                
                # cretaing grpup of duplicated for same hash 
                groups[content_hash].append({
                    "name": filename,
                    "path": blob.name,
                    "size": blob.size,
                    "last_modified": blob.last_modified,
                    "content_hash": content_hash,
                })

            duplicates = [
                entry
                for members in groups.values()
                if len(members) > 1
                for entry in members
            ]
            return duplicates
        except Exception as e:
            logger.error(f"Failed to find duplicate blobs: {str(e)}")
            return []