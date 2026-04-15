from azure.storage.blob import BlobServiceClient
from src.utils import azure_connection_string, azure_blob_container_name, logger


class AzureBlobConnection: 
    __instance = None
    _initialized = None

    def __new__(cls): 
        if cls.__instance is None: 
            cls.__instance = super(AzureBlobConnection, cls).__new__(cls)
        return cls.__instance
    

    def __init__(self):
        if AzureBlobConnection._initialized: 
            return 

        try:
            self.blob_client =  BlobServiceClient.from_connection_string(azure_connection_string)
            logger.info("Connected to Azure Blob Client.")
        except Exception as e: 
            logger.error("Unable to connect to Azure Blob Client: ", str(e) )


    def get_root_container_client(self): 
        self.container_client = self.blob_client.get_container_client(
            container=azure_blob_container_name
        )

        if not self.container_client.exists(): 
            self.init_container()
        else: 
            logger.info(f"Blob Container {azure_blob_container_name} already exist.")
        return self.container_client

    def init_container(self): 
        try: 
            self.blob_client.create_container(azure_blob_container_name)
            logger.info(f"Created blob container {azure_blob_container_name}.")
            self.container_client = self.blob_client.get_container_client(
                container=azure_blob_container_name
            )
        except Exception as e: 
            logger.error(f"Error on creating blob container {azure_blob_container_name} : ", str(e))



if __name__ == "__main__": 
    conn = AzureBlobConnection()
    client = conn.get_root_container_client()
