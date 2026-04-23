"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from src.utils import logger
from src.entities.user import User
from src.services.directory_service import DirectoryService


class SystemService(
    DirectoryService # inherits Directory Service parent class
    ):
    """
    Main System Service that can be exposes on enpoints 
    and responsible to inherit all the sub services.
    """
    def __init__(self, user: User):
        # if no user info (user id) is provided 
        if not user:
            logger.error("No user provided in system service")
            raise ValueError("No user provided in system service")
        
        super().__init__(user) 


  