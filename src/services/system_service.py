from src.utils import logger, get_username_from_email
from src.entities.user import User
from src.services.azure_storage_service import AzureStorageService
from src.services.directory_service import DirectoryService


class SystemService(DirectoryService):


    def __init__(self, user: User):
        # if no user info (user id) is provided 
        if not user:
            logger.error("No user provided in system service")
            raise ValueError("No user provided in system service")

        super().__init__(user) 


  