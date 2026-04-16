from src.database.core.azure_blob_connection import AzureBlobConnection
from src.utils import logger
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
