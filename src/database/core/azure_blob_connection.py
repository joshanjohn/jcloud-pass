from azure.storage.blob import BlobServiceClient, ContainerClient
from src.utils import azure_connection_string, logger

class AzureBlobConnection: 
    def __init__(self):
        """
        Initializes a fresh connection to the Azure Blob Service.
        """
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
            logger.info("Connected to Azure Blob Service Client.")
        except Exception as e: 
            logger.error(f"Unable to connect to Azure: {e}")
            raise

    def get_user_container(self, user_id: str) -> ContainerClient:
        """
        Fetches or creates a container specifically for the given user_id.
        """
        # Azure rules: Must be lowercase and no underscores
        container_name = user_id.lower().replace("_", "-")
        
        container_client = self.blob_service_client.get_container_client(container_name)

        try:
            # Check if exists, if not, create it
            if not container_client.exists():
                container_client.create_container()
                logger.info(f"Created new container for user: {container_name}")
            else:
                logger.info(f"Using existing container for user: {container_name}")
                
            return container_client
            
        except Exception as e:
            logger.error(f"Error accessing container {container_name}: {e}")
            raise